# Build a Sample Interior Page

Build a complete UMD interior/subpage HTML file and save it to `/test/` in the main repo.

## Setup

1. Read `TEMPLATE.html` — use its full `<head>` block (critical CSS + cdn.js script) verbatim.
2. Read `umd-component-registry.json` — source of truth for all slots and attributes.
3. Follow every rule in `RULES.md` exactly.

## Page identity

Use a **subpage of a University of Maryland college or department** — not a homepage. Good examples:
- Graduate Admissions (e.g. `test/clark-graduate-admissions.html`)
- Research Areas (e.g. `test/arhu-research.html`)
- About the Department (e.g. `test/bsos-about.html`)
- Faculty & Staff (e.g. `test/sphl-faculty.html`)
- News & Events (e.g. `test/smith-news.html`)

Pick a college and subpage type that haven't been used recently. Name the file `test/{dept}-{subpage}.html`.

## Required sections — use this order

1. **Utility header** — `<umd-element-utility-header>` (hardcoded)
2. **Navigation header** — `<umd-element-navigation-header sticky class="umd-layout-space-horizontal-full">` with logo + 4–5 nav items. Mark the current section active if the component supports it.
3. **Hero minimal** — `umd-element-hero-minimal`. Use `data-theme="maryland"` for a red branded header or `data-theme="dark"` for a photography-backed variant. Include headline and subhead text that orient the user to what this subpage is about.
4. **Intro text block** — `<section class="umd-layout-vertical-interior">` with `umd-layout-space-horizontal-normal` wrapper. Use `umd-element-section-intro` (centered variant — no horizontal wrapper needed on the component itself) for a brief section overview.
5. **Pathway highlight** — `umd-element-pathway-highlight` (if available in registry). If not, use `umd-element-pathway data-display="overlay" data-theme="dark"` for a featured callout. Tie this to the page topic.
6. **Content cards** — `<section class="umd-layout-vertical-interior">` with `umd-layout-space-horizontal-normal` wrapper. A 3-column grid of `umd-element-card` relevant to the page topic (programs, research areas, news stories, faculty spotlights, etc.). Each card: headline (linked), image, short description.
7. **Quote** — `<section class="umd-layout-vertical-interior">` with `umd-layout-space-horizontal-small` wrapper. A single `umd-element-quote` (standard, no `data-display="featured"`). Attribution should be a student, faculty, or alumni name + title.
8. **Accordion FAQ** — `<section class="umd-layout-vertical-interior">` with `umd-layout-space-horizontal-normal` wrapper. A `umd-element-section-intro` intro + 4–5 `umd-element-accordion-item` elements with realistic Q&A relevant to the page (admissions questions, program details, research FAQs, etc.).
9. **Footer** — `<umd-element-footer>` with department contact info.

## Content guidelines

- Write real-sounding copy throughout. No lorem ipsum.
- Image slots: use `https://picsum.photos/seed/{slug}/{w}/{h}` for placeholder images.
- CTA links: realistic relative URLs for the department (`/apply`, `/research/projects`, `/faculty`, etc.).
- Do not invent eyebrow slots (RULES.md §13).
- Accordion items: questions should be specific and useful (e.g. "What GRE scores are required?" not "What is the program?").

## Spacing and layout

- Every top-level `<section>` gets `class="umd-layout-vertical-interior"` (not landing).
- `umd-layout-space-horizontal-normal` (1280px) is the standard interior page width.
- `umd-layout-space-horizontal-small` (992px) for narrow content like quotes.
- `umd-layout-space-horizontal-smallest` (800px) for article body text if used.
- Hero-minimal and pathway are full-bleed — do NOT wrap in a horizontal spacing class.
- `data-theme` does not cascade — set it individually on child components (RULES.md §14).

## Output

Write the completed HTML file to `/test/{dept}-{subpage}.html`. Confirm the filename when done.
