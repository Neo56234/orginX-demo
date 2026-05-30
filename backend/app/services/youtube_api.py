import logging
import re
import httpx
from typing import Optional
from app.config import get_settings

logger = logging.getLogger("originx.services.youtube_api")

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEOS_URL = "https://www.googleapis.com/youtube/v3/videos"


def extract_video_id(url: str) -> Optional[str]:
    """Extract YouTube video ID from a URL."""
    m = re.search(r"(?:v=|youtu\.be/|/embed/|/v/)([A-Za-z0-9_-]{11})", url)
    return m.group(1) if m else None


def get_video_metadata(video_url: str) -> Optional[dict]:
    """
    Fetch title, channel, description, and publish date for a specific YouTube video.
    Returns None if the API key is missing or the request fails.
    """
    settings = get_settings()
    if not settings.youtube_api_key:
        return None

    video_id = extract_video_id(video_url)
    if not video_id:
        return None

    params = {
        "part": "snippet",
        "id": video_id,
        "key": settings.youtube_api_key,
    }
    try:
        resp = httpx.get(YOUTUBE_VIDEOS_URL, params=params, timeout=10)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        if not items:
            return None
        s = items[0]["snippet"]
        return {
            "video_id": video_id,
            "title": s.get("title", ""),
            "channel_title": s.get("channelTitle", ""),
            "description": (s.get("description") or "")[:500],
            "published_at": s.get("publishedAt", ""),
        }
    except Exception as e:
        logger.warning("YouTube metadata fetch failed for %s: %s", video_url, e)
        return None


def search_duplicate_videos(query: str, max_results: int = 5) -> list[dict]:
    """
    Search YouTube for duplicate/related videos using a text query.
    Uses YouTube Data API v3 (free tier: 10,000 units/day).

    Returns list of:
    {
        "video_id": str,
        "title": str,
        "published_at": str,   # ISO datetime
        "channel_title": str,
        "url": str,
    }

    Phase 1 implementation:
    - Build query from OCR text + claimed context
    - Call YouTube search endpoint with order=date
    - Return sorted results (oldest first)
    """
    settings = get_settings()

    if not settings.youtube_api_key:
        logger.warning("YouTube API key not set — skipping search")
        return []

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "order": "date",
        "maxResults": max_results,
        "key": settings.youtube_api_key,
    }

    # ── Phase 1: uncomment and test ────────────────────────────────────────
    try:
        resp = httpx.get(YOUTUBE_SEARCH_URL, params=params, timeout=10)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        return [
            {
                "video_id": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "published_at": item["snippet"]["publishedAt"],
                "channel_title": item["snippet"]["channelTitle"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            }
            for item in items
            if item.get("id", {}).get("videoId")
        ]
    except Exception as e:
        logger.warning("YouTube API search failed: %s", e)
        return []
    # ──────────────────────────────────────────────────────────────────────
