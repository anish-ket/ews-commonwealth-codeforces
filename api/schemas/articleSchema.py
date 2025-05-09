def indArticle(article)-> dict:
    return{
        "title": article["title"],
        "description": article["description"],
        "severity_score": str(article["severity_score"]),
        "stability_index": str(article["stability_index"]),
        "content": article["content"],
        "imgURL": article["imgURL"],
        "eventName": article["eventName"],
        "eventID": str(article["eventID"]),
        "alignment": str(article["alignment"]),
        "source": article["source"],
        "sourceID": str(article["sourceID"]),
        "sourceLogo": article["sourceLogo"],
        "link": article["link"],
        "timestamp": article["timestamp"],
        "location": article["location"],
        "embedding": article["embedding"],
    }

def listArticles(articles)-> list:
    return [indArticle(article) for article in articles]
