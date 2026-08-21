#!/usr/bin/env python3
"""Validate data-theme values in a built page against registry/.

Catches misspelled and component-invalid theme values. This matters most for
values that render via the component's *default* fall-through -- notably
umd-element-pathway's data-theme="white" -- where a typo produces output
identical to the correct value and is therefore invisible on the page.

Usage:  python3 tools/check-themes.py <file.html> [more.html ...]
Exit:   0 = clean, 1 = problems found, 2 = usage/registry error
"""
import sys, os, json, glob
from html.parser import HTMLParser

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_allowed():
    """tag -> set(valid data-theme values), read from registry/."""
    allowed = {}
    files = glob.glob(os.path.join(REPO, 'registry', 'registry-*.json'))
    if not files:
        sys.exit('error: no registry files found under registry/')

    def walk(node):
        if isinstance(node, dict):
            tag = node.get('tag')
            attrs = node.get('attrs')
            if tag and isinstance(attrs, list):
                for a in attrs:
                    if isinstance(a, dict) and a.get('name') == 'data-theme':
                        allowed[tag] = set(a.get('values') or [])
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    for f in files:
        with open(f, encoding='utf-8') as fh:
            walk(json.load(fh))
    return allowed


class ThemeChecker(HTMLParser):
    """Two severities, because 'not listed for this component' and
    'not a theme word at all' are very different situations.

    ERROR   -- value is not in the design system's theme vocabulary at all.
               Almost certainly a typo. This is the case that is otherwise
               invisible: a component that ignores the attribute renders a
               misspelled value identically to a correct one.
    WARNING -- value is a real theme word, but the registry does not list it
               for this component. Usually inert (the component ignores it),
               occasionally an intentional convention the registry has not
               caught up with -- pathway's data-theme="white" was exactly this.
               Worth a look; not a failure.
    """

    def __init__(self, allowed, vocabulary):
        super().__init__(convert_charrefs=True)
        self.allowed = allowed
        self.vocabulary = vocabulary
        self.errors = []
        self.warnings = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if 'data-theme' not in d:
            return
        value = d['data-theme']
        if tag not in self.allowed:
            return          # unknown component: registry has no opinion
        ok = self.allowed[tag]
        line = self.getpos()[0]

        if value is None or value.strip() == '':
            self.errors.append((line, tag, value or '', 'empty value', ok))
        elif value not in self.vocabulary:
            self.errors.append((line, tag, value, 'not a design system theme '
                                'value (likely a typo)', ok))
        elif value not in ok:
            self.warnings.append((line, tag, value, 'not listed for this '
                                  'component in registry/ -- likely inert', ok))


def check(path, allowed, vocabulary):
    with open(path, encoding='utf-8') as fh:
        src = fh.read()
    p = ThemeChecker(allowed, vocabulary)
    p.feed(src)

    def emit(items, label):
        for line, tag, value, reason, ok in items:
            print(f'{label} {path}:{line}: {tag} data-theme="{value}" -- '
                  f'{reason}. Valid here: {"|".join(sorted(ok)) or "(none)"}')

    emit(p.errors, 'ERROR  ')
    emit(p.warnings, 'WARNING')
    return len(p.errors), len(p.warnings)


def main(argv):
    if not argv:
        sys.exit(__doc__)
    allowed = load_allowed()
    vocabulary = set().union(*allowed.values()) if allowed else set()
    errors = warnings = 0
    for path in argv:
        e, w = check(path, allowed, vocabulary)
        errors += e
        warnings += w

    n = len(argv)
    if errors:
        print(f'\n{errors} error(s), {warnings} warning(s) in {n} file(s).')
        return 1
    if warnings:
        print(f'\n0 errors, {warnings} warning(s) in {n} file(s).')
        return 0
    print(f'data-theme OK ({n} file(s) checked).')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
