# Recreate this page / convert this page to the design system

Build a complete UMD landing page HTML file based on an existing page and save it to `/Users/zjocson/repos/design-system-page-builder/examples/`. Help identify the right UMD design system component for all components on a given piece of content or use case.



## Required page structure

Every page must open with these three elements, in this order, before any content:

1. **Global university header** — `<umd-element-navigation-utility data-alert-off="true" role="navigation" aria-label="Utility navigation"></umd-element-navigation-utility>` (hardcoded, no config, never omit — this is the UMD-wide bar from umd.edu)
2. **Site utility header** — `<umd-element-utility-header></umd-element-utility-header>` (hardcoded, no config)
3. **Site navigation header** — `<umd-element-navigation-header sticky class="umd-layout-space-horizontal-full">` with logo and nav items from the source page

## Step 1: Download source assets (subagent)

Before doing any analysis or building, spawn a subagent to download the source page assets into `/Users/zjocson/repos/design-system-page-builder/tmp/`. The subagent should:

1. Create the directory `/Users/zjocson/repos/design-system-page-builder/tmp/` if it does not exist.
2. Download the full HTML of the source URL and save it as `tmp/source.html`.
3. Parse `tmp/source.html` and download all referenced assets:
   - Images (`<img src>`, `srcset`, CSS `background-image` URLs, `<picture><source srcset>`)
   - Videos (`<video src>`, `<source src>`)
   - Linked CSS files (`<link rel="stylesheet" href>`)
   - Inline and linked JavaScript files (`<script src>`)
4. Save each asset into a mirrored subdirectory under `tmp/` (e.g. `tmp/assets/images/`, `tmp/assets/css/`, `tmp/assets/js/`, `tmp/assets/video/`).
5. Use `curl` or `wget` for downloads. Skip assets that return non-200 status — log skipped URLs to `tmp/skipped-assets.txt`.
6. Return a summary of what was downloaded.

Wait for the subagent to complete before proceeding.

## Step 2: Setup

1. Read `TEMPLATE.html` — use its full `<head>` block (critical CSS + cdn.js script) verbatim. Do not rebuild it. The CSS comes from `styles/critical.css` (single source of truth for all CSS rules).
2. Read `registry/registry-index.json` for the category map and `lookup_by_tag`. Load only the specific category files you need for the content types on this page. Do not suggest components that are not in the registry — if no equivalent exists, skip that content and tell the user.
3. Read `LAYOUT-PATTERNS.md` for HTML patterns when using rich text sections, dark backgrounds, two-column grids, or inline CTA rows.
4. **Read `tmp/source.html`** to understand the page structure, content, and asset references. Use the downloaded files in `tmp/` as the authoritative source — do not re-fetch the live URL.
5. Follow every rule in `RULES.md` exactly.

## Page identity

Use content and images from the source page as the fictional client. Shorten the page title used in the command and name the output file `examples/{title}.html`.

**Images:** Extract actual image paths from `tmp/source.html` — do not guess or construct URLs. For the generated page, copy the downloaded images from `tmp/assets/images/` into `/Users/zjocson/repos/design-system-page-builder/images/projects/{title}/` (where `{title}` matches the output filename, e.g. `images/projects/ischool/`) and reference them as repo-relative paths: `../images/projects/{title}/filename.jpg`. Videos go into `images/media/`.


## Process

1. **Understand the content** — read `tmp/source.html` and the downloaded assets to understand what each component on the page does:
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
| Top-of-page hero with image (landing page) | `umd-element-hero` (no `data-display` for standard background image; `data-display="overlay"` only for an explicit color-panel overlay effect) |
| Top-of-page hero with image (interior page) | `umd-element-hero data-layout-height="small"` — **always use the small height on interior pages** (RULES.md §21) |
| Page title / section header bar | `umd-element-hero-minimal` |
| Split image + text feature | `umd-element-pathway` (`data-display="overlay"` for emphasized content, standard for typical use) |
| Stats / metrics | `umd-element-stat` with grid wrapper or `umd-element-stat` in a `sticky-column` when a text introduction is needed |
| Featured event + upcoming list | `umd-element-sticky-columns`: sticky column = `umd-element-event display="promo"`, static column = `umd-layout-grid-gap-stacked` of `umd-element-event data-display="list"`. See LAYOUT-PATTERNS.md "Events Section". |
| One featured item + many secondary items | `umd-element-sticky-columns` — general pattern for any "one editorial pick + list" layout (events, news, research). Sticky = featured; static = list. |
| News/story cards | `umd-element-card` (standard) or `umd-element-card-overlay` (type="image" for photo bg) |
| Section heading + CTA | `umd-element-section-intro` (centered) or `umd-element-section-intro-wide` (with watermark) |
| Pull quote / testimonial | `umd-element-quote` (standard) or `data-display="featured"` for a quote that stands out |
| Full-bleed image scroll effect | `umd-layout-image-expand` for high visual |
| Row of 2–4 standalone navigation links | `umd-element-card-overlay` (no image, `slot="cta-icon"`) in a grid — NOT secondary CTAs |
| FAQ / expandable content | `umd-element-accordion-item` |
| Person profile | `umd-element-person-bio` |
| Icon + text card | `umd-element-card-icon` |
| Video card | `umd-element-card-video` |
| Grid of logo | `umd-element-hero-grid` |
| Top-level navigation | `umd-element-navigation-header` + `umd-element-nav-item` |


