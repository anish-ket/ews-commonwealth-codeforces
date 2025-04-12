import json
import pandas as pd
import spacy
import numpy as np
import pymongo
import ssl
import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from sentence_transformers import SentenceTransformer
from datetime import datetime, timezone
from sklearn.cluster import AgglomerativeClustering

# Load spaCy model for NER
nlp = spacy.load("en_core_web_sm")

# Load SentenceTransformer model
print("Loading SentenceTransformer model...")
model = SentenceTransformer('pauhidalgoo/finetuned-sts-ca-mpnet-base')
print("Model loaded successfully!")

# MongoDB connection details (keep password secure in production)
MONGO_URI = "mongodb+srv://parthdesai635:<parth0301>@ewd.azvnj.mongodb.net/?retryWrites=true&w=majority&appName=EWD"
DATABASE_NAME = "NewsDB"
COLLECTION_NAME = "News1"

# Configurable parameters
CLUSTERING_DISTANCE = 0.35    # Distance threshold for hierarchical clustering - lower value creates more clusters

# Load dataset
with open("filtered_news_articles.json", "r") as f:
    news_data = json.load(f)

df = pd.DataFrame(news_data)

# Ensure necessary columns exist
def safe_get(col):
    return df[col] if col in df.columns else ""
df["source_country"] = safe_get("source_country")
df["news_type"] = safe_get("news_type")
df["countries_mentioned"] = safe_get("countries_mentioned")
df["source"] = safe_get("source")
df["content"] = safe_get("content")
df.fillna("", inplace=True)

# Extract entities for severity calculation (used internally, not stored in output)
def extract_ner_entities(text):
    text = str(text)
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PERSON", "GPE", "LOC", "EVENT"]:
            # Assign higher weights to important entity types
            if ent.label_ in ["EVENT", "GPE"]:
                weight = 0.05
            else:
                weight = 0.03
            entities[ent.text.lower()] = weight
    return entities

# Extract entities but don't include in final output
df["_ner_entities"] = (df["title"] + " " + df["description"]).apply(extract_ner_entities)

# Convert published_date to datetime with consistent timezone handling
df["published_date"] = pd.to_datetime(df["published_date"], errors="coerce", utc=True)
df.dropna(subset=["published_date"], inplace=True)
df.reset_index(drop=True, inplace=True)

# Get article embeddings using SentenceTransformer (used internally, not stored in output)
print("Computing article embeddings...")
article_texts = [f"{title} {desc}" for title, desc in zip(df["title"], df["description"])]
embeddings = model.encode(article_texts, normalize_embeddings=True)
print(f"Generated embeddings shape: {embeddings.shape}")

# Group articles by news_type for better clustering
print("Grouping articles by news type...")
news_types = df["news_type"].unique()
print(f"Found {len(news_types)} different news types: {', '.join(news_types)}")

all_cluster_labels = []
next_cluster_id = 0

# Process each news type separately
for news_type in news_types:
    print(f"Processing news_type: {news_type}")
    mask = df["news_type"] == news_type
    type_indices = df[mask].index.tolist()
    
    if len(type_indices) <= 1:
        # If only one article of this type, assign unique cluster
        print(f"Only one article found for {news_type}, assigning unique cluster.")
        for idx in type_indices:
            all_cluster_labels.append(next_cluster_id)
            next_cluster_id += 1
        continue
        
    # Get embeddings for this news type
    type_embeddings = embeddings[type_indices]
    
    # Calculate distance between embeddings (1 - cosine_similarity)
    distance_matrix = 1 - np.dot(type_embeddings, type_embeddings.T)
    np.fill_diagonal(distance_matrix, 0)  # Ensure zero self-distance
    
    # Ensure distance matrix is valid
    distance_matrix = np.maximum(distance_matrix, 0)  # Ensure no negative distances
    
    # Use hierarchical clustering
    clustering = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=CLUSTERING_DISTANCE,
        metric='precomputed',
        linkage='average'
    )
    
    type_cluster_labels = clustering.fit_predict(distance_matrix)
    print(f"Created {len(set(type_cluster_labels))} clusters for {news_type}")
    
    # Remap cluster IDs to ensure uniqueness across types
    for label in type_cluster_labels:
        all_cluster_labels.append(label + next_cluster_id)
    
    next_cluster_id += max(type_cluster_labels) + 1 if len(type_cluster_labels) > 0 else 1

