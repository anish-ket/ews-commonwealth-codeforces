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
import google.generativeai as genai
from time import sleep
from collections import defaultdict

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

GOOGLE_API_KEY = "AIzaSyDZr_wSUvi2kHGqDppUrpxzrnCTRgm7kxA"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)
EVENT_MODEL = "gemini-2.0-flash"  # Change from gemini-2.0-flash to this more reliable model


# RateLimiter class for Gemini API
class RateLimiter:
    def __init__(self, max_calls=15):
        self.calls = []
        self.max_calls = max_calls
    
    def wait(self):
        now = datetime.now(timezone.utc)
        # Remove calls older than 1 minute
        self.calls = [call for call in self.calls if (now - call).total_seconds() < 60]
        
        if len(self.calls) >= self.max_calls:
            oldest = self.calls[0]
            wait_time = (60 - (now - oldest).total_seconds()) + 0.1
            print(f"⏳ Rate limit reached. Waiting {wait_time:.1f}s...")
            sleep(wait_time)
        
        self.calls.append(now)

limiter = RateLimiter()

def generate_event_name_with_gemini(articles):
    """Generate an event name using Gemini based on article titles"""
    try:
        limiter.wait()
        print(f"Attempting to generate name with Gemini for event with {len(articles)} articles...")
        
        # Extract titles, handling potential missing keys
        titles = []
        for article in articles:
            if 'title' in article and article['title']:
                titles.append(article['title'])
        
        if not titles:
            print("No titles found in articles, skipping Gemini name generation")
            return None
            
        # Create a simpler prompt for more reliability
        prompt = "Generate a short 3-5 word headline that summarizes these news articles. ONLY provide the headline text:\n\n" + "\n".join(titles[:2])
        
        print("Calling Gemini API for event name...")
        model = genai.GenerativeModel(EVENT_MODEL)
        response = model.generate_content(prompt)
        
        if hasattr(response, 'text') and response.text:
            event_name = response.text.strip().strip('"\'').strip()
            print(f"Gemini successfully generated event name: '{event_name}'")
            if len(event_name) > 50:
                event_name = event_name[:47] + "..."
            return event_name
        else:
            print("Gemini returned empty response for event name")
            return None
        
    except Exception as e:
        print(f"⚠️ Gemini error generating event name: {str(e)}")
        return None  # Don't retry

def generate_event_summary_with_gemini(articles):
    """Generate a comprehensive event summary using Gemini"""
    try:
        limiter.wait()
        print(f"Attempting to generate summary with Gemini for event with {len(articles)} articles...")
        
        # Prepare article data in a more robust way
        titles_and_descriptions = []
        for article in articles:
            title = article.get('title', '')
            desc = article.get('description', '')
            if title or desc:
                titles_and_descriptions.append(f"Title: {title}\nDescription: {desc}")
        
        if not titles_and_descriptions:
            print("No content found for summary generation")
            return "No summary available."
            
        # Use only the first article to avoid context length issues
        prompt = "Write a 2-3 sentence summary of this news article:\n\n" + titles_and_descriptions[0]
        
        print("Calling Gemini API for event summary...")
        model = genai.GenerativeModel(EVENT_MODEL)
        response = model.generate_content(prompt)
        
        if hasattr(response, 'text') and response.text:
            summary = response.text.strip()
            print(f"Gemini successfully generated summary of length {len(summary)}")
            if len(summary) > 500:
                summary = summary[:497] + "..."
            return summary
        else:
            print("Gemini returned empty response for summary")
            return "No summary available."
        
    except Exception as e:
        print(f"⚠️ Gemini error generating summary: {str(e)}")
        # Fallback summary without retrying
        if articles and 'description' in articles[0] and articles[0]['description']:
            print("Using article description as fallback summary")
            return articles[0]['description']
        return "No summary available."

