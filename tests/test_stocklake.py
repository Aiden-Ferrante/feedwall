"""Stocklake ingest: failures are logged, never silent; rows are labelled lake."""
import urllib.error

from brain import db, stocklake
from tests.conftest import FakeResponse, fake_json_response


def patch_urlopen(monkeypatch, fn):
    monkeypatch.setattr(stocklake.urllib.request, "urlopen", fn)


def test_unreachable_is_logged(tmp_db, monkeypatch, capsys):
    def refuse(*a, **k):
        raise urllib.error.URLError(ConnectionRefusedError(111, "Connection refused"))
    patch_urlopen(monkeypatch, refuse)
    assert stocklake.ingest(db.connect()) == 0
    err = capsys.readouterr().err
    assert "stocklake: unreachable" in err and "Connection refused" in err


def test_non_json_is_logged(tmp_db, monkeypatch, capsys):
    patch_urlopen(monkeypatch, lambda *a, **k: FakeResponse(b"<html>oops</html>"))
    assert stocklake.ingest(db.connect()) == 0
    assert "non-JSON response" in capsys.readouterr().err


def test_wrong_shape_is_logged(tmp_db, monkeypatch, capsys):
    patch_urlopen(monkeypatch, lambda *a, **k: fake_json_response({"data": []}))
    assert stocklake.ingest(db.connect()) == 0
    assert "no 'rows' key (got ['data'])" in capsys.readouterr().err


def test_good_rows_stored_as_lake_and_malformed_logged(tmp_db, monkeypatch, capsys):
    payload = {"rows": [
        {"series": "CPI", "date": "2026-01-14T00:00:00", "value": 3.1, "source": "bls"},
        {"series": "CPI", "date": "2026-01-14", "value": 3.1},     # same id: deduped
        {"series": "", "date": "2026-01-14"},                      # malformed
        {"date": "2026-01-14"},                                     # malformed
    ]}
    patch_urlopen(monkeypatch, lambda *a, **k: fake_json_response(payload))
    con = db.connect()
    assert stocklake.ingest(con) == 1
    row = con.execute("SELECT * FROM items").fetchone()
    assert row["id"] == "stocklake/CPI/2026-01-14"
    assert row["score_source"] == "lake" and row["lane"] == "markets"
    assert "skipped 2 of 4 rows" in capsys.readouterr().err


def test_empty_rows_is_quiet(tmp_db, monkeypatch, capsys):
    # a reachable lake with nothing new is not an error
    patch_urlopen(monkeypatch, lambda *a, **k: fake_json_response({"rows": []}))
    assert stocklake.ingest(db.connect()) == 0
    assert capsys.readouterr().err == ""
