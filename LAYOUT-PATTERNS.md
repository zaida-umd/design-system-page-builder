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

If the hero is dark **and** the first content section is also a full dark section, omit `umd-layout-vertical-landing` from the hero's `<section>` to eliminate the white gap. See `RULES.md §19` for the canonical rule and full examples.

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

## Stat Card Grid (block stats in a grid)

**Use only when the user asks for the "card" version of stats** — `umd-element-stat data-display="block"`. The block variant renders each stat as a filled card with a red top border, gray background, and a watermark texture. For the plain (non-card) stat layout, use the default `umd-element-stat` in any grid or sticky-columns layout — both are valid.

**Required pieces for a stat card grid:**
- `data-display="block"` on every `umd-element-stat`
- `class="umd-layout-grid-child-fill-height"` on every stat so cards equalize height
- A grid container — use a **standard grid utility**, not a custom CSS grid:
  - `umd-layout-grid-gap-two` for 2 stats
  - `umd-layout-grid-gap-three` for 3 stats
  - `umd-layout-grid-columns-four` for 4 stats
  - Custom grids (e.g. `news-grid-three`) won't be picked up by the grid entry-animation script and will need an explicit `umd-animation-grid` opt-in marker to animate. Prefer the standard utility so animations work automatically.
- **Do not** add `data-decoration-line` — the red top border is built into block display; the accent line is for the non-card variant only
- **Do not** add `data-visual-size="large"` — block already implies large sizing

**Slot names:**
- `slot="stat"` — the number (`<span>` recommended)
- `slot="text"` — the descriptive label (this is the named default slot — a plain `<p>` with no slot attribute will not render)
- `slot="sub-text"` — optional source/citation line

```html
<div class="umd-layout-grid-gap-three">
  <umd-element-stat data-display="block" class="umd-layout-grid-child-fill-height">
    <span slot="stat">100+</span>
    <p slot="text">Undergraduate Majors</p>
  </umd-element-stat>
  <umd-element-stat data-display="block" class="umd-layout-grid-child-fill-height">
    <span slot="stat">18:1</span>
    <p slot="text">Student-to-Faculty Ratio</p>
  </umd-element-stat>
  <umd-element-stat data-display="block" class="umd-layout-grid-child-fill-height">
    <span slot="stat">69</span>
    <p slot="text">Colleges, schools and programs ranked in the top 25 nationwide</p>
    <p slot="sub-text">2025 U.S. News &amp; World Report</p>
  </umd-element-stat>
</div>
```

**When to choose card grid vs. sticky-columns vs. plain stat grid:**
- **Card grid (block)** — homogenous stats, no editorial framing column needed, want strong visual presence.
- **Sticky-columns** — there's a meaningful intro paragraph that should sit alongside the stats while scrolling. Works for stats *and* events; the deciding factor is whether you have enough text to justify the sticky column. Sparse intros look weak in a sticky column.
- **Plain stat grid (default `umd-element-stat`, no `data-display`)** — minimalist, text-only stats; use `data-decoration-line` here if you want the accent line.

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

    <div class="umd-layout-grid-columns-four">
      <umd-element-card data-visual-image-aligned="true">...</umd-element-card>
      <umd-element-card data-visual-image-aligned="true">...</umd-element-card>
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
<!-- ✓ Dark section with body copy — headline + text + primary CTA + line accent leading into masonry -->
<section class="umd-layout-background-full-dark umd-layout-vertical-landing">
  <div class="umd-layout-space-horizontal-normal">

    <umd-element-section-intro data-theme="dark" include-separator class="umd-layout-vertical-landing-child">
      <h2 slot="headline">Welcome to the College of Information</h2>
      <div slot="text">
        <p>The University of Maryland College of Information is a top-ranked research and teaching college where faculty, staff, and students are passionate about using information and technology.</p>
      </div>
      <div slot="actions">
        <umd-element-call-to-action data-display="primary" data-theme="dark">
          <a href="/about/">Learn More</a>
        </umd-element-call-to-action>
      </div>
    </umd-element-section-intro>

    <div class="umd-layout-grid-masonry">
      <umd-element-card-overlay>...</umd-element-card-overlay>
      <umd-element-card-overlay>...</umd-element-card-overlay>
      <umd-element-card-overlay>...</umd-element-card-overlay>
      <umd-element-card-overlay>...</umd-element-card-overlay>
    </div>

  </div>