def generate_event_timeline_with_gemini(articles):
    """Generate a chronological timeline for an event using Gemini"""
    try:
        limiter.wait()
        print(f"Attempting to generate timeline with Gemini for event with {len(articles)} articles...")
        
        # Prepare timeline data - sort articles by date first
        sorted_articles = sorted(articles, key=lambda x: x.get('published_date', ''))
        
        # Format timeline entries for prompt
        timeline_entries = []
        for article in sorted_articles:
            date = article.get('published_date', 'Unknown date')
            title = article.get('title', 'No title')
            timeline_entries.append(f"{date}: {title}")
        
        if not timeline_entries:
            return "No timeline available."
            
        # Avoid using the f-string with potentially complex content
        entries_text = "\n".join(timeline_entries[:5])  # Limit to 5 entries
        
        prompt = f"""
        Create a concise chronological timeline for this news event based on these articles. 
        For each entry, include:
        - The date (formatted as DD Month YYYY)
        - A very brief summary (5-10 words) of what happened
        - Keep the entire timeline under 5 bullet points if possible
        
        Articles in chronological order:
        {entries_text}
        
        Respond with just the timeline in bullet points, nothing else.
        Example format:
        - 15 June 2023: Earthquake struck northern region
        - 16 June 2023: Rescue operations began with 100+ saved
        """
        
        print("Calling Gemini API for timeline generation...")
        model = genai.GenerativeModel(EVENT_MODEL)
        response = model.generate_content(prompt)
        
        if hasattr(response, 'text') and response.text:
            timeline = response.text.strip()
            print(f"Gemini successfully generated timeline of length {len(timeline)}")
            if len(timeline) > 1000:  # Safety check
                timeline = timeline[:997] + "..."
            return timeline
        else:
            print("Gemini returned empty response for timeline")
            return "No timeline available."
        
    except Exception as e:
        print(f"⚠️ Gemini error generating timeline: {str(e)}")
        # Fallback timeline without retrying
        try:
            sorted_articles = sorted(articles, key=lambda x: x.get('published_date', ''))
            fallback_timeline = []
            for article in sorted_articles[:3]:  # Just show first 3 as fallback
                date = article.get('published_date', 'Unknown date')
                title = article.get('title', 'No title')
                fallback_timeline.append(f"- {date}: {title[:50]}{'...' if len(title)>50 else ''}")
            return "\n".join(fallback_timeline)
        except:
            return "No timeline available."



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
with open("filtered_news_articles1.json", "r") as f:
    news_data = json.load(f)

# Load existing events if available
existing_events = []
existing_articles_urls = set()
try:
    with open("news_events_ner1.json", "r") as f:
        existing_events = json.load(f)
        print(f"Loaded {len(existing_events)} existing events from news_events_ner1.json")
        
        # Create a set of existing article URLs for deduplication
        for event in existing_events:
            for article in event["articles"]:
                if "link" in article:
                    existing_articles_urls.add(article["link"])
        
        print(f"Found {len(existing_articles_urls)} existing article URLs")
except FileNotFoundError:
    print("No existing events file found. Starting fresh.")
except json.JSONDecodeError:
    print("Error parsing existing events file. Starting fresh.")

# Filter out articles that already exist in our events
new_articles = []
for article in news_data:
    if article.get("link") not in existing_articles_urls:
        new_articles.append(article)

print(f"Found {len(new_articles)} new articles to process")

# If no new articles, we can exit early
if not new_articles:
    print("No new articles to process. Exiting.")
    exit()

# Replace the original news_data with only new articles
news_data = new_articles

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
    # Generate event name with Gemini
    print(f"Processing event {cluster_id} with {len(event['articles'])} articles...")
    event_name = generate_event_name_with_gemini(event["articles"])
    if not event_name:
        # Fallback to original method if Gemini fails
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

    # Generate summary with Gemini
    summary = generate_event_summary_with_gemini(event["articles"])
    if not summary:
        summary = "No summary available."
        
    # Generate timeline with Gemini
    timeline = generate_event_timeline_with_gemini(event["articles"])

    severity = calculate_severity(event)

    articles = []
    for article in event["articles"]:
        article_clean = {k: v for k, v in article.items() if not k.startswith('_')}
        articles.append(article_clean)

    cleaned_event = {
        "name": event_name,
        "summary": summary,  # Add the generated summary
        "timeline": timeline,  # Add the generated timeline
        "event_id": str(cluster_id),
        "severity": severity,
        "articles": articles,
        "createdAt": datetime.now(timezone.utc).isoformat(),
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "articleCount": len(articles)
    }
    cleanedEvents.append(cleaned_event)

