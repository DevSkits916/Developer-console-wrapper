"""Background fetch tasks."""

import logging

from apscheduler.schedulers.background import BackgroundScheduler

from .connectors import trustpilot_connector, yelp_connector
from .db import SessionLocal
from .models import Review
from .utils import normalize_review

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def fetch_and_store_yelp(business_url: str):
    session = SessionLocal()
    try:
        raw_list = yelp_connector.fetch_reviews_for_business(business_url)
        for raw in raw_list:
            norm = normalize_review(
                {
                    "business_id": business_url,
                    "business_name": None,
                    "review_id": hash(raw.get("text")),
                    "author": None,
                    "rating": None,
                    "text": raw.get("text"),
                    "date": None,
                    "url": business_url,
                    "raw_html": raw.get("raw_html"),
                },
                "yelp",
            )
            existing = session.query(Review).filter_by(review_id=norm["review_id"]).first()
            if existing:
                continue
            session.add(Review(**norm))
        session.commit()
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("task error: %s", exc)
    finally:
        session.close()


def start_scheduler():
    scheduler.add_job(
        lambda: fetch_and_store_yelp("https://www.yelp.com/biz/some-business"),
        "interval",
        minutes=60,
        id="yelp_poc",
        replace_existing=True,
    )
    scheduler.start()
