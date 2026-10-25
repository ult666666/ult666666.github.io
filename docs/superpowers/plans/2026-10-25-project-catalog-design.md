# Project catalog design

The profile and portfolio have grown to 19 public project repositories. Selected work, foundations and the engineering lab have useful detail, but readers cannot search across the whole collection or quickly distinguish a browser demo from a local library, research snapshot or coursework.

Build a static project explorer at `/projects/catalog.html`. All projects render into HTML at build time, with a concrete scenario, implementation review route and scope statement. JavaScript progressively adds text search and area selection; the page remains useful without it. Search combines whitespace-separated terms with AND, across name, area, stack and explanatory text. Search and area compose; reset restores all projects and zero results has a clear message. No external service, analytics, account or new runtime dependency.

Keep the current visual system, responsive layout, keyboard access and reduced-motion support. Preserve all existing case studies, education wording and Claude's remote changes. Show no invented employment, customer use, duration, adoption or deployment claims. Public inventory contains only public repositories; private repository names never enter it.

The root profile will show six selected projects and compact specialty routes, followed by an expandable complete inventory. A catalog link connects the profile and homepage to deeper review. Three independent repository audits will choose bounded runnable workflow improvements separately, with their own source and verification records.

The catalog source lives in `docs/project-catalog.json`, not in the public payload. A standard-library generator validates it, escapes text and restricts URLs before writing HTML. `--check` fails when the generated page differs. Add only the generated page, CSS and JS to the reviewed public allowlist.
