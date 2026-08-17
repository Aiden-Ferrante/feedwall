# Source shopping list

What it would take to close the 17 uncovered questions in [QUESTIONS.md](QUESTIONS.md).

Every endpoint below was probed on **2026-08-06**. `alive` = responded; `needs key` =
responded with an auth error, so the endpoint is real and the only barrier is free
registration. Decision of record: **free API keys are acceptable** (no paid service, no
cloud LLM, no vendor lock-in).

Shape: `obs` = observations (typed rows), `doc` = documents (prose).

## Core - closes the gaps

Sorted by leverage: how many standing questions each unlocks.

| Source | Auth | Shape | Cadence | Answers | Probe |
|---|---|---|---|---|---|
| **FRED** `api.stlouisfed.org/fred` | free key | obs | daily | 1, 2, 4, 6, 7, 9, 26 | needs key |
| **EIA v2** `api.eia.gov/v2` | free key | obs | hourly | 27, 28, 29 | needs key |
| **SEC EDGAR** `data.sec.gov` | none (UA hdr) | obs+doc | daily | 30, 31, 15 | alive 200 |
| **Federal Register** `federalregister.gov/api/v1` | none | doc | daily | 11, 16, 10 | alive 200 |
| **Census** `api.census.gov/data` | free key | obs | monthly | 24, 26, 6 | alive 302 |
| **BLS v2** `api.bls.gov/publicAPI/v2` | key optional | obs | monthly | 1, 2 | alive 200 |
| **BEA** `apps.bea.gov/api` | free key | obs | quarterly | 2, 6 | alive 200 |
| **ACLED** `acleddata.com/api` | free key | obs | daily | 14 | needs key 403 |
| **IMF PortWatch** (ArcGIS FeatureServer) | none | obs | daily | 17 | alive 200 |
| **Congress.gov** `api.congress.gov/v3` | free key | obs+doc | daily | 10 | needs key 403 |
| **Trade.gov CSL** `data.trade.gov/consolidated_screening_list/v1` | free key | obs | irregular | 16 | needs key 401 |
| **CDC Socrata** `data.cdc.gov/resource` | none | obs | weekly | 25 | alive 200 |

**Twelve sources close 15 of the 16 gaps.** Seven need a free key; five need nothing.
For comparison, the existing 143 RSS feeds answer 3 questions well.

FRED alone covers seven questions, because it re-publishes BLS, BEA, Census and Treasury
series alongside market rates, spreads and breakevens. Hit BLS/BEA/Census directly when
the authoritative original and its revision history matter; use FRED for breadth.

## Keyless strengtheners

Cheap additions that lift `partial` to `covered`.

| Source | Shape | Lifts | Probe |
|---|---|---|---|
| **Treasury FiscalData** `api.fiscaldata.treasury.gov` | obs | 5 - debt to penny, interest expense | alive 200 |
| **Bank of England** news RSS | doc | 3 - non-Fed/ECB central banks | alive 200 |
| **Bank of Japan** `boj.or.jp/en/rss` | doc | 3 | alive 200 |
| **Redfin Data Center** (public S3 TSV) | obs | 26 - weekly housing, metro-level | alive 200 |
| **UN World Population Prospects** data portal API | obs | 24 - global demographics | alive 200 |
| **WHO** news RSS | doc | 25 - global outbreaks | alive 200 |
| **OFAC SDN** `sanctionslistservice.ofac.treas.gov` | obs | 16 - sanctions list snapshots | alive 302 |

## Still hard

Honest gaps that this list does not close. (Q8, capital rotation, was cut rather than
faked - fund-flow data is genuinely paywalled.)

- **Q19 - compute supply.** No single API. Assemble from TSMC monthly revenue, SEMI
  billings, EIA datacentre load, and Federal Register export-control notices. Stays
  partial by construction.
- **Q15 - US-China restriction.** Federal Register and BIS give the legal facts; posture
  and interpretation need think-tank documents (CSIS, Rhodium). Document-shaped, no API.
- **Q21 - AI in production.** Inherently anecdotal. Stays a document question.

## Sequencing

**Order by source shape, not by subject.** Shape decides how much new machinery a source
needs; the first source of any shape pays for every later one that shares it. Grouping by
subject would mean building four different adapters in phase 1 and none of them twice.

| Phase | Add | Shape | New machinery | Answers | Covered |
|---|---|---|---|---|:--:|
| — | *baseline* | | | | 4 |
| **0** | BoE, BoJ, WHO RSS | rss | none - paste 3 URLs into FreshRSS | 3, 25(p) | 5 |
| **1** | FRED | time series | **the entire observation path** | 1, 2, 4, 6, 7, 9, 26 | 12 |
| **2** | EIA, Treasury FiscalData | time series | none - reuses phase 1 | 5, 27, 28, 29 | 15 |
| **3** | BLS, BEA, Census | time series | none - reuses phase 1 | 24, deepens 1/2/6/26 | 16 |
| **4** | ACLED, IMF PortWatch, CDC | record query | paginated record adapter | 14, 17, 25 | 19 |
| **5** | SEC EDGAR | entity fact | concept-by-period adapter | 30, 31 | 21 |
| **6** | Federal Register, Congress.gov, OFAC/CSL | doc + snapshot | doc path reuse, list diffing | 10, 11, 16 | 24 |

Ends at **24 of 28 covered**. The remaining four (15, 19, 21, 23) are synthesis questions
that stay partial by nature, not for lack of a source.

### Why phase 1 is one source

FRED alone answers seven questions, so it is the only source worth paying the
architecture cost on. Everything gets decided once, here: Parquet layout, the series
registry, incremental fetch and watermarking, immutable raw versus derived tables,
scheduling, and failure surfacing. Phases 2 and 3 then add six more sources for close to
zero marginal design work, because they are the same shape.

Resist widening phase 1. A second source added before the first one is finished doubles
the design surface while proving nothing new.

### Cheapest real win

Phase 0 is three RSS URLs pasted into FreshRSS and takes minutes. It lifts Q3 (central
bank stance) from partial to covered and puts the first crack in Q25. Worth doing before
any of the rest, purely because it costs nothing.

## Notes

- **GDELT** (global event database) did not respond to probing and is unverified here.
  Worth revisiting for Q14/Q15 - it is broad but noisy, and ACLED is the higher-precision
  choice for conflict specifically.
- **UCDP** returned 401; it is an alternative or complement to ACLED for conflict events.
- Nearly every source above is **observation-shaped**, which is the point: closing these
  gaps is a data-ingestion problem, not a feed-subscription problem.
