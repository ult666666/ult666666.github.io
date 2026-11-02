# The playable Blast Radius build

`projects/blast-radius-demo.html` is a single-file offline build of [Blast Radius Daily](https://github.com/ult666666/blast-radius-daily), linked from the project explorer as **Play offline demo**. It runs the real Phaser scenes and the shared deterministic engine with fictional, in-tab scores and votes. Reddit, Redis, moderation and comments are outside this build.

It works on desktop and landscape layouts, with pointer or keyboard play (Tab, the arrow keys, Space or Enter, and D to deploy) and a hidden accessible copy of the board for screen readers. That support is checked with Playwright and axe-core in Chromium, not with a physical screen reader or inside Reddit's apps.

## How the file is pinned

[`blast-demo-lock.json`](blast-demo-lock.json) records the upstream source commit, whether that checkout was clean, and the file's SHA-256 and size:

| Field | Value |
| --- | --- |
| Source commit | `9eedbd275ede53895c31b66e7a626ee80fdbb899` |
| SHA-256 | `667061938927e177673d6a93f1125a5ff415f3af0f23fb29d9362414d73c02c5` |
| Size | 2,587,824 bytes |

Rebuilding that commit in a clean clone on 2 November 2026 reproduced the vendored file byte for byte. The staging build (`scripts/build_site.py`) refuses changed bytes, a missing lock, an unknown or dirty source and mismatched source metadata before it writes any output. `tests/test_blast_demo.py` checks the embedded runtime, its connection-blocking Content Security Policy and the bundled license notices. The other portfolio pages keep their stricter rule of no scripts except the explorer's search.

The browser suite (`tests/blast_showcase.cjs`) opens the game from the explorer and plays it to the same score twice: once with the pointer and once with the keyboard alone.

## Refreshing it

1. Build a reviewed, green `main` of blast-radius-daily in a clean checkout with `npm run build:demo`.
2. Copy only `dist-demo/blast-radius-demo.html` into `projects/`.
3. Update `blast-demo-lock.json` from the build's manifest.
4. Run the full portfolio checks, including the catalog-to-game browser journey.

Do not edit the generated HTML by hand. The vendored file keeps its own BSD-3-Clause license and third-party notices, shown under its **Source and bundled licenses** control.
