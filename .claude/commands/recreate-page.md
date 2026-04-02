# Recreate this page

Build a complete UMD landing page HTML file based on an existing page and save it to `/Users/zjocson/repos/design-system-page-builder/examples/`. Help identify the right UMD design system component for all components on a given piece of content or use case.



## Setup

1. Read `/Users/zjocson/repos/design-system-page-builder/TEMPLATE.html` — use its full `<head>` block (critical CSS + cdn.js script) verbatim. Do not rebuild it.
2. Read `/Users/zjocson/repos/design-system-page-builder/registry/registry-index.json` to see available categories and which components are in each.
3. Based on the content types on the page, read only the relevant category file(s):
   - Navigation/headers/footer → `/Users/zjocson/repos/design-system-page-builder/registry/registry-navigation.json`
   - Heroes → `/Users/zjocson/repos/design-system-page-builder/registry/registry-heroes.json`
   - Cards and feeds → `/Users/zjocson/repos/design-system-page-builder/registry/registry-cards.json`
   - Pathways, section intros, image expand, sticky columns → `/Users/zjocson/repos/design-system-page-builder/registry/registry-content.json`
3. If the content type of a component is unclear, read all four files. Do not suggest components not in the registry. If there is no equivalent, skip the content but message the user that there was no match for a piece of content.
4. Follow every rule in `/Users/zjocson/repos/design-system-page-builder/RULES.md` exactly.

## Page identity

Use content and images from the URL provided in the command as the fictional client. Shorten the page title used in the command and name the output file `examples/{title}.html`.

**Images:** Fetch the URL and extract actual `src` attribute values from the page's HTML — do not guess or construct image URLs. Use the exact URLs found in the source.


## Process

1. **Understand the content** — ask (or infer from context) what the content is for each component on the page and what job it needs to do:
   - What *type* of content is it? (headline + image, stats, quote, navigation, cards, hero, etc.)
   - What is its *purpose* on the page? (capture attention, orient the user, showcase data, provide navigation, feature a story, etc.)
   - Where does it appear? (top of page, mid-page section, sidebar, full-width band, etc.)
   - Are there constraints? (must have image, needs a CTA, has a lot of text, etc.)

2. **Match to registry** — scan the registry for candidates and narrow to the best option.

3. **Recommend** — for each component:
   - Component tag name
   - Why it fits this content
   - Any variants or attributes to use (`data-display`, `data-theme`, etc.)
   - Any gotchas or rules that apply (reference the relevant RULES.md section)
   - A minimal working code example with realistic placeholder content

4. **Distinguish close alternatives** — if two components are similar (e.g. `umd-element-hero` vs `umd-element-hero-minimal`, or `umd-element-pathway` overlay vs standard), explain the tradeoff clearly so the user can choose.

## Component cheat-sheet (quick reference)

| Content type | First component to consider |
|---|---|
| Top-of-page hero with image | `umd-element-hero` (`data-display="overlay"` for photo, `data-display="stacked"` for clean) |
| Page title / section header bar | `umd-element-hero-minimal` |
| Split image + text feature | `umd-element-pathway` (`data-display="overlay"` for emphasized content, standard for typical use) |
| Stats / metrics | `umd-element-stat` with grid wrapper or `umd-element-stat` in a `sticky-column` when a text introduction is needed |
| News/story cards | `umd-element-card` (standard) or `umd-element-card-overlay` (type="image" for photo bg) |
| Section heading + CTA | `umd-element-section-intro` (centered) or `umd-element-section-intro-wide` (with watermark) |
| Pull quote / testimonial | `umd-element-quote` (standard) or `data-display="featured"` for a quote that stands out |
| Full-bleed image scroll effect | `umd-layout-image-expand` for high visual |
| FAQ / expandable content | `umd-element-accordion-item` |
| Person profile | `umd-element-person-bio` |
| Icon + text card | `umd-element-card-icon` |
| Video card | `umd-element-card-video` |
| Grid of logo | `umd-element-hero-grid` |
| Top-level navigation | `umd-element-navigation-header` + `umd-element-nav-item` |


## Spacing and layout

- Every top-level `<section>` gets `class="umd-layout-vertical-landing"`.
- Pathway and hero are full-bleed — do NOT wrap in a horizontal spacing class.
- Card grids and section intros go inside a `umd-layout-space-horizontal-larger` wrapper.
- `umd-element-quote` uses `umd-layout-space-horizontal-normal` (1280px) — not `larger` (RULES.md §12).
- `data-theme` does not cascade — set it on every child component that needs it (RULES.md §14).
- `umd-element-pathway-highlight` requires real body copy in `slot="text"`. If the source has only a quote and attribution, use `umd-element-quote` instead (RULES.md §5).

## Image fallback

Always use real image URLs extracted from the source page. Only fall back to local images if a URL is confirmed broken — do not replace a working image.

To verify: attempt to fetch the image URL. If it returns a non-200 status (401, 403, 404, etc.) or fails to load, it is broken. If it returns image content, use it as-is regardless of the CDN or domain.

When a URL is confirmed unavailable (hotlink protection, 401/403, dynamically loaded content, no source image):
1. Read `/Users/zjocson/repos/design-system-page-builder/images/images-index.json`
2. Determine the size tier: **large** for heroes, pathways, image-expand — **small** for cards
3. Match the content context to the closest tag (`campus`, `people`, `events`, `research`)
4. If no tag match, collect all entries with `"default": true` in the correct tier and pick one at random
5. Reference the image as a repo-relative path: `../images/large/campus/filename.jpg`

## Output

Write the completed HTML file to `/Users/zjocson/repos/design-system-page-builder/examples/{title}.html`. Confirm the filename when done.