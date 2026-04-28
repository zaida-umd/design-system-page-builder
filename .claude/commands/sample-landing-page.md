# Sample Landing Page

Build a sample/test UMD landing page from this fixed recipe — known set of design system components, content from `https://gradschool.umd.edu/`, output to `/test/test-landing.html`. This command does NOT take a brief or fresh content. For a brief-driven landing page, use `/build-landing-page` instead. For converting a real existing page, use `/recreate-page`.


## Setup

1. Read `TEMPLATE.html` — use its full `<head>` block (critical CSS + cdn.js script) verbatim. Do not rebuild it. The CSS comes from `styles/critical.css` (single source of truth for all CSS rules).
2. Read `registry/registry-index.json` for the category map, then load only the category files you need for this page's content types.
3. Follow every rule in `RULES.md` exactly.
4. Read `LAYOUT-PATTERNS.md` for HTML patterns when using rich text sections, dark backgrounds, two-column grids, or inline CTA rows.

## Page identity

Use a content and images from https://gradschool.umd.edu/ as the fictional client. Name the output file  `test/test-landing.html`. You will override this file.

## Required sections — use this order

1. **Global university header** — `<umd-element-navigation-utility data-alert-off="true" role="navigation" aria-label="Utility navigation"></umd-element-navigation-utility>` (hardcoded, no config, never omit — this is the UMD-wide bar from umd.edu)
2. **Site utility header** — `<umd-element-utility-header></umd-element-utility-header>` (hardcoded, no config)
3. **Navigation header** — `<umd-element-navigation-header sticky class="umd-layout-space-horizontal-full">` with logo using `../images/logos/primary-logo-dark.svg` and nav items from https://gradschool.umd.edu/
3. **Hero** — `umd-element-hero` with `data-theme="dark" data-animation data-layout-text="center"`. Include headline, subhead text and a primary CTA. Use assets - video or image - from https://gradschool.umd.edu/.
4. **Section Intro** — `umd-element-section-intro` with `include-separator` inside `<section class="umd-layout-vertical-landing">` wrapper. Include text only, no headline or CTA: "The University of Maryland is located just steps from the US capitol of Washington, DC - a global center of science, politics, business, and culture. This prime location gives students unparalleled access to national research and policy institutions, performing and visual arts, and national and international decision makers.".
4. **Pathway (right image)** — `umd-element-pathway data-display="overlay" data-theme="light"` for the Choose Maryland content.
5. **Pathway (left image)** — same as above but add `data-layout-image-position="left"` for Grand Challenges Graduate Communities content.
6. **Stats section** — `<section class="umd-layout-vertical-landing">` with a `umd-layout-space-horizontal-larger` wrapper. Include a grid of **3 stats** using `umd-element-stat data-visual-size="large" data-decoration-line`. Follow the stats grid layout rules from RULES.md §9. Always use `slot="text"` for stat labels (RULES.md §11).
7. **Card grid** — `<section class="umd-layout-vertical-landing">` with `umd-layout-space-horizontal-larger` wrapper. Include `umd-element-section-intro-wide` with a "View All" CTA + a 3-column grid of `umd-element-card-overlay type="image"` (news/story cards). **`type="image"` is required** — without it the image slot is ignored and the card renders text-only. Each card gets headline (linked), image, text blurb. These news stories are on https://gradschool.umd.edu/ — **always use local library images for card-overlay** (remote Drupal URLs block hotlinking). Read `images/images-index.json`, use the `small` tier, match each story's context to the closest tag (`people`, `research`, `campus`, `events`), and reference as `../images/small/{path}`.
8. **Image expand quote** — `<section class="umd-layout-vertical-landing">` wrapping `umd-layout-image-expand`. Do **not** add a black background to the section unless a dark theme or black background is explicitly requested. Place a `umd-element-quote data-display="featured" data-theme="dark" data-visual-transparent="true"` directly inside `div[slot="content"]`. Always add `data-visual-transparent="true"` — without it the quote renders an opaque background card that blocks the image. Apply `class="block max-w-[480px] w-full mr-auto"` directly on the `div[slot="content"]` element (not a child wrapper). Include these CSS rules in your `<style>` block: `.max-w-\[480px\] { max-width: 480px; } .w-full { width: 100%; } .block { display: block; } .mr-auto { margin-right: auto; }`. Do **not** add `color: white` inline styles — `data-theme="dark"` handles text color when `data-visual-transparent="true"` is present. See RULES.md §17.
9. **Footer** — `<umd-element-footer data-display="visual">` with logo and campus background image. Always use `../images/logos/footer-logo.svg` for `slot="logo"` and `../images/large/campus/footer-campus.jpg` for `slot="image"`. The `slot="image"` `alt` must be non-empty (e.g., `alt="University of Maryland campus"`) — the visual footer drops the slotted image entirely if `alt=""` and does not fall back to the default. Do not add contact info, address, or social links to the visual footer — the visual variant renders the logo and image only.

## Content guidelines

- Use content from https://gradschool.umd.edu/
- Hero should use current image or video from https://gradschool.umd.edu/ hero: https://gradschool.umd.edu/sites/default/files/2023-02/Campus%20Beauties_Loop_1.mp4
- Stat values should be plausible for a top-20 research university (e.g. "$900M+ Research expenditures", "3,400 Undergraduate students", "150+ Faculty").
- CTA links: use links that occur on https://gradschool.umd.edu/.
- Do not invent eyebrow slots unless the content naturally has a category label (RULES.md §13).

## Spacing and layout

- Every top-level `<section>` gets `class="umd-layout-vertical-landing"`.
- Pathway and hero are full-bleed — do NOT wrap in a horizontal spacing class.
- Card grids and section intros go inside a `umd-layout-space-horizontal-larger` wrapper.
- `data-theme` does not cascade — set it on every child component that needs it (RULES.md §14).

## Image fallback

See CLAUDE.md §Images for the full fallback lookup procedure.

## Output

Write the completed HTML file to `/test/test-landing.html`. Confirm the filename when done.
