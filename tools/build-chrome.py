#!/usr/bin/env python3
"""Inline a project's shared site chrome into every page under `pages/`.

Run from a project root that vendors page-builder as a submodule, after
editing anything in `shared/`:

    python3 page-builder/tools/build-chrome.py
    python3 page-builder/tools/build-chrome.py --check   # CI: non-zero if stale

Source of truth is the project's `shared/` directory — see `tools/chrome.py`
for the region contract, the `{{ROOT}}` depth token, and the contextual-drawer
rules. Regions whose source file is absent are skipped, so a project needs only
the files it actually has.

How it works
  Each region is delimited by `SHARED:<key>:START` / `:END` comments. On the
  first run those markers do not exist yet, so the script LOCATES the existing
  region by content and wraps it — that is the migration path for a project
  whose chrome is currently copy-pasted into each page. On later runs it simply
  replaces what is between the markers. Both paths are idempotent.

  A project that also generates pages imports `chrome.Chrome` and emits the
  same blocks, so running either that generator or this script converges on the
  same bytes.

Migrating a project whose pages carry chrome CSS or scripts inline
  This script does not strip inline chrome rules out of a page's own <style> or
  <script> blocks — what counts as "chrome CSS" differs per project, and a
  wrong guess deletes real page styles. Move those rules into
  `shared/chrome.css` / `shared/chrome-scripts.html` by hand first, delete the
  originals, then run this script. The `--check` run afterwards confirms every
  page converged.
"""
import argparse
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chrome import Chrome  # noqa: E402


# ------------------------------------------------------------------- locate
# Used only on the first run, to find chrome that is not yet marker-wrapped.
def find_between(src, start_re, end_re):
    a = re.search(start_re, src)
    if not a:
        return None
    b = re.search(end_re, src[a.start():])
    if not b:
        return None
    return a.start(), a.start() + b.end()


def locate_header(src):
    """The header stack, whichever component it happens to open with.

    Projects vary in whether they carry the utility nav and utility header
    above `umd-element-navigation-header`, so this anchors on the earliest of
    the three that is present and closes on the navigation header.
    """
    starts = [m.start() for m in (
        re.search(r'[ \t]*<umd-element-navigation-utility\b', src),
        re.search(r'[ \t]*<umd-element-utility-header\b', src),
        re.search(r'[ \t]*<umd-element-navigation-header\b', src),
    ) if m]
    if not starts:
        return None
    a = min(starts)
    b = re.search(r'</umd-element-navigation-header>', src[a:])
    return (a, a + b.end()) if b else None


def locate_footer(src):
    return find_between(src, r'[ \t]*<umd-element-footer\b', r'</umd-element-footer>')


def locate_head_meta(src):
    """Insert the shared <head> meta immediately after the viewport meta.

    Anchored there rather than at the top of <head> so it lands below charset
    and viewport — which browsers want early — and above the page's own
    <title>/description, which stay per-page.
    """
    m = re.search(r'^[ \t]*<meta name="viewport"[^>]*>[^\n]*$', src, re.M)
    # m.end() sits on the newline; +1 puts the block on its own line below.
    return (m.end() + 1, m.end() + 1) if m else None


def locate_css_slot(src):
    """Insert a new chrome-CSS block immediately before </head>."""
    m = re.search(r'\n</head>', src)
    return (m.start() + 1, m.start() + 1) if m else None


def locate_gate_slot(src):
    """The gate block goes in <head>, like the chrome CSS.

    It has to be in the document head, not the body: it locks the page in CSS
    before the first paint, so a body-level insertion would flash the content
    it exists to hide.
    """
    return locate_css_slot(src)


def locate_script_slot(src):
    """Insert the chrome scripts immediately before </body>."""
    m = re.search(r'\n</body>', src)
    return (m.start() + 1, m.start() + 1) if m else None


# An end-of-body shared-script tag, with any HTML comment attached above it.
# `scripts/<name>.js` only — the cdn.js tag in <head> is served from a
# `/dist/` path and inline <script> blocks have no src, so neither matches.
_SHARED_SCRIPT = (r'(?:[ \t]*<!--(?:(?!-->).)*?-->[ \t]*\n)?'
                  r'[ \t]*<script src="[^"]*scripts/[\w-]+\.js"></script>[ \t]*')


