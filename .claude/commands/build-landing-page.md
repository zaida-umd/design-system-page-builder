# Build Landing Page (brief-driven)

Build a fresh UMD landing page from the user's brief. Use this when the user wants a new landing page about a specific topic, audience, or campaign — not a recreation of an existing URL (use `/recreate-page` for that), and not a fixed sample/test page (use `/sample-landing-page` for that).

## Brief intake

The user's `$ARGUMENTS` should describe: page topic/audience, key sections needed, any required CTAs or links, image direction (campus/people/research/events). If the brief is too thin to act on (e.g. "build a landing page" with no topic), ask one clarifying question covering all gaps at once before building.

## Setup

1. Read `TEMPLATE.html` — use its full `<head>` block (critical CSS + cdn.js script) verbatim. Do not rebuild it. The CSS comes from `styles/critical.css` (single source of truth for all CSS rules).
2. Read `registry/registry-index.json` for the category map and `lookup_by_tag`. Load only the specific category files you need for the content types in the brief.
3. Read `LAYOUT-PATTERNS.md` for HTML patterns when using rich text sections, dark backgrounds, two-column grids, or inline CTA rows.
4. Read `RULES.md` and follow every rule.
5. Read `OVERRIDES.md` — if the brief calls for a layout that an existing entry already solves (e.g. full-width outline CTA → `.umd-action-outline-block`), reuse the documented class instead of re-inventing it.

## Page identity

Slug the page from the brief (e.g. "Sustainability initiatives" → `sustainability-initiatives`). Output to `examples/{slug}.html` unless the user specifies a different path.

## Component selection

Use the cheat-sheet from `/recreate-page` for first-pass component matching. For each section in the brief:
- Match the content type to the registry entry that fits.
- If no DS component fits a content need, check `OVERRIDES.md` for a documented page-built class first. Only invent a new one if nothing in either source fits.
- Distinguish close alternatives (e.g. `umd-element-hero` vs `umd-element-hero-minimal`) and pick consciously, not by default.

## Spacing and layout

Same rules as `/recreate-page`:
- Every top-level `<section>` gets `class="umd-layout-vertical-landing"` — except dark sections immediately followed by another dark section (omit on the preceding ones).
- Pathway and hero are full-bleed — do NOT wrap in a horizontal spacing class.
- Card grids and section intros go inside a `umd-layout-space-horizontal-larger` wrapper.
- `umd-element-quote` uses `umd-layout-space-horizontal-normal` (1280px).
- `data-theme` does not cascade — set it on every child component that needs it.

## Required page chrome

Open with these three elements in this order:
1. **Global university header** — `<umd-element-navigation-utility data-alert-off="true" role="navigation" aria-label="Utility navigation"></umd-element-navigation-utility>`
2. **Site utility header** — `<umd-element-utility-header></umd-element-utility-header>`
3. **Site navigation header** — `<umd-element-navigation-header sticky class="umd-layout-space-horizontal-full">` with logo and nav items appropriate to the brief's site/department.

Close with the visual footer (see CLAUDE.md §Logos and `/recreate-page` for the snippet).

## Images

No source page to download from — pull from the local library:
1. Read `images/images-index.json`.
2. Size tier: **large** for heroes, pathways, image-expand; **small** for cards.
3. Match the brief's tone to a tag (`campus`, `people`, `events`, `research`); fall back to `default: true` entries.
4. Reference as repo-relative paths: `../images/{tier}/{tag}/filename.jpg`.

## Output

Write the completed HTML file to `/Users/zjocson/repos/design-system-page-builder/examples/{slug}.html`. Confirm the filename when done. If a preview server is running, verify the page renders before reporting success.

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
