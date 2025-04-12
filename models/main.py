from transformers import pipeline
import json
import pandas as pd
import spacy
import numpy as np
from datetime import datetime, timezone
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load SentenceTransformer model
print("Loading SentenceTransformer model...")
model = SentenceTransformer('pauhidalgoo/finetuned-sts-ca-mpnet-base')
print("Model loaded successfully!")

# Load severity classification pipeline
print("Loading sentiment severity classification pipeline...")
sentiment_pipe = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")
print("Sentiment model loaded successfully!")

# MongoDB connection details (keep password secure in production)
MONGO_URI = "mongodb+srv://parthdesai635:<parth0301>@ewd.azvnj.mongodb.net/?retryWrites=true&w=majority&appName=EWD"
DATABASE_NAME = "NewsDB"
COLLECTION_EVENT = "News2"
COLLECTION_ARTICLE = "Articles2"
# Severity mapping function
def sentiment_to_severity(label):
    severity_map = {
        "Very Negative": (0, 0.2),
        "Negative": (0.2, 0.4),
        "Neutral": (0.4, 0.6),
        "Positive": (0.6, 0.8),
        "Very Positive": (0.8, 1.0)
    }
    return severity_map.get(label, (4, 6))  # Default to neutral range if label is unexpected

# Load dataset
with open("filtered_news_articles.json", "r") as f:
    news_data = json.load(f)

df = pd.DataFrame(news_data)

def safe_get(col):
    return df[col] if col in df.columns else ""
df["source_country"] = safe_get("source_country")
df["news_type"] = safe_get("news_type")
df["countries_mentioned"] = safe_get("countries_mentioned")
df["source"] = safe_get("source")
df["content"] = safe_get("content")
df.fillna("", inplace=True)

def extract_ner_entities(text):
    text = str(text)
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PERSON", "GPE", "LOC", "EVENT"]:
            weight = 0.05 if ent.label_ in ["EVENT", "GPE"] else 0.03
            entities[ent.text.lower()] = weight
    return entities

df["_ner_entities"] = (df["title"] + " " + df["description"]).apply(extract_ner_entities)

df["published_date"] = pd.to_datetime(df["published_date"], errors="coerce", utc=True)
df.dropna(subset=["published_date"], inplace=True)
df.reset_index(drop=True, inplace=True)

# Embeddings
print("Computing article embeddings...")
article_texts = [f"{title} {desc}" for title, desc in zip(df["title"], df["description"])]
embeddings = model.encode(article_texts, normalize_embeddings=True)
print(f"Generated embeddings shape: {embeddings.shape}")

# Clustering by news_type
print("Grouping articles by news type...")
news_types = df["news_type"].unique()
print(f"Found {len(news_types)} different news types: {', '.join(news_types)}")

all_cluster_labels = []
next_cluster_id = 0
CLUSTERING_DISTANCE = 0.35

for news_type in news_types:
    print(f"Processing news_type: {news_type}")
    mask = df["news_type"] == news_type
    type_indices = df[mask].index.tolist()

    if len(type_indices) <= 1:
        for idx in type_indices:
            all_cluster_labels.append(next_cluster_id)
            next_cluster_id += 1
        continue

    type_embeddings = embeddings[type_indices]
    distance_matrix = 1 - np.dot(type_embeddings, type_embeddings.T)
    np.fill_diagonal(distance_matrix, 0)
    distance_matrix = np.maximum(distance_matrix, 0)

    clustering = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=CLUSTERING_DISTANCE,
        metric='precomputed',
        linkage='average'
    )
    type_cluster_labels = clustering.fit_predict(distance_matrix)

    for label in type_cluster_labels:
        all_cluster_labels.append(label + next_cluster_id)

    next_cluster_id += max(type_cluster_labels) + 1 if len(type_cluster_labels) > 0 else 1

print(f"Total clusters created: {len(set(all_cluster_labels))}")

# New severity function using sentiment pipeline
def calculate_severity(event):
    if not event["articles"]:
        return 0.0

    severity_scores = []

    for article in event["articles"]:
        text = f"{article['title']} {article['description']}".strip()
        try:
            prediction = sentiment_pipe(text)[0]
            label = prediction["label"]
            score = prediction["score"]
            low, high = sentiment_to_severity(label)
            severity = low + (high - low) * score
            severity_scores.append(severity)
        except Exception as e:
            print(f"Error classifying article: {e}")
            severity_scores.append(5.0)  # Fallback to neutral midpoint

    avg_severity = sum(severity_scores) / len(severity_scores)
    article_count_factor = min(1.0, len(event["articles"]) * 0.05)
    final_severity = min(10.0, avg_severity + article_count_factor)

    return round(final_severity, 2)

# Form events
print("Forming events...")
events = {}
for idx, cluster_id in enumerate(all_cluster_labels):
    if cluster_id not in events:
        events[cluster_id] = {"articles": []}

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
        "_ner_entities": df.at[idx, "_ner_entities"]
    }
    events[cluster_id]["articles"].append(article)

