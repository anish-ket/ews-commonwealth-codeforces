# pip install requests BeautifulSoup newspaper3k spacy google-genai
# python -m spacy download en_core_web_md
import requests
import json
from bs4 import BeautifulSoup
import newspaper
from newspaper import Article
import spacy
import re
# from google import genai
# from google.generativeai import GenerativeModel
import google.generativeai as genai
from time import sleep
from datetime import datetime, timedelta
from collections import defaultdict

# Initialize Gemini client
GOOGLE_API_KEY = "AIzaSyDZr_wSUvi2kHGqDppUrpxzrnCTRgm7kxA"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)
MODEL_ID = "gemini-2.0-flash"

# Configuration for the optimized pipeline
KEYWORD_CONFIDENCE_THRESHOLD = 3  # Minimum keyword matches to consider
GEMINI_RATE_LIMIT = 15  # Max requests per minute

# Load spaCy model
nlp = spacy.load("en_core_web_md")

# Sources and country configurations
sources = {
    "Times of India" : {
        "RSSlink" : "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
        "Country" : "India"
    },
    "NDTV" : {
        "RSSlink" : "https://feeds.feedburner.com/ndtvnews-top-stories",
        "Country" : "India"
    },

    "The Hindu" : {
        "RSSlink" : "https://www.thehindu.com/news/national/feeder/default.rss",
        "Country" : "India"
    },

    "Mint Politics" : {
        "RSSlink" : "https://www.livemint.com/rss/politics",
        "Country" : "India"
    },

    "Mint News" : {
        "RSSlink" : "https://www.livemint.com/rss/news",
        "Country" : "India"
    },

    "CNBC Politics" : {
        "RSSlink" : "https://www.cnbctv18.com/commonfeeds/v1/cne/rss/politics.xml",
        "Country" : "India"
    },

    "CNBC Economics" : {
        "RSSlink" : "https://www.cnbctv18.com/commonfeeds/v1/cne/rss/economy.xml",
        "Country" : "India"
    },

    "CNBC World" : {
        "RSSlink" : "https://www.cnbctv18.com/commonfeeds/v1/cne/rss/world.xml",
        "Country" : "India"
    },

    "CNBC Market" : {
        "RSSlink" : "https://www.cnbctv18.com/commonfeeds/v1/cne/rss/market.xml",
        "Country" : "India"
    },

    "DNA India" : {
        "RSSlink" : "https://www.dnaindia.com/feeds/india.xml",
        "Country" : "India"
    },

    "The Star Online": {
        "RSSlink": "https://www.thestar.com.my/rss/News/Nation",
        "Country": "Malaysia"
    },
    
    "The Sun (Malaysia)": {
        "RSSlink": "https://thesun.my/rss/local",
        "Country": "Malaysia"
    },
    
    "Free Malaysia Today": {
        "RSSlink": "https://www.freemalaysiatoday.com/category/nation/feed/",
        "Country": "Malaysia"
    },

    "The Sydney Morning Herald": {
        "RSSlink": "https://www.smh.com.au/rss/feed.xml",
        "Country": "Australia"
    },

    "Independent Australia": {
        "RSSlink": "http://feeds.feedburner.com/IndependentAustralia",
        "Country": "Australia"
    },

    "The Age": {
        "RSSlink": "https://www.theage.com.au/rss/feed.xml",
        "Country": "Australia"
    },

    "The Straits Times": {
        "RSSlink": "https://www.straitstimes.com/news/singapore/rss.xml",
        "Country": "Singapore"
    },

    "Channel NewsAsia": {
        "RSSlink": "https://www.channelnewsasia.com/rssfeeds/8395986",
        "Country": "Singapore"
    },

    "Business Times": {
        "RSSlink": "https://www.businesstimes.com.sg/rss/singapore",
        "Country": "Singapore"
    },

    "CBC News": {
        "RSSlink": "https://www.cbc.ca/webfeed/rss/rss-world",
        "Country": "Canada"
    },

    "Toronto Star": {
        "RSSlink": "https://www.thestar.com/search/?f=rss&t=article&c=news/canada*&l=50&s=start_time&sd=desc",
        "Country": "Canada"
    },

    "Global News (Canada)": {
        "RSSlink": "https://globalnews.ca/feed/",
        "Country": "Canada"
    }
}

