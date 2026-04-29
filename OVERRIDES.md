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

## umd-element-pathway — image aspect ratio

**Shadow rule overridden:** `.pathway-image-container`, `.image-container`, `.umd-asset-image-wrapper-scaled` size from intrinsic image ratio. No exposed CSS variable or `::part` for the image container.

**Override applied:** Force `aspect-ratio: 1 / 1` on the image container. Inject via `customElements.whenDefined('umd-element-pathway')` after hydration.

**Reason:** Source page used pathway photos with mixed aspect ratios; design called for a uniform 1:1 grid feel across the page.

**Pages using this:**
- [test/admissions-recreation.html](test/admissions-recreation.html)
- [examples/admissions-academics.html](examples/admissions-academics.html)

---

## umd-element-banner-promo — stacked actions gap

**Shadow rule overridden:** Banner-promo reprojects `slot="actions"` into its shadow DOM under `.banner-promo-actions` with no gap between stacked CTAs.

**Override applied:**
```js
'.banner-promo-actions{display:flex!important;flex-direction:column!important;align-items:flex-end!important;gap:8px!important}'
```
Injected after `customElements.whenDefined('umd-element-banner-promo')`.

**Reason:** When primary + secondary CTAs stack vertically (rather than the default inline layout), they render flush against each other. Light-DOM `gap` does not propagate because the actions are reprojected into shadow DOM.

**Pages using this:**
- [test/admissions-recreation.html](test/admissions-recreation.html)
- [examples/admissions-academics.html](examples/admissions-academics.html)

---

## umd-element-navigation-header — logo max-width

**Shadow rule overridden:** [`design-system/packages/elements/source/composite/navigation/header.ts:204`](design-system/packages/elements/source/composite/navigation/header.ts) hard-codes `.element-header-logo img { max-width: 240px }` at tablet+ with no exposed CSS variable.

**Override applied:**
```js
'.element-header-logo img{max-width:320px!important}'
```
Injected after `customElements.whenDefined('umd-element-navigation-header')`.

**Reason:** The Undergraduate Admissions wordmark is wider than the default UMD primary logo and gets visually clipped at 240px. 320px lets the full "University of Maryland Undergraduate Admissions" lockup render legibly.

**Pages using this:**
- [test/admissions-recreation.html](test/admissions-recreation.html)

---

# Page-built components

## .umd-action-outline-block — full-width outline CTA

**DS counterpart:** `umd-element-call-to-action data-display="outline"`.

**Why a page-built version was needed:** The DS outline CTA hard-codes `max-width: 380px` inside its shadow DOM. In layouts that need outline CTAs to fill a grid cell (e.g. the "Information For" 4-column row on admissions), the DS component cannot stretch. Replaced with a plain `<a>` using a light-DOM class that mirrors the DS visual (border, padding, hover) without the max-width cap.

**Class definition:** Light + dark variants. `.umd-action-outline-block` is the light version (white background, dark text); add `.dark` for the dark-section variant (transparent background, white text/border with white-fill hover).

**Pages using this:**
- [test/admissions-recreation.html](test/admissions-recreation.html) — "Information For" 4-up row in the dark section after the hero
- [examples/search.html](examples/search.html) — "Show more / Show less" toggle for the AI Summary block (full-width outline button)

---

## .umd-text-line-trailing / .umd-text-line-trailing-dark — eyebrow with trailing line

**DS counterpart:** None. The DS has `umd-element-section-intro` for centered eyebrows, but no inline eyebrow + trailing horizontal rule pattern.

**Why a page-built version was needed:** Common UMD editorial pattern (uppercase tracked label + horizontal line that fills the rest of the row). Used to label content groups inside a section without consuming the visual weight of a full section-intro.

**Class definition:** `<p class="umd-text-line-trailing"><span>Label</span></p>`. The `<span>` masks the absolutely-positioned line so the label text stays readable. `.umd-text-line-trailing-dark` flips background/colors for dark sections.

