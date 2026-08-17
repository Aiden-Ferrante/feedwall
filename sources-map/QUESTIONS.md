# Standing questions

The 29 questions this system exists to answer. These define "quality" — a source is
good only relative to a question it helps answer.

Each is a **monitoring** question: something with a current state that changes over
time. Not predictions, not one-off lookups.

Coverage against the 143 feeds as of 2026-08-06:
`**` strong · `*` adequate · `~` partial · `-` nothing

| # | Subject | Question | Cadence | Have |
|---|---|---|---|:--:|
| 1 | economy | Is the labour market tightening or loosening? | monthly | ~ |
| 2 | economy | Where is inflation heading, and in which components? | monthly | ~ |
| 3 | economy | Which central banks are shifting stance, and how fast? | per-meeting | ~ |
| 4 | economy | Are credit conditions tightening - spreads, lending, delinquencies? | weekly | - |
| 5 | economy | What is the fiscal trajectory and debt-service burden? | quarterly | * |
| 6 | economy | How is the household sector holding up - income, savings, debt? | monthly | ~ |
| 7 | markets | What is the market pricing for rates and inflation ahead? | daily | - |
| 9 | markets | Is stress building in any funding or credit market? | daily | - |
| 10 | politics | What legislation with economic consequence is actually moving? | weekly | - |
| 11 | politics | How is AI and tech regulation evolving, and where? | weekly | - |
| 14 | geopolitics | Which conflicts are escalating or de-escalating? | daily | - |
| 15 | geopolitics | What is the state of US-China tech and trade restriction? | weekly | - |
| 16 | geopolitics | Where are sanctions and export controls tightening? | irregular | - |
| 17 | geopolitics | Are trade chokepoints and shipping lanes disrupted? | daily | - |
| 18 | technology | Where is the frontier of model capability, by what measure? | weekly | ** |
| 19 | technology | What is the state of compute supply - chips, fabs, power? | weekly | ~ |
| 20 | technology | What can be run locally, at what cost and quality? | weekly | ** |
| 21 | technology | Where is AI actually in production, with what results? | weekly | ~ |
| 22 | science | What new ML research changes practice? | daily | ** |
| 23 | science | What major results are landing outside ML? | weekly | ~ |
| 24 | society | What is happening to demographics - births, migration, households? | quarterly | - |
| 25 | society | What is the state of public health - outbreaks, mortality trends? | weekly | - |
| 26 | society | What is happening to housing affordability and supply? | monthly | - |
| 27 | energy | What is happening to electricity demand, especially datacentre load? | monthly | - |
| 28 | energy | What are energy prices doing, and why? | daily | - |
| 29 | energy | How fast is the energy transition actually moving - deployed capacity? | quarterly | - |
| 30 | business | What are earnings and guidance signalling about the real economy? | quarterly | - |
| 31 | business | Which industries are consolidating or being disrupted? | monthly | ~ |

Numbering is stable and gappy on purpose. Cut on 2026-08-06:

- **12** (elections) and **13** (court rulings) - drifted toward news-of-the-day rather
  than a monitorable state.
- **8** (capital rotation) - no honest free answer. Fund-flow data is the one genuinely
  paywalled category; everything free is a rough proxy.

## Standing tally

28 questions.

- strong: 3 (18, 20, 22) - all AI/ML
- adequate: 1 (5)
- partial: 8
- nothing: 16

Roughly 15 of the 16 uncovered questions are answered by **structured data**, not prose.
The coverage gap and the architecture gap are the same gap: the document half of the
pipeline is mature, the observation half barely exists.

See [SOURCES.md](SOURCES.md) for what would close it.
