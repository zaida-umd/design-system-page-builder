# Claude Code — Design System Page Builder

## Check commands before starting any work

The `.claude/commands/` directory contains slash commands for this project. **Before writing any HTML page or doing any page-building task, check if a command exists for it.**

| Task | Command file |
|---|---|
| Build a test landing page | `.claude/commands/build-landing-page.md` |
| Build a test interior page | `.claude/commands/build-interior-page.md` |
| Evaluate a design | `.claude/commands/evaluate-design.md` |
| Recommend a component | `.claude/commands/recommend-component.md` |
| Recreate an existing page | `.claude/commands/recreate-page.md` |

**Do not build pages from scratch** when a command file covers the task. The command file defines the required sections, content source, file naming, image sources, spacing rules, and output path. Follow it exactly.

## Source of truth hierarchy

1. `.claude/commands/*.md` — task instructions (check first)
2. `RULES.md` — layout, spacing, and component usage rules
3. `registry/` — component slots and attributes (verified from NPM)
4. `styles/critical.css` — **single source of truth for all CSS rules** (canonical file)
5. `TEMPLATE.html` — inlines `styles/critical.css` verbatim + HTML skeleton (copy `<head>` block verbatim)
6. `LAYOUT-PATTERNS.md` — CSS-only utility class HTML patterns and examples
7. `REQUIRED-CSS.md` — explains *why* each CSS rule group is needed (commentary, no CSS to copy)

## Logos

Never use a broken or placeholder logo image. Use these local fallbacks whenever a real department logo is unavailable:

- **Header** (`slot="logo"` in `umd-element-navigation-header`): `../images/logos/primary-logo-dark.svg`
- **Footer** (`slot="logo"` in `umd-element-footer`): `../images/logos/footer-logo.svg`

## Images

When a real image URL is unavailable (hotlink protection, dynamic content):
1. Read `images/images-index.json`
2. Size tier: **large** for heroes, pathways, image-expand — **small** for cards
3. Match context to tag (`campus`, `people`, `events`, `research`); fall back to `default: true` entries
4. Reference as repo-relative path: `../images/large/campus/filename.jpg`

## Registry is the source of truth for components

Do not re-derive slots or attributes from NPM source or Storybook. Use `registry/` JSON files. See `RULES.md §8`.
