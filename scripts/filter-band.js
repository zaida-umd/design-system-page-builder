/* ============================================================
   FILTER BAND — client-side category + text filtering for
   static listing pages. Pairs with the "Filter band" pattern in
   LAYOUT-PATTERNS.md (markup uses upstream element.min.css /
   layout.min.css classes: umd-layout-background-highlight-light,
   umd-text-line-trailing-light, umd-field-select-wrapper, …).

   Usage:
     <script src="../page-builder/scripts/filter-band.js"></script>

   Markup contract (data-attribute driven, no hard-coded ids):
     <form data-filter-band data-filter-items=".resource-item">
       <select data-filter-select>      — value "all" or a category
       <input  data-filter-search>      — free-text, matches textContent
       <button data-filter-clear type="reset">
     </form>
     <p data-filter-count aria-live="polite"></p>   — anywhere on page
     Each filterable item carries data-category="…".

   Multiple independent bands per page are supported; each form's
   data-filter-items selector scopes its own item set.
   ============================================================ */
(function () {
  function initBand(form) {
    var select   = form.querySelector('[data-filter-select]');
    var search   = form.querySelector('[data-filter-search]');
    var clearBtn = form.querySelector('[data-filter-clear]');
    var countEl  = document.querySelector('[data-filter-count]');
    var items    = document.querySelectorAll(form.dataset.filterItems || '[data-category]');
    var total    = items.length;

    function applyFilters() {
      var category = select ? select.value : 'all';
      var query    = search ? search.value.trim().toLowerCase() : '';
      var visible  = 0;

      items.forEach(function (item) {
        var matchCat    = (category === 'all' || item.dataset.category === category);
        var matchSearch = (!query || item.textContent.toLowerCase().indexOf(query) !== -1);

        if (matchCat && matchSearch) {
          item.removeAttribute('hidden');
          visible++;
        } else {
          item.setAttribute('hidden', '');
        }
      });

      if (countEl) {
        countEl.textContent = 'Displaying ' + visible + ' of ' + total + ' results';
      }
    }

    if (select) select.addEventListener('change', applyFilters);
    if (search) search.addEventListener('input', applyFilters);
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      applyFilters();
    });
    if (clearBtn) {
      clearBtn.addEventListener('click', function () {
        /* type="reset" clears the fields; re-run filters afterwards */
        setTimeout(applyFilters, 0);
      });
    }
  }

  function init() {
    document.querySelectorAll('form[data-filter-band]').forEach(initBand);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