cleanedEvents = []
for cluster_id, event in events.items():
    titles = [article["title"] for article in event["articles"]]
    all_words = " ".join(titles).lower().split()
    meaningful_words = [word for word in all_words if len(word) > 4 
                        and word not in ["about", "after", "their", "these", "those", "would", "could"]]
    
    if meaningful_words:
        word_freq = {}
        for word in meaningful_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:3]
        event_name = " ".join(word for word, _ in top_words).title()
    else:
        event_name = "Event " + str(cluster_id)

    severity = calculate_severity(event)

    articles = []
    for article in event["articles"]:
        article_clean = {k: v for k, v in article.items() if not k.startswith('_')}
        articles.append(article_clean)

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

# Save results
with open("news_events_ner2.json", "w") as f:
    json.dump(cleanedEvents, f, indent=4)

print(f"Events processed and stored in news_events_ner.json with severity scores.")
print(f"Number of events detected: {len(cleanedEvents)}")

event_sizes = [len(event["articles"]) for event in cleanedEvents]
if event_sizes:
    print(f"Average event size: {sum(event_sizes)/len(event_sizes):.2f} articles")
    print(f"Largest event: {max(event_sizes)} articles")
    print(f"Smallest event: {min(event_sizes)} articles")


# MongoDB connection (commented out as in original)
# uri = "mongodb+srv://parthdesai635:parth0301@ewd.azvnj.mongodb.net/?appName=EWD"
# try:
#     print("Connecting to MongoDB...")
#     client = MongoClient(uri, server_api=ServerApi('1'))
#     client.admin.command('ping')
#     print("Connected to MongoDB!")
#     db = client[DATABASE_NAME]
#     collection = db[COLLECTION_NAME]
#     # Insert data in batches...
# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
# finally:
#     if 'client' in locals():
#         client.close()


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
    
    # Access database and collection for events
    db = client[DATABASE_NAME]
    events_collection = db[COLLECTION_EVENT]
    articles_collection = db[COLLECTION_ARTICLE]  # Create a separate collection for articles
    
    # Insert events data first
    print("Pushing events to MongoDB...")
    batch_size = 10  # Smaller batch size
    successful_event_inserts = 0
    successful_article_inserts = 0
    
    # Create events without the articles array first
    events_for_upload = []
    for event in cleanedEvents:
        # Create a copy of the event without articles for main collection
        event_copy = {k: v for k, v in event.items() if k != 'articles'}
        event_copy['articleCount'] = len(event['articles'])  # Make sure we have the count
        events_for_upload.append(event_copy)
    
    # Upload events in batches
    for i in range(0, len(events_for_upload), batch_size):
        batch = events_for_upload[i:i+batch_size]
        if batch:
            try:
                result = events_collection.insert_many(batch, ordered=False)
                successful_event_inserts += len(result.inserted_ids)
                print(f"Inserted event batch {i//batch_size + 1}: {len(result.inserted_ids)} events")
            except pymongo.errors.BulkWriteError as bwe:
                # Some documents might still have been inserted
                print(f"Event batch {i//batch_size + 1} had errors but some events may have been inserted")
                if hasattr(bwe, 'details'):
                    print(f"Error details: {bwe.details}")
    
    print(f"Successfully inserted {successful_event_inserts} out of {len(events_for_upload)} events")
    
    # Now upload all articles with references to their parent events
    all_articles = []
    for event in cleanedEvents:
        event_id = event['event_id']
        for article in event['articles']:
            # Add event reference to article
            article['event_id'] = event_id
            article['event_name'] = event['name']
            article['_id'] = f"{event_id}_{article['link'].split('/')[-1]}"  # Create unique ID
            all_articles.append(article)
    
    # Upload articles in batches
    print(f"Pushing {len(all_articles)} articles to MongoDB...")
    for i in range(0, len(all_articles), batch_size):
        batch = all_articles[i:i+batch_size]
        if batch:
            try:
                result = articles_collection.insert_many(batch, ordered=False)
                successful_article_inserts += len(result.inserted_ids)
                print(f"Inserted article batch {i//batch_size + 1}: {len(result.inserted_ids)} articles")
            except pymongo.errors.BulkWriteError as bwe:
                # Some documents might still have been inserted
                print(f"Article batch {i//batch_size + 1} had errors but some articles may have been inserted")
                if hasattr(bwe, 'details'):
                    print(f"Error details: {bwe.details}")
    
    print(f"Successfully inserted {successful_article_inserts} out of {len(all_articles)} articles")
    
    # Add summary of the upload operation
    print(f"\nMongoDB Upload Summary:")
    print(f"- Events Collection: {successful_event_inserts} events uploaded to {COLLECTION_EVENT}")
    print(f"- Articles Collection: {successful_article_inserts} articles uploaded to {COLLECTION_ARTICLE}")

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