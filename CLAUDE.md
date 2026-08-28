# Claude Code — Design System Page Builder

## Check commands before starting any work

The `.claude/commands/` directory contains slash commands for this project. **Before writing any HTML page or doing any page-building task, check if a command exists for it.**

| Task | Command file |
|---|---|
| Stand up a **whole site / new project repo** (front door) | `.claude/commands/new-project.md` |
| Plan a page from a brief **or raw content** (front door) | `.claude/commands/plan-page.md` |
| Build a sample/test landing page (fixed recipe) | `.claude/commands/sample-landing-page.md` |
| Build a sample/test interior page (fixed recipe) | `.claude/commands/sample-interior-page.md` |
| Build a fresh landing page from a brief | `.claude/commands/build-landing-page.md` |
| Build a fresh interior page from a brief | `.claude/commands/build-interior-page.md` |
| Evaluate a design | `.claude/commands/evaluate-design.md` |
| Recommend a component | `.claude/commands/recommend-component.md` |
| Recreate an existing page | `.claude/commands/recreate-page.md` |
| QA a component after a DS update | `.claude/commands/qa-component.md` |

**Do not build pages from scratch** when a command file covers the task. The command file defines the required sections, content source, file naming, image sources, spacing rules, and output path. Follow it exactly.

To choose between the commands:
- **`/new-project <name, url, or brief>`** — the **site-level front door**. Use when the work is a whole site or multi-page section, in any of its three flavors: closely recreating an existing site, overhauling one, or building something new. Scaffolds a project repo from `templates/project-scaffold/`, derives the IA, builds the shared header and footer **once**, then hands each page to `/recreate-page` or `/plan-page`. The per-page commands all assume chrome and IA already exist — this is what creates them. Also documents how to retrofit a pre-scaffold project repo.
- **`/plan-page <brief or raw content>`** — the **front door** when you have content (or a topic) but not a finished plan. Detects brief vs raw content, surveys the site (existing) or peers (new) for visual tone, derives an ordered **Page Plan** (sections → components, copy source, image source), self-validates against `/evaluate-design`, then hands off to `/build-landing-page` or `/build-interior-page`. Use this rather than calling a build command directly whenever the structure isn't already decided.
- **`/build-landing-page`** / **`/build-interior-page`** — render a page. Preferred path is via `/plan-page` (Page Plan mode); they also accept a raw `<brief>` directly (Brief mode) for simple pages. Output to the `page-builder-examples` repo.
- **`/recreate-page <url>`** — convert a real existing page (downloads source assets first, mirrors structure). Targets either the `page-builder-examples` repo (default) or a project repo; in a project with `shared/` chrome it writes `<main>` only and lets `tools/build-chrome.py` splice the rest.
- **`/sample-landing-page`** / **`/sample-interior-page`** — fixed-recipe showcase pages (no brief, no inputs); output to `test/`. Use only for fixture/test work.
- **`/qa-component <component-or-ticket>`** — focused component QA page for verifying a DS submodule update; output to `qa/`.

`/plan-page` plans but does not render or harvest — it delegates both to the build command. The build and URL-driven commands (`/build-landing-page`, `/build-interior-page`, `/recreate-page`) run a final harvest step that updates `OVERRIDES.md` with any shadow injections or page-built classes the new page introduced. The `sample-*` and `qa-component` commands skip this step.

## Output folder guide

| Folder | What lives here | Written by |
|---|---|---|
| A project repo (`<name>-design`) | Real design work — a whole site or section, in its own repo vendoring this one | `/new-project`, then `/recreate-page` or `/plan-page` targeting that repo |
| `page-builder-examples` repo | Realistic one-off pages from briefs or real URLs — for demos and client review | `/build-landing-page`, `/build-interior-page`, `/recreate-page` |
| `test/` | Fixed-recipe fixture pages — for validating the page builder itself | `/sample-landing-page`, `/sample-interior-page` |
| `qa/` | Isolated component test pages — for visually verifying DS submodule updates | `/qa-component` |

Never write QA pages to `test/` or the `page-builder-examples` repo, and never write demo/fixture pages to `qa/`.

`test/` and `qa/` are fixtures for validating the builder itself. Real design work never lands here — it goes to a project repo (below) or to `page-builder-examples`.

