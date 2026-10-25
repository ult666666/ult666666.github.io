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
  form.addEventListener('submit', event => event.preventDefault());
  query.addEventListener('input', filter);
  area.addEventListener('change', filter);
  form.addEventListener('reset', event => {
    event.preventDefault();
    query.value = '';
    area.value = 'all';
    filter();
    query.focus();
  });
  form.hidden = false;
  filter();
})();