def locate_page_scripts(src):
    """The existing shared-script tags, so they are REPLACED, not duplicated.

    TEMPLATE.html ships one such tag with a comment above it. Falls back to a
    pure insertion before </body> for a page that has none yet.
    """
    spans = [m.span() for m in re.finditer('(?s)' + _SHARED_SCRIPT, src)]
    if spans:
        return spans[0][0], spans[-1][1]
    return locate_script_slot(src)


LOCATORS = {
    'head-meta': locate_head_meta,
    'header': locate_header,
    'footer': locate_footer,
    'chrome-css': locate_css_slot,
    'gate': locate_gate_slot,
    'page-scripts': locate_page_scripts,
    'chrome-scripts': locate_script_slot,
}


# ------------------------------------------------------------------- splice
def strip(src, key):
    """Remove a region a project no longer supplies.

    Deleting a file from `shared/` has to actually retire the region — a
    project that drops `gate.html` to go public, or `chrome-scripts.html` after
    an injection lands upstream, would otherwise keep the last generated block
    in every page with nothing left to regenerate it from. A page that never
    carried the region is untouched.
    """
    m = re.search(r'(?s)[ \t]*<!-- SHARED:%s:START.*?<!-- SHARED:%s:END -->\n?'
                  % (key, key), src)
    if not m:
        return src, 'unchanged'
    return src[:m.start()] + src[m.end():], 'removed'


def splice(src, chrome, key, page):
    block = chrome.block(key, page)

    m = re.search(r'(?s)[ \t]*<!-- SHARED:%s:START.*?<!-- SHARED:%s:END -->'
                  % (key, key), src)
    if m:
        if src[m.start():m.end()] == block:
            return src, 'unchanged'
        return src[:m.start()] + block + src[m.end():], 'updated'

    span = LOCATORS[key](src)
    if span is None:
        return src, 'absent'
    a, b = span
    # A zero-width span is a pure insertion (the region has no existing markup
    # to replace); it needs its own trailing newline, or the block runs into
    # whatever follows — e.g. "<!-- SHARED:chrome-css:END --></head>".
    tail = '\n' if a == b else ''
    return src[:a] + block + tail + src[b:], 'migrated'


# ---------------------------------------------------------------------- run
def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--root', default=os.getcwd(),
                    help='project root holding shared/ and pages/ (default: cwd)')
    ap.add_argument('--pages', default='pages',
                    help='directory of pages to write, relative to root (default: pages)')
    ap.add_argument('--check', action='store_true',
                    help='exit non-zero if any page would change; write nothing')
    args = ap.parse_args()

    try:
        chrome = Chrome(args.root)
    except FileNotFoundError as e:
        sys.exit('error: %s' % e)

    root = chrome.root
    pages = sorted(glob.glob(os.path.join(root, args.pages, '**', '*.html'),
                             recursive=True))
    if not pages:
        sys.exit('error: no .html files under %s/' % args.pages)

    keys = chrome.keys()
    if not keys:
        sys.exit('error: %s holds none of the known chrome files (%s)'
                 % (chrome.shared, ', '.join(chrome.source_file(k) for k in LOCATORS)))

    changed, report = [], []
    for path in pages:
        original = open(path, encoding='utf-8').read()
        src = original
        notes = []
        for key in LOCATORS:
            if key in keys:
                src, status = splice(src, chrome, key, path)
            else:
                src, status = strip(src, key)
            if status != 'unchanged':
                notes.append('%s:%s' % (key, status))

        name = os.path.relpath(path, root)
        if src != original:
            changed.append(name)
            if not args.check:
                open(path, 'w', encoding='utf-8').write(src)
        report.append((name, 'CHANGED' if src != original else 'ok', notes))

    w = max(len(n) for n, _, _ in report)
    for name, status, notes in report:
        print('  %-*s  %-8s %s' % (w, name, status, '; '.join(notes)))

    print('\n%d/%d page(s) %s  [regions: %s]'
          % (len(changed), len(pages),
             'would change' if args.check else 'written', ', '.join(keys)))
    if args.check and changed:
        sys.exit(1)


if __name__ == '__main__':
    main()