## Using this repo in a design project

Real design projects live in their own repo and vendor this one as a submodule at `page-builder/`: `admissions-design`, `belonging-design`, `strategic-plan-design`, and `page-builder-examples` all do. Those repos own their pages, images, briefs, and overrides; this repo owns the rules, registry, CSS, commands, and shared tooling.

**Starting a new project:** copy `templates/project-scaffold/` — it carries the `pages/ + shared/ + images/ + briefs/` skeleton, a project `CLAUDE.md`/`README.md`/`OVERRIDES.md`, and starter chrome partials. `templates/project-scaffold/SCAFFOLD.md` has the bootstrap steps. Do not hand-roll a project layout; three projects did and diverged three ways.

All three kinds of project — closely recreating an existing site, overhauling one, and building something new — use that same scaffold. They differ only in where content and structure come from, which is `/plan-page`'s and `/recreate-page`'s business, not the repo layout's.

**Shared chrome.** A project keeps its header and footer once, in `shared/`, and inlines them into every page with `tools/build-chrome.py`. Never copy chrome between pages, and never hand-edit chrome inside a page — it sits between `SHARED:<key>:START`/`:END` markers and the next build overwrites it.

| Tool | What it does |
|---|---|
| `tools/build-chrome.py` | Splices a project's `shared/` chrome into every page under `pages/`. `--check` exits non-zero if any page is stale. |
| `tools/chrome.py` | The library behind it — region contract, `{{ROOT}}` depth expansion, contextual-drawer stamping. Import it from a project's own page generators so both paths emit identical bytes. |
| `tools/check-themes.py` | Registry-driven `data-theme` validator. |

**Paths in shared files use `{{ROOT}}`, never `../`.** Project pages sit at more than one depth, so a fixed prefix is wrong on half of them. This applies to end-of-body scripts too: `TEMPLATE.html` ships `src="../scripts/grid-animations.js"`, which is correct only for a page in this repo's `test/` — a project references it as `{{ROOT}}page-builder/scripts/...` from `shared/page-scripts.html`.

**Never commit project-specific work into this repo.** Project images, chrome, and overrides belong in the project. This submodule is shared by every project.

## Source of truth hierarchy

Each file has a distinct role — don't duplicate rules across them. When a topic could fit two files, prefer the higher-priority one and reference it from the others.

1. **`.claude/commands/*.md`** — task instructions for each slash command. Check first.
2. **`RULES.md`** — hard mechanical rules: required structure, slot names, attribute requirements, spacing classes, component-specific gotchas (things that fail silently or render wrong if violated). Build commands enforce these.
3. **`registry/`** — component slots and attributes verified from NPM. Source of truth for what a component accepts.
4. **`styles/critical.css`** — **single source of truth for all CSS rules** (canonical file). When inlining into a page, copy verbatim — never trim "unused" rules. Animation/keyframe rules and feature-specific utilities pair with each other; dropping one silently breaks the related feature when used later (e.g. trimming `@keyframes slide-in-from-left` + `@supports (animation-timeline: scroll())` breaks every `.umd-watermark` animation).
5. **`TEMPLATE.html`** — inlines `styles/critical.css` verbatim + HTML skeleton (copy `<head>` block verbatim). End-of-body scripts live in `scripts/` (`grid-animations.js`, `filter-band.js`) and are referenced by `src` — **never paste them inline into pages**; from a project repo the path is `../page-builder/scripts/<name>.js`.
6. **`LAYOUT-PATTERNS.md`** — HTML pattern recipes for utility classes and multi-component layouts (rich text, masonry, grids, sticky columns, link-card grids). Reference, not enforcement.
7. **`.claude/commands/evaluate-design.md`** — design-judgment checks for catching design mistakes (variety, rhythm, dark-theme overuse, watermark adjacency). Not a hard-rule enforcer; complements `RULES.md`.
8. **`OVERRIDES.md`** — page-specific deviations (shadow injections, page-built classes). Append-only log, not a rule source.
9. **`REQUIRED-CSS.md`** — commentary on *why* each CSS rule group is needed (no CSS to copy).
10. **`QA-REFERENCE.md`** — how to check the design system's own QA site (`qa-designteam.umd-servd.com`) for how a component is *supposed* to render. Consult it **before** recording any DS behaviour as broken; it outranks the notes in this repo, which are a translation and can go stale.

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

