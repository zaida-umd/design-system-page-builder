# Component Overrides & Page-Built Components

A log of **page-specific** deviations from the UMD design system. Two categories:

1. **Shadow overrides** — CSS injected into a component's shadow root to change a hard-coded rule that has no exposed CSS variable or `::part()` hook.
2. **Page-built components** — light-DOM classes/utilities authored on a single page because no DS component fits, or the closest DS component has shadow-DOM constraints that block the design (e.g. fixed max-width, fixed aspect, reprojected slots).

Both categories are **opt-in for the listed pages only.** Other pages should NOT inherit them by default — the design rationale that justified the override on page A may not apply to page B.

## When to add an entry here

Add an entry whenever a page does any of:

- Injects CSS into a component's shadow root (`el.shadowRoot.appendChild(<style>)`)
- Overrides `::part()` rules in ways that contradict the component's intended part styling
- Overrides CSS custom properties beyond documented theme tokens
- Defines a new light-DOM utility class that mirrors or extends a DS component (e.g. `.umd-action-outline-block` mirroring `umd-element-call-to-action data-display="outline"`)
- Defines a new layout class not in `LAYOUT-PATTERNS.md` or `styles/critical.css`

## When NOT to add an entry here

- **Styles that belong in `styles/critical.css`** — if every page needs it, promote it instead. Example: utility-nav anchor styles live in `critical.css`, not here.
- **Documented patterns from `LAYOUT-PATTERNS.md`** — those are sanctioned reuse, not overrides.
- **`data-*` attributes the component already supports** — that's configuration.

## How to use this log

Before adding a new shadow override or page-built class, search this file for the component name or class. If the same item already exists:

- Copy it verbatim.
- Add the new page to the "Pages using this" list.

If the same entry repeatedly accumulates pages, that's a signal to either:

- Propose a CSS variable or `::part()` upstream in the design system (for shadow overrides), or
- Graduate the class into `styles/critical.css` and document the pattern in `LAYOUT-PATTERNS.md` (for page-built components).

## Harvest step (end-of-task)

The `/recreate-page`, `/build-landing-page`, and `/build-interior-page` commands run a final harvest step that scans the new HTML file for shadow-injection IIFEs and locally-defined `.umd-*` classes that aren't in `styles/critical.css`, then appends entries here with the new page in the "Pages using this" list. The harvest does not run at the start of a build because the overrides aren't known until the page is finished.

---

# Shadow overrides

## Card-overlay horizontal padding (desktop+)

**Component:** `umd-element-card-overlay` (image variant). Renders content inside a shadow-DOM `.card-overlay-image-container` with hard-coded horizontal padding of `token.spacing.md` (24px) at every breakpoint — upstream styles only adjust `padding-top` at `medium.min`, leaving sides at 24px from mobile through 4K. On wide viewports this crowds the headline/eyebrow/CTA against the card edges.

**Override:** Shadow-inject step-up horizontal padding aligned to upstream token breakpoints (`highDef.min` = 1200px, `maximum.min` = 1500px). Vertical padding unchanged.

```css
.card-overlay-image-container { padding-left: 24px !important; padding-right: 24px !important; }
@media (min-width: 1200px) { .card-overlay-image-container { padding-left: 32px !important; padding-right: 32px !important; } }
@media (min-width: 1500px) { .card-overlay-image-container { padding-left: 48px !important; padding-right: 48px !important; } }
```

Injected after `customElements.whenDefined('umd-element-card-overlay')`, applied to every instance's `shadowRoot`.

**Upstream candidate:** fold into `web-elements-library/src/composite/card/overlay/image.ts` as additional `createMediaQuery` entries on the `card-overlay-image-container` style block, mirroring the existing `medium.min` paddingTop step-up.

**Pages using this:**
- [test/card-overlay-padding.html](test/card-overlay-padding.html) — isolated test page (temporary; remove when override graduates upstream)

---

# Page-built components

## .umd-action-outline-block — full-width outline CTA

**DS counterpart:** `umd-element-call-to-action data-display="outline"`.

**Why a page-built version was needed:** The DS outline CTA hard-codes `max-width: 380px` inside its shadow DOM. In layouts that need outline CTAs to fill a grid cell, the DS component cannot stretch. Replaced with a plain `<a>` using a light-DOM class that mirrors the DS visual (border, padding, hover) without the max-width cap.

**Class definition:** Light + dark variants. `.umd-action-outline-block` is the light version (white background, dark text); add `.dark` for the dark-section variant (transparent background, white text/border with white-fill hover).

**Pages using this:**
- [examples/search.html](examples/search.html) — "Show more / Show less" toggle for the AI Summary block (full-width outline button)
