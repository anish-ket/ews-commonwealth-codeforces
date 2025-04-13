from fastapi import APIRouter, Depends, HTTPException
from api.models.articles import Article
from api.models.events import Event
from api.config.database import get_db

router = APIRouter()

@router.post("/articles/")
async def create_article(article: Article, db=Depends(get_db)):
    # Pydantic ensures all fields are provided (non-null)
    article_dict = article.dict(by_alias=True, exclude={"id"})  # Exclude id for insertion
    try:
        result = db["MainArticles"].insert_one(article_dict)
        return {"id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create article: {str(e)}")

@router.get("/articles/{id}")
async def get_article(id: str, db=Depends(get_db)):
    article = db["MainArticles"].find_one({"_id": id})
    if article:
        return article
    raise HTTPException(status_code=404, detail="Article not found")

@router.post("/events/")
async def create_event(event: Event, db=Depends(get_db)):
    # Pydantic ensures all fields are provided (non-null)
    event_dict = event.dict(by_alias=True, exclude={"id"})  # Exclude id for insertion
    try:
        result = db["MainEvents"].insert_one(event_dict)
        return {"id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create event: {str(e)}")

@router.get("/events/{id}")
async def get_event(id: str, db=Depends(get_db)):
    event = db["MainEvents"].find_one({"_id": id})
    if event:
        return event
    raise HTTPException(status_code=404, detail="Event not found")
