/* Reviewer routes remain usable without enhancement and on narrow screens. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

module.exports = async function engineeringShowcase(browser, base) {
  for (const javaScriptEnabled of [true, false]) {
    const context = await browser.newContext({javaScriptEnabled, reducedMotion:'reduce'});
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    try {
      const response = await page.goto(base + '/projects/engineering-lab.html');
      assert.equal(response.status(), 200, 'Engineering showcase must be published');
      for (const name of ['RelayBox', 'TraceBench', 'Impact Ledger']) {
        assert.equal(await page.getByRole('heading', {name, exact:true}).count(), 1);
      }
      for (const repo of ['relaybox', 'tracebench', 'impact-ledger']) {
        assert(await page.locator(`a[href="https://github.com/ult666666/${repo}"]`).count() >= 1);
        assert(await page.locator(`a[href="https://github.com/ult666666/${repo}/blob/main/docs/VERIFICATION.md"]`).count() >= 1);
      }
      assert.equal(await page.getByText('Independent portfolio projects · Synthetic data', {exact:true}).count(), 1);
      for (const width of [360, 768, 1440]) {
        await page.setViewportSize({width, height:1000});
        // Load at each viewport, including when script execution is disabled.
        // This avoids measuring a preceding viewport's transient scroll extent.
        await page.goto(base + '/projects/engineering-lab.html');
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `Showcase overflow at ${width}`);
      }
      await page.setViewportSize({width:1440, height:1000});
      const out = path.resolve(__dirname, '..', 'test-results');
      fs.mkdirSync(out, {recursive:true});
      if (javaScriptEnabled) {
        await page.screenshot({path:path.join(out, 'engineering-lab-desktop.png'),fullPage:true});
        await page.setViewportSize({width:390, height:844});
        await page.goto(base + '/projects/engineering-lab.html');
        const capture = await page.screenshot({path:path.join(out, 'engineering-lab-mobile.png'),fullPage:true});
        assert.equal(capture.readUInt32BE(16), 390, 'Mobile evidence must use the requested viewport');
      }
      assert.deepEqual(errors, []);
    } finally { await context.close(); }
  }
  const page = await browser.newPage();
  try {
    await page.goto(base);
    await page.getByRole('link', {name:'Explore the engineering lab ↗',exact:true}).click();
    assert.equal(new URL(page.url()).pathname, '/projects/engineering-lab.html');
  } finally { await page.close(); }
  console.log('ENGINEERING_SHOWCASE_PASS: three source/verification routes, homepage discovery, 3 widths and no-JavaScript access');
};
