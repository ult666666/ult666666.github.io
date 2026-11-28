# Site design

How this site looks and why. Change this brief before changing the site.

## History

- **October 2026.** A dark template (near-black background, neon-lime accent, glows, glassy
  cards, mono all-caps labels and slogans as headings) was replaced with a printed-page design:
  cream paper, a book serif, italic margin notes and a long project table.
- **27 November 2026.** The printed-page version still read as generic. The cream background,
  book serif and italic labels are a common default look, and the 21-row index with three-line
  descriptions filled half of the home page. This revision keeps the structure and the plain
  voice and changes the presentation: near-white page, one sans-serif, screenshots on coloured
  mats, a one-line index and shorter copy everywhere on the home page.

## The idea

A bright, quiet page where the projects supply the colour. Dark ink on near-white, the system
sans-serif, each featured screenshot set on its own coloured mat, and an index that fits each
project on one line.

## Principles

1. **Say it plainly, and briefly.** First person, short sentences, specific nouns. One or two
   sentences per featured project and one line per index entry. No slogans, no em-dash
   flourishes, no "crafted", "seamless", "robust" or "inspectable".
2. **Show fewer things, properly.** Five projects get a screenshot. Everything is listed once in
   the index.
3. **Let the work carry the colour.** The interface is ink on near-white. Colour comes from the
   project screenshots and their mats, and from the one dark contact card.
4. **Let type do the work.** One system sans-serif; weight, size and tracking carry the
   hierarchy. Monospace is for code only.
5. **Keep motion small.** Screenshots lift a few pixels on hover. Nothing glows or animates on
   load, and `prefers-reduced-motion` turns the lift off.
6. **Keep it plain and fast.** No web fonts, no cookies, no third-party requests, and no
   JavaScript except the project explorer's search, which only filters entries already on the
   page. Every image has its intrinsic size set, so nothing jumps while loading.
7. **Be accessible by default.** WCAG AA contrast, underlined links, a visible focus ring, a skip
   link, real headings and tables, reduced motion respected, readable at 200% zoom and at 320 px.

## Tokens

### Colour (light only)

| Token | Value | Use | Contrast on `--paper` |
|---|---|---|---|
| `--paper` | `#fbfbfa` | Page background | n/a |
| `--paper-deep` | `#f1f1ee` | Code blocks, panels | n/a |
| `--surface` | `#ffffff` | Cards, inputs, walkthroughs | n/a |
| `--ink` | `#121214` | Text, headings, links | 18.1:1 |
| `--ink-2` | `#45454c` | Secondary text | 9.2:1 |
| `--muted` | `#6c6c74` | Captions, metadata, input borders | 5.0:1 |
| `--focus` | `#1f4fd1` | Link hover, focus ring | 6.5:1 |
| `--rule` | `#e6e5e1` | Hairlines (decorative) | n/a |
| `--rule-strong` | `#c9c8c2` | Stronger dividers (decorative) | n/a |

Mats behind the featured screenshots:

| Project | Mat |
|---|---|
| Frontier AI Valuation Lab | `#d9e5dc`, sage |
| crossbook | `#efe3d3`, sand |
| LineageGuard Studio | `#d8e2f0`, pale blue |
| Luma Keys | `#24223a`, night |
| MOTIONX | `#e8e1f0`, lilac |

The contact card is `--ink` with `--paper` text; its links use a lighter focus ring (`#9db3ff`)
so focus stays visible on the dark background.

### Type

- `--font`: -apple-system, BlinkMacSystemFont, Segoe UI, system-ui, Roboto, Helvetica Neue,
  Arial. SF Pro on Apple devices, Segoe UI on Windows. Nothing is downloaded.
- `--display`: the same stack, preferring the display cut where the platform has one.
- `--mono`: the system monospace font, for code and commands only.
- Body: 17 px (16.5 px under 600 px) at line height 1.6.
- Headings use weight 600 to 650 with negative tracking: the name on the home page is up to
  98 px at −0.045em, section headings 30–42 px, project names 21–25 px (the lead up to 34 px).

### Space and shape

- Page width up to 1200 px with 32 px gutters (20 px on phones).
- Selected work is a two-column grid; the lead project spans both columns. It becomes one
  column under 760 px.
