# feedwall

[![ci](https://github.com/Aiden-Ferrante/feedwall/actions/workflows/ci.yml/badge.svg)](https://github.com/Aiden-Ferrante/feedwall/actions/workflows/ci.yml)

A local, keyless news filter: FreshRSS pulls primary-source feeds (AI/ML, systems, markets, tech), a local LLM (gemma4 via Ollama) scores each item 0-10 for relevance to me, and the top items become a morning briefing and a wall dashboard.

**Result:** 24,178 items scored from 120 distinct feeds (more than the ~97 currently subscribed, listed below; feeds come and go over time) between 2026-07-03 and 2026-10-15 (read-only query of `brain-data/curated.sqlite`), and an audit of that store found three failures that every run had reported as success.

## What went wrong / what I learned

- **Green exit codes hid silent failures.** The three below came from querying the store, not from logs or exit codes; the runs that produced them exited 0.
- **Fallback scores looked like real scores.** When scoring a starred item threw, the brain stored a default score of 7.0. 1,990 rows sit at exactly 7.0, and nothing in a row said which came from the fallback.
  *Fixed:* every row now carries `score_source` (`model`, `fallback` or `lake`); the fallback is logged, counted in the run summary and tagged in the briefing. The migration adds the column to existing DBs and labels only what it can prove (Stocklake ids); older rows stay `NULL` rather than being guessed.
- **A source produced nothing for its whole life.** `brain/stocklake.py` returned 0 on any error ("not an error, just no signal"); the store holds 0 rows with an id like `stocklake/%`, so the cross-feed never landed a single item and never said so.
  *Fixed:* unreachable service, non-JSON, a payload with no `rows` key and malformed rows are each logged to stderr.
- **The cap, not the filter, decided what was read.** `bin/morning.sh` runs with `--limit 250`; 91 of the 98 days with any scoring recorded exactly 250 scored rows, so most days the volume cap, not the relevance score, decided what got scored. *Not fixed yet.*

## Quickstart

Stdlib only; Python 3.11+. The repo ships a small synthetic DB (`examples/demo.sqlite`, 11 invented rows built by `examples/make_demo_db.py`) so the briefing renders on a fresh clone:

```
git clone https://github.com/Aiden-Ferrante/feedwall && cd feedwall
FEEDWALL_DB=examples/demo.sqlite python3 -m briefing.render --stdout --as-of 2026-01-15T07:00+00:00
FEEDWALL_DB=examples/demo.sqlite python3 -m brain stats
pip install pytest && python3 -m pytest -q   # no network: Ollama and FreshRSS are mocked
```

Scoring for real needs FreshRSS (`cp .env.example .env`, set both passwords, `docker compose up -d`, then subscribe feeds from the `.opml` files) and Ollama with `gemma4:latest` pulled; then `python3 -m brain run --limit 250 --hours 36`. Real scored data goes to `brain-data/` (gitignored).

## How it works

```
FreshRSS (:8970) ──> skip filters ──> brain (gemma4 via Ollama) ──> brain-data/curated.sqlite
   firehose         (deterministic)     score/lane/tldr, JSON schema      │            │
                                                                     briefing/     dashboard/
                                                                Markdown ~06:45   wall (:8975)
```

- **Deterministic before the model.** CI tags, build-number releases and translated duplicates are dropped by rules in `brain/config.py` before any model call (`skip_reason` in `brain/__main__.py`).
- **Constrained model output.** Ollama is called with a JSON schema (`format`), temperature 0.1 and thinking off; scores are clamped to 0-10 and unknown lanes become `other`.
- **Deterministic after the model.** Papers and benchmark feeds are pinned to their lanes regardless of what the model says; papers are kept out of the news top-5.

| Piece | What | How it runs |
|---|---|---|
| **FreshRSS** | feed reader that does the fetching, ~97 feeds, 20-min refresh | `docker compose up -d` |
| **brain/** | scores unread items 0-10 for relevance, picks a lane, writes a one-line TL;DR; uses my FreshRSS stars as few-shot taste examples; optionally ingests a local market-data service (Stocklake `/api/whatsnew`) | `python3 -m brain run [--limit N --hours H]` |
| **briefing/** | "What moved" Markdown note: top-5 + one line per lane. `--stdout` prints it; otherwise it is POSTed to `FEEDWALL_VAULTWRITER_URL/briefing`, a small local service of mine that saves it into my notes folder (an Obsidian "vault") | `python3 -m briefing.render [--stdout]` |
| **dashboard/** | zero-dependency web page on **:8975** over the same DB | `python3 dashboard/server.py` |
| **bin/morning.sh** | brain run + briefing, daily | systemd --user timer `feedwall-briefing` @ 06:45 (`make install-unit`) |

## Configuration

All settings are environment variables (or `.env`, see `.env.example`); defaults are neutral and local.

| Variable | Default | What |
|---|---|---|
| `FEEDWALL_USER` | `feedwall` | FreshRSS user (compose creates it, the brain logs in as it) |
| `FEEDWALL_API_PASS` / `FRESHRSS_PASSWORD` | none | FreshRSS API / web passwords |
| `FEEDWALL_DB` | `brain-data/curated.sqlite` | scored-items DB |
| `FEEDWALL_OLLAMA_URL`, `FEEDWALL_MODEL` | `http://localhost:11434`, `gemma4:latest` | scorer |
| `FEEDWALL_STOCKLAKE_URL` | `http://localhost:8420` | optional market-data source |
| `FEEDWALL_VAULTWRITER_URL` | `http://localhost:8799` | where the briefing is POSTed |
| `FEEDWALL_STUDY_DEBT` | off | opt-in briefing section from a separate private study app (`FEEDWALL_LEARN_URL`) |
| `FEEDWALL_TZ` | `UTC` | FreshRSS container timezone |

## Daily habit

Read the briefing (or the wall at http://localhost:8975). **Star** what you love in FreshRSS — stars become few-shot taste examples for the scorer. **Prune** feeds that bore you — pruning is the coarse filter, the brain is the fine one.

## Ops notes

- Feeds ledger + discovery log: [discovered.md](discovered.md). Starter pack: `starter.opml`.
- Scoring needs gemma4 warm in Ollama; cold load under GPU contention can take ~6 min (service timeout allows 3h).
- Credentials: `cp .env.example .env` and set `FRESHRSS_PASSWORD` / `FEEDWALL_API_PASS` before `docker compose up -d` (compose refuses to start without them). To rotate later: `docker exec feedwall ./cli/update-user.php --user "$FEEDWALL_USER" --password=... --api-password=...`, then update `.env`. FreshRSS listens on 127.0.0.1:8970 only.
- Timers: `systemctl --user list-timers feedwall-briefing.timer`; logs: `journalctl --user -u feedwall-briefing`.
- Gaps by design: Discord (GPU MODE) and X/Twitter — lurk in-app. Reddit sometimes 403s FreshRSS's UA.
- The `benchmarks` lane (`benchmarks.opml`) has a standing gap: **Epoch AI, Artificial Analysis, LMArena and LiveBench publish no usable feed** — check those by hand. Details and the traps (LMArena returns HTTP 200 *HTML* for `/rss`) are in [discovered.md](discovered.md).
- The wall's nav bar and `make check` use an optional sibling checkout of my shared UI kit (`../fleet-ui`, override with `FLEET_UI_CSS`); without it the page renders unstyled.
