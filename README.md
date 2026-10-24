# Charles Dai — software development portfolio

[![Portfolio checks](https://github.com/ult666666/ult666666.github.io/actions/workflows/portfolio.yml/badge.svg)](https://github.com/ult666666/ult666666.github.io/actions/workflows/portfolio.yml)

**Portfolio:** https://ult666666.github.io/
**GitHub:** https://github.com/ult666666

**[Fintech portfolio](https://ult666666.github.io/fintech.html):** Explore Capital Strategy Studio: a working financing decision that connects business objectives, ownership, scenario analysis and inspectable full stack engineering.

A responsive portfolio connecting nine selected projects, three engineering-lab additions and seven foundations builds to source code, live demonstrations where available, and four detailed engineering case studies. Built as a small static site, with no application backend, analytics, account collection, or external font dependency.

The homepage also offers a [six-project recent-build spotlight](https://ult666666.github.io/#recent-builds): shortcuts to source, demos and clear local/synthetic boundaries, not extra claims of production deployments.

The first-screen specialty routes jump to real projects without client-side routing. Four gallery images come directly from pinned commits in their public project repositories; SHA-256 digests, source paths, and dimensions are recorded in [docs/RECENT_VISUALS.json](docs/RECENT_VISUALS.json). Two additional cards use decorative CSS diagrams. No screenshot requires personal or account data.

## Start the review

The homepage features **Frontier AI Valuation Lab** first. Its [engineering review guide](https://ult666666.github.io/projects/frontier-ai-valuation-lab.html#review-guide) connects a short demo journey to the public source and checks for calculation consistency, exact navigation handoffs, save failures and evidence provenance. The evidence table becomes stacked cards on small screens and remains readable without JavaScript.

The project uses illustrative forecasts and a dated research snapshot. Its shared browser/API engine establishes consistency; the separate Python reference supplies the independent arithmetic check. Linked verification records identify the scope and date of their results.

## Selected projects

The [engineering lab](https://ult666666.github.io/projects/engineering-lab.html) adds three independent, AI-assisted portfolio builds: [RelayBox](https://github.com/ult666666/relaybox) for durable signed webhook ingestion, [TraceBench](https://github.com/ult666666/tracebench) for offline AI evaluation, and [Impact Ledger](https://github.com/ult666666/impact-ledger) for full-stack nonprofit operations reporting. Their READMEs provide reproducible local quickstarts, synthetic fixtures, test evidence and English/Chinese handoff documentation. The [hosted Impact Ledger preview](https://ult666666.github.io/impact-ledger/) runs on a bundled synthetic snapshot; persistence belongs to its local Python API.

The first workflow releases add [RelayBox 0.2.0 local processing and receipts](https://github.com/ult666666/relaybox/releases/tag/v0.2.0), [TraceBench 0.2.0 standalone HTML reports](https://github.com/ult666666/tracebench/releases/tag/v0.2.0), and [Impact Ledger 1.1.0 prior-period comparison and printing](https://github.com/ult666666/impact-ledger/releases/tag/v1.1.0). Open the [synthetic evaluation report](https://ult666666.github.io/tracebench/) to inspect its two deliberate regressions. These links preserve a dated release scope; timing observations and prices are supplied fixtures, and local receipt publication is a separate transaction from inbox acknowledgment.

The [foundations page](https://ult666666.github.io/projects/foundations.html) adds seven independent, AI-assisted builds that check well-studied methods against references they did not produce: [quantkit](https://github.com/ult666666/quantkit) for option pricing, portfolios and look-ahead-safe backtests; [powerlift](https://github.com/ult666666/powerlift) for experiment statistics; [ledgerline](https://github.com/ult666666/ledgerline) for an idempotent double-entry ledger API; [saas-analytics-warehouse](https://github.com/ult666666/saas-analytics-warehouse) for tested dbt metrics; [searchlite](https://github.com/ult666666/searchlite) for explainable search ranking; [contrastkit](https://github.com/ult666666/contrastkit) for accessible color; and [citecheck](https://github.com/ult666666/citecheck) for Claude API question answering whose citations are checked against the retrieved sources. Each section gives one runnable command and its observed result. The hosted [dbt docs](https://ult666666.github.io/saas-analytics-warehouse/), [search demo](https://ult666666.github.io/searchlite/) and [Palette Auditor](https://ult666666.github.io/contrastkit/) use synthetic or bundled data.

| Project | Scope | Evidence |
| --- | --- | --- |
| LineageGuard Studio | Typed orchestration, evidence readiness, interruption recovery and evaluations | [Source](https://github.com/ult666666/lineageguard-datahub-agent) · [Demo](https://lineageguard-datahub-agent.vercel.app/) |
| MOTIONX | Next.js studio website and separate Python outreach validation | [Source](https://github.com/ult666666/motionx-studio) · [Site](https://madebymotionx.com/) |
| Agentic Trading Research | Research-only architecture and deterministic gates | [Public research snapshot](https://github.com/ult666666/agentic-trading-research) |
| ProofCast | Local media generation with asset provenance | [Source](https://github.com/ult666666/proofcast-backblaze) |
| Blast Radius Daily | Deterministic Devvit community puzzle | [Source](https://github.com/ult666666/blast-radius-daily) |
| Teen Budgeting | Coursework demo; fictional data and no persistent authentication | [Source](https://github.com/ult666666/teen-budgeting-hw3) |
| JUST-QR | Focused browser utility | [Source](https://github.com/ult666666/JUST-QR) |
| Luma Keys | AI-assisted offline piano practice desktop app: numbered score, sheet music and falling notes, 3-D hands playing a planned fingering, graded sight reading and on-device PDF recognition | [Source](https://github.com/ult666666/luma-keys) · [Hand motion design](https://github.com/ult666666/luma-keys/blob/main/docs/HAND_MOTION_DESIGN.md) |
| Frontier AI Valuation Lab | AI-assisted independent fintech project; capital decisions, economic FCFF valuation, independent numerical references and a shared browser/Node.js API | [Source](https://github.com/ult666666/frontier-ai-valuation-lab) · [Capital Studio](https://frontier-ai-valuation-lab.vercel.app/capital.html#worked-decision) · [Case study](https://ult666666.github.io/projects/frontier-ai-valuation-lab.html) |

## Inspect the engineering

The homepage now connects three concrete questions to public implementation evidence: financial arithmetic, rejected schema-change inputs, and the publication boundary of the portfolio itself. These routes work without JavaScript and distinguish verification from forecasts, deployment authority and absolute-security claims.

The [publication boundary](docs/PUBLICATION_BOUNDARY.md) records a reproduced directory-copy weakness and its repair. An exact `public-files.json` inventory replaces implicit approval of everything in `assets/` or `projects/`. The staged site carries a deterministic `release-manifest.json` with per-file SHA-256 values and is verified again before upload. Sensitive findings belong in the private route in [SECURITY.md](SECURITY.md), never a public issue with secrets attached.

## Local development

Use Python 3.11+ and Node.js 22+.

```sh
python3 -m http.server 4319 --bind 127.0.0.1
python3 -B -m unittest discover -s tests -v
npm ci --ignore-scripts --no-audit --no-fund
npx playwright install chromium
npm run build
PORTFOLIO_TEST_ROOT=_site npm run test:browser
python3 -B scripts/build_site.py --verify _site
```

The build refuses to overwrite an existing `_site` directory. Start with a fresh checkout or remove only your previously generated `_site` output before rebuilding.

The optional browser harness accepts `PLAYWRIGHT_MODULE` for an installed Playwright package and `PORTFOLIO_CHROMIUM_EXECUTABLE` for an available Chromium binary. `PORTFOLIO_CHROMIUM_ARGS` accepts a JSON array of explicit launch arguments when the development environment needs them. These settings do not affect the published site.

The [installed synthetic operations handoff](examples/operations_handoff/README.md) is a source-only integration of released RelayBox 0.4.0, TraceBench 0.3.0 and Impact Ledger 1.2.0 wheels. It verifies real signed HTTP delivery, receipts, advisory CSV imports, exact bilingual fixture accounting, recovery and recorded contract exits 0/3/2 in a fresh offline environment. Its normalized [clean report](examples/operations_handoff/evidence/clean.html) and deliberately [mutated regression report](examples/operations_handoff/evidence/synthetic-regression.html) stay outside the Pages inventory. The separate read-only `handoff.yml` workflow downloads only the hash-locked public release assets before running the drill.

## Architecture

- `index.html`: accessible static project content; all projects remain available without JavaScript.
- `projects/engineering-lab.html`: a static review route for three complementary engineering projects, their source, architecture and verification records.
- `projects/foundations.html`: a static review route for seven reference-checked builds, each with source, design notes, live demos where available and one runnable proving test.
- `fintech.html` / `fintech.css`: the dedicated fintech gateway, a labeled three-plan capital comparison and direct links to the working decision studio and its evidence.
- `styles.css`: responsive layout, visible keyboard focus, reduced-motion support.
- `script.js`: progressively enhanced project filters and mobile navigation.
- `scripts/build_cases.py`: deterministic case-study source and optional escaped reviewer guide; `--check` catches stale generated pages.
- `public-files.json`: exact reviewed deployment paths; new assets require an explicit inventory update.
- `scripts/build_site.py`: snapshot-based static staging and byte verification; unlisted assets, unsafe file types and missing reviewed files refuse before output.
- `release-manifest.json`: generated public SHA-256 inventory, not a signature or security certification.
- `tests/`: structural/metadata/deployment checks plus real Chromium interaction checks.
- `.github/workflows/portfolio.yml`: tests on pull requests and pushes; deploys only tested main-branch artifacts.

## Evidence and scope

The portfolio links to documented work, not fabricated employers, client engagements, contribution history or inflated usage statistics. Live websites, coursework, prototypes and research are labeled separately. The trading research project is not a deployed automated trading service or evidence of investment returns.

The Fintech gateway and filter highlight Frontier AI Valuation Lab, an independent, AI-assisted project by Charles Dai. Application **4.0 introduces Capital Strategy Studio**. The portfolio's static three-plan illustration comes from its hypothetical Anthropic worked decision: a $25 billion capital objective and an 88% retained-stake floor. A and B meet both objectives; C preserves more ownership but falls $5 billion short of the capital objective. Raising the retained-stake floor to 90% leaves A eligible. The live application carries the complete editable calculation.

The review journey follows **Define → Compare → Challenge → Record**. Visitors can compare up to six financing plans across nine explicit scenarios, inspect signed residual allocations and finite-scenario minimax regret, and see when pairwise switching values or the more demanding all-scenario pricing interval change the conclusion. The analyst's choice and reasoning remain separate from the comparison rule. Exact share links, a recomputed JSON decision record, a standalone HTML brief and the worked PDF keep those inputs and judgments together.

The business case, financial model, numerical reference and engineering architecture are documented separately so their claims are inspectable. The application uses a shared browser/Node.js handler with a bounded request parser, complete result parity and stale-response invalidation. Its independent Python capital reference uses Decimal cash-flow arithmetic and Fraction share ledgers. This is a deterministic research demo: scenario counts are not probabilities, signed residual allocations are not investment returns, and quoted financing offers are hypothetical. Read the [capital method](https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/CAPITAL_STRATEGY.md), inspect the [architecture](https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/ARCHITECTURE.md), or open the [worked decision brief](https://frontier-ai-valuation-lab.vercel.app/downloads/Frontier_AI_Capital_Decision.html).

The existing tools remain available as supporting workspaces. Value Horizon preserves the explicit forecast and shows how many terminal cash-flow years remain when later cash flows and residual value are set to zero.

Application 3.6 introduced **Ownership Frontier** within the existing [Financing Lens](https://frontier-ai-valuation-lab.vercel.app/index.html#ownership-example). It connects an explicit ownership constraint to the maximum primary capital at an independently entered pre-money or post-money quote. Retaining 90% of a starting stake means a 10% holder stays at or above 9% of the company. In the hypothetical $250 billion pre-money example, the capital limit is approximately $27.78 billion; the current $25 billion round leaves $2.78 billion within that limit. Interpreting the same quote as post-money changes the limit to $25 billion.

The browser/API calculation contract and dedicated financing links and HTML/JSON exports carry the complete case, including the retention minimum. The portfolio explains the financial distinction and links to the working tool; it does not add a second financial calculator. The primary round assumes equal economic rights and retained cash, with no fees, option-pool changes, SAFEs, secondary sales or preferences. The limit is conditional ownership arithmetic, not an estimate of company funding needs or a recommended raise. Operating-case saves in the Research Casebook retain their existing scope. Read the [method](https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/FINANCING_LENS.md) or download the [worked PDF](https://frontier-ai-valuation-lab.vercel.app/downloads/Frontier_AI_Financing_Lens.pdf).

The case study connects financial-model review, a shared browser/Node.js calculation engine, dated sources and independent numerical verification. Its proof links lead to the actual methodology, API contract, verification record and source register. Scenario enterprise values and hypothetical equity bridges are distinct from security-specific price targets or trading results. The 18 October 2026 financial snapshot is unchanged.

The [Capital Strategy 4.0 local portfolio verification record](docs/verification/capital-4.0-local.json) records 34 structural tests, the real browser workflow, 56 navigation-resilience checks, the reviewed staged-file manifest and preserved concurrent changes. Production deployment verification is recorded separately in the application's release evidence. The historical [Ownership Frontier 3.6 record](docs/verification/ownership-3.6-local.json) and [Financing Lens 3.5 receipt](docs/verification/financing-3.5-local.json) retain their original revision and scope.

Project screenshots were copied from the corresponding public project repositories; their source links appear above. Social previews are generated from the checked-in SVG. No private trading source, runtime, credentials or personal financial data is included.

`assets/luma-keys-practice.png` is downscaled to 1440 × 900 and reduced to a 256-color palette from `docs/screenshots/practice-hands.png` in Luma Keys commit `b5d41ea8804b0cd4d3a489436536e7f7f490f2ab`. SHA-256: `75ec4d8632c3e0c64886b3219ca6e7ac6880edeea5eac14afee5754bcd18a326`. It shows the app's development build on a public-domain Mutopia score.

## LineageGuard Studio 2.0

The [Studio case study](projects/lineageguard.html) now documents the executable DAG, source-bound evidence, bounded runtime, local SQLite writer fencing, recovery and evaluations. Its screenshot is copied byte-for-byte from the verified public Studio source. Browser-session preview and durable-local behavior are clearly separated. The original classic demo remains available in its repository. No private trading runtime or real catalog data is included.


### Review Inspector: portable, offline consistency checks

The LineageGuard case study now includes the shipped [Review Inspector](projects/lineageguard.html#review-inspector), a three-minute engineering walkthrough, and revision-pinned implementation/test links. It distinguishes recomputed internal consistency from source authentication, recorded decisions from inspection-time evidence freshness, and browser/local persistence from cloud execution.

`assets/lineageguard-review-inspector.png` is copied byte-for-byte from `assets/review-inspector.png` in LineageGuard commit `6ed607b5c9ff6f46f2bb3214b04d040b04c02c52`. SHA-256: `53afbb9e409fc1e94e3fdf024c4ed90ba0bc9a14695a5422893c110c12efc266`. It shows synthetic source data. No private local browser screenshot or runtime is published.

The Inspector revision's 120 Node tests, 31 browser journeys and 19 evaluation assertions describe separate overlapping checks. They do not retroactively change the original v2.0.0 release receipt or establish independent catalog truth. Showcase tests cover pinned links, screenshot integrity, accessible anchors, no-JavaScript content, responsive widths and publication inventory. Other case pages and the fintech gateway remain byte-identical in this update.

The [Inspector showcase verification record](docs/verification/lineageguard-inspector-showcase.json) binds the public source screenshot, authored case files and preserved other projects. Deployment results are verified separately after publication.

## License

The source code is available under the [MIT License](LICENSE). The portfolio's written content, images and other media are © 2026 Charles Dai, all rights reserved, and are not covered by the MIT License.
