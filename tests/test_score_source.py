"""score_source: schema, migration on legacy DBs, and the fallback path."""
import sqlite3
import types

import pytest

from brain import __main__ as cli
from brain import db
from tests.conftest import item

LEGACY_SCHEMA = """
CREATE TABLE items (
    id TEXT PRIMARY KEY, feed TEXT, category TEXT, title TEXT, url TEXT,
    published INTEGER, snippet TEXT, lane TEXT, score REAL, tldr TEXT,
    starred INTEGER DEFAULT 0, scored_at INTEGER);
CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT);
"""


def make_legacy(path):
    con = sqlite3.connect(path)
    con.executescript(LEGACY_SCHEMA)
    con.executemany(
        "INSERT INTO items (id, title, lane, score, scored_at) VALUES (?,?,?,?,?)",
        [("a/1", "model or fallback?", "tech", 7.0, 1),
         ("a/2", "real score", "tech", 8.0, 1),
         ("stocklake/CPI/2026-01-01", "CPI", "markets", 6.5, 1)])
    con.commit()
    con.close()


def sources(con):
    return {r["id"]: r["score_source"] for r in con.execute("SELECT id, score_source FROM items")}


def test_new_db_has_column(tmp_db):
    con = db.connect()
    assert "score_source" in {r[1] for r in con.execute("PRAGMA table_info(items)")}


def test_migration_on_legacy_db(tmp_db):
    make_legacy(tmp_db)
    con = db.connect()
    # only the provable label is backfilled; nothing is guessed
    assert sources(con) == {"a/1": None, "a/2": None, "stocklake/CPI/2026-01-01": "lake"}
    # data untouched
    assert con.execute("SELECT score FROM items WHERE id='a/1'").fetchone()[0] == 7.0


def test_migration_is_idempotent(tmp_db):
    make_legacy(tmp_db)
    db.connect().close()
    con = db.connect()        # second connect must not fail on ALTER TABLE
    db.migrate(con)
    assert sum(1 for r in con.execute("PRAGMA table_info(items)") if r[1] == "score_source") == 1


def test_upsert_records_source_and_rejects_unknown(tmp_db):
    con = db.connect()
    db.upsert_item(con, item(id="m"), "tech", 5.0, "t")
    db.upsert_item(con, item(id="f"), "other", 7.0, "", score_source="fallback")
    assert sources(con) == {"m": "model", "f": "fallback"}
    db.upsert_item(con, item(id="f"), "tech", 6.0, "rescored")   # rescore overwrites label
    assert sources(con)["f"] == "model"
    with pytest.raises(ValueError):
        db.upsert_item(con, item(id="z"), "tech", 5.0, "t", score_source="guess")


class FakeClient:
    def __init__(self, unread=(), starred=()):
        self._unread, self._starred = list(unread), list(starred)

    def unread(self, **kw):
        return iter(self._unread)

    def starred(self):
        return iter(self._starred)


def test_run_labels_fallback_and_logs(tmp_db, monkeypatch, capsys):
    good = item(id="u/1", title="Unread news")
    starred_ok = item(id="s/ok", title="Starred fine")
    starred_bad = item(id="s/bad", title="Starred broken")

    def fake_score(it, prompt):
        if it["id"] == "s/bad":
            raise TimeoutError("ollama timed out")
        return {"score": 8.0, "lane": "tech", "tldr": "ok"}

    monkeypatch.setattr(cli.freshrss, "Client",
                        lambda: FakeClient([good], [starred_ok, starred_bad]))
    monkeypatch.setattr(cli.score, "score_item", fake_score)
    monkeypatch.setattr(cli.stocklake, "ingest", lambda con: 0)
    cli.cmd_run(types.SimpleNamespace(hours=48, limit=10))

    con = db.connect()
    rows = {r["id"]: dict(r) for r in con.execute("SELECT * FROM items")}
    assert rows["u/1"]["score_source"] == "model"
    assert rows["s/ok"]["score_source"] == "model"
    assert rows["s/bad"]["score_source"] == "fallback"
    assert rows["s/bad"]["score"] == cli.FALLBACK_SCORE
    assert rows["s/bad"]["starred"] == 1
    out = capsys.readouterr()
    assert "scoring failed for starred Starred broken" in out.err
    assert "(1 fallback scores)" in out.out


def test_run_skips_noise_before_scoring(tmp_db, monkeypatch):
    scored = []
    monkeypatch.setattr(cli.freshrss, "Client", lambda: FakeClient(
        [item(id="n/1", title="b6032"), item(id="n/2", title="trunk/abc"),
         item(id="n/3", title="Real", url="https://example.com/x")]))
    monkeypatch.setattr(cli.score, "score_item",
                        lambda it, p: scored.append(it["id"]) or {"score": 5.0, "lane": "tech", "tldr": ""})
    monkeypatch.setattr(cli.stocklake, "ingest", lambda con: 0)
    cli.cmd_run(types.SimpleNamespace(hours=48, limit=10))
    assert scored == ["n/3"]
