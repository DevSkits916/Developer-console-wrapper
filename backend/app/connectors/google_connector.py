"""Placeholder module for Google Business Profile API integration."""

import logging
import os

logger = logging.getLogger(__name__)


def fetch_reviews_for_location(location_id: str, api_key: str | None = None):
    """Fetch reviews for a Google Business Profile location via the official API."""
    _ = os.getenv("GOOGLE_API_KEY", api_key)
    raise NotImplementedError(
        "Plug in your Google Business Profile API client implementation here."
    )
