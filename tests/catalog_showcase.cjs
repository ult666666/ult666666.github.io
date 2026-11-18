/* Search and area filters compose over real static HTML; no JS retains every route. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

module.exports = async (browser, base) => {
  const page = await browser.newPage({viewport:{width:1440,height:1000}, reducedMotion:'reduce'});
  const errors = [], external = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.route('**/*', route => {
    if (new URL(route.request().url()).origin === base) return route.continue();
    external.push(route.request().url()); return route.abort();
  });
  await page.goto(base + '/projects/catalog.html');
  await page.locator('#catalog-query').waitFor({state:'visible',timeout:4000});
  assert.equal(await page.locator('.catalog-card:visible').count(),20);
  const out = path.resolve(__dirname,'..','test-results'); fs.mkdirSync(out,{recursive:true});
  await page.screenshot({path:path.join(out,'catalog-desktop.png')});
  await page.getByLabel('Focus area').selectOption('backend');
  await page.getByLabel('Search projects').fill('  PYTHON   sqlite  ');
  assert.deepEqual(await page.locator('.catalog-card:visible').evaluateAll(nodes=>nodes.map(n=>n.id).sort()),
                   ['citecheck','impact-ledger','ledgerline','relaybox']);
  assert.equal(await page.locator('#catalog-count').innerText(),'4 of 20 projects');
  const filteredUrl = new URL(page.url());
  assert.equal(filteredUrl.searchParams.get('area'), 'backend');
  assert.equal(filteredUrl.searchParams.get('q'), 'PYTHON   sqlite');
  await page.reload();
  assert.equal(await page.getByLabel('Focus area').inputValue(), 'backend');
  assert.equal(await page.getByLabel('Search projects').inputValue(), 'PYTHON   sqlite');
  assert.equal(await page.locator('#catalog-count').innerText(), '4 of 20 projects');
  await page.getByLabel('Search projects').fill('CUPED');
  assert.equal(await page.locator('.catalog-card:visible').count(),0);
  assert.equal(await page.locator('#catalog-empty').isVisible(),true);
  await page.getByLabel('Focus area').selectOption('data');
  assert.equal(await page.locator('.catalog-card:visible').getAttribute('id'),'powerlift');
  await page.getByRole('button',{name:'Clear filters'}).click();
  assert.equal(await page.getByLabel('Search projects').inputValue(),'');
  assert.equal(await page.getByLabel('Focus area').inputValue(),'all');
  assert.equal(new URL(page.url()).search, '');
  assert.equal(await page.locator('.catalog-card:visible').count(),20);
  assert.equal(await page.locator('#catalog-empty').isVisible(),false);
  await page.getByLabel('Search projects').focus();
  await page.keyboard.press('Tab');
  assert.equal(await page.locator('#catalog-area').evaluate(n=>n===document.activeElement),true);
  await page.setViewportSize({width:320,height:800});
  await page.getByLabel('Search projects').fill('relaybox');
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth <= innerWidth),true, JSON.stringify(await page.evaluate(()=>[...document.querySelectorAll('*')].filter(n=>n.getBoundingClientRect().right>innerWidth).map(n=>({tag:n.tagName,class:n.className,right:n.getBoundingClientRect().right})))));
  await page.screenshot({path:path.join(out,'catalog-mobile.png'),fullPage:true});
  await page.goto(base + '/projects/catalog.html?area=unknown&q=C%2B%2B&from=profile#top');
  assert.equal(await page.getByLabel('Focus area').inputValue(), 'all');
  assert.equal(await page.getByLabel('Search projects').inputValue(), 'C++');
  await page.getByRole('button', {name:'Clear filters'}).click();
  assert.equal(new URL(page.url()).search, '?from=profile');
  assert.equal(new URL(page.url()).hash, '#top');
  assert.deepEqual(errors,[]); assert.deepEqual(external,[]);
  await page.close();
  const context = await browser.newContext({javaScriptEnabled:false,viewport:{width:320,height:800}});
  const plain = await context.newPage();
  await plain.goto(base + '/projects/catalog.html?area=finance&q=ledger');
  assert.equal(await plain.locator('.catalog-card:visible').count(),20);
  assert.equal(await plain.getByRole('search').isVisible(),false);
  assert.equal(await plain.locator('#relaybox').getByRole('link',{name:'Source',exact:true}).getAttribute('href'),
               'https://github.com/ult666666/relaybox');
  assert.equal(await plain.evaluate(()=>document.documentElement.scrollWidth <= innerWidth),true);
  await context.close();
  console.log('Project catalog: composed filters, reset, keyboard, 320px and no-JS checks passed');
};
