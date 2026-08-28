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
- **Card-grid budget.** Well-built pages carry only **1–2 true card-grid sections** and never repeat the same card treatment twice — variety comes from rotating the component type (overlay / icon / aligned standard / carousel-wrapped) *and* the grid shape (2-up, 3-up, 4-up, masonry, no-gap). Flag a plan with 3+ card grids: convert the weakest to a list treatment (next check), a pathway, or cut it.
- **Card vs list — when a grid is the wrong shape.** Cards are for scannable, parallel content where each item has a strong image and short copy. Switch to a **list treatment** — `umd-element-card data-display="list"` stacked rows (optionally inside sticky-columns), an accordion stack, or rich-text columns/tables — when any of these hold. No fixed item count; judge by image strength and copy density:
  - **Photography is uncompelling, secondary, or unavailable.** Don't force weak or utility-grade images into a grid; a list de-emphasizes them (or drops them entirely via accordion/rich text).
  - **The page has already spent its card budget.** If earlier sections used the card treatments, render the next collection as a list rather than a third grid.
  - **The page needs white space.** A list with one featured item (or a plain stacked list) reads calmer than another wall of tiles — use it deliberately to lower density.
  - **The content is procedural or reference material** — deadlines, steps, rosters, resource links. These want rich-text columns, a table, or accordions, not cards.
- **Duplicate card-overlay CTA rows.** When `umd-element-card-overlay` is used to replace a row of standalone CTAs or navigation links — no images, no body copy in the original — and that pattern appears twice on the page, flag it as repetitive. Differentiate the secondary set by converting to `umd-element-card-icon`. Use `icon-link.svg` for internal links, `icon-new-window.svg` for external; use `-dark` icon variants on `data-theme="dark"` cards. Reserve `umd-element-card-overlay` for the set where the content is richer or more featured.
- **Standalone link rows → card-overlay.** If a section contains only 2–4 standalone navigation links with no supporting body copy, use `umd-element-card-overlay` (no image, with `slot="cta-icon"`) in a grid instead of secondary CTAs in `umd-layout-grid-inline-tablet-rows`. See `LAYOUT-PATTERNS.md` "Link Cards Grid" section.
- **Section rhythm.** A landing page should rotate through full-bleed, narrow, wide treatments. Penalize three consecutive sections that share the same width and treatment.
- **Palate cleansers between heavy bands.** Flag any two adjacent *heavy* sections — dark bands, dense card grids, long pathway runs — with no low-density break between them. The fixes, all proven in real projects: a standalone `umd-element-quote` (locked to `umd-layout-space-horizontal-normal`), a 3-up imageless stat row, a full-bleed `umd-layout-image-expand` + featured quote as a mid-page reset, or a whitespace intro (eyebrow + rich text in a narrow lock). Quotes and stats are not filler — they are the breathing room that makes the heavy sections land.

### Dark theming and visual weight

- **Dark theme overuse — judgment, not a count.** Dark sections near the top of a landing page are intentional and correct. A dark hero (overlay, standard/background, or stacked) naturally leads into one or two dark sections below it to maintain visual weight. Do not penalize this. Penalize dark theming that continues into the lower half of the page on content-heavy sections (events lists, news feeds, program grids) where scannability matters. If a section's primary purpose is content scanning, prefer light background + watermark. The test: dark sections should feel like a bold, purposeful band — not the default that every section defaults to.
- **Adjacent dark sections — gap rule.** See `RULES.md §19` for the mechanical rule (omit `umd-layout-vertical-landing` from the preceding dark section). The design check: if you are about to chain three or more dark sections together, ask whether a light section between them would improve scannability — chaining dark beyond two sections almost always reads as monotonous. If you keep them, the gap must be eliminated; if you can't eliminate the gap (because the design needs spacing), switch the second section to light.

### Section intros — visual enrichment