# Merge new events with existing events if any
if existing_events:
    print("Merging new events with existing events...")
    
    # For each existing event, create embeddings for comparison
    existing_event_texts = []
    for event in existing_events:
        # Create a composite text representation of the event
        titles = [article["title"] for article in event["articles"][:3]]  # Use first 3 articles
        event_text = " ".join(titles)
        existing_event_texts.append(event_text)
    
    existing_event_embeddings = model.encode(existing_event_texts, normalize_embeddings=True)
    
    # For each new event, check if it's similar to an existing event
    merged_events = 0
    events_to_add = []
    
    for new_event in cleanedEvents:
        # Create embedding for the new event
        new_titles = [article["title"] for article in new_event["articles"][:3]]
        new_event_text = " ".join(new_titles)
        new_event_embedding = model.encode([new_event_text], normalize_embeddings=True)[0]
        
        # Calculate similarities with existing events
        similarities = np.dot(existing_event_embeddings, new_event_embedding)
        
        # If similar enough to an existing event, merge them
        if np.max(similarities) > 0.4:  # Lower threshold from 0.5 to 0.4
            most_similar_idx = np.argmax(similarities)
            
            # Update the event name if needed (keep the one with more articles)
            if len(new_event["articles"]) > len(existing_events[most_similar_idx]["articles"]):
                existing_events[most_similar_idx]["name"] = new_event["name"]
                # Also update the summary!
                if "summary" in new_event and new_event["summary"] != "No summary available.":
                    existing_events[most_similar_idx]["summary"] = new_event["summary"]
                # Also update the timeline!
                if "timeline" in new_event and new_event["timeline"] != "No timeline available.":
                    existing_events[most_similar_idx]["timeline"] = new_event["timeline"]
            
            # Add new articles to the existing event
            for article in new_event["articles"]:
                if article["link"] not in [a.get("link") for a in existing_events[most_similar_idx]["articles"]]:
                    existing_events[most_similar_idx]["articles"].append(article)
            
            # Update article count and timestamps
            existing_events[most_similar_idx]["articleCount"] = len(existing_events[most_similar_idx]["articles"])
            existing_events[most_similar_idx]["updatedAt"] = datetime.now(timezone.utc).isoformat()
            
            # Recalculate severity with the new articles
            event_to_recalculate = existing_events[most_similar_idx].copy()
            existing_events[most_similar_idx]["severity"] = calculate_severity(event_to_recalculate)
            
            merged_events += 1
        else:
            # This is a truly new event, add it to our collection
            events_to_add.append(new_event)
    
    # Add truly new events to our collection
    final_events = existing_events + events_to_add
    print(f"Merged {merged_events} events with existing events")
    print(f"Added {len(events_to_add)} completely new events")
else:
    # No existing events, just use the new ones
    final_events = cleanedEvents

# Sort events by severity (descending) and recency of update
final_events.sort(key=lambda x: (x["severity"], x["updatedAt"]), reverse=True)

# Add before saving to JSON:
# Final cleanup to ensure all events have proper summaries and timelines
for event in final_events:
    # Summary cleanup
    if "summary" not in event or not event["summary"] or event["summary"] == "No summary available.":
        print(f"Missing summary for event: {event['name']} - generating fallback")
        # Try to use the first article's description as a fallback summary
        if event.get("articles") and len(event["articles"]) > 0 and "description" in event["articles"][0]:
            event["summary"] = event["articles"][0]["description"]
        else:
            event["summary"] = f"News event about {event['name']}."
            
    # Timeline cleanup
    if "timeline" not in event or not event["timeline"] or event["timeline"] == "No timeline available.":
        print(f"Missing timeline for event: {event['name']} - generating fallback")
        # Create a simple timeline from article dates and titles
        if event.get("articles") and len(event["articles"]) > 0:
            try:
                sorted_articles = sorted(event["articles"], key=lambda x: x.get('published_date', ''))
                fallback_timeline = []
                for article in sorted_articles[:3]:  # Just show first 3 as fallback
                    date = article.get('published_date', 'Unknown date')
                    title = article.get('title', 'No title')
                    fallback_timeline.append(f"- {date}: {title[:50]}{'...' if len(title)>50 else ''}")
                event["timeline"] = "\n".join(fallback_timeline)
            except:
                event["timeline"] = f"Timeline information not available for {event['name']}."
        else:
            event["timeline"] = f"Timeline information not available for {event['name']}."

# Save results
with open("news_events_ner3.json", "w") as f:
    json.dump(final_events, f, indent=4)

print(f"Events processed and stored in news_events_ner3.json with severity scores.")
print(f"Total events in system: {len(final_events)}")

event_sizes = [len(event["articles"]) for event in final_events]
if event_sizes:
    print(f"Average event size: {sum(event_sizes)/len(event_sizes):.2f} articles")
    print(f"Largest event: {max(event_sizes)} articles")
    print(f"Smallest event: {min(event_sizes)} articles")

