# Claude Code — Design System Page Builder

## Check commands before starting any work

The `.claude/commands/` directory contains slash commands for this project. **Before writing any HTML page or doing any page-building task, check if a command exists for it.**

| Task | Command file |
|---|---|
| Build a sample/test landing page (fixed recipe) | `.claude/commands/sample-landing-page.md` |
| Build a sample/test interior page (fixed recipe) | `.claude/commands/sample-interior-page.md` |
| Build a fresh landing page from a brief | `.claude/commands/build-landing-page.md` |
| Build a fresh interior page from a brief | `.claude/commands/build-interior-page.md` |
| Evaluate a design | `.claude/commands/evaluate-design.md` |
| Recommend a component | `.claude/commands/recommend-component.md` |
| Recreate an existing page | `.claude/commands/recreate-page.md` |

**Do not build pages from scratch** when a command file covers the task. The command file defines the required sections, content source, file naming, image sources, spacing rules, and output path. Follow it exactly.

To choose between the four page-building commands:
- **`/recreate-page <url>`** — convert a real existing page (downloads source assets first, mirrors structure).
- **`/build-landing-page <brief>`** / **`/build-interior-page <brief>`** — fresh pages from a topic/audience brief; output to `examples/`.
- **`/sample-landing-page`** / **`/sample-interior-page`** — fixed-recipe showcase pages (no brief, no inputs); output to `test/`. Use only for fixture/test work.

The three brief- or URL-driven commands all run a final harvest step that updates `OVERRIDES.md` with any shadow injections or page-built classes the new page introduced. The two `sample-*` commands skip this step because they reuse the same fixed recipe each time.

## Source of truth hierarchy

Each file has a distinct role — don't duplicate rules across them. When a topic could fit two files, prefer the higher-priority one and reference it from the others.

1. **`.claude/commands/*.md`** — task instructions for each slash command. Check first.
2. **`RULES.md`** — hard mechanical rules: required structure, slot names, attribute requirements, spacing classes, component-specific gotchas (things that fail silently or render wrong if violated). Build commands enforce these.
3. **`registry/`** — component slots and attributes verified from NPM. Source of truth for what a component accepts.
4. **`styles/critical.css`** — **single source of truth for all CSS rules** (canonical file).
5. **`TEMPLATE.html`** — inlines `styles/critical.css` verbatim + HTML skeleton (copy `<head>` block verbatim).
6. **`LAYOUT-PATTERNS.md`** — HTML pattern recipes for utility classes and multi-component layouts (rich text, masonry, grids, sticky columns, link-card grids). Reference, not enforcement.
7. **`.claude/commands/evaluate-design.md`** — design-judgment checks for catching design mistakes (variety, rhythm, dark-theme overuse, watermark adjacency). Not a hard-rule enforcer; complements `RULES.md`.
8. **`OVERRIDES.md`** — page-specific deviations (shadow injections, page-built classes). Append-only log, not a rule source.
9. **`REQUIRED-CSS.md`** — commentary on *why* each CSS rule group is needed (no CSS to copy).

## Logos

Never use a broken or placeholder logo image. Use these local fallbacks whenever a real department logo is unavailable:

- **Header** (`slot="logo"` in `umd-element-navigation-header`): `../images/logos/primary-logo-dark.svg`
- **Footer** (`slot="logo"` in `umd-element-footer`): `../images/logos/footer-logo.svg`

**Always add an `onerror` runtime fallback** when using an external logo URL — many UMD-domain URLs are hotlink-protected and 403 from local pages. The footer/header components do **not** detect a broken `src` and do **not** render the default UMD wordmark when the slot exists; they just render the broken `<img>`. Use:

```html
<!-- Header logo -->
<img src="https://example.umd.edu/dept-logo.png" alt="…"
  onerror="this.onerror=null;this.src='../images/logos/primary-logo-dark.svg';" />

<!-- Footer logo -->
<img src="https://example.umd.edu/dept-logo.png" alt="…"
  onerror="this.onerror=null;this.src='../images/logos/footer-logo.svg';" />
```

`this.onerror=null` prevents an infinite loop if the fallback also fails.

## Images

When a real image URL is unavailable (hotlink protection, dynamic content):
1. Read `images/images-index.json`
2. Size tier: **large** for heroes, pathways, image-expand — **small** for cards
3. Match context to tag (`campus`, `people`, `events`, `research`); fall back to `default: true` entries
4. Reference as repo-relative path: `../images/large/campus/filename.jpg`

## Keeping critical.css in sync with the design system

`styles/critical.css` is a **handcrafted CSS translation** of design system tokens and styles. It cannot be imported directly from the styles package (which is a TypeScript/JSS module, not raw CSS). Instead, audit it manually whenever the `design-system` submodule is updated.

### When to audit

Only needed when the submodule version changes (`git submodule update` or a bump in `.gitmodules`). If the submodule hasn't moved, `critical.css` cannot have drifted.

### How to audit

```bash
cd design-system/packages/styles
pnpm install && pnpm build:css
# Output: dist/css/layout.min.css — compare class-by-class against critical.css
```

### Layout categories to check

All four layout categories in `design-system/packages/styles/source/layout/` map to `critical.css`:

| Source path | CSS classes in critical.css |
|---|---|
| `layout/space/horizontal.ts` | `umd-layout-space-horizontal-*` |
| `layout/space/vertical.ts` | `umd-layout-vertical-landing`, `umd-layout-vertical-landing-child`, `umd-layout-vertical-interior*` |
| `layout/space/columns.ts` | `umd-layout-space-columns-left` |
| `layout/grid/gap.ts` | `umd-layout-grid-gap-two`, `umd-layout-grid-gap-stacked` |
| `layout/grid/base.ts` | `umd-layout-grid-columns-four` |
| `layout/grid/inline.ts` | `umd-layout-grid-inline-tablet-rows` |
| `layout/grid/masonary.ts` | `umd-layout-grid-masonry` |
| `layout/grid/child.ts` | `umd-layout-grid-child-fill-height` |
| `layout/background/full.ts` | `umd-layout-background-full-dark` |
| `layout/alignment/block.ts` | `umd-layout-alignment-block-stacked` |

Token values to cross-check: spacing (`sm`=16px, `md`=24px, `lg`=32px, `xl`=40px) and breakpoints (`large.min`=650px, `tablet.min`=768px, `desktop.min`=1024px, `highDef.min`=1200px).

## Registry is the source of truth for components

Do not re-derive slots or attributes from NPM source or Storybook. Use `registry/` JSON files. See `RULES.md §8`.
