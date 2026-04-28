# Build Interior Page (brief-driven)

Build a fresh UMD interior/subpage from the user's brief. Use this when the user wants a new interior page — breadcrumb + sidebar + long-form content — about a specific topic. NOT for sample/test pages (use `/sample-interior-page`) or recreating an existing URL (use `/recreate-page`).

## Brief intake

The user's `$ARGUMENTS` should describe: page title, breadcrumb trail, eyebrow label, sidebar nav items (or whether to omit the sidebar), and the body content sections (rich text, accordions, person bios, callouts, etc.). If the brief is too thin (e.g. "build an interior page about X" with no trail or sidebar guidance), ask one consolidated clarifying question before building.

## Setup

1. Read `TEMPLATE.html` — use its full `<head>` block (critical CSS + cdn.js script) verbatim.
2. Read `registry/registry-index.json` for the category map; load only the category files you need.
3. Read `RULES.md` — pay special attention to §21 for interior-page layout rules.
4. Read `LAYOUT-PATTERNS.md` for column/sidebar patterns.
5. Read `OVERRIDES.md` — reuse documented page-built classes (e.g. `.umd-text-line-trailing`) before inventing new ones.

## Page identity

Slug from the brief title (e.g. "Honors program admissions" → `honors-program-admissions`). Output to `examples/{slug}.html` unless the user specifies otherwise.

## Required structure

Open with the same three nav elements as `/build-landing-page` (utility nav, utility header, navigation header).

For interior pages specifically (RULES.md §21):
- **Hero** must use `umd-element-hero data-layout-height="small"` — never the default landing-size hero.
- **Breadcrumb** comes after the hero, inside the outer page wrapper, before the column layout.
- **Sidebar + content** uses the documented `umd-layout-space-columns-left` pattern with `max-w-[800px]` content column. Omit the sidebar only if the brief explicitly says single-column.
- **Footer** — visual footer (same snippet as `/build-landing-page`).

## Component selection

Match content sections to registry components. Common interior patterns:
- Long-form prose → `umd-element-rich-text` (or rich-text utility classes from critical.css)
- Expandable Q&A → `umd-element-accordion-item` in a stack
- Person profile → `umd-element-person-bio`
- Side-quote pull / callout → `umd-element-quote`
- Cross-link sections → `umd-element-card` grid inside a horizontal lock

## Images

Same library lookup as `/build-landing-page` — read `images/images-index.json`, pick by tier and tag, reference repo-relative paths.

## Output

Write to `/Users/zjocson/repos/design-system-page-builder/examples/{slug}.html`. Confirm the filename. If a preview server is running, verify the page renders before reporting success.

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
