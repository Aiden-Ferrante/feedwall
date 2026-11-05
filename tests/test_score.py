"""Score parsing against a mocked Ollama /api/chat response (no network)."""
import json

import pytest

from brain import score
from tests.conftest import fake_json_response, item


def ollama_body(content):
    """Ollama non-streaming chat shape: the model's JSON arrives as a string."""
    if not isinstance(content, str):
        content = json.dumps(content)
    return {"model": "m", "message": {"role": "assistant", "content": content}, "done": True}


@pytest.fixture
def mock_ollama(monkeypatch):
    calls = []

    def install(content):
        def fake_urlopen(req, timeout=None):
            calls.append(json.loads(req.data.decode()))
            return fake_json_response(ollama_body(content))
        monkeypatch.setattr(score.urllib.request, "urlopen", fake_urlopen)
        return calls
    return install


def test_parses_valid_response(mock_ollama):
    mock_ollama({"score": 8.5, "lane": "systems", "tldr": "A kernel got faster."})
    out = score.score_item(item(), "sys")
    assert out == {"score": 8.5, "lane": "systems", "tldr": "A kernel got faster."}


def test_request_is_schema_constrained_and_thinking_off(mock_ollama):
    calls = mock_ollama({"score": 5, "lane": "tech", "tldr": "t"})
    score.score_item(item(category="Releases"), "SYSTEM PROMPT")
    payload = calls[0]
    assert payload["format"] == score.RESPONSE_SCHEMA
    assert payload["think"] is False
    assert payload["stream"] is False
    assert payload["messages"][0] == {"role": "system", "content": "SYSTEM PROMPT"}
    # category lane hint is passed to the model as a soft prior
    assert "(lane hint: systems)" in payload["messages"][1]["content"]


@pytest.mark.parametrize("raw,expected", [(14, 10.0), (-3, 0.0), ("7", 7.0)])
def test_score_is_clamped_to_0_10(mock_ollama, raw, expected):
    mock_ollama({"score": raw, "lane": "tech", "tldr": "t"})
    assert score.score_item(item(), "s")["score"] == expected


def test_unknown_lane_becomes_other(mock_ollama):
    mock_ollama({"score": 5, "lane": "astrology", "tldr": "t"})
    assert score.score_item(item(), "s")["lane"] == "other"


def test_missing_fields_get_safe_defaults(mock_ollama):
    mock_ollama({})
    assert score.score_item(item(), "s") == {"score": 0.0, "lane": "other", "tldr": ""}


def test_tldr_truncated(mock_ollama):
    mock_ollama({"score": 5, "lane": "tech", "tldr": "x" * 1000})
    assert len(score.score_item(item(), "s")["tldr"]) == 400


def test_non_json_content_raises(mock_ollama):
    # The caller (brain run) must see the failure; score_item never invents a score.
    mock_ollama("sorry, I can't do that")
    with pytest.raises(json.JSONDecodeError):
        score.score_item(item(), "s")


def test_papers_prompt_differs_and_includes_stars():
    stars = [{"title": "Loved paper", "lane": "papers"}]
    p = score.build_system_prompt(stars, papers=True)
    n = score.build_system_prompt(stars)
    assert "research-paper triage" in p and "news-curation" in n
    assert '"Loved paper" (papers)' in p
