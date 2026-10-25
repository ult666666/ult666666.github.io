/* The foundations review route stays usable by keyboard, without enhancement and on narrow screens. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const ROUTE = '/projects/foundations.html';
const REPOS = ['quantkit', 'powerlift', 'ledgerline', 'saas-analytics-warehouse', 'searchlite', 'contrastkit',
  'citecheck'];
const LIVE = ['https://ult666666.github.io/saas-analytics-warehouse/', 'https://ult666666.github.io/searchlite/',
  'https://ult666666.github.io/contrastkit/'];

module.exports = async function foundationsShowcase(browser, base) {
  for (const javaScriptEnabled of [true, false]) {
    const context = await browser.newContext({javaScriptEnabled, reducedMotion:'reduce'});
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    try {
      const response = await page.goto(base + ROUTE);
      assert.equal(response.status(), 200, 'Foundations page must be published');
      for (const name of REPOS) {
        assert.equal(await page.getByRole('heading', {name, exact:true}).count(), 1, `${name} has one heading`);
        assert(await page.locator(`a[href="https://github.com/ult666666/${name}/blob/main/docs/DESIGN.md"]`).count() >= 1,
          `${name} links its design notes`);
      }
      for (const url of LIVE) assert.equal(await page.locator(`a[href="${url}"]`).count(), 1, `Live link ${url}`);
      assert.equal(await page.getByText('Independent portfolio projects · Synthetic and fictional data', {exact:true}).count(), 1);
      const entry = page.locator('.lab-index a').first();
      assert.equal(await page.locator('.lab-index a').count(), REPOS.length, 'The index reaches every project');
      // Reach the index through actual keyboard navigation, then follow it.
      for (let attempt = 0; attempt < 30; attempt++) {
        await page.keyboard.press('Tab');
        if (await entry.evaluate(node => node === document.activeElement)) break;
      }
      assert(await entry.evaluate(node => node === document.activeElement), 'Tab reaches the project index');
      assert(await entry.evaluate(node => {
        const style = getComputedStyle(node);
        return style.outlineStyle !== 'none' && parseFloat(style.outlineWidth) >= 2;
      }), 'The project index has a visible keyboard focus ring');
      await page.keyboard.press('Enter');
      assert.equal(new URL(page.url()).hash, '#section-1');
      const walkthroughs = page.locator('details.lab-walkthrough');
      assert.equal(await walkthroughs.count(), REPOS.length, 'Each project needs a runnable review route');
      for (const walkthrough of await walkthroughs.all()) {
        const summary = walkthrough.locator('summary');
        assert.equal(await walkthrough.getAttribute('open'), null);
        await summary.focus();
        await page.keyboard.press('Enter');
        assert.notEqual(await walkthrough.getAttribute('open'), null, 'Keyboard opens native walkthrough');
        assert(await walkthrough.locator('pre code').isVisible(), 'Runnable command stays readable without JavaScript');
        assert(await walkthrough.locator('a[href*="/test"]').count() >= 1, 'Walkthrough links to the proving test');
        await page.keyboard.press('Space');
        assert.equal(await walkthrough.getAttribute('open'), null, 'Space closes the native walkthrough');
      }
      for (const width of [320, 360, 768, 1440]) {
        await page.setViewportSize({width, height:1000});
        // Load at each viewport so a previous width's scroll extent cannot leak into the measurement.
        await page.goto(base + ROUTE);
        for (const summary of await page.locator('details.lab-walkthrough > summary').all()) await summary.click();
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `Foundations overflow at ${width}`);
        assert.equal(await page.locator('.lab-walkthrough pre,.lab-index a,.lab-definitions,.lab-copy h2').evaluateAll(nodes =>
          nodes.some(node => node.scrollWidth > node.clientWidth + 1)), false, `Commands, names and evidence fit at ${width}`);
      }
      await page.setViewportSize({width:1440, height:1000});
      await page.goto(base + ROUTE);
      await page.evaluate(() => document.documentElement.style.zoom = '2');
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'Foundations page fits at 200% zoom');
      await page.evaluate(() => document.documentElement.style.zoom = '');
      if (javaScriptEnabled) {
        const out = path.resolve(__dirname, '..', 'test-results');
        fs.mkdirSync(out, {recursive:true});
        await page.screenshot({path:path.join(out, 'foundations-desktop.png'), fullPage:true});
        await page.setViewportSize({width:320, height:844});
        await page.goto(base + ROUTE);
        const capture = await page.screenshot({path:path.join(out, 'foundations-mobile.png'), fullPage:true});
        assert.equal(capture.readUInt32BE(16), 320, 'Mobile evidence must use the requested viewport');
      }
      assert.deepEqual(errors, []);
    } finally { await context.close(); }
  }
  const page = await browser.newPage();
  try {
    await page.goto(base);
    await page.getByRole('link', {name:'Foundations', exact:true}).click();
    assert.equal(new URL(page.url()).pathname, ROUTE);
  } finally { await page.close(); }
  console.log('FOUNDATIONS_SHOWCASE_PASS: seven native keyboard walkthroughs, source/design/live links, 320/360/768/1440 widths, 200% zoom, focus and no-JavaScript access');
};
