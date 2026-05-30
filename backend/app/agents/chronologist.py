import logging
import re
import redis
from app.agents.base import BaseAgent

logger = logging.getLogger("originx.agent.chronologist")


def _make_search_query(claimed_context: str) -> str:
    """
    Convert a raw Bengali claim string into a cleaner YouTube search query.
    Removes trailing year-in-parens (২০২৬)/(2026), strips punctuation, truncates.
    """
    from app.utils.language import normalize_bengali_numerals
    cleaned = normalize_bengali_numerals(claimed_context)
    cleaned = re.sub(r'\(\d{4}\)\s*$', '', cleaned).strip()  # remove trailing (2026)
    cleaned = cleaned.rstrip('!?।')                           # strip sentence-end punctuation
    if len(cleaned) > 80:
        cleaned = cleaned[:80].rsplit(' ', 1)[0]              # truncate at word boundary
    return cleaned.strip() or claimed_context[:80]


class ChronologistAgent(BaseAgent):
    """
    🕐 Chronologist — determines WHEN the video was actually filmed.

    Signals (Phase 1 implementation):
    - Wayback Machine CDX API: earliest archive date
    - YouTube Data API: earliest upload date of matching video
    - pHash match against local known_cases DB (with known dates)
    - OCR date/timestamp extraction from frames
    - Platform metadata (upload date from yt-dlp)

    Output: { earliest_date, earliest_source_url, confidence, evidence[] }
    """

    name = "chronologist"

    def __init__(self, investigation_id: str, redis_client: redis.Redis):
        super().__init__(investigation_id, redis_client)

    def run(self, frames: list[str], context: dict) -> dict:
        from app.services.wayback import get_earliest_archive
        from app.services.youtube_api import search_duplicate_videos, get_video_metadata

        self.emit_started()
        self.emit_progress(0.1, "Fetching video source metadata...")

        video_url = context.get("video_url", "")
        claimed_context = context.get("claimed_context", "")
        evidence = []

        earliest_date = None
        earliest_url = None

        # 0. YouTube video metadata — channel name is strong geo evidence
        if video_url:
            meta = get_video_metadata(video_url)
            if meta:
                channel = meta.get("channel_title", "")
                title = meta.get("title", "")
                pub_date = (meta.get("published_at") or "")[:10]
                finding = {
                    "type": "youtube_metadata",
                    "description": f'Source video: "{title}" — channel: "{channel}" — published: {pub_date}',
                    "weight": "high",
                    "channel": channel,
                    "title": title,
                    "date": pub_date,
                }
                evidence.append(finding)
                self.emit_finding(finding)
                if pub_date:
                    earliest_date = pub_date
                    earliest_url = video_url

        # 1. Wayback Machine
        if video_url:
            self.emit_progress(0.3, "Querying Wayback Machine for earliest archive...")
            wb_result = get_earliest_archive(video_url)
            if wb_result:
                earliest_date = wb_result["datetime"].strftime("%Y-%m-%d")
                earliest_url = wb_result["snapshot_url"]
                finding = {
                    "type": "wayback_hit",
                    "description": f"Wayback Machine: archived {earliest_date} — web.archive.org",
                    "weight": "high",
                    "date": earliest_date,
                    "url": earliest_url,
                }
                evidence.append(finding)
                self.emit_finding(finding)
            else:
                self.emit_finding({
                    "type": "wayback_miss",
                    "description": "Wayback Machine: no archive found for this URL.",
                    "weight": "low",
                })

        # 2. YouTube Search
        if claimed_context and claimed_context != "No context provided":
            self.emit_progress(0.6, "Searching YouTube for earlier uploads...")
            yt_results = search_duplicate_videos(_make_search_query(claimed_context))
            if yt_results:
                yt_results_sorted = sorted(yt_results, key=lambda x: x.get("published_at") or "")
                # Emit top-3 earliest results individually
                for r in yt_results_sorted[:3]:
                    yt_date = (r.get("published_at") or "")[:10] or "unknown date"
                    title = (r.get("title") or "Untitled")[:65]
                    finding = {
                        "type": "youtube_earliest",
                        "description": f'YouTube: "{title}" — uploaded {yt_date}',
                        "weight": "medium",
                        "url": r.get("url", ""),
                        "date": yt_date,
                    }
                    evidence.append(finding)
                    self.emit_finding(finding)

                oldest = yt_results_sorted[0]
                yt_earliest = (oldest.get("published_at") or "")[:10]
                if yt_earliest and (not earliest_date or yt_earliest < earliest_date):
                    earliest_date = yt_earliest
                    earliest_url = oldest.get("url", "")
            else:
                self.emit_finding({
                    "type": "youtube_miss",
                    "description": "YouTube: no earlier uploads found matching this context.",
                    "weight": "low",
                })

        output = {
            "earliest_date": earliest_date,
            "earliest_source_url": earliest_url,
            "confidence": 0.8 if earliest_date else 0.0,
            "evidence": evidence,
        }

        self.emit_complete(output)
        logger.info("Chronologist complete — investigation=%s", self.investigation_id)
        return output
