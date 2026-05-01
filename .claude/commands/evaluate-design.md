# Evaluate a Page Design

Review a proposed page plan for design problems **before any HTML is written**. Catch design mistakes — not enforce hard rules (those live in `RULES.md` and are checked by the build commands).

## Input

The page concept is: `$ARGUMENTS`

If no concept is provided, ask the user to describe the page they want to build.

---

## Step 1 — Read context files

1. Read `registry/registry-index.json` — category map and `lookup_by_tag`. Then read the category files relevant to the page's content types (typically heroes, cards, content; add feeds/carousel/quote/etc. as needed).
2. Read `RULES.md` — full file. The hard layout/spacing/component rules are checked here, not in this command.
3. Read `LAYOUT-PATTERNS.md` for HTML pattern recipes (rich text, grids, dark sections, masonry).
4. If a specific page URL is mentioned, fetch it to understand the content.

---

## Step 2 — Propose a component plan

For each section of the page, state:
- The component name (exact tag from the registry)
- Why this component fits the content better than alternatives
- What variant/attributes you'll use (theme, display mode, layout position)
- What content goes in each slot

Format:

```
### Section [N]: [Component tag]
- **Why this component:** ...
- **Attributes:** data-theme="...", data-display="...", etc.
- **Slots:** slot="headline" → ..., slot="text" → ..., etc.
- **Alternatives considered:** [tag] — rejected because ...
```

---

## Step 3 — Design checks

Walk the plan against these design-judgment checks. Each is a *mistake to catch*, not a score. Hard mechanical rules (theme cascade, slot names, spacing classes, full-bleed wrappers) are enforced by `RULES.md` — do not restate them here.

### Layout rhythm and variety

- **Card-layout variety across multiple card sections.** When a page has more than one card-based section, do not use the same card type for all of them. Mix `umd-element-card` (standard), `umd-element-card-overlay type="image"`, `umd-element-card-overlay` (no image, link-style), `umd-element-card-icon`, and masonry grids so each section reads as visually distinct. Two consecutive sections of standard cards is the most common offender — convert one to image-overlay or masonry. If the page already has imageless overlay cards, prefer image-overlay (not another standard set) for the next card section.
- **Duplicate card-overlay CTA rows.** When `umd-element-card-overlay` is used to replace a row of standalone CTAs or navigation links — no images, no body copy in the original — and that pattern appears twice on the page, flag it as repetitive. Differentiate the secondary set by converting to `umd-element-card-icon`. Use `icon-link.svg` for internal links, `icon-new-window.svg` for external; use `-dark` icon variants on `data-theme="dark"` cards. Reserve `umd-element-card-overlay` for the set where the content is richer or more featured.
- **Standalone link rows → card-overlay.** If a section contains only 2–4 standalone navigation links with no supporting body copy, use `umd-element-card-overlay` (no image, with `slot="cta-icon"`) in a grid instead of secondary CTAs in `umd-layout-grid-inline-tablet-rows`. See `LAYOUT-PATTERNS.md` "Link Cards Grid" section.
- **Section rhythm.** A landing page should rotate through full-bleed, narrow, wide treatments. Penalize three consecutive sections that share the same width and treatment.

### Dark theming and visual weight

- **Dark theme overuse — judgment, not a count.** Dark sections near the top of a landing page are intentional and correct. A dark hero (overlay, standard/background, or stacked) naturally leads into one or two dark sections below it to maintain visual weight. Do not penalize this. Penalize dark theming that continues into the lower half of the page on content-heavy sections (events lists, news feeds, program grids) where scannability matters. If a section's primary purpose is content scanning, prefer light background + watermark. The test: dark sections should feel like a bold, purposeful band — not the default that every section defaults to.
- **Adjacent dark sections — gap rule.** See `RULES.md §19` for the mechanical rule (omit `umd-layout-vertical-landing` from the preceding dark section). The design check: if you are about to chain three or more dark sections together, ask whether a light section between them would improve scannability — chaining dark beyond two sections almost always reads as monotonous. If you keep them, the gap must be eliminated; if you can't eliminate the gap (because the design needs spacing), switch the second section to light.

### Section intros — visual enrichment

- **Consecutive watermark intros.** `umd-element-section-intro-wide` with a watermark in back-to-back sections is too much — each watermark competes with the other and neither reads clearly. Alternate: use `umd-element-section-intro` (centered, no watermark) for one, or use a watermark only on the section where the visual richness adds the most value. Never place two watermarked section intros adjacent to each other.
- **Plain section-intros on featured sections.** `umd-element-section-intro` supports `include-separator`, which adds a decorative red vertical line above the headline. Use it when the section anchors a significant block (especially on dark or featured backgrounds). Don't leave section intros plain when the section warrants visual weight.
- **section-intro-wide watermark depth.** `umd-element-section-intro-wide` benefits from a watermark word for visual depth. Split the section label: keep a short topical title in `slot="headline"` and add `<div class="umd-watermark" aria-hidden="true"><span>[WORD]</span></div>` as the first child of the containing horizontal-space div. Example: headline = "UMD INFO", watermark = "News".

### Component-context judgment

- **`umd-layout-image-expand` background context.** Wrap in a dark section (`background:#000` or `umd-layout-background-full-dark`) only when image-expand sits between other dark sections. On a predominantly light page, the built-in dark overlay is sufficient — adding a dark wrapper creates an isolated dark island. (For text-color rules inside the content slot, see `RULES.md §17`.)
- **Hero variant fit.** `umd-element-hero` (no `data-display`) is the default. `data-display="overlay"` is a specific design choice for a composited overlay panel — flag it if it's been chosen by default rather than for the overlay effect. (See `RULES.md §22`.)

---

## Step 4 — Component-specific risks

Any component-specific rule that fails silently or produces broken output is a hard rule and lives in `RULES.md`. When the plan includes one of these, link to the rule rather than restating it:

- `umd-element-stat` slot names — `RULES.md §11`
- `umd-element-event` `display` vs `data-display` — `RULES.md §26`
- `umd-element-quote data-display="featured"` actions slot wrapper — `RULES.md §28`
- `umd-element-card-overlay type="image"` requirement for image backgrounds — `RULES.md §16`
- `umd-layout-image-expand` text color and quote transparency — `RULES.md §17`
- Footer visual variant non-empty `alt` — `RULES.md §29`
- Standard card `data-visual-image-aligned="true"` default — `RULES.md §30`
- Section-intro + masonry compensation CSS — `LAYOUT-PATTERNS.md` "Masonry compensation rule"

Flag any others you spot during planning that aren't yet documented — those are candidates for promotion into `RULES.md`.

---

## Step 5 — Output

Produce a brief in this format:

```
## Design Review: [Page Title]
**Date:** [today's date]

### Component Plan
[Section-by-section plan from Step 2]

### Design Checks
[Issues caught from Step 3 — or "no issues" if clean. Be specific: name the section, the problem, and the fix.]

### Component-specific risks
[Bulleted list from Step 4 of rules that apply to chosen components]

### Recommendation
[PROCEED — plan is sound] OR [REVISE — see issues above]
```

No score. The recommendation is binary: either the plan has design issues that need fixing, or it doesn't.

---

## Usage

```
/evaluate-design A landing page for UMD's College of Engineering featuring research highlights, faculty spotlights, and an application CTA
```
