# Build a Sample Interior Page

Build a complete UMD interior/subpage HTML file using real content from the "Traditions of the Past" page (`https://umd.edu/about/traditions-of-the-past`). Save it to `test/test-interior-page.html`.


## Setup

1. Read `TEMPLATE.html` — use its full `<head>` block (critical CSS + cdn.js script) verbatim. The CSS comes from `styles/critical.css` (single source of truth for all CSS rules).
2. Registry files in `registry/` are the source of truth for all slots and attributes.
3. Follow every rule in `RULES.md` exactly.
4. Read `LAYOUT-PATTERNS.md` for HTML patterns when using rich text sections, dark backgrounds, two-column grids, or inline CTA rows.

---

## Page identity

**File:** `test/test-interior-page.html`

This is the "Traditions of the Past" subpage from `umd.edu/about/traditions-of-the-past`.

**Breadcrumb:** Home → Traditions & History → Traditions of the Past

**Eyebrow:** History & Traditions

**H1:** Traditions of the Past

---

## Required sections — use this order

### 1. Global university navigation (full-width, outside page wrapper)

```html
<umd-element-navigation-utility data-alert-off="true" role="navigation" aria-label="Utility navigation"></umd-element-navigation-utility>
```

### 2. Site header (full-width, outside page wrapper)

```html
<umd-element-utility-header></umd-element-utility-header>
```

### 3. Navigation header (full-width, outside page wrapper)

`umd-element-navigation-header` with `sticky` attribute and `class="umd-layout-space-horizontal-full"`.

- Logo: `slot="logo"` → `<a href="/"><img src="../images/logos/primary-logo-dark.svg" alt="University of Maryland" /></a>`
- Nav items: About, Traditions & History (active), Alumni, Give

### 4. Hero — background hero small, centered text

`umd-element-hero` with `data-layout-height="small"` and `data-layout-text="center"`.

- Wrap in `<section>` with **no** spacing class (dark section does not need `umd-layout-vertical-landing` — the content below starts inside the 800px column with its own spacing).
- `slot="eyebrow"`: `<p slot="eyebrow">History &amp; Traditions</p>` (≤16 chars ✓)
- `slot="headline"`: `<h1 slot="headline">Traditions of the Past</h1>`
- `slot="image"`: `<img slot="image" src="../images/large/campus/shaking.webp" alt="Students holding newspapers up during a game" />`

### 5. Breadcrumb (inside outer wrapper, before columns)

Wrap in `<div class="umd-layout-space-horizontal-larger umd-layout-space-vertical-interior">`:

```html
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/about/history">Traditions &amp; History</a></li>
    <li aria-current="page">Traditions of the Past</li>
  </ol>
</nav>
```

### 6. Sidebar + content column layout

This is the core interior layout. Use these exact production classes — **do not write custom CSS**:

```html
<div class="umd-layout-space-horizontal-larger">
  <div class="umd-layout-space-columns-left">

    <!-- Sidebar: left nav (hidden below 1024px via built-in CSS) -->
    <div id="umd-shell-sidebar-container">
      <umd-element-nav-slider>
        <nav slot="primary-slide-links">
          <a href="/about">About UMD</a>
          <a href="/about/history">History &amp; Traditions</a>
          <a href="/about/traditions-of-the-past">Traditions of the Past</a>
          <a href="/about/symbols">University Symbols</a>
          <a href="/about/fight-song">Fight Song</a>
        </nav>
      </umd-element-nav-slider>
    </div>

    <!-- Main content column: constrained to 800px -->
    <div id="umd-shell-content" class="max-w-[800px]">

      <!-- sections go here — see below -->

    </div>
  </div>
</div>
```

**`max-w-[800px]`** is a Tailwind utility class. Add it to the critical CSS block in `<head>`:
```css
.max-w-\[800px\] { max-width: 800px; }
```

### 7. Content sections (inside `max-w-[800px]` content column)

Use `umd-layout-space-vertical-interior` between sections and `umd-layout-space-vertical-interior-child` between heading and content within a section.

#### Section A — Beanies (H2 + image left + text)

```html
<section class="umd-layout-space-vertical-interior">
  <h2 class="umd-layout-space-vertical-interior-child">Beanies</h2>
  <umd-element-media-inline>
    <img slot="image" src="../images/small/people/freshman-beanie.webp" alt="Young student wearing a beanie and a sign saying I can't help it (I'm a freshman)" />
    <div slot="text" class="umd-text-rich-advanced">
      <p>From the 1910s to the 1960s, freshman students were required to wear beanies everywhere they went on campus, from their first day of school until the freshmen-sophomore tug-of-war, held during the spring semester. The beanies were known as "rat caps" for the men, and "rabbit caps" for the women.</p>
    </div>
  </umd-element-media-inline>
</section>
```

#### Section B — Byrd Beach (H3 + image right + text)

