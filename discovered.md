# feedwall — discovered sources ledger

Auto-maintained by the `/loop` feed-discovery task. Newly **validated** feeds get imported into FreshRSS under a `Discovered — <focus>` category; this file is the human-readable log + the dedupe reference (all xmlUrls added live here or in `starter.opml`).

## Focus rotation (cycle 2 — set 2026-07-03; cycle 1 complete, see below)
1. macro & economic data primary sources (agencies, central banks, data releases)
2. econ analysis & commentary (economists worth reading, labor/inflation substacks)
3. local-LLM ecosystem — releases & tooling (llama.cpp, LM Studio, inference stacks)
4. local-LLM ecosystem — practitioners & guides
5. builders in public — Show HN & indie hackers
6. builders in public — engineering build-logs & devtools
(then repeat)

**Last focus:** backlog-promotion pass (2026-07-03 — CYCLE 2 FULLY COMPLETE, all backlogs promoted)
**Next focus:** none scheduled — discovery loop wound down 2026-07-03; re-arm with a new rotation when a fresh vein is wanted

<details><summary>Cycle 1 rotation (complete)</summary>
AI-lab official blogs → individual AI/ML researchers → AI/ML & systems podcasts → markets/quant primary sources → GPU/systems practitioners → forums & communities → publications/journals — all done; backlogs promoted 2026-07-03.
</details>

---

## 2026-06-30 — AI-lab official blogs
- OpenAI — News · https://openai.com/news/rss.xml · org · frontier lab's own announcements & research posts, primary source.
- Google DeepMind — Blog · https://deepmind.google/blog/rss.xml · org · DeepMind research/product announcements straight from the lab.
- Microsoft Research — Blog · https://www.microsoft.com/en-us/research/feed/ · org · MSR papers & project releases across ML/systems.
- NVIDIA Technical Blog · https://developer.nvidia.com/blog/feed/ · org · deep GPU/CUDA/inference engineering from the source (doubles for the systems lane).
- Apple Machine Learning Research · https://machinelearning.apple.com/rss.xml · org · Apple's own ML research posts, low-volume/high-signal.
- EleutherAI — Blog · https://blog.eleuther.ai/index.xml · org · open-research lab; interpretability & LLM-training write-ups.
- Qwen (Alibaba) — Blog · https://qwenlm.github.io/blog/index.xml · org · primary release notes for the Qwen model family.

### Validated backlog (pull in on the next AI-lab pass)
- Google Research — Blog · https://research.google/blog/rss/
- Databricks — Blog · https://www.databricks.com/blog/feed.xml
- Together AI — Blog · https://www.together.ai/blog/rss.xml
- NVIDIA corporate blog · https://blogs.nvidia.com/feed/ (more PR than the developer blog)

## 2026-07-01 — individual AI/ML researchers
- Andrej Karpathy · https://karpathy.github.io/feed.xml · individual · rare but essential deep-dives on LLMs/training from a field-shaping practitioner.
- Chip Huyen · https://huyenchip.com/feed.xml · individual · ML-systems & production-AI design, book-quality essays.
- Nathan Lambert — Interconnects · https://www.interconnects.ai/feed · individual · frontier post-training/RLHF analysis, very active + high signal.
- Sander Dieleman · https://sander.ai/feed.xml · individual · deep generative/diffusion-model theory from a DeepMind researcher.
- Tim Dettmers · https://timdettmers.com/feed/ · individual · quantization & GPU-efficient training (also feeds the systems lane).
- Eugene Yan · https://eugeneyan.com/rss/ · individual · applied ML, LLM eval & recsys from an industry practitioner.
- Sebastian Ruder · https://www.ruder.io/rss/ · individual · NLP research distilled; long-running high-signal newsletter.

### Validated backlog (next individuals pass)
- Jay Alammar · https://jalammar.github.io/feed.xml
- François Chollet · https://fchollet.substack.com/feed
- Cameron R. Wolfe · https://cameronrwolfe.substack.com/feed
- Ferenc Huszár — inFERENCe · https://www.inference.vc/rss/
- Chris Olah · https://colah.github.io/rss.xml (rare updates, high signal)
- fast.ai · https://www.fast.ai/index.xml

