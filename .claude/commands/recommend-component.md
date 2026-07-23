# Recommend the Best Component

Help identify the right UMD design system component for a given piece of content or use case.


## Setup

1. Read `registry/registry-index.json` first. Use `categories` to see what's available and `lookup_by_tag` to find which file a specific component lives in.
2. Read only the category file(s) you need (14 categories total: navigation, heroes, cards, content, feeds, carousel, accordion, alerts, brand, layout, person, quote, slider, social).
3. Do not suggest components that are not in the registry.

## Process

1. **Understand the content** — ask (or infer from context) what the content is and what job it needs to do:
   - What *type* of content is it? (headline + image, stats, quote, navigation, cards, hero, form, etc.)
   - What is its *purpose* on the page? (capture attention, orient the user, showcase data, provide navigation, feature a story, etc.)
   - Where does it appear? (top of page, mid-page section, sidebar, full-width band, etc.)
   - Are there constraints? (must have image, needs a CTA, has a lot of text, etc.)

   **If the content type is genuinely ambiguous** (e.g. a number that could be a stat or body copy; a short passage that could be a quote or a callout; links that could be navigation or CTAs), ask 1–2 targeted clarifying questions before recommending — a confident recommendation for the wrong content type is worse than a question.

2. **Match to registry** — scan the registry for candidates and narrow to 1–3 best options.

3. **Recommend** — for each candidate:
   - Component tag name
   - Why it fits this content
   - Any variants or attributes to use (`data-display`, `data-theme`, etc.)
   - Any gotchas or rules that apply (reference the relevant RULES.md section)
   - A minimal working code example with realistic placeholder content

4. **Distinguish close alternatives** — if two components are similar (e.g. `umd-element-hero` vs `umd-element-hero-minimal`, or `umd-element-pathway` overlay vs standard), explain the tradeoff clearly so the user can choose.

## Component cheat-sheet (quick reference)

**This table is the single source for content-type → component matching** — `/recreate-page`, `/build-landing-page`, `/build-interior-page`, and `/plan-page` all reference it; do not maintain parallel copies elsewhere. It is hand-maintained and can drift from the registry as the DS submodule updates: **before quoting any row, verify the tag and attributes against the `registry/` file** — the registry wins on conflict, and a stale row should be fixed here when caught.

| Content type | First component to consider |
|---|---|
| Top-of-page hero (site home page) | `umd-element-hero data-display="standard"` — full-height; centered text by default (RULES.md §22). `data-display="overlay"` is an explicit design choice, not the photo default |
| Top-of-page hero (any other landing) | `umd-element-hero data-display="standard" data-layout-height="small" data-layout-text="center"` — small + centered is the default for non-home landings (RULES.md §22). Pull body copy + multi-CTA rows into a section-intro below |
| Top-of-page hero (interior page) | `umd-element-hero data-display="standard" data-layout-height="small"` with image, or `umd-element-hero-minimal` when no image (RULES.md §21) |
| Page title / section header bar | `umd-element-hero-minimal` |
| Split image + text feature | `umd-element-pathway` (`data-display="overlay"` for emphasized/standalone content, standard for typical use) |
| Stats / metrics | `umd-element-stat` with grid wrapper — or stacked large stats (`data-decoration-line="true" data-visual-size="large"` in `umd-layout-grid-gap-stacked`) in a `umd-element-sticky-columns` static column when a text introduction is needed |
| Featured event + upcoming list | `umd-element-sticky-columns`: sticky column = `umd-element-event display="promo"`, static column = `umd-layout-grid-gap-stacked` of `umd-element-event data-display="list"`. See LAYOUT-PATTERNS.md "Events Section" |
| One featured item + many secondary items | `umd-element-sticky-columns` — general pattern for any "one editorial pick + list" layout (events, news, research). Sticky = featured; static = list |
| News/story cards | `umd-element-card` (standard) or `umd-element-card-overlay` (type="image" for photo bg) |
| Card carousel with no real images | `umd-element-card-overlay data-theme="dark"` (color version — no `type="image"`) inside `umd-element-carousel-cards`; never standard cards with placeholder images |
| Grid of image-overlay feature cards | `umd-element-card-overlay type="image"` in `umd-layout-grid-columns-*` (no-gap mosaic) or `umd-layout-grid-gap-*` (separated); add `class="size-large"` when cards are the section's primary visual. See `LAYOUT-PATTERNS.md` "Overlay-Card Grids" |
| Section heading + CTA | `umd-element-section-intro` (centered) or `umd-element-section-intro-wide` — watermark on at most one featured section per page (see `/evaluate-design`) |
| Pull quote / testimonial | `umd-element-quote` wrapped in `umd-layout-space-horizontal-normal`; `data-display="featured"` for large format |
| Quote + editorial body copy | `umd-element-pathway-highlight` — only when real body copy exists alongside the quote; quote-only → use `umd-element-quote` |
| Full-bleed image scroll effect | `umd-layout-image-expand` |
| Row of 2–4 standalone navigation links | `umd-element-card-overlay` (no image, `slot="cta-icon"`) in a grid — NOT secondary CTAs |
| FAQ / expandable content | `umd-element-accordion-item` |
| Person profile | `umd-element-person-bio`. **Do NOT use inside `umd-element-carousel-thumbnail`** — that carousel only takes `umd-element-card` slides (RULES.md §27) |
| Icon + text card | `umd-element-card-icon` |
| Video card | `umd-element-card-video` or `umd-element-hero-brand-video` |
| Grid logo/brand hero | `umd-element-hero-grid` or `umd-element-hero-logo` |
| Top-level navigation | `umd-element-navigation-header` + `umd-element-nav-item` |

## Output format

Lead with the **primary recommendation** and a one-line rationale. Then show the code example. If there are strong alternatives, list them after with a brief "vs" comparison. Keep it concise — the user can ask to go deeper on any option.