```html
<section class="umd-layout-space-vertical-interior">
  <h3 class="umd-layout-space-vertical-interior-child">Byrd Beach</h3>
  <umd-element-media-inline data-layout-alignment="right">
    <img slot="image" src="../images/small/campus/Students-at-Byrd-Beach-1985.webp" alt="Students at Byrd Beach 1985" />
    <div slot="text" class="umd-text-rich-advanced">
      <p>For decades, until everyday access to the football stadium was cut off, students greeted the return of springtime warmth by donning their bathing suits and stretching out along the bleachers in then-Byrd Stadium to study, tan and people-watch.</p>
    </div>
  </umd-element-media-inline>
</section>
```

#### Section C — Class Wars (H3 + image left + multi-paragraph text)

```html
<section class="umd-layout-space-vertical-interior">
  <h3 class="umd-layout-space-vertical-interior-child">Class Wars</h3>
  <umd-element-media-inline>
    <img slot="image" src="../images/small/people/tug-of-war2.webp" alt="Vintage photo of students playing tug of war" />
    <div slot="text" class="umd-text-rich-advanced">
      <p>What happened when the beanie-wearing freshmen squared off against their arch-nemesis, the sophomore class? In the early part of the 20th century, the competition involved first- and second-year students playing King of the Mountain on a 120-foot iron water tower located on campus.</p>
      <p>This tradition continued until 1913 when wily sophomore Robert McCutcheon knocked down the freshman flag with a well-aimed rifle shot that severed its staff.</p>
      <p>This annual struggle between the freshman and sophomore classes during the spring semester marked the end of the beanie-wearing season for the freshman. The traditional contest over Paint Branch Creek began about 1915 and continued into the early 1950s.</p>
    </div>
  </umd-element-media-inline>
</section>
```

#### Section D — Kissing Tunnel (H3 + text only, no image)

```html
<section class="umd-layout-space-vertical-interior">
  <h3 class="umd-layout-space-vertical-interior-child">Kissing Tunnel</h3>
  <div class="umd-text-rich-advanced">
    <p>Located beneath Regents Drive south of Memorial Chapel, the historic Kissing Tunnel got its name by being a popular stop after a College Park date night back in the 1950s and 1960s, when all residence halls were single-gender.</p>
  </div>
</section>
```

#### Section E — May Day (H3 + image right + text)

```html
<section class="umd-layout-space-vertical-interior">
  <h3 class="umd-layout-space-vertical-interior-child">May Day</h3>
  <umd-element-media-inline data-layout-alignment="right">
    <img slot="image" src="../images/small/people/may-day.webp" alt="Vintage photo of young women in formal light dresses seated around a woman in a large seat" />
    <div slot="text" class="umd-text-rich-advanced">
      <p>Adele H. Stamp, the university's dean of women from 1922 to 1960, began the tradition of celebrating May Day at Maryland. The ceremony, last held in 1961, featured a Maypole dance, pageant, Mortar Board tapping for senior women and crowning of the queen.</p>
    </div>
  </umd-element-media-inline>
</section>
```

### 8. Footer (full-width, outside page wrapper)

```html
<footer class="overflow-hidden">
  <umd-element-footer data-display="visual" data-theme="dark">
    <a slot="logo" href="/"><img src="../images/logos/footer-logo.svg" alt="University of Maryland" /></a>
  </umd-element-footer>
</footer>
```

---

## Layout structure summary

```
<umd-element-navigation-utility>     ← full-width
<umd-element-utility-header>         ← full-width
<umd-element-navigation-header>      ← full-width

<section>                            ← hero (full-width, no spacing class)
  <umd-element-hero data-layout-height="small" data-layout-text="center">

<div class="umd-layout-space-horizontal-larger umd-layout-space-vertical-interior">
  breadcrumb nav

<div class="umd-layout-space-horizontal-larger">
  <div class="umd-layout-space-columns-left">
    <div id="umd-shell-sidebar-container">      ← 242px, hidden <1024px
      <umd-element-nav-slider>
    <div id="umd-shell-content" class="max-w-[800px]">
      <section class="umd-layout-space-vertical-interior"> × 5  ← traditions content

<footer>
  <umd-element-footer>
```

---

## Critical CSS

All interior page CSS (`.umd-layout-space-columns-left`, `.max-w-[800px]`, interior spacing aliases, media-inline registration, etc.) is already included in `TEMPLATE.html` via `styles/critical.css`. No additional CSS rules need to be added — use the template's `<head>` block verbatim.

---

## Rules checklist before saving

- [ ] No `umd-layout-vertical-landing` on any interior section
- [ ] `umd-layout-space-columns-left` used (not a custom grid)
- [ ] Left nav uses `slot="primary-slide-links"` with bare `<a>` elements
- [ ] Hero eyebrow ≤ 16 characters
- [ ] No broken logo images — `../images/logos/primary-logo-dark.svg` (header), `../images/logos/footer-logo.svg` (footer)
