# feedwall

A local, keyless news filter: FreshRSS pulls primary-source feeds (AI/ML, systems, markets, tech), a local LLM (gemma4 via Ollama) scores each item 0-10 for relevance to me, and the top items become a morning briefing and a wall dashboard.

**Result:** 24,178 items scored from 120 distinct feeds (more than the ~97 currently subscribed, listed below; feeds come and go over time) between 2026-07-03 and 2026-10-15 (read-only query of `brain-data/curated.sqlite`), and an audit of that store found three failures that every run had reported as success.

## Quickstart

```
git clone https://github.com/Aiden-Ferrante/feedwall && cd feedwall
python3 -m briefing.render --stdout   # stdlib only; on a fresh clone prints an empty briefing, "0 items scored"
python3 -m brain stats                # "items scored: 0" until the brain has run
```

Scoring for real needs FreshRSS (`cp .env.example .env`, set both passwords, `docker compose up -d`, then subscribe feeds from the `.opml` files) and Ollama with `gemma4:latest` pulled; then `python3 -m brain run --limit 250 --hours 36`. `brain-data/` is gitignored, so no scored data ships with the repo.

## What went wrong / what I learned

- **Green exit codes hid silent failures.** The three below came from querying the store, not from logs or exit codes; the runs that produced them exited 0.
- **Fallback scores look like real scores.** When scoring a starred item throws, `brain/__main__.py:62` stores a default score of 7.0. 1,990 rows sit at exactly 7.0, and nothing in a row says which came from the fallback.
- **A source produced nothing for its whole life.** `brain/stocklake.py` returns 0 on any error ("not an error, just no signal"); the store holds 0 rows with an id like `stocklake/%`, so the cross-feed never landed a single item and never said so.
- **The cap, not the filter, decided what was read.** `bin/morning.sh:7` runs with `--limit 250`; 91 of the 98 days with any scoring recorded exactly 250 scored rows, so most days the volume cap, not the relevance score, decided what got scored.

```
FreshRSS (:8970) ──> brain (gemma4 via Ollama) ──> brain-data/curated.sqlite
   firehose             score/lane/tldr                 │            │
                                                   briefing/      dashboard/
                                              vault note ~06:45   wall (:8975)
```

## Pieces

| Piece | What | How it runs |
|---|---|---|
| **FreshRSS** | intake backbone, ~97 feeds, 20-min refresh | `docker compose up -d` (MC: `feedwall`) |
| **brain/** | scores unread items 0–10 "for me?", lane, TL;DR via local gemma4; syncs stars as taste signal; ingests Stocklake `/api/whatsnew` | `python3 -m brain run [--limit N --hours H]` |
| **briefing/** | "What moved" note — top-5 + lane digest — into the vault **via vaultwriter** `/briefing` → `Distillation/Briefings/` | `python3 -m briefing.render [--stdout]` |
| **dashboard/** | zero-dep wall on **:8975** over curated.sqlite | `python3 dashboard/server.py` (MC: `feedwall-wall`) |
| **bin/morning.sh** | brain run + briefing, daily | systemd --user timer `feedwall-briefing` @ 06:45 |

## Daily habit

Read the briefing in Obsidian (or the wall at http://localhost:8975). **Star** what you love in FreshRSS — stars become few-shot taste examples for the scorer. **Prune** feeds that bore you — pruning is the coarse filter, the brain is the fine one.

## Ops notes

- Feeds ledger + discovery log: [discovered.md](discovered.md). Starter pack: `starter.opml`.
- Scoring needs gemma4 warm in Ollama; cold load under GPU contention can take ~6 min (service timeout allows 2h).
- Credentials: `cp .env.example .env` and set `FRESHRSS_PASSWORD` / `FEEDWALL_API_PASS` before `docker compose up -d` (compose refuses to start without them). Login is `mooteo`. To rotate later: `docker exec feedwall ./cli/update-user.php --user mooteo --password=... --api-password=...`, then update `.env`. FreshRSS listens on 127.0.0.1:8970 only.
- Timers: `systemctl --user list-timers feedwall-briefing.timer`; logs: `journalctl --user -u feedwall-briefing`.
- Gaps by design: Discord (GPU MODE) and X/Twitter — lurk in-app. Reddit sometimes 403s FreshRSS's UA.
- The `benchmarks` lane (`benchmarks.opml`) has a standing gap: **Epoch AI, Artificial Analysis, LMArena and LiveBench publish no usable feed** — check those by hand. Details and the traps (LMArena returns HTTP 200 *HTML* for `/rss`) are in [discovered.md](discovered.md).
