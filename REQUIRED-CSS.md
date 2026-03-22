# UMD Page Builder — Required CSS Reference

Every CSS rule in `TEMPLATE.html` exists for a specific reason. This document explains what each block does and what breaks without it.

Verified against `@universityofmaryland/web-components-library@1.17.18`.

---

## 1. Component `:not(:defined)` rules

```css
umd-element-pathway:not(:defined) {
  content-visibility: hidden;
}
```

**What it does:** Hides the component's raw slotted content (unstyled HTML) during the brief window between page parse and `cdn.js` registering the custom element.

**What breaks without it:** Users see a flash of unstyled content (FOUC) — raw headings, paragraphs, and images appear briefly before the shadow DOM takes over.

---

## 2. Component `:defined` rules — `display: block`

```css
umd-element-pathway {
  display: block;
  container-type: inline-size;
}
```

**What it does:** Custom elements default to `display: inline` per the HTML spec. The UMD components don't set `:host { display: block }` in their shadow styles. Without an explicit `display: block` from outside the shadow boundary, the host element has no block-level width for container queries to measure.

**What breaks without it:** Every component that uses `@container` queries internally (pathways, cards, heroes, section-intros) collapses to a single-column stacked layout because the container query threshold (e.g., `@container (min-width: 800px)`) never fires against a zero-width inline box.

---

## 3. `container-type` split — `normal` vs `inline-size`

This is the most critical distinction in the CSS.

### GROUP 1: `container-type: normal`

```css
umd-element-navigation-header,
umd-element-nav-item,
umd-element-call-to-action,
umd-element-utility-header {
  display: block;
  container-type: normal;
}
```

**What it does:** These components use internal layout mechanisms (e.g., `grid-auto-flow: column` in the nav header) that are **broken by size containment**. Setting `container-type: normal` gives them a block box without imposing size containment.

**What breaks with `inline-size`:**
- **Nav header:** Nav items collapse to zero width and stack/overlap. The header's internal grid layout fails because `inline-size` containment prevents the grid children from contributing to the container's intrinsic size.
- **Nav items:** Dropdown menus and link text collapse.
- **CTAs:** Button text may collapse or overflow.

### GROUP 2: `container-type: inline-size`

```css
umd-element-pathway,
umd-element-card,
umd-element-hero,
/* ... all layout components ... */
umd-element-footer {
  display: block;
  container-type: inline-size;
}
```

**What it does:** Enables `@container` queries inside the shadow DOM to fire based on the host element's inline size (width). This is what triggers two-column layouts at breakpoints like `@container (min-width: 800px)`.

**What breaks without it:** All multi-column layouts collapse to single-column stacked. Only `data-display="hero"` pathways are immune (they use padding-based layout, not container queries).

### GROUP 3: Full-bleed — `umd-layout-image-expand`

```css
umd-layout-image-expand {
  display: block;
  container-type: inline-size;
  width: 100%;
}
```

**What it does:** In addition to the standard `display: block` + `container-type: inline-size`, this component needs explicit `width: 100%` because it's meant to span the full viewport.

**What breaks without `width: 100%`:** The component collapses to the intrinsic width of its content slot, which may be much narrower than the viewport.

**Do not wrap** this component in a `umd-layout-space-horizontal-*` class — it manages its own full-bleed width.

---

## 4. Font stack

```css
:root {
  font-family: "Interstate", Helvetica, Arial, Verdana, sans-serif;
}
p, li, label, input, textarea, select {
  font-family: "Interstate", Helvetica, Arial, Verdana, sans-serif;
}
```

