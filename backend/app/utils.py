import random
import time
import requests


def human_delay(min_s: float = 2, max_s: float = 6) -> None:
    time.sleep(random.uniform(min_s, max_s))


def safe_get(url, headers=None, timeout: int = 15):
    headers = headers or {"User-Agent": "ReviewAgent/1.0 (+contact@example.com)"}
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.text


def normalize_review(raw, platform: str):
    return {
        "platform": platform,
        "business_id": raw.get("business_id"),
        "business_name": raw.get("business_name"),
        "review_id": raw.get("review_id"),
        "author": raw.get("author"),
        "rating": float(raw.get("rating", 0)) if raw.get("rating") else None,
        "text": raw.get("text"),
        "date": raw.get("date"),
        "url": raw.get("url"),
        "raw_html": raw.get("raw_html"),
    }
