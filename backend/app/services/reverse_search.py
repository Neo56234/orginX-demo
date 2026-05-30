import logging
import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger("originx.services.reverse_search")

YANDEX_UPLOAD_URL = "https://yandex.com/images/search"

def yandex_reverse_search(image_path: str) -> list[dict]:
    """
    Best-effort reverse image search via Yandex.
    Returns empty list on any failure (CAPTCHA, timeout, parse error).
    """
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()

        # Upload image to Yandex
        with httpx.Client(timeout=15, follow_redirects=True) as client:
            resp = client.post(
                YANDEX_UPLOAD_URL,
                params={"rpt": "imageview", "format": "json"},
                files={"upfile": ("frame.jpg", image_data, "image/jpeg")},
                headers={"User-Agent": "Mozilla/5.0"},
            )

        if resp.status_code != 200:
            logger.warning("Yandex reverse search returned status %d", resp.status_code)
            return []

        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        for item in soup.select(".serp-item")[:5]:
            link = item.select_one("a[href]")
            title = item.select_one(".serp-item__title")
            if link:
                results.append({
                    "url": link.get("href", ""),
                    "title": title.get_text(strip=True) if title else "",
                    "source_domain": "",
                    "snippet": "",
                })
        return results

    except Exception as e:
        logger.warning("Yandex reverse search failed (best-effort): %s", e)
        return []
