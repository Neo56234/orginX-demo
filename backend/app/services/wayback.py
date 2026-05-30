import logging
import httpx
from typing import Optional
from datetime import datetime

logger = logging.getLogger("originx.services.wayback")

CDX_API_URL = "http://web.archive.org/cdx/search/cdx"


def get_earliest_archive(url: str) -> Optional[dict]:
    """
    Query Wayback Machine CDX API for the earliest archived snapshot of a URL.
    Free API — no key required.

    Returns:
    {
        "timestamp": "20190315142233",
        "datetime": datetime,
        "snapshot_url": "https://web.archive.org/web/20190315142233/{url}",
        "status_code": "200",
    }
    or None if no archive found.

    Phase 1 implementation:
    - Query CDX API with limit=1&output=json&fl=timestamp,statuscode&filter=statuscode:200
    - Parse earliest result
    - Return structured dict
    """

    params = {
        "url": url,
        "output": "json",
        "fl": "timestamp,statuscode",
        "filter": "statuscode:200",
        "limit": 1,
        "from": "",
    }

    # ── Phase 1: uncomment and test ────────────────────────────────────────
    try:
        resp = httpx.get(CDX_API_URL, params=params, timeout=10)
        resp.raise_for_status()
        
        # httpx .json() fails if response is empty, check text first
        if not resp.text.strip():
            return None
            
        data = resp.json()
        if len(data) < 2:   # first row is header
            return None
        row = data[1]
        ts = row[0]
        dt = datetime.strptime(ts, "%Y%m%d%H%M%S")
        return {
            "timestamp": ts,
            "datetime": dt,
            "snapshot_url": f"https://web.archive.org/web/{ts}/{url}",
            "status_code": row[1],
        }
    except Exception as e:
        logger.warning("Wayback CDX query failed for %s: %s", url, e)
        return None
    # ──────────────────────────────────────────────────────────────────────
