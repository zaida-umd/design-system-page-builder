# UMD Design System — Required CSS Reference

Verified against `@universityofmaryland/web-components-library@1.17.18`.

This file documents **every CSS rule** that must be present in your `<style>` block for UMD web components to function correctly. The complete CSS is already assembled in `TEMPLATE.html` — use that as your starting point. This file exists as a reference for understanding what each rule does and why it's needed.

---

## 1. Critical Component Registration

**Why:** Every UMD web component uses shadow DOM with `@container` queries for responsive layout. These queries only fire if the host element has `container-type: inline-size` set. The `cdn.js` script registers the custom elements but does **not** inject these styles. If they're missing, all two-column layouts collapse to single-column.

**When it breaks:** `cdn.js` loads before the CSS → elements upgrade before `:defined` rules exist → `container-type` never gets set → `@container` queries never fire.

```css
/* GROUP 1: container-type: normal
   These components use grid-auto-flow / internal layout that
   breaks under inline-size containment. */
umd-element-utility-header,
umd-element-navigation-header,
umd-element-nav-item,
umd-element-call-to-action {
  display: block;
  container-type: normal;
}

/* GROUP 2: container-type: inline-size
   These components use shadow DOM @container queries that fire
   against the host element. Without inline-size on the host,
   two-column layouts collapse to stacked. */
umd-element-hero,
umd-element-hero-minimal,
umd-element-hero-expand,
umd-element-hero-logo,
umd-element-hero-grid,
umd-element-hero-brand-video,
umd-element-pathway,
umd-element-pathway-highlight,
umd-element-section-intro,
umd-element-section-intro-wide,
umd-element-card,
umd-element-card-overlay,
umd-element-card-icon,
umd-element-card-video,
umd-element-quote,
umd-element-stat,
umd-element-person-bio,
umd-element-accordion-item,
umd-element-footer {
  display: block;
  container-type: inline-size;
}

/* Full-bleed: image-expand needs explicit width: 100% — without it,
   the host collapses to the width of its content slot */
umd-layout-image-expand {
  display: block;
  container-type: inline-size;
  width: 100%;
}
```

Both groups also need `:not(:defined)` rules with `content-visibility: hidden` to prevent FOUC. See `TEMPLATE.html` for the complete selectors.

---

## 2. Font Stack

**Why:** UMD uses Interstate as its primary typeface. The font is licensed — `@font-face` declarations with embedded font data live in UMD's production build pipeline. This CSS sets the font-family stack so Interstate renders when available, with clean fallbacks when it's not.

```css
:root {
  --umd-font-sans:     "Interstate", Helvetica, Arial, Verdana, sans-serif;
  --umd-font-serif:    "Crimson Pro", Georgia, serif;
  --umd-font-campaign: "Barlow Condensed", Arial Narrow, sans-serif;
}
body, p, li, dd, dt, input, select, textarea, button {
  font-family: var(--umd-font-sans);
}
```

**To render Interstate:** Either link UMD's production `critical.css` from the CMS build, or self-host the font files with your own `@font-face` declarations. Without the font loaded, layouts render correctly — only the typeface changes.

---

## 3. Vertical Spacing

**Why:** Consistent spacing between page sections and between items within sections. The design system defines these tokens but `cdn.js` does not inject them.

### Landing pages

```css
/* Between top-level sections */
.umd-layout-space-vertical-landing           { margin-bottom: 56px; }
@media (min-width: 768px)  { .umd-layout-space-vertical-landing  { margin-bottom: 80px; } }
@media (min-width: 1024px) { .umd-layout-space-vertical-landing  { margin-bottom: 120px; } }

/* Between items within a section */
.umd-layout-space-vertical-landing-child     { margin-bottom: 32px; }
@media (min-width: 768px)  { .umd-layout-space-vertical-landing-child { margin-bottom: 40px; } }
@media (min-width: 1024px) { .umd-layout-space-vertical-landing-child { margin-bottom: 48px; } }
```

> **Note:** cdn.js also registers the alias names `umd-layout-vertical-landing` and `umd-layout-vertical-landing-child` (without `space-`). Both forms work, but the canonical names with `space-` are what UMD's production sites use.

### Interior pages

```css
.umd-layout-space-vertical-interior          { margin-bottom: 56px; }
@media (min-width: 1024px) { .umd-layout-space-vertical-interior { margin-bottom: 80px; } }

.umd-layout-space-vertical-interior-child    { margin-bottom: 32px; }
```

---

## 4. Horizontal Spacing (Page Locks)

**Why:** Centers content and applies responsive side padding. Different `max-width` values create content width tiers.

```css
/* Shared padding — all variants */
[class^="umd-layout-space-horizontal-"] {
  display: block;
  margin-left: auto;
  margin-right: auto;
  padding-left: 24px;
  padding-right: 24px;
}
@media (min-width: 768px) {
  [class^="umd-layout-space-horizontal-"] {
    padding-left: 48px;
    padding-right: 48px;
  }
}
@media (min-width: 1200px) {
  [class^="umd-layout-space-horizontal-"] {
    padding-left: 64px;
    padding-right: 64px;
  }
}

/* Per-class max-width */
.umd-layout-space-horizontal-full     { max-width: 100%;   }
.umd-layout-space-horizontal-larger   { max-width: 1600px; }
.umd-layout-space-horizontal-large    { max-width: 1400px; }
.umd-layout-space-horizontal-normal   { max-width: 1280px; }
.umd-layout-space-horizontal-small    { max-width: 992px;  }
.umd-layout-space-horizontal-smallest { max-width: 800px;  }
```

### Class usage guide

