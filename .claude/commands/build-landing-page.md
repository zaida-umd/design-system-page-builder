# Build a Sample Landing Page

Build a complete UMD landing page HTML file and save it to `/test/` in the main repo.

## Phase 0 — Design evaluation (run before writing any HTML)

Before touching a file, act as an objective design critic. This prevents generating mediocre output and self-approving it.

1. Read `umd-component-registry.json` to know all available components and variants.
2. For each required section below, state **why** you chose that component over alternatives, which attributes you'll use, and what content fills each slot.
3. Score the proposed plan on four dimensions (0–10 each):
   - **Component fitness** — best component for the content type, not just a safe default
   - **Layout variety** — at least 3 distinct visual patterns; penalize if the same section type repeats more than twice
   - **Content hierarchy** — clear path from hero → value → evidence → CTA
   - **Design integrity** — RULES.md compliance (theme, spacing, slot names) in the plan
4. If any dimension scores below 6, revise the plan before proceeding. State the revised score.
5. List any known component-specific risks (e.g. slot name gotchas, required attributes, full-bleed constraints).
6. Only proceed to HTML after the plan scores ≥ 24/40 with no dimension below 6.

Output the evaluation as a brief design plan with scores before writing the first line of HTML.

---

## Setup

1. Read `TEMPLATE.html` — use its full `<head>` block (critical CSS + cdn.js script) verbatim. Do not rebuild it.
2. Read `umd-component-registry.json` — use it as the source of truth for all slots and attributes.
3. Follow every rule in `RULES.md` exactly.

## Page identity

Use a content and images from https://gradschool.umd.edu/ as the fictional client. Name the output file  `test/test-landing.html`. You will override this file.

## Required sections — use this order

1. **Utility header** — `<umd-element-utility-header>` (hardcoded, no config)
2. **Navigation header** — `<umd-element-navigation-header sticky class="umd-layout-space-horizontal-full">` with logo and nav items from https://gradschool.umd.edu/ 
3. **Hero** — `umd-element-hero` with `data-theme="dark" data-animation`. Include headline, subhead text and a primary CTA. Use assets - video or image - from https://gradschool.umd.edu/.
4. **Section Intro** — `umd-element-section-intro` with `include-separator`. Include text only, no headline or CTA: "The University of Maryland is located just steps from the US capitol of Washington, DC - a global center of science, politics, business, and culture. This prime location gives students unparalleled access to national research and policy institutions, performing and visual arts, and national and international decision makers.".
4. **Pathway (left image)** — `umd-element-pathway data-display="overlay" data-theme="light"` for the Choose Maryland content.
5. **Pathway (right image)** — same as above but add `data-layout-image-position="right"` for Grand Challenges Graduate Communities content.
6. **Stats section** — `<section class="umd-layout-vertical-landing">` with a `umd-layout-space-horizontal-larger` wrapper. Include `umd-element-section-intro` + a grid of **3 stats** using `umd-element-stat data-visual-size="large" data-decoration-line`. Follow the stats grid layout rules from RULES.md §9. Always use `slot="text"` for stat labels (RULES.md §11).
7. **Card grid** — `<section class="umd-layout-vertical-landing">` with `umd-layout-space-horizontal-larger` wrapper. Include `umd-element-section-intro-wide` with a "View All" CTA + a 3-column grid of `umd-element-card` (news/story cards). Each card gets headline (linked), image, text blurb. These news stories are on https://gradschool.umd.edu/ 
8. **Image expand quote** — `<section style="background:#000;" class="umd-layout-vertical-landing">` wrapping `umd-layout-image-expand`. Place a `umd-element-quote data-display="featured" data-theme="dark" data-visual-transparent="true"` inside the `slot="content"` div. Always add `data-visual-transparent="true"` — without it the quote renders an opaque background card that blocks the image. Constrain and align with `style="display: block; width: 100%; max-width: 480px; margin-left: auto;"` on the content div (or `margin-right: auto` for left-aligned). Do **not** add `color: white` inline styles — `data-theme="dark"` handles text color when `data-visual-transparent="true"` is present. See RULES.md §17.
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

## Output

Write the completed HTML file to `/test/test-landing.html`. Confirm the filename when done.
