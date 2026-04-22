# UMD Layout Patterns — CSS-Only Reference

These are **CSS utility class patterns**, not web components. They are not injected by `cdn.js`. All CSS definitions live in `styles/critical.css` (the single source of truth) and are already included in the TEMPLATE.html `<style>` block. All classes are from `@universityofmaryland/web-styles-library`.

This file documents **HTML usage patterns** — how to compose these classes in markup. For the CSS definitions themselves, see `styles/critical.css`.

---

## Hero-to-Content Spacing Rule

The `<section>` that wraps a hero **must carry `umd-layout-vertical-landing`** (landing pages) or `umd-layout-vertical-interior` (interior pages) to create the gap between the hero bottom and the first content section.

```html
<!-- ✓ Landing page — hero section carries the spacing -->
<section class="umd-layout-vertical-landing">
  <umd-element-hero data-theme="dark" data-animation>
    ...
  </umd-element-hero>
</section>

<!-- ✓ Interior page — same rule, different class -->
<section class="umd-layout-vertical-interior">
  <umd-element-hero data-display="small">
    ...
  </umd-element-hero>
</section>
```

### Exception: adjacent dark sections

If the hero is dark **and** the first content section is also a full dark section, omit the spacing class from the hero's `<section>`. The two dark blocks merge visually and no gap is needed.

```html
<!-- ✓ Dark hero directly above dark section — no gap needed -->
<section>
  <umd-element-hero data-theme="dark" data-animation>...</umd-element-hero>
</section>
<section class="umd-layout-vertical-landing umd-layout-background-full-dark">
  <!-- stats, events, cards on dark background -->
</section>

<!-- ✗ Wrong — adding spacing here creates a white gap between two dark blocks -->
<section class="umd-layout-vertical-landing">
  <umd-element-hero data-theme="dark" data-animation>...</umd-element-hero>
</section>
<section class="umd-layout-vertical-landing umd-layout-background-full-dark">
  ...
</section>
```

---

## Masonry Grid (`umd-layout-grid-masonry`)

Two-column staggered layout. Odd children are offset upward, even children are pushed down, creating a visual zigzag. Stacks to a single column on mobile.

**When to use:** 4 image-overlay cards on landing pages. Works especially well when cards have equal dimensions and strong images.

**When NOT to use:** Mixed content types, lists, or cards where visual hierarchy matters — use `umd-layout-grid-gap-two` for plain two-column grids.

```html
<!-- 4 overlay cards in staggered masonry -->
<div class="umd-layout-grid-masonry">
  <umd-element-card-overlay type="image">
    <img slot="image" src="/img1.jpg" alt="" />
    <h2 slot="headline"><a href="/research">Research</a></h2>
    <p slot="text">Body copy.</p>
  </umd-element-card-overlay>
  <umd-element-card-overlay type="image">
    <img slot="image" src="/img2.jpg" alt="" />
    <h2 slot="headline"><a href="/academics">Academics</a></h2>
    <p slot="text">Body copy.</p>
  </umd-element-card-overlay>
  <umd-element-card-overlay type="image">
    <img slot="image" src="/img3.jpg" alt="" />
    <h2 slot="headline"><a href="/partners">Partners</a></h2>
    <p slot="text">Body copy.</p>
  </umd-element-card-overlay>
  <umd-element-card-overlay type="image">
    <img slot="image" src="/img4.jpg" alt="" />
    <h2 slot="headline"><a href="/alumni">Alumni</a></h2>
    <p slot="text">Body copy.</p>
  </umd-element-card-overlay>
</div>
```

Add per-page CSS to set card height (the stagger depends on cards having a defined height):

```css
.umd-layout-grid-masonry umd-element-card-overlay {
  min-height: 420px;
}
@media (min-width: 768px) {
  .umd-layout-grid-masonry umd-element-card-overlay { min-height: 480px; }
}
```

**Stagger mechanics** (for reference — defined in `critical.css`):

| Child position | Desktop offset |
|---|---|
| 1st (odd) | `margin-top: 0` (first-child override) |
| 2nd (even) | `margin-top: 40px` (pushed down) |
| 3rd (odd) | `margin-top: -40px` (pulled up) |
| 4th (even) | `margin-top: 0` |

---

## Three-Column Offset Grid (`umd-layout-grid-offset-three`)

