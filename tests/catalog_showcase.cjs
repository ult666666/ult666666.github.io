/* Search and area filters compose over real static HTML; no JS retains every route. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {assertProjectLinkNames, contrastRatio} = require('./accessibility_assertions.cjs');
const projectCount = require('../docs/project-catalog.json').projects.length;

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
  assert.equal(await page.locator('.catalog-card:visible').count(),projectCount);
  for (const field of await page.locator('.catalog-controls input, .catalog-controls select').all()) {
    const colors = await field.evaluate(el => ({
      border: getComputedStyle(el).borderTopColor,
      inside: getComputedStyle(el).backgroundColor,
      outside: getComputedStyle(document.body).backgroundColor
    }));
    for (const surface of [colors.inside, colors.outside]) {
      assert(contrastRatio(colors.border, surface) >= 3, `Search field border ${colors.border} on ${surface}`);
    }
  }
  const out = path.resolve(__dirname,'..','test-results'); fs.mkdirSync(out,{recursive:true});
  await page.screenshot({path:path.join(out,'catalog-desktop.png')});
  await page.getByLabel('Focus area').selectOption('backend');
  await page.getByLabel('Search projects').fill('  PYTHON   sqlite  ');
  assert.deepEqual(await page.locator('.catalog-card:visible').evaluateAll(nodes=>nodes.map(n=>n.id).sort()),
                   ['citecheck','impact-ledger','ledgerline','relaybox']);
  assert.equal(await page.locator('#catalog-count').innerText(),`4 of ${projectCount} projects`);
  const filteredUrl = new URL(page.url());
  assert.equal(filteredUrl.searchParams.get('area'), 'backend');
  assert.equal(filteredUrl.searchParams.get('q'), 'PYTHON   sqlite');
  await page.reload();
  assert.equal(await page.getByLabel('Focus area').inputValue(), 'backend');
  assert.equal(await page.getByLabel('Search projects').inputValue(), 'PYTHON   sqlite');
  assert.equal(await page.locator('#catalog-count').innerText(), `4 of ${projectCount} projects`);
  await page.getByLabel('Search projects').fill('CUPED');
  assert.equal(await page.locator('.catalog-card:visible').count(),0);
  assert.equal(await page.locator('#catalog-empty').isVisible(),true);
  await page.getByLabel('Focus area').selectOption('data');
  assert.equal(await page.locator('.catalog-card:visible').getAttribute('id'),'powerlift');
  await page.getByRole('button',{name:'Clear filters'}).click();
  assert.equal(await page.getByLabel('Search projects').inputValue(),'');
  assert.equal(await page.getByLabel('Focus area').inputValue(),'all');
  assert.equal(new URL(page.url()).search, '');
  assert.equal(await page.locator('.catalog-card:visible').count(),projectCount);
  assert.equal(await page.locator('#catalog-empty').isVisible(),false);
  // A term in a folded walkthrough must still reach its project.
  await page.getByLabel('Search projects').fill('post office recorded');
  assert.equal(await page.locator('.catalog-card:visible').getAttribute('id'), 'snowfall-os');
  assert.equal(await page.getByRole('link', {name:'Explore the village (Snowfall OS)'}).isVisible(), true);
  await page.getByRole('button',{name:'Clear filters'}).click();
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
  assert.equal(await plain.locator('.catalog-card:visible').count(),projectCount);
  assert.equal(await plain.getByRole('search').isVisible(),false);
  const walkthrough = plain.locator('#snowfall-os details');
  const command = walkthrough.locator('pre');
  assert.equal(await walkthrough.getAttribute('open'), null);
  await walkthrough.locator('summary').focus();
  await plain.keyboard.press('Enter');
  assert.equal(await command.isVisible(), true, 'No-script keyboard walkthrough');
  assert.equal(await plain.evaluate(()=>document.documentElement.scrollWidth <= innerWidth), true);
  await plain.keyboard.press('Space');
  assert.equal(await command.isVisible(), false);
  await plain.emulateMedia({media:'print'});
  assert.equal(await command.evaluate(el=>el.checkVisibility({contentVisibilityAuto:true})), true, 'Print includes folded commands');
  await plain.emulateMedia({media:'screen'});
  await assertProjectLinkNames(plain.locator('.catalog-card'), 'h2', '.catalog-links a');
  assert.equal(await plain.getByRole('link',{name:'Source (RelayBox)',exact:true}).getAttribute('href'),
               'https://github.com/ult666666/relaybox');
  assert.equal(await plain.evaluate(()=>document.documentElement.scrollWidth <= innerWidth),true);
  await context.close();
  console.log('Project catalog: composed filters, reset, keyboard, 320px and no-JS checks passed');
};
