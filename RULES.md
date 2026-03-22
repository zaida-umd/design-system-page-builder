# UMD Page Builder — Implementation Rules

Verified against `@universityofmaryland/web-components-library@1.17.18`.

**Companion files:**
- `TEMPLATE.html` — complete page skeleton with all required CSS already assembled
- `REQUIRED-CSS.md` — explains what each CSS rule does and why
- `umd-component-registry.json` — component API reference (slots, attrs, aliases)

This file contains **only implementation rules and gotchas** — things that will silently break if done wrong.

---

## 1. CSS must load before cdn.js

The critical CSS `<style>` block must be parsed before `cdn.js` runs. If the script loads first, elements upgrade before `:defined` rules exist and `container-type` never gets set. All two-column layouts (pathways, card grids) collapse to stacked. The complete CSS is in `TEMPLATE.html` — use it as-is.

Inline the CSS as a `<style>` block, not a `<link>` — relative `<link>` paths fail when opening HTML directly from disk.

**Exception:** `umd-element-nav-item` must use `container-type: normal` — not `inline-size`. See §3 for details.

---

## 2. Page structure — required element order

Every page follows this skeleton:

1. `<umd-element-utility-header>` — global UMD bar, zero-config, never modify
2. `<umd-element-navigation-header>` — site nav, configured per department
3. Page content (heroes, sections, cards, pathways, etc.)
4. `<umd-element-footer>` — site footer

---

## 3. Navigation header

Nav items go inside a `<nav slot="main-navigation">` wrapper — not slotted directly onto the header:

```html
<!-- ✓ Correct -->
<umd-element-navigation-header sticky class="umd-layout-space-horizontal-full">
  <a slot="logo" href="/">Logo</a>
  <nav slot="main-navigation">
    <umd-element-nav-item>
      <a slot="primary-link" href="/about">About</a>
    </umd-element-nav-item>
  </nav>
</umd-element-navigation-header>
```

- `sticky` is a boolean attribute — use `sticky` not `sticky="true"`
- Always add `class="umd-layout-space-horizontal-full"` to the header element
- **Critical CSS exception:** `umd-element-nav-item` must use `container-type: normal`, not `inline-size`. The nav header uses `grid-auto-flow: column` internally — `inline-size` containment prevents the grid from sizing nav items correctly, causing them to collapse and overlap. The override is already in `TEMPLATE.html`:

```css
umd-element-nav-item:defined {
  content-visibility: visible;
  container-type: normal;
  display: block;
}
```

---

## 4. Pathway wrapper rules

### Standard pathway needs a dark section wrapper

The standard pathway (no `data-display`) only themes the **text column** — the image column is always transparent. Without a containing dark background, the image column floats on white.

```html
<!-- ✓ Correct — dark wrapper contains both columns -->
<section style="background: #000;">
  <umd-element-pathway data-theme="dark">...</umd-element-pathway>
</section>

<!-- ✗ Wrong — image column floats on white -->
<umd-element-pathway data-theme="dark">...</umd-element-pathway>
```

### Overlay pathway is self-contained

`data-display="overlay"` fills full width with the image as background. Text panel gets an opaque background from the theme. No wrapper needed.

### Hero pathway exception

`data-display="hero"` uses padding-based layout (not container queries). Works even without the critical CSS.

### Quick reference

| Variant | Dark wrapper? | Critical CSS? |
|---|---|---|
| Standard (no data-display) | ✓ Required | ✓ Required |
| `data-display="overlay"` | No | ✓ Required |
| `data-display="hero"` | No | Not required |
| `data-display="sticky"` | No | ✓ Required |

---

## 5. CTA button — direct child rule

The link or button must be a **direct child** of `umd-element-call-to-action` — no wrapper divs:

```html
<!-- ✓ Correct -->
<umd-element-call-to-action data-display="primary">
  <a href="/apply">Apply Now</a>
</umd-element-call-to-action>

<!-- ✗ Wrong -->
<umd-element-call-to-action data-display="primary">
  <div><a href="/apply">Apply Now</a></div>
</umd-element-call-to-action>
```

When placing CTAs inside an `actions` slot, wrap the CTA(s) in a `<div slot="actions">`:

```html
<div slot="actions">
  <umd-element-call-to-action data-display="primary">
    <a href="/apply">Apply Now</a>
  </umd-element-call-to-action>
</div>
```

---

## 6. Slot rules

- Slot content must be **direct children** of the component element
- Headline slots expect heading elements (`h1`–`h6`)
- Image slots expect `<img>` (not a div wrapping an img)
- The `logo` slot (header + footer) must be `<a>` wrapping `<img>` — not just `<img>`

---

## 7. `data-theme` does NOT cascade

Each component that needs dark theme must have `data-theme` set **individually**. A parent's theme does not cross shadow DOM boundaries into child components.

