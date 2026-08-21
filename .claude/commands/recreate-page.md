# Recreate this page / convert this page to the design system

Build a complete UMD landing page HTML file based on an existing page and save it to `/Users/zjocson/repos/page-builder-examples/examples/`. Help identify the right UMD design system component for all components on a given piece of content or use case.



## Required page structure

Every page must open with these three elements, in this order, before any content:

1. **Global university header** — `<umd-element-navigation-utility data-alert-off="true" role="navigation" aria-label="Utility navigation"></umd-element-navigation-utility>` (hardcoded, no config, never omit — this is the UMD-wide bar from umd.edu)
2. **Site utility header** — `<umd-element-utility-header></umd-element-utility-header>` (hardcoded, no config)
3. **Site navigation header** — `<umd-element-navigation-header sticky class="umd-layout-space-horizontal-full">` with logo and nav items from the source page

## Step 1: Download source assets (subagent)

Before doing any analysis or building, spawn a subagent to download the source page assets into `/Users/zjocson/repos/page-builder-examples/tmp/`. The subagent should:

1. Create the directory `/Users/zjocson/repos/page-builder-examples/tmp/` if it does not exist.
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

Use content and images from the source page as the fictional client. Shorten the page title used in the command and name the output file `examples/{title}.html` in the page-builder-examples repo.

## Copy fidelity (mandatory)

**Never paraphrase, summarize, or invent body copy, headlines, attributions, stats, or CTA labels.** All visible text must be lifted verbatim from `tmp/source.html`.

For every text-bearing component (hero body, pathway body, quote, attribution + sub-text, stat label, CTA label, card headline + body, banner copy, deadline list, breadcrumb labels):

1. **Locate the source string** in `tmp/source.html`. If you can't find it, do not write placeholder copy — flag the missing copy in your summary and ask the user.
2. **Copy it verbatim** into the corresponding slot. Preserve apostrophes, em dashes, ampersands, casing, line breaks, hashtags (e.g. `#BeATerp`), and trailing punctuation. Encode `&` as `&amp;`, `<`/`>` as entities only as required by HTML.
3. **Do not "improve" the wording.** No compression for length, no rewrites for tone, no synthesized paraphrases that "sound right." If the source copy doesn't fit the component, raise it instead of paraphrasing.
4. **Verify before writing.** When in doubt about a string, re-read the relevant block of `tmp/source.html` rather than guessing from memory.

If a section on the source page has no DS-equivalent component and the user hasn't directed how to handle it, omit it and note the omission in your summary — do not invent substitute copy.

This rule applies during the initial build *and* every later edit to a recreate-page output. When the user asks for a copy change without supplying the new text, ask for the verbatim string before editing.

**Images:** Extract actual image paths from `tmp/source.html` — do not guess or construct URLs. For the generated page, copy the downloaded images from `tmp/assets/images/` into `/Users/zjocson/repos/page-builder-examples/images/projects/{title}/` (where `{title}` matches the output filename, e.g. `images/projects/sph/`) and reference them as repo-relative paths: `../images/projects/{title}/filename.jpg`. Do not commit video files to this repo — use a poster image for video heroes instead.


## Process

1. **Understand the content** — read `tmp/source.html` and the downloaded assets to understand what each component on the page does:
   - What *type* of content is it? (headline + image, stats, quote, navigation, cards, hero, etc.)
   - What is its *purpose* on the page? (capture attention, orient the user, showcase data, provide navigation, feature a story, etc.)
   - Where does it appear? (top of page, mid-page section, sidebar, full-width band, etc.)
   - Are there constraints? (must have image, needs a CTA, has a lot of text, etc.)

2. **Inventory carousels and side navigation in the source** — before mapping content to components, scan the source for these two patterns specifically:
   - **Carousels / sliders** (Slick, Owl, Revolution, Gavias slider-layer, Swiper, etc. — often `<ul>`/`<div>` with `data-` attributes for animation). If the source uses a carousel for a content set, recreate it with the matching DS carousel — do **not** flatten to a grid. Mapping: image slider → `umd-element-carousel-image-wide` or `-image`; thumbnail-driven people/photo carousel → `umd-element-carousel-thumbnail`; row of cards → `umd-element-carousel-cards`. Flattening a carousel to a grid changes the page rhythm and over-emphasizes content the source intentionally treated as supplementary.
   - **Side / left-rail navigation.** Many CMS templates render a sub-section nav rail. Don't drop it. Recreate it as `umd-element-accordion-item` groups near the bottom of the page — one accordion per natural parent section — unless the user directs otherwise. See `LAYOUT-PATTERNS.md` "Side Navigation as Accordion Stack" and `RULES.md §32` for the wrap and gap.

3. **Match to registry** — scan the registry for candidates and narrow to the best option.

