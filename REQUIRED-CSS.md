# UMD Design System — Required CSS Reference

Verified against `@universityofmaryland/web-components-library@1.18.2`.

This file explains **why** each CSS rule group is needed. The actual CSS lives in **`styles/critical.css`** (the single source of truth). `TEMPLATE.html` inlines that file in `<head>` before `cdn.js`.

---

## 1. Critical Component Registration (`styles/critical.css` — section 1)

**Why:** Every UMD web component uses shadow DOM with `@container` queries for responsive layout. These queries only fire if the host element has `container-type: inline-size` set. The `cdn.js` script registers the custom elements but does **not** inject these styles. If they're missing, all two-column layouts collapse to single-column.

**When it breaks:** `cdn.js` loads before the CSS -> elements upgrade before `:defined` rules exist -> `container-type` never gets set -> `@container` queries never fire.

**Two container-type groups:**
- **GROUP 1 (`container-type: normal`):** Navigation, headers, CTAs. Using `inline-size` on these breaks their `grid-auto-flow: column` internal layout.
- **GROUP 2 (`container-type: inline-size`):** Heroes, pathways, cards, quotes, stats, footer, nav-slider, media-inline, breadcrumb. Required for `@container` queries that fire two-column layouts.
- **GROUP 3 (full-bleed):** `umd-layout-image-expand` — needs `width: 100%` in addition to `container-type: inline-size`, or the host collapses to content width.

**Load order:** Always inline this CSS as a `<style>` block in `<head>`, before the `<script>` tag for `cdn.js`. A `<link>` to a relative CSS file will fail when opening HTML directly from disk.

---

## 2. Font Stack (`styles/critical.css` — section 2)

**Why:** UMD uses Interstate as its primary typeface. This CSS sets the font-family stack; the `@font-face` declarations themselves come from the `css/font-faces.min.css` bundle that `TEMPLATE.html` links (see RULES.md §2). The stack lists fallbacks so type still renders cleanly if that bundle is unavailable.

**Font stacks defined:**
- `--umd-font-sans`: Interstate, Helvetica, Arial, Verdana, sans-serif
- `--umd-font-serif`: Crimson Pro, Georgia, serif
- `--umd-font-campaign`: Barlow Condensed, Arial Narrow, sans-serif

**To render Interstate:** Keep the `font-faces.min.css` `<link>` from `TEMPLATE.html`'s `<head>` block — no self-hosting needed. Without it the stack falls back to Helvetica/Arial; layouts render correctly, only the typeface changes.

---

## 3. Vertical Spacing (`styles/critical.css` — section 3)

**Why:** Consistent spacing between page sections and between items within sections. The design system defines these tokens but `cdn.js` does not inject them.

**Classes provided:**
- `.umd-layout-vertical-landing` / `.umd-layout-vertical-landing-child` — landing pages
- `.umd-layout-vertical-interior` / `.umd-layout-vertical-interior-child` — interior pages (aliases: `.umd-layout-space-vertical-interior*`)
- `.umd-layout-space-vertical-headline-large` — headline-to-grid gap

See RULES.md §10 for usage rules (when to apply, landing vs. interior).

---

## 4. Horizontal Spacing / Page Locks (`styles/critical.css` — section 4)

**Why:** Centers content and applies responsive side padding. Different `max-width` values create content width tiers.

**Classes provided:** Six `umd-layout-space-horizontal-*` variants from `full` (100%) down to `smallest` (800px).

See RULES.md §12 for the class usage guide and which components go in which lock.

---

## 5. Watermark Decoration (`styles/critical.css` — section 5)

**Why:** Large, faded text behind section headers. Purely decorative (`aria-hidden`). Uses scroll-driven animation where supported.

**Critical:** All three class names (`.umd-text-decoration-watermark`, `.umd-watermark`, `.umd-watermark-dark`) must be in the `:is()` selector. Omitting one means that variant gets no positioning or font styles.

See RULES.md §15 for the watermark HTML pattern.

---

## 6. Layout Patterns (`styles/critical.css` — sections 7–8)

**Why:** Grid utilities, dark section backgrounds, figure alignment, and CTA row layout. These are CSS utility classes from `@universityofmaryland/web-styles-library` — not injected by `cdn.js`.

