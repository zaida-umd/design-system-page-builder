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
after it are left alone. Keep page-local CSS in a SECOND block — a page that
appends its own rules to the end of the first block loses them on the next
sync. That is not hypothetical: it destroyed test-rich-text-landing.html's
.stats-row / .news-grid grid CSS on 2026-08-28, silently, and the stats and
news sections rendered as stacked full-width blocks for ten days before anyone
noticed. The tool now refuses to overwrite a block containing selectors that
are not in critical.css, and names them; pass --force to override.
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
FORCE = False


class ForeignCSS(Exception):
    """The first <style> block holds rules that are not in critical.css."""
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


SELECTOR_RE = re.compile(r'(?:^|[{}])\s*([^{}@/][^{}]*?)\s*\{', re.M)


def selectors(css):
    """Rough set of selectors in a stylesheet. Comments stripped first.

    Deliberately loose — it only needs to be good enough to notice rules that
    are in a page's <style> block but not in critical.css. At-rules are skipped
    (the [^{}@/] guard), so selectors nested in @media still get collected.
    """
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    out = set()
    for m in SELECTOR_RE.finditer(css):
        # Normalise whitespace: the same grouped selector is indented
        # differently in critical.css and in a page's inlined copy, and a
        # newline-vs-space difference must not read as a different rule.
        sel = ' '.join(m.group(1).split())
        if sel:
            out.add(sel)
    return out


def foreign_rules(block, css):
    """Selectors present in a page's block but absent from critical.css.

    This is the guard for the failure that ate test-rich-text-landing.html's
    grid CSS on 2026-08-28: that page kept its page-local .stats-row/.news-grid
    rules at the END of the same <style> block critical.css was inlined into,
    so re-inlining silently overwrote them. Nothing errored; the stats and news
    grids just stopped being grids. A page keeping local CSS must put it in a
    SECOND <style> block, which this tool never touches.
    """
    return sorted(selectors(block) - selectors(css))


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

    existing = src[start:tail]
    with open(CRITICAL, encoding='utf-8') as fh:
        stray = foreign_rules(existing, fh.read())
    if stray and not FORCE:
        raise ForeignCSS(stray)

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
    ap.add_argument('--force', action='store_true',
                    help='overwrite a <style> block even if it holds rules that are not '
                         'in critical.css (default: refuse — those rules would be lost)')
    args = ap.parse_args()

    global FORCE
    FORCE = args.force

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
        stale, blocked = [], []
        for p in files:
            with open(p, encoding='utf-8') as fh:
                before = fh.read()
            try:
                r = rewrite(p)
            except ForeignCSS as e:
                blocked.append((os.path.relpath(p, root), e.args[0]))
                continue
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
        for rel, rules in blocked:
            print('  BLOCKED  %s — page-local CSS in the inline block: %s'
                  % (rel, ', '.join(rules[:5]) + (' ...' if len(rules) > 5 else '')))
        print('\n%d file(s) stale, %d blocked' % (len(stale), len(blocked)))
        sys.exit(1 if (stale or blocked) else 0)

    changed, skipped, blocked = [], [], []
    for p in files:
        rel = os.path.relpath(p, root)
        try:
            r = rewrite(p)
        except ForeignCSS as e:
            blocked.append((rel, e.args[0]))
            continue
        if r is None:
            skipped.append(rel)
        elif r:
            changed.append(rel)
    for c in changed:
        print('  updated  ' + c)
    for rel, rules in blocked:
        print('  BLOCKED  ' + rel)
        print('           these rules are in the inline block but not in critical.css')
        print('           and would be destroyed: ' + ', '.join(rules[:8])
              + (' ...' if len(rules) > 8 else ''))
        print('           Move them to a SECOND <style> block (never touched), or')
        print('           re-run with --force if they are genuinely disposable.')
    print('\n%d file(s) updated, %d already current, %d without an inline block, %d blocked'
          % (len(changed), len(files) - len(changed) - len(skipped) - len(blocked),
             len(skipped), len(blocked)))
    if blocked:
        sys.exit(1)


if __name__ == '__main__':
    main()