4. **Recommend** — for each component:
   - Component tag name
   - Why it fits this content
   - Any variants or attributes to use (`data-display`, `data-theme`, etc.)
   - Any gotchas or rules that apply (reference the relevant RULES.md section)
   - A minimal working code example with realistic placeholder content

4. **Distinguish close alternatives** — if two components are similar (e.g. `umd-element-hero` vs `umd-element-hero-minimal`, or `umd-element-pathway` overlay vs standard), explain the tradeoff clearly so the user can choose.

## Component cheat-sheet

Use the content-type → component cheat-sheet in `/recommend-component` — it is the **single source** for first-pass matching (do not maintain a copy here). Verify tags/attributes against `registry/` before use; the registry wins on conflict.


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
  <a slot="logo" href="/"><img src="../page-builder/images/logos/footer-logo.svg" alt="University of Maryland" onerror="this.onerror=null;this.src='../page-builder/images/logos/footer-logo.svg';" /></a>
  <img slot="image" src="../page-builder/images/large/campus/footer-campus.jpg" alt="University of Maryland campus" />
</umd-element-footer>
```
Do not add contact info, address, or social links — the visual variant renders the logo and image only. Do not use an external logo URL in the footer. The `slot="image"` `alt` must be non-empty — the visual footer's image renderer drops the slotted image entirely if `alt=""` (it does not fall back to the default).

For `slot="logo"` in `umd-element-navigation-header`, use a confirmed accessible URL from the downloaded source. If unavailable or uncertain, fall back to `../page-builder/images/logos/primary-logo-dark.svg`. When using an external URL, always add `onerror="this.onerror=null;this.src='../page-builder/images/logos/primary-logo-dark.svg';"` to the `<img>` so hotlink-blocked logos swap to the local fallback at runtime — see CLAUDE.md §Logos.

## Image fallback

Prefer images downloaded into `tmp/assets/images/` — these are already verified. Copy them to `images/projects/{title}/` in the page-builder-examples repo and reference as repo-relative paths: `../images/projects/{title}/filename.jpg`. Do not copy video files into this repo — use a poster image instead.

If an image was not downloaded (listed in `tmp/skipped-assets.txt` or absent from `tmp/assets/images/`), fall back to the library lookup in CLAUDE.md §Images.

## Output

Write the completed HTML file to `/Users/zjocson/repos/page-builder-examples/examples/{title}.html`. Confirm the filename when done.

## Cleanup

After the output file is confirmed written, delete the `tmp/` directory:

```bash
rm -rf /Users/zjocson/repos/page-builder-examples/tmp
```

## Attribute check (after writing)

Run the registry-driven `data-theme` validator on the new page:

```bash
python3 /Users/zjocson/repos/design-system-page-builder/tools/check-themes.py <output-file>
```

- **ERROR** — the value is not in the design system's theme vocabulary, i.e. a typo. Fix before reporting success. These are the ones worth tooling for: a component that ignores an unrecognized `data-theme` renders a misspelled value *identically* to a correct one (pathway `whte` vs `white`), so the mistake is invisible on the page and in a screenshot.
- **WARNING** — a real theme word the registry does not list for that component. Usually inert; confirm it is deliberate. If it turns out to be genuinely supported, update `registry/` rather than silencing the warning.

Exit code is non-zero only for errors, so warnings will not block a build.

---

## Harvest overrides (final step)

After cleanup, spawn an `Explore` subagent to scan the new HTML file and update `OVERRIDES.md`. Brief it like this:

> Scan `<output-path>` for two things:
> 1. **Shadow injections** — IIFEs that call `el.shadowRoot.appendChild(<style>)`. Capture the target component tag, the CSS string injected, and the leading comment that explains why.
> 2. **Page-built components** — light-DOM CSS classes defined in the inline `<style>` block whose names are NOT present in `styles/critical.css` (typically a custom component with no DS equivalent, e.g. a page-specific `.sp-venn-diagram` block). Skip any class that IS in `critical.css` — that includes `.umd-action-outline-block`, `.umd-text-line-trailing`, and all `umd-layout-grid-*` classes (a no-gap card grid is already `umd-layout-grid-columns-*` upstream — never harvest a hand-rolled duplicate). For each genuine page-built class, capture the class name, its DS counterpart (if any), and why a page-built version was needed (read the leading comment).
>
> Then read `OVERRIDES.md`. For each item found:
> - If an entry already exists, append `<output-path>` to the "Pages using this" list (only if not already listed).
> - If no entry exists, append a new entry under the correct heading (Shadow overrides / Page-built components) using the existing entry format.
>
> Do NOT add entries for classes already in `styles/critical.css` — those are sanctioned, not overrides. Do NOT modify the preamble.
>
> Report a one-line summary: `OVERRIDES.md: +N new entries, +M pages added to existing entries`.