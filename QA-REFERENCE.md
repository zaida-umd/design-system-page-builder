# Design system QA reference site

`qa-designteam.umd-servd.com` renders the design system's components as the
design team intends them. It is the **ground truth for how a component is
supposed to look and behave** — ahead of this repo's notes, which are a
translation and can go stale.

## When to use it

**Before recording any design-system behaviour as broken.** If a component
appears not to work, check the QA page for it first. In one session this step
would have prevented three wrong findings, two of which were committed as
guidance telling future pages to work around bugs that did not exist:

| Claimed bug | What the QA page showed |
|---|---|
| `.size-large` renders 424px in a 560px box | Renders 560px there — the cards are grid items, so `height:100%` resolves. A CSS rule, not a component bug. |
| `data-visual-size="large"` on quotes is unrendered | Renders 32px vs 22px natively. The claim was true at 1.18.12 and never rechecked after the bump. |
| The quotes page is broken, component never registers | It registers fine — the DOM had been read before the components upgraded. |

Also use it when a rule here disagrees with what a page is doing, when a
component's markup contract is unclear, or when picking between variants.

**Do not** treat a difference as a bug on its own. The QA site may run a
different version than the pin in `.gitmodules` — check its `cdn.js` version
before concluding anything about ours.

## Page map

One index at `/components` links everything, so finding a component costs a
single page visit rather than a crawl. Re-read the index if a component is not
in this list; the site gains pages.

| Component area | Path |
|---|---|
| Index of all component pages | `/components` |
| Accordion | `/components/accordion` |
| Banner promo | `/components/banner-promo` |
| Cards — all | `/components/cards-index` |
| Cards — standard | `/components/cards-index/standard-cards` |
| Cards — overlay | `/components/cards-index/overlay-cards` |
| Cards — icon | `/components/cards-index/icon-cards` |
| Carousels | `/components/carousels` |
| Events | `/components/events` |
| Images and media | `/components/images-and-media` |
| Lists | `/components/lists-and-lists` |
| Pathways | `/components/pathways` |
| Person / bio | `/components/person-bio` |
| Section intros | `/components/section-intros` |
| Statistics | `/components/statistics` |
| Text and quotes | `/components/text-quotes` |

## How to read a page

Use the **Claude in Chrome** tools, not the in-app browser — the site sits
behind the user's browser session and Chrome already carries it.

**Wait for the components to upgrade before measuring anything.** Reading too
early reports `customElements.get(...) === false` and no shadow roots, which
looks exactly like a broken page. Confirm `defined: true` first, then measure.

Measure inside the shadow root, not the light DOM. Several components clone
their slotted content rather than slotting it, so a light-DOM element can read
0px high while the rendered clone is correct.

```js
// Find every instance wherever it lives, including inside other shadow roots
const found = [];
const walk = (root, path) => root.querySelectorAll('*').forEach(el => {
  if (el.tagName.toLowerCase() === 'umd-element-quote') found.push({ path, el });
  if (el.shadowRoot) walk(el.shadowRoot, path + '>' + el.tagName.toLowerCase());
});
walk(document, 'document');
```

Check whether the page carries its own workaround before concluding the
component does something natively:

```js
[...document.querySelectorAll('script:not([src])')]
  .some(s => /shadowRoot/.test(s.textContent))   // true = the page is polyfilling
```

## Access

The site is behind browser auth. It works from Claude in Chrome because the
user's Chrome session already holds it — **Claude cannot authenticate itself**.
If a page returns a login wall instead of content, say so and ask the user to
sign in; do not try to work around it.

## The local equivalent

For attribute contracts specifically, the submodule is faster and needs no
browser: `design-system/packages/model/source/attributes/checks.ts` defines
exactly what every attribute check accepts, deprecated spellings included. It
settled three wrong guesses in one session. Reach for it first when the question
is "does this attribute do anything", and for the QA site when the question is
"what should this look like".
