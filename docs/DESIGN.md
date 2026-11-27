# Site design

How this site looks and why. The redesign of October 2026 replaced a dark template-style
layout with a quieter, printed-page design. This file is the brief that implementation
follows; change the brief before changing the site.

## What was wrong with the old design

A reviewer said the site "looks like AI". The reasons:

1. **Template palette.** Near-black background, neon-lime accent, glows and glassy cards.
2. **Template type.** Heavy, tightly tracked display headlines over small all-caps mono labels
   ("01 / SELECTED WORK") on every section.
3. **Slogans instead of headings.** "Built, not just imagined." "Thoughtful by design."
   "Systems that earn trust." Each ended in a lime full stop.
4. **Everything was a card.** Bordered, rounded boxes, tag pills and a ↗ on every link.
5. **Stock sections.** A three-step "approach" with icons, a tools panel, a "Have a problem worth
   solving?" call-to-action band.
6. **Volume over choice.** Fifteen project blocks, three banners and four "specialty" pills on one
   page, about 8,900 px tall on a laptop and 15,200 px on a phone.
7. **The same disclaimer everywhere.** Honest, but repeated on almost every card.

## The idea

A personal site that reads like a well-kept notebook. One person introduces themselves
plainly, shows a few projects properly, with figures and captions, and keeps an index of
everything else. Paper-coloured background, dark ink, one blue for links, a book serif and
a page grid with notes in the margin.

## Principles

1. **Say it plainly.** Headings describe; they don't sell. First person, short sentences,
   specific nouns. No em-dash flourishes, no "considered", "crafted", "seamless", "robust" or
   "inspectable".
2. **Show fewer things, properly.** One lead project and four more get a real screenshot and a
   short paragraph each. Everything is listed once in the index.
3. **Let type do the work.** Serif for headings and reading, system sans-serif for homepage navigation and labels, monospace for code.
   Weight, size and italics carry the hierarchy; colour doesn't.
4. **Use one accent, for links only.** Blue ink. Nothing glows, lifts or animates on hover
   beyond a colour change.
5. **Keep process notes together.** The source repository records AI assistance. Each technical case explains the limits of its data and examples.
6. **Keep it plain and fast.** No web fonts, no cookies, no third-party requests, and no
   JavaScript except the project explorer's search, which only filters entries already on the
   page. Every image has its intrinsic size set, so nothing jumps while loading.
7. **Be accessible by default.** WCAG AA contrast, visible focus, a skip link, real headings and
   tables, reduced motion respected, readable at 200% zoom and at 320 px.

## Tokens

### Colour (light only)

| Token | Value | Use | Contrast on `--paper` |
|---|---|---|---|
| `--paper` | `#f6f3ec` | Page background | n/a |
| `--paper-deep` | `#ece7dc` | Figure mats, code, table group rows | n/a |
| `--ink` | `#1d1b17` | Text, headings | 15.5:1 |
| `--ink-2` | `#46423b` | Secondary text | 9.0:1 |
| `--muted` | `#6b665c` | Captions, metadata | 5.2:1 (4.6:1 on `--paper-deep`) |
| `--link` | `#2343b5` | Links, focus ring | 7.5:1 |
| `--link-hover` | `#152c86` | Hovered links | 10.9:1 |
| `--rule` | `#d6cfc1` | Hairlines (decorative) | n/a |
| `--rule-strong` | `#a89f8f` | Table and figure borders (decorative) | n/a |

The site is light-only. A dark theme would need every inner-page component
re-checked; it can come later as its own change.

### Type

- `--serif`: Charter, Bitstream Charter, Sitka Text, Cambria, Georgia, serif. Charter ships
  with macOS and iOS; Windows falls back to Sitka Text or Cambria. Nothing is downloaded.
- `--sans`: system sans-serif for the homepage’s small labels. The long-form case studies retain their serif navigation.
- `--mono`: the system monospace font, for code and commands only.
- Body: 18 px (17 px under 600 px) at line height 1.6. Reading measure about 66 characters.
- Scale: opening sentence 44 px, lede 23 px, section labels 27 px, lead project 25 px, other
  projects 22 px. Headings use regular or bold weight and normal tracking; margin notes are italic.

### Space and grid

- Page width up to 1180 px with 32 px gutters (20 px on phones).
- Desktop grid: a 200 px margin column for section labels and notes, then the main column.
  Under 900 px the margin column stacks above its section.
- Vertical rhythm in multiples of 8 px. Sections are separated by a hairline and 96 px of space
  (64 px on phones).
- Corners: 2 px on images, nothing else rounded.

## Home page

1. **Header.** The name, linking home, and four links: Work, Index, About, Contact. On phones the
   links wrap under the name; there is no menu button and no script.
2. **Introduction.** Charles’s name and a short introduction sit beside the Snowfall OS
   sample village. Its caption describes what opening a cottage does.
3. **Selected work.** The financing model leads the gallery. Four more projects follow in
   two columns, with screenshots of the actual tools. The gallery stacks on a phone.
4. **Index.** The table contains 21 projects, grouped by subject. Each row gives an outcome,
   the tools used and a way to explore it. The coursework row links to a short overview.
5. **About.** What I test against, with two concrete examples (Hull's worked option price,
   repeated testing in powerlift), and two links to the evidence behind the projects.
6. **Contact.** One sentence with the email address and GitHub.
7. **Footer.** Copyright, the site source and a link back to the top.

## Copy rules

- No lists of three where one example will do, and no colon-then-list sentence twice in a row.
- No stock phrases: "where software meets", "the parts nobody sees", "do the talking".
- Specifics over adjectives: name the reference a result is checked against.
- Say "synthetic data" once on the home page. Keep the limits on the project pages, once each.
- At most two numbers in a sentence, and one or two memorable numbers per section. Test, mutant and
  check counts go stale; they belong in each project's own verification record, not on these pages.
- No slogans or two-beat taglines, no bold lead-ins on paragraphs or list items, and no qualifiers
  such as "exactly", "deliberately" or "carefully" unless the exactness is the point.
- Use typographic apostrophes and quotes in prose; keep straight quotes inside code.

## Inner pages

Case studies, the engineering lab, foundations, the fintech page, the project explorer and the
404 page share the same header, footer, palette and type. Footers link to the site source.

A November 2026 pass rewrote their body copy in the same plain voice as the home page:

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

- The project filters, the mobile menu button and `script.js`. The index replaces the filters,
  and four links fit without a menu.
- The "how I approach a build" panel, the approach cards, the tools panel and the lime contact
  band.
- The "Smaller builds" thumbnails (they repeated the index at an unreadable size), the figure
  captions, the "last updated" note and the fintech page's four-area band.
- The "Fintech feature", "Engineering lab" and "Foundations" banners. Those pages are linked from
  the index rows and the selected work instead.
- The ambient gradients, glows and hover lifts.
- On inner pages (November 2026): the evidence-card grid and the "Read the source too" box at the
  end of each case study, the reviewer guide's step cards and implementation table, the switching
  value stat card, the numbered labels above lab projects, the "How to review the work" panels and
  the numbered proof list on the fintech page. A plain list of links replaces each of them.
