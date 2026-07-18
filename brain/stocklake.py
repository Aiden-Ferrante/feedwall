"""Stocklake cross-feed: ingest recent lake signals as briefing items.

Pulls GET /api/whatsnew from the local Stocklake (:8420) — series with fresh
prints in the last N days — and stores them as pre-scored markets-lane items.
No LLM pass: these are the user's own curated data series, so freshness IS the
signal. Skips silently when Stocklake isn't running (it's often stopped).
"""

import json
import time
import urllib.request

from . import db

STOCKLAKE_URL = "http://localhost:8420"
BASE_SCORE = 6.5  # notable-but-not-headline; briefing shows >= 6 in lanes


def ingest(con, days: int = 3) -> int:
    try:
        with urllib.request.urlopen(
            f"{STOCKLAKE_URL}/api/whatsnew?days={days}", timeout=10
        ) as r:
            rows = json.loads(r.read().decode()).get("rows", [])
    except Exception:
        return 0  # lake down or unreachable — not an error, just no signal
    added = 0
    for row in rows:
        series = str(row.get("series", "")).strip()
        date = str(row.get("date", ""))[:10]
        if not series or not date:
            continue
        item = {
            "id": f"stocklake/{series}/{date}",
            "feed": "Stocklake",
            "category": "Stocklake",
            "title": f"{series}: new print {row.get('value', '')} ({date})",
            "url": f"{STOCKLAKE_URL}/",
            "published": int(time.time()),
            "snippet": f"source={row.get('source', '')}",
        }
        if item["id"] in db.known_ids(con):
            continue
        db.upsert_item(con, item, "markets", BASE_SCORE,
                       f"Fresh {series} data landed in the lake ({date}).")
        added += 1
    return added
