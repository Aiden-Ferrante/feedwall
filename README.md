# feedwall

A read-only **frontier-awareness system**: wide firehose intake (AI/ML, systems, markets, tech — ~97 curated primary-source feeds) curated by a local LLM to your taste, surfaced as a morning briefing and a glanceable wall. Fully local and keyless. See [PLAN.md](PLAN.md) for the architecture decisions.

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
- Login `mooteo` / change the default password (Settings → Profile), then update `FEEDWALL_API_PASS` env for the brain if you change the API password.
- Timers: `systemctl --user list-timers feedwall-briefing.timer`; logs: `journalctl --user -u feedwall-briefing`.
- Gaps by design: Discord (GPU MODE) and X/Twitter — lurk in-app. Reddit sometimes 403s FreshRSS's UA.
- The `benchmarks` lane (`benchmarks.opml`) has a standing gap: **Epoch AI, Artificial Analysis, LMArena and LiveBench publish no usable feed** — check those by hand. Details and the traps (LMArena returns HTTP 200 *HTML* for `/rss`) are in [discovered.md](discovered.md).
