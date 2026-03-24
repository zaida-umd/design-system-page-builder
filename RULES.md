# UMD Page Builder — Rules

Verified against `@universityofmaryland/web-components-library@1.17.18`.  
Source: NPM package analysis + `beta.umd-staging.com` inspection.

---

## 1. Required files — every page needs both

Every standalone UMD HTML page must load these two files in `<head>`:

```html
<!-- CORRECT order: critical CSS first, then cdn.js -->
<style>
  /* contents of umd-critical.css inlined here */
</style>
<script src="https://unpkg.com/@universityofmaryland/web-components-library@1.17.18/dist/cdn.js"></script>
```

**Critical:** the CSS rules must be parsed before `cdn.js` runs and registers the custom elements. If `cdn.js` loads first, elements upgrade before `:defined` rules exist and `container-type` never gets set. Always inline the critical CSS as a `<style>` block (not a `<link>`) when serving standalone HTML files — a `<link>` to a relative path will fail if the file is opened directly from disk.
- All two-column layouts (pathway standard/overlay/sticky, card grids, etc.) collapse to stacked. Only `data-display="hero"` pathway variants are immune — they use padding-based internal layout rather than container queries.
- Body copy (`p`, `li`) falls back to the browser default sans-serif instead of Interstate.

`umd-critical.css` is derived from the UMD build pipeline's `critical.css`. It provides:
1. `component:defined { container-type: inline-size }` for every element tag — required for shadow DOM `@container` queries to fire.
2. `font-family: "Interstate"` on `:root`, `p`, `li`, and form elements.

---

## 2. Interstate font

Interstate is a **licensed typeface**. The `@font-face` declarations with base64-encoded font data live in UMD's production `critical.css` (build artifact). `umd-critical.css` sets the font-family stack but does not embed the font.

For the font to actually render as Interstate you must either:
- Link UMD's production `critical.css` from your CMS or build output, OR  
- Self-host the Interstate font files and add `@font-face` declarations yourself.

Without the font loaded, the stack falls back to `Helvetica, Arial, Verdana, sans-serif`. All layouts and sizing will still be correct — only the typeface changes.

Font stacks (for reference):
```css
--umd-font-sans:     "Interstate", Helvetica, Arial, Verdana, sans-serif;
--umd-font-serif:    "Crimson Pro", Georgia, serif;
--umd-font-campaign: "Barlow Condensed", Arial Narrow, sans-serif;
```

---

## 3. Page structure — required element order

```html
<!-- 1. Global university header — hardcoded, never modified -->
<umd-element-utility-header></umd-element-utility-header>

<!-- 2. Site navigation header — configurable per department -->
<umd-element-navigation-header sticky>
  <a slot="logo" href="/">...</a>
  <nav slot="main-navigation">
    <umd-element-nav-item>
      <a slot="primary-link" href="/about">About</a>
    </umd-element-nav-item>
  </nav>
</umd-element-navigation-header>

<!-- 3. Page content -->
...

<!-- 4. Footer -->
<umd-element-footer>...</umd-element-footer>
```

`umd-element-utility-header` is self-contained and zero-configurable. Hardcode it on every page. Never modify it.

---

## 4. Navigation header — slot structure

Nav items must be placed inside a `<nav slot="main-navigation">` wrapper, not slotted directly onto the header:

```html
<!-- ✓ Correct -->
<umd-element-navigation-header sticky>
  <a slot="logo" href="/">Logo</a>
  <nav slot="main-navigation">
    <umd-element-nav-item>
      <a slot="primary-link" href="/research">Research</a>
    </umd-element-nav-item>
    <umd-element-nav-item>
      <a slot="primary-link" href="/about">About</a>
    </umd-element-nav-item>
  </nav>
</umd-element-navigation-header>

<!-- ✗ Wrong — slot="nav-item-0" is not a valid slot -->
<umd-element-nav-item slot="nav-item-0">...</umd-element-nav-item>
```

`sticky` is a boolean attribute — use `sticky` not `sticky="true"`.

