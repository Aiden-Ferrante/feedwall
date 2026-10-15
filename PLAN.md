# feedwall — build-out plan (v1, 2026-07-02)

Decisions locked: **both surfaces from day one** · **ranked + lane digest** shape ·
**gemma4** scorer (Learn-hub's proven critic model) · all four expansions.
Constraints: keyless/local only, FreshRSS stays the intake backbone (adopt-first),
vault writes ONLY through vaultwriter (:8799, new-files-only).

## Architecture

```
FreshRSS (:8970, ~57+ feeds, 20-min refresh)
        │  Google-Reader-compatible API (api/greader.php)
        ▼
  brain/  ── fetch unread since last run
        │  gemma4 (local Ollama): score 0–10 "for Aiden?", lane, 1-line TL;DR
        ▼
  curated.sqlite  (items, scores, lanes, tldrs, star-feedback)
        │                          │
        ▼                          ▼
  briefing/                   dashboard/
  morning "What moved"        read-only web wall (Channel brand,
  note → vaultwriter :8799    GitHub-dark), :8975, MC-registered
  (systemd --user timer ~7am)
```

Taste feedback loop: stars/favorites in FreshRSS are fetched via the same API and
become few-shot examples in the scorer prompt ("loved" vs "skipped"). Pruning
feeds in FreshRSS remains the coarse filter; the brain is the fine filter.

## Output shape (both surfaces): ranked + lane digest

1. **Top 5 overall** — highest score across all lanes, TL;DR + why-it-scored.
2. **Lane digest** — one line per lane (AI/ML · systems · markets · causal/stats ·
   data-eng · tech): best item or "quiet day in <lane>" (silence is signal).
3. Briefing note lands as a sibling of the daily note; dashboard renders the same
   ranking live with lane columns underneath.

## Phases

### Phase 1 — curation brain (build first; everything else is a view)
- `brain/fetch.py` — FreshRSS greader API client (login token → unread items since
  watermark; also pull starred items for the taste set).
- `brain/score.py` — gemma4 via local Ollama (`/api/chat`, JSON mode): score, lane,
  tldr per item. Batch, cache by item id — never re-score. Resolve exact model tag
  from `ollama list` at build time (Learn hub's gemma4 critic tag).
- `brain/db.py` — SQLite schema: items(id, feed, title, url, published, lane,
  score, tldr, starred, scored_at) + runs watermark table.
- CLI: `python -m brain run` = fetch → score → store. Idempotent.
- **Verify:** run on live backlog; spot-check 20 scored items; tune prompt until
  ranking "feels right" (use starred items as ground truth).

### Phase 2 — two surfaces (thin, parallel once brain output exists)
- `briefing/render.py` — read curated.sqlite → markdown (shape above) → POST to
  vaultwriter :8799 as `Daily Briefing YYYY-MM-DD.md` next to the daily note.
  Never writes the vault directly.
- systemd --user service + timer (~07:00, catch-up on missed boots) — same pattern
  as boox2obsidian.
- `dashboard/` — FastAPI + one static page (stdlib-lean, GitHub-dark #0d1117 /
  Channel blue #4da3ff), port **:8975**, read-only over curated.sqlite.
  Register in Mission Control apps.yaml (alongside feedwall :8970 itself — do that
  registration in this phase too).
- **Verify:** one real briefing note lands in the vault via vaultwriter; dashboard
  renders same top-5 + lanes; MC shows both services green.

### Phase 3 — taste loop + polish (after living with it ~a week)
- Star-feedback ingestion → few-shot block in scorer prompt; weekly re-eval of
  score threshold (aim: top-5 hit rate "would I have wanted this?").
- Briefing links back to FreshRSS item + original URL; add "yesterday I starred X"
  recap line.
- Optional: score-decay/dedup across near-identical stories (same event, many feeds).

### Expansion track (cheap, parallel — mostly config not code)
1. Let the discovery /loop finish: forums & communities pass, publications/journals
   pass; then promote the validated backlogs (researchers, podcasts, markets, systems).
2. **YouTube as RSS** — new "Video" category: GPU MODE lectures, Karpathy, etc. via
   `https://www.youtube.com/feeds/videos.xml?channel_id=<ID>` (resolve channel_ids).
3. **GitHub releases** — `releases.atom` for load-bearing repos: vllm, pytorch,
   ollama, freshrss, duckdb, langgraph (category "Releases", lane=systems).
4. **Stocklake cross-feed** — smallest viable seam: a tiny script exposes notable
   lake signals (attention/positioning anomalies) as a local RSS/JSON feed the brain
   ingests like any other source; briefing shows them in the markets lane.

## Non-goals (v1)
- No posting/participation features (role = stay aware).
- No cloud LLMs, no API keys anywhere.
- No replacing FreshRSS UI — it stays the full-firehose fallback reader.
- Discord/X remain manual lurks (no fragile bridges).

## Open items
- ~~Change FreshRSS default password~~ done 2026-10-15: rotated; creds in `.env`
  (gitignored), brain reads env/.env with no hardcoded default; port bound to 127.0.0.1.
- Mission Control registration for: feedwall (:8970), feedwall-dashboard (:8975),
  briefing timer (status-only entry).