| Class | max-width | Use for |
|---|---|---|
| `umd-layout-space-horizontal-full` | 100% | Navigation header, full-bleed sections |
| `umd-layout-space-horizontal-larger` | 1600px | Wide landing page content, card grids |
| `umd-layout-space-horizontal-large` | 1400px | Standard landing page content |
| `umd-layout-space-horizontal-normal` | 1280px | Body content, interior pages |
| `umd-layout-space-horizontal-small` | 992px | Narrow content columns |
| `umd-layout-space-horizontal-smallest` | 800px | Article body, forms |

---

## 5. Grid Layouts

**Why:** Responsive grid classes for card grids and content layouts. These are defined in `cdn.js` (`web-styles-library → layout/grid/gap`) and emitted as CSS class rules. They must be included in your `<style>` block.

```css
/* 4-column grid: 1 → 2 → 4 columns */
.umd-layout-grid-gap-four {
  display: grid;
  grid-gap: 32px;
}
@media (min-width: 650px) {
  .umd-layout-grid-gap-four {
    grid-template-columns: repeat(2, 1fr);
  }
  .umd-layout-grid-gap-four > p:not(:last-child) { margin-bottom: 0; }
}
@media (min-width: 1024px) {
  .umd-layout-grid-gap-four {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* 3-column grid: 1 → 3 columns */
.umd-layout-grid-gap-three {
  display: grid;
  grid-gap: 32px;
}
@media (min-width: 768px) {
  .umd-layout-grid-gap-three {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* 2-column grid: 1 → 2 columns */
.umd-layout-grid-gap-two {
  display: grid;
  grid-gap: 32px;
}
@media (min-width: 650px) {
  .umd-layout-grid-gap-two {
    grid-template-columns: repeat(2, 1fr);
  }
  .umd-layout-grid-gap-two > p:not(:last-child) { margin-bottom: 0; }
}
@media (min-width: 1024px) {
  .umd-layout-grid-gap-two {
    grid-gap: 40px;
  }
}

/* Stacked (single column) */
.umd-layout-grid-gap-stacked {
  display: grid;
  grid-template-columns: 1fr;
  grid-gap: 24px;
}
@media (min-width: 1024px) {
  .umd-layout-grid-gap-stacked {
    grid-gap: 40px;
  }
}

/* Masonry (2-column, uneven rows) */
.umd-layout-grid-masonry {
  display: grid;
  grid-template-columns: 1fr;
  grid-gap: 24px;
}
@media (min-width: 768px) {
  .umd-layout-grid-masonry {
    grid-template-columns: 1fr 1fr;
    grid-gap: 32px;
  }
}
@media (min-width: 1024px) {
  .umd-layout-grid-masonry {
    grid-gap: 40px;
  }
}
```

### Grid class usage guide

| Class | Columns | Use for |
|---|---|---|
| `umd-layout-grid-gap-four` | 1 → 2 → 4 | Card grids (cards, card overlays) |
| `umd-layout-grid-gap-three` | 1 → 3 | Three-column layouts |
| `umd-layout-grid-gap-two` | 1 → 2 | Two-column content grids |
| `umd-layout-grid-gap-stacked` | 1 | Single-column stacked items |
| `umd-layout-grid-masonry` | 1 → 2 | Masonry/uneven grid layouts |

### Grid child utilities

```css
/* Force equal-height children in a grid */
.umd-layout-grid-child-fill-height,
.umd-layout-grid-child-fill-height > * {
  height: 100%;
}

/* Span a child across two grid columns */
.umd-layout-grid-child-size-double {
  grid-column: span 2;
}
```

---

## 6. Watermark (Optional Decorative Pattern)

**Why:** Large, faded text behind section headers. Purely decorative (`aria-hidden`). Uses scroll-driven animation where supported.

The watermark wrapper `<div>` must carry `position: relative` and `isolation: isolate` to create the correct stacking context. Apply these on the `.umd-text-decoration-watermark` class itself — NOT on the horizontal spacing class.

```css
/* Watermark container — needs positioning context */
.umd-text-decoration-watermark {
  position: relative;
  isolation: isolate;
}

/* Base positioning and font — all three class names */
:is(.umd-text-decoration-watermark, .umd-watermark, .umd-watermark-dark) > * {
  position: absolute;
  top: 20px;
  left: -2%;
  color: #f1f1f1;
  font-weight: 700;
  text-transform: uppercase;
  font-size: min(calc(44px + 13vw), 240px);
  line-height: 0;
  pointer-events: none;
  user-select: none;
  white-space: nowrap;
}

/* Light variant */
:is(.umd-text-decoration-watermark, .umd-watermark):not(.umd-watermark-dark) > * {
  opacity: 0.6;
  z-index: -1;
}

/* Dark variant */
.umd-watermark-dark > * {
  opacity: 0.12;
  z-index: inherit;
}

/* Scroll-driven entrance animation */
@keyframes slide-in-from-left {
  from { transform: translate(-15vw); }
  to   { transform: translate(0); }
}
@media (prefers-reduced-motion: no-preference) {
  @supports (animation-timeline: scroll()) {
    :is(.umd-text-decoration-watermark, .umd-watermark, .umd-watermark-dark) > * {
      animation: slide-in-from-left forwards;
      animation-timeline: view();
      animation-range-start: 0;
      animation-range-end: 100vh;
      transform: translate(-15vw);
    }
  }
}
```

**Critical:** All three class names (`.umd-text-decoration-watermark`, `.umd-watermark`, `.umd-watermark-dark`) must be in the `:is()` selector. Omitting one means that variant gets no positioning or font styles.