- **Watermarks — restrained accent, not a default.** A watermark word is a decorative accent for **at most one section per page** — the single most featured band — not a standard enrichment for every `section-intro-wide`. Real project pages use zero or one watermark; flag a plan with two or more, and never place watermarked intros adjacent. When one is warranted, split the section label: short topical title in `slot="headline"`, plus `<div class="umd-watermark" aria-hidden="true"><span>[WORD]</span></div>` as the first child of the containing horizontal-space div (e.g. headline "UMD INFO", watermark "News"). Default for everything else: no watermark.
- **Plain section-intros on featured sections.** `umd-element-section-intro` supports `include-separator`, which adds a decorative red vertical line above the headline. Use it when the section anchors a significant block (especially on dark or featured backgrounds). Don't leave section intros plain when the section warrants visual weight.
- **Intros are optional — image-led card sections can open cold.** Not every section needs a section-intro. On production umd.edu pages, strong card sections (a feature grid right after the hero, a masonry grid) open with no heading at all — the imagery carries the section. Flag a plan that reflexively caps every section with an intro; reserve intros for sections whose content needs framing (feeds, carousels, mixed content), and let self-explanatory card grids breathe without one.

### Component-context judgment

- **`umd-layout-image-expand` background context.** Wrap in a dark section (`background:#000` or `umd-layout-background-full-dark`) only when image-expand sits between other dark sections. On a predominantly light page, the built-in dark overlay is sufficient — adding a dark wrapper creates an isolated dark island. (For text-color rules inside the content slot, see `RULES.md §17`.)
- **Hero variant fit.** `data-display="standard"` is the default. `data-display="overlay"` is a specific design choice for a composited overlay panel — flag it if it's been chosen by default rather than for the overlay effect. (See `RULES.md §22`.)
- **Hero size: home vs landing.** A full-height standard hero belongs on the site home page only. On any other landing (department, program, sub-section), use `data-layout-height="small"` — a full-height hero on a non-home landing reads as a homepage and over-emphasizes the section. Flag full-height heroes on non-home landings.
- **Hero variant by page role, not just height.** `umd-element-hero-minimal` is built for interior pages and section headers; a home page that opens on it reads as a subpage. Home pages take the background hero (`umd-element-hero data-display="standard"`) — full height when the imagery earns it, `data-layout-height="small"` when there is only one usable image. Flag `hero-minimal` on any home page.
- **Hero text alignment continuity.** When the element directly below the hero is centered (a `umd-element-section-intro`, which is always centered), the hero should also be centered (`data-layout-text="center"`). Mismatched alignment between hero and the section directly under it reads as accidentally inconsistent. Flag a left-aligned hero followed immediately by a centered section-intro (or vice versa).
- **Hero stuffing — pull body copy into a section-intro.** Flag heroes that try to carry: a multi-line subhead in `slot="text"`, hierarchical text (separate title + body + tagline), or more than 2 CTAs in `slot="actions"`. Move the body copy and CTA row into a `umd-element-section-intro` directly below the hero. Hero keeps the page title (and at most one primary CTA). See `RULES.md §22` and `LAYOUT-PATTERNS.md` "Hero + section-intro split".
- **Overlay-card height — `size-large`.** When `umd-element-card-overlay type="image"` cards are the primary visual of a section (e.g. a 2-up principles grid), add `class="size-large"` so the image gets vertical room (min-height 320 → 560px, shipped upstream — no per-page CSS). Flag primary overlay-card grids left at default height where the image crops too tight; skip it for compact card rows, and never combine it with masonry. See `LAYOUT-PATTERNS.md` "Overlay-Card Grids".
- **Grid gap vs. no-gap.** No-gap grids (`umd-layout-grid-columns-*`) read as one continuous photo mosaic; gapped grids (`umd-layout-grid-gap-*`, 32px) read as discrete tiles. Choose no-gap for edge-to-edge image-overlay walls, gapped for separated or standard cards. Never hand-roll a no-gap grid class — the upstream `umd-layout-grid-columns-*` already exist. See `LAYOUT-PATTERNS.md` "Overlay-Card Grids".
- **Card content stays in its card — unless the list earns its own section.** When a card carries a short link list (3–5 items) plus its intro sentence, lift the list out into rich-text columns and the row splits into two unrelated patterns for no gain. Keep it in the card. The judgment flips when the list is genuinely long, or when the content designs better as its own thing — a 12-item resource index, a set that wants grouping headers or two columns of its own. Then rich text or an accordion is the better home and the card was the wrong container. The mistake to catch is **assuming** either direction: decomposing a short list because rich text feels tidier, or cramming a long one into a card because it started there.
- **Do not restate what embedded media already displays.** A YouTube embed renders its own title bar; a poster frame usually carries a title too. A heading directly above one repeats the same words a few pixels apart. Let the media speak, or replace the heading with framing the media does not provide.
- **Legibility inside a themed component, not just across the page.** Dark-theme guidance above is about how much dark a page carries. This is narrower: check that a themed variant is actually readable. `umd-element-stat data-display="block" data-theme="dark"` renders its label text unreadably; imageless overlay cards on a light band are fine because the card supplies its own dark face. When a component offers a themed card variant, look at the label and body colours it produces before choosing it — the number or headline usually survives the theme while the supporting text does not.
- **Feeds for time-sensitive, hand-authored for evergreen.** Use feed components (`umd-feed-news`, `umd-feed-events-list`) only for content that genuinely updates (news, events) — and hand-authored components (cards, carousels, pathways) for evergreen content, even when a feed *could* render it. A feed of static content goes stale-looking; hand-authored "latest news" goes stale in fact. Flag the mismatch in either direction. (Feeds also require a server context — CORS blocks them on localhost.)
- **Extend rather than force-fit.** When content genuinely has no DS component (a Venn diagram, a filterable timeline, chart infographics), flag any plan that bends a DS component far outside its intent. The right move is a purpose-built light-DOM component — documented in `OVERRIDES.md` — after first checking `OVERRIDES.md` for an existing page-built class that already solves it. A contorted DS component reads worse than an honest custom one.

