#!/usr/bin/env python3
"""Manage the accounts on a project's prototype access gate.

Run from a project root that vendors page-builder as a submodule:

    python3 page-builder/tools/gate.py --write shared/gate.html            # add
    python3 page-builder/tools/gate.py --list shared/gate.html             # show
    python3 page-builder/tools/gate.py --remove reviewer shared/gate.html  # drop

Then re-run the inliner so every page picks the change up:

    python3 page-builder/tools/build-chrome.py

The password is read with getpass — never echoed, never an argument, so it
does not land in shell history or the process list. What gets written to the
repo is a PBKDF2-HMAC-SHA256 hash and its salt; the plaintext is not stored
anywhere by this script and cannot be recovered from what is.

That hash still ships to every visitor's browser inside the page, so it is
open to an offline attack by anyone with the URL. Use a password with real
entropy, do not reuse a password that unlocks anything else, and keep the
project repo private. `page-builder/scripts/gate.js` sets out what the gate
does and does not protect.
"""
import argparse
import getpass
import hashlib
import json
import os
import re
import secrets
import sys

START = '/* GATE:USERS:START'
END = 'GATE:USERS:END */'

# Matches the whole users block including both marker comments, so a rewrite
# reproduces them and stays idempotent.
_BLOCK = re.compile(
    r'(?P<indent>[ \t]*)/\* GATE:USERS:START[^\n]*\n'
    r'(?P<body>.*?)'
    r'[ \t]*/\* GATE:USERS:END \*/',
    re.S)

_USERS = re.compile(r'users:\s*(\[.*?\])\s*$', re.S)
_ITERATIONS = re.compile(r'iterations:\s*(\d+)')

DEFAULT_ITERATIONS = 310000


def load(path):
    if not os.path.isfile(path):
        sys.exit('error: %s does not exist. Copy it from '
                 'page-builder/templates/project-scaffold/shared/gate.html' % path)
    with open(path, encoding='utf-8') as fh:
        return fh.read()


def parse(src, path):
    """The gate's (iterations, users, match) — users as a list of dicts.

    The users block is written by this script alone and is plain JSON with a
    trailing `users:` key, so json.loads is enough; anything else means the
    block was hand-edited, which the error says.
    """
    m = _BLOCK.search(src)
    if not m:
        sys.exit('error: no GATE:USERS markers in %s — is this a gate.html?' % path)

    body = m.group('body')
    u = _USERS.search(body.strip())
    if not u:
        sys.exit('error: the GATE:USERS block in %s has no `users: [...]` array.' % path)
    try:
        users = json.loads(u.group(1))
    except ValueError:
        sys.exit('error: the users array in %s is not valid JSON — it was '
                 'hand-edited. Reset it to `users: []` and re-add accounts.' % path)

    it = _ITERATIONS.search(src)
    return (int(it.group(1)) if it else DEFAULT_ITERATIONS), users, m


def render(users, indent):
    """The users block, marker comments included, at the file's indent."""
    if users:
        rows = ',\n'.join(
            '%s  { "user": %s, "salt": "%s", "hash": "%s" }'
            % (indent, json.dumps(u['user']), u['salt'], u['hash'])
            for u in users)
        array = '[\n%s\n%s]' % (rows, indent)
    else:
        array = '[]'
    return ('%s/* GATE:USERS:START — written by page-builder/tools/gate.py; '
            'do not hand-edit */\n'
            '%susers: %s\n'
            '%s/* GATE:USERS:END */' % (indent, indent, array, indent))


def save(path, src, match, users):
    out = src[:match.start()] + render(users, match.group('indent')) + src[match.end():]
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(out)


def derive(password, salt_hex, iterations):
    return hashlib.pbkdf2_hmac(
        'sha256', password.encode('utf-8'), bytes.fromhex(salt_hex),
        iterations, dklen=32).hex()


def ask_credentials():
    user = input('Username: ').strip()
    if not user:
        sys.exit('error: username cannot be empty.')

    password = getpass.getpass('Password: ')
    if len(password) < 8:
        sys.exit('error: use at least 8 characters. This hash is published in '
                 'the page source, so a short password is guessable offline.')
    if password != getpass.getpass('Confirm password: '):
        sys.exit('error: passwords did not match. Nothing was written.')
    return user, password


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('path', nargs='?', default='shared/gate.html',
                    help='the project gate file (default: shared/gate.html)')
    ap.add_argument('--write', metavar='PATH', dest='write_path',
                    help='add or replace an account in PATH')
    ap.add_argument('--list', action='store_true', help='list configured usernames')
    ap.add_argument('--remove', metavar='USERNAME', help='remove an account')
    args = ap.parse_args()

    path = args.write_path or args.path
    src = load(path)
    iterations, users, match = parse(src, path)

    if args.list:
        if not users:
            print('%s: no accounts — the gate will refuse everyone.' % path)
        else:
            print('%s: %d account(s) at %d PBKDF2 rounds'
                  % (path, len(users), iterations))
            for u in users:
                print('  %s' % u['user'])
        return

    if args.remove:
        target = args.remove.strip().lower()
        kept = [u for u in users if u['user'].strip().lower() != target]
        if len(kept) == len(users):
            sys.exit('error: no account named %r in %s' % (args.remove, path))
        save(path, src, match, kept)
        print('Removed %r. %d account(s) left.' % (args.remove, len(kept)))
        print('Anyone signed in as that account keeps their session until it '
              'expires — change another password to invalidate every session.')
        print('\nNow run:  python3 page-builder/tools/build-chrome.py')
        return

    user, password = ask_credentials()
    salt = secrets.token_hex(16)
    entry = {'user': user, 'salt': salt, 'hash': derive(password, salt, iterations)}

    replaced = False
    for i, u in enumerate(users):
        if u['user'].strip().lower() == user.strip().lower():
            users[i], replaced = entry, True
    if not replaced:
        users.append(entry)

    save(path, src, match, users)
    print('\n%s %r in %s (%d PBKDF2 rounds).'
          % ('Replaced' if replaced else 'Added', user, path, iterations))
    print('The password itself was not written anywhere — record it in a '
          'password manager before you close this terminal.')
    print('\nNow run:  python3 page-builder/tools/build-chrome.py')


if __name__ == '__main__':
    main()
