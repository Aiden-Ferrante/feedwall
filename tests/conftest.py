import io
import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from brain import config  # noqa: E402

DEMO_DB = ROOT / "examples" / "demo.sqlite"


@pytest.fixture
def tmp_db(tmp_path, monkeypatch):
    """Point the brain at an empty DB in a temp dir."""
    path = tmp_path / "curated.sqlite"
    monkeypatch.setattr(config, "DB_PATH", path)
    return path


@pytest.fixture
def demo_db(tmp_path, monkeypatch):
    """A private copy of the committed synthetic demo DB."""
    path = tmp_path / "demo.sqlite"
    shutil.copy(DEMO_DB, path)
    monkeypatch.setattr(config, "DB_PATH", path)
    return path


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        self.close()


def fake_json_response(obj) -> FakeResponse:
    return FakeResponse(json.dumps(obj).encode())


def item(**kw) -> dict:
    base = {"id": "x/1", "feed": "Feed", "category": "Tech News", "title": "A title",
            "url": "https://example.com/a", "published": 1_700_000_000,
            "snippet": "snippet"}
    base.update(kw)
    return base