- Corners: 16 px on mats and cards, 10 px on screenshots and code blocks, fully rounded buttons.
- Screenshots on mats are inset at the top and sides and run off the bottom edge, so they read
  as app windows rising out of the mat.

## Home page

1. **Header.** The name, linking home, and four links: Work, Index, About, Contact. On phones the
   links wrap under the name; there is no menu button and no script.
2. **Introduction.** The name, two sentences, an Email button, a GitHub button and the city,
   beside the Snowfall OS sample village.
3. **Selected work.** The financing model leads at full width. crossbook, LineageGuard Studio,
   Luma Keys and MOTIONX follow in two columns. Each has its screenshot on a mat, its name and
   main tools, one or two sentences and its links.
4. **Index.** All 21 projects in five groups, one line each: name, what it is, tools and links.
   The column headings are kept for screen readers and hidden visually. Under 900 px the tools
   column is dropped from the table layout; under 760 px each row becomes a short entry.
5. **About.** Two short paragraphs and links to two write-ups on how the work is checked.
6. **Contact.** One sentence with the email address, on the dark card.
7. **Footer.** Copyright, GitHub, the site source and a link back to the top.

## Copy rules

- Featured descriptions stay under about 30 words. Index lines fit on one line and end without
  a full stop.
- No lists of three where one example will do, and no colon-then-list sentence twice in a row.
- No stock phrases: "where software meets", "the parts nobody sees", "do the talking".
- Specifics over adjectives: name the reference a result is checked against.
- Say "synthetic data" once on the home page. Keep the limits on the project pages, once each.
  The trading research line says plainly that it can’t place orders.
- At most two numbers in a sentence. Test, mutant and check counts go stale; they belong in each
  project's own verification record, not on these pages.
- No slogans or two-beat taglines, no bold lead-ins, and no qualifiers such as "exactly",
  "deliberately" or "carefully" unless the exactness is the point.
- Use typographic apostrophes and quotes in prose; keep straight quotes inside code.

## Inner pages

Case studies, the engineering lab, foundations, the fintech page, the project explorer and the
404 page share the same header, footer, tokens and type. In the November 27 revision they took
on the sans-serif, ink links, rounded screenshots with soft shadows, rounded code blocks and
walkthroughs, and pill buttons. Their body copy was not rewritten in that pass.

An earlier November 2026 pass had already rewritten their body copy in a plain voice:

- **Case studies** have plain section headings, short sections, one Limits list and a closing
  "Code and docs" list of links. "Try it" sections are ordered lists. Section ids did not change.
  Heroes crop app screenshots to the working interface, as the home page does.
- **Foundations and the engineering lab** open with the page name and one sentence, without a
  numbered label above each project. Each walkthrough has two halves, "Try it" (the command and its
  expected result) and "Read the code". The commands and expected results are the ones recorded in
  [FOUNDATIONS.md](FOUNDATIONS.md) and [ENGINEERING_LAB.md](ENGINEERING_LAB.md).
- **The fintech page** keeps its worked comparison and four steps, then a plain list of code and
  docs and one Limits section.
- **The project explorer** keeps the project outcome, technology and links visible. Each technical entry has a native disclosure for its walkthrough, limits and local commands. The coursework entry is a short overview.

## What was removed on purpose

- November 27, 2026: the featured-project shortcut links under "Selected work", the visible
  index column headings, the serif type and italic labels, the cream paper colour and the
  "Portfolio" wordmark (the header now shows the name).
- The project filters, the mobile menu button and `script.js`. The index replaces the filters,
  and four links fit without a menu.
- The "how I approach a build" panel, the approach cards, the tools panel and the lime contact
  band.
- The "Smaller builds" thumbnails (they repeated the index at an unreadable size), the "last
  updated" note and the fintech page's four-area band.
- The "Fintech feature", "Engineering lab" and "Foundations" banners. Those pages are linked from
  the index rows and the selected work instead.
- The ambient gradients and glows.
- On inner pages (November 2026): the evidence-card grid and the "Read the source too" box at the
  end of each case study, the reviewer guide's step cards and implementation table, the switching
  value stat card, the numbered labels above lab projects, the "How to review the work" panels and
  the numbered proof list on the fintech page. A plain list of links replaces each of them.
