---
name: Avoid repetitive straight card grids — use layout variety
description: Don't repeat standard card grids; break them up with masonry, offset, or non-straight components like pathways
type: feedback
---

Avoid using standard card styles (`umd-element-card`) repetitiously in a straight grid. If a section has multiple items, prefer visual variation.

**Why:** Straight grids of uniform cards feel monotonous. Masonry, offset, or overlay layouts create rhythm and visual interest. The designer's mockup consistently broke up straight elements.

**How to apply:**
- For 2–3 feature cards with images: prefer `umd-element-card-overlay` in `umd-layout-grid-masonry` over `umd-element-card` in a straight grid.
- For longer lists: consider mixing a featured item (pathway or sticky column) with a supporting list.
- Ask: is there a non-straight component that fits? (`umd-element-pathway`, `umd-element-card-overlay`, masonry layout) — use it before defaulting to a uniform grid.