An alternative to a flat 3-column grid when you want visual interest. Use for 3 overlay or image cards. See `critical.css` for the CSS definition.

---

## Section-Intro to Content Spacing

`umd-element-section-intro` and `umd-element-section-intro-wide` have no built-in bottom margin. Place the spacing class **directly on the section-intro component** to create the gap between the heading and the content (cards, list, feed) below it.

- **Landing pages:** `umd-layout-vertical-landing-child` — `margin-bottom: 32px` → `40px` → `48px`
- **Interior pages:** `umd-layout-vertical-interior-child` — `margin-bottom: 32px`

```html
<!-- ✓ Landing page — spacing class on the section-intro component -->
<section class="umd-layout-vertical-landing">
  <div class="umd-layout-space-horizontal-larger">

    <umd-element-section-intro-wide class="umd-layout-vertical-landing-child">
      <h2 slot="headline">Latest News</h2>
      <div slot="actions">
        <umd-element-call-to-action data-display="secondary">
          <a href="/news">View All</a>
        </umd-element-call-to-action>
      </div>
    </umd-element-section-intro-wide>

    <div class="grid-four">
      <umd-element-card data-aligned>...</umd-element-card>
      <umd-element-card data-aligned>...</umd-element-card>
    </div>

  </div>
</section>
```

```html
<!-- ✓ Dark section — same rule, data-theme="dark" on intro -->
<section class="umd-layout-vertical-landing umd-layout-background-full-dark">
  <div class="umd-layout-space-horizontal-normal">

    <umd-element-section-intro data-theme="dark" class="umd-layout-vertical-landing-child">
      <h2 slot="headline">Upcoming Events</h2>
      <div slot="actions">
        <umd-element-call-to-action data-display="secondary" data-theme="dark">
          <a href="/events">View All Events</a>
        </umd-element-call-to-action>
      </div>
    </umd-element-section-intro>

    <div class="umd-layout-grid-gap-stacked">
      <umd-element-event data-display="list" data-theme="dark">...</umd-element-event>
    </div>

  </div>
</section>
```

```html
<!-- ✓ Interior page — use umd-layout-vertical-interior-child instead -->
<section class="umd-layout-vertical-interior">
  <div class="umd-layout-space-horizontal-normal">

    <umd-element-section-intro class="umd-layout-vertical-interior-child">
      <h2 slot="headline">Faculty Research</h2>
    </umd-element-section-intro>

    <div class="umd-layout-grid-gap-two">
      <umd-element-card>...</umd-element-card>
    </div>

  </div>
</section>
```

```html
<!-- ✗ Wrong — class on the grid, not the intro. This adds margin-bottom
     BELOW the cards (gap to next section), not between heading and cards. -->
<umd-element-section-intro-wide>...</umd-element-section-intro-wide>
<div class="grid-four umd-layout-vertical-landing-child">...</div>
```

---

## Footer Address Markup

`umd-element-footer` uses **extract-and-append** (not native HTML slot projection). The component moves `slot="address"` content directly into its shadow DOM, so light-DOM CSS targeting `[slot="address"]` has no effect.

The shadow DOM applies `color: white` only to `p`, `a`, and `span` children of the address wrapper. **Always wrap each address line in a `<span>`** — raw text nodes and `<br>` tags get no color treatment and appear black on the dark footer background.

```html
<!-- ✓ Correct — each line in a <span> -->
<address slot="address">
  <span>1101 Engineering Building</span>
  <span>College Park, MD 20742</span>
</address>

<!-- ✗ Wrong — raw text with <br> gets no color, appears invisible on dark footer -->
<address slot="address">
  1101 Engineering Building<br />
  College Park, MD 20742
</address>
```

---

## Rich Text Advanced (`umd-text-rich-advanced`)

A content wrapper for editorial/body copy sections. Provides 18px body text, 1.5em line height, and animated underline link hover styles.

### Light background — single column

```html
<div class="umd-layout-space-horizontal-small">
  <div class="umd-text-rich-advanced">
    <hr>
    <p>Body copy goes here.</p>
  </div>
</div>
```

### Light background — two columns

