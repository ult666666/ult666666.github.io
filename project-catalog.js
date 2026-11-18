/* Progressive enhancement: content and links are already present in the document. */
(() => {
  const form = document.querySelector('.catalog-controls');
  if (!form) return;
  const query = document.getElementById('catalog-query');
  const area = document.getElementById('catalog-area');
  const count = document.getElementById('catalog-count');
  const empty = document.getElementById('catalog-empty');
  const projects = [...document.querySelectorAll('.catalog-card')].map(card => ({
    card,
    text: card.textContent.toLocaleLowerCase('en'),
    areas: card.dataset.areas.split(' ')
  }));
  function filter() {
    const terms = query.value.toLocaleLowerCase('en').trim().split(/\s+/).filter(Boolean);
    let shown = 0;
    for (const project of projects) {
      const matches = (area.value === 'all' || project.areas.includes(area.value))
        && terms.every(term => project.text.includes(term));
      project.card.hidden = !matches;
      if (matches) shown += 1;
    }
    count.textContent = `${shown} of ${projects.length} projects`;
    empty.hidden = shown !== 0;
  }
  function restoreFromUrl() {
    const params = new URLSearchParams(location.search);
    query.value = params.get('q') || '';
    area.value = params.get('area') || 'all';
    if (!area.value) area.value = 'all';
    filter();
  }
  function saveFilters() {
    const url = new URL(location.href);
    const search = query.value.trim();
    if (search) url.searchParams.set('q', search);
    else url.searchParams.delete('q');
    if (area.value !== 'all') url.searchParams.set('area', area.value);
    else url.searchParams.delete('area');
    if (url.href === location.href) return;
    try {
      history.replaceState(history.state, '', url);
    } catch (error) {
      // Some browsers limit how often a document can update its history.
      // Filtering still works, and the change event retries the final value.
      if (error.name !== 'SecurityError') throw error;
    }
  }

  form.addEventListener('submit', event => {
    event.preventDefault();
    saveFilters();
  });
  query.addEventListener('input', () => {
    filter();
    saveFilters();
  });
  query.addEventListener('change', saveFilters);
  area.addEventListener('change', () => {
    filter();
    saveFilters();
  });
  form.addEventListener('reset', event => {
    event.preventDefault();
    query.value = '';
    area.value = 'all';
    filter();
    saveFilters();
    query.focus();
  });
  window.addEventListener('pageshow', restoreFromUrl);
  window.addEventListener('popstate', restoreFromUrl);
  form.hidden = false;
  restoreFromUrl();
})();
