"""Deterministic pre-scoring skip filters (brain.__main__.skip_reason)."""
import pytest

from brain.__main__ import skip_reason
from tests.conftest import item


@pytest.mark.parametrize("title,url,reason", [
    ("trunk/abc123", "https://github.com/x", "ci/nightly tag"),
    ("ciflow/inductor/123", "https://github.com/x", "ci/nightly tag"),
    ("Nightly/2026-01-01", "https://github.com/x", "ci/nightly tag"),
    ("b6032", "https://github.com/x", "build-number release"),
    ("  b123 ", "https://github.com/x", "build-number release"),
    ("Post", "https://metr.org/es/blog/x", "translated duplicate"),
    ("Post", "https://metr.org/zh-Hans/blog/x", "translated duplicate"),
    ("", "https://example.com", "no title"),
    ("   ", "https://example.com", "no title"),
])
def test_skipped(title, url, reason):
    assert skip_reason(item(title=title, url=url)) == reason


@pytest.mark.parametrize("title,url", [
    ("v2.5.0 released", "https://github.com/x"),
    ("b12", "https://github.com/x"),            # too short to be a build number
    ("b6032 and friends", "https://github.com/x"),
    ("Post", "https://metr.org/blog/es-tax"),   # locale must be a path prefix
    ("Post", "https://example.com/en/blog"),    # English is kept
])
def test_kept(title, url):
    assert skip_reason(item(title=title, url=url)) is None