### Dark theme — when to use it (positive triggers)

Beyond avoiding overuse (above), use a dark section deliberately when:

- **Connecting a dark hero to the section right under it.** Especially on the home page, a dark hero followed by a dark section feels like one continuous brand band — intentional and correct.
- **Calling attention to a single section.** One dark band on an otherwise light page acts as a visual exclamation point for the section's content.
- **Highlighting video content.** Video posters and players read better against dark surrounds.
- **Breaking up a long page.** When a landing has many light sections in a row, a single dark band mid-page resets the rhythm.

Avoid dark theme as a *default* for weighty sections (stats, large card grids) on non-home landings — it stacks visual weight without serving any of the triggers above. The user feedback that drove this rule: "This isn't a home page so we don't need that weighted top section."

**Dark inside components — the band-free alternative.** A page can carry full brand weight with **zero dark bands**: a dark hero, dark-themed card faces (`umd-element-card-overlay data-theme="dark"`) on light sections, and the dark visual footer (umd.edu/academics does exactly this). When a plan wants dark presence but its content sections are all scannable, prefer dark *components on light backgrounds* over `umd-layout-background-full-dark` wrappers. Conversely, when full-bleed dark bands are used, keep them as **one contiguous block** (hero flowing through the first sections, as on umd.edu/art) rather than alternating dark/light stripes down the page.

---

## Step 4 — Component-specific risks

Any component-specific rule that fails silently or produces broken output is a hard rule and lives in `RULES.md`. When the plan includes one of these, link to the rule rather than restating it:

- `umd-element-stat` slot names — `RULES.md §11`
- `umd-element-event` `display` vs `data-display` — `RULES.md §26`
- `umd-element-quote data-display="featured"` actions slot wrapper — `RULES.md §28`
- `umd-element-card-overlay type="image"` requirement for image backgrounds — `RULES.md §16`
- `umd-layout-image-expand` text color and quote transparency — `RULES.md §17`
- Rich-text eyebrow/header color — the `umd-sans-*` classes set no color, so a header inherits the DS `#454545` gray and reads muddy, not black. Needs `text-black` (light) / `text-white` (dark) — `RULES.md §18`
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
