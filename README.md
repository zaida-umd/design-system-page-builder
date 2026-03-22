# UMD Design System Page Builder

A Claude-assisted workflow for generating complete, valid HTML pages using the [UMD Design System](https://github.com/UMD-Digital/design-system) web components (`@universityofmaryland/web-components-library`).

## What this is

Feed page content or a site URL into a Claude project and get back a complete, standards-compliant UMD Design System HTML page. The system is built on a verified component registry, a set of composition rules, and a ready-to-copy page template — all maintained against a specific pinned version of the design system.

**Current DS version:** `@universityofmaryland/web-components-library@1.17.18`

## Repository structure

```
design-system-page-builder/
├── README.md                        ← you are here
├── umd-component-registry.json      ← canonical component reference (slots, attrs, variants)
├── RULES.md                         ← composition rules, gotchas, and required CSS patterns
├── TEMPLATE.html                    ← copy-paste page skeleton with all critical CSS
├── REQUIRED-CSS.md                  ← reference: what each CSS rule does and why
├── pages/                           ← generated test/output pages
│   └── (your pages go here)
└── design-system/                   ← git submodule → UMD-Digital/design-system
    ├── packages/components/         ← component source code
    └── ...
```

## Setup

### 1. Clone with submodule

```bash
git clone --recursive git@github.com:zaida-umd/design-system-page-builder.git
cd design-system-page-builder
```

If you already cloned without `--recursive`:

```bash
git submodule init
git submodule update
```

### 2. Update the design system submodule (when a new DS version drops)

```bash
cd design-system
git pull origin main
cd ..
git add design-system
git commit -m "Update design-system submodule to latest"
```

### 3. Claude project setup

Add these files as project knowledge in your Claude project:
- `umd-component-registry.json`
- `RULES.md`
- `TEMPLATE.html`
- `REQUIRED-CSS.md`

The full `design-system/` directory is too large for project knowledge, but having it on disk means Claude (via Claude in Chrome or computer use) can inspect specific source files when investigating component behavior.

## How it works

1. **Registry** (`umd-component-registry.json`) — Every component's tag name, slots, attributes, variants, and known gotchas, verified directly from the npm package source.

2. **Rules** (`RULES.md`) — Composition patterns, CSS requirements, spacing utilities, and hard-won lessons from testing. Covers critical CSS load order, `container-type` splits, pathway background requirements, theme cascade behavior, and more.

3. **Template** (`TEMPLATE.html`) — A complete page skeleton with all required CSS pre-assembled. Copy it, fill in the content sections, and you have a working page.

4. **CSS Reference** (`REQUIRED-CSS.md`) — Documents every CSS rule in the template: what it does, why it's needed, and what breaks without it.

## Key principles

- **`cdn.js` is the authoritative source** — not staging pages, not official docs. Discrepancies are documented as gotchas.
- **`data-theme` does not cascade** across shadow DOM boundaries. Each child component needs its own theme attribute.
- **`container-type` is component-specific** — nav header, nav-item, and CTA need `normal`; everything else needs `inline-size`.
- **Critical CSS must load before `cdn.js`** — inline `<style>` block, not a `<link>` tag, for standalone HTML files.
- **Don't invent content** — eyebrows, headlines, and labels come from the source material or not at all.

## Verification sources (in priority order)

1. `cdn.js` dist file (from npm package or submodule build)
2. `beta.umd-staging.com` (live DOM inspection)
3. Storybook references

When sources disagree, `cdn.js` wins and the discrepancy is documented in the registry.