```html
<div class="umd-layout-space-horizontal-small">
  <div class="umd-layout-grid-gap-two">
    <div class="umd-text-rich-advanced">
      <hr>
      <p>Left column body copy.</p>
      <div class="umd-layout-grid-inline-tablet-rows">
        <umd-element-call-to-action data-display="secondary">
          <a href="/page">CTA Label</a>
        </umd-element-call-to-action>
      </div>
    </div>
    <div class="umd-text-rich-advanced">
      <hr>
      <p class="umd-sans-larger-bold">OPTIONAL INLINE HEADLINE</p>
      <p>Right column body copy.</p>
    </div>
  </div>
</div>
```

### Dark background — two columns

Use `umd-layout-background-full-dark` on the section wrapper. Switch to `umd-text-rich-advanced-dark`. Add `text-white` to any inline typography classes.

A separate headline above the grid uses both the horizontal lock and the vertical headline spacing class:

```html
<section class="umd-layout-background-full-dark">

  <!-- Optional: separate section headline above the grid -->
  <h2 class="umd-layout-space-horizontal-small umd-layout-space-vertical-headline-large text-white umd-sans-extralarge-bold">
    Section Headline
  </h2>

  <div class="umd-layout-space-horizontal-small">
    <div class="umd-layout-grid-gap-two">

      <div class="umd-text-rich-advanced-dark">
        <p class="text-white umd-sans-large">INLINE LABEL OR SUBHEAD</p>
        <p>Body copy — inherits white from dark variant.</p>
        <p class="text-white umd-sans-larger-bold">"A pull-quote style headline."</p>
        <p>Attribution, <i>Title</i></p>
      </div>

      <div class="umd-text-rich-advanced-dark">
        <figure class="umd-layout-alignment-block-stacked">
          <img src="/image.jpg" alt="Description">
        </figure>
        <p>Caption or follow-up copy beneath the image.</p>
      </div>

    </div>
  </div>

</section>
```

### Dark background — single column

```html
<section class="umd-layout-background-full-dark">
  <div class="umd-layout-space-horizontal-small">
    <div class="umd-text-rich-advanced-dark">
      <p>Body copy, inherits white text from dark variant.</p>
      <figure class="umd-layout-alignment-block-stacked">
        <img src="/image.jpg" alt="Description">
      </figure>
      <p>Follow-up copy after image.</p>
    </div>
  </div>
</section>
```

---

## Layout Classes Used in These Patterns

### `umd-layout-space-horizontal-small` — 992px content lock

The standard lock for these rich text sections. Centers content with responsive side padding and a 992px max-width. Use on landing pages where a narrower reading column is intended.

For full CSS definition, see RULES.md §12.

### `umd-layout-grid-gap-two` — two-column grid

Stacks on mobile, becomes `repeat(2, 1fr)` at 650px+.

```css
.umd-layout-grid-gap-two {
  display: grid;
}
@media (min-width: 650px) {
  .umd-layout-grid-gap-two {
    grid-template-columns: repeat(2, 1fr);
    gap: 32px;
  }
}
@media (min-width: 1024px) {
  .umd-layout-grid-gap-two { gap: 40px; }
}
```

### `umd-layout-grid-inline-tablet-rows` — inline CTA row

Stacks CTAs vertically on mobile, switches to a flex row at 650px+. Use to wrap multiple `umd-element-call-to-action` elements side by side.

```css
.umd-layout-grid-inline-tablet-rows {
  align-items: flex-start;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
@media (min-width: 650px) {
  .umd-layout-grid-inline-tablet-rows {
    flex-direction: row;
    flex-wrap: wrap;
    align-items: center;
  }
}
```

### Adjacent dark sections — eliminating white gaps

When two dark-background sections appear next to each other, `umd-layout-vertical-landing` on the first section creates a white `margin-bottom` gap between them. Omit `umd-layout-vertical-landing` from the first section to merge them visually.

```html
<!-- ✓ Correct — no white gap between dark sections -->
<section style="background:#000;">
  <umd-layout-image-expand>...</umd-layout-image-expand>
</section>
<section class="umd-layout-vertical-landing umd-layout-background-full-dark">
  <!-- stats, cards, or other dark content -->
</section>

<!-- ✗ Wrong — umd-layout-vertical-landing on the first dark section
     produces a white margin gap before the second dark section -->
<section class="umd-layout-vertical-landing" style="background:#000;">
  <umd-layout-image-expand>...</umd-layout-image-expand>
</section>
<section class="umd-layout-vertical-landing umd-layout-background-full-dark">
  ...
</section>
```