### A reversed (white) logo is not a broken logo — `onerror` will not save you

Many UMD sites put their department logo on a **dark** header, so the only file
they publish is the reversed/white variant. `umd-element-navigation-header` has
**no dark theme** — it is white — so that file renders invisible.

It returns HTTP 200, so `onerror` never fires. Nothing errors, nothing is
missing from the network log, and the header just looks like it has no logo.
Check the fills before trusting a downloaded logo:

```bash
grep -o 'fill="[^"]*"' logo.svg | sort | uniq -c   # mostly #FFF/#FEFEFE = reversed
```

Recolouring is usually not safe either: on a UMD lockup the white fills are
shared between the wordmark and the flag globe's quadrants, so a blanket swap
corrupts the globe. When no dark variant is published, fall back to
`primary-logo-dark.svg` above and keep the reversed original alongside for
reference.

If the source site has no logo *image* at all — some sites set their brand as
styled text — the `slot="logo"` anchor accepts text, and that is a better
recreation than inventing a logo.

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

### The stylesheet pin follows the submodule

Pages load the `web-styles-library` CSS bundles from unpkg at a **pinned version**, and that pin must match the `packages/styles` version inside the current submodule pin. The two move together — a submodule bump is not finished until the stylesheet links are repointed.

Do not leave the links unversioned. An unpinned `unpkg.com/@universityofmaryland/web-styles-library/css/...` URL floats to whatever npm publishes as `latest`, so page CSS changes with no commit, `critical.css` gets audited against a version no page is guaranteed to load, and visual regressions appear with nothing in the history to explain them.

**On every submodule bump:**

```bash
# 1. Read the styles version the new submodule pin ships
grep -m1 '"version"' design-system/packages/styles/package.json

# 2. Repoint every stylesheet link to it (TEMPLATE.html + test/ + qa/)
OLD=1.8.16; NEW=<version from step 1>
# Match the URL path form (@VER/css/), never the bare token — prose comments
# cite versions historically and must not be rewritten. See the note below.
grep -rl "web-styles-library@$OLD/css/" TEMPLATE.html test qa \
  | xargs sed -i '' "s|web-styles-library@$OLD/css/|web-styles-library@$NEW/css/|g"

# 3. Confirm none were missed — this must print nothing
grep -rn "web-styles-library/css/" TEMPLATE.html test qa
```

Then run the `critical.css` audit below against that same version, and update the version stamp in the `styles/critical.css` header.

### The components pin follows the submodule too

The `cdn.js` script tag's `web-components-library@…` version must match the `packages/components` version in the current submodule pin, and `components_version` in every `registry/*.json` must match both. All three move together with the stylesheet pin.

```bash
# Version the new submodule pin ships
grep -m1 '"version"' design-system/packages/components/package.json

OLD=1.19.5; NEW=<version from above>
# Again, match the URL path form (@VER/dist/), not the bare token.
grep -rl "web-components-library@$OLD/dist/" TEMPLATE.html test qa \
  | xargs sed -i '' "s|web-components-library@$OLD/dist/|web-components-library@$NEW/dist/|g"
sed -i '' "s|\"components_version\": \"$OLD\"|\"components_version\": \"$NEW\"|" registry/registry-*.json
```

Then diff the component API surface across the two versions and apply any real changes to `registry/` before updating `last_verified`:

```bash
git -C design-system diff --stat <old-tag> <new-tag> -- packages/components/source/
```

**Writing version numbers in comments.** `critical.css` is inlined verbatim into every page, so any version it names shows up when you grep a built page. Phrase historical references so they cannot be mistaken for a pin — `RETIRED (upstream since web-styles-library@1.8.14)`, not `RETIRED (web-styles-library@1.8.14)` — and keep the bump `sed` scoped to the URL path form above so a tombstone is never rewritten into a false claim.

That diff is the verification — it shows exactly which components' slots or attributes moved, so the rest of the registry stays valid without re-deriving it. **Carousels are the high-risk area**: they were substantially refactored across the 1.18 → 1.19 line, so QA any page using `umd-element-carousel-*` after a bump.

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
