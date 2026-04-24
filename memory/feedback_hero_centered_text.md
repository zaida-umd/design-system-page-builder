---
name: Center hero text when followed by non-full-width content
description: Use centered hero text when the section below is not full-bleed (e.g. quote, masonry overlay cards)
type: feedback
---

When a background/default hero is followed by a component that isn't full-width (e.g. `umd-element-quote`, masonry overlay cards, standard card grids), default to centered text.

**Why:** Left-aligned hero text creates a visual mismatch when the content below snaps to a narrower content width. Centered text anchors the page visually and transitions more gracefully.

**How to apply:** Add `data-layout-text="center"` to `umd-element-hero`. For a background image hero this pairs with `data-display="overlay"`. Only use left-aligned text when the following section is itself full-width (e.g. a pathway, a dark full-bleed section, or another hero).
