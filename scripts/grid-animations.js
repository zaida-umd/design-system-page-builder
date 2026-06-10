/* ============================================================
   GRID ENTRY ANIMATIONS — canonical shared script
   Staggered fade-in-from-bottom for grid children on scroll.

   Usage (from a project repo's pages/):
     <script src="../page-builder/scripts/grid-animations.js"></script>
   Usage (from examples/ or test/ inside this repo):
     <script src="../scripts/grid-animations.js"></script>

   Behavior:
   - Cumulative stagger: each child in a grid fades in 100ms after
     the previous one; row-mates (same offsetTop) land together.
   - Opt out per grid with data-animation="off" on the container.
   - Injects its own initial-state CSS and keyframes, so it works
     even on pages that don't link animation.min.css. The names
     match the upstream bundle (fade-in-from-bottom,
     .umd-animation-transition-fade-bottom) so the two never fight.
   - Bails out under prefers-reduced-motion: reduce, and explicitly
     reveals children in case animation.min.css set them opacity: 0
     (the upstream .umd-animation-grid rule is not motion-guarded).

   Do NOT copy this inline into pages — reference it by src so all
   pages share one implementation.
   ============================================================ */
(function () {
  var GRID_SELECTORS = [
    '.umd-layout-grid-gap-two',
    '.umd-layout-grid-gap-three',
    '.umd-layout-grid-gap-stacked',
    '.umd-layout-grid-columns-four',
    '.umd-layout-grid-masonry',
    '.umd-layout-grid-inline-tablet-rows',
    '.umd-animation-grid',
    '.umd-grid-animation'
  ].map(function (sel) { return sel + ':not([data-animation="off"])'; });

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    /* animation.min.css sets .umd-animation-grid > * { opacity: 0 }
       without a motion guard — make sure nothing stays hidden. */
    var reveal = document.createElement('style');
    reveal.textContent =
      ':where(' + GRID_SELECTORS.join(',') + ') > * {' +
      ' opacity: 1; transform: none; animation: none; }';
    document.head.appendChild(reveal);
    return;
  }

  var style = document.createElement('style');
  style.textContent = [
    '@keyframes fade-in-from-bottom {',
    '  from { opacity: 0; transform: translateY(50px); }',
    '  to   { opacity: 1; transform: translateY(0); }',
    '}',
    ':where(' + GRID_SELECTORS.join(',') + ') > * {',
    '  opacity: 0;',
    '  transform: translateY(50px);',
    '}',
    '.umd-animation-transition-fade-bottom {',
    '  animation: fade-in-from-bottom 1s forwards;',
    '}'
  ].join('\n');
  document.head.appendChild(style);

  function tagRowOffsets(grid) {
    var children = Array.prototype.slice.call(grid.children);
    var prevTop = null;
    children.forEach(function (child) {
      var top = child.getBoundingClientRect().top;
      if (prevTop !== null && Math.abs(top - prevTop) < 1) {
        child.dataset.animation = 'offset';
      } else {
        delete child.dataset.animation;
      }
      prevTop = top;
    });
  }

  function init() {
    var grids = document.querySelectorAll(GRID_SELECTORS.join(','));
    if (!grids.length) return;

    grids.forEach(tagRowOffsets);
    window.addEventListener('resize', function () {
      grids.forEach(tagRowOffsets);
    });

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var children = Array.prototype.slice.call(entry.target.children);
        var delay = 0;
        children.forEach(function (child) {
          if (child.dataset.animation === 'offset') {
            child.style.animationDelay = (delay - 0.15) + 's';
          } else {
            child.style.animationDelay = delay + 's';
            delay += 0.1;
          }
          child.classList.add('umd-animation-transition-fade-bottom');
        });
        observer.unobserve(entry.target);
      });
    }, { threshold: 0.1 });

    grids.forEach(function (grid) { observer.observe(grid); });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
