from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Event(BaseModel):
    eventHeadline: str
    location: str
    leftSummary: str
    centerSummary: str
    rightSummary: str
    lCount: int
    cCount: int
    rCount: int
    totalArticles: int
    centroid_embedding: str
    severity_score: int
    stability_index: int
    # publishedDate will be set automatically
