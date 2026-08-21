# Build Landing Page

Build a fresh UMD landing page — full-width hero and a rhythm of full-bleed / narrow / wide sections. NOT for fixed sample/test pages (use `/sample-landing-page`) or recreating an existing URL (use `/recreate-page`).

There are two ways in:

- **Page Plan mode (preferred)** — invoked by `/plan-page` with a Page Plan. Structure, components, copy source, image source, and chrome are already decided and validated. Consume the plan; do **not** re-derive any of it.
- **Brief mode** — invoked directly with a brief. Derive the structure here. For anything beyond a simple page, prefer routing the user through `/plan-page` first so intake, tone survey, and design validation happen once, in one place.

---

## Intake

### Page Plan mode

If a Page Plan was supplied, it is authoritative:
- Use its section order and component choices as-is. **Skip** brief-intake, the reference-page step, and first-pass component selection below.
- The plan already passed the `/evaluate-design` Step 3 checks (plan-page self-validates) — do not re-run them.
- Honor `copy-source` and per-section `image-source` (see [Copy and images](#copy-and-images)).
- Use the plan's surveyed **chrome** (header logo + nav, footer) so the page matches its site.

### Brief mode

`$ARGUMENTS` should describe: page topic/audience, key sections needed, any required CTAs or links, image direction (campus/people/research/events). If the brief is too thin to act on (e.g. "build a landing page" with no topic), ask **one** clarifying question covering all gaps at once before building. Copy is generated in brief mode unless the user supplied real copy to preserve.

---

## Copy and images

Honor these in both modes:

- **Copy source**
  - `verbatim` — use the user's **exact words**. You may only structure copy into sections/slots, trim to a component's slot limits, and add the labels/eyebrows/headings a component structurally requires. Never paraphrase or invent body copy.
  - `generate` — write realistic copy in the site's voice, using the plan's tone brief (or the brief).
- **Image source** (per section)
  - `provided <url>` — reference the URL directly with the CLAUDE.md `onerror` fallback. **Do not download it into this repo** — it holds only the fallback library; a required local copy belongs in the output project's own assets (e.g. `page-builder-examples/images/projects/{project}/`, referenced as `../images/projects/...`).
  - `library <tier>/<tag>` — pull from the fallback library (steps below). **large** for heroes, pathways, image-expand; **small** for cards.
  - `none` — imageless. Prefer an imageless component variant (e.g. color overlay cards, `data-theme="dark"`, no `type="image"`) over a forced stock photo.

**Prefer `none` over stock.** Reach for `library` only where the page genuinely needs a visual anchor or the brief/plan asks to be more visual — this is a landing page, so heroes and featured bands legitimately earn imagery, but don't stock-fill every section.

**Library lookup** (for `library` sections, and any brief-mode section with no provided image):
1. Read `images/images-index.json`.
2. Size tier: **large** for heroes/pathways/image-expand; **small** for cards.
3. Match the section's tone to a tag (`campus`, `people`, `events`, `research`); fall back to `default: true` entries.
4. Reference the fallback library at `../page-builder/images/{tier}/{tag}/filename.jpg` (in a standalone project repo that vendors its own copy, `../images/{tier}/{tag}/filename.jpg`). See [Output](#output) for why `../` resolves.

---

## Optional reference page(s) step (brief mode only; skip if no reference URL)

Only when the user supplies an explicit reference URL to **mirror** (not just a site to match — that survey already happened in `/plan-page`). Before any analysis or building, spawn a subagent to download the source page assets into `/Users/zjocson/repos/page-builder-examples/tmp/`. The subagent should:

1. Create the directory `/Users/zjocson/repos/page-builder-examples/tmp/` if it does not exist.
2. Download the full HTML of the source URL and save it as `tmp/source.html`.
3. Parse `tmp/source.html` and download all referenced assets:
   - Images (`<img src>`, `srcset`, CSS `background-image` URLs, `<picture><source srcset>`)
   - Videos (`<video src>`, `<source src>`)
   - Linked CSS files (`<link rel="stylesheet" href>`)
   - Inline and linked JavaScript files (`<script src>`)
4. Save each asset into a mirrored subdirectory under `tmp/` (e.g. `tmp/assets/images/`, `tmp/assets/css/`, `tmp/assets/js/`, `tmp/assets/video/`).
5. Use `curl` or `wget` for downloads. Skip assets that return non-200 status — log skipped URLs to `tmp/skipped-assets.txt`.
6. Return a summary of what was downloaded.

Wait for the subagent to complete before proceeding.

---

## Setup

1. Read `TEMPLATE.html` — use its full `<head>` block (critical CSS + cdn.js script) verbatim. Do not rebuild it. The CSS comes from `styles/critical.css` (single source of truth for all CSS rules).
2. Read `registry/registry-index.json` for the category map and `lookup_by_tag`. Load only the specific category files you need for the content types in the plan/brief.
3. Read `LAYOUT-PATTERNS.md` for HTML patterns when using rich text sections, dark backgrounds, two-column grids, or inline CTA rows.
4. Read `RULES.md` and follow every rule.
5. Read `OVERRIDES.md` — if the plan/brief calls for a layout that an existing entry already solves (e.g. full-width outline CTA → `.umd-action-outline-block`), reuse the documented class instead of re-inventing it.

---

## Page identity

Slug from the plan/brief (e.g. "Sustainability initiatives" → `sustainability-initiatives`). See [Output](#output) for the destination.

---

## Component selection

**Page Plan mode:** components are already chosen — skip this section.

**Brief mode:** use the `/recommend-component` cheat-sheet for first-pass matching (the single source for content-type → component). For each section in the brief:
- Match the content type to the registry entry that fits.
- If no DS component fits a content need, check `OVERRIDES.md` for a documented page-built class first. Only invent a new one if nothing in either source fits.
- Distinguish close alternatives (e.g. `umd-element-hero` vs `umd-element-hero-minimal`) and pick consciously, not by default.

### Hero defaults for landing pages

Unless the page is the **site home page**, use a small + centered standard hero:

```html
<umd-element-hero data-display="standard" data-layout-height="small" data-layout-text="center">
  <h1 slot="headline">Page Title</h1>
  <img slot="image" src="…" alt="…" />
</umd-element-hero>
```

A full-height hero (omit `data-layout-height`) is reserved for the site home. If the content includes a long subhead, hierarchical text, or more than 2 CTAs, pull that into a separate `umd-element-section-intro` directly below the hero — see `RULES.md §22` and `LAYOUT-PATTERNS.md` "Hero + section-intro split".

---

## Spacing and layout

- Every top-level `<section>` gets `class="umd-layout-vertical-landing"` — except dark sections immediately followed by another dark section (see `RULES.md §19`).
- Pathway and hero are full-bleed — do NOT wrap in a horizontal spacing class.
- Card grids and section intros go inside a `umd-layout-space-horizontal-larger` wrapper.
- `umd-element-quote` uses `umd-layout-space-horizontal-normal` (1280px).
- All other layout/component rules: see `RULES.md` (theming, slot patterns, spacing, component-specific gotchas).

---

## Required page chrome

Open with these three elements in this order:
1. **Global university header** — `<umd-element-navigation-utility data-alert-off="true" role="navigation" aria-label="Utility navigation"></umd-element-navigation-utility>`
2. **Site utility header** — `<umd-element-utility-header></umd-element-utility-header>`
3. **Site navigation header** — `<umd-element-navigation-header sticky class="umd-layout-space-horizontal-full">` with logo and nav items appropriate to the site/department (use the plan's surveyed chrome when available).

Close with the visual footer (see CLAUDE.md §Logos and `/recreate-page` for the snippet).

---

## Design check

- **Page Plan mode:** already validated by plan-page — skip.
- **Brief mode:** run the `/evaluate-design` Step 3 checks against the plan before writing HTML (card-layout variety, dark-theme overuse, section rhythm, consecutive watermark intros, hero fit).

---

## Output

**Default (demo/example):** create a new folder in the `page-builder-examples` repo and write `index.html` inside it:

```
/Users/zjocson/repos/page-builder-examples/{slug}/index.html
```

The page sits one level below the repo root, so relative paths resolve: end-of-body scripts as `../page-builder/scripts/...`, the fallback image library as `../page-builder/images/...`, and project images as `../images/projects/...`.

**Exception — standalone project repo:** when the work is its own cloned project (e.g. `admissions-design`, `strategic-plan-design`, where `design-system-page-builder` is a submodule and the repo keeps its pages in a `pages/` dir), write into that repo's convention (`pages/{slug}.html`) instead. Same one-level depth; that repo vendors its own `images/` so the library reference is `../images/...`.

Confirm the output path when done. If a preview server is running, verify the page renders before reporting success.

---

## Cleanup

If the reference-page step ran, delete the `tmp/` directory after the output file is confirmed written:
```bash
rm -rf /Users/zjocson/repos/page-builder-examples/tmp
```

---

## Attribute check (after writing)

Run the registry-driven `data-theme` validator on the new page:

```bash
python3 /Users/zjocson/repos/design-system-page-builder/tools/check-themes.py <output-file>
```

- **ERROR** — the value is not in the design system's theme vocabulary, i.e. a typo. Fix before reporting success. These are the ones worth tooling for: a component that ignores an unrecognized `data-theme` renders a misspelled value *identically* to a correct one (pathway `whte` vs `white`), so the mistake is invisible on the page and in a screenshot.
- **WARNING** — a real theme word the registry does not list for that component. Usually inert; confirm it is deliberate. If it turns out to be genuinely supported, update `registry/` rather than silencing the warning.

Exit code is non-zero only for errors, so warnings will not block a build.

---

## Harvest overrides (final step)

After the page is written and verified, spawn an `Explore` subagent to scan the new HTML file and update `OVERRIDES.md`. Brief it like this:

> Scan `<output-path>` for two things:
> 1. **Shadow injections** — IIFEs that call `el.shadowRoot.appendChild(<style>)`. Capture the target component tag, the CSS string injected, and the leading comment that explains why.
> 2. **Page-built components** — light-DOM CSS classes defined in the inline `<style>` block whose names are NOT present in `styles/critical.css`. For each, capture the class name, its DS counterpart (if any), and why a page-built version was needed (read the leading comment).
>
> Then read `OVERRIDES.md`. For each item found:
> - If an entry already exists, append `<output-path>` to the "Pages using this" list (only if not already listed).
> - If no entry exists, append a new entry under the correct heading (Shadow overrides / Page-built components) using the existing entry format.
>
> Do NOT add entries for classes already in `styles/critical.css` — those are sanctioned, not overrides. Do NOT modify the preamble.
>
> Report a one-line summary: `OVERRIDES.md: +N new entries, +M pages added to existing entries`.