```html
<!-- ✓ Correct — each component themed independently -->
<umd-element-section-intro-wide data-theme="dark">
  <h2 slot="headline">Our Research</h2>
  <umd-element-call-to-action data-display="secondary" data-theme="dark" slot="actions">
    <a href="/research">Explore All</a>
  </umd-element-call-to-action>
</umd-element-section-intro-wide>

<!-- ✗ Wrong — CTA renders with light styles -->
<umd-element-section-intro-wide data-theme="dark">
  <h2 slot="headline">Our Research</h2>
  <umd-element-call-to-action data-display="secondary" slot="actions">
    <a href="/research">Explore All</a>
  </umd-element-call-to-action>
</umd-element-section-intro-wide>
```

Always audit every child component when applying a dark theme.

---

## 8. Don't invent eyebrows

The `eyebrow` slot is optional on heroes, pathways, cards, and section intros. Only populate it when the source content explicitly provides a label. Never fabricate one to fill space.

```html
<!-- ✓ Correct — no eyebrow in source, don't add one -->
<umd-element-pathway data-theme="dark">
  <h2 slot="headline">Choose Maryland</h2>
  ...
</umd-element-pathway>
```

---

## 9. Stat component — `slot="text"` gotcha

The descriptive label **requires** `slot="text"`. Despite documentation calling it the "default slot", bare unslotted children are silently ignored. Always wrap in a div:

```html
<!-- ✓ Correct -->
<umd-element-stat data-visual-size="large" data-decoration-line>
  <span slot="stat">600+</span>
  <div slot="text"><p>Doctoral degrees conferred annually</p></div>
</umd-element-stat>

<!-- ✗ Wrong — text silently dropped, no error -->
<umd-element-stat data-visual-size="large" data-decoration-line>
  <span slot="stat">600+</span>
  <p>Doctoral degrees conferred annually</p>
</umd-element-stat>
```

---

## 10. Stats layout — max 4 large per row

| Count | Layout |
|---|---|
| 1–4 | Single grid row, `repeat(N, 1fr)` |
| 5 | Row of 3, then row of 2 centered |
| 6 | Two rows of 3 |
| 7 | Row of 4, then row of 3 |
| 8 | Two rows of 4 |

For 5 stats (3+2), center the second row:
```html
<div style="display:grid; grid-template-columns:repeat(3,1fr); gap:48px 32px;">
  <!-- 3 stats -->
</div>
<div style="display:grid; grid-template-columns:repeat(2,1fr); gap:48px 32px; max-width:calc(66.66% + 16px); margin:48px auto 0;">
  <!-- 2 stats centered -->
</div>
```

Block stats (`data-display="block"`) use `umd-layout-grid-child-fill-height` on each stat for equal card heights.

---

## 11. Horizontal spacing — which components get wrapped

**Do NOT wrap** in a horizontal spacing class (these are full-bleed):
- `umd-element-pathway` (all variants)
- `umd-element-hero` (all variants)
- `umd-element-hero-minimal`, `hero-expand`, `hero-logo`, `hero-grid`, `hero-brand-video`
- `umd-layout-image-expand`

**DO wrap** in `.umd-layout-space-horizontal-larger` (or appropriate tier):
- Card grids
- `umd-element-section-intro-wide`
- Stat groups
- Body content blocks

**Navigation header** always gets `class="umd-layout-space-horizontal-full"` on the element itself.

**`umd-element-section-intro`** (centered) constrains its own width — no wrapper needed.

---

## 12. Watermark pattern

The watermark is a CSS utility class on a sibling `div` placed **before** `umd-element-section-intro-wide`, inside a `.umd-layout-space-horizontal-larger` wrapper. Not a component attribute.

```html
<!-- Light watermark -->
<div class="umd-layout-space-horizontal-larger">
  <div class="umd-text-decoration-watermark">
    <span aria-hidden="true" role="presentation">Featured Stories</span>
  </div>
  <umd-element-section-intro-wide>
    <h2 slot="headline">Featured Stories</h2>
  </umd-element-section-intro-wide>
</div>

<!-- Dark watermark -->
<div class="umd-layout-space-horizontal-larger">
  <div class="umd-watermark-dark">
    <span aria-hidden="true" role="presentation">Our Research</span>
  </div>
  <umd-element-section-intro-wide data-theme="dark">
    <h2 slot="headline">Our Research</h2>
  </umd-element-section-intro-wide>
</div>
```

The span text should echo the headline. It is `aria-hidden="true"` and `role="presentation"` — purely decorative.

---

## 13. Image-expand is full-bleed

`umd-layout-image-expand` requires `width: 100%` in critical CSS. Without it, the host collapses to the width of its content slot. Do not wrap in a horizontal spacing class. Use a wrapping `<section>` with `umd-layout-vertical-landing` for spacing:

```html
<section class="umd-layout-vertical-landing">
  <umd-layout-image-expand>
    <div slot="content">...</div>
    <img slot="image" src="/photo.jpg" alt="" />
  </umd-layout-image-expand>
</section>
```

---

## 14. `data-theme="maryland"` behavior

Maryland theme applies a solid red background (#e21833) with white text to the **text column only** (on pathways) or the component body. It does not add any other styling. Avoid for quote/spotlight content where a dark theme is more appropriate.

---

## 15. Registry is the source of truth

Do not re-derive known components from NPM source or Storybook. Use `umd-component-registry.json`. It has been verified directly from NPM package source for version `1.17.18`. Only add new components after source verification — never guess slot or attribute names.
