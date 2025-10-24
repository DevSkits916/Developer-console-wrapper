"""Simulation endpoints for safe testing."""

from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/simulate", tags=["simulate"])


class SimPost(BaseModel):
    business_id: str
    platform: str
    text: str
    rating: int


@router.post("/post")
def simulate_post(payload: SimPost):
    return {
        "status": "ok",
        "platform": payload.platform,
        "business_id": payload.business_id,
        "posted_text": payload.text,
        "posted_rating": payload.rating,
        "posted_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "note": "This is a simulation. No external sites were contacted.",
    }
