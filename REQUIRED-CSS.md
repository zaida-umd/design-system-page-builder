# UMD Design System — Required CSS Reference

Verified against `@universityofmaryland/web-components-library@1.17.18`.

This file documents **every CSS rule** that must be present in your `<style>` block for UMD web components to function correctly. The complete CSS is already assembled in `TEMPLATE.html` — use that as your starting point. This file exists as a reference for understanding what each rule does and why it's needed.

---

## 1. Critical Component Registration

**Why:** Every UMD web component uses shadow DOM with `@container` queries for responsive layout. These queries only fire if the host element has `container-type: inline-size` set. The `cdn.js` script registers the custom elements but does **not** inject these styles. If they're missing, all two-column layouts collapse to single-column.

**When it breaks:** `cdn.js` loads before the CSS → elements upgrade before `:defined` rules exist → `container-type` never gets set → `@container` queries never fire.

```css
/* Every component tag that uses container queries */
umd-element-hero:defined,
umd-element-hero-minimal:defined,
umd-element-hero-expand:defined,
umd-element-hero-logo:defined,
umd-element-hero-grid:defined,
umd-element-hero-brand-video:defined,
umd-element-card:defined,
umd-element-card-overlay:defined,
umd-element-card-icon:defined,
umd-element-card-video:defined,
umd-element-pathway:defined,
umd-element-pathway-highlight:defined,
umd-element-section-intro:defined,
umd-element-section-intro-wide:defined,
umd-element-stat:defined,
umd-element-quote:defined,
umd-element-call-to-action:defined,
umd-element-footer:defined,
umd-element-navigation-header:defined,
umd-element-utility-header:defined {
  display: block;
  container-type: inline-size;
}

/* EXCEPTION: nav-item must use container-type: normal.
   inline-size containment breaks the grid-auto-flow: column layout
   inside the nav header shadow DOM — nav items collapse and overlap. */
umd-element-nav-item:defined {
  content-visibility: visible;
  container-type: normal;
  display: block;
}

/* image-expand needs explicit width: 100% — without it, the host
   collapses to the width of its content slot (e.g. a narrow quote)
   and the full-bleed image animation breaks */
umd-layout-image-expand:defined {
  display: block;
  container-type: inline-size;
  width: 100%;
}
```

**Load order:** Always inline this CSS as a `<style>` block in `<head>`, before the `<script>` tag for `cdn.js`. A `<link>` to a relative CSS file will fail when opening HTML directly from disk.

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
.umd-layout-vertical-landing           { margin-bottom: 56px; }
@media (min-width: 768px)  { .umd-layout-vertical-landing  { margin-bottom: 80px; } }
@media (min-width: 1024px) { .umd-layout-vertical-landing  { margin-bottom: 120px; } }

/* Between items within a section */
.umd-layout-vertical-landing-child     { margin-bottom: 32px; }
@media (min-width: 768px)  { .umd-layout-vertical-landing-child { margin-bottom: 40px; } }
@media (min-width: 1024px) { .umd-layout-vertical-landing-child { margin-bottom: 48px; } }
```

### Interior pages

```css
.umd-layout-vertical-interior          { margin-bottom: 56px; }
@media (min-width: 1024px) { .umd-layout-vertical-interior { margin-bottom: 80px; } }

.umd-layout-vertical-interior-child    { margin-bottom: 32px; }
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

### Extra properties for section-intro-wide wrapper

When `.umd-layout-space-horizontal-larger` wraps `umd-element-section-intro-wide`, three additional properties are required:

```css
.umd-layout-space-horizontal-larger {
  position: relative;         /* watermark span is position:absolute */
  container-type: inline-size; /* fires component's internal @container query */
  isolation: isolate;         /* local stacking context for watermark z-index */
}
```

---

## 5. Watermark (Optional Decorative Pattern)

**Why:** Large, faded text behind section headers. Purely decorative (`aria-hidden`). Uses scroll-driven animation where supported.

```css
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