</section>
```

Notes:
- `include-separator` — boolean attribute that adds a decorative red vertical line accent above the headline
- `slot="text"` accepts a `<div>` with `<p>` body copy; renders between headline and actions
- `data-display="primary"` on the CTA is appropriate here — dark sections use `data-theme="dark"` on the CTA too
- The `umd-layout-vertical-landing-child` class goes on `umd-element-section-intro`, not on the grid

### Masonry compensation rule

`umd-layout-grid-masonry` applies `margin-top: -32px` (tablet) / `-40px` (desktop) to row-2+ odd items for the stagger effect. Those negative margins pull content upward, consuming the `umd-layout-vertical-landing-child` margin-bottom on the section-intro above. Add this CSS rule to restore the visual gap:

```css
@media (min-width: 768px) {
  umd-element-section-intro + .umd-layout-grid-masonry,
  umd-element-section-intro-wide + .umd-layout-grid-masonry { padding-top: 32px; }
}
@media (min-width: 1024px) {
  umd-element-section-intro + .umd-layout-grid-masonry,
  umd-element-section-intro-wide + .umd-layout-grid-masonry { padding-top: 40px; }
}
```

This rule is included in `styles/critical.css`. Pages using this pattern have it automatically via the `<head>` block.

```html
<!-- ✗ Wrong — class on the grid, not the intro. This adds margin-bottom
     BELOW the cards (gap to next section), not between heading and cards. -->
<umd-element-section-intro-wide>...</umd-element-section-intro-wide>
<div class="umd-layout-grid-columns-four umd-layout-vertical-landing-child">...</div>
```

---

## Events Section — Featured Promo + Stacked List

Use `umd-element-sticky-columns` when you have one editorially featured event and a list of upcoming events. The sticky column holds the featured event (visible while the user scrolls the list); the static column holds the list.

**When to use:** Any events section with a "featured" or "highlighted" event plus 3–6 upcoming events below.

**Light vs. dark background:** For events sections in the lower half of the page, prefer a light background with `umd-element-section-intro-wide` and a watermark. Dark theming is appropriate early in the page (after a dark hero) but events sections are primarily for scanning — a light background improves readability. If the page already has a dark band earlier (stats, image-expand, pathway), the events section should contrast it with light.

```html
<section class="umd-layout-vertical-landing">
  <!-- Watermark + section heading -->
  <div class="umd-layout-space-horizontal-larger">
    <div class="umd-watermark" aria-hidden="true">
      <span role="presentation">Events</span>
    </div>
    <umd-element-section-intro-wide class="umd-layout-vertical-landing-child">
      <h2 slot="headline">Upcoming Events</h2>
      <div slot="actions">
        <umd-element-call-to-action data-display="secondary">
          <a href="/events">View All Events</a>
        </umd-element-call-to-action>
      </div>
    </umd-element-section-intro-wide>
  </div>

  <!-- Sticky: featured event | Static: event list -->
  <umd-element-sticky-columns
    class="umd-layout-space-horizontal-larger"
    data-layout-position="100px">

    <div slot="sticky-column">
      <!-- Note: use display="promo" (deprecated attr), NOT data-display="promo" — see RULES.md §26 -->
      <umd-element-event display="promo">
        <img slot="image" src="../images/event.jpg" alt="Event photo" />
        <time slot="start-date-iso" datetime="2026-05-01T09:00:00">May 1, 2026</time>
        <h3 slot="headline"><a href="/events/featured">Featured Event Title</a></h3>
        <p slot="location">Stamp Student Union</p>
        <div slot="text">
          <p>Short description of the featured event — 1–2 sentences.</p>
        </div>
      </umd-element-event>
    </div>

    <div slot="static-column">
      <div class="umd-layout-grid-gap-stacked">
        <umd-element-event data-display="list">
          <time slot="start-date-iso" datetime="2026-04-23T12:00:00">April 23, 2026</time>
          <h3 slot="headline"><a href="/events/1">Event One Title</a></h3>
          <p slot="location">Room 1234, Building Name</p>
        </umd-element-event>
        <umd-element-event data-display="list">
          <time slot="start-date-iso" datetime="2026-04-25T14:00:00">April 25, 2026</time>
          <h3 slot="headline"><a href="/events/2">Event Two Title</a></h3>
          <p slot="location">Virtual</p>
        </umd-element-event>
        <!-- add 3–5 total list events -->
      </div>
    </div>

  </umd-element-sticky-columns>
