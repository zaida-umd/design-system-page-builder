# UMD Page Builder — Rules

Verified against `@universityofmaryland/web-components-library@1.18.2`.  
Source: NPM package analysis + `beta.umd-staging.com` inspection.

---

## 1. Required files — every page needs both

Every standalone UMD HTML page must load these two files in `<head>`:

```html
<!-- CORRECT order: critical CSS first, then cdn.js -->
<style>
  /* contents of styles/critical.css inlined here */
</style>
<script src="https://unpkg.com/@universityofmaryland/web-components-library@1.18.2/dist/cdn.js"></script>
```

The canonical CSS is in **`styles/critical.css`** — the single source of truth. `TEMPLATE.html` inlines it verbatim. When updating CSS rules, edit `styles/critical.css` first, then copy changes to `TEMPLATE.html`.

**Critical:** the CSS rules must be parsed before `cdn.js` runs and registers the custom elements. If `cdn.js` loads first, elements upgrade before `:defined` rules exist and `container-type` never gets set. Always inline the critical CSS as a `<style>` block (not a `<link>`) when serving standalone HTML files — a `<link>` to a relative path will fail if the file is opened directly from disk.
- All two-column layouts (pathway standard/overlay/sticky, card grids, etc.) collapse to stacked. Only `data-display="hero"` pathway variants are immune — they use padding-based internal layout rather than container queries.
- Body copy (`p`, `li`) falls back to the browser default sans-serif instead of Interstate.

`styles/critical.css` provides component registration, fonts, vertical/horizontal spacing, watermark, layout patterns, typography, rich text, interior page layout, and utility classes. See REQUIRED-CSS.md for explanations of what each section does and why it's needed.

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

### Pathway CTAs — slot, display, and count

CTAs belong **inside the pathway**, in `slot="actions"` — never as a sibling element rendered after the pathway. The pathway lays out actions as part of its text-column composition; siblings break the visual hierarchy and don't pick up the pathway's theme.

**Allowed `data-display` values:** `primary`, `secondary` (omit for default). **Do not use `data-display="outline"` in pathways.** The outline CTA is reserved for Maryland/red overlay variants and has a hard-coded shadow-DOM `max-width: 380px` that fights pathway layouts (see [OVERRIDES.md](OVERRIDES.md) — `.umd-action-outline-block` is the page-built workaround when an outline-style block is needed elsewhere).

**Maximum count:** **1 primary + up to 5 secondary** in a single pathway action slot. Beyond that, the action stack visually dominates the body copy.

**When approaching 5 secondaries** — switch to the shell utility-nav pattern (separator-divided links) instead of stacking five secondary CTA components. Use `.umd-shell-utility-item` / `.umd-shell-utility-actions` from `styles/critical.css` §14:

```html
<umd-element-pathway>
  <img slot="image" src="…" alt="…" />
  <h2 slot="headline">Living-Learning Programs</h2>
  <div slot="text"><p>About half of UMD's first-year students join a living-learning program.</p></div>
  <div slot="actions">
    <!-- 1 primary -->
    <umd-element-call-to-action data-display="primary">
      <a href="/learn-more">Learn About Programs</a>
    </umd-element-call-to-action>
    <!-- Tertiary row — utility-nav-style separators instead of 5 stacked secondaries -->
    <div style="display:flex; flex-wrap:wrap; margin-top:16px;">
      <div class="umd-shell-utility-item">
        <div class="umd-shell-utility-actions"><a href="/honors">Honors</a></div>
      </div>
      <div class="umd-shell-utility-item">
        <div class="umd-shell-utility-actions"><a href="/scholars">Scholars</a></div>
      </div>
      <div class="umd-shell-utility-item">
        <div class="umd-shell-utility-actions"><a href="/global">Global Communities</a></div>
      </div>
      <div class="umd-shell-utility-item">
        <div class="umd-shell-utility-actions"><a href="/cs">CS Connect</a></div>
      </div>
      <div class="umd-shell-utility-item">
        <div class="umd-shell-utility-actions"><a href="/all">All LLPs</a></div>
      </div>
    </div>
  </div>
</umd-element-pathway>
```

The `.umd-shell-utility-item` selector is intentionally not scoped to the navigation header so it can be reused in pathway, banner-promo, and section-intro action slots.

### `umd-element-pathway-highlight` requires substantive text content

`umd-element-pathway-highlight` is a two-column component: a text column on the left and a pull-quote column on the right. The `text` slot must contain real, substantive body copy — not just a restatement of the quote. If the source content is only a quote with attribution and no accompanying text, use `umd-element-quote` instead.

