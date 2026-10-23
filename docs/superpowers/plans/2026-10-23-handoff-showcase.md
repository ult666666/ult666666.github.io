# Operations Handoff Showcase Implementation Plan

> **For agentic workers:** Execute natively with superpowers:executing-plans. No child agents; the parent owns independent review and delivery. Steps use checkbox syntax for tracking.

**Goal:** Let a portfolio visitor follow the verified installed handoff and inspect its exact synthetic operational results.

**Architecture:** Extend the existing Engineering Lab with one always-visible native HTML section and an intro anchor link. Reuse its visual language and stylesheet; keep the source drill and all evidence outside the public payload.

**Tech Stack:** Native HTML/CSS, Python standard-library structural tests, existing Playwright Chromium browser suite.

**Spec:** `../../../../brief-handoff-showcase.md` in task-owned `work/` (T15 brief; supplied execution authorization covers this plan).

## Global Constraints

- Work in the specified task-owned checkout on `feat/handoff-showcase` from clean `main` `5e5726b46b30f957bf5c1867fb754fb86277b00c`.
- Preserve the exact 31-file staged inventory, eight homepage cards, four generated cases, three existing native walkthroughs and navigation anchors.
- No new public files, JavaScript, dependencies, remote mutations, publication, release-lock changes, parent ledger edits or child agents.
- Evidence links use reviewed ancestor `0dd85f87a7cdcd46030ff81bbb4de456019385ce`; releases remain RelayBox 0.4.0 / TraceBench 0.3.0 / Impact Ledger 1.2.0.
- Verify from fresh canonical temporary staging with `PORTFOLIO_TEST_ROOT`; preserve existing ignored `_site`.

## Review Focus

- A visitor may mistake HTML source links for hosted interactive reports: label the fixed GitHub code views explicitly.
- A visitor may copy a command before preparing its wheels: state checkout, Python 3.11+, separate explicit download, trusted existing parents and fresh output prerequisites next to it.
- A small screen or 200% zoom may clip a date, currency value or command: check page and element widths at 320px and zoom, with and without JavaScript.
- Keyboard visitors need visible focus and native disclosures: exercise actual Tab/Enter/Space and focus outline in Chromium.
- Print must preserve the comparison, mutation and reproduction evidence: inspect print media visibility and rendered PDF text.

---

### Task 1: Visitor explanation, evidence and exact comparison

**Files:**
- Create: `tests/test_handoff_showcase.py`.
- Modify: `projects/engineering-lab.html`, `styles.css`.
- Update: this plan and task-owned `../report-handoff-showcase.md`.

**Interfaces:**
- Consumes reviewed `examples/operations_handoff/{README.md,release-lock.json,oracle.json,cases.jsonl,evidence/}` and hand-derived CSV arithmetic.
- Produces `#operations-handoff`, an intro link, a captioned row/column-header table, fixed-SHA source links and one prepared-local-path verification command.

- [x] Write structural tests for stable discovery, fixed evidence destinations, semantic numeric table and deliberate 0/3/2 recorded-contract outcomes. Use literal hand-checked values, not the production summarizer.
- [x] Run `python3 -B -m unittest discover -s tests -p test_handoff_showcase.py -v`; confirm missing-section failures before implementing.
- [x] Add the concise HTML/CSS section and refresh the three release notes using released-tag documentation. Distinguish participant-hours, session-hours and the receipt/import/ack transactions; state educational AI-assisted bilingual synthetic scope.
- [x] Run the focused tests and check unchanged inventory, original case generation and release lock.

### Task 2: Real staged browser and whole-checkout verification

**Files:**
- Modify: `tests/engineering_showcase.cjs`.
- Update: this plan and task-owned `../report-handoff-showcase.md`.

**Interfaces:**
- Consumes Task 1's anchor/table/command and the existing browser suite's local staged HTTP server.
- Produces browser assertions for discovery, exact accessible table, no-JavaScript content, keyboard focus/disclosures, 320px/200% zoom wrapping, and print visibility.

- [x] Write the browser assertions before product HTML/CSS. Run them against a fresh baseline stage and confirm the missing handoff anchor fails.
- [x] Run the complete existing browser suite against a new stage built by `scripts.build_site.build/verify`; inspect real desktop/mobile/print captures.
- [x] Run `HANDOFF_WHEEL_DIR=../handoff-wheels python3 -B -m unittest discover -s tests -v`; expect all 67 original/integration tests plus new focused tests, no skips.
- [x] Independently compute table values from CSVs with standard-library `csv` and `Decimal`, compare to checked-in oracle and actual recorded evidence, and verify pinned source paths exist at the reviewed ancestor.
- [x] Check four cases unchanged, exact 31-file public payload before/after browser, `_site` untouched, `git diff --check`, and no forbidden scope changes.
- [x] Record exact RED/GREEN evidence, commands, commit, limits and final clean branch; commit locally. Parent performs independent review/PR/hosted verification.

## Execution record

- Baseline: clean `main` at the specified SHA; created `feat/handoff-showcase`. Full released-wheel baseline passed 67 tests with no skips.
- Ruling: use the explicitly assigned checkout and branch, without creating another worktree; scope and parent ownership are already specified. No approval loop or child reviewer is needed here.
- Pre-flight: Task 2 consumes the same public anchor, table and command specified by Task 1; no conflicting interfaces.
- Task 1: five focused tests failed on the absent handoff/release routes before implementation, then passed. A test initially counted all 11 homepage articles; source inspection showed three are approach cards, so the assertion now counts the eight project cards explicitly.
- Task 2: the real staged browser first failed on the missing intro link, then passed all existing journeys and the new handoff checks. Visual print review exposed pale table headings; an added contrast assertion reproduced the failure before the print palette correction. Final browser run passed with JavaScript enabled/disabled, 320/360/768/1440 widths, 200% zoom, keyboard focus and print contrast.
- Final verification: 72 Python tests passed with the actual released wheels and no skips; four generated cases verified; the new staging inventory verified before/after browser at 31 files; all 33 prior lab links remain; existing `_site` hashes remained identical.
- Independent arithmetic and fixed-source checks: current/prior fixture totals match the supplied oracle and recorded evidence; all four linked files are byte-identical at reviewed ancestor `0dd85f87a7cdcd46030ff81bbb4de456019385ce`. No release lock or source drill changes.
- Whole-branch independent review and remote delivery remain parent-owned under the dispatch; this author performed a scoped self-review, not an independent approval. No deferred findings or further rulings.
