#!/usr/bin/env python3
"""Re-inline styles/critical.css into TEMPLATE.html and any built pages.

`critical.css` is the canonical stylesheet, but every page carries its own
VERBATIM COPY inlined in a <style> block — it has to load before cdn.js, so a
<link> will not do. That means a fix to critical.css reaches exactly nothing on
its own: TEMPLATE.html keeps handing out the old copy, and every page already
built keeps its stale one. Bugs get diagnosed, fixed at the source, and still
appear on every page.

    python3 tools/inline-critical.py                     # TEMPLATE.html
    python3 tools/inline-critical.py test qa             # + those directories
    python3 tools/inline-critical.py --check ...         # non-zero if stale
    python3 tools/inline-critical.py --root ../foo pages # a project's pages

What gets inlined is critical.css minus its leading file-header comment,
indented to sit inside the block. The header is stripped because it discusses
`<style>` tags in prose and a literal closing tag there would end the block
early — the reason this is a script and not a copy-paste step.

Only the FIRST <style> block in a file is touched; page-specific <style> blocks
after it are left alone.
"""
import argparse
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CRITICAL = os.path.join(REPO, 'styles', 'critical.css')

OPEN_RE = re.compile(r'([ \t]*)<style>\n')
CLOSE = '</style>'


def payload(indent='  '):
    """critical.css, header stripped and indented for the <style> block."""
    with open(CRITICAL, encoding='utf-8') as fh:
        css = fh.read()

    # Strip the leading /* ... */ file header.
    if css.lstrip().startswith('/*'):
        end = css.find('*/')
        if end == -1:
            sys.exit('error: critical.css opens a block comment it never closes')
        css = css[end + 2:]
    css = css.strip('\n')

    body = indent + '  '
    out = []
    for line in css.split('\n'):
        out.append(body + line if line.strip() else '')
    return '\n'.join(out)


def rewrite(path):
    """Replace the first <style> block's contents. Returns True if changed."""
    with open(path, encoding='utf-8') as fh:
        src = fh.read()

    m = OPEN_RE.search(src)
    if not m:
        return None                      # no inline block — not a built page
    start = m.end()
    end = src.find(CLOSE, start)
    if end == -1:
        return None
    # Keep the closing tag on its own indented line.
    tail = src.rfind('\n', start, end)
    if tail == -1:
        return None

    new = src[:start] + payload(m.group(1)) + src[tail:]
    if new == src:
        return False
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(new)
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('targets', nargs='*',
                    help='directories of .html files to sync, relative to --root '
                         '(TEMPLATE.html is always included when --root is this repo)')
    ap.add_argument('--root', default=REPO,
                    help='where the target directories live (default: the page-builder repo)')
    ap.add_argument('--check', action='store_true',
                    help='exit non-zero if any file is stale; write nothing')
    args = ap.parse_args()

    files = []
    root = os.path.abspath(args.root)
    if root == REPO:
        files.append(os.path.join(REPO, 'TEMPLATE.html'))
    for t in args.targets:
        files += sorted(glob.glob(os.path.join(root, t, '**', '*.html'), recursive=True))
    if not files:
        sys.exit('error: no files to sync')

    if args.check:
        # Compare without writing.
        stale = []
        for p in files:
            with open(p, encoding='utf-8') as fh:
                before = fh.read()
            r = rewrite(p)
            if r is None:
                continue
            with open(p, encoding='utf-8') as fh:
                after = fh.read()
            if r:
                with open(p, 'w', encoding='utf-8') as fh:
                    fh.write(before)     # restore
                stale.append(os.path.relpath(p, root))
        for s in stale:
            print('  STALE  ' + s)
        print('\n%d file(s) stale' % len(stale))
        sys.exit(1 if stale else 0)

    changed, skipped = [], []
    for p in files:
        r = rewrite(p)
        rel = os.path.relpath(p, root)
        if r is None:
            skipped.append(rel)
        elif r:
            changed.append(rel)
    for c in changed:
        print('  updated  ' + c)
    print('\n%d file(s) updated, %d already current, %d without an inline block'
          % (len(changed), len(files) - len(changed) - len(skipped), len(skipped)))


if __name__ == '__main__':
    main()
