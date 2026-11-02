# Case studies

How the five case studies are built, and the background behind the two most detailed ones.

## How they are built

`scripts/build_cases.py` holds each case study as plain data: a short introduction, sections with stable ids, one Limits section and a closing "Code and docs" list. Running the script writes `projects/<slug>.html`. With `--check` it fails if a page is stale, and `npm run build` runs that check. All text is escaped when it is rendered, and `tests/test_case_review.py` checks that markup in the data cannot become an element or an attribute.

Section ids stay the same when the text changes, because other pages and repositories link to them, for example `#call-auctions`, `#dbt-manifest`, `#review-inspector`, `#review-guide` and `#engineering-evidence`.

The pages follow the copy rules in [DESIGN.md](DESIGN.md): plain headings, one or two numbers per section, limits stated once, and AI assistance mentioned once near the end. Test counts and other figures that go stale belong in each project's own verification record, not on these pages.

## Frontier AI Valuation Lab and the fintech page

The fintech page's three-plan table comes from the app's hypothetical Anthropic worked decision: a $25 billion capital objective and an 88% retained-stake floor. Plans A and B meet both objectives. Plan C keeps more ownership but falls $5 billion short of the capital objective. Raising the floor to 90% leaves only A. The live application has the full, editable calculation.

Capital Strategy Studio (application 4.0) follows four steps: define, compare, challenge and record. It compares up to six financing plans across up to nine scenarios, shows signed residual allocations and finite-scenario minimax regret, and shows when a pairwise switching value or the stricter all-scenario pricing interval changes the conclusion. The analyst's choice and reasoning stay separate from the comparison rule. Share links, a recalculated JSON decision record, a standalone HTML brief and the worked PDF keep the inputs and the judgment together.

The application runs one handler in the browser and in Node.js, with a bounded request parser and a check that both return the same result. Its independent Python capital reference uses Decimal cash-flow arithmetic and Fraction share ledgers. Scenario counts are not probabilities, signed residual allocations are not investment returns, and the financing offers are hypothetical. The methods are in the app's [capital method](https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/CAPITAL_STRATEGY.md) and [architecture](https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/ARCHITECTURE.md) documents.

Ownership Frontier, added in application 3.6 inside the Financing Lens, connects an ownership constraint to the most primary capital a round can raise at an entered pre-money or post-money quote. Keeping 90% of a starting stake means a 10% holder stays at or above 9% of the company. At the hypothetical $250 billion pre-money quote the limit is about $27.78 billion, so the $25 billion round leaves $2.78 billion of room. Read as post-money, the same quote gives a limit of $25 billion. The round model assumes equal economic rights and retained cash, with no fees, option-pool changes, SAFEs, secondary sales or preferences. The limit is ownership arithmetic, not an estimate of how much a company needs. See the [financing method](https://github.com/ult666666/frontier-ai-valuation-lab/blob/main/docs/FINANCING_LENS.md).

Value Horizon keeps the explicit forecast and shows how many terminal cash-flow years remain when later cash flows and residual value are set to zero. The financial snapshot behind all of these is dated 18 October 2026 and is unchanged by application 4.0.

### Verification records

These records describe the portfolio pages at the time of each release. Production deployment checks are recorded in the application's own release notes.

- [capital-4.0-local.json](verification/capital-4.0-local.json): 34 structural tests, the browser workflow, 56 navigation-resilience checks, the reviewed staged-file manifest and the concurrent changes it preserved.
- [ownership-3.6-local.json](verification/ownership-3.6-local.json) and [financing-3.5-local.json](verification/financing-3.5-local.json) keep their original revision and scope.

## LineageGuard Studio

The case study covers the review workflow and its compiled graph, evidence bound to its source, the bounded runtime, SQLite writer fencing and recovery, the labelled policy benchmark, the dbt manifest adapter, Review Inspector and saved-review comparison. Its hero screenshot is copied unchanged from the public Studio source. The browser-session preview and the durable local runtime are described separately. The original classic demo is still in the repository.

Review Inspector was added on `main` after the `v2.0.0` tag. It keeps recomputed internal consistency apart from source authentication, recorded decisions apart from evidence freshness at inspection time, and browser or local storage apart from any cloud execution. The page's Inspector and comparison links are pinned to commit `ed48eea4370d28c52f3268fadcd3b82a3632a691`, the Studio redesign the screenshots come from.

Suite sizes, as recorded when the page last stated them:

- At the Inspector revision: 120 Node tests, 31 browser journeys and 19 evaluation assertions.
- At commit `bc14370`, checked on 2 November 2026: 201 Node tests (20 of them seeded property tests, 4 on generated dbt manifests), 45 browser journey checks across both storage modes, 19 evaluation assertions and the 105-case policy benchmark.

These are separate, overlapping checks. They do not change the original `v2.0.0` release record, and they are not independent evidence that a catalog is correct. Current numbers are in the repository's [verification record](https://github.com/ult666666/lineageguard-datahub-agent/blob/main/docs/VERIFICATION.md).

[lineageguard-inspector-showcase.json](verification/lineageguard-inspector-showcase.json) binds the public source screenshot, the authored case files and the other projects' pages as they were when the Inspector section was added.
