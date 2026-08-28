"""Shared site chrome — one source of truth for a project's header and footer.

Every page in a design project must carry the same header, navigation, logo,
and footer. Copy-pasting that chrome between pages is what this module exists
to prevent: the copies drift, and a page assembled from a sibling's markup plus
TEMPLATE.html's <head> silently loses the CSS the chrome depends on — no
console error, no broken layout, just unstyled chrome.

A project keeps its chrome in a `shared/` directory:

    shared/head-meta.html       <head> meta every page carries (robots,
                                theme-color, verification tokens)
    shared/header.html          header stack (navigation-utility +
                                utility-header + navigation-header, with the
                                project's own nav items and logo)
    shared/footer.html          footer
    shared/chrome.css           CSS companions the chrome markup depends on
    shared/page-scripts.html    end-of-body <script src> tags every page loads
    shared/chrome-scripts.html  chrome-driven shadow injections

All six are optional — a region whose file is absent is simply skipped, so a
project with no shadow injections needs no `chrome-scripts.html`.

`head-meta` is site-wide meta only. A page's own `<title>` and
`<meta name="description">` stay in the page — they differ per page, and the
region is spliced verbatim into all of them.

`page-scripts` exists for the same reason as `{{ROOT}}`: TEMPLATE.html ships
`<script src="../scripts/grid-animations.js">`, which is right for a page in
this repo's own `test/` and wrong everywhere else — a project needs
`page-builder/scripts/...`, at a depth that differs per page. Left to
hand-editing it silently 404s on exactly the pages that sit one level deeper.

`tools/build-chrome.py` splices these into hand-authored pages. A project that
also *generates* pages (a script that emits `pages/programs.html` from a data
file) imports this module and emits the same blocks, so both paths produce
byte-identical output and running either converges.

Markup, CSS, and scripts are deliberately in ONE module. Splitting them is the
original bug described above.

Usage from a project's own build script, with page-builder vendored as a
submodule at `page-builder/`:

    import sys, os
    ROOT = os.path.dirname(os.path.abspath(__file__))        # project root
    sys.path.insert(0, os.path.join(ROOT, 'page-builder', 'tools'))
    from chrome import Chrome

    chrome = Chrome(ROOT)
    html = chrome.block('header', 'pages/academics/programs.html')

Depth
    Pages live at more than one depth under `pages/` (`pages/index.html` but
    also `pages/academics/programs.html`), so the chrome cannot hard-code
    `../`. Every path in `shared/` is written repo-root-relative behind a
    `{{ROOT}}` token, and `payload`/`block` expand it to the right number of
    `../` for the page being written:

        <img src="{{ROOT}}images/logos/site-logo.svg">
        <a href="{{ROOT}}pages/academics/programs.html">Programs</a>

    `payload`/`block` therefore take the OUTPUT PAGE PATH, not a depth —
    `depth_of()` derives the depth from it, and the drawer needs the path
    itself (see below). `depth_of()` is public for callers resolving {{ROOT}}
    in their own body markup.

Contextual drawer
    The mobile drawer in `shared/header.html` is one shared blob, but it has to
    open on the section the reader is already in. The design system drives that
    from two attributes — `data-active` on the children-slides group,
    `data-selected` on the current link — so `_mark_current` stamps them per
    page, matching the page's own path against the drawer's hrefs while they
    are still {{ROOT}}-relative.

    The section is the page's directory under `pages/`, which is why the
    drawer's `data-parent-ref` values ARE those directory names. A page in no
    section, or in a section with no drawer group, matches nothing and the
    drawer opens at its top level — which is correct.

    Only the region between `<!-- DRAWER:START` and `<!-- DRAWER:END -->` is
    stamped. The desktop nav deliberately carries no current-page state. A
    header with no DRAWER markers is left alone.
"""
import os
import re

ROOT_TOKEN = '{{ROOT}}'

_START = '  <!-- SHARED:%s:START — generated from shared/%s; do not edit here -->'
_END = '  <!-- SHARED:%s:END -->'

# key -> (source file, wrapper applied to the file's contents)
REGIONS = {
    'head-meta':      ('head-meta.html',     lambda s: s),
    'header':         ('header.html',        lambda s: s),
    'footer':         ('footer.html',        lambda s: s),
    'chrome-css':     ('chrome.css',         lambda s: '  <style>\n' + s + '\n  </style>'),
    'page-scripts':   ('page-scripts.html',  lambda s: s),
    'chrome-scripts': ('chrome-scripts.html', lambda s: s),
}

_DRAWER_START = '<!-- DRAWER:START'
_DRAWER_END = '<!-- DRAWER:END -->'


