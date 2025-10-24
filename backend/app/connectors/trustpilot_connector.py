"""Read-only Trustpilot connector."""

import logging

from bs4 import BeautifulSoup

from ..utils import human_delay, safe_get

logger = logging.getLogger(__name__)


def fetch_reviews_for_business(business_slug: str):
    url = f"https://www.trustpilot.com/review/{business_slug}"
    reviews = []
    try:
        html = safe_get(url)
        soup = BeautifulSoup(html, "html.parser")
        for block in soup.select("section.review"):
            text = block.get_text(" ", strip=True)
            reviews.append({"text": text, "raw_html": str(block)})
        human_delay(2, 5)
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("trustpilot fetch error: %s", exc)
    return reviews
