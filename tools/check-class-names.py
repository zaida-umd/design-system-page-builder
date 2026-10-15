#!/usr/bin/env python3
"""Check a built page's house class names against RULES.md section 40.

A house class is any class a page uses or defines that the design system does
not ship: not in styles/critical.css, not in a DS `umd-<namespace>-` family,
and not a CMS-style utility. Each one is a class a developer has to carry into
the CMS, so it must already be in the production convention:

    umd-<namespace>-<component>[-<part>]     full words, single hyphens

Errors:   no `umd-<namespace>-` prefix, a foreign `umd-` namespace, BEM `__`/`--`,
          uppercase, a state class (`is-open`, `open`, ...), or a known
          abbreviation (`desc`, `num`, `chev`, any 1-2 letter word).
Warnings: a word not in the system dictionary. These are often abbreviations
          (`wta`) but may be real terms (`faq`, `terp`). Confirm by eye.

Usage:  python3 tools/check-class-names.py --namespace admissions <file.html> [...]
Exit:   0 = clean or warnings only, 1 = errors found, 2 = usage error
"""
import argparse, os, re, sys
from html.parser import HTMLParser

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# DS namespaces: a `umd-<these>-...` class belongs to the design system or the
# CMS shell, never to a project. Extended at runtime from critical.css.
DS_NAMESPACES = {
    'element', 'layout', 'text', 'sans', 'serif', 'animation', 'action',
    'field', 'forms', 'interactive', 'statistic', 'shell', 'watermark',
    'pill', 'skip', 'eyebrow', 'media', 'adjacent', 'filter', 'campaign',
    'tailwing', 'tailwings',
}
# Page-builder scaffolding that never reaches the CMS.
EXEMPT_PREFIXES = ('umd-gate',)
# Short forms the CMS itself ships (`umd-shell-nav-promo-img`, ...).
ALLOWED_SHORT = {'img', 'nav', 'cta', 'faq', 'faqs', 'umd'}
# Real two-letter words, so `is-in` is not reported as an abbreviation.
TWO_LETTER_WORDS = {'in', 'on', 'to', 'of', 'at', 'by', 'up', 'an', 'or',
                    'no', 'is', 'as', 'be', 'do', 'go', 'me', 'my', 'we', 'us'}
# Web vocabulary missing from the system dictionary.
WEB_WORDS = {'promo', 'intro', 'stat', 'stats', 'checklist', 'lede',
             'dropdown', 'zigzag', 'navbar', 'tooltip', 'carousel', 'url'}
ABBREVIATIONS = {
    'desc': 'description', 'abbr': 'abbreviation', 'num': 'number',
    'chev': 'chevron', 'btn': 'button', 'intl': 'international',
    'req': 'requirement', 'reqs': 'requirements', 'sep': 'separator',
    'msg': 'message', 'cal': 'calendar', 'rep': 'representative',
    'reps': 'representatives', 'info': 'information', 'col': 'column',
    'cols': 'columns', 'hdr': 'header', 'ftr': 'footer', 'lbl': 'label',
    'txt': 'text', 'img-wrap': 'figure', 'ctrl': 'control',
    'prev': 'previous', 'nxt': 'next', 'sect': 'section', 'wrap': None,
}
STATE_WORDS = {'open', 'active', 'selected', 'collapsed', 'expanded',
               'visible', 'hidden', 'current', 'disabled'}
# Tailwind-style utilities the CMS itself emits. Not house classes.
UTILITY = re.compile(
    r'^(?:(?:sm|md|lg|xl|hover|focus):)?(?:'
    r'[mp][trblxy]?-|(?:max|min)-[wh]-|[wh]-|text-|bg-|fill-|gap-|size-|'
    r'items-|justify-|overflow-|transition|duration-|caption-|'
    r'(?:inline-)?(?:block|flex|grid|table)(?:-|$)|'
    r'(?:relative|absolute|fixed|sticky|hidden|flex-none|sr-only)$)')

CLASS_IN_CSS = re.compile(r'\.(-?[A-Za-z_][\w-]*)')


def css_classes(css):
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    css = re.sub(r'url\([^)]*\)', '', css)
    css = re.sub(r'"[^"]*"|\'[^\']*\'', '', css)
    # Only selectors, not declaration values like `0.5rem` or `1.2`.
    sels = re.sub(r'\{[^{}]*\}', '{}', css)
    return set(CLASS_IN_CSS.findall(sels))


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.used, self.css, self.script, self._in = set(), [], [], None

    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k == 'class' and v:
                self.used.update(v.split())
        if tag in ('style', 'script'):
            self._in = tag

    def handle_endtag(self, tag):
        if tag == self._in:
            self._in = None

    def handle_data(self, data):
        if self._in == 'style':
            self.css.append(data)
        elif self._in == 'script':
            self.script.append(data)


def load_dictionary():
    for path in ('/usr/share/dict/words', '/usr/share/dict/web2'):
        if os.path.exists(path):
            with open(path, encoding='utf-8', errors='ignore') as fh:
                return {w.strip().lower() for w in fh}
    return None


def in_dictionary(word, words):
    if words is None or word.isdigit() or word in words:
        return True
    for suffix, repl in (('ies', 'y'), ('es', ''), ('s', ''), ('ing', ''),
                         ('ed', ''), ('d', ''), ('er', '')):
        if word.endswith(suffix) and word[:-len(suffix)] + repl in words:
            return True
    return False


def check(name, ns, words):
    errors, warnings = [], []
    want = f'umd-{ns}-'
    if name != name.lower():
        errors.append('uppercase; use lowercase words joined by hyphens')
    if '__' in name or '--' in name:
        errors.append('BEM `__`/`--`; a variant is just another hyphenated part')
    parts = name.lower().replace('__', '-').replace('--', '-').split('-')
    if name.startswith(want):
        words_part = parts[2 + ns.count('-'):]
    elif name.startswith('umd-'):
        errors.append(f'namespace `umd-{parts[1]}-` is not this project\'s; '
                      f'use `{want}…` (or the exact DS/CMS name if one exists)')
        words_part = parts[2:]
    else:
        errors.append(f'no namespace; rename to `{want}…`')
        words_part = parts
    if parts[0] in ('is', 'has') or (len(words_part) == 1 and words_part[0] in STATE_WORDS):
        errors.append('state class; use `hidden`, `aria-expanded` or a `data-*` attribute')
    for w in words_part:
        if not w or w in ALLOWED_SHORT or w in WEB_WORDS or w.isdigit():
            continue
        if w in ABBREVIATIONS and ABBREVIATIONS[w]:
            errors.append(f'`{w}` is an abbreviation; write `{ABBREVIATIONS[w]}`')
        elif len(w) <= 2 and w not in TWO_LETTER_WORDS:
            errors.append(f'`{w}` is an abbreviation; write the full word(s)')
        elif not in_dictionary(w, words):
            warnings.append(f'`{w}` is not a dictionary word; abbreviation?')
    return errors, warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--namespace', required=True,
                    help="the project's site namespace, e.g. admissions")
    ap.add_argument('files', nargs='+')
    args = ap.parse_args()
    ns = args.namespace.strip().lower()
    if not re.fullmatch(r'[a-z]+(?:-[a-z]+)*', ns) or ns in DS_NAMESPACES:
        print(f'error: bad namespace {args.namespace!r}', file=sys.stderr)
        return 2

    with open(os.path.join(REPO, 'styles', 'critical.css'), encoding='utf-8') as fh:
        sanctioned = css_classes(fh.read())
    DS_NAMESPACES.update(c.split('-')[1] for c in sanctioned
                         if c.startswith('umd-') and c.count('-') >= 2)
    words = load_dictionary()

    n_err = n_warn = 0
    for path in args.files:
        page = Page()
        with open(path, encoding='utf-8') as fh:
            page.feed(fh.read())
        # Classes toggled from script are state, so they count as house classes too.
        toggled = set(re.findall(r'classList\.(?:add|remove|toggle|contains)\(\s*[\'"]([\w-]+)',
                                 '\n'.join(page.script)))
        candidates = page.used | css_classes('\n'.join(page.css)) | toggled
        house = sorted(
            c for c in candidates
            if c not in sanctioned
            and not c.startswith(EXEMPT_PREFIXES)
            and not UTILITY.match(c)
            and not (c.startswith('umd-') and c.count('-') >= 1
                     and c.split('-')[1] in DS_NAMESPACES and c.split('-')[1] != ns))
        for c in house:
            errs, warns = check(c, ns, words)
            for e in errs:
                print(f'ERROR   {path}: .{c} — {e}')
            for w in warns:
                print(f'WARNING {path}: .{c} — {w}')
            n_err += bool(errs)
            n_warn += bool(warns) and not errs
    print(f'{len(args.files)} file(s): {n_err} class(es) with errors, '
          f'{n_warn} with warnings only', file=sys.stderr)
    return 1 if n_err else 0


if __name__ == '__main__':
    sys.exit(main())