</section>
```

**Notes:**
- The "View All Events" CTA belongs in the section-intro-wide `slot="actions"` — do not repeat it at the bottom of the event list.
- `umd-element-event data-display="list"` works correctly with `data-display`; only `promo` and `feature` require the deprecated `display` attribute.
- `data-layout-position="100px"` should match the sticky nav height so the promo event clears it when scrolling.
- If a live events feed is needed, `umd-feed-events-list` can replace the stacked list — but it requires a server context (CORS blocks it on localhost).

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

See `RULES.md §19` for the canonical rule and full examples. Short version: omit `umd-layout-vertical-landing` from every dark section *except the last one in the group* — that last one carries the margin to push away from the next light section.

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

Two distinct uses:

### Inside rich text — auto-styled

Use a plain `<hr>` directly inside `umd-text-rich-advanced` or `umd-text-rich-advanced-dark`. No extra class needed — the rich text class styles it automatically.

```html
<div class="umd-text-rich-advanced">
  <hr>
  <p>Content following the rule.</p>
</div>
```

### Standalone — section divider above an editorial block

When the rule sits **above** the rich-text wrapper (as a section eyebrow divider), use `.umd-text-divider`. It is independent of the rich text class — applying `.umd-text-rich-advanced` is **not** required for the divider to render correctly. Add `.dark` for white-on-black sections.

```html
<section class="umd-layout-vertical-landing">
  <div class="umd-layout-space-horizontal-small">
    <hr class="umd-text-divider" />
    <p class="umd-sans-larger-bold mb-md" style="text-transform:uppercase;">Study Here</p>
    <div class="umd-text-rich-advanced">
      <p>Body copy goes here.</p>
    </div>
    <div style="margin-top:24px;">
      <umd-element-call-to-action data-display="primary">
        <a href="/programs">Explore All Programs</a>
      </umd-element-call-to-action>
    </div>
  </div>
</section>
```

The divider is **optional** — only use it where the design calls for an explicit horizontal rule above the eyebrow. A bare eyebrow + body without the divider is also valid.

---

## Hero + Section-Intro Split

When a hero would otherwise carry a multi-line subhead, hierarchical text (title + body), or more than 2 CTAs, pull the body copy and CTA row into a `umd-element-section-intro` directly below the hero. The hero keeps just the page title; the section-intro carries the lede + actions. See `RULES.md §22` for the rule.

```html
<!-- Hero — page title only -->
<section class="umd-layout-vertical-landing">
  <umd-element-hero data-display="standard" data-layout-height="small" data-layout-text="center">
    <h1 slot="headline">Page Title</h1>
    <img slot="image" src="/hero.jpg" alt="…" />
  </umd-element-hero>
</section>