# Generate statistics on event sizes
event_size_distribution = {}
for event in final_events:
    article_count = len(event["articles"])
    event_size_distribution[article_count] = event_size_distribution.get(article_count, 0) + 1

# Print the distribution
print("\nEvent size distribution:")
for size in sorted(event_size_distribution.keys()):
    print(f"Events with {size} article{'s' if size != 1 else ''}: {event_size_distribution[size]} ({(event_size_distribution[size]/len(final_events)*100):.1f}%)")

# dont uncomment this code written below, it was commented from before

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

# dont uncomment this code written above, it was commented from before


MONGO_URI = "mongodb+srv://user:ritul6789@ewd.azvnj.mongodb.net/?appName=EWD"
DATABASE_NAME = "NewsDB"
COLLECTION_EVENT = "News3"
COLLECTION_ARTICLE = "Articles3"


print("\nUploading data from news_events_ner3.json to MongoDB...")

# Load the JSON file
with open("news_events_ner3.json", "r") as f:
    final_events = json.load(f)
    print(f"Loaded {len(final_events)} events from news_events_ner3.json")

try:
    print("Connecting to MongoDB...")
    
    # Use the simpler connection string that worked before
    # MONGO_URI = "mongodb+srv://parthdesai635:parth0301@ewd.azvnj.mongodb.net/?appName=EWD"
    
    # Create client with simpler configuration
    client = MongoClient(
        MONGO_URI,
        server_api=ServerApi('1')
    )
    
    # Verify connection
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
    
    # Access database
    db = client[DATABASE_NAME]
    events_collection = db[COLLECTION_EVENT]
    articles_collection = db[COLLECTION_ARTICLE]
    
    # Upload events (let MongoDB assign _id)
    successful_event_inserts = 0
    batch_size = 10
    
    for i in range(0, len(final_events), batch_size):
        batch = []
        for event in final_events[i:i+batch_size]:
            batch.append({
                "name": event.get("name", "Unnamed Event"),
                "summary": event.get("summary", ""),
                "timeline": event.get("timeline", ""),
                "event_id": event.get("event_id"),  # Keep your existing event_id
                "severity": event.get("severity", 0),
                "createdAt": event.get("createdAt", datetime.now(timezone.utc).isoformat()),
                "updatedAt": event.get("updatedAt", datetime.now(timezone.utc).isoformat()),
                "articleCount": len(event.get("articles", []))
            })
        
        try:
            result = events_collection.insert_many(batch, ordered=False)
            successful_event_inserts += len(result.inserted_ids)
            print(f"Inserted event batch {i//batch_size + 1}: {len(result.inserted_ids)} events")
        except Exception as e:
            print(f"Error inserting batch {i//batch_size + 1}: {str(e)}")
            # Fallback to individual inserts
            for doc in batch:
                try:
                    events_collection.insert_one(doc)
                    successful_event_inserts += 1
                except Exception as e:
                    print(f"Failed to insert event: {str(e)}")
    
    print(f"Successfully inserted {successful_event_inserts}/{len(final_events)} events")
    
    # Upload articles (let MongoDB assign _id)
    successful_article_inserts = 0
    all_articles_count = sum(len(event.get("articles", [])) for event in final_events)
    
    for event in final_events:
        event_id = event.get("event_id")
        for article in event.get("articles", []):
            try:
                # Let MongoDB generate its own _id by not providing one
                article_doc = {
                    "event_id": event_id,
                    "event_name": event.get("name", "Unnamed Event"),
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "published_date": article.get("published_date", ""),
                    "source": article.get("source", ""),
                    "source_country": article.get("source_country", ""),
                    "news_type": article.get("news_type", ""),
                    "countries_mentioned": article.get("countries_mentioned", []),
                    "link": article.get("link", ""),
                    "content": article.get("content", "")
                }
                articles_collection.insert_one(article_doc)
                successful_article_inserts += 1
            except Exception as e:
                print(f"Failed to insert article: {str(e)}")
    
    print(f"Successfully inserted {successful_article_inserts}/{all_articles_count} articles")
    
    # Final summary
    print("\nUpload Summary:")
    print(f"Events: {successful_event_inserts}/{len(final_events)}")
    print(f"Articles: {successful_article_inserts}/{all_articles_count}")

except pymongo.errors.ConnectionFailure as e:
    print(f"Connection failed: {str(e)}")
except pymongo.errors.OperationFailure as e:
    print(f"Operation failed: {str(e)}")
    print("Please verify your MongoDB credentials and permissions")
