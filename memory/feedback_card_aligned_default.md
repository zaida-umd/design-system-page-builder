---
name: Always use data-aligned on umd-element-card
description: Standard cards should always use data-aligned by default so images crop to consistent height in grids
type: feedback
---

Always add `data-visual-image-aligned="true"` to `umd-element-card` by default when placing cards in a grid.

**Why:** Without `data-visual-image-aligned="true"`, card images render at their natural height, causing uneven rows when images have different aspect ratios.

**How to apply:** Any time `umd-element-card` appears in a grid layout, include `data-visual-image-aligned="true"` unless there is a specific reason not to (e.g. a single standalone card where consistent cropping doesn't matter).

**CORRECTION (2026-08-28, verified against DS 1.19.5):** the attribute is
`data-visual-image-aligned="true"`. **There is no `data-aligned`** — it appears
nowhere in the design system and matches nothing, so a card written with it
silently does not align. The value must be the literal string `"true"`; a bare
attribute is inert, because the check is `isAttributeTrue`, not attribute
presence. Deprecated predecessor: `aligned="true"`. See RULES §15b.

(This directory is superseded by the Claude memory system — see the note in
MEMORY.md here. It is corrected rather than deleted because it is still the
copy that gets read from inside the repo.)
