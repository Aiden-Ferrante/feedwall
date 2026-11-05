"""Build examples/demo.sqlite: a small, fully synthetic scored-items DB.

Every row is invented for the demo (example.com URLs, "Demo" feeds); none of it
is real scoring output. It exists so a fresh clone can render a real briefing:

    FEEDWALL_DB=examples/demo.sqlite python3 -m briefing.render --stdout --as-of 2026-01-15T07:00

Deterministic: rerunning produces the same rows. Run from the repo root:
    python3 examples/make_demo_db.py
"""

import datetime
import os
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "examples" / "demo.sqlite"
AS_OF = datetime.datetime(2026, 1, 15, 7, 0, tzinfo=datetime.timezone.utc)

# (id, feed, category, title, lane, score, tldr, hours_before_as_of, starred, source)
ROWS = [
    ("demo/1", "Demo Lab Blog", "AI/ML — Blogs & Newsletters",
     "Demo: a 7B model matches a 70B baseline on a synthetic reasoning suite",
     "ai-ml", 9.0, "Synthetic example item: a small model reports parity with a larger one on an invented benchmark.", 3, 0, "model"),
    ("demo/2", "Demo Systems Notes", "Discovered — GPU/systems practitioners",
     "Demo: fusing the KV-cache write into the attention kernel",
     "systems", 8.0, "Synthetic example item: a kernel write-up describing one fused memory pass.", 5, 0, "model"),
    ("demo/3", "Demo Central Bank", "Markets & Econ",
     "Demo: policy rate held, statement language unchanged",
     "markets", 7.0, "Synthetic example item: a rate decision with no change in guidance.", 8, 0, "model"),
    ("demo/4", "Demo Evals Org", "Benchmarks & Evals",
     "Demo: leaderboard v2 adds a contamination check",
     "benchmarks", 8.0, "Synthetic example item: an invented leaderboard adds a held-out split.", 6, 0, "model"),
    ("demo/5", "Demo Starred Feed", "Tech News",
     "Demo: starred item the model failed to score",
     "other", 7.0, "", 4, 1, "fallback"),
    ("demo/6", "Demo Data Eng Blog", "Code & Launches",
     "Demo: a columnar format release with faster dictionary decoding",
     "data-eng", 6.5, "Synthetic example item: a file-format minor release.", 10, 0, "model"),
    ("demo/7", "Demo Tech Wire", "Tech News",
     "Demo: ten gadgets you won't believe",
     "tech", 2.0, "Synthetic example item: listicle with no information.", 2, 0, "model"),
    ("demo/p1", "Demo arXiv", "Papers",
     "Demo paper: speculative decoding with a learned draft-acceptance predictor",
     "papers", 9.0, "Synthetic example item: an invented paper on speculative decoding.", 12, 0, "model"),
    ("demo/p2", "Demo arXiv", "Papers",
     "Demo paper: a harness-agnostic benchmark for long-horizon coding agents",
     "papers", 7.0, "Synthetic example item: an invented agent benchmark paper.", 14, 0, "model"),
    ("stocklake/DEMO_SERIES/2026-01-14", "Stocklake", "Stocklake",
     "DEMO_SERIES: new print 3.1 (2026-01-14)",
     "markets", 6.5, "Fresh DEMO_SERIES data landed in the lake (2026-01-14).", 9, 0, "lake"),
    # outside the 24h window: must not appear
    ("demo/old", "Demo Lab Blog", "AI/ML — Blogs & Newsletters",
     "Demo: last week's news (outside the window)",
     "ai-ml", 10.0, "Synthetic example item that is too old for the window.", 24 * 7, 0, "model"),
]


def main() -> None:
    sys.path.insert(0, str(ROOT))
    os.environ["FEEDWALL_DB"] = str(OUT)
    if OUT.exists():
        OUT.unlink()
    from brain import db  # noqa: E402  (reads FEEDWALL_DB at import)
    con = db.connect()
    t0 = int(AS_OF.timestamp())
    for (id_, feed, cat, title, lane, score, tldr, hrs, starred, src) in ROWS:
        ts = t0 - hrs * 3600
        con.execute(
            "INSERT INTO items (id, feed, category, title, url, published, snippet, lane,"
            " score, tldr, starred, scored_at, score_source)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (id_, feed, cat, title, f"https://example.com/{id_}", ts,
             "Synthetic demo snippet.", lane, score, tldr, starred, ts, src),
        )
    con.commit()
    con.execute("VACUUM")
    con.close()
    print(f"wrote {len(ROWS)} synthetic rows -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