**Rule:** The section that provides the spacing gap to the next section should always be the LAST dark section in the group — it carries `umd-layout-vertical-landing` to push away from the following light section. All preceding dark sections in the group omit it.

---

### `umd-layout-background-full-dark` — full-width dark section

Black background with vertical padding that scales with viewport. Replaces manual `background: #000` when you also need the built-in top/bottom padding.

```css
.umd-layout-background-full-dark {
  background-color: #000000;
  padding: 48px 0;
}
@media (min-width: 768px) {
  .umd-layout-background-full-dark { padding: 80px 0; }
}
@media (min-width: 1200px) {
  .umd-layout-background-full-dark { padding: 104px 0; }
}
```

### `umd-layout-space-vertical-headline-large` — headline bottom spacing

Apply to a section headline that sits immediately above a content grid. Creates a gap between the headline and the grid below.

```css
.umd-layout-space-vertical-headline-large { margin-bottom: 16px; }
@media (min-width: 1024px) {
  .umd-layout-space-vertical-headline-large { margin-bottom: 24px; }
}
```

### `umd-layout-alignment-block-stacked` — stacked figure content

Use on `<figure>` elements inside rich text. Children stack vertically with 16px gaps between them (first child has no top margin).

```css
.umd-layout-alignment-block-stacked {
  display: flex;
  flex-direction: column;
}
.umd-layout-alignment-block-stacked > * { margin-top: 16px; }
.umd-layout-alignment-block-stacked > *:first-child { margin-top: 0; }
```

---

## Typography Classes for Inline Headlines

These are used inside `umd-text-rich-advanced` (or `-dark`) to create in-content headlines and labels. Apply directly to `<p>` elements (not heading tags, which carry semantic weight).

| Class | Use | Size |
|---|---|---|
| `umd-sans-large` | Section labels, small inline subheads | 18px, bold, 1.25em line height |
| `umd-sans-larger-bold` | Standard inline headlines, pull-quote style | 18–22px responsive, bold |
| `umd-sans-extralarge-bold` | Separate section headline above a grid | 18–32px responsive, bold |

Add `text-white` on dark backgrounds.

```css
.umd-sans-large {
  font-family: "Interstate", Helvetica, Arial, Verdana, sans-serif;
  font-weight: 700;
  font-size: 18px;
  line-height: 1.25em;
}

.umd-sans-larger-bold {
  font-family: "Interstate", Helvetica, Arial, Verdana, sans-serif;
  font-weight: 700;
  font-size: 18px;
  line-height: 1.40em;
  text-wrap: pretty;
}
@media (min-width: 650px) {
  .umd-sans-larger-bold { font-size: calc(18px + 0.5vw); }
}
@media (min-width: 1024px) {
  .umd-sans-larger-bold { font-size: 22px; line-height: 1.25em; }
}

.umd-sans-extralarge-bold {
  font-family: "Interstate", Helvetica, Arial, Verdana, sans-serif;
  font-weight: 700;
  font-size: 18px;
  line-height: 1.25em;
  text-wrap: pretty;
}
@media (min-width: 650px) {
  .umd-sans-extralarge-bold { font-size: calc(18px + 1.16vw); }
}
@media (min-width: 1024px) {
  .umd-sans-extralarge-bold { font-size: 32px; line-height: 1.125em; }
}

/* Color utility — define in page style block */
.text-white { color: #ffffff; }
```

---

## Rich Text Advanced CSS

Include both variants when either may appear in the page.

```css
/* Light variant */
.umd-text-rich-advanced {
  font-size: 18px;
  line-height: 1.5em;
}
.umd-text-rich-advanced a {
  color: #000000;
  background-image: linear-gradient(#000000, #000000);
  position: relative;
  background-position: left calc(100% - 1px);
  background-repeat: no-repeat;
  background-size: 100% 1px;
  transition: color 0.5s, background-size 0.5s, background-image 0.5s, background-position 0.5s;
}
.umd-text-rich-advanced a:hover,
.umd-text-rich-advanced a:focus {
  background-image: linear-gradient(#E21833, #E21833);
}

/* Dark variant */
.umd-text-rich-advanced-dark {
  font-size: 18px;
  line-height: 1.5em;
}
.umd-text-rich-advanced-dark p,
.umd-text-rich-advanced-dark li { color: #ffffff; }
.umd-text-rich-advanced-dark a {
  color: #ffffff;
  background-image: linear-gradient(#ffffff, #ffffff);
  position: relative;
  background-position: left calc(100% - 1px);
  background-repeat: no-repeat;
  background-size: 100% 1px;
  transition: color 0.5s, background-size 0.5s, background-image 0.5s, background-position 0.5s;
}
.umd-text-rich-advanced-dark a:hover,
.umd-text-rich-advanced-dark a:focus {
  background-image: linear-gradient(#FFD200, #FFD200);
}
```

