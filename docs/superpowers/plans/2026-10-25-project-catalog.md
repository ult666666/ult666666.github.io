# Project Explorer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Make all 19 public projects navigable through concrete scenarios and inspectable implementation routes.

**Architecture:** Generate static HTML from a reviewed JSON inventory. Add client-side filtering to the already-rendered cards; keep all content available without JavaScript. Integrate generation checking with the existing public-only build.

**Tech Stack:** Python standard library, HTML/CSS, browser JavaScript, existing Playwright.

**Spec:** `docs/superpowers/plans/2026-10-25-project-catalog-design.md`

## Global Constraints

- No external service, analytics, account or new runtime dependency.
- Preserve all existing case studies, education wording and Claude's remote changes.
- Show no invented employment, customer use, duration, adoption or deployment claims.
- Public inventory contains only public repositories; private repository names never enter it.
- Add only the generated page, CSS and JS to the reviewed public allowlist.

## Review Focus

- HTML-like project text must render as text; links must use allowed HTTPS or local routes.
- Empty or multiword searches and an area filter must compose without hiding unrelated reset results.
- No JavaScript must leave all project explanations and links accessible.
- A stale generated page must fail CI instead of silently shipping old data.
- Narrow screens, keyboard focus and no-result feedback must remain usable.

### Task 1: Generated, validated project inventory

**Files:** Create `docs/project-catalog.json`, `scripts/build_catalog.py`, `projects/catalog.html`, `tests/test_catalog.py`.

**Interfaces:** `render(catalog: dict) -> str`; `validate(catalog: dict) -> None`; CLI `--check` compares current generated HTML.

- [x] Write tests exercising rendering of literal hostile text, duplicate/invalid IDs, unsafe links and stale output.
- [x] Run `python3 -B -m unittest discover -s tests -p test_catalog.py -v`; observe missing-generator failures.
- [x] Implement schema validation, escaped static rendering and deterministic check/write CLI; add the reviewed inventory.
- [x] Run the same tests; expect all pass.

### Task 2: Progressive project search and publication wiring

**Files:** Create `project-catalog.css`, `project-catalog.js`, `tests/catalog_showcase.cjs`; modify `tests/browser_smoke.cjs`, `package.json`, `scripts/build_site.py`, `public-files.json`, `index.html`, `sitemap.xml`, `README.md`.

**Interfaces:** Existing smoke suite calls `catalog_showcase(browser, base)`; controls filter rendered `.catalog-card` elements, update a polite result count, and reset both inputs.

- [x] Add real Chromium scenarios for combined search/area, case/whitespace normalization, no results, reset, no-JS, keyboard and 320px layout; observe search missing before implementation.
- [x] Implement styles and local filtering without fetch or dynamic HTML injection. Wire generator `--check` before site staging.
- [x] Run Python suite, fresh staged build and complete browser suite; expect passing results and unchanged existing routes.
- [x] Review rendered desktop/mobile captures and stage allowlist before committing.

### Task 3: Profile and publication

**Files:** Modify profile repository `README.md`; save verification and summary under task `outputs/`.

- [x] Condense the latest profile into six selected projects, specialty navigation and an expandable complete catalog, preserving all 19 current projects and current education.
- [x] Review both diffs and current remote heads; rebase if concurrent changes appear.
- [ ] Commit and open scoped PRs; attach both PRs, verify hosted checks and merge reviewed heads within user's shipping authorization.
- [ ] Verify public catalog and profile, save receipts and source checkpoint.