# List of countries to filter for - add variations, abbreviations, adjectives, demonyms
country_variations = {
    "India": ["India", "Indian", "Indians", "New Delhi", "Delhi", "Mumbai", "Bangalore", "Chennai", 
              "Kolkata", "Hyderabad", "Modi", "BJP", "Congress Party", "Rupee"],
    
    "Canada": ["Canada", "Canadian", "Canadians", "Ottawa", "Toronto", "Vancouver", "Montreal", 
               "Quebec", "Alberta", "Ontario", "Trudeau", "CAD", "Loonie"],
    
    "Singapore": ["Singapore", "Singaporean", "Singaporeans", "SG", "Lion City", 
                 "Changi", "Lee Hsien Loong", "PAP", "SGD"],
    
    "Nigeria": ["Nigeria", "Nigerian", "Nigerians", "Lagos", "Abuja", "Naira", 
                "Buhari", "APC", "PDP"],
    
    "Australia": ["Australia", "Australian", "Australians", "Aussie", "Aussies", "Sydney", 
                  "Melbourne", "Canberra", "Brisbane", "Perth", "AUD", "Albanese"],
    
    "Malaysia": ["Malaysia", "Malaysian", "Malaysians", "Kuala Lumpur", "KL", 
                 "Putrajaya", "Sabah", "Sarawak", "Anwar Ibrahim", "Ringgit", "MYR"],
    
    "United Kingdom": ["United Kingdom", "UK", "Britain", "British", "Britons", "England", 
                      "Scotland", "Wales", "Northern Ireland", "London", "Manchester", 
                      "Birmingham", "Liverpool", "Edinburgh", "Glasgow", "Belfast", 
                      "British", "Pound", "Sterling", "GBP", "Starmer", "Labour", "Tory", "Conservative"]
}

# Flatten the country variations for easier lookup
target_countries = list(country_variations.keys())
country_keywords = {}
for country, variations in country_variations.items():
    for variation in variations:
        country_keywords[variation.lower()] = country

def detect_countries(text):
    """Detect mentions of target countries in the text"""
    text_lower = text.lower()
    mentioned_countries = set()
    
    # First try direct keyword matching (efficient)
    for keyword, country in country_keywords.items():
        # Use word boundary matching to avoid partial matches
        if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
            mentioned_countries.add(country)
    
    # If we have a decent amount of text, also use spaCy for geopolitical entities
    if len(text) > 100 and len(mentioned_countries) == 0:
        # Process with spaCy, limiting text length for performance
        doc = nlp(text[:5000])
        
        # Extract locations from named entities
        for ent in doc.ents:
            if ent.label_ in ["GPE", "LOC"]:
                # Check if this entity matches any of our target countries or their variations
                ent_text = ent.text.lower()
                for keyword, country in country_keywords.items():
                    # Allow partial matches for countries and major cities
                    if keyword in ent_text or ent_text in keyword:
                        mentioned_countries.add(country)
    
    return list(mentioned_countries)

class RateLimiter:
    def __init__(self):
        self.calls = []
    
    def wait(self):
        now = datetime.now()
        # Remove calls older than 1 minute
        self.calls = [call for call in self.calls if (now - call).total_seconds() < 60]
        
        if len(self.calls) >= GEMINI_RATE_LIMIT:
            oldest = self.calls[0]
            wait_time = (60 - (now - oldest).total_seconds()) + 0.1
            print(f"⏳ Rate limit reached. Waiting {wait_time:.1f}s...")
            sleep(wait_time)
        
        self.calls.append(datetime.now())

limiter = RateLimiter()

def keyword_filter(text):
    """More permissive keyword filtering"""
    text_lower = text.lower()
    
    # Immediate exclusion only for clearly irrelevant content
    if any(term in text_lower for term in [
        'sports', 'cricket', 'football', 'movie', 'entertainment',
        'celebrity', 'actor', 'actress', 'music', 'concert'
    ]):
        return None
    
    # More inclusive category detection
    category_scores = {
        'Environment': 0,
        'Politics': 0, 
        'Economics': 0
    }
    
    # Environmental terms (relaxed)
    env_terms = ['climate', 'environment', 'pollut', 'emission', 'sustain',
                'conserv', 'wildlife', 'forest', 'energy', 'green']
    category_scores['Environment'] = sum(term in text_lower for term in env_terms)
    
    # Political terms (relaxed)
    political_terms = ['election', 'government', 'minister', 'president',
                      'policy', 'law', 'political', 'vote', 'democracy']
    category_scores['Politics'] = sum(term in text_lower for term in political_terms)
    
    # Economic terms (relaxed)
    economic_terms = ['economy', 'market', 'finance', 'trade', 'gdp',
                     'inflation', 'bank', 'business', 'investment']
    category_scores['Economics'] = sum(term in text_lower for term in economic_terms)
    
    # Get best category if meets relaxed threshold
    best_category = max(category_scores, key=category_scores.get)
    if category_scores[best_category] >= 2:  # Lowered from 3 to 2
        return best_category
    return None

