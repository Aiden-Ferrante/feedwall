"""Configuration for the feedwall curation brain.

Everything local and keyless. Values come from environment variables with
sane defaults for this machine; FEEDWALL_API_PASS is the FreshRSS API
password (Settings -> Profile -> API management).
"""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FRESH_URL = os.environ.get("FEEDWALL_FRESH_URL", "http://localhost:8970/api/greader.php")
FRESH_USER = os.environ.get("FEEDWALL_USER", "mooteo")
FRESH_API_PASS = os.environ.get("FEEDWALL_API_PASS", "changeme-feedwall")

OLLAMA_URL = os.environ.get("FEEDWALL_OLLAMA_URL", "http://localhost:11434")
MODEL = os.environ.get("FEEDWALL_MODEL", "gemma4:latest")

DB_PATH = Path(os.environ.get("FEEDWALL_DB", ROOT / "brain-data" / "curated.sqlite"))

VAULTWRITER_URL = os.environ.get("FEEDWALL_VAULTWRITER_URL", "http://localhost:8799")

# Learn hub (txt2kg learn service) — source of the briefing's "Study debt" section.
LEARN_URL = os.environ.get("FEEDWALL_LEARN_URL", "http://localhost:8010")

LANES = ["papers", "ai-ml", "systems", "markets", "causal-stats", "data-eng", "tech"]

# Research papers get their own lane with a papers-specific rubric (see
# score.build_system_prompt). Cap per run so an arXiv burst can't crowd the
# news lanes out of the shared --limit budget.
PAPERS_CATEGORY = "Papers"
PAPERS_MAX_PER_RUN = 40

# Feed noise that should never reach the scorer (e.g. PyTorch's releases.atom
# emits a "release" for every trunk/ciflow CI tag; llama.cpp cuts a bare
# build-number release like "b6032" on nearly every merge).
TITLE_SKIP_PREFIXES = ("trunk/", "ciflow/", "nightly/")
TITLE_SKIP_RE = r"^b\d{3,6}$"

# FreshRSS category label -> lane hint (soft prior, model may override)
CATEGORY_LANE_HINTS = {
    "Papers": "papers",
    "AI/ML — Blogs & Newsletters": "ai-ml",
    "Discovered — AI-lab official blogs": "ai-ml",
    "Discovered — individual AI/ML researchers": "ai-ml",
    "Discovered — AI/ML & systems podcasts": "ai-ml",
    "Stats & Causal": "causal-stats",
    "Code & Launches": "tech",
    "Markets & Econ": "markets",
    "Discovered — markets/quant primary sources": "markets",
    "Tech News": "tech",
    "Discovered — GPU/systems practitioners": "systems",
    "Releases": "systems",
    "Video": "ai-ml",
    "Stocklake": "markets",
    "Discovered — macro & econ data": "markets",
    "Discovered — econ analysis & commentary": "markets",
    "Discovered — local-LLM releases & tooling": "systems",
    "Discovered — local-LLM practitioners & guides": "ai-ml",
    "Discovered — builders in public": "tech",
}

PROFILE = """The reader is a data-science master's student and heavy builder.
Interests, in priority order:
1. Frontier AI/ML research: LLMs, training/inference techniques, evals, agents, model releases.
2. GPU/systems/infrastructure: CUDA, kernels, vLLM, performance engineering, distributed systems.
3. Causal inference and statistics: Pearl-style causality, econometrics, probabilistic modeling.
4. Data engineering: lakehouses, DuckDB/Parquet, pipelines.
5. Markets and finance-x-AI: quant research, macro data releases, regulator/central-bank primary sources.
6. Adjacent frontier tech that a builder should know about.
They strongly prefer primary sources, technical depth, and information density.
They dislike clickbait, hype, engagement-bait, product-marketing fluff, and rewrites of other outlets' reporting."""

PAPERS_PROFILE = """The reader tracks new research papers in a few tight niches.
Core niches (score generously when squarely on-topic):
1. Efficient LLM inference and serving: quantization, KV-cache techniques,
   speculative decoding, attention/GPU kernels, MoE inference, serving systems,
   latency/throughput engineering.
2. LLM agents and their evaluation: coding agents, agent harnesses and
   scaffolding, agent benchmarks (SWE-bench-style), reliability and
   long-horizon behavior, context engineering.
Secondary niche (solid papers welcome, bar is higher):
3. Econophysics and quantitative markets: market microstructure,
   information-theoretic market modeling, trading/statistical finance.
Anything outside these niches should score low unless it is a genuinely
landmark result a broad ML audience must know about."""
