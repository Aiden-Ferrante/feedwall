"""Stocklake cross-feed: ingest recent lake signals as briefing items.

Pulls GET /api/whatsnew from a local Stocklake data service (:8420) — series
with fresh prints in the last N days — and stores them as pre-scored
markets-lane items (score_source='lake'). No LLM pass: these are curated data
series, so freshness IS the signal.

Stocklake is optional and often stopped. That is fine, but it must be *visible*:
every failure (unreachable, bad JSON, unexpected payload shape, malformed rows)
is logged to stderr. An earlier version returned 0 on any exception, and the
cross-feed landed zero items over its whole life without ever saying so.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request

from . import db

STOCKLAKE_URL = os.environ.get("FEEDWALL_STOCKLAKE_URL", "http://localhost:8420")
BASE_SCORE = 6.5  # notable-but-not-headline; briefing shows >= 6 in lanes


def _log(msg: str) -> None:
    print(f"  ! stocklake: {msg}", file=sys.stderr)


def ingest(con, days: int = 3) -> int:
    url = f"{STOCKLAKE_URL}/api/whatsnew?days={days}"
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            payload = json.loads(r.read().decode())
    except urllib.error.URLError as e:
        _log(f"unreachable at {url} ({e.reason}); 0 lake signals this run")
        return 0
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        _log(f"non-JSON response from {url}: {e}")
        return 0
    except Exception as e:  # noqa: BLE001 — log anything else, never hide it
        _log(f"request to {url} failed: {type(e).__name__}: {e}")
        return 0
    if not isinstance(payload, dict) or "rows" not in payload:
        keys = sorted(payload) if isinstance(payload, dict) else type(payload).__name__
        _log(f"unexpected payload shape from {url}: no 'rows' key (got {keys})")
        return 0
    rows = payload["rows"] or []
    known = db.known_ids(con)
    added = malformed = 0
    for row in rows:
        series = str(row.get("series", "")).strip() if isinstance(row, dict) else ""
        date = str(row.get("date", ""))[:10] if isinstance(row, dict) else ""
        if not series or not date:
            malformed += 1
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
        if item["id"] in known:
            continue
        db.upsert_item(con, item, "markets", BASE_SCORE,
                       f"Fresh {series} data landed in the lake ({date}).",
                       score_source="lake")
        known.add(item["id"])
        added += 1
    if malformed:
        _log(f"skipped {malformed} of {len(rows)} rows missing series/date")
    return added
