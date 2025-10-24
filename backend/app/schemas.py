from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ReviewIn(BaseModel):
    platform: str
    business_id: str
    business_name: str
    review_id: str
    author: Optional[str]
    rating: Optional[float]
    text: Optional[str]
    date: Optional[datetime]
    url: Optional[str]
    raw_html: Optional[str]


class ReviewOut(ReviewIn):
    id: int
    analyzed_sentiment: Optional[str]
    tags: Optional[str]

    class Config:
        orm_mode = True
