---
name: Always use data-aligned on umd-element-card
description: Standard cards should always use data-aligned by default so images crop to consistent height in grids
type: feedback
---

Always add `data-aligned` to `umd-element-card` by default when placing cards in a grid.

**Why:** Without `data-aligned`, card images render at their natural height, causing uneven rows when images have different aspect ratios.

**How to apply:** Any time `umd-element-card` appears in a grid layout, include `data-aligned` unless there is a specific reason not to (e.g. a single standalone card where consistent cropping doesn't matter).
