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

## 2 November 2026 upgrade walkthroughs

Each project merged one upgrade in November 2026. Each section now keeps its original walkthrough and adds a second one for the new capability. Every command below ran on 2 November 2026 in a fresh copy of that repository's `main` (`git archive origin/main`), with its dependencies installed in the copy:

| Project (main) | Command | Observed result |
| --- | --- | --- |
| quantkit (7efb979), VaR model validation | `uv run pytest tests/test_var_size_power.py -v` | 3 passed |
| powerlift (11300a2), A/B/n tests with Dunnett | `uv run pytest tests/test_many_to_one.py -k "scipy_dunnett or family_wise" -v` | 2 passed, 24 deselected |
| ledgerline (51ecfc1), holds | `uv run pytest tests/test_holds_concurrency.py -v` | 8 passed |
| saas-analytics-warehouse (f18a390), incremental loads and snapshot | `make incremental-check MONTHS=6 SCALE=0.25 DAILY_DAYS=14` | `Relations compared: 24`, all equal, `Incremental build equals the full refresh.` The full `make incremental-check` gave the same result in 3 minutes 25 seconds |
| searchlite (62ef3a9), MaxScore and block-max top-k | `npx vitest run test/engine/pruning.test.ts` | 17 passed |
| contrastkit (0eba84a), anomalous trichromacy | `npx contrastkit check 2f855a c53030 --cvd deuteranomaly:0.6 --cvd deuteranopia` (after `npm ci` and `npm run build`) | ΔE_OK 0.076 under deuteranomaly at 0.6 and 0.063 under deuteranopia, against 0.269 for typical vision; WCAG ratio 1.20:1, exit code 1 |
| citecheck (83cad56), claim-level checker | `uv run citecheck ask --checker lexical "Do I need a doctor's note when I take a sick day?"`, then the same question without `--checker lexical` | Lexical: sentence 1 supported (10 of 10 content words found). Claim-level: unsupported, "only the claim is negated". No API call |

After the independent review fixes merged later on 2 November 2026, two of these commands were run again on the new `main`: powerlift (5e7c5d5) gave 2 passed, 32 deselected, because the review added Dunnett tests to the same file, and searchlite (e3b3c5a) gave 19 passed, with two new pruning tests. The pages show these current results.

The original walkthroughs were run again on the same branches. quantkit gave 7 passed, powerlift 12 passed and searchlite 2 passed, 47 skipped, as recorded on 23 October. contrastkit's `npx contrastkit check 777 fff` still gave 4.47:1, failing AA, with exit code 1. Three results had changed and the page now states them:

- ledgerline's `uv run pytest tests/test_concurrency.py -v` gives 7 passed, not 6.
- saas-analytics-warehouse's `make data build` reports `PASS=192 WARN=0 ERROR=0` (it was 173), with the snapshot and its four history tests.
- citecheck's default checker is now claim-level: the expense question's second sentence is unsupported because "the claim says 60 days where the cited text says 30 days". No API call is made.

`tests/test_foundations.py` now also pins these observed results and rejects the three stale ones. The browser suite requires two walkthroughs in every section and opens all fourteen by keyboard. The published held-out, simulation and timing figures on the page come from each repository's README on `main`, and the page links the method behind each one.

## 17 November 2026 walkthrough verification

All fourteen Foundations walkthroughs and the seven corresponding catalog workflows ran from fresh checkouts of the public revisions below. The Python projects used Python 3.12.13 with uv. The TypeScript projects used Node 24.18.0 and npm 11.16.0.

| Project and revision | First walkthrough | Second walkthrough | Catalog result |
| --- | --- | --- | --- |
| [quantkit e6d3e02](https://github.com/ult666666/quantkit/tree/e6d3e024b192157c59b2adb468a17780d164e6e9) | Seven look-ahead tests passed. The six built-in strategy cases scrambled future prices at ten sampled cutoffs each. | All three VaR size and power tests passed. | The 99% EWMA forecast recorded 14 exceptions in 1,009 days, with three in the last 250 days. |
| [powerlift 59c2f52](https://github.com/ult666666/powerlift/tree/59c2f526bbdd9622a6f749f477da09fd8b2be254) | Twelve published-boundary tests passed. | Two Dunnett checks passed, with 32 other tests deselected. | The four arms each had 2,000 observations. Only D differed significantly from the control under Dunnett’s adjustment, with an estimated increase of 0.948. |
| [ledgerline 4558a6a](https://github.com/ult666666/ledgerline/tree/4558a6a447dc3a331244f630c88c26e7353a0aba) | Seven transfer concurrency tests passed on SQLite. | Eight hold concurrency tests passed on SQLite and four PostgreSQL cases were skipped. All 19 tests in the two files passed together on an isolated PostgreSQL 16.2 server. | The HTTP hold demo reused the capture transaction on retry and ended with $68 posted, $0 held and $68 available. Reconciliation found two transactions and four entries. |
| [saas-analytics-warehouse 56b1b49](https://github.com/ult666666/saas-analytics-warehouse/tree/56b1b49864f97eb26708c8645ca5b39a451c35a1) | The default 36-month build completed all 198 dbt nodes, including the MRR bridge reconciliation, with zero warnings or errors. | All 25 relations matched the full refresh after 14 daily loads. The comparison counts duplicate rows and rounds floating-point values to ten decimal places. | The 24-month build’s December 2024 report reconciled eight churned customers and $1,514 of lost MRR. Five customers with payment failures accounted for $1,430 of that loss. |
| [searchlite 8accfde](https://github.com/ult666666/searchlite/tree/8accfde3b60257712930fa512c7bdab72863bec0) | The highlighting and score explanation checks passed. Vitest skipped the other 49 tests in those files. | All 19 pruning tests passed. | All three judged queries passed for the saved three-document index. |
| [contrastkit a722e57](https://github.com/ult666666/contrastkit/tree/a722e574f3c321929cac8819faf27046ffa76b56) | Gray on white measured 4.47:1 and failed normal-text AA. The CLI exited 1. | Green on red measured 1.20:1 and exited 1. The OKLab distance was 0.269 for typical vision, 0.076 for deuteranomaly at severity 0.6 and 0.063 for deuteranopia. | All 294 library and 70 app tests passed. The built CLI reproduced the green/red result. |
| [citecheck 79ae1a8](https://github.com/ult666666/citecheck/tree/79ae1a81a0e7362508848070f861c6cd449d6bc5) | The first expense sentence matched nine of nine content words. The checker flagged 60 days in the second sentence against the cited 30 days. | Word overlap accepted the sick-note sentence with ten of ten content words. The claim-level checker flagged the flipped negation. | The claim-level checker flagged 44 of 48 unsupported sentences and two of 29 supported ones. Word overlap flagged 20 of 48 and one of 29, respectively. All answers were replayed fixtures. |
