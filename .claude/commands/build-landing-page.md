# Build a Sample Landing Page

Build a complete UMD landing page HTML file and save it to `/test/` in the main repo.


## Setup

1. Read `TEMPLATE.html` — use its full `<head>` block (critical CSS + cdn.js script) verbatim. Do not rebuild it.
2. Registry files in `registry/` are the source of truth for all slots and attributes (already read above).
3. Follow every rule in `RULES.md` exactly.

## Page identity

Use a content and images from https://gradschool.umd.edu/ as the fictional client. Name the output file  `test/test-landing.html`. You will override this file.

## Required sections — use this order

1. **Global university header** — `<umd-element-navigation-utility data-alert-off="true" role="navigation" aria-label="Utility navigation"></umd-element-navigation-utility>` (hardcoded, no config, never omit — this is the UMD-wide bar from umd.edu)
2. **Site utility header** — `<umd-element-utility-header></umd-element-utility-header>` (hardcoded, no config)
3. **Navigation header** — `<umd-element-navigation-header sticky class="umd-layout-space-horizontal-full">` with logo from here: https://umd-main.files.svdcdn.com/production/umd/logos/default/primary-logo-dark.svg?dm=1722455539 and nav items from https://gradschool.umd.edu/
3. **Hero** — `umd-element-hero` with `data-theme="dark" data-animation data-layout-text="center"`. Include headline, subhead text and a primary CTA. Use assets - video or image - from https://gradschool.umd.edu/.
4. **Section Intro** — `umd-element-section-intro` with `include-separator` inside `<section class="umd-layout-vertical-landing">` wrapper. Include text only, no headline or CTA: "The University of Maryland is located just steps from the US capitol of Washington, DC - a global center of science, politics, business, and culture. This prime location gives students unparalleled access to national research and policy institutions, performing and visual arts, and national and international decision makers.".
4. **Pathway (right image)** — `umd-element-pathway data-display="overlay" data-theme="light"` for the Choose Maryland content.
5. **Pathway (left image)** — same as above but add `data-layout-image-position="left"` for Grand Challenges Graduate Communities content.
6. **Stats section** — `<section class="umd-layout-vertical-landing">` with a `umd-layout-space-horizontal-larger` wrapper. Include a grid of **3 stats** using `umd-element-stat data-visual-size="large" data-decoration-line`. Follow the stats grid layout rules from RULES.md §9. Always use `slot="text"` for stat labels (RULES.md §11).
7. **Card grid** — `<section class="umd-layout-vertical-landing">` with `umd-layout-space-horizontal-larger` wrapper. Include `umd-element-section-intro-wide` with a "View All" CTA + a 3-column grid of `umd-element-card-overlay type="image"` (news/story cards). **`type="image"` is required** — without it the image slot is ignored and the card renders text-only. Each card gets headline (linked), image, text blurb. These news stories are on https://gradschool.umd.edu/ — **always use local library images for card-overlay** (remote Drupal URLs block hotlinking). Read `images/images-index.json`, use the `small` tier, match each story's context to the closest tag (`people`, `research`, `campus`, `events`), and reference as `../images/small/{path}`.
8. **Image expand quote** — `<section class="umd-layout-vertical-landing">` wrapping `umd-layout-image-expand`. Do **not** add a black background to the section unless a dark theme or black background is explicitly requested. Place a `umd-element-quote data-display="featured" data-theme="dark" data-visual-transparent="true"` directly inside `div[slot="content"]`. Always add `data-visual-transparent="true"` — without it the quote renders an opaque background card that blocks the image. Apply `class="block max-w-[480px] w-full mr-auto"` directly on the `div[slot="content"]` element (not a child wrapper). Include these CSS rules in your `<style>` block: `.max-w-\[480px\] { max-width: 480px; } .w-full { width: 100%; } .block { display: block; } .mr-auto { margin-right: auto; }`. Do **not** add `color: white` inline styles — `data-theme="dark"` handles text color when `data-visual-transparent="true"` is present. See RULES.md §17.
9. **Footer** — `<umd-element-footer>` with logo, department name, address, phone, email, and social links.

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

When a real image URL is unavailable (hotlink protection, dynamically loaded content, no source image):
1. Read `/Users/zjocson/repos/design-system-page-builder/images/images-index.json`
2. Determine the size tier: **large** for heroes, pathways, image-expand — **small** for cards
3. Match the content context to the closest tag (`campus`, `people`, `events`, `research`)
4. If no tag match, collect all entries with `"default": true` in the correct tier and pick one at random
5. Reference the image as a repo-relative path: `../images/large/campus/filename.jpg`

## Output

Write the completed HTML file to `/test/test-landing.html`. Confirm the filename when done.
