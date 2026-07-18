"""Score items with a local Ollama model (stdlib only)."""

import json
import urllib.request

from . import config

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "score": {"type": "number"},
        "lane": {"type": "string", "enum": config.LANES + ["other"]},
        "tldr": {"type": "string"},
    },
    "required": ["score", "lane", "tldr"],
}


def build_system_prompt(starred_rows, papers: bool = False) -> str:
    if papers:
        parts = [
            "You are a research-paper triage judge reading arXiv abstracts.",
            config.PAPERS_PROFILE,
            "For each paper you receive, respond with JSON: "
            '{"score": 0-10, "lane": one of '
            + json.dumps(config.LANES + ["other"])
            + ', "tldr": one plain sentence stating the paper\'s concrete '
            "contribution}.",
            "Scoring guide: 9-10 = squarely in a core niche AND a substantive "
            "contribution (new method, strong results, or rigorous analysis); "
            "7-8 = clearly in a niche, ordinary but solid; 4-6 = adjacent to a "
            "niche or incremental; 0-3 = off-niche, survey-mill output, or "
            "trivial. Judge the CONTRIBUTION stated in the abstract, not the "
            "title's ambition. The tldr must state what the paper actually "
            "shows or builds, with numbers when the abstract gives them.",
        ]
    else:
        parts = [
            "You are a personal news-curation judge.",
            config.PROFILE,
            "For each item you receive, respond with JSON: "
            '{"score": 0-10, "lane": one of '
            + json.dumps(config.LANES + ["other"])
            + ', "tldr": one plain sentence stating the concrete substance}.',
            "Scoring guide: 9-10 = must-see primary-source news or deep technical "
            "content squarely in the reader's interests; 7-8 = solidly worth a look; "
            "4-6 = fine but ordinary; 0-3 = clickbait, fluff, PR, off-topic, or "
            "information-free. Judge INFORMATIVENESS, not popularity. "
            "The tldr must state the actual finding/announcement, never tease it.",
        ]
    if starred_rows:
        examples = "; ".join(f'"{r["title"]}" ({r["lane"]})' for r in starred_rows)
        parts.append(
            "Recent items the reader starred (treat similar content as high-score): "
            + examples
        )
    return "\n".join(parts)


def score_item(item: dict, system_prompt: str) -> dict:
    hint = config.CATEGORY_LANE_HINTS.get(item["category"], "")
    user = (
        f"Feed: {item['feed']}\nFolder: {item['category']}"
        + (f" (lane hint: {hint})" if hint else "")
        + f"\nTitle: {item['title']}\nExcerpt: {item['snippet'][:500]}"
    )
    payload = {
        "model": config.MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user},
        ],
        "format": RESPONSE_SCHEMA,
        "stream": False,
        # Disable the model's chain-of-thought: scoring is a schema-constrained
        # score/lane/tldr judgment, not a reasoning task. Leaving thinking on made
        # gemma4 emit reasoning tokens before every JSON — the dominant cost of the
        # serial ~250-item run, which pushed the morning briefing past its 2h
        # systemd timeout. Harmlessly ignored by non-thinking models.
        "think": False,
        "options": {"temperature": 0.1},
    }
    req = urllib.request.Request(
        f"{config.OLLAMA_URL}/api/chat",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        body = json.loads(r.read().decode())
    out = json.loads(body["message"]["content"])
    score = max(0.0, min(10.0, float(out.get("score", 0))))
    lane = out.get("lane", "other")
    if lane not in config.LANES + ["other"]:
        lane = "other"
    return {"score": score, "lane": lane, "tldr": str(out.get("tldr", ""))[:400]}