```html
<!-- ✓ Correct — real body copy in text slot, quote supplements it -->
<umd-element-pathway-highlight>
  <h2 slot="headline">A Message from Our Board Chair</h2>
  <div slot="text">
    <p>Albert Carey has led the foundation for over a decade, guiding strategy and donor engagement across the university's most ambitious initiatives.</p>
  </div>
  <p slot="highlight">I invite you to support past, present and future Terps.</p>
  <p slot="highlight-attribution">— Albert P. Carey '74</p>
</umd-element-pathway-highlight>

<!-- ✗ Wrong — no real text, quote is the only content -->
<umd-element-pathway-highlight>
  <h2 slot="headline">Albert P. Carey '74</h2>
  <p slot="highlight">I invite you to support past, present and future Terps.</p>
  <p slot="highlight-attribution">— Albert P. Carey '74</p>
</umd-element-pathway-highlight>

<!-- ✓ Correct fallback — quote-only content belongs here -->
<umd-element-quote>
  <p slot="quote">I invite you to support past, present and future Terps.</p>
  <p slot="attribution">Albert P. Carey '74</p>
</umd-element-quote>
```

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

Do not re-derive known components from NPM source or Storybook. Use the registry JSON. The registry has been verified directly from NPM package source for version `1.18.2`. Only add new components to the registry after verification — never guess slots or attribute names.

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

### CSS

All vertical spacing rules are defined in `styles/critical.css` — section 3. They are already included in the TEMPLATE.html `<style>` block.

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

### Section intro → content grid spacing (48px desktop)

A section intro or section header **always** needs `umd-layout-vertical-landing-child` between it and the content grid below it. This class delivers the standard child gap: 32px mobile → 40px tablet → **48px desktop**.

- For `umd-element-section-intro`: add the class directly to the element.
- For `umd-element-section-intro-wide`: wrap it in a `<div class="umd-layout-vertical-landing-child">` (do not add directly to the component — the wrapper approach avoids interfering with internal watermark positioning).

```html
<!-- section-intro: class directly on the element -->
<umd-element-section-intro class="umd-layout-vertical-landing-child">
  <h2 slot="headline">Our Programs</h2>
</umd-element-section-intro>
<div class="card-grid">...</div>

<!-- section-intro-wide: wrapper div carries the spacing class -->
<div class="umd-layout-vertical-landing-child">
  <umd-element-section-intro-wide>
    <h2 slot="headline">Latest News</h2>
  </umd-element-section-intro-wide>
</div>
<umd-feed-news data-token="..."></umd-feed-news>
```

This rule applies whether the content that follows is a card grid, a feed component (`umd-feed-news`, `umd-feed-news-list`, `umd-feed-news-featured`), CTA buttons, or any other content block.

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

### CSS

All horizontal spacing rules are defined in `styles/critical.css` — section 4. They are already included in the TEMPLATE.html `<style>` block.

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

### Carousel and banner-promo — lock matrix

| Component | Wrap in lock? | Recommended lock |
|---|---|---|
| `umd-element-carousel-cards` | ✗ No | Component is full-bleed and provides its own black background + internal lock. Wrapping in a horizontal lock breaks the bleed. |
| `umd-element-carousel-thumbnail` | ✓ Yes | `umd-layout-space-horizontal-larger` (1600px) |
| `umd-element-carousel-image` / `-image-wide` / `-multiple-image` | ✓ Yes | `umd-layout-space-horizontal-larger` (1600px) |
| `umd-element-carousel` (standard) | ✓ Yes | `umd-layout-space-horizontal-larger` (1600px) |
| `umd-element-banner-promo` | ✓ Yes | `umd-layout-space-horizontal-larger` (1600px) |

```html
<!-- ✓ Card carousel — full-bleed, no wrapper -->
<section class="umd-layout-vertical-landing">
  <umd-element-carousel-cards>
    <h2 slot="headline">Resources</h2>
    <div slot="cards">…</div>
  </umd-element-carousel-cards>
</section>

<!-- ✓ Thumbnail carousel — wrapped in larger lock -->
<section class="umd-layout-vertical-landing">
  <div class="umd-layout-space-horizontal-larger">
    <umd-element-carousel-thumbnail>…</umd-element-carousel-thumbnail>
  </div>
</section>

<!-- ✓ Banner-promo — wrapped in larger lock -->
<section class="umd-layout-vertical-landing">
  <div class="umd-layout-space-horizontal-larger">
    <umd-element-banner-promo>…</umd-element-banner-promo>
  </div>
</section>
```

### Quote uses `umd-layout-space-horizontal-normal`

`umd-element-quote` is not full-bleed. Wrap it in `.umd-layout-space-horizontal-normal` (1280px) to constrain its width and maintain consistent page gutters:

```html
<div class="umd-layout-space-horizontal-normal">
  <umd-element-quote>
    <p slot="quote">Quote text here.</p>
    <p slot="attribution">Person Name, Title</p>
  </umd-element-quote>
</div>
```

### Extra properties required when wrapping `umd-element-section-intro-wide`

