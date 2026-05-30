import logging
import redis
from app.agents.base import BaseAgent

logger = logging.getLogger("originx.agent.tracer")


class TracerAgent(BaseAgent):
    """
    🔍 Tracer — finds every prior appearance of this video online.

    Signals (Phase 1 implementation):
    - Reverse image search: Yandex (automated HTTP, best effort)
    - InVID/WeVerify API
    - YouTube Data API duplicate search
    - pHash match against local known_cases DB

    Output: { appearances: [{url, date, platform, title}], evidence[] }
    """

    name = "tracer"

    def __init__(self, investigation_id: str, redis_client: redis.Redis):
        super().__init__(investigation_id, redis_client)

    def run(self, frames: list[str], context: dict) -> dict:
        from app.services.reverse_search import yandex_reverse_search
        from app.services.youtube_api import search_duplicate_videos

        self.emit_started()
        self.emit_progress(0.1, "Running reverse search across platforms...")

        appearances = []
        evidence = []
        claimed_context = context.get("claimed_context", "")

        # 1. Reverse Image Search (Best Effort)
        if frames:
            mid_frame = frames[len(frames) // 2]
            self.emit_progress(0.3, "Querying Yandex Reverse Image Search...")
            yandex_results = yandex_reverse_search(mid_frame)
            if yandex_results:
                for r in yandex_results[:5]:
                    url = r.get("url", "")
                    title = (r.get("title") or "Untitled")[:70]
                    date = r.get("date") or "unknown date"
                    try:
                        domain = url.split("/")[2] if url.startswith("http") else "web"
                    except IndexError:
                        domain = "web"
                    appearances.append({"url": url, "date": date, "platform": "Web", "title": title})
                    finding = {
                        "type": "reverse_search_hit",
                        "description": f'Visual match: "{title}" — {domain} ({date})',
                        "weight": "medium",
                        "url": url,
                    }
                    evidence.append(finding)
                    self.emit_finding(finding)
            else:
                self.emit_finding({
                    "type": "reverse_search_miss",
                    "description": "Yandex reverse search: no visual matches found.",
                    "weight": "low",
                })

        # 2. YouTube Duplicate Search
        if claimed_context and claimed_context != "No context provided":
            self.emit_progress(0.6, "Querying YouTube for duplicate videos...")
            yt_results = search_duplicate_videos(claimed_context)
            if yt_results:
                for r in yt_results[:4]:
                    pub = (r.get("published_at") or "")[:10] or "unknown date"
                    title = (r.get("title") or "Untitled")[:70]
                    appearances.append({"url": r["url"], "date": pub, "platform": "YouTube", "title": title})
                    finding = {
                        "type": "youtube_match",
                        "description": f'YouTube duplicate: "{title}" — published {pub}',
                        "weight": "high",
                        "url": r["url"],
                        "date": pub,
                    }
                    evidence.append(finding)
                    self.emit_finding(finding)
            else:
                self.emit_finding({
                    "type": "youtube_miss",
                    "description": "YouTube search: no duplicate videos found for this context.",
                    "weight": "low",
                })

        # Aggregate and sort
        valid_appearances = [a for a in appearances if a.get("date")]
        valid_appearances.sort(key=lambda x: x["date"])

        earliest_url = None
        earliest_date = None

        if valid_appearances:
            oldest = valid_appearances[0]
            earliest_url = oldest["url"]
            earliest_date = oldest["date"]

        output = {
            "appearances": appearances,
            "earliest_appearance_url": earliest_url,
            "earliest_appearance_date": earliest_date,
            "evidence": evidence,
        }

        self.emit_complete(output)
        logger.info("Tracer complete — investigation=%s", self.investigation_id)
        return output