def gemini_verify(article, proposed_category):
    """Gemini verification with correct API usage"""
    try:
        limiter.wait()
        
        # Create prompt text
        prompt = f"Does this article focus on {proposed_category}? Reply only YES or NO.\n\n" \
                 f"Title: {article['title']}\n" \
                 f"Content: {article['content'][:1500]}"
        
        # Correct API call format
        model = genai.GenerativeModel(MODEL_ID)
        response = model.generate_content(prompt)
        
        # Parse response safely
        if hasattr(response, 'text'):
            answer = response.text.strip().lower()
            return answer.startswith('yes')
        return False
        
    except Exception as e:
        print(f"⚠️ Gemini error (will retry): {str(e)}")
        sleep(2)
        return gemini_verify(article, proposed_category)  # Retry

def process_articles(articles):
    """Optimized processing pipeline"""
    print(f"\n🔍 Starting processing of {len(articles)} articles...")
    
    results = {
        'keyword_rejected': 0,
        'sent_to_gemini': 0,
        'gemini_verified': 0,
        'final_counts': defaultdict(int)
    }
    
    filtered_articles = []
    
    for idx, article in enumerate(articles, 1):
        text = f"{article['title']} {article['content'][:2000]}"
        category = keyword_filter(text)
        
        if not category:
            results['keyword_rejected'] += 1
            continue
            
        results['sent_to_gemini'] += 1
        if gemini_verify(article, category):
            article['news_type'] = category
            filtered_articles.append(article)
            results['final_counts'][category] += 1
            results['gemini_verified'] += 1
            print(f"✅ {idx}/{len(articles)}: {category} - {article['title'][:50]}...")
        else:
            print(f"❌ {idx}/{len(articles)}: Rejected by Gemini")
    
    # Reporting
    print("\n📊 Final Results:")
    print(f"Articles processed: {len(articles)}")
    print(f"Rejected by keywords: {results['keyword_rejected']} ({(results['keyword_rejected']/len(articles))*100:.1f}%)")
    print(f"Sent to Gemini: {results['sent_to_gemini']}")
    print(f"Approved by Gemini: {results['gemini_verified']}")
    print("\nApproved articles by category:")
    for cat, count in results['final_counts'].items():
        print(f"- {cat}: {count}")
    
    return filtered_articles

def articleScraper(sourceURL, source, country):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(sourceURL, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, "xml")
        scraped_articles = []
        
        for item in soup.find_all("item"):
            try:
                link_text = item.link.text if item.link else ""
                if not link_text:
                    continue
                    
                article = Article(link_text)
                article.download()
                article.parse()
                
                content = article.text
                title = item.title.text if item.title else "No title"
                
                # Check if article mentions target countries
                countries_mentioned = detect_countries(title + " " + content)
                if not countries_mentioned and country not in target_countries:
                    continue
                
                # Always include the source country
                if country in target_countries and country not in countries_mentioned:
                    countries_mentioned.append(country)
                
                scraped_articles.append({
                    "title": title,
                    "link": link_text,
                    "description": item.description.text if hasattr(item, 'description') and item.description else "No description",
                    "published_date": item.pubDate.text if hasattr(item, 'pubDate') and item.pubDate else "No date",
                    "source": source,
                    "source_country": country,
                    "countries_mentioned": countries_mentioned,
                    "content": content
                })
                
                if len(scraped_articles) >= 5:  # Limit to 5 articles per source
                    break
                    
            except Exception as e:
                print(f"Error processing article from {source}: {str(e)}")
                continue
                
        print(f"Scraped {len(scraped_articles)} Articles from {source}")
        return scraped_articles
        
    except Exception as e:
        print(f"Error accessing RSS feed for {source}: {str(e)}")
        return []

def main():
    all_articles = []
    
    # Scrape articles from all sources
    for source in sources:
        try:
            articles = articleScraper(sources[source]['RSSlink'], source, sources[source]['Country'])
            all_articles.extend(articles)
        except Exception as e:
            print(f"Error scraping from {source}: {str(e)}")
    
    if not all_articles:
        print("No articles were scraped.")
        return
    
    # Use the new optimized pipeline instead of gemini_classify_articles
    print("\nProcessing articles with optimized pipeline...")
    filtered_articles = process_articles(all_articles)
    
    # Save results
    with open("filtered_news_articles1.json", "w") as f:
        json.dump(filtered_articles, f, indent=4)
    
    # No need for additional reporting as process_articles already generates reports
    print("\nFiltered news articles have been saved to 'filtered_news_articles1.json'")

if __name__ == "__main__":
    main()