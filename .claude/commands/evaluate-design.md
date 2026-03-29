# Evaluate a Page Design

Act as an objective design critic and planner. Given a page concept or request, produce a scored design brief **before any HTML is written**. The goal is to prevent self-evaluation bias by separating the planning decision from the generation step.

## Input

The page concept is: `$ARGUMENTS`

If no concept is provided, ask the user to describe the page they want to build.

---

## Step 1 — Read context files

1. Read `umd-component-registry.json` — this is the source of truth for all available components, slots, and attributes.
2. Read `RULES.md` sections 3, 5, 9, 11, 13, 14 — these govern layout, theming, and slot usage.
3. If a specific page URL is mentioned, fetch it to understand the content.

---

## Step 2 — Propose a component plan

For each section of the page, state:
- The component name (exact tag from the registry)
- Why this component fits the content better than alternatives
- What variant/attributes you'll use (theme, display mode, layout position)
- What content goes in each slot

Format:

```
### Section [N]: [Component tag]
- **Why this component:** ...
- **Attributes:** data-theme="...", data-display="...", etc.
- **Slots:** slot="headline" → ..., slot="text" → ..., etc.
- **Alternatives considered:** [tag] — rejected because ...
```

---

## Step 3 — Score the design brief

Grade the proposed plan on four dimensions before any HTML is written. Be a tough critic — generous scores defeat the purpose.

### 1. Component Fitness (0–10)
Are the chosen components the best match for each content type? Would a different component better serve the content? Are any components being misused (wrong display mode, wrong content type)?

### 2. Layout Variety (0–10)
Does the page avoid repetition? Is there a rhythm of full-bleed, narrow, wide sections? Does it use at least 3 distinct visual patterns? Penalize pages that repeat the same section type more than twice.

### 3. Content Hierarchy (0–10)
Is the most important content first and visually prominent? Is there a clear path from hero → value prop → supporting evidence → CTA? Are callouts and stats placed where they'll have maximum impact?

### 4. Design Integrity (0–10)
Does the plan follow RULES.md? Are themes applied correctly (data-theme on each child, not cascaded)? Are spacing classes appropriate (landing vs interior)? Are full-bleed sections NOT wrapped in horizontal spacing classes?

**Total: X / 40**

If any dimension scores below 6, **stop here** and revise the plan before proceeding. Explain what needs to change.

---

## Step 4 — Identify risks

List any known pitfalls for the proposed component choices. Examples:
- "umd-element-quote with data-display="featured" requires data-visual-transparent="true" in image-expand context or it will block the background"
- "Stats grid requires slot="text" for labels — slot="label" is not valid"
- "Pathway overlay variant needs full-bleed — do not wrap in horizontal spacing class"

---

## Step 5 — Output the design brief

Produce a structured brief in this format:

```
## Design Brief: [Page Title]
**Date:** [today's date]
**Total Score:** X / 40

### Component Plan
[Section-by-section plan from Step 2]

### Scores
- Component Fitness: X/10 — [1-sentence rationale]
- Layout Variety: X/10 — [1-sentence rationale]
- Content Hierarchy: X/10 — [1-sentence rationale]
- Design Integrity: X/10 — [1-sentence rationale]

### Risks to Watch
[Bulleted list from Step 4]

### Build Approval
[APPROVED — proceed to build] OR [REVISION NEEDED — see notes below]
```

---

## Usage

This command can be run standalone:

```
/evaluate-design A landing page for UMD's College of Engineering featuring research highlights, faculty spotlights, and an application CTA
```

It is also embedded as Phase 0 in `/build-landing-page` and `/build-interior-page`. In that context, proceed to HTML only after the brief is approved (score ≥ 24/40 with no dimension below 6).
