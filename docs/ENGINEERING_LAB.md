# Engineering lab review route

The engineering lab adds complementary public source projects to the existing portfolio:

- RelayBox: durable signed webhook ingestion, transactional claims and stale-worker fencing.
- TraceBench: deterministic offline checks of recorded AI outputs and compatible baseline comparison.
- Impact Ledger: nonprofit operations reporting with separate session and attendance records.

These are independent, AI-assisted educational projects. Data is synthetic. The Impact Ledger hosted preview uses a bundled snapshot, while its local Python API supports persistent imports. Each repository documents its own supported interfaces and deployment limits. The lab does not claim external adoption, production operation, or professional engagements.

## Runnable reviewer walkthroughs

Each project now has a native HTML disclosure with a reproducible test command,
its expected behavior, direct implementation and test links, and the boundary of
the guarantee. RelayBox demonstrates stale-token rejection after reclamation;
TraceBench distinguishes a regression from an improvement; Impact Ledger checks
the grain of people, attendance and spending. These routes refer to actual
repository tests and work without JavaScript.

The browser suite opens every disclosure by keyboard with JavaScript both enabled
and disabled, checks the visible commands and proving-test links, and measures all
three open disclosures at 360, 768 and 1440 pixels. Long commands wrap instead of
creating a horizontal scrollbar. No new visitor assets or publication roots are
needed.

The accompanying [lease-clock engineering note](notes/lease-clock.md) explains an
actual review finding, the transaction-order correction, and the three focused
commands that reproduce its evidence. Its timestamps are a synthetic logical
example, not a production incident or performance measurement.

## Publication

`projects/engineering-lab.html` is an explicitly reviewed entry in `public-files.json`. It uses the existing stylesheet and progressively enhanced navigation. The homepage entry and sitemap make it discoverable without changing the original eight project cards or their filters. Public staging still refuses unlisted files and verifies every released byte. Local résumés informed topic selection but are not source assets or part of the publication inventory.

## Verification

On 23 October 2026, Python 3.15.0 / Node 24.18.0 / Playwright 1.61.1:

```sh
python3 -B -m unittest discover -s tests -v
npm ci --ignore-scripts --no-audit --no-fund
npx playwright install chromium
npm run build
PORTFOLIO_TEST_ROOT=_site npm run test:browser
python3 -B scripts/build_site.py --verify _site
```

The local structural suite passed 49 tests. Browser checks covered the original journeys, the lab's source and verification links, homepage discovery, 360/768/1440 widths, navigation with JavaScript disabled, and screenshots inspected at desktop and mobile sizes. `tests/engineering_showcase.cjs` is integrated into the existing browser command. Staged deployment semantic checks also require the three source and verification routes.

These checks establish page behavior and publication consistency. They do not verify the correctness of all linked project code; each project's own verification record carries that scope. Hosted URLs are checked separately during shipping.
