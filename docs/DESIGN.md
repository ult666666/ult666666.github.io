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
plainly, shows four projects properly, with figures and captions, and keeps an honest index
of everything else. Paper-coloured background, dark ink, one blue for links, a book serif and
a page grid with notes in the margin.

## Principles

1. **Say it plainly.** Headings describe; they don't sell. First person, short sentences,
   specific nouns. No em-dash flourishes, no "considered", "crafted", "seamless", "robust" or
   "inspectable".
2. **Show fewer things, properly.** One lead project and three more get a real screenshot and a
   short paragraph each. Everything is listed once in the index.
3. **Let type do the work.** One serif family for everything, with monospace only for code.
   Weight, size and italics carry the hierarchy; colour doesn't.
4. **Use one accent, for links only.** Blue ink. Nothing glows, lifts or animates on hover
   beyond a colour change.
5. **Say it honestly, once.** AI assistance and synthetic data are stated once in the index
   note, and each project page keeps its own scope section.
6. **Keep it plain and fast.** No web fonts, no cookies, no third-party requests, and no
   JavaScript except the project explorer's search, which only filters entries already on the
   page. Every image has its intrinsic size set, so nothing jumps while loading.
7. **Be accessible by default.** WCAG AA contrast, visible focus, a skip link, real headings and
   tables, reduced motion respected, readable at 200% zoom and at 320 px.

## Tokens

### Colour (light only)

| Token | Value | Use | Contrast on `--paper` |
|---|---|---|---|
| `--paper` | `#f6f3ec` | Page background | — |
| `--paper-deep` | `#ece7dc` | Figure mats, code, table group rows | — |
| `--ink` | `#1d1b17` | Text, headings | 15.5:1 |
| `--ink-2` | `#46423b` | Secondary text | 9.0:1 |
| `--muted` | `#6b665c` | Captions, metadata | 5.2:1 (4.6:1 on `--paper-deep`) |
| `--link` | `#2343b5` | Links, focus ring | 7.5:1 |
| `--link-hover` | `#152c86` | Hovered links | 10.9:1 |
| `--rule` | `#d6cfc1` | Hairlines (decorative) | — |
| `--rule-strong` | `#a89f8f` | Table and figure borders (decorative) | — |

The site is deliberately light-only. A dark theme would need every inner-page component
re-checked; it can come later as its own change.

### Type

- `--serif`: Charter, Bitstream Charter, Sitka Text, Cambria, Georgia, serif. Charter ships
  with macOS and iOS; Windows falls back to Sitka Text or Cambria. Nothing is downloaded.
- `--sans`: kept as a name for small UI text, but it points at `--serif`. A serif body with a
  system-sans UI is the default "tasteful" pairing; one family reads as a choice.
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
2. **Introduction.** One sentence as the page heading ("I'm Charles Dai. I build software where
   the numbers have to be right."), a paragraph about school and MOTIONX, one line about the
   internships I want, and plain links to email and GitHub.
3. **Selected work.** Frontier AI Valuation Lab leads with a wide screenshot. LineageGuard Studio,
   Luma Keys and MOTIONX follow as rows of image and text. Screenshots are cropped to the working
   interface, never to an app's own headline. No figure captions: nothing refers to them.
4. **Index.** One table of 17 published projects, grouped into finance, data, AI and backend, and
   product and design. Coursework and tiny tools stay on GitHub. Links use one vocabulary
   (Live, Case study or Notes, Code) in one order, in a quieter colour than body links. The
   margin note says once that the projects were built with AI coding assistants and that hosted
   demos run on synthetic data.
5. **About.** What I test against, with two concrete examples (Hull's worked option price,
   Jennison and Turnbull's tables), and two links for reading instead of clicking.
6. **Contact.** One sentence with the email address and GitHub.
7. **Footer.** Copyright, "no cookies or tracking", the site's source and a link back to the top.

## Copy rules

- No lists of three where one example will do, and no colon-then-list sentence twice in a row.
- No stock phrases: "where software meets", "the parts nobody sees", "do the talking".
- Specifics over adjectives: name the reference a result is checked against.
- Say "synthetic data" once on the home page. Keep the honest limits on the project pages.

## Inner pages

Case studies, the engineering lab, foundations and the fintech page share the same header,
footer, palette and type. Their headings lose the coloured full stops and all-caps mono
eyebrows, their tag pills become a dotted list, and their opening lines are rewritten in the same
plain voice. Case-study heroes align with the article column. The lab pages lose their two-beat
taglines and arrow triplets, and their project index becomes a plain contents list. The rest of
their body copy is unchanged in this pass and still carries some of the old voice.

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
