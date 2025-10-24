from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from .db import Base
import datetime


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, index=True)
    business_id = Column(String, index=True)
    business_name = Column(String)
    review_id = Column(String, unique=True, index=True)
    author = Column(String)
    rating = Column(Float)
    text = Column(Text)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    url = Column(String)
    raw_html = Column(Text)
    analyzed_sentiment = Column(String, nullable=True)
    tags = Column(String, nullable=True)
