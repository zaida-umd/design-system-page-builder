# /qa-component

Build a focused QA test page for a specific design system component or component combination, to visually verify behavior (scroll, hover, layout, alignment) after a DS submodule update.

**Input:** one of:
- Component tag name — `umd-element-navigation-header`
- Linear ticket ID — `DSYS-3025`
- Both — `DSYS-3025 umd-element-navigation-header`
- Combination keyword — `sticky-columns`, `nav-slider`, `card-grid`

**Output:** `qa/{slug}.html` — where `{slug}` is the ticket ID if provided, otherwise a kebab-case component or combination name.

This command does NOT take a brief and does NOT run a harvest step. For building real pages, use `/build-landing-page` or `/build-interior-page` instead.

---

## Setup

1. Read `TEMPLATE.html` — use its full `<head>` block (critical CSS + CDN script) verbatim.
2. Read `registry/registry-index.json` for the category map and `lookup_by_tag`; then load the specific category file for the component(s) under test.
3. Read every RULES.md section that applies to the component(s) under test.
4. If a Linear ticket ID was provided, fetch the issue to get context on what was fixed — use that to decide which variants and interactions to target.

---

## QA label banner

At the very top of `<body>`, before any DS elements, add a plain HTML banner that identifies what is being tested. This is the only non-DS HTML in the page — it must not affect component rendering below it.

```html
<div style="background:#ffeb3b;color:#000;padding:8px 16px;font:13px/1.4 monospace;border-bottom:2px solid rgba(0,0,0,.2);position:sticky;top:0;z-index:9999;">
  QA: {component or combination} | {ticket ID and title if available}
</div>
```

---

## Page structure

Build a **full page** — global nav, site nav, navigation header, content, footer — not a stripped-down fragment. Many bugs (scroll lock, sticky behavior, viewport height, z-index stacking) only reproduce in the full page context.

Follow the same shell structure as interior pages (`umd-element-navigation-utility` → `umd-element-utility-header` → `umd-element-navigation-header` → content → `umd-element-footer`), unless the component under test IS the shell (e.g. testing the nav header itself — then still include it, just populate it more thoroughly).

For the **navigation header**, always include:
- `sticky` attribute
- `class="umd-layout-space-horizontal-full"`
- Logo per CLAUDE.md logo rules
- At least three nav items with one having a dropdown sub-menu (tests mobile open/close and scroll)

For the **footer**, use `data-display="visual"` with **no `slot="image"`** — QA pages omit the footer background image to keep the file focused on the components under test.

---

## Content: test cases

After the shell, build **labeled test case sections** — one `<section>` per variant. Each section gets a plain `<h2>` above the component identifying what variant is being tested. Use `umd-layout-space-vertical-landing` (landing pages) or `umd-layout-space-vertical-interior` (interior context) between sections.

### Variant selection

Cover the variants most likely to surface the known bug, plus the canonical default:

| Scenario | What to include |
|---|---|
| Default / light theme | Always include first |
| Dark theme | Include unless the bug is demonstrably light-only |
| Size or layout attribute variants | Include all named variants (`data-size`, `data-layout-*`, `data-display`) |
| Mobile-specific bug | Note in the banner — visual verification requires resizing to ≤ 768px |
| Combination (e.g. sticky columns) | Show the full pattern from `LAYOUT-PATTERNS.md` — do not stub it |
| Alignment / icon bugs | Use real slot content with enough items to trigger the misalignment |

For each section, use **canonical slot content** from the registry — the minimum real content needed to render the component correctly. Do not use Lorem Ipsum; use short realistic UMD-appropriate copy.

Use **local images only** — read `images/images-index.json`, match tier and context tag, reference as `../images/{tier}/{tag}/filename.jpg`. Never use remote image URLs.

---

## Spacing and layout rules (same as all pages)

- Wrap content sections in `umd-layout-space-horizontal-larger` (or `umd-layout-space-horizontal-full` for full-bleed components).
- Use `umd-layout-vertical-landing` on landing-context sections, `umd-layout-space-vertical-interior` on interior-context sections.
- Follow all RULES.md §§ that apply to the component(s) under test.

---

## Output

Write the completed HTML file to `qa/{slug}.html`. Confirm the filename.

If a preview server is running, reload and verify the page renders. Take a screenshot as proof. If the bug is scroll- or interaction-related, note that manual resize to mobile viewport (≤ 768px) is needed to verify that behavior.

---

## Rules checklist before saving

- [ ] QA label banner present and sticky
- [ ] Full page shell (nav + footer) — not a fragment
- [ ] Navigation header has `sticky` + `umd-layout-space-horizontal-full` + dropdown sub-menu
- [ ] Each test case section has a plain `<h2>` label above it
- [ ] All images are local (`../images/…`) — no remote URLs
- [ ] Logo fallbacks use `onerror` handler per CLAUDE.md
- [ ] No custom CSS beyond the template `<head>` block
- [ ] All component slots verified against registry
- [ ] All applicable RULES.md sections checked
