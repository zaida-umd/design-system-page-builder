# Build Interior Page

Build a fresh UMD interior/subpage — hero + breadcrumb + (optional) left sidebar + long-form content column. NOT for fixed sample/test pages (use `/sample-interior-page`) or recreating an existing URL (use `/recreate-page`).

There are two ways in:

- **Page Plan mode (preferred)** — invoked by `/plan-page` with a Page Plan. Structure, components, copy source, image source, and chrome are already decided and validated. Consume the plan; do **not** re-derive any of it.
- **Brief mode** — invoked directly with a brief. Derive the structure here. For anything beyond a simple page, prefer routing the user through `/plan-page` first so intake, tone survey, and design validation happen once, in one place.

---

## Intake

### Page Plan mode

If a Page Plan was supplied, it is authoritative:
- Use its section order and component choices as-is. **Skip** brief-intake and first-pass component selection below.
- The plan already passed the `/evaluate-design` Step 3 checks (plan-page self-validates) — do not re-run them.
- Honor `copy-source` and per-section `image-source` (see [Copy and images](#copy-and-images)).
- Use the plan's surveyed **chrome** (header logo + nav, footer, breadcrumb root) so the page matches its site.

### Brief mode

`$ARGUMENTS` should describe: page title, breadcrumb trail, eyebrow label, sidebar nav items (or whether to omit the sidebar), and the body content sections (rich text, accordions, person bios, callouts, etc.). If the brief is too thin (e.g. "build an interior page about X" with no trail or sidebar guidance), ask **one** consolidated clarifying question before building. Copy is generated in brief mode unless the user supplied real copy to preserve.

---

## Copy and images

Honor these in both modes:

- **Copy source**
  - `verbatim` — use the user's **exact words**. You may only structure copy into sections/slots, trim to a component's slot limits, and add the labels/eyebrows/headings a component structurally requires. Never paraphrase or invent body copy.
  - `generate` — write realistic copy in the site's voice, using the plan's tone brief (or the brief).
- **Image source** (per section)
  - `provided <url>` — reference the URL directly with the CLAUDE.md `onerror` fallback. **Do not download it into this repo** — it holds only the fallback library; a required local copy belongs in the consuming project's assets.
  - `library <tier>/<tag>` — look up `images/images-index.json`, pick by tier + tag. **large** for background heroes; **small** for `umd-element-media-inline` and cards. Reference the fallback library at `../page-builder/images/{tier}/{tag}/filename.jpg` (in a standalone project repo that vendors its own copy, `../images/{tier}/{tag}/filename.jpg`).
  - `none` — imageless. Use a text-only `umd-text-rich-advanced` block (or the minimal hero for a heroless top) rather than forcing a stock image.

If invoked in brief mode with no plan, choose image sources with the same default plan-page uses: **prefer `none` over stock** — reach for `library` only where the page genuinely needs a visual anchor or the brief asks to be more visual.

---

## Setup

1. Read `TEMPLATE.html` — use its full `<head>` block (critical CSS + cdn.js) verbatim. All interior CSS is already in `styles/critical.css`; no extra CSS is needed.
2. Read `registry/registry-index.json`; load only the category files you need.
3. Read `RULES.md` — follow every rule, **§21 for interior-page layout**.
4. Read `LAYOUT-PATTERNS.md` for the column/sidebar patterns.
5. Read `OVERRIDES.md` — reuse documented page-built classes (e.g. `.umd-text-line-trailing`) before inventing new ones.

---

## Page identity

Slug from the plan/brief title (e.g. "Honors program admissions" → `honors-program-admissions`). See [Output](#output) for the destination.

---

## Required structure (RULES.md §21)

Follow the §21 skeleton exactly — the breadcrumb and the columns layout each get their **own** `umd-layout-space-horizontal-larger` wrapper (not a shared outer div). Interior-specific points:

- **Chrome** — open with the same three full-width elements as `/build-landing-page`: `umd-element-navigation-utility` (with `data-alert-off="true"`), `umd-element-utility-header`, then `umd-element-navigation-header` (`sticky`, `class="umd-layout-space-horizontal-full"`) with the site's logo and nav items.
- **Hero — interior options only.** Use `umd-element-hero-minimal` (no image needed) **or** `umd-element-hero data-layout-height="small"`. Never a landing-size or full-height hero, and don't add `data-display="overlay"` unless explicitly requested (§22). Eyebrow text must be **≤ 16 characters**. Pick by image source: a background hero when `image-source` is `provided`/`library` large; the **minimal hero** when it's `none`.
- **Breadcrumb** — always `umd-element-breadcrumb` (never a hand-coded `<nav>`/`<ol>`), after the hero, in its own `umd-layout-space-horizontal-larger umd-layout-space-vertical-interior` wrapper. Follow the §21 `slot="paths"` pattern (Home link → intermediate links → current page as `<p aria-label="Current Page">`). Use the plan's surveyed breadcrumb root when available.
- **Sidebar + content column** — `umd-layout-space-columns-left` (never a custom grid); sidebar in `#umd-shell-sidebar-container`, content in `#umd-shell-content` with `max-w-[800px]`. The left nav is `umd-element-nav-slider` (interior-only) with its two-level slot structure — `slot="primary-slide-links"` holds only the bold parent; child links live in `slot="children-slides"` under `data-active`, current page marked `data-selected`. **Omit the sidebar only if the plan/brief says single-column.**
- **Content sections** — `umd-element-media-inline` is the primary editorial component (`data-layout-alignment="right"` to flip the image side); text-only sections use a bare `umd-text-rich-advanced` block. Always wrap `slot="text"` content in `umd-text-rich-advanced`. Headings carry `class="umd-layout-space-vertical-interior-child text-black umd-sans-larger-bold"`. Use interior spacing only — `umd-layout-space-vertical-interior` between sections, `umd-layout-space-vertical-interior-child` between a heading and its content. **Never** `umd-layout-vertical-landing*` on an interior page.
- **Component subset** — interior pages use only the §21 subset (media-inline, rich text, standard/overlay cards, event/event-list, quote, accordion). Do not place landing-only components (pathways, stats, section-intros, sticky-columns, full-height heroes) on an interior page.
- **Footer** — visual footer (same snippet as `/build-landing-page`; see CLAUDE.md §Logos).

---

## Design check

- **Page Plan mode:** already validated by plan-page — skip.
- **Brief mode:** run the `/evaluate-design` Step 3 checks that apply to interior pages (component fit, hero-size/variant, imageless-variant vs forced stock) against your plan before writing HTML.

---

## Output

**Default (demo/example):** create a new folder in the `page-builder-examples` repo and write `index.html` inside it:

```
/Users/zjocson/repos/page-builder-examples/{slug}/index.html
```

The page sits one level below the repo root, so relative paths resolve: end-of-body scripts as `../page-builder/scripts/...`, the fallback image library as `../page-builder/images/...`, and project images as `../images/projects/...`.

**Exception — standalone project repo:** when the work is its own cloned project (e.g. `admissions-design`, `strategic-plan-design`, where `design-system-page-builder` is a submodule and the repo keeps its pages in a `pages/` dir), write into that repo's convention (`pages/{slug}.html`) instead. Same one-level depth; that repo vendors its own `images/` so the library reference is `../images/...`.

Confirm the output path when done. If a preview server is running, verify the page renders before reporting success.

## Rules checklist before saving

- [ ] No `umd-layout-vertical-landing*` on any interior section
- [ ] `umd-layout-space-columns-left` used (not a custom grid)
- [ ] Left nav uses `slot="primary-slide-links"` (bold parent only) + `slot="children-slides"`; current page `data-selected`
- [ ] Hero is minimal or `data-layout-height="small"`; eyebrow ≤ 16 characters
- [ ] `slot="text"` wrapped in `umd-text-rich-advanced`; headings carry `text-black umd-sans-larger-bold`
- [ ] No landing-only components on the page
- [ ] No broken logo images — `../images/logos/primary-logo-dark.svg` (header), `../images/logos/footer-logo.svg` (footer)
- [ ] `copy-source` honored (verbatim copy not paraphrased); `image-source` honored (no forced stock)
- [ ] `tools/check-themes.py` reports no ERRORs (misspelled `data-theme` values render identically to correct ones)

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