**Pages using this:**
- [test/admissions-recreation.html](test/admissions-recreation.html) — labels the "Information For" row inside the dark section

---

## .umd-layout-grid-cards-no-gap — 3-up overlay-card grid, no gap

**DS counterpart:** `umd-layout-grid-gap-three` exists but applies a gap. There is no zero-gap variant.

**Why a page-built version was needed:** Overlay cards designed to read as a single banded surface (cards touching edge-to-edge) — adding any gap visually fragments the band.

**Companion rule:** Use with `umd-element-card-overlay.size-large` (the `.size-large` class is documented in CLAUDE.md / `web-components.ts`) so the cards have a consistent min-height across the row.

**Pages using this:**
- [test/admissions-recreation.html](test/admissions-recreation.html) — 3-up overlay-card bank below the Massey quote

---

## .umd-layout-grid-tuition-two — 2-column 1.5fr/1fr grid

**DS counterpart:** `umd-layout-grid-gap-two` is symmetric (1fr/1fr); the DS has no asymmetric two-column grid utility.

**Why a page-built version was needed:** The Tuition & Aid section pairs a wide editorial column (headline + body + primary CTA) with a narrower resource list. Symmetric columns gave the resource list more space than its content needed, breaking the visual hierarchy.

**Pages using this:**
- [test/admissions-recreation.html](test/admissions-recreation.html) — Tuition & Aid section

---

## .quote-with-chevron / .chevron-overlap — brand-chevron + quote overlap

**DS counterpart:** None. `umd-element-brand-logo-animation` is a drop-in decoration with no positioning hooks.

**Why a page-built version was needed:** To position the brand chevron behind a quote with deliberate overlap into the dark section above and the cards below. The DS component has no built-in z-index or overflow contract that supports this layout.

**Pages using this:**
- [test/admissions-recreation.html](test/admissions-recreation.html) — Massey quote between About UMD (dark) and the 3-up overlay-card bank

---

## .umd-layout-background-full-dark-arrow-right — dark section with right-arrow watermark

**DS counterpart:** `umd-layout-background-full-dark` (canonical dark band). No DS variant layers a brand background image inside the band.

**Why a page-built version was needed:** The "Information For" band on admissions calls for the FearlesslyForward right-arrow PNG anchored at `-420px 0` so only the right tail of the arrow shows behind the 4-up CTA grid. Bottom padding bumps to 160px on desktop (≥1024px) so the arrow has visual breathing room before the next section.

**Class definition:** Modifier on `.umd-layout-background-full-dark`. Sets `background: #000 url(https://fearlesslyforward.umd.edu/images/arrows/bg-arrow-right-white.png) no-repeat -420px 0` and overrides `padding-bottom: 160px` at desktop only.

**Pages using this:**
- [test/admissions-recreation.html](test/admissions-recreation.html) — Information For dark band

---

## .umd-layout-background-full-dark-no-top — dark section with no top padding

**DS counterpart:** `umd-layout-background-full-dark` (canonical dark band always carries top + bottom padding).

**Why a page-built version was needed:** When a dark band immediately follows another dark band that already has a generous bottom pad (e.g. Information For → About UMD pathway on admissions), keeping the second band's top padding stacks empty space. This modifier zeros the top pad while preserving the bottom pad for downstream rhythm.

**Pages using this:**
- [test/admissions-recreation.html](test/admissions-recreation.html) — About UMD pathway dark band, sitting below the Information For band

---

## .deadlines-table — minimal date/event two-column rows

**DS counterpart:** `umd-element-event` displays exist but render as cards. No DS component exists for compact tabular date listings.

**Why a page-built version was needed:** "Important Dates" needed a dense, scannable list of N deadlines (event name + date), not card stacks. Native `<table>` with light styling fits the use case better than forcing a card component.

**Pages using this:**
- [test/admissions-recreation.html](test/admissions-recreation.html) — Important Dates section
