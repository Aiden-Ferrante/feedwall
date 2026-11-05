# feedwall: notes for coding agents

- Python 3.11+, stdlib only at runtime. Tests: `pip install pytest && pytest -q`.
- Never call a real Ollama or FreshRSS from tests; mock `urllib.request.urlopen`.
- Every stored score carries `score_source` (`model`, `fallback`, `lake`). A
  default score must never be written without saying so.
- A source that fails must log to stderr; "returned 0 items" and "could not
  reach the source" must stay distinguishable.
- Credentials live in `.env` (gitignored, see `.env.example`); nothing personal
  (usernames, hostnames, home paths) is hardcoded. Configure through env vars.
