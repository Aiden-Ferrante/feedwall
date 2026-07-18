"""SQLite store for scored items (stdlib only)."""

import sqlite3
import time

from . import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
    id        TEXT PRIMARY KEY,
    feed      TEXT,
    category  TEXT,
    title     TEXT,
    url       TEXT,
    published INTEGER,
    snippet   TEXT,
    lane      TEXT,
    score     REAL,
    tldr      TEXT,
    starred   INTEGER DEFAULT 0,
    scored_at INTEGER
);
CREATE INDEX IF NOT EXISTS idx_items_pub ON items(published);
CREATE INDEX IF NOT EXISTS idx_items_score ON items(score);
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
"""


def connect() -> sqlite3.Connection:
    config.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(config.DB_PATH)
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    return con


def known_ids(con) -> set:
    return {r["id"] for r in con.execute("SELECT id FROM items")}


def upsert_item(con, item: dict, lane: str, score: float, tldr: str):
    con.execute(
        """INSERT INTO items (id, feed, category, title, url, published, snippet,
                              lane, score, tldr, scored_at)
           VALUES (:id, :feed, :category, :title, :url, :published, :snippet,
                   :lane, :score, :tldr, :scored_at)
           ON CONFLICT(id) DO UPDATE SET lane=:lane, score=:score, tldr=:tldr,
                                         scored_at=:scored_at""",
        {**item, "lane": lane, "score": score, "tldr": tldr,
         "scored_at": int(time.time())},
    )


def mark_starred(con, item_id: str):
    con.execute("UPDATE items SET starred=1 WHERE id=?", (item_id,))


def get_meta(con, key: str, default=None):
    row = con.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
    return row["value"] if row else default


def set_meta(con, key: str, value: str):
    con.execute(
        "INSERT INTO meta (key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value),
    )


# Recency = MAX(published, scored_at): "new to the reader", not "new to the
# publisher". arXiv feed items carry submission timestamps that lag their
# public announcement by 1-3 days, so filtering on published alone would
# silently drop freshly-announced papers from the daily window.
def top_since(con, since_unix: int, limit: int = 50):
    return con.execute(
        "SELECT * FROM items WHERE MAX(published, scored_at) >= ? "
        "ORDER BY score DESC, published DESC LIMIT ?",
        (since_unix, limit),
    ).fetchall()


def lane_best_since(con, lane: str, since_unix: int):
    return con.execute(
        "SELECT * FROM items WHERE lane = ? AND MAX(published, scored_at) >= ? "
        "ORDER BY score DESC LIMIT 1",
        (lane, since_unix),
    ).fetchone()


def lane_top_since(con, lane: str, since_unix: int, limit: int):
    return con.execute(
        "SELECT * FROM items WHERE lane = ? AND MAX(published, scored_at) >= ? "
        "AND score >= 6.0 ORDER BY score DESC LIMIT ?",
        (lane, since_unix, limit),
    ).fetchall()


def starred_examples(con, limit: int = 8):
    return con.execute(
        "SELECT title, lane FROM items WHERE starred=1 ORDER BY published DESC LIMIT ?",
        (limit,),
    ).fetchall()
