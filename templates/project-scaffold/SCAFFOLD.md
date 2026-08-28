# Project scaffold

The starting skeleton for a **new design project** built on the page builder —
a repo of its own that vendors this one as a `page-builder/` submodule.

This file documents the scaffold. It is **not** copied into the new project.

## What a project repo looks like

```
<project>/
├── CLAUDE.md          project rules; layers on page-builder/CLAUDE.md
├── README.md          human-facing orientation
├── OVERRIDES.md       project-specific shadow injections and CSS overrides
├── pages/             the pages, one directory per site section
├── shared/            header, footer, and their CSS/script companions
├── briefs/            page briefs and source notes
├── images/            project-owned images (logos, photography)
└── page-builder/      submodule → design-system-page-builder
```

The three intake modes — recreating an existing site closely, overhauling one,
or building something new — all produce this same layout. They differ only in
where content and structure come from, which is a question for `/plan-page`,
`/recreate-page`, and the build commands, not for the repo skeleton.

## Bootstrap

From the directory that will hold the new repo:

```bash
PROJECT_SLUG=belonging          # repo/dir name, lowercase
PROJECT_NAME="Belonging"        # human name used in prose

git init "$PROJECT_SLUG-design" && cd "$PROJECT_SLUG-design"
git submodule add https://github.com/zaida-umd/design-system-page-builder.git page-builder
cp -R page-builder/templates/project-scaffold/. .
rm SCAFFOLD.md
```

Substitute the two tokens **before** creating any page, so only scaffold files
are touched. Target them by name — a blanket `s/{{.*}}//` also destroys
`{{ROOT}}`, which is a real runtime token the chrome depends on and must
survive into the committed files:

```bash
grep -rl '{{PROJECT_NAME}}\|{{PROJECT_SLUG}}' . --exclude-dir=page-builder --exclude-dir=.git \
  | tr '\n' '\0' \
  | xargs -0 sed -i '' -e "s|{{PROJECT_NAME}}|$PROJECT_NAME|g" -e "s|{{PROJECT_SLUG}}|$PROJECT_SLUG|g"

# Must print nothing but {{ROOT}} occurrences:
grep -rno '{{[A-Z_]*}}' . --exclude-dir=page-builder --exclude-dir=.git | grep -v '{{ROOT}}'
```

(`grep -rlZ | xargs -0` does not work here — BSD grep emits newline-separated
names for `-lZ`, so sed receives every path as one argument and fails.)

Now create the first page and build the chrome into it:

```bash
cp page-builder/TEMPLATE.html pages/index.html
python3 page-builder/tools/build-chrome.py
git add -A && git commit -m "Initial scaffold from page-builder templates/project-scaffold"
```

`TEMPLATE.html` ships a placeholder header and footer; the first build-chrome
run **replaces** them with the project's `shared/` chrome and reports
`header:migrated; footer:migrated`. That is the expected first-run output, not a
warning.

`TEMPLATE.html` also carries its own page-authoring placeholders —
`{{PAGE_TITLE}}`, `{{HEADLINE}}`, `{{IMAGE_URL}}`, `{{CTA_URL}}` and friends.
Those are **page-level**, filled in as you write each page, and are unrelated to
the two project tokens above. That is why the verification grep runs before any
page exists.

## Then

1. Replace the placeholder nav items, logo, and footer image in `shared/`, and
   rename the `example-section` placeholders to this project's real sections.
2. Re-run `python3 page-builder/tools/build-chrome.py` after every `shared/` edit.
3. Read `page-builder/CLAUDE.md` for the canonical design-system rules, then
   this project's `CLAUDE.md` for what layers on top.

Until step 1, a fresh page logs one expected 404 for
`images/logos/<slug>-logo.svg` — the header's `onerror` fallback catches it and
renders the UMD wordmark, so the page is correct meanwhile. It clears the moment
you drop the real logo in.

## The five chrome regions

| Region | Source | Spliced |
|---|---|---|
| `header` | `shared/header.html` | replaces the header stack |
| `footer` | `shared/footer.html` | replaces `umd-element-footer` |
| `chrome-css` | `shared/chrome.css` | `<style>` before `</head>` |
| `page-scripts` | `shared/page-scripts.html` | replaces the end-of-body `scripts/*.js` tags |
| `chrome-scripts` | `shared/chrome-scripts.html` | shadow injections before `</body>` |

Delete any file the project does not need — the inliner skips a region whose
source is absent.

`page-scripts` matters more than it looks. `TEMPLATE.html` ships
`<script src="../scripts/grid-animations.js">`, which is correct only for a page
in the page-builder repo's own `test/` directory. In a project it has to point
at `page-builder/scripts/`, one extra `../` deeper for a page in a section
folder — so hand-editing it is how a site ends up with grid animations silently
dead on half its pages.

## Keeping the scaffold honest

The scaffold ships **no copy of `TEMPLATE.html`, `critical.css`, or the
registry** — those live in the submodule and a duplicate here would go stale
the first time the design system moves. `pages/index.html` is created by
copying `page-builder/TEMPLATE.html` at bootstrap time, so a new project always
starts from the current skeleton.