**Classes provided:**
- `.umd-layout-grid-gap-two` — two-column grid
- `.umd-layout-grid-inline-tablet-rows` — inline CTA row
- `.umd-layout-background-full-dark` — full-width dark section
- `.umd-layout-alignment-block-stacked` — stacked figure content
- `.umd-layout-grid-gap-stacked` — single-column stacked grid
- `.umd-layout-grid-child-fill-height` — equal-height card grid children

See LAYOUT-PATTERNS.md for HTML usage examples with these classes.

---

## 7. Typography (`styles/critical.css` — section 9)

**Why:** Inline headline classes used inside `umd-text-rich-advanced` for in-content headlines and labels. Not injected by `cdn.js`.

**Classes provided:**
- `.umd-sans-large` — 18px section labels
- `.umd-sans-larger-bold` — 18–22px responsive inline headlines
- `.umd-sans-extralarge-bold` — 18–32px responsive section headlines
- `.umd-sans-largest-uppercase` — 32–44px uppercase headings (sticky columns)
- `.text-black`, `.text-white` — color utilities

See LAYOUT-PATTERNS.md for which elements these apply to (`<p>` not heading tags).

---

## 8. Rich Text Advanced (`styles/critical.css` — section 10)

**Why:** Editorial body copy styling. 18px/1.5em with animated underline link hover. Two variants: light (`.umd-text-rich-advanced`) and dark (`.umd-text-rich-advanced-dark`).

See LAYOUT-PATTERNS.md for HTML patterns (single column, two columns, dark background, CTAs inside rich text).

---

## 9. Interior Page Layout (`styles/critical.css` — section 11)

**Why:** Sidebar + content column flex layout and content column max-width. These production UMD classes are not in `cdn.js` — they must be defined locally.

**Classes provided:**
- `.umd-layout-space-columns-left` — sidebar + content flex layout
- `.max-w-[800px]` — content column cap

See RULES.md §21 for the full interior page layout skeleton.

---

## 10. Image-Expand & Sticky Columns Utilities (`styles/critical.css` — sections 12–13)

**Why:** Utility classes for constraining content inside `umd-layout-image-expand` and spacing inside `umd-element-sticky-columns`. Not in `cdn.js`.

See RULES.md §17 for image-expand patterns and §20 for sticky columns patterns.

---

## 11. Filter Band Companions (`styles/critical.css` — section 23)

**Why:** The filterable-listing pattern is almost entirely upstream classes; only the search row, the results count and the divider list are page-built. See LAYOUT-PATTERNS.md "Filter Band".

**Classes provided:**
- `.umd-filter-search-row` / `.umd-filter-search-btn` — text input + 44×44 red submit
- `.umd-filter-results-count` — the live count line
- `.umd-filter-list` / `.umd-filter-item` — zero-gap stack with `1px #d0d0d0` rules between visible items

**The `border-top: 0` line is a collision fix, not decoration.** When the items are `umd-element-card[data-display="list"]`, the component puts `border-top: 1px solid #E6E6E6` + `padding-top: 24px` on every sibling after the first. That border lands directly against `.umd-filter-item`'s own `border-bottom`, and the pair renders as one doubled 2px rule in two greys. The divider list owns its rules, so the component's is zeroed. The selector carries tag names because it has to clear the component rule's `0,2,2`.

---

## 12. Pill List Anchor Color (`styles/critical.css` — section 24)

**Why:** `element.min.css` styles `.umd-text-cluster-pill` (deprecated alias `.umd-pill-list`) with a `#FAFAFA` chip ground, `8px 12px` box, 12px Interstate and a `#FFD200` hover on `<a>` children — but the **light** variant never declares `color`. An anchor chip therefore renders in the browser's default blue/purple with a UA underline. The **dark** variant does declare one (`color:#FFFFFF`, `#000000` on hover), so the omission is an asymmetry in the package rather than an implied black.

Same shape as section 11's utility-nav rules: upstream styles a wrapper this composition does not use, and the bare `<a>` is left unstyled.

**Scoped to the light class names**, so the dark variant's white is untouched.

**Retire when** `composePill()`'s light branch gains `color: color.black` — `packages/styles/source/element/text/cluster.ts` in the design-system submodule.

> Note: the section numbers above refer to `styles/critical.css`. Entries 1–10 in this file predate several critical.css sections and their references have drifted; entries 11–12 are accurate.