<!-- Section-intro (text-only variant — see RULES.md §31) carries the lede + CTA row -->
<section class="umd-layout-vertical-landing">
  <div class="umd-layout-space-horizontal-larger">
    <umd-element-section-intro>
      <div slot="text">
        <p>The long body sentence the page leads with — one paragraph, no separate title.</p>
      </div>
      <div slot="actions">
        <umd-element-call-to-action data-display="secondary">
          <a href="/path-a">First action</a>
        </umd-element-call-to-action>
        <umd-element-call-to-action data-display="secondary">
          <a href="/path-b">Second action</a>
        </umd-element-call-to-action>
        <umd-element-call-to-action data-display="secondary">
          <a href="/path-c">Third action</a>
        </umd-element-call-to-action>
      </div>
    </umd-element-section-intro>
  </div>
</section>
```

When the body sentence has a separate section title, use the standard headline + text combination instead. The text-only variant is specifically for "lede paragraph, no title."

---

## Side Navigation as Accordion Stack (landing pages)

When recreating a source page that uses left-rail / side navigation, drop it into `umd-element-accordion-item` groups near the bottom of the landing page (above the footer). One accordion per natural parent section (e.g. "Future Students", "Current Students"). See `RULES.md §32` for the wrap and gap tokens.

```html
<section class="umd-layout-vertical-landing">
  <div class="umd-layout-space-horizontal-small">
    <div style="display: grid; gap: var(--umd-space-min);">
      <umd-element-accordion-item>
        <p slot="headline">Future Students</p>
        <div slot="text">
          <ul style="list-style:none; padding:0; margin:0;">
            <li style="padding:8px 0; border-bottom:1px solid #e6e6e6;">
              <a href="/path-a" style="color:#000; text-decoration:none;">Page A</a>
            </li>
            <li style="padding:8px 0; border-bottom:1px solid #e6e6e6;">
              <a href="/path-b" style="color:#000; text-decoration:none;">Page B</a>
            </li>
            <li style="padding:8px 0;">
              <a href="/path-c" style="color:#000; text-decoration:none;">Page C</a>
            </li>
          </ul>
        </div>
      </umd-element-accordion-item>

      <umd-element-accordion-item>
        <p slot="headline">Current Students</p>
        <div slot="text">…</div>
      </umd-element-accordion-item>
    </div>
  </div>
</section>
```

Why a list with `border-bottom` instead of plain `<ul>`: the accordion body has no built-in list styling — the inline padding/border per `<li>` produces a clean clickable row.

---

## Link Cards Grid (`umd-element-card-overlay` without image)

When a section contains only a row of standalone links — no supporting body copy, no images, just navigation destinations — use `umd-element-card-overlay` without an image slot instead of a row of secondary CTAs. Without `type="image"` and without a `slot="image"`, the card renders as a text-only dark card. Use `slot="cta-icon"` for the arrow link.

**When to use this pattern:** A row of 2–4 links that each represent a destination (topic, program, action) **and the source has no image** for them. The cards provide visual weight and a dark card grid is more scannable than a row of pill buttons.

**If the source has any image (icon, photo, banner crop) for these cards:** use the image-overlay variant instead — see `RULES.md §16` "When the source has any image, use the image variant". The image is part of the navigational affordance and a text-only card loses that signal.

```html
<!-- ✓ With source image — image-overlay variant -->
<div class="umd-layout-grid-columns-four umd-layout-grid-child-fill-height">
  <umd-element-card-overlay type="image" data-theme="dark">
    <img slot="image" src="../images/projects/example/destination-a.jpg" alt="" />
    <h3 slot="headline"><a href="/path-a">Destination A</a></h3>
    <a slot="cta-icon" href="/path-a">Explore</a>
  </umd-element-card-overlay>
  <!-- repeat for each destination -->
