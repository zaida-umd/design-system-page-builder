# Recommend the Best Component

Help identify the right UMD design system component for a given piece of content or use case.

## Setup

Read `umd-component-registry.json` in full before making any recommendation. This is the authoritative source — do not suggest components not in the registry.

## Process

1. **Understand the content** — ask (or infer from context) what the content is and what job it needs to do:
   - What *type* of content is it? (headline + image, stats, quote, navigation, cards, hero, form, etc.)
   - What is its *purpose* on the page? (capture attention, orient the user, showcase data, provide navigation, feature a story, etc.)
   - Where does it appear? (top of page, mid-page section, sidebar, full-width band, etc.)
   - Are there constraints? (must have image, needs a CTA, has a lot of text, etc.)

2. **Match to registry** — scan the registry for candidates and narrow to 1–3 best options.

3. **Recommend** — for each candidate:
   - Component tag name
   - Why it fits this content
   - Any variants or attributes to use (`data-display`, `data-theme`, etc.)
   - Any gotchas or rules that apply (reference the relevant RULES.md section)
   - A minimal working code example with realistic placeholder content

4. **Distinguish close alternatives** — if two components are similar (e.g. `umd-element-hero` vs `umd-element-hero-minimal`, or `umd-element-pathway` overlay vs standard), explain the tradeoff clearly so the user can choose.

## Component cheat-sheet (quick reference)

| Content type | First component to consider |
|---|---|
| Top-of-page hero with image | `umd-element-hero` (`data-display="overlay"` for photo, `data-display="stacked"` for clean) |
| Page title / section header bar | `umd-element-hero-minimal` |
| Split image + text feature | `umd-element-pathway` (`data-display="overlay"` for standalone, standard for dark-section use) |
| Stats / metrics | `umd-element-stat` with grid wrapper |
| News/story cards | `umd-element-card` (standard) or `umd-element-card-overlay` (type="image" for photo bg) |
| Section heading + CTA | `umd-element-section-intro` (centered) or `umd-element-section-intro-wide` (with watermark) |
| Pull quote / testimonial | `umd-element-quote` (standard) or `data-display="featured"` for large format |
| Full-bleed image scroll effect | `umd-layout-image-expand` |
| FAQ / expandable content | `umd-element-accordion-item` |
| Person profile | `umd-element-person-bio` |
| Icon + text card | `umd-element-card-icon` |
| Video card | `umd-element-card-video` or `umd-element-hero-brand-video` |
| Grid logo/brand hero | `umd-element-hero-grid` or `umd-element-hero-logo` |
| Top-level navigation | `umd-element-navigation-header` + `umd-element-nav-item` |

## Output format

Lead with the **primary recommendation** and a one-line rationale. Then show the code example. If there are strong alternatives, list them after with a brief "vs" comparison. Keep it concise — the user can ask to go deeper on any option.