# Verify clustering results
print(f"Total clusters created: {len(set(all_cluster_labels))}")

# Function to calculate severity score
def calculate_severity(event):
    """Calculate event severity based on multiple factors"""
    if not event["articles"]:
        return 0.0
    
    severity_score = 0.0
    total_entities = 0
    important_keywords = [
        "crisis", "war", "death", "killed", "attack", "disaster", 
        "emergency", "conflict", "pandemic", "catastrophe"
    ]
    
    # Count articles by source credibility
    high_credibility_sources = ["Times of India", "NDTV", "The Hindu", "BBC", "CNN", "The Guardian"]
    credible_article_count = sum(1 for article in event["articles"] 
                             if article["source"] in high_credibility_sources)
    
    # Calculate article freshness factor (higher weight for newer articles)
    now = datetime.now(timezone.utc)  # Use timezone-aware datetime
    freshness_sum = 0
    
    for article in event["articles"]:
        # Process NER entities
        for entity, weight in article["_ner_entities"].items():
            severity_score += float(weight)
            total_entities += 1
        
        # Check for important keywords
        article_text = (article["title"] + " " + article["description"]).lower()
        keyword_matches = sum(keyword in article_text for keyword in important_keywords)
        severity_score += keyword_matches * 0.05
        
        # Add freshness factor - ensure timezone-aware comparison
        try:
            # Handle both ISO format with and without timezone
            if isinstance(article["published_date"], str):
                if 'Z' in article["published_date"]:
                    article_date = datetime.fromisoformat(article["published_date"].replace('Z', '+00:00'))
                else:
                    article_date = datetime.fromisoformat(article["published_date"])
                    if article_date.tzinfo is None:
                        article_date = article_date.replace(tzinfo=timezone.utc)
            else:
                article_date = article["published_date"]
                if article_date.tzinfo is None:
                    article_date = article_date.replace(tzinfo=timezone.utc)
                    
            days_old = (now - article_date).days
            freshness_factor = max(0, 1 - (days_old / 14))  # Higher for newer articles
            freshness_sum += freshness_factor
        except Exception as e:
            print(f"Date parsing error: {e}, using default freshness")
            freshness_sum += 0.5  # Default freshness
    
    # Normalize entity score
    if total_entities > 0:
        severity_score = severity_score / total_entities
    
    # Factor in article count (diminishing returns for many articles)
    article_count_factor = min(0.5, len(event["articles"]) * 0.05)
    
    # Factor in freshness
    average_freshness = freshness_sum / len(event["articles"]) if event["articles"] else 0
    
    # Factor in source credibility
    credibility_factor = credible_article_count / len(event["articles"]) if event["articles"] else 0
    
    # Combine all factors
    final_severity = (
        severity_score * 0.5 +
        article_count_factor * 0.2 +
        average_freshness * 0.15 +
        credibility_factor * 0.15
    )
    
    return round(min(1.0, final_severity), 2)

# Generate events based on cluster labels
print("Forming events...")
events = {}
for idx, cluster_id in enumerate(all_cluster_labels):
    if cluster_id not in events:
        events[cluster_id] = {"articles": []}
    
    # For articles, only include the specified fields
    article = {
        "title": df.at[idx, "title"],
        "description": df.at[idx, "description"],
        "published_date": df.at[idx, "published_date"].isoformat(),
        "source": df.at[idx, "source"],
        "source_country": df.at[idx, "source_country"],
        "news_type": df.at[idx, "news_type"],
        "countries_mentioned": df.at[idx, "countries_mentioned"],
        "link": df.at[idx, "link"],
        "content": df.at[idx, "content"],
        "_ner_entities": df.at[idx, "_ner_entities"]  # Used internally for severity calculation
    }
    
    events[cluster_id]["articles"].append(article)

