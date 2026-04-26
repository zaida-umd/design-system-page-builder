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

**Why:** UMD uses Interstate as its primary typeface. The font is licensed — `@font-face` declarations with embedded font data live in UMD's production build pipeline. This CSS sets the font-family stack so Interstate renders when available, with clean fallbacks when it's not.

**Font stacks defined:**
- `--umd-font-sans`: Interstate, Helvetica, Arial, Verdana, sans-serif
- `--umd-font-serif`: Crimson Pro, Georgia, serif
- `--umd-font-campaign`: Barlow Condensed, Arial Narrow, sans-serif

**To render Interstate:** Either link UMD's production `critical.css` from the CMS build, or self-host the font files with your own `@font-face` declarations. Without the font loaded, layouts render correctly — only the typeface changes.

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
