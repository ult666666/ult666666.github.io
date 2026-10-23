# Installed operations handoff implementation plan

> **For agentic workers:** Execute inline with superpowers:executing-plans. Parent supplies the independent whole-branch review; no child agents or publication.

**Goal:** Verify a deterministic bilingual operations handoff using only the three reviewed released wheels.

**Architecture:** A standard-library launcher validates the lock, wheels and output destination before creating a private fresh venv. An isolated child runs real loopback services and installed TraceBench CLI, then the launcher publishes only explicitly named normalized evidence files after all assertions pass.

**Tech Stack:** Python 3.11+, unittest, venv/pip offline, released RelayBox 0.4.0, TraceBench 0.3.0 and Impact Ledger 1.2.0.

**Spec:** Parent task brief `../brief-installed-handoff.md` (outside the source repository).

## Global constraints

- Source-only tooling; exact public allowlist, eight cards, four cases and existing browser workflow stay intact.
- No source imports, network in verifier, shell commands, real records, secrets, database/venv/raw-log publication, pushes or ledger edits.
- Trust released project code and local output parents; no hostile concurrent-replacement sandbox claim.
- Fixed oracle: 4 sessions/7 attendance before the advisory race; current 2 sessions/3 people/4 attendance/7 participant-hours/3.5 session-hours/130.25 budget/130.25 actual/0 variance; prior 2/2/3/3.25/2/130.10/131.00/0.90.
- CI read-only, bounded and using existing pinned Actions; parent checks hosted execution and publication.

## Review focus

- Existing, symlink, hard-link or source-aliased output must remain untouched (Task 1).
- Wheel set, metadata and SHA mismatch must fail before installation (Task 1).
- Child failure or partial publication must leave no claimed-success directory (Task 1).
- Advisory preview must not reserve IDs; a competing import forces whole-file duplicate rejection (Task 2).
- Contract baseline must catch an actual recorded mutation with exit 3, while malformed input exits 2 (Task 2).

### Task 1: Safe offline launcher

Files: `scripts/verify_handoff.py`, `tests/test_handoff.py`, `examples/operations_handoff/release-lock.json`.
Interfaces: `validate_inputs(wheel_dir, output, lock) -> (canonical_wheels, canonical_output)`; `verify(wheel_dir, output) -> None`.

- [x] Write unit tests for missing/foreign/hash/metadata wheels, selected symlinks, existing and aliased output, Unicode/spaced/leading-hyphen names, no mutation before validation, and subprocess-failure cleanup.
- [x] Run `python3 -B -m unittest discover -s tests -p test_handoff.py -v`; observe missing launcher failure.
- [x] Implement strict bounded wheel validation; fresh venv installation with argv lists, cleared PYTHONPATH and `-I`; private temporary execution and exclusive final output publication.
- [x] Re-run focused tests and the complete existing suite.
- [x] Commit launcher and tests.

### Task 2: Real installed handoff and contract reports

Files: `examples/operations_handoff/{run_installed.py,sessions.csv,attendance.csv,participants.json,oracle.json,cases.jsonl,README.md}`, integration test in `tests/test_handoff.py`.
Interfaces: isolated child `run_installed.py --fixtures DIR --output DIR`, with fresh venv interpreter; bounded whitelist of normalized files consumed by launcher.

- [x] Write independent assertions for exact counts/cents/hundredths, inclusive filters, recovery columns, retained clean/regression reports and exit codes 0/3/2; observe failed integration before child exists.
- [x] Implement signed HTTP 202/200 stable identity and 409 unchanged replay; real receipt worker; metrics nonmutation; canonical receipt CSV adapter; HTTP preview/import/summary/comparison, repeated-import rejection and separate-program advisory race.
- [x] Stop service/worker before acknowledged inbox backup, verify, CLI restore to new path; compare every persisted column privately, report only normalized counts/equality.
- [x] Run installed CLI against actual records and checked-in json_subset cases, clean baseline and deliberate synthetic mutation; retain JSON/Markdown/HTML reports and bounded input/output hashes.
- [x] Run offline full integration against parent's exact locked wheel directory, then full portfolio suite and staged browser/publication checks; inspect retained reports for paths/tokens/runtime files.
- [x] Commit child, fixtures and evidence.

### Task 3: Read-only CI and handoff documentation

Files: `.github/workflows/handoff.yml`, `scripts/fetch_handoff_wheels.py`, README and final external `../report-installed-handoff.md`.
Interfaces: fetcher requires explicit `--download --output NEW_DIR`; fixed reviewed HTTPS URLs only, bounded request time and wheel size; verifier remains offline.

- [x] Write failing fetcher tests for missing explicit mode, protected destination, bounded download and wrong hash with cleanup.
- [x] Implement explicit downloader and separate CI job with pinned checkout/setup-python, no write permissions/secrets and explicit evidence artifact paths.
- [x] Document English and concise Chinese operations, transaction boundaries, artifact trust and synthetic regression limits.
- [x] Run full suite, offline integration, staged browser and exact publication validation; report exact commits, release locks, red/green commands and remaining parent review/hosted CI responsibilities.
- [x] Commit CI/docs, leave clean feature branch for parent review.

## Execution record

- Task 1: seven boundary failures observed before the launcher existed; focused tests then passed. Full suite at that checkpoint: 57 tests, one explicitly skipped installed integration. Commit `fd54fd7`.
- Task 2: real offline installed integration first failed because the child was absent, then passed against the exact locked wheels. A thread-start failure test reproduced an open bound-server cleanup gap; fixed and green. Full final suite: 67/67, including the installed integration.
- Task 3: five downloader failures observed before implementation; a redirect-chain deadline test subsequently failed, then passed after propagating the shared deadline to redirected requests. Two real public-download/offline runs reproduced all ten retained evidence files byte-for-byte.
- Fresh temporary public staging passed four-case generation, 64 navigation checks, Inspector and engineering showcase workflows, responsive/filter/no-JavaScript browser checks and exact 31-file publication verification. Plain `npm run build` initially refused the pre-existing `_site` as designed; that directory was preserved.
- Ruling: compare every persisted column and logical metadata across restore, and verify each physical file against its own recovery receipt. SQLite backup can alter physical bytes; identical physical SHA across different backup generations is not required by the spec.
- No child agents, parent effort-ledger edits or remote mutations. Independent whole-branch review, actual hosted CI, PR/merge and any visitor/publication route remain parent responsibilities.