</div>
```

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

## Utility Navigation Slot (`slot="utility-navigation"`)

The canonical production pattern (matches umd.edu). CSS lives in `critical.css` §11 — see RULES.md §4 for the gotchas (link color reset + `gap:0` override are mandatory). Each item is `.umd-shell-utility-item` → `.umd-shell-utility-actions` → `<a class="umd-sans-smaller">`. The `:not(:last-child)` separator border comes for free from the base layer.

```html
<div slot="utility-navigation">
  <!-- Plain link item -->
  <div class="umd-shell-utility-item">
    <div class="umd-shell-utility-actions">
      <a class="umd-sans-smaller" href="/give">Give</a>
    </div>
  </div>

  <!-- Search item — DS magnifying-glass SVG, icon right of text -->
  <div class="umd-shell-utility-item">
    <div class="umd-shell-utility-actions">
      <a class="umd-sans-smaller" href="/search" style="display:inline-flex;align-items:center;gap:5px;">
        Search
        <svg aria-hidden="true" width="14" height="14" viewBox="0 0 96 96" fill="currentColor" style="flex-shrink:0;">
          <path fill-rule="evenodd" clip-rule="evenodd" d="M79.3401 42.2306C79.3401 54.1438 69.6826 63.8013 57.7694 63.8013C45.8562 63.8013 36.1987 54.1438 36.1987 42.2306C36.1987 30.3174 45.8562 20.6599 57.7694 20.6599C69.6826 20.6599 79.3401 30.3174 79.3401 42.2306ZM91 42.2306C91 60.5833 76.1222 75.4612 57.7694 75.4612C51.3447 75.4612 45.3458 73.6379 40.2619 70.4806L24.2216 86.5209H5L30.2245 60.8255C26.6351 55.5189 24.5388 49.1195 24.5388 42.2306C24.5388 23.8778 39.4167 9 57.7694 9C76.1222 9 91 23.8778 91 42.2306Z"/>
        </svg>
      </a>
    </div>
  </div>
</div>
```

### Dropdown item (production `aria-hidden` toggle)

The DS has **no native dropdown** for this slot. Production uses a `<button>` toggle + a sibling `.umd-shell-utility-links[aria-hidden]` panel, with JS flipping `aria-hidden` / `aria-expanded`. The panel CSS (positioning, show/hide, chevron rotation) is already in `critical.css` §11.

```html
<div class="umd-shell-utility-item">
  <div class="umd-shell-utility-actions">
    <button class="umd-sans-smaller" aria-controls="giving-dropdown" aria-expanded="false" aria-label="Toggle for Giving links">
      <span aria-hidden="true">Giving</span>
      <svg aria-hidden="true" width="11" height="7" viewBox="0 0 11 7" fill="none">
        <path fill-rule="evenodd" clip-rule="evenodd" d="M5.3136 3.70222L8.16278 0.5L10.625 0.500009L6.63731 5.18995L6.63916 5.19202L5.31635 6.75L5.3136 6.74677L5.31086 6.74999L3.98805 5.19201L3.98989 5.18995L0.00221157 0.500005L2.46443 0.500007L5.3136 3.70222Z"/>
      </svg>
    </button>
  </div>
  <div id="giving-dropdown" class="umd-shell-utility-links" aria-hidden="true">
    <a class="umd-sans-smaller" href="#"><span>Make a Gift</span></a>
    <a class="umd-sans-smaller" href="#"><span>Scholarship Fund</span></a>
  </div>
</div>
```

```html
<!-- Toggle script: click opens, click outside closes -->
<script>
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('button[aria-controls]');
    if (btn) {
      var panel = document.getElementById(btn.getAttribute('aria-controls'));
      if (!panel) return;
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', open ? 'false' : 'true');
      panel.setAttribute('aria-hidden', open ? 'true' : 'false');
      e.stopPropagation();
      return;
    }
    document.querySelectorAll('.umd-shell-utility-links[aria-hidden="false"]').forEach(function (panel) {
      panel.setAttribute('aria-hidden', 'true');
      var ctrl = document.querySelector('[aria-controls="' + panel.id + '"]');
      if (ctrl) ctrl.setAttribute('aria-expanded', 'false');
    });
  });
</script>
```