# Add event metadata and calculate severity
cleanedEvents = []
for cluster_id, event in events.items():
    # Generate event name from most common entities or title words
    titles = [article["title"] for article in event["articles"]]
    all_words = " ".join(titles).lower().split()
    # Filter out common stop words
    meaningful_words = [word for word in all_words if len(word) > 4 
                      and word not in ["about", "after", "their", "these", "those", "would", "could"]]
    
    if meaningful_words:
        # Get most frequent words for the event name
        word_freq = {}
        for word in meaningful_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:3]
        event_name = " ".join(word for word, _ in top_words).title()
    else:
        event_name = "Event " + str(cluster_id)
    
    # Calculate severity
    severity = calculate_severity(event)
    
    # Remove internal fields from articles
    articles = []
    for article in event["articles"]:
        article_clean = {k: v for k, v in article.items() if not k.startswith('_')}
        articles.append(article_clean)
    
    # Create cleaned event object with only requested fields
    cleaned_event = {
        "name": event_name,
        "event_id": str(cluster_id),
        "severity": severity,
        "articles": articles,
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "articleCount": len(articles)
    }
    
    cleanedEvents.append(cleaned_event)

# Save events to file
with open("news_events_ner.json", "w") as f:
    json.dump(cleanedEvents, f, indent=4)

print(f"Events processed and stored in news_events_ner.json with severity scores.")
print(f"Number of events detected: {len(cleanedEvents)}")

# Print some stats about events
event_sizes = [len(event["articles"]) for event in cleanedEvents]
if event_sizes:
    print(f"Average event size: {sum(event_sizes)/len(event_sizes):.2f} articles")
    print(f"Largest event: {max(event_sizes)} articles")
    print(f"Smallest event: {min(event_sizes)} articles")

# Try MongoDB Atlas connection with Server API v1
uri = "mongodb+srv://parthdesai635:parth0301@ewd.azvnj.mongodb.net/?appName=EWD"

try:
    print("Connecting to MongoDB with Server API v1...")
    
    # Create a new client and connect to the server
    client = MongoClient(
        uri, 
        server_api=ServerApi('1'),
        # tlsCAFile=certifi.where()  # Use certifi for certificate verification
    )
    
    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("Pinged your deployment. Successfully connected to MongoDB!")
    
    # Access database and collection
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    
    # Insert data in smaller batches to avoid timeouts
    print("Pushing events to MongoDB...")
    batch_size = 10  # Smaller batch size
    successful_inserts = 0
    
    for i in range(0, len(cleanedEvents), batch_size):
        batch = cleanedEvents[i:i+batch_size]
        if batch:
            try:
                result = collection.insert_many(batch, ordered=False)
                successful_inserts += len(result.inserted_ids)
                print(f"Inserted batch {i//batch_size + 1}: {len(result.inserted_ids)} events")
            except pymongo.errors.BulkWriteError as bwe:
                # Some documents might still have been inserted
                print(f"Batch {i//batch_size + 1} had errors but some documents may have been inserted")
                print(f"Error details: {bwe.details}")
    
    print(f"Successfully inserted {successful_inserts} out of {len(cleanedEvents)} events")

except pymongo.errors.ConnectionFailure as e:
    print(f"Connection error: {e}")
except pymongo.errors.OperationFailure as e:
    print(f"Authentication or operation error: {e}")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    print("Falling back to local storage only")

finally:
    if 'client' in locals():
        client.close()
        print("MongoDB connection closed.")