## 2026-07-01 — AI/ML & systems podcasts
- Latent Space · https://www.latent.space/feed · podcast · practitioner AI-engineering interviews, very high signal on what's shipping.
- Dwarkesh Podcast · https://www.dwarkeshpatel.com/feed · podcast · deep long-form interviews with researchers & founders.
- ThursdAI · https://sub.thursdai.news/feed · podcast · weekly frontier-AI news roundup — good for staying current.
- Practical AI (Changelog) · https://changelog.com/practicalai/feed · podcast · applied ML/AI in production.
- Oxide and Friends · https://oxide-and-friends.transistor.fm/rss · podcast · deep systems/hardware engineering (Bryan Cantrill et al).
- The Changelog · https://changelog.com/podcast/feed · podcast · software/infra engineering interviews.
- Lex Fridman Podcast · https://lexfridman.com/feed/podcast/ · podcast · broad but high-signal AI/science long-form conversations.

### Podcast backlog / to-resolve (next podcast pass)
- The TWIML AI Podcast — feed URL didn't resolve; find real RSS.
- Machine Learning Street Talk (MLST) — resolve RSS (anchor/podbean).
- No Priors, The Cognitive Revolution — resolve RSS.
- The Gradient Podcast — skipped as near-dup of The Gradient publication (already tracked).

## 2026-07-01 — markets/quant primary sources
- arXiv q-fin · https://export.arxiv.org/rss/q-fin · publication · primary quant-finance research papers (also serves the finance×AI / causal-econ lane).
- Liberty Street Economics (NY Fed) · https://libertystreeteconomics.newyorkfed.org/feed/ · org · primary NY Fed staff research blog.
- Aswath Damodaran — Musings on Markets · https://aswathdamodaran.blogspot.com/feeds/posts/default · individual · valuation/corporate-finance, exceptionally high signal.
- Calculated Risk · https://www.calculatedriskblog.com/feeds/posts/default · individual · primary macro/housing data analysis.
- Alpha Architect · https://alphaarchitect.com/feed/ · org · quant/factor-investing research straight from the firm.
- Robert Carver — Investment Idiocy · https://qoppac.blogspot.com/feeds/posts/default · individual · systematic/quant trading from a practitioner.
- SEC — Press Releases · https://www.sec.gov/news/pressreleases.rss · org · primary regulator announcements & enforcement.

### Validated backlog (next markets pass)
- FRED Blog (St. Louis Fed) · https://fredblog.stlouisfed.org/feed/
- Bank Underground (Bank of England) · https://bankunderground.co.uk/feed/
- Fed — FEDS Notes · https://www.federalreserve.gov/feeds/feds_notes.xml
- Newfound / Flirting with Models · https://blog.thinknewfound.com/feed/
- BLS news releases — https://www.bls.gov/feed/news_release.rss returns 403 to curl; retry via FreshRSS UA or find mirror.

## 2026-07-01 — GPU/systems practitioners
- Lei Mao — Log Book · https://leimao.github.io/feed.xml · individual · deep CUDA/GPU-programming write-ups.
- Simon Boehm (siboehm) · https://siboehm.com/feed.xml · individual · GPU kernel optimization (the famous CUDA matmul series).
- PyTorch — Blog · https://pytorch.org/blog/feed.xml · org · framework internals, perf work, releases.
- Answer.AI · https://www.answer.ai/index.xml · org · systems+ML research lab (FSDP/QLoRA-style work).
- Brendan Gregg · https://www.brendangregg.com/blog/rss.xml · individual · systems-performance authority (eBPF, flame graphs).
- Dan Luu · https://danluu.com/atom.xml · individual · rigorous systems/perf/hardware analysis.
- Marc Brooker · https://brooker.co.za/blog/rss.xml · individual · distributed-systems design from an AWS principal engineer.

### Validated backlog (next systems pass)
- Julia Evans (jvns) · https://jvns.ca/atom.xml
- matklad (Alex Kladov) · https://matklad.github.io/feed.xml
- Cloudflare — Blog · https://blog.cloudflare.com/rss/
- Meta — Engineering · https://engineering.fb.com/feed/

## 2026-07-03 — plan build-out expansion (forums + publications passes, backlog promotion, Video/Releases)
- **Video (new category):** GPU MODE lectures, Karpathy, 3Blue1Brown, MLST — YouTube channel RSS (`videos.xml?channel_id=`). MLST resolves the podcast-backlog to-do.
- **Releases (new category):** vLLM, PyTorch, Ollama, FreshRSS, DuckDB, LangGraph — `releases.atom` for load-bearing repos.
- **Forums & communities:** Lobsters · LessWrong Curated · r/MachineLearning · r/LocalLLaMA · PyTorch Forums. (HN already tracked. Discord/GPU MODE stays manual. Note: Reddit rate-limits FreshRSS's UA — r/LocalLLaMA erroring, may recover or need pruning.)
- **Publications/journals:** Quanta · IEEE Spectrum · MIT Tech Review · JMLR · ACM Queue · Nature Machine Intelligence. (Distill.pub skipped — archived/dead.)
- **Backlogs promoted:** Google Research, Databricks, Together AI (AI-lab) · Alammar, Chollet, Wolfe, Huszár, Olah, fast.ai (individuals) · FRED Blog, Bank Underground, FEDS Notes, Flirting with Models (markets) · jvns, matklad, Cloudflare, Meta Engineering (systems). NVIDIA corporate blog left unpromoted (PR-heavy; developer blog already in).
- **Stocklake cross-feed:** not RSS — `brain/stocklake.py` ingests `/api/whatsnew` directly as pre-scored markets-lane items; skips silently when the lake is down.
- Vault total now ~97 feeds.

## 2026-07-03 — macro & econ data primary sources (cycle 2, pass 1)
- BEA — News Releases · https://apps.bea.gov/rss/rss.xml · org · GDP/income/spending prints straight from the agency.
- Census — Economic Indicators · https://www.census.gov/economic-indicators/indicator.xml · org · retail sales, housing starts, trade — the raw indicator calendar.
- Atlanta Fed — Macroblog · https://www.atlantafed.org/RSS/macroblog · org · GDPNow-adjacent staff analysis of incoming data.
- ECB — Press Releases · https://www.ecb.europa.eu/rss/press.html · org · the other big central bank, primary.
- Apricitas Economics · https://www.apricitas.io/feed · individual · data-dense macro charting substack (jobs/inflation/industry).
- Employ America · https://www.employamerica.org/feed/ · org · labor-market research shop — the "jobs report" deep-read.
- Econbrowser · https://econbrowser.com/feed · individual · Hamilton & Chinn, rigorous macro-data econometrics.

### Backlog (next macro pass)
- CBO — Publications · https://www.cbo.gov/publications/all/rss.xml
- BLS news releases — persistent 403 bot-wall (curl + browser UA); jobs-report coverage arrives via Employ America / Calculated Risk / FRED Blog instead.
- conversableeconomist.com (429 rate-limit — retry), IMF blogs RSS (403).

## 2026-07-03 — econ analysis & commentary (cycle 2, pass 2)
- Noahpinion (Noah Smith) · https://www.noahpinion.blog/feed · individual · prolific data-driven econ commentary; strong on jobs/industrial policy.
- Paul Krugman · https://paulkrugman.substack.com/feed · individual · Nobel laureate reading the data prints in real time.
- The Grumpy Economist (John Cochrane) · https://www.grumpy-economist.com/feed · individual · rigorous counterweight to Krugman — deliberate ideological range.
- Conversable Economist (Timothy Taylor) · https://conversableeconomist.com/feed/ · individual · JEP managing editor; pure substance, zero engagement-bait.
- VoxEU / CEPR · https://cepr.org/rss.xml · publication · research-based policy columns from working economists.
- Klement on Investing · https://klementoninvesting.substack.com/feed · individual · behavioral finance/markets crossover, daily and dense.
- Tim Harford · https://timharford.com/feed/ · individual · FT "Undercover Economist"; statistical literacy angle.

### Backlog (next econ-commentary pass)
- Brad DeLong · https://braddelong.substack.com/feed
- EconLog · https://www.econlib.org/feed/
- The Overshoot (Matthew Klein) — feed dead (000), site may have moved.

## 2026-07-03 — local-LLM releases & tooling (cycle 2, pass 3)
- llama.cpp releases · https://github.com/ggml-org/llama.cpp/releases.atom · org · the foundation of the whole local-inference stack (note: repo moved to ggml-org).
- SGLang releases · https://github.com/sgl-project/sglang/releases.atom · org · vLLM's main serving rival; structured-generation engine.
- llamafile releases · https://github.com/Mozilla-Ocho/llamafile/releases.atom · org · Mozilla's single-file local-LLM distribution.
- Open WebUI releases · https://github.com/open-webui/open-webui/releases.atom · org · the de-facto local chat front-end over Ollama.
- Unsloth releases · https://github.com/unslothai/unsloth/releases.atom · org · efficient local fine-tuning — pairs with the DGX.
- ExLlamaV3 releases · https://github.com/turboderp-org/exllamav3/releases.atom · org · leading quantized-inference engine for consumer GPUs.
- KoboldCpp releases · https://github.com/LostRuins/koboldcpp/releases.atom · org · llama.cpp distribution with wide model/feature support.
- Lane hints extended in brain/config.py for all cycle-2 categories (econ→markets, tooling→systems, practitioners→ai-ml, builders→tech).

## 2026-07-03 — local-LLM practitioners & guides (cycle 2, pass 4)
- Georgi Gerganov · https://ggerganov.github.io/feed.xml · individual · llama.cpp/ggml author — the local-inference stack from its source.
- Philipp Schmid · https://www.philschmid.de/rss · individual · hands-on deploy/fine-tune guides (now at DeepMind).
- The Kaitchup (Benjamin Marie) · https://kaitchup.substack.com/feed · individual · quantization & consumer-GPU LLM experiments — squarely the local lane.
- Hamel Husain · https://hamel.dev/index.xml · individual · LLM evals & fine-tuning consulting write-ups.
- Vicki Boykis · https://vickiboykis.com/index.xml · individual · ML-eng essays (Normconf) — also feeds the data-eng lane.
- Jason Liu (jxnl) · https://jxnl.co/feed_rss_created.xml · individual · structured outputs / instructor author; applied-LLM patterns.

### Backlog (next practitioners pass)
- Maxime Labonne — blog feed 404s (Quarto move?); find real RSS or use his HF posts.

## 2026-07-03 — builders in public: Show HN & indie hackers (cycle 2, pass 5)
- Show HN (50+ points) · https://hnrss.org/show?points=50 · forum · what builders are shipping, pre-filtered by community traction.
- Pieter Levels · https://levels.io/rss/ · individual · the archetype build-in-public solo founder.
- DHH · https://world.hey.com/dhh/feed.atom · individual · 37signals founder; opinionated building/business essays.
- Mitchell Hashimoto · https://mitchellh.com/feed.xml · individual · HashiCorp founder now building Ghostty in public; deep eng posts.
- Ben Kuhn · https://www.benkuhn.net/index.xml · individual · Anthropic eng-manager essays on building/working well.
- Paul Graham — Essays · http://www.aaronsw.com/2002/feeds/pgessays.rss · individual · canonical builder essays (community-maintained feed).
- A Smart Bear (Jason Cohen) · https://asmartbear.com/index.xml · individual · WP Engine founder; rigorous startup/product essays.

### Skipped/backlog (builders pass)
- Indie Hackers — feed.xml returns HTML, no real RSS → manual watch below.
- Rob Walling — /feed 404s; find real URL next pass.

## 2026-07-03 — builders in public: engineering build-logs & devtools (cycle 2, pass 6 — final fresh focus)
- Tailscale — Blog · https://tailscale.com/blog/index.xml · org · the network your whole tailnet runs on; excellent eng writing.
- Fly.io — Blog · https://fly.io/blog/feed.xml · org · consistently the best infra-engineering prose on the internet.
- Oxide Computer — Blog · https://oxide.computer/blog/feed · org · building servers from scratch in public (podcast already tracked).
- antirez · https://antirez.com/rss · individual · Redis creator, back to writing systems essays.
- Xe Iaso · https://xeiaso.net/blog.rss · individual · prolific homelab/infra build-logs — kindred spirit to the DGX setup.
- fasterthanli.me (Amos) · https://fasterthanli.me/index.xml · individual · deep Rust/systems teaching build-logs.
- Andrew Kelley · https://andrewkelley.me/rss.xml · individual · Zig creator; language-building in public.

### Backlog (builders/devtools)
- Supabase — https://supabase.com/rss.xml (validated)
- Zed — https://zed.dev/blog.rss (validated)
- TigerBeetle — blog feed 404; find real URL.

## 2026-07-03 — backlog promotion (cycle 2, final pass)
- CBO — Publications · https://www.cbo.gov/publications/all/rss.xml · org · budget/economic projections primary source (→ macro & econ data).
- Brad DeLong · https://braddelong.substack.com/feed · individual · economic history + macro commentary (→ econ commentary).
- EconLog · https://www.econlib.org/feed/ · publication · multi-author econ essays (→ econ commentary).
- Maxime Labonne · https://maximelabonne.substack.com/feed · individual · fine-tuning/merging guides — substack found after github.io feed 404'd (→ local-LLM practitioners).
- Supabase — Blog · https://supabase.com/rss.xml · org · devtools build-in-public (→ builders).
- Zed — Blog · https://zed.dev/blog.rss · org · editor engineering build-logs (→ builders).
- Startups for the Rest of Us · https://www.startupsfortherestofus.com/feed · podcast · Rob Walling's bootstrapper podcast — resolved after blog feed 404'd (→ builders).

## Manual watch (no feed)
- TigerBeetle — no discoverable blog feed (all common paths 404). Watch: https://tigerbeetle.com/blog
- Indie Hackers — no working RSS. Watch: https://www.indiehackers.com/
- LM Studio — no RSS (lmstudio.ai/feed is an SPA fallback, not a feed). Watch: https://lmstudio.ai/blog
- unsloth blog — no RSS. Watch: https://unsloth.ai/blog (releases feed added instead)
- vLLM blog — no RSS. Watch: https://blog.vllm.ai (releases feed already tracked)
- Anthropic — no public RSS on anthropic.com/news (404). Watch via X @AnthropicAI or the news page: https://www.anthropic.com/news
- Mistral AI — no working RSS (news page is JS-rendered). Watch: https://mistral.ai/news
- Stability AI — no RSS. Watch: https://stability.ai/news
- GPU MODE (ex-CUDA MODE) — Discord community + YouTube lectures, no site RSS. To wire the lectures as a feed, resolve the YouTube channel_id and use https://www.youtube.com/feeds/videos.xml?channel_id=<ID>. Otherwise lurk the Discord.

## 2026-07-17 — papers lane retarget

The `Papers` category was rebuilt for the dedicated `papers` lane (see
`papers.opml`). The five broad arXiv category firehoses (cs.AI, cs.CL, cs.LG,
stat.ML, econ.EM — hundreds of items/day, folded into ai-ml) were unsubscribed
and replaced with three targeted arXiv **API query** feeds
(`export.arxiv.org/api/query?search_query=...`, Atom, sorted by submittedDate):

- efficient LLM inference/serving (quantization, KV cache, speculative
  decoding, kernels, MoE inference, serving) — ~5-10/day
- agents, harnesses & evals (coding agents, agent benchmarks/evals,
  SWE-bench, reliability, context engineering) — ~10-20/day
- econophysics & quant markets (q-fin.TR/ST/CP + econophysics) — ~4/day

To re-add a firehose, the old URLs were `https://export.arxiv.org/rss/<cat>`.
Query terms are edited by regenerating the URL (any OR list of `all:"..."`
phrases works) and updating both FreshRSS and `papers.opml`.

## 2026-08-13 — benchmarks lane

New `benchmarks` lane + `Benchmarks & Evals` FreshRSS category (`benchmarks.opml`),
for reading model-release claims critically: what a quoted score measures, whether
the benchmark is saturated/contaminated, and when a harness version changes under
the number. Lane boundary: **benchmarks = a benchmark or leaderboard changed**;
research *about* evaluation stays in `papers` (that lane's agents/evals arXiv query
already matches "agent benchmark"/"agent evaluation"/"SWE-bench").

Every URL below was fetched and confirmed to return real XML with entries:

- METR — blog · https://metr.org/feed.xml · org · time-horizon evals ("task length a model finishes at 50% reliability"), the best long-horizon-autonomy signal.
- ARC Prize — blog · https://arcprize.org/feed.xml · org · ARC-AGI-2/3 results and the contamination-resistant eval design argument.
- Stanford CRFM (HELM) · https://crfm.stanford.edu/feed.xml · org · HELM leaderboards + the AI Index saturation work.
- SWE-bench — releases · https://github.com/SWE-bench/SWE-bench/releases.atom · repo · harness/dataset versions; Verified-vs-Pro scores are not comparable across versions.
- tau2-bench — releases · https://github.com/sierra-research/tau2-bench/releases.atom · repo · multi-turn tool-use agent eval.
- Gorilla / BFCL — releases · https://github.com/ShishirPatil/gorilla/releases.atom · repo · function-calling leaderboard (AST-compared, not LLM-judged).
- Terminal-Bench — commits · https://github.com/harbor-framework/terminal-bench-1/commits/main.atom · repo · long-horizon shell agent eval; `releases.atom` and `tags.atom` are both **empty**, so commits it is (sparse — ~2 bursts in 2026). The old `laude-institute/terminal-bench` URL **301s** here (caught on first actualize); repo moved under the Harbor framework.

### No RSS — check by hand (all four verified: no feed, no autodiscovery link)
- **Epoch AI** · https://epoch.ai — JS-rendered, 404 on every feed path tried. NOTE: `epoch.substack.com/feed` resolves but is an unrelated blog ("epochs and talents", last post 2020) — do **not** subscribe it.
- **Artificial Analysis** · https://artificialanalysis.ai — 404 on /feed, /rss, /rss.xml, /blog/rss.xml. The single most useful independent leaderboard (composite of ~10 evals, ~72h refresh) and it has no feed. Email newsletter only.
- **LMArena** · https://news.lmarena.ai — SPA that returns **HTTP 200 with HTML** for /rss, /rss.xml, /feed, /index.xml. Subscribing any of those would silently add a broken feed; don't.
- **LiveBench** · https://github.com/LiveBench/LiveBench — releases/tags empty and `commits/main.atom` runs several commits/day of build churn. Rejected as noise; the monthly question rotation isn't announced via feed anyway. Watch https://livebench.ai.

Standing gap: the leaderboards with the best methodology are the ones without feeds.
If this lane ever justifies it, the fix is a small scraper posting into FreshRSS —
not more feed-path guessing.

## 2026-09-20 — research lane added (`research.opml`), and its standing gaps

21 feeds added across four groups: arXiv systems categories (cs.DC / cs.AR / cs.PF),
serving-stack release atoms, engineering blogs, and individual authors. Every one was
tested for a parsing XML feed body, not an HTTP 200 — the LMArena trap recorded above
bites here too (Papers with Code and alphaXiv both return 200 `text/html` for their
feed paths).

**No usable feed — check these by hand:**

| Source | What happens | Why it matters |
|---|---|---|
| **OpenReview** | `api2.openreview.net` returns **403** to an unauthenticated client; `/rss` is 404 | This is the one that hurts. Review threads are the highest-signal content in the field and there is no way to subscribe. |
| **MLSys proceedings** | `proceedings.mlsys.org` serves HTML only, no feed | The home venue for this lane. |
| **USENIX conference pages** (OSDI, ATC, NSDI) | per-conference `rss.xml` is 404 — only the site-wide `;login:` feed works, and it is added | Proceedings drop as a batch; a calendar reminder beats a feed. |
| **ACM SIGOPS / SOSP** | no feed | |
| **Papers with Code · alphaXiv · Deep Learning Monitor** | 200 `text/html` or 404 | Curation layers; browse, don't subscribe. |
| **Modal · Baseten · Anyscale · LMSYS · vLLM blog** | 404 on every common feed path; Anyscale returns HTML | Their *release* atoms work and are added instead. |

**The workaround for OpenReview** is a browser bookmark, not a feed: ICLR publishes
reviews and decisions for **all** submissions including rejected ones, which is what
makes it the place to read. NeurIPS publishes reviews for accepted papers only; ICML
publishes neither.
