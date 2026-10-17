# Charles Dai — software development portfolio

[![Portfolio checks](https://github.com/ult666666/ult666666.github.io/actions/workflows/portfolio.yml/badge.svg)](https://github.com/ult666666/ult666666.github.io/actions/workflows/portfolio.yml)

**Portfolio:** https://ult666666.github.io/
**GitHub:** https://github.com/ult666666

A responsive portfolio connecting seven real public projects to source code, live demonstrations where available, and three engineering case studies. Built as a small static site, with no application backend, analytics, account collection, or external font dependency.

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

## Architecture

- `index.html`: accessible, server-rendered project content; all projects remain available without JavaScript.
- `styles.css`: responsive layout, visible keyboard focus, reduced-motion support.
- `script.js`: progressively enhanced project filters and mobile navigation.
- `scripts/build_cases.py`: deterministic case-study source; `--check` catches stale generated pages.
- `scripts/build_site.py`: allowlisted static staging; Git metadata, local reports, tests and dependencies are never deployed.
- `tests/`: structural/metadata/deployment checks plus real Chromium interaction checks.
- `.github/workflows/portfolio.yml`: tests on pull requests and pushes; deploys only tested main-branch artifacts.

## Evidence and scope

The portfolio links to documented work, not fabricated employers, client engagements, contribution history or inflated usage statistics. Live websites, coursework, prototypes and research are labeled separately. The trading research project is not a deployed automated trading service or evidence of investment returns.

Project screenshots were copied from the corresponding public project repositories; their source links appear above. Social previews are generated from the checked-in SVG. No private trading source, runtime, credentials or personal financial data is included.