---

## 5. Pathway usage rules

### Background context is required for non-overlay variants

The standard pathway (`umd-element-pathway` with no `data-display`) renders a two-column layout where only the **text column** gets a theme background. The image column is always transparent. This means:

| Theme | Text column background | Image column background | Page context needed? |
|---|---|---|---|
| (none) | white | transparent | ⚠ Both float on white — broken |
| `dark` | black | transparent | ✓ Wrap in `background: #000` section |
| `maryland` | red (#e21833) | transparent | ✓ Wrap in `background: #000` section |

**Rule:** Standard pathway must only be used when a dark section wrapper (`background: #000` or similar) contains the entire component — so both columns sit within a contained dark field.

```html
<!-- ✓ Correct — dark theme inside dark section -->
<section style="background: #000;">
  <umd-element-pathway data-theme="dark">...</umd-element-pathway>
</section>

<!-- ✗ Wrong — text column floats on white page -->
<umd-element-pathway data-theme="dark">...</umd-element-pathway>
```

### Overlay pathway is self-contained

`data-display="overlay"` fills the full component width with the image as background. The text panel gets an opaque background from the theme. No wrapper needed.

Background panel color by theme:
- No theme → white panel
- `data-theme="dark"` → black panel (recommended for photography)  
- `data-theme="maryland"` → red panel
- `data-theme="light"` → light gray panel

### Hero pathway exception

`data-display="hero"` uses a padding-based internal two-column layout instead of container queries. It renders correctly even **without** `umd-critical.css` — this is why it was the only variant working before the critical CSS was identified.

### Summary

| Variant | Requires wrapper? | Requires critical CSS? |
|---|---|---|
| Standard (no data-display) | ✓ Dark section wrapper | ✓ |
| `data-display="overlay"` | No | ✓ |
| `data-display="hero"` | No | No (padding-based) |
| `data-display="sticky"` | No | ✓ |

---

## 6. CTA button

`umd-element-call-to-action` wraps an `<a>` or `<button>`. The link must be a direct child:

```html
<umd-element-call-to-action data-display="primary">
  <a href="/apply">Apply Now</a>
</umd-element-call-to-action>
```

Valid `data-display` values: `primary`, `secondary`. Omit for default style.

---

## 7. Slots — general rules

- Slot content must be **direct children** of the component element, not nested wrappers (unless the slot description explicitly says to wrap).
- Use the correct element type per slot. Most headline slots expect heading elements (`h1`–`h6`). Most image slots expect `img` (not a `div` wrapping an `img`).
- The `logo` slot in headers and footers must be an `<a>` wrapping an `<img>` — not just an `<img>` or text.

---

## 8. Registry is the source of truth

Do not re-derive known components from NPM source or Storybook. Use the registry JSON. The registry has been verified directly from NPM package source for version `1.17.18`. Only add new components to the registry after verification — never guess slots or attribute names.

---

## 9. Stats layout rules

### Large stats (data-visual-size="large") — max 4 per row

Large stats are wide enough that rows of more than 4 become cramped. The rules are:

| Count | Layout |
|---|---|
| 1–4 | Single grid row, `repeat(N, 1fr)` |
| 5 | Row of 3, then row of 2 centered beneath |
| 6 | Two rows of 3 |
| 7 | Row of 4, then row of 3 |
| 8 | Two rows of 4 |

For the 3+2 case (5 stats), center the second row by constraining its max-width:

```html
<!-- Row 1: 3 stats -->
<div style="display:grid; grid-template-columns:repeat(3,1fr); gap:48px 32px;">
  <umd-element-stat data-visual-size="large" data-decoration-line>...</umd-element-stat>
  <umd-element-stat data-visual-size="large" data-decoration-line>...</umd-element-stat>
  <umd-element-stat data-visual-size="large" data-decoration-line>...</umd-element-stat>
</div>
<!-- Row 2: 2 stats centered (max-width matches 2 of 3 columns) -->
<div style="display:grid; grid-template-columns:repeat(2,1fr); gap:48px 32px; max-width:calc(66.66% + 16px); margin:48px auto 0;">
  <umd-element-stat data-visual-size="large" data-decoration-line>...</umd-element-stat>
  <umd-element-stat data-visual-size="large" data-decoration-line>...</umd-element-stat>
</div>
```

Block stats (`data-display="block"`) follow the same row-count rule but use `umd-layout-grid-child-fill-height` on each stat for equal card heights.

---

## 10. Vertical spacing

The design system provides CSS utility classes for consistent spacing between sections and between items within sections. These classes must be applied in your own `<style>` block — they are not injected by `cdn.js`.

### Landing / full-width pages

**Between sections** — add `umd-layout-vertical-landing` to each `<section>`:

| Breakpoint | Spacing |
|---|---|
| Mobile (default) | 56px `margin-bottom` |
| Tablet (≥768px) | 80px |
| Desktop (≥1024px) | 120px |

**Between items within a section** — add `umd-layout-vertical-landing-child` to child containers:

| Breakpoint | Spacing |
|---|---|
| Mobile (default) | 32px `margin-bottom` |
| Tablet (≥768px) | 40px |
| Desktop (≥1024px) | 48px |

### Interior pages

**Page content area** — add `umd-layout-vertical-interior` for top/bottom page margins:

| Breakpoint | Spacing |
|---|---|
| Mobile + Tablet (default) | 56px `margin-bottom` |
| Desktop (≥1024px) | 80px |

**Between items within a section** — add `umd-layout-vertical-interior-child`:

| All breakpoints | 32px `margin-bottom` |
|---|---|

### CSS to include in your `<style>` block

```css
/* Landing page — between sections */
.umd-layout-vertical-landing           { margin-bottom: 56px; }
@media (min-width: 768px)  { .umd-layout-vertical-landing  { margin-bottom: 80px; } }
@media (min-width: 1024px) { .umd-layout-vertical-landing  { margin-bottom: 120px; } }

/* Landing page — between items within a section */
.umd-layout-vertical-landing-child     { margin-bottom: 32px; }
@media (min-width: 768px)  { .umd-layout-vertical-landing-child { margin-bottom: 40px; } }
@media (min-width: 1024px) { .umd-layout-vertical-landing-child { margin-bottom: 48px; } }

/* Interior page — page content area margins */
.umd-layout-vertical-interior          { margin-bottom: 56px; }
@media (min-width: 1024px) { .umd-layout-vertical-interior { margin-bottom: 80px; } }

/* Interior page — between items within a section */
.umd-layout-vertical-interior-child    { margin-bottom: 32px; }
```

### Usage pattern

```html
<!-- Landing page: each top-level section gets umd-layout-vertical-landing -->
<section class="umd-layout-vertical-landing" style="background:#000;">
  <umd-element-pathway data-theme="dark">...</umd-element-pathway>
</section>

<section class="umd-layout-vertical-landing">
  <div class="page-lock">
    <!-- section intro gets umd-layout-vertical-landing-child -->
    <umd-element-section-intro class="umd-layout-vertical-landing-child">...</umd-element-section-intro>
    <!-- card grid follows -->
    <div class="news-grid">...</div>
  </div>
</section>
```

### Note on pathway sections

Pathway and hero components manage their own internal spacing. When wrapping a pathway in a dark `<section>`, apply `umd-layout-vertical-landing` to the `<section>` element, not to the component itself. The section's `margin-bottom` creates the gap to the next section.

---

## 11. Stat component — slot="text" gotcha

The official documentation describes the descriptive label as the "default slot", implying children with no `slot` attribute. **This is wrong.** The component reads it as a named slot and bare unslotted children are silently ignored.

Always use `slot="text"` for the descriptive label:

```html
<!-- ✓ Correct -->
<umd-element-stat data-visual-size="large" data-decoration-line>
  <span slot="stat">600+</span>
  <div slot="text"><p>Doctoral degrees conferred annually</p></div>
</umd-element-stat>

<!-- ✗ Wrong — text silently dropped -->
<umd-element-stat data-visual-size="large" data-decoration-line>
  <span slot="stat">600+</span>
  <p>Doctoral degrees conferred annually</p>
</umd-element-stat>
```

All three slots:
- `slot="stat"` — the number/value (max 6 chars)
- `slot="text"` — the descriptive label (wrap in a `div`)
- `slot="sub-text"` — attribution/context

---

## 12. Horizontal spacing

The design system provides CSS utility classes for consistent horizontal padding and max-width constraints. These are layout "lock" classes — they center content and apply responsive side padding. They must be defined in your own `<style>` block and applied to host or wrapper elements.

Source: `@universityofmaryland/web-styles-library` → `layout/space/horizontal.js`  
Breakpoints: `tablet.min` = 768px, `highDef.min` = 1200px  
Padding scale: `spacing.md` (24px) → `spacing.2xl` (48px) → `spacing.4xl` (64px)

### Available classes

| Class | max-width | Use for |
|---|---|---|
| `umd-layout-space-horizontal-full` | 100% | Navigation header, full-bleed sections |
| `umd-layout-space-horizontal-larger` | 1600px | Wide landing page content |
| `umd-layout-space-horizontal-large` | 1400px | Standard landing page content |
| `umd-layout-space-horizontal-normal` | 1280px | Body content, interior pages |
| `umd-layout-space-horizontal-small` | 992px | Narrow content columns |
| `umd-layout-space-horizontal-smallest` | 800px | Article body, forms |

### CSS to include in your `<style>` block

All classes share the same padding scale — only `max-width` differs:

```css
/* Shared padding behaviour — apply to all variants */
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
.umd-layout-space-horizontal-full    { max-width: 100%;    }
.umd-layout-space-horizontal-larger  { max-width: 1600px;  }
.umd-layout-space-horizontal-large   { max-width: 1400px;  }
.umd-layout-space-horizontal-normal  { max-width: 1280px;  }
.umd-layout-space-horizontal-small   { max-width: 992px;   }
.umd-layout-space-horizontal-smallest{ max-width: 800px;   }
```

### Navigation header requires `umd-layout-space-horizontal-full`

The navigation header must carry this class on its host element so its internal lock spans the full viewport width with consistent side padding:

```html
<!-- ✓ Correct -->
<umd-element-navigation-header sticky class="umd-layout-space-horizontal-full">
  ...
</umd-element-navigation-header>

<!-- ✗ Wrong — header ignores page horizontal rhythm -->
<umd-element-navigation-header sticky>
  ...
</umd-element-navigation-header>
```

### Content grids and page-lock wrappers

For card grids and body content that should not span full viewport width, apply the appropriate class to a wrapper `<div>` rather than the component itself:

```html
<div class="umd-layout-space-horizontal-larger">
  <umd-element-section-intro-wide>...</umd-element-section-intro-wide>
  <div class="news-grid">
    <umd-element-card-overlay>...</umd-element-card-overlay>
    <umd-element-card-overlay>...</umd-element-card-overlay>
    <umd-element-card-overlay>...</umd-element-card-overlay>
  </div>
</div>
```

Pathway and hero components manage their own internal horizontal spacing — do not wrap them in a horizontal spacing class.

### Extra properties required when wrapping `umd-element-section-intro-wide`

When `.umd-layout-space-horizontal-larger` wraps `umd-element-section-intro-wide`, two additional properties are required beyond the standard padding/max-width:

```css
.umd-layout-space-horizontal-larger {
  /* ...standard padding rules... */
  position: relative;       /* required — watermark span is position:absolute */
  container-type: inline-size; /* required — fires the component's internal container
                                  query that puts headline and CTA in a flex row at 500px+ */
  isolation: isolate;       /* required when watermark is present — creates a local
                                  stacking context so z-index:-1 on the watermark goes
                                  behind the headline text, not behind the page background */
}
```

`section-intro` (centered variant, `umd-element-section-intro`) constrains its own width internally and does not need a horizontal spacing wrapper.

---

## 13. Don't invent eyebrows

The `eyebrow` slot is optional on pathways, heroes, cards, and section intros. Only populate it when the source content explicitly includes a label or category above the headline. Do not invent one to fill the space or add context — an empty eyebrow slot is correct and intentional.

```html
<!-- ✓ Correct — no eyebrow in source, don't add one -->
<umd-element-pathway data-theme="dark">
  <h2 slot="headline">Choose Maryland</h2>
  ...
</umd-element-pathway>

<!-- ✗ Wrong — eyebrow fabricated to add context -->
<umd-element-pathway data-theme="dark">
  <p slot="eyebrow">Graduate Studies at Maryland</p>
  <h2 slot="headline">Choose Maryland</h2>
  ...
</umd-element-pathway>
```

---

## 14. `data-theme` does not cascade

Each component that needs dark (or any) theme styling must have `data-theme` set on it **individually**. A parent component's theme does not cascade into child components — even when a child is slotted inside a parent that has `data-theme="dark"`.

```html
<!-- ✓ Correct — each component gets its own data-theme -->
<umd-element-section-intro-wide data-theme="dark">
  <h2 slot="headline">Our Research</h2>
  <umd-element-call-to-action data-display="secondary" data-theme="dark" slot="actions">
    <a href="/research">Explore All</a>
  </umd-element-call-to-action>
</umd-element-section-intro-wide>

<!-- ✗ Wrong — CTA still renders with light styles -->
<umd-element-section-intro-wide data-theme="dark">
  <h2 slot="headline">Our Research</h2>
  <umd-element-call-to-action data-display="secondary" slot="actions">
    <a href="/research">Explore All</a>
  </umd-element-call-to-action>
</umd-element-section-intro-wide>
```

This applies to all nested component combinations: pathway + CTA, section-intro + CTA, card + CTA, etc. Always audit every child component when applying a dark theme.

---

## 15. Watermark pattern (`umd-text-decoration-watermark`)

The watermark is **not a component attribute** — it is a CSS utility class applied to a sibling `div` placed immediately before `umd-element-section-intro-wide`, inside the `.umd-layout-space-horizontal-larger` wrapper.

The span text should echo the headline. It is `aria-hidden="true"` and `role="presentation"` — purely decorative. The scroll-driven entrance animation fires automatically from the class.

### Light variant — `.umd-text-decoration-watermark`

```html
<div class="umd-layout-space-horizontal-larger">
  <div class="umd-text-decoration-watermark">
    <span aria-hidden="true" role="presentation">Featured Stories</span>
  </div>
  <umd-element-section-intro-wide>
    <h2 slot="headline">Featured Stories</h2>
    <umd-element-call-to-action data-display="secondary" slot="actions">
      <a href="/news">View All News</a>
    </umd-element-call-to-action>
  </umd-element-section-intro-wide>
</div>
```

### Dark variant — `.umd-watermark-dark`

```html
<div class="umd-layout-space-horizontal-larger">
  <div class="umd-watermark-dark">
    <span aria-hidden="true" role="presentation">Our Research</span>
  </div>
  <umd-element-section-intro-wide data-theme="dark">
    <h2 slot="headline">Our Research</h2>
    <umd-element-call-to-action data-display="secondary" data-theme="dark" slot="actions">
      <a href="/research">Explore All</a>
    </umd-element-call-to-action>
  </umd-element-section-intro-wide>
</div>
```

Note: `umd-element-call-to-action` requires its own `data-theme="dark"` — see rule 14.

### Required CSS (add to your `<style>` block)

```css
/* Base styles — all three classes */
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

**Critical:** All three watermark classes (`.umd-text-decoration-watermark`, `.umd-watermark`, `.umd-watermark-dark`) must be included in the base `:is()` selector. Omitting `.umd-watermark-dark` from the base selector means the dark variant span gets none of the positioning or font styles.

---

## 16. Card overlay — `type="image"` is required for image backgrounds

`umd-element-card-overlay` has two visual modes: solid-color background (default) and image background. The image background variant requires the deprecated `type="image"` attribute — without it, `slot="image"` is silently ignored and the component renders as a solid-color card.

```html
<!-- ✓ Correct — image variant with type="image" -->
<umd-element-card-overlay type="image">
  <img slot="image" src="/news.jpg" alt="" />
  <h3 slot="headline"><a href="/news/story">Headline</a></h3>
  <p slot="eyebrow">Category</p>
</umd-element-card-overlay>

<!-- ✗ Wrong — image silently ignored, renders as solid-color card -->
<umd-element-card-overlay>
  <img slot="image" src="/news.jpg" alt="" />
  <h3 slot="headline"><a href="/news/story">Headline</a></h3>
</umd-element-card-overlay>
```

Note: This uses the deprecated `type` attribute, not `data-type`. The attribute name is confirmed from cdn.js source.

---

## 17. Image expand (`umd-layout-image-expand`)

### Text must be explicitly white

The image-expand component does **not** support `data-theme`. It has no internal text color styling — the shadow DOM text-lock container defaults to `color: rgb(0, 0, 0)` (black). Since content overlays the image with a dark semi-transparent overlay (`rgba(0,0,0,0.65)`), black text is invisible.

**All text in the `content` slot must be explicitly set to white**, either via inline styles or utility classes:

```html
<!-- ✓ Correct — explicit white text -->
<umd-layout-image-expand>
  <div slot="content">
    <div>
      <h2 style="color: white;">Section Heading</h2>
      <p style="color: white;">Supporting text for this section.</p>
    </div>
  </div>
  <img slot="image" src="/feature.jpg" alt="" />
</umd-layout-image-expand>

<!-- ✗ Wrong — text renders black, invisible on dark overlay -->
<umd-layout-image-expand>
  <div slot="content">
    <div>
      <h2>Section Heading</h2>
      <p>Supporting text.</p>
    </div>
  </div>
  <img slot="image" src="/feature.jpg" alt="" />
</umd-layout-image-expand>
```

### Dark section wrapper required

Always wrap `umd-layout-image-expand` in a section with `background: #000` (or use the `umd-layout-background-full-dark` class). The image starts small and expands — the black background fills the gaps around the image during the scroll animation.

```html
<!-- ✓ Correct — dark wrapper provides visual continuity -->
<section style="background: #000;">
  <umd-layout-image-expand>
    ...
  </umd-layout-image-expand>
</section>
```

### Full-bleed — no horizontal spacing, no max-width on host

The component is full-bleed (same rule as pathway and hero — see §12). Do **not** wrap in a horizontal spacing class. The shadow DOM applies its own internal `max-width: 1600px` on the text-lock container, with `margin: 0 auto` and responsive padding (`24px` → `48px` → `64px`). Setting `max-width` on the host will break the full-bleed image animation.

### Critical CSS for the host

The host element requires `width: 100%` in critical CSS. Without it, the host collapses to content width and the 100vw image animation breaks.

```css
umd-layout-image-expand:not(:defined) {
  content-visibility: hidden;
}
umd-layout-image-expand {
  display: block;
  container-type: inline-size;
  width: 100%;
}
```

### Summary of gotchas

| Issue | Symptom | Fix |
|---|---|---|
| No `color: white` on text | Text invisible (black on dark overlay) | Add `style="color:white"` to every text element in content slot |
| No dark section wrapper | White gaps around image during scroll | Wrap in `<section style="background:#000;">` |
| Missing `width: 100%` | Component collapses to narrow strip | Add to critical CSS (see GROUP 3 in TEMPLATE.html) |
| `max-width` on host | Image animation clipped | Remove — shadow DOM handles text-lock max-width internally |
| No `data-theme` attribute | (N/A — attribute does not exist) | Use inline `color: white` instead |
