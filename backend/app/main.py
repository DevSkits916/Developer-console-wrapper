"""FastAPI entry point."""

import logging

from fastapi import Depends, FastAPI, HTTPException

from .db import Base, SessionLocal, engine
from .models import Review
from .schemas import ReviewIn, ReviewOut
from .simulate import router as simulate_router
from .tasks import start_scheduler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Review Agent (PoC)")

Base.metadata.create_all(bind=engine)
app.include_router(simulate_router)


@app.get("/reviews", response_model=list[ReviewOut])
def list_reviews(limit: int = 50):
    db = SessionLocal()
    try:
        return (
            db.query(Review)
            .order_by(Review.date.desc())
            .limit(limit)
            .all()
        )
    finally:
        db.close()


@app.post("/ingest", response_model=ReviewOut)
def ingest_review(item: ReviewIn):
    db = SessionLocal()
    try:
        existing = db.query(Review).filter_by(review_id=item.review_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="already exists")
        review = Review(**item.dict())
        db.add(review)
        db.commit()
        db.refresh(review)
        return review
    finally:
        db.close()


start_scheduler()