---

## Horizontal Rules

Use a plain `<hr>` directly inside `umd-text-rich-advanced` or `umd-text-rich-advanced-dark`. No extra class needed — the rich text class styles it automatically.

```html
<div class="umd-text-rich-advanced">
  <hr>
  <p>Content following the rule.</p>
</div>
```

---

## Link Cards Grid (`umd-element-card-overlay` without image)

When a section contains only a row of standalone links — no supporting body copy, no images, just navigation destinations — use `umd-element-card-overlay` without an image slot instead of a row of secondary CTAs. Without `type="image"` and without a `slot="image"`, the card renders as a text-only dark card. Use `slot="cta-icon"` for the arrow link.

**When to use this pattern:** A row of 2–4 links that each represent a destination (topic, program, action). The cards provide visual weight and a dark card grid is more scannable than a row of pill buttons.

**When NOT to use:** If links have supporting descriptions, use `umd-element-card` (standard). If links are secondary actions accompanying a primary button, keep using `umd-layout-grid-inline-tablet-rows` with CTAs.

```html
<!-- 2-column link card grid — uses existing umd-layout-grid-gap-two -->
<div class="umd-layout-grid-gap-two">
  <umd-element-card-overlay>
    <h3 slot="headline"><a href="/page-one">First Destination</a></h3>
    <a slot="cta-icon" href="/page-one">Go</a>
  </umd-element-card-overlay>
  <umd-element-card-overlay>
    <h3 slot="headline"><a href="/page-two">Second Destination</a></h3>
    <a slot="cta-icon" href="/page-two">Go</a>
  </umd-element-card-overlay>
</div>

<!-- 3-column link card grid — add page-specific CSS class -->
<div class="link-cards-three">
  <umd-element-card-overlay>
    <h3 slot="headline"><a href="/page-one">First Destination</a></h3>
    <a slot="cta-icon" href="/page-one">Go</a>
  </umd-element-card-overlay>
  <umd-element-card-overlay>
    <h3 slot="headline"><a href="/page-two">Second Destination</a></h3>
    <a slot="cta-icon" href="/page-two">Go</a>
  </umd-element-card-overlay>
  <umd-element-card-overlay>
    <h3 slot="headline"><a href="/page-three">Third Destination</a></h3>
    <a slot="cta-icon" href="/page-three">Go</a>
  </umd-element-card-overlay>
</div>
```

Add this CSS to the page `<style>` block for 3-column grids (not in critical.css — define per page):

```css
.link-cards-three {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}
@media (min-width: 650px) {
  .link-cards-three { grid-template-columns: repeat(3, 1fr); }
}
```

---

## CTAs Inside Rich Text

Wrap one or more `umd-element-call-to-action` in `umd-layout-grid-inline-tablet-rows`. On dark backgrounds, add `data-theme="dark"` to each CTA (theme does not cascade — see RULES.md §14).

```html
<!-- Light background -->
<div class="umd-layout-grid-inline-tablet-rows">
  <umd-element-call-to-action data-display="secondary">
    <a href="/page-one">Primary Action</a>
  </umd-element-call-to-action>
  <umd-element-call-to-action data-display="secondary">
    <a href="/page-two">Secondary Action</a>
  </umd-element-call-to-action>
</div>

<!-- Dark background — each CTA needs data-theme="dark" -->
<div class="umd-layout-grid-inline-tablet-rows">
  <umd-element-call-to-action data-display="secondary" data-theme="dark">
    <a href="/page-one">Primary Action</a>
  </umd-element-call-to-action>
  <umd-element-call-to-action data-display="secondary" data-theme="dark">
    <a href="/page-two">Secondary Action</a>
  </umd-element-call-to-action>
</div>
```