## Spacing and layout

- Every top-level `<section>` gets `class="umd-layout-vertical-landing"` — **except** dark sections that are immediately followed by another dark section. Omit `umd-layout-vertical-landing` from preceding dark sections to avoid a white gap; only the final dark section in the group carries it.
- Pathway and hero are full-bleed — do NOT wrap in a horizontal spacing class.
- Card grids and section intros go inside a `umd-layout-space-horizontal-larger` wrapper.
- `umd-element-quote` uses `umd-layout-space-horizontal-normal` (1280px) — not `larger` (RULES.md §12).
- `data-theme` does not cascade — set it on every child component that needs it (RULES.md §14).
- `umd-element-pathway-highlight` requires real body copy in `slot="text"`. If the source has only a quote and attribution, use `umd-element-quote` instead (RULES.md §5).

## Footer

Always use the visual footer:
```html
<umd-element-footer data-display="visual">
  <a slot="logo" href="/"><img src="../images/logos/footer-logo.svg" alt="University of Maryland" onerror="this.onerror=null;this.src='../images/logos/footer-logo.svg';" /></a>
  <img slot="image" src="../images/large/campus/footer-campus.jpg" alt="University of Maryland campus" />
</umd-element-footer>
```
Do not add contact info, address, or social links — the visual variant renders the logo and image only. Do not use an external logo URL in the footer. The `slot="image"` `alt` must be non-empty — the visual footer's image renderer drops the slotted image entirely if `alt=""` (it does not fall back to the default).

For `slot="logo"` in `umd-element-navigation-header`, use a confirmed accessible URL from the downloaded source. If unavailable or uncertain, fall back to `../images/logos/primary-logo-dark.svg`. When using an external URL, always add `onerror="this.onerror=null;this.src='../images/logos/primary-logo-dark.svg';"` to the `<img>` so hotlink-blocked logos swap to the local fallback at runtime — see CLAUDE.md §Logos.

## Image fallback

Prefer images downloaded into `tmp/assets/images/` — these are already verified. Copy them to `images/projects/{title}/` and reference as repo-relative paths: `../images/projects/{title}/filename.jpg`. Copy any video files to `images/media/`.

If an image was not downloaded (listed in `tmp/skipped-assets.txt` or absent from `tmp/assets/images/`), fall back to the library lookup in CLAUDE.md §Images.

## Output

Write the completed HTML file to `/Users/zjocson/repos/design-system-page-builder/examples/{title}.html`. Confirm the filename when done.

## Cleanup

After the output file is confirmed written, delete the `tmp/` directory:

```bash
rm -rf /Users/zjocson/repos/design-system-page-builder/tmp
```

## Harvest overrides (final step)

After cleanup, spawn an `Explore` subagent to scan the new HTML file and update `OVERRIDES.md`. Brief it like this:

> Scan `<output-path>` for two things:
> 1. **Shadow injections** — IIFEs that call `el.shadowRoot.appendChild(<style>)`. Capture the target component tag, the CSS string injected, and the leading comment that explains why.
> 2. **Page-built components** — light-DOM CSS classes defined in the inline `<style>` block whose names are NOT present in `styles/critical.css` (e.g. `.umd-action-outline-block`, `.umd-layout-grid-cards-no-gap`, `.umd-text-line-trailing`). For each, capture the class name, its DS counterpart (if any), and why a page-built version was needed (read the leading comment).
>
> Then read `OVERRIDES.md`. For each item found:
> - If an entry already exists, append `<output-path>` to the "Pages using this" list (only if not already listed).
> - If no entry exists, append a new entry under the correct heading (Shadow overrides / Page-built components) using the existing entry format.
>
> Do NOT add entries for classes already in `styles/critical.css` — those are sanctioned, not overrides. Do NOT modify the preamble.
>
> Report a one-line summary: `OVERRIDES.md: +N new entries, +M pages added to existing entries`.