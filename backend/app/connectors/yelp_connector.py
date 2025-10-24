"""Read-only public fetcher for Yelp business pages."""

from bs4 import BeautifulSoup
import logging

from ..utils import human_delay, safe_get

logger = logging.getLogger(__name__)


def fetch_reviews_for_business(business_url: str, max_pages: int = 1):
    """Fetch public review snippets from Yelp business page(s)."""
    reviews = []
    try:
        html = safe_get(business_url)
        soup = BeautifulSoup(html, "html.parser")
        for node in soup.select("p.comment__09f24__gu0rG, span.raw__09f24__T4Ezm"):
            text = node.get_text(strip=True)
            if not text:
                continue
            reviews.append({"text": text, "raw_html": str(node)})
        human_delay(2, 4)
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("yelp fetch error: %s", exc)
    return reviews