When `.umd-layout-space-horizontal-larger` wraps `umd-element-section-intro-wide`, three additional properties are required: `position: relative` (watermark span is `position:absolute`), `container-type: inline-size` (fires the component's internal `@container` query), and `isolation: isolate` (creates a local stacking context for watermark `z-index`). These are already defined in `styles/critical.css` — section 6.

`section-intro` (centered variant, `umd-element-section-intro`) constrains its own width internally and does not need a horizontal spacing wrapper.

---

## 13. Don't invent eyebrows — and keep them short

The `eyebrow` slot is optional on pathways, heroes, cards, and section intros. Only populate it when the source content explicitly includes a label or category above the headline. Do not invent one to fill the space or add context — an empty eyebrow slot is correct and intentional.

**Character limit: 16 characters maximum.** Eyebrows are visual labels — short category tags, not sentences. If the natural label exceeds 16 characters, either abbreviate it or omit the eyebrow entirely.

```html
<!-- ✓ Correct — no eyebrow in source, don't add one -->
<umd-element-pathway data-theme="dark">
  <h2 slot="headline">Choose Maryland</h2>
  ...
</umd-element-pathway>

<!-- ✓ Correct — short label from source content -->
<umd-element-hero>
  <p slot="eyebrow">Graduate School</p>  <!-- 14 chars ✓ -->
  <h1 slot="headline">Apply Today</h1>
</umd-element-hero>

<!-- ✗ Wrong — eyebrow fabricated to add context -->
<umd-element-pathway data-theme="dark">
  <p slot="eyebrow">Graduate Studies at Maryland</p>
  <h2 slot="headline">Choose Maryland</h2>
  ...
</umd-element-pathway>

<!-- ✗ Wrong — eyebrow too long (>16 chars) -->
<umd-element-hero>
  <p slot="eyebrow">Clark School of Engineering</p>  <!-- 26 chars ✗ -->
  <h1 slot="headline">Advancing the Future</h1>
</umd-element-hero>
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

### CSS

All watermark rules are defined in `styles/critical.css` — section 5. They are already included in the TEMPLATE.html `<style>` block.

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

### Text must be explicitly white (raw HTML content)

The image-expand component does **not** support `data-theme`. It has no internal text color styling — the shadow DOM text-lock container defaults to `color: rgb(0, 0, 0)` (black). Since content overlays the image with a dark semi-transparent overlay (`rgba(0,0,0,0.65)`), black text is invisible.

**When placing raw HTML in the `content` slot, all text must be explicitly set to white**, either via inline styles or utility classes:

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

### Placing a quote inside image-expand — use `data-visual-transparent="true"`

When `umd-element-quote` is placed in the `content` slot, add `data-visual-transparent="true"` to the quote component. This removes the quote's opaque background card so the image shows through. The quote's `data-theme="dark"` then handles all text color internally — no `color: white` inline styles needed on the slot content.

Also constrain the quote panel width and align it using utility classes directly on `div[slot="content"]` — the shadow DOM's text-lock is full-width by default. Use these classes on the slot element itself (not a child wrapper). The utility classes (`.max-w-[480px]`, `.w-full`, `.block`, `.mr-auto`) are defined in `styles/critical.css` — section 12 and already included in the TEMPLATE.html `<style>` block.

```html
<!-- ✓ Correct — transparent quote, constrained and left-aligned -->
<umd-layout-image-expand>
  <div slot="content" class="block max-w-[480px] w-full mr-auto">
    <umd-element-quote data-display="featured" data-theme="dark" data-visual-transparent="true">
      <p slot="quote">Quote text here.</p>
      <p slot="attribution">Person Name</p>
      <p slot="attribution-sub-text">Title, Department</p>
    </umd-element-quote>
  </div>
  <img slot="image" src="/feature.jpg" alt="" />
</umd-layout-image-expand>

<!-- ✗ Wrong — inline styles on a child wrapper div instead of the slot element -->
<div slot="content">
  <div style="display: block; width: 100%; max-width: 480px; margin-right: auto;">
    ...
  </div>
</div>

<!-- ✗ Wrong — opaque card blocks the image -->
<umd-element-quote data-display="featured" data-theme="dark">...</umd-element-quote>
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

The host element requires `width: 100%` in critical CSS. Without it, the host collapses to content width and the 100vw image animation breaks. This is already defined in `styles/critical.css` — section 1, GROUP 3.

### Summary of gotchas

| Issue | Symptom | Fix |
|---|---|---|
| No `color: white` on raw text | Text invisible (black on dark overlay) | Add `style="color:white"` to every text element in content slot |
| Quote has opaque background | Background card blocks image | Add `data-visual-transparent="true"` to `umd-element-quote` |
| Quote fills full width | Quote panel too wide, poor composition | Add `max-width: 480px` + `margin-left/right: auto` on `div[slot="content"]` |
| No dark section wrapper | White gaps around image during scroll | Wrap in `<section style="background:#000;">` |
| Missing `width: 100%` | Component collapses to narrow strip | Add to critical CSS (see GROUP 3 in TEMPLATE.html) |
| `max-width` on host | Image animation clipped | Remove — shadow DOM handles text-lock max-width internally |
| No `data-theme` attribute | (N/A — attribute does not exist) | Use `data-visual-transparent="true"` + `data-theme="dark"` on quote instead |

---

## 18. Rich text advanced pattern (`umd-text-rich-advanced`)

`umd-text-rich-advanced` is a **CSS class** (not a component). It creates a styled content area for editorial copy: 18px body text, 1.5em line height, and animated red-underline link hover. The dark variant is `umd-text-rich-advanced-dark` — a separate class, not an attribute.

Full HTML examples, CSS definitions, and all supporting layout classes are in **LAYOUT-PATTERNS.md**.

### Key gotchas

**Dark backgrounds require the `-dark` class variant:**

```html
<!-- ✓ Correct on dark background -->
<div class="umd-text-rich-advanced-dark">...</div>

<!-- ✗ Wrong — links render black, invisible on dark -->
<div class="umd-text-rich-advanced">...</div>
```

**Inline typography on dark backgrounds requires `text-white`:**

Inline headline classes (`umd-sans-large`, `umd-sans-larger-bold`, `umd-sans-extralarge-bold`) output black text by default. On dark backgrounds, add `text-white` to force white. Define `.text-white { color: #ffffff; }` in your `<style>` block.

```html
<!-- ✓ Correct -->
<p class="text-white umd-sans-larger-bold">Inline headline</p>

<!-- ✗ Wrong — black text on black background -->
<p class="umd-sans-larger-bold">Inline headline</p>
```

**Inline typography uses `<p>` not heading tags:**

Inline headline elements inside `umd-text-rich-advanced` are styled `<p>` elements, not `<h2>` etc. Heading tags carry semantic weight and should only be used for the section headline above the grid.

**The lock for these sections is `umd-layout-space-horizontal-small` (992px):**

These rich text sections use the 992px lock, not the 1280px normal lock. See §12 for the full CSS.

**CTAs inside rich text wrap in `umd-layout-grid-inline-tablet-rows`:**

Do not place `umd-element-call-to-action` directly in the rich text div without a wrapper. The `umd-layout-grid-inline-tablet-rows` wrapper handles stacking on mobile and inline flex at tablet+. Each CTA still needs its own `data-theme="dark"` on dark backgrounds (theme does not cascade — see §14).

---

## 19. No vertical spacing between adjacent dark sections

`umd-layout-vertical-landing` adds `margin-bottom` to create a gap to the next section. When the page background is white, this gap shows as white space. When two consecutive sections are both dark (e.g. a dark hero followed by a `umd-layout-background-full-dark` section), that white margin punches a visible gap between them.

**Rule:** Remove `umd-layout-vertical-landing` from a section when the section immediately following it is dark.

```html
<!-- ✓ Correct — dark hero flows flush into dark rich text section -->
<section>
  <umd-element-hero data-display="overlay" data-theme="dark">...</umd-element-hero>
</section>

<section class="umd-layout-background-full-dark umd-layout-vertical-landing">
  ...
</section>

<!-- The dark section itself keeps umd-layout-vertical-landing for the gap
     after it, before the next (non-dark) section. -->

<!-- ✗ Wrong — margin-bottom on hero section creates white gap -->
<section class="umd-layout-vertical-landing">
  <umd-element-hero data-display="overlay" data-theme="dark">...</umd-element-hero>
</section>

<section class="umd-layout-background-full-dark umd-layout-vertical-landing">
  ...
</section>
```

This applies to any dark-to-dark transition: hero → dark section, dark section → dark section, dark pathway → dark section, etc. The section that provides spacing is always the one that comes **before** the next non-dark section — keep `umd-layout-vertical-landing` on that one.

---

## 20. Sticky columns — slot content patterns

`umd-element-sticky-columns` is a layout container. The component itself has no opinions about how slot content is styled — you are responsible for applying the correct UMD typography and layout classes inside each slot.

### Sticky column (left — sticks while user scrolls)

Use the following pattern, verified against umd.edu production markup:

```html
<div slot="sticky-column">
  <h2 class="umd-sans-largest-uppercase mb-md">Section Heading</h2>
  <div class="umd-text-rich-advanced mb-sm">
    <p>Supporting body copy at 18px with 1.5em line height.</p>
  </div>
  <div class="umd-layout-grid-inline-tablet-rows">
    <umd-element-call-to-action data-display="secondary">
      <a href="/page">Learn More</a>
    </umd-element-call-to-action>
  </div>
</div>
```

- `umd-sans-largest-uppercase` — 800-weight uppercase heading, scales from 32px → 44px
- `mb-md` — 24px bottom margin between heading and body copy
- `umd-text-rich-advanced` — 18px body copy with animated red underline links
- `mb-sm` — 16px bottom margin between body copy and CTA
- `umd-layout-grid-inline-tablet-rows` — stacks CTA(s) on mobile, inline flex at 650px+

### Static column (right — scrolls normally)

Wrap content in `umd-layout-grid-gap-stacked` — a single-column grid with 24px gap. Do **not** use a custom CSS grid. For stats, use `data-animation="offset"` on each `umd-element-stat`:

```html
<div slot="static-column">
  <div class="umd-layout-grid-gap-stacked">
    <umd-element-stat data-visual-size="large" data-decoration-line data-animation="offset">
      <span slot="stat">44k</span>
      <div slot="text"><p>Combined graduates and undergraduates</p></div>
    </umd-element-stat>
    <umd-element-stat data-visual-size="large" data-decoration-line data-animation="offset">
      <span slot="stat">400k</span>
      <div slot="text"><p>Alumni around the world</p></div>
    </umd-element-stat>
  </div>
</div>
```

- `umd-layout-grid-gap-stacked` — `display: grid; grid-template-columns: 1fr; gap: 24px` — items stack vertically
- `data-animation="offset"` — scroll-triggered entrance animation on each stat

### CSS

All sticky columns utility classes (`.umd-layout-grid-gap-stacked`, `.umd-sans-largest-uppercase`, `.mb-md`, `.mb-sm`) are defined in `styles/critical.css` — sections 8, 9, and 13. They are already included in the TEMPLATE.html `<style>` block.

### Host attributes

Always apply the horizontal spacing class and sticky offset on the host element:

```html
<umd-element-sticky-columns
  class="umd-layout-space-horizontal-larger"
  data-layout-position="100px">
```

- `class="umd-layout-space-horizontal-larger"` — page gutters (1600px max-width)
- `data-layout-position="100px"` — sticky top offset; set to match your sticky nav height so the sticky column clears it when scrolling

---

## 21. Interior page layout

Interior pages are distinct from landing pages in structure, available components, spacing classes, and critical CSS requirements. All rules in this section are verified from the production UMD.edu stylesheet and HTML.

---

### Critical CSS — interior page additions

All interior page CSS is now included in `styles/critical.css` and the TEMPLATE.html `<style>` block. No additional CSS is needed for interior pages beyond what the template already provides. The relevant sections in `styles/critical.css` are:

- **Section 1** — Component registration: `umd-element-nav-slider`, `umd-element-media-inline`, and `umd-element-breadcrumb` are in GROUP 2
- **Section 3** — Vertical spacing: interior spacing aliases (`.umd-layout-space-vertical-interior*` and `.umd-layout-vertical-interior*`)
- **Section 9** — Typography: `.umd-sans-larger-bold`, `.text-black`
- **Section 10** — Rich text: `.umd-text-rich-advanced` (light and dark variants)
- **Section 11** — Interior layout: `.umd-layout-space-columns-left`, `.max-w-[800px]`

---

### Page HTML skeleton

The correct element order for an interior page. Note that the breadcrumb and the columns layout each have their **own** `umd-layout-space-horizontal-larger` wrapper — they are not nested inside a shared outer div.

```html
<!-- Full-width: always outside any wrapper -->
<umd-element-navigation-utility data-alert-off="true" ...></umd-element-navigation-utility>
<umd-element-utility-header></umd-element-utility-header>
<umd-element-navigation-header sticky class="umd-layout-space-horizontal-full">...</umd-element-navigation-header>

<!-- Hero: full-width, no spacing class on <section> -->
<section>
  <umd-element-hero data-layout-height="small">...</umd-element-hero>
</section>

<!-- Breadcrumb: own horizontal wrapper + vertical spacing -->
<div class="umd-layout-space-horizontal-larger umd-layout-space-vertical-interior">
  <umd-element-breadcrumb>
    <div slot="paths">
      <a href="/" aria-label="Return Home"><span aria-hidden="true">Home</span></a>
      <a href="/section"><span>Section Name</span></a>
      <p aria-label="Current Page"><span>Current Page Title</span></p>
    </div>
  </umd-element-breadcrumb>
</div>

<!-- Columns layout: own horizontal wrapper -->
<div class="umd-layout-space-horizontal-larger">
  <div class="umd-layout-space-columns-left">
    <div id="umd-shell-sidebar-container">
      <!-- umd-element-nav-slider (optional) -->
    </div>
    <div id="umd-shell-content" class="max-w-[800px]">
      <!-- content sections -->
    </div>
  </div>
</div>

<footer>
  <umd-element-footer>...</umd-element-footer>
</footer>
```

---

### Heroes available on interior pages

Two hero options are used on interior pages:

**1. Background hero — small (`umd-element-hero`)**

Standard background hero with `data-layout-height="small"`. Available in two text alignments (see §22 — standard/background is the default, not overlay):

| Variant | Attributes |
|---|---|
| Left text (default) | `data-layout-height="small"` |
| Centered text | `data-layout-height="small" data-layout-text="center"` |

The `data-display="overlay"` attribute is an **explicit design choice** for the overlay variant. Do not add it to interior page heroes unless specifically requested.

**2. Minimal hero (`umd-element-hero-minimal`)**

No background image required. Three theme states for interior use:

| Variant | Attribute |
|---|---|
| No background (default) | *(omit `data-theme`)* |
| Light background | `data-theme="light"` |
| Dark background | `data-theme="dark"` |

> `data-theme="maryland"` (red background) is available but **not typically used** on interior pages.

All full-height heroes (`hero-expand`, `hero-logo`, `hero-grid`, `hero-brand-video`) and non-small standard hero variants are **landing-page only** — do not use on interior pages.

---

### Breadcrumb

Always use `umd-element-breadcrumb` — never a hand-coded `<nav>` or `<ol>`. Place it after the hero, before the columns layout, in its own wrapper div carrying both the horizontal lock and the vertical spacing class. The component handles all separator, link, and current-page styling internally.

```html
<div class="umd-layout-space-horizontal-larger umd-layout-space-vertical-interior">
  <umd-element-breadcrumb>
    <div slot="paths">
      <a href="/" aria-label="Return Home"><span aria-hidden="true">Home</span></a>
      <a href="/about"><span>About</span></a>
      <p aria-label="Current Page"><span>Traditions of the Past</span></p>
    </div>
  </umd-element-breadcrumb>
</div>
```

Rules for `slot="paths"` content:
- First link: `<a href="/" aria-label="Return Home"><span aria-hidden="true">Home</span></a>`
- Intermediate links: `<a href="..."><span>Label</span></a>`
- Current page: `<p aria-label="Current Page"><span>Label</span></p>` (not a link)

---

### Sidebar + content column layout

Interior pages that include a left nav use **`umd-layout-space-columns-left`** — a production UMD layout class. Do **not** write a custom CSS grid. This class is not in `cdn.js` — it must be defined in the page's critical CSS (see above).

| Breakpoint | Behaviour |
|---|---|
| <768px | Single column, sidebar hidden |
| 768px–1023px | Flex row, sidebar hidden (`display: none`) |
| ≥1024px | Sidebar visible: 242px wide, 120px gap, content fills remainder |

The content column carries `max-w-[800px]` to cap editorial text at 800px. This is a Tailwind utility and must also be defined in critical CSS.

---

### Left navigation (sidebar)

`umd-element-nav-slider` is interior-only. It uses a two-level slot structure (verified from production UMD.edu HTML):

```html
<umd-element-nav-slider>
  <!-- LEVEL 1: parent section — renders BOLD as a section label -->
  <div slot="primary-slide-links">
    <a href="/about" data-child-ref="about-section"><span>About UMD</span></a>
  </div>
  <!-- LEVEL 2: child pages — renders at normal weight -->
  <!-- data-active = open on page load; also triggers the "back" indicator -->
  <!-- data-selected = current page link -->
  <div slot="children-slides">
    <div data-active data-parent-ref="about-section">
      <a href="/about/history"><span>History &amp; Traditions</span></a>
      <a href="/about/traditions-of-the-past" data-selected><span>Traditions of the Past</span></a>
      <a href="/about/symbols"><span>University Symbols</span></a>
    </div>
  </div>
</umd-element-nav-slider>
```

Slot rules:
- `slot="primary-slide-links"`: Use `<div>` (not `<nav>`). Links here render **bold** — section headers only, not individual page links.
- `slot="children-slides"`: `<div data-parent-ref="{id}">` groups. `data-active` opens the panel on load and triggers the "back" indicator. `data-selected` marks the current page.
- `data-child-ref` on the parent link must exactly match `data-parent-ref` on the children group.
- Wrap all link text in `<span>`.

---

### Spacing rules — interior pages

Interior pages use the `umd-layout-space-vertical-interior` and `umd-layout-space-vertical-interior-child` classes. The `umd-layout-vertical-interior*` aliases are combined in the same CSS rule and both work — prefer the `umd-layout-space-*` form (matches production).

**`umd-layout-space-vertical-interior`** — on each top-level `<section>` within the content column. Controls space between major content blocks:

| Breakpoint | `margin-bottom` |
|---|---|
| Default (mobile/tablet) | 56px |
| ≥1024px | 80px |

**`umd-layout-space-vertical-interior-child`** — on the heading or element directly above grouped content within a section. Controls space between a section heading and what follows it:

| All breakpoints | 32px `margin-bottom` |
|---|---|

Never use `umd-layout-vertical-landing` or `umd-layout-vertical-landing-child` on interior pages.

---

### Typography — interior content column

All headings and body copy inside the `max-w-[800px]` content column require explicit CSS classes. These classes are **not** part of `cdn.js` — they must be declared in critical CSS.

**Headings (H2, H3):**
```html
<h2 class="umd-layout-space-vertical-interior-child text-black umd-sans-larger-bold">Section Title</h2>
```
- `umd-sans-larger-bold` — 22px / 700 weight / 1.25em line-height at desktop
- `text-black` — `color: #000`

**Body copy:**
```html
<div class="umd-text-rich-advanced">
  <p>Body copy. 18px / 1.5em line-height / color #454545.</p>
  <p>Second paragraph — 24px top margin from first-child exception.</p>
</div>
```
- `umd-text-rich-advanced` sets size, color, paragraph spacing, and link styles
- Always wrap `slot="text"` content in `umd-text-rich-advanced` inside `umd-element-media-inline`

---

### Component subset — interior pages

Only the following components are used on interior page layouts. Do not place landing-page-only components on interior pages.

**Always on every page**
- Global university header (`umd-element-utility-header`)
- Site header with navigation (`umd-element-navigation-header` + `umd-element-nav-item`)
- Footer (`umd-element-footer`)

**Heroes — interior options only**
- Background hero small — `umd-element-hero` with `data-layout-height="small"`
- Minimal hero — `umd-element-hero-minimal`

**Content — available on interior pages**
- Inline media (`umd-element-media-inline`) — primary editorial content component
- Headlines and rich text (`umd-text-rich-advanced` CSS class)
- Standard cards (`umd-element-card`) — block and list variants
- Overlay cards (`umd-element-card-overlay`)
- Event cards and event lists (`umd-element-event`)
- Events list feed (`umd-feed-events-list`)
- Standard carousel *(not yet in registry)*
- Banner promo *(not yet in registry)*
- Accordion *(not yet in registry)*
- Quote (`umd-element-quote`)
- Logo grid *(not yet in registry)*
- Stat layouts (`umd-element-stat`)
- People cards — list and block *(not yet in registry)*
- Bio card *(not yet in registry)*
- Tabs *(not yet in registry)*

**Landing-page only — do not use on interior pages**

`pathway`, `pathway-highlight`, `section-intro`, `section-intro-wide`, `image-expand`, `sticky-columns`, `card-icon`, `card-video`, `hero-expand`, `hero-logo`, `hero-grid`, `hero-brand-video`.

---

## 22. Default hero — use the standard (background) hero

The default hero for landing pages is `umd-element-hero` with **no `data-display` attribute**. In this mode the image renders as a full background behind the text. This is the standard, expected treatment.

**Do not default to `data-display="overlay"`** — the overlay variant is a specific design choice with different visual behavior (composited color overlay on the image). Use it only when a true text-over-image overlay effect is explicitly desired.

| Intent | Correct |
|---|---|
| Standard page opener with background image | *(no `data-display`)* |
| Text-over-image with color overlay panel | `data-display="overlay"` |
| Shorter version for interior pages | `data-display="default-interior"` or `data-layout-height="small"` |

```html
<!-- ✓ Default — background image hero -->
<umd-element-hero data-theme="dark" data-animation>
  <img slot="image" src="/hero.jpg" alt="" />
  <h1 slot="headline">Fearless Ideas Start Here</h1>
</umd-element-hero>

<!-- Only use overlay when an overlay panel effect is specifically needed -->
<umd-element-hero data-display="overlay" data-theme="dark">
  <img slot="image" src="/hero.jpg" alt="" />
  <h1 slot="headline">Fearless Ideas Start Here</h1>
</umd-element-hero>
```

---

## 23. Hero section — when to add `umd-layout-vertical-landing`

Hero components manage their own internal spacing but produce no external bottom margin. Whether to add `umd-layout-vertical-landing` to the hero `<section>` depends entirely on what follows it.

**Add `umd-layout-vertical-landing`** when the section immediately after the hero has a light/white background (section intro, card grid, pathway, etc.) — the margin creates the expected breathing room between the hero and the next section.

**Omit `umd-layout-vertical-landing`** when a dark-background section immediately follows the hero. The margin would create a visible white gap between two dark elements. Instead, let the next section provide its own spacing (see §19).

```html
<!-- ✓ Light content follows — include the spacing -->
<section class="umd-layout-vertical-landing">
  <umd-element-hero data-theme="dark">...</umd-element-hero>
</section>
<section class="umd-layout-vertical-landing">
  <umd-element-section-intro>...</umd-element-section-intro>
</section>

<!-- ✓ Dark section follows — omit spacing on hero, keep it on the dark section -->
<section>
  <umd-element-hero data-theme="dark">...</umd-element-hero>
</section>
<section class="umd-layout-background-full-dark umd-layout-vertical-landing">
  ...
</section>
```

---

## 24. Pathway section padding — only when on a dark/colored band

Pathway components do not provide internal top/bottom breathing room. **However, `umd-layout-vertical-landing` already provides the section-level rhythm** that pathways need when they sit on the page's default background. Don't double up.

**Rule:**

- **Default (light page background):** Wrap the pathway in a `<section class="umd-layout-vertical-landing">` and **do not** add inline `padding: 80px 0`. The vertical-landing margin handles spacing.
- **Dark or colored band:** When the pathway sits inside a section with its own background (e.g. `background: #000`, `umd-layout-background-full-dark`), `umd-layout-vertical-landing` margins collapse against the band edges and the pathway looks flush against the colored boundary. Add `padding: 80px 0` to the section so the pathway has internal breathing room inside the band.

```html
<!-- ✓ Default — vertical-landing only, no inline padding -->
<section class="umd-layout-vertical-landing">
  <umd-element-pathway>
    ...
  </umd-element-pathway>
</section>

<!-- ✓ Dark band — inline 80px padding required -->
<section class="umd-layout-background-full-dark" style="padding: 80px 0;">
  <umd-element-pathway data-theme="dark">
    ...
  </umd-element-pathway>
</section>

<!-- ✗ Wrong — stacks vertical-landing margin AND 80px inline padding on a default-bg section -->
<section class="umd-layout-vertical-landing" style="padding: 80px 0;">
  <umd-element-pathway>...</umd-element-pathway>
</section>
```

This applies to: standard pathway (no `data-display`), `data-display="hero"`, `data-display="sticky"`.

**Overlay pathway (`data-display="overlay"`) is exempt** — it manages its own internal padding regardless of band background.

---

## 25. Logo images — always use local fallbacks

See **CLAUDE.md §Logos** for the header/footer fallback file paths. The core rule:

- **Footer logo:** Always use the local `../images/logos/footer-logo.svg`. Do not attempt external department logo URLs — they typically fail on the dark footer background (wrong color or hotlink-blocked).
- **Header logo:** A department-specific external logo is acceptable only when you have confirmed the URL is accessible and renders on a dark background. When in doubt, use the local fallback.

---

## 26. `umd-element-event` — promo and feature require deprecated `display` attribute

`umd-element-event` is the only component where `data-display="promo"` and `data-display="feature"` do not work. In the design system source, `isDisplay.promo` and `isDisplay.feature` check only the deprecated `display` attribute — not `data-display`. Using `data-display="promo"` fails silently and renders the default block card instead.

**Rule:** Use `display="promo"` and `display="feature"` (the deprecated attribute name) on `umd-element-event`. All other display variants on this component (`list`) and `data-display` on all other components work normally.

```html
<!-- ✓ Correct — uses deprecated display attribute for promo -->
<umd-element-event display="promo">
  <img slot="image" src="/event.jpg" alt="Event photo" />
  <h3 slot="headline"><a href="/events/symposium">Annual Symposium</a></h3>
  <time slot="start-date-iso" datetime="2026-05-01T09:00:00">May 1, 2026</time>
</umd-element-event>

<!-- ✗ Wrong — data-display="promo" silently renders as block card -->
<umd-element-event data-display="promo">
  <img slot="image" src="/event.jpg" alt="Event photo" />
  <h3 slot="headline"><a href="/events/symposium">Annual Symposium</a></h3>
  <time slot="start-date-iso" datetime="2026-05-01T09:00:00">May 1, 2026</time>
</umd-element-event>
```

The `promo` display renders text overlaid on the background image (overlay card style) — it requires `slot="image"`. The `feature` display uses a large date sign with an eyebrow ribbon.

Note: `data-display="list"` on `umd-element-event` works correctly with `data-display` (it has both old and new attribute support).

---

## 27. Carousel slot patterns — which card to use where

The carousel components do not enforce child types in the DS source — slots accept any block element. But the visual treatment of each carousel only fits certain cards. Use this matrix.

### `umd-element-carousel-cards` — built-in dark texture surface

The carousel ships its own dark SVG-textured background, so slotted cards must be designed for a dark surface. Two options:

| Card | When to use |
|---|---|
| `umd-element-card` with `data-theme="dark"` | Standard text + image card on the dark texture. Use when each card has body copy beyond the headline. |
| `umd-element-card-overlay data-theme="dark"` | Image-overlay card. Use when each card is primarily image-driven and the headline overlays the image. |

Do **not** use light-theme standard cards — they render a white block on the dark texture.

```html
<!-- ✓ Standard dark cards -->
<umd-element-carousel-cards>
  <h2 slot="headline">Resources</h2>
  <div slot="cards">
    <umd-element-card data-theme="dark">
      <img slot="image" src="/img.jpg" alt="…" />
      <h3 slot="headline"><a href="/x">Title</a></h3>
      <p slot="text">Supporting copy.</p>
    </umd-element-card>
  </div>
</umd-element-carousel-cards>

<!-- ✓ Image-overlay cards -->
<umd-element-carousel-cards>
  <div slot="cards">
    <umd-element-card-overlay data-theme="dark">
      <p slot="headline"><a href="/x"><span>Title</span></a></p>
      <div slot="text"><p>Supporting copy.</p></div>
    </umd-element-card-overlay>
  </div>
</umd-element-carousel-cards>
```

### `umd-element-carousel-thumbnail` — transparent slot surface

The thumbnail carousel reads `data-thumbnail` from the **host element** of each block (not a child). The visible card sits on the carousel's own surface, so use card variants that don't paint their own background.

| Card | How |
|---|---|
| `umd-element-card` | Set `data-visual-transparent="true"`, `data-visual-image-aligned="true"`, and `data-thumbnail="<url>"` on the host. |
| `umd-element-person-bio` | Set `data-thumbnail="<url>"` on the host. The person-bio's natural layout (image + name + role) suits a thumbnail strip. |

Do **not** use `umd-element-card-overlay` — overlay cards always render their own background, which conflicts with the carousel's surface.

```html
<umd-element-carousel-thumbnail>
  <div slot="blocks">
    <umd-element-card
      data-visual-transparent="true"
      data-visual-image-aligned="true"
      data-thumbnail="/portrait-thumb.jpg">
      <img slot="image" src="/portrait.jpg" alt="Person Name" />
      <p slot="headline">Person Name '00</p>
      <div slot="text"><p>Title or accomplishment</p></div>
    </umd-element-card>
  </div>
</umd-element-carousel-thumbnail>
```

### Other carousels

- `umd-element-carousel-image` / `-multiple-image`: slot accepts plain `<img>` elements only — alt text is enforced by a runtime warning. No card components.
- `umd-element-carousel-image-wide`: slot expects `<figure>` or `<div>` with an inner `<img>` plus `data-headline` / `data-text` divs for caption metadata. No card components.
- `umd-element-carousel` (base): generic — accepts any block. Use only when none of the specialized carousels fit.