# TEMPLATE.html carries no robots meta — it is the generic page-builder
# skeleton, and whether a page should be indexed is a project decision, not a
# design-system one. Prototype and client-review projects generally should not
# surface in search. The googlebot line is a belt-and-braces duplicate: a
# robots.txt is only read from the HOST root, and a GitHub Pages project site is
# served from /<repo>/, so a robots.txt in a project repo would never be
# fetched — the meta is the only mechanism that actually applies there.
ROBOTS_META = ('<meta name="robots" content="noindex, nofollow">\n'
               '  <meta name="googlebot" content="noindex, nofollow">')


def with_robots(head):
    """Insert the noindex meta right after the viewport meta. Idempotent."""
    if 'name="robots"' in head:
        return head
    m = re.search(r'^(\s*)<meta name="viewport"[^>]*>[^\n]*$', head, re.M)
    assert m, 'head has no viewport meta to anchor the robots meta to'
    return head[:m.end()] + '\n' + m.group(1) + ROBOTS_META + head[m.end():]


class Chrome:
    """The chrome in one project's `shared/` directory.

    `root` is the PROJECT root — the directory holding `shared/` and `pages/`.
    It is never derived from this file's location: with page-builder vendored
    as a submodule, `__file__` sits inside `page-builder/tools/`, which is not
    the project root. Callers pass it explicitly.
    """

    def __init__(self, root, shared_dir='shared'):
        self.root = os.path.abspath(root)
        self.shared = os.path.join(self.root, shared_dir)
        if not os.path.isdir(self.shared):
            raise FileNotFoundError(
                'no %s/ directory in %s — is this a project root?'
                % (shared_dir, self.root))

    # ------------------------------------------------------------- regions
    def source_file(self, key):
        return REGIONS[key][0]

    def has(self, key):
        """Whether this project supplies the region. Absent files are skipped."""
        return os.path.isfile(os.path.join(self.shared, self.source_file(key)))

    def keys(self):
        """The regions this project actually supplies, in canonical order."""
        return [k for k in REGIONS if self.has(k)]

    def _read(self, name):
        with open(os.path.join(self.shared, name), encoding='utf-8') as fh:
            return fh.read().rstrip('\n')

    # ------------------------------------------------------------- paths
    def depth_of(self, path):
        """How many `../` a page at `path` needs to reach the project root."""
        rel = os.path.relpath(os.path.abspath(
            os.path.join(self.root, path)), self.root)
        return len(rel.replace(os.sep, '/').split('/')) - 1

    def _rel(self, page):
        """`page` as a project-relative, forward-slash path."""
        return os.path.relpath(
            os.path.abspath(os.path.join(self.root, page)),
            self.root).replace(os.sep, '/')

    def _resolve(self, text, depth):
        return text.replace(ROOT_TOKEN, '../' * depth)

    # ------------------------------------------------------------- drawer
    @staticmethod
    def _self_hrefs(rel):
        """The {{ROOT}}-relative hrefs that mean "the page being written".

        A section landing page is linked as the directory (`pages/tuition/`),
        never as `pages/tuition/index.html`, so both spellings count as self.
        """
        hrefs = {ROOT_TOKEN + rel}
        if rel.endswith('/index.html'):
            hrefs.add(ROOT_TOKEN + rel[:-len('index.html')])
        return hrefs

    def _mark_current(self, text, rel):
        """Stamp data-active / data-selected on the drawer for one page.

        Runs BEFORE {{ROOT}} is resolved, so hrefs are still comparable to
        `rel` without knowing the page's depth.
        """
        start = text.find(_DRAWER_START)
        if start == -1:
            return text
        end = text.index(_DRAWER_END, start) + len(_DRAWER_END)
        drawer = text[start:end]

        parts = rel.split('/')
        section = parts[1] if parts[0] == 'pages' and len(parts) > 2 else None
        if section:
            drawer = drawer.replace(
                '<div data-parent-ref="%s">' % section,
                '<div data-parent-ref="%s" data-active>' % section)

        for href in self._self_hrefs(rel):
            # The closing quote is part of the needle so that pages/academics/
            # does not also match pages/academics/programs.html.
            drawer = drawer.replace('<a href="%s"' % href,
                                    '<a href="%s" data-selected' % href)

        return text[:start] + drawer + text[end:]

    # ------------------------------------------------------------- output
    def payload(self, key, page):
        """The region's content, without markers, rendered for `page`.

        `page` is the output path (absolute or project-relative): it fixes both
        the {{ROOT}} depth and, for the header, which drawer entries are
        current.
        """
        src, wrap = REGIONS[key]
        text = wrap(self._read(src))
        if key == 'header':
            text = self._mark_current(text, self._rel(page))
        return self._resolve(text, self.depth_of(page))

    def block(self, key, page):
        """The region's content wrapped in its SHARED:<key> markers."""
        return '\n'.join([_START % (key, self.source_file(key)),
                          self.payload(key, page),
                          _END % key])
