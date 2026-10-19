# Charles Dai — software development portfolio

[![Portfolio checks](https://github.com/ult666666/ult666666.github.io/actions/workflows/portfolio.yml/badge.svg)](https://github.com/ult666666/ult666666.github.io/actions/workflows/portfolio.yml)

**Portfolio:** https://ult666666.github.io/
**GitHub:** https://github.com/ult666666

**[Fintech portfolio](https://ult666666.github.io/fintech.html):** Explore Value Horizon, the Ownership Frontier in Financing Lens, and the financial and engineering evidence behind the working Frontier AI Valuation Lab.

A responsive portfolio connecting eight real public projects to source code, live demonstrations where available, and four engineering case studies. Built as a small static site, with no application backend, analytics, account collection, or external font dependency.

## Start the review

The homepage features **Frontier AI Valuation Lab** first. Its [engineering review guide](https://ult666666.github.io/projects/frontier-ai-valuation-lab.html#review-guide) connects a short demo journey to the public source and checks for calculation consistency, exact navigation handoffs, save failures and evidence provenance. The evidence table becomes stacked cards on small screens and remains readable without JavaScript.

The project uses illustrative forecasts and a dated research snapshot. Its shared browser/API engine establishes consistency; the separate Python reference supplies the independent arithmetic check. Linked verification records identify the scope and date of their results.

## Selected projects

| Project | Scope | Evidence |
| --- | --- | --- |
| LineageGuard | Metadata-aware schema-change review | [Source](https://github.com/ult666666/lineageguard-datahub-agent) · [Demo](https://lineageguard-datahub-agent.vercel.app/) |
| MOTIONX | Next.js studio website and separate Python outreach validation | [Source](https://github.com/ult666666/motionx-studio) · [Site](https://madebymotionx.com/) |
| Agentic Trading Research | Research-only architecture and deterministic gates | [Public research snapshot](https://github.com/ult666666/agentic-trading-research) |
| ProofCast | Local media generation with asset provenance | [Source](https://github.com/ult666666/proofcast-backblaze) |
| Blast Radius Daily | Deterministic Devvit community puzzle | [Source](https://github.com/ult666666/blast-radius-daily) |
| Teen Budgeting | Coursework demo; fictional data and no persistent authentication | [Source](https://github.com/ult666666/teen-budgeting-hw3) |
| JUST-QR | Focused browser utility | [Source](https://github.com/ult666666/JUST-QR) |
| Frontier AI Valuation Lab | AI-assisted independent fintech project; reviewed economic FCFF model and shared browser/Node.js API | [Source](https://github.com/ult666666/frontier-ai-valuation-lab) · [Demo](https://frontier-ai-valuation-lab.vercel.app/) · [Case study](https://ult666666.github.io/projects/frontier-ai-valuation-lab.html) |

## Local development

Use Python 3.11+ and Node.js 22+.

```sh
python3 -m http.server 4319 --bind 127.0.0.1
python3 -B -m unittest discover -s tests -v
npm ci --ignore-scripts --no-audit --no-fund
npx playwright install chromium
npm run test:browser
npm run build
```

The build refuses to overwrite an existing `_site` directory. Start with a fresh checkout or remove only your previously generated `_site` output before rebuilding.

The optional browser harness accepts `PLAYWRIGHT_MODULE` for an installed Playwright package and `PORTFOLIO_CHROMIUM_EXECUTABLE` for an available Chromium binary. `PORTFOLIO_CHROMIUM_ARGS` accepts a JSON array of explicit launch arguments when the development environment needs them. These settings do not affect the published site.

## Architecture

- `index.html`: accessible static project content; all projects remain available without JavaScript.
- `fintech.html` / `fintech.css`: the dedicated fintech gateway, a labeled static valuation illustration and direct links to the working research tools and their evidence.
- `styles.css`: responsive layout, visible keyboard focus, reduced-motion support.
- `script.js`: progressively enhanced project filters and mobile navigation.
- `scripts/build_cases.py`: deterministic case-study source and optional escaped reviewer guide; `--check` catches stale generated pages.
- `scripts/build_site.py`: allowlisted static staging; Git metadata, local reports, tests and dependencies are never deployed.
- `tests/`: structural/metadata/deployment checks plus real Chromium interaction checks.
- `.github/workflows/portfolio.yml`: tests on pull requests and pushes; deploys only tested main-branch artifacts.

## Evidence and scope

The portfolio links to documented work, not fabricated employers, client engagements, contribution history or inflated usage statistics. Live websites, coursework, prototypes and research are labeled separately. The trading research project is not a deployed automated trading service or evidence of investment returns.

The Fintech gateway and filter highlight Frontier AI Valuation Lab, an independent, AI-assisted project by Charles Dai. Value Horizon preserves the explicit forecast and shows how many terminal cash-flow years remain in the valuation when later cash flows and residual value are set to zero. The portfolio's Anthropic Base illustration is a frozen example, not a second financial calculator. The live application carries the interaction and full calculation context.

Application 3.6 adds **Ownership Frontier** within the existing [Financing Lens](https://frontier-ai-valuation-lab.vercel.app/index.html#ownership-example). It connects an explicit ownership constraint to the maximum primary capital at an independently entered pre-money or post-money quote. Retaining 90% of a starting stake means a 10% holder stays at or above 9% of the company. In the hypothetical $250 billion pre-money example, the capital limit is approximately $27.78 billion; the current $25 billion round leaves $2.78 billion within that limit. Interpreting the same quote as post-money changes the limit to $25 billion.

The browser/API calculation contract and dedicated financing links and HTML/JSON exports carry the complete case, including the retention minimum. The portfolio explains the financial distinction and links to the working tool; it does not add a second financial calculator. The primary round assumes equal economic rights and retained cash, with no fees, option-pool changes, SAFEs, secondary sales or preferences. The limit is conditional ownership arithmetic, not an estimate of company funding needs or a recommended raise. Operating-case saves in the Research Casebook retain their existing scope. Read the [method](https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/FINANCING_LENS.md) or download the [worked PDF](https://frontier-ai-valuation-lab.vercel.app/downloads/Frontier_AI_Financing_Lens.pdf).

The case study connects financial-model review, a shared browser/Node.js calculation engine, dated sources and independent numerical verification. Its proof links lead to the actual methodology, API contract, verification record and source register. Scenario enterprise values and hypothetical equity bridges are distinct from security-specific price targets or trading results. The 18 October 2026 financial snapshot is unchanged.

The [Ownership Frontier 3.6 local portfolio verification record](docs/verification/ownership-3.6-local.json) records the current portfolio checks, preserved content and source hashes. It covers this portfolio integration; production deployment verification is recorded separately. The earlier [Financing Lens 3.5 receipt](docs/verification/financing-3.5-local.json) remains available as historical evidence.

Project screenshots were copied from the corresponding public project repositories; their source links appear above. Social previews are generated from the checked-in SVG. No private trading source, runtime, credentials or personal financial data is included.