**What it does:** Sets the Interstate font family on all body text and form elements. Interstate is a licensed typeface — these rules set the *stack* but do not embed the font. Without separate `@font-face` declarations (from UMD's production build), the browser falls back to Helvetica/Arial.

**What breaks without it:** Body text renders in the browser's default sans-serif (usually Times New Roman or system default). Layouts and sizing are unaffected — only the typeface changes.

---

## 5. Vertical spacing classes

```css
.umd-layout-vertical-landing           { margin-bottom: 56px; }
@media (min-width: 768px)  { .umd-layout-vertical-landing  { margin-bottom: 80px; } }
@media (min-width: 1024px) { .umd-layout-vertical-landing  { margin-bottom: 120px; } }
```

**What it does:** Provides consistent responsive spacing between page sections (landing pages) and between items within sections. Four classes are available:

| Class | Use for | Mobile | Tablet | Desktop |
|---|---|---|---|---|
| `umd-layout-vertical-landing` | Between sections (landing pages) | 56px | 80px | 120px |
| `umd-layout-vertical-landing-child` | Between items in a section (landing) | 32px | 40px | 48px |
| `umd-layout-vertical-interior` | Page content area (interior pages) | 56px | 56px | 80px |
| `umd-layout-vertical-interior-child` | Between items (interior pages) | 32px | 32px | 32px |

**What breaks without it:** Sections butt up against each other with no vertical rhythm. The page looks cramped and loses the deliberate spacing hierarchy.

**Source:** `@universityofmaryland/web-styles-library` → `layout/vertical.js`

---

## 6. Horizontal spacing classes (page-lock)

```css
[class^="umd-layout-space-horizontal-"] {
  display: block;
  margin-left: auto;
  margin-right: auto;
  padding-left: 24px;
  padding-right: 24px;
}
```

**What it does:** Centers content with responsive side padding and a max-width cap. Six width tiers are available:

| Class | max-width | Use for |
|---|---|---|
| `umd-layout-space-horizontal-full` | 100% | Navigation header, full-bleed sections |
| `umd-layout-space-horizontal-larger` | 1600px | Wide landing page content |
| `umd-layout-space-horizontal-large` | 1400px | Standard landing page content |
| `umd-layout-space-horizontal-normal` | 1280px | Body content, interior pages |
| `umd-layout-space-horizontal-small` | 992px | Narrow content columns |
| `umd-layout-space-horizontal-smallest` | 800px | Article body, forms |

**What breaks without it:** Content spans the full viewport with no padding, or has no max-width constraint. On wide screens, text lines become unreadably long.

**Note:** Pathway, hero, and `umd-layout-image-expand` manage their own horizontal spacing internally — do not wrap them in these classes.

**Source:** `@universityofmaryland/web-styles-library` → `layout/space/horizontal.js`

---

## 7. Section-intro-wide wrapper properties

```css
.umd-layout-space-horizontal-larger {
  position: relative;
  container-type: inline-size;
  isolation: isolate;
}
```

**What it does:** Three properties required when `.umd-layout-space-horizontal-larger` wraps `umd-element-section-intro-wide`:

- **`position: relative`** — The watermark `<span>` is `position: absolute` and needs an anchor.
- **`container-type: inline-size`** — Fires the section-intro-wide's internal container query that puts headline and CTA in a flex row at 500px+.
- **`isolation: isolate`** — Creates a local stacking context so `z-index: -1` on the watermark goes behind the headline text, not behind the page background.

**What breaks without it:**
- Without `position: relative`: Watermark floats to the nearest ancestor or viewport edge.
- Without `container-type: inline-size`: Section intro stays stacked (headline above CTA) even on wide screens.
- Without `isolation: isolate`: Watermark disappears behind the page background.

---

## 8. Watermark decoration

```css
:is(.umd-text-decoration-watermark, .umd-watermark, .umd-watermark-dark) > * {
  position: absolute;
  top: 20px;
  left: -2%;
  /* ... */
}
```

**What it does:** Positions and styles the large decorative background text used on section intros. Three class names are supported (all must appear in the base `:is()` selector):

- `.umd-text-decoration-watermark` — light variant (60% opacity, z-index: -1)
- `.umd-watermark` — alias for the light variant
- `.umd-watermark-dark` — dark variant (12% opacity, z-index: inherit)

The scroll-driven animation (`animation-timeline: view()`) is progressive enhancement — browsers that don't support it get a static watermark.

**What breaks without it:** The watermark text renders as normal-sized paragraph text in the document flow, pushing content down.

**Critical:** All three class names must be in the base `:is()` selector. Omitting `.umd-watermark-dark` means the dark variant gets no positioning or font styling at all.

---

## 9. Grid utilities

```css
.umd-layout-grid-child-fill-height {
  display: flex;
  flex-direction: column;
}
.umd-layout-grid-child-fill-height > * {
  flex: 1;
}
```

**What it does:** Makes grid children stretch to equal heights within a row. Used primarily with block-style stats (`data-display="block"`) and card grids.

**What breaks without it:** Cards/stats in a row have uneven heights based on their content length, creating a ragged grid.