except Exception as e:
    print(f"Unexpected error: {str(e)}")
finally:
    if 'client' in locals():
        client.close()
        print("MongoDB connection closed.")


















# OLD CODE (commented out)

# Try MongoDB Atlas connection with Server API v1
# uri = "mongodb+srv://parthdesai635:parth0301@ewd.azvnj.mongodb.net/?appName=EWD"

# try:
#     print("Connecting to MongoDB with Server API v1...")
    
#     # Create a new client and connect to the server
#     client = MongoClient(
#         uri, 
#         server_api=ServerApi('1'),
#         # tlsCAFile=certifi.where()  # Use certifi for certificate verification
#     )
    
#     # Send a ping to confirm a successful connection
#     client.admin.command('ping')
#     print("Pinged your deployment. Successfully connected to MongoDB!")
    
#     # Access database and collection for events
#     db = client[DATABASE_NAME]
#     events_collection = db[COLLECTION_EVENT]
#     articles_collection = db[COLLECTION_ARTICLE]  # Create a separate collection for articles
    
#     # Insert events data first
#     print("Pushing events to MongoDB...")
#     batch_size = 10  # Smaller batch size
#     successful_event_inserts = 0
#     successful_article_inserts = 0
    
#     # Create events without the articles array first
#     events_for_upload = []
#     for event in cleanedEvents:
#         # Create a copy of the event without articles for main collection
#         event_copy = {k: v for k, v in event.items() if k != 'articles'}
#         event_copy['articleCount'] = len(event['articles'])  # Make sure we have the count
#         events_for_upload.append(event_copy)
    
#     # Upload events in batches
#     for i in range(0, len(events_for_upload), batch_size):
#         batch = events_for_upload[i:i+batch_size]
#         if batch:
#             try:
#                 result = events_collection.insert_many(batch, ordered=False)
#                 successful_event_inserts += len(result.inserted_ids)
#                 print(f"Inserted event batch {i//batch_size + 1}: {len(result.inserted_ids)} events")
#             except pymongo.errors.BulkWriteError as bwe:
#                 # Some documents might still have been inserted
#                 print(f"Event batch {i//batch_size + 1} had errors but some events may have been inserted")
#                 if hasattr(bwe, 'details'):
#                     print(f"Error details: {bwe.details}")
    
#     print(f"Successfully inserted {successful_event_inserts} out of {len(events_for_upload)} events")
    
#     # Now upload all articles with references to their parent events
#     all_articles = []
#     for event in cleanedEvents:
#         event_id = event['event_id']
#         for article in event['articles']:
#             # Add event reference to article
#             article['event_id'] = event_id
#             article['event_name'] = event['name']
#             article['_id'] = f"{event_id}_{article['link'].split('/')[-1]}"  # Create unique ID
#             all_articles.append(article)
    
#     # Upload articles in batches
#     print(f"Pushing {len(all_articles)} articles to MongoDB...")
#     for i in range(0, len(all_articles), batch_size):
#         batch = all_articles[i:i+batch_size]
#         if batch:
#             try:
#                 result = articles_collection.insert_many(batch, ordered=False)
#                 successful_article_inserts += len(result.inserted_ids)
#                 print(f"Inserted article batch {i//batch_size + 1}: {len(result.inserted_ids)} articles")
#             except pymongo.errors.BulkWriteError as bwe:
#                 # Some documents might still have been inserted
#                 print(f"Article batch {i//batch_size + 1} had errors but some articles may have been inserted")
#                 if hasattr(bwe, 'details'):
#                     print(f"Error details: {bwe.details}")
    
#     print(f"Successfully inserted {successful_article_inserts} out of {len(all_articles)} articles")
    
#     # Add summary of the upload operation
#     print(f"\nMongoDB Upload Summary:")
#     print(f"- Events Collection: {successful_event_inserts} events uploaded to {COLLECTION_EVENT}")
#     print(f"- Articles Collection: {successful_article_inserts} articles uploaded to {COLLECTION_ARTICLE}")

# except pymongo.errors.ConnectionFailure as e:
#     print(f"Connection error: {e}")
# except pymongo.errors.OperationFailure as e:
#     print(f"Authentication or operation error: {e}")
# except Exception as e:
#     print(f"Error connecting to MongoDB: {e}")
#     print("Falling back to local storage only")

# finally:
#     if 'client' in locals():
#         client.close()
#         print("MongoDB connection closed.")