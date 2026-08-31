/* ============================================================================
   Prototype access gate — client-side sign-in for a GitHub Pages preview site.

   WHAT THIS IS FOR
     A prototype published to GitHub Pages is served from a public URL. This
     keeps it blank for anyone who arrives without the shared credentials, and
     — with the noindex meta that tools/chrome.py stamps into every page — off
     search engines. It is the barrier for casual visitors and crawlers on a
     client-review prototype.

   WHAT THIS IS NOT
     It is not access control. Everything needed to check the password ships
     to the browser, so the page markup is retrievable with `curl` by anyone
     who knows the URL, and the stored hash can be attacked offline. Never put
     anything behind it that would actually matter if it leaked — real student
     data, unreleased announcements, anything under FERPA. If content needs
     genuine protection it belongs behind server-side auth, not here.

     Because the markup ships in the clear either way, the project repo itself
     should be private. A public repo publishes the same pages a second time,
     where no gate applies at all.

   HOW IT LOCKS
     shared/gate.html locks the page in CSS, with no JavaScript involved:

         html:not(.umd-gate-unlocked) body { visibility: hidden }

     So the content is hidden from the first paint, before this file has even
     been fetched, and it stays hidden if this file 404s, throws, or the reader
     has JavaScript off. The only thing that reveals a page is this script
     verifying a password. Fail-closed is the whole design — do not "improve"
     it by moving the lock into JS.

   HOW IT VERIFIES
     PBKDF2-HMAC-SHA256 over the typed password with the account's salt, at
     GATE.iterations rounds, compared against the stored hash. The plaintext
     password appears nowhere in this repo or the published site. Generate an
     account with:

         python3 page-builder/tools/gate.py --write shared/gate.html

     crypto.subtle needs a secure context — https:// or localhost. A page
     opened over file:// cannot verify and says so rather than unlocking.

   HOW THE SESSION PERSISTS
     On success the derived key is kept under a storage key fingerprinted from
     the current account list, so every page on the site unlocks without
     retyping and changing the password invalidates every outstanding session.
     GATE.rememberHours sets the window; 0 confines it to the one tab.
   ========================================================================= */
(function () {
  'use strict';

  var GATE = window.UMD_GATE;
  if (!GATE || !GATE.users || !GATE.users.length) {
    return fail('This prototype gate is not configured.',
      'shared/gate.html has no accounts. Run page-builder/tools/gate.py.');
  }

  var ITERATIONS = GATE.iterations || 310000;
  var REMEMBER_MS = (GATE.rememberHours == null ? 12 : GATE.rememberHours) * 3600e3;
  var UNLOCKED = 'umd-gate-unlocked';

  /* Fingerprint of the account list, so a password change logs everyone out.
     Not a security boundary — just a cache key — so a plain string hash is
     the right tool and WebCrypto would be theatre. */
  var STORE_KEY = 'umd-gate:' + djb2(GATE.users.map(function (u) {
    return u.user + ':' + u.salt + ':' + u.hash;
  }).join('|'));

  /* rememberHours: 0 means "this tab only", which is exactly sessionStorage.
     Both are wrapped because Safari's private mode throws on write, and a
     storage failure must degrade to "ask every page", never to "stay open". */
  var store = REMEMBER_MS > 0 ? safeStorage('localStorage') : safeStorage('sessionStorage');

  sweep();
  if (isRemembered()) return unlock();
  ready(prompt);

  /* ---------------------------------------------------------------- crypto */

  function derive(password, saltHex) {
    var subtle = window.crypto && window.crypto.subtle;
    if (!subtle) {
      return Promise.reject(new Error(
        'This browser cannot verify the password here. Open the prototype ' +
        'over https:// (or http://localhost) rather than as a local file.'));
    }
    return subtle.importKey('raw', utf8(password), 'PBKDF2', false, ['deriveBits'])
      .then(function (key) {
        return subtle.deriveBits({
          name: 'PBKDF2',
          salt: unhex(saltHex),
          iterations: ITERATIONS,
          hash: 'SHA-256'
        }, key, 256);
      })
      .then(hex);
  }

  /* Resolves to the derived key on success, null on a bad username OR a bad
     password. The two are deliberately not distinguished in the message. */
  function verify(username, password) {
    var name = String(username).trim().toLowerCase();
    var account = null;
    for (var i = 0; i < GATE.users.length; i++) {
      if (GATE.users[i].user.trim().toLowerCase() === name) account = GATE.users[i];
    }
    /* Derive against a decoy salt for an unknown username so a wrong name and
       a wrong password take the same time to come back. */
    var salt = account ? account.salt : GATE.users[0].salt;
    return derive(password, salt).then(function (got) {
      return account && got === account.hash ? got : null;
    });
  }

  /* ---------------------------------------------------------------- session */

  function isRemembered() {
    var raw = store.get(STORE_KEY);
    if (!raw) return false;
    var saved;
    try { saved = JSON.parse(raw); } catch (e) { store.remove(STORE_KEY); return false; }
    if (saved.expires && Date.now() > saved.expires) { store.remove(STORE_KEY); return false; }
    for (var i = 0; i < GATE.users.length; i++) {
      if (saved.key === GATE.users[i].hash) return true;
    }
    store.remove(STORE_KEY);   // stale — the accounts changed under it
    return false;
  }

  function remember(key) {
    store.set(STORE_KEY, JSON.stringify({
      key: key,
      expires: REMEMBER_MS > 0 ? Date.now() + REMEMBER_MS : 0
    }));
  }

  /* Drop derived keys from superseded account lists. Rotating a password
     changes STORE_KEY, so the previous entry is orphaned rather than
     overwritten — it can no longer unlock anything, but it is the PBKDF2
     output of the old password and should not sit in storage forever. */
  function sweep() {
    [safeStorage('localStorage'), safeStorage('sessionStorage')].forEach(function (s) {
      s.keys().forEach(function (k) {
        if (k.indexOf('umd-gate:') === 0 && k !== STORE_KEY) s.remove(k);
      });
    });
  }

  function safeStorage(which) {
    var s = null;
    try { s = window[which]; s.setItem('__gate', '1'); s.removeItem('__gate'); }
    catch (e) { s = null; }
    return {
      get: function (k) { try { return s && s.getItem(k); } catch (e) { return null; } },
      set: function (k, v) { try { s && s.setItem(k, v); } catch (e) {} },
      remove: function (k) { try { s && s.removeItem(k); } catch (e) {} },
      keys: function () {
        try { return s ? Object.keys(s) : []; } catch (e) { return []; }
      }
    };
  }

  /* ------------------------------------------------------------------- UI */

  function prompt() {
    var el = document.createElement('div');
    el.className = 'umd-gate';
    el.setAttribute('role', 'dialog');
    el.setAttribute('aria-modal', 'true');
    el.setAttribute('aria-labelledby', 'umd-gate-title');

    el.innerHTML =
      '<form class="umd-gate__panel" novalidate>' +
        '<p class="umd-gate__eyebrow">Prototype preview</p>' +
        '<h1 class="umd-gate__title" id="umd-gate-title"></h1>' +
        '<p class="umd-gate__message"></p>' +
        '<label class="umd-gate__label" for="umd-gate-user">Username</label>' +
        '<input class="umd-gate__input" id="umd-gate-user" name="username" type="text" ' +
          'autocomplete="username" autocapitalize="off" autocorrect="off" spellcheck="false" required>' +
        '<label class="umd-gate__label" for="umd-gate-pass">Password</label>' +
        '<input class="umd-gate__input" id="umd-gate-pass" name="password" type="password" ' +
          'autocomplete="current-password" required>' +
        '<p class="umd-gate__error" role="alert" aria-live="assertive"></p>' +
        '<button class="umd-gate__submit" type="submit">View prototype</button>' +
        '<p class="umd-gate__note"></p>' +
      '</form>';

    var title = el.querySelector('.umd-gate__title');
    var message = el.querySelector('.umd-gate__message');
    var note = el.querySelector('.umd-gate__note');
    var error = el.querySelector('.umd-gate__error');
    var submit = el.querySelector('.umd-gate__submit');
    var form = el.querySelector('form');
    var user = el.querySelector('#umd-gate-user');

    title.textContent = GATE.title || 'This prototype is private';
    message.textContent = GATE.message ||
      'Sign in with the credentials shared with you to view this preview.';
    note.textContent = GATE.note || '';
    if (!note.textContent) note.hidden = true;

    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      if (submit.disabled) return;

      var username = form.username.value;
      var password = form.password.value;
      if (!username || !password) {
        return show(error, 'Enter both a username and a password.');
      }

      submit.disabled = true;
      submit.textContent = 'Checking…';
      error.textContent = '';

      verify(username, password).then(function (key) {
        if (!key) {
          submit.disabled = false;
          submit.textContent = 'View prototype';
          form.password.value = '';
          form.password.focus();
          return show(error, 'That username and password did not match.');
        }
        remember(key);
        el.remove();
        unlock();
      }).catch(function (err) {
        submit.disabled = false;
        submit.textContent = 'View prototype';
        show(error, err.message || 'Could not check that password.');
      });
    });

    el.addEventListener('keydown', function (ev) {
      /* Submit on Enter explicitly. A form's implicit submission is easy to
         lose — it depends on the button staying inside the form and on no
         ancestor swallowing the key — and a sign-in box that ignores Enter
         reads as broken. requestSubmit fires the submit handler, which
         disables the button on entry, so this cannot double-submit. */
      if (ev.key === 'Enter' && ev.target.tagName === 'INPUT') {
        ev.preventDefault();
        return form.requestSubmit ? form.requestSubmit() : submit.click();
      }

      /* Tab must not escape into the hidden page behind the dialog. */
      if (ev.key !== 'Tab') return;
      var focusable = el.querySelectorAll('input, button');
      var first = focusable[0];
      var last = focusable[focusable.length - 1];
      if (ev.shiftKey && document.activeElement === first) {
        ev.preventDefault(); last.focus();
      } else if (!ev.shiftKey && document.activeElement === last) {
        ev.preventDefault(); first.focus();
      }
    });

    document.body.appendChild(el);
    user.focus();
  }

  function show(node, text) {
    node.textContent = text;
  }

  function unlock() {
    document.documentElement.classList.add(UNLOCKED);
    document.dispatchEvent(new CustomEvent('umd-gate:unlocked'));
  }

  /* A configuration problem must not unlock the page — it reports itself in
     the space the dialog would have used and leaves the content hidden. */
  function fail(title, detail) {
    ready(function () {
      var el = document.createElement('div');
      el.className = 'umd-gate';
      el.innerHTML = '<div class="umd-gate__panel">' +
        '<p class="umd-gate__eyebrow">Prototype preview</p>' +
        '<h1 class="umd-gate__title"></h1><p class="umd-gate__message"></p></div>';
      el.querySelector('.umd-gate__title').textContent = title;
      el.querySelector('.umd-gate__message').textContent = detail;
      document.body.appendChild(el);
    });
  }

  /* ---------------------------------------------------------------- helpers */

  function ready(fn) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn);
    } else {
      fn();
    }
  }

  function utf8(s) { return new TextEncoder().encode(s); }

  function unhex(s) {
    var out = new Uint8Array(s.length / 2);
    for (var i = 0; i < out.length; i++) out[i] = parseInt(s.substr(i * 2, 2), 16);
    return out;
  }

  function hex(buf) {
    var bytes = new Uint8Array(buf), out = '';
    for (var i = 0; i < bytes.length; i++) out += ('0' + bytes[i].toString(16)).slice(-2);
    return out;
  }

  function djb2(s) {
    var h = 5381;
    for (var i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) | 0;
    return (h >>> 0).toString(36);
  }
}());
