# Foundations review route

The foundations page adds seven public source projects to the portfolio. Each implements a well-studied method and checks it against a reference the code did not produce:

- quantkit: option pricing, portfolio construction and a daily backtester with an enforced no-look-ahead contract; checked against Hull's worked example, put–call parity and closed-form portfolios.
- powerlift: A/B-test design and analysis; group sequential boundaries checked against Jennison & Turnbull's tables and published Lan–DeMets bounds, and tests against SciPy and statsmodels.
- ledgerline: a FastAPI double-entry ledger; balance, immutability, idempotency and reconciliation invariants enforced by unit, concurrency and Hypothesis state-machine tests.
- saas-analytics-warehouse: a dbt and DuckDB warehouse for a fictional SaaS company; MRR bridge reconciliation and movement exclusivity enforced as data tests that fail the build.
- searchlite: a TypeScript search engine; `explain()` must reproduce the returned score, and highlighting must escape hostile document text.
- contrastkit: WCAG 2.2 contrast, OKLCH fixes and color-vision simulation; checked against the WCAG formula, published simulation matrices and fix properties.
- citecheck: question answering with the Claude API over a fictional handbook; every sentence must cite a retrieved passage, and a checker rejects unretrieved citations and flags sentences whose numbers or content words are missing from their sources. Tests and the evaluation replay hand-written synthetic responses, so no model output is claimed.

These are independent, AI-assisted educational projects. Data is synthetic or fictional. The hosted dbt docs, search demo and Palette Auditor run on generated or bundled data. The page does not claim external adoption, production operation, or professional engagements.

## Runnable reviewer walkthroughs

Each project has a native HTML disclosure with one focused command, its expected result, a link to the proving test and a link to the implementation it exercises. The commands below were run on 23 October 2026 against each repository's published `main` branch:

| Project | Command | Observed result |
| --- | --- | --- |
| quantkit | `uv run pytest tests/test_backtest_engine.py -k lookahead -v` | 7 passed |
| powerlift | `uv run pytest tests/test_sequential.py -k "jennison_turnbull or published_bounds or five_looks" -v` | 12 passed |
| ledgerline | `uv run pytest tests/test_concurrency.py -v` | 6 passed |
| saas-analytics-warehouse | `make data build` | dbt `PASS=173 WARN=0 ERROR=0`, including `assert_mrr_bridge_reconciles` |
| searchlite | `npx vitest run test/engine/highlight.test.ts test/engine/scoring.test.ts -t "hostile\|exactly the score"` | 2 passed, 47 skipped |
| contrastkit | `npx contrastkit check 777 fff` (after `npm ci` and `npm run build`) | `4.47:1`, fails AA for normal text, exit code 1 |
| citecheck (run 24 October 2026) | `uv run citecheck index examples/handbook`, then `uv run citecheck ask "What is the deadline for submitting an expense?"` | Sentence 1 supported (9 of 9 content words); sentence 2 unsupported because `60` is in no cited passage; no API call |

The routes refer to actual repository tests and work without JavaScript. `tests/test_foundations.py` pins the exact commands, the seven source and design-note links, the three hosted links and the stated scope, so the page cannot drift from this record unnoticed.

## Publication

`projects/foundations.html` is an explicitly reviewed entry in `public-files.json`. It reuses the engineering lab's existing styles and progressively enhanced navigation, so no new visitor assets are published. The homepage entry and sitemap make it discoverable without changing the original eight project cards or their filters. Public staging still refuses unlisted files and verifies every released byte, and the staged semantic checks require all seven source and design-note routes.

## Verification

On 23 October 2026, and again on 24 October 2026 after citecheck was added, Python 3.13.9 / Node 24.18.0 / Playwright 1.61.1:

```sh
python3 -B -m unittest discover -s tests -v
npm ci --ignore-scripts --no-audit --no-fund
npm run build
PORTFOLIO_TEST_ROOT=_site npm run test:browser
python3 -B scripts/build_site.py --verify _site
```

The structural suite passed 77 tests, with the existing installed-handoff integration test skipped because it needs prepared wheels. `tests/foundations_showcase.cjs` runs inside the existing browser command: it opens every walkthrough (seven since 24 October 2026) by keyboard with JavaScript enabled and disabled, checks the source, design-note and hosted links, measures 320, 360, 768 and 1440 pixel widths with every walkthrough open, checks 200% zoom and follows the homepage entry. The staged payload verified 32 public files.

These checks establish page behavior and publication consistency. They do not verify the correctness of all linked project code; each repository's own tests and design notes carry that scope.

## 25 October 2026 workflow extensions

The original boundary walkthroughs above remain intact. The page now also links to complete, source-backed workflows: quantkit's six-file prior-data-only portfolio example; powerlift's seeded CSV → SRM/horizon gates → CUPED readout; ledgerline's disposable real-HTTP wallet lifecycle; searchlite's local-docs index and snapshot-only query; ContrastKit's actual browser download → CLI audit → fix → passing audit; and citecheck's real SQLite regressions for fenced-code citation boundaries. These additions are demonstrations on fictional inputs, not adoption or financial-performance claims.

The project explorer at `/projects/catalog.html` covers all 20 public projects. Its local commands point to the current workflows and their proving tests; the dated results above remain a record of the original walkthroughs.

## Selected-month churn investigation

After saas-analytics-warehouse PR1 merged at682595bcc89daa4160a7b697bcbb01f4d2e8ed75 on25 October2026, the page and catalog gained its read-only customer investigation route. The documented24-month synthetic build and module consumer reconcile historical customer count, total lost MRR and the payment-failure subset before writing three CSVs plus Markdown to a new directory. The source consumer passed88 Python tests, existing full lint/type/SQL checks,173/173 fresh dbt nodes, independent review and hosted CI. An isolated installed wheel produced identical outputs. Current active status does not erase historical churn; month-end and fictional-data limits remain explicit. The original dated bridge walkthrough above is preserved.
