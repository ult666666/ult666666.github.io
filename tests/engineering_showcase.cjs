/* Reviewer routes remain usable without enhancement and on narrow screens. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

function contrastOnWhite(color) {
  const channels = color.match(/[\d.]+/g).slice(0, 3).map(value => Number(value) / 255);
  const linear = channels.map(value => value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4);
  return 1.05 / (0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2] + 0.05);
}

async function captureHandoff(page, handoff, destination) {
  // A document clip keeps the actual sticky header at the top of the page,
  // outside this lower section, rather than compositing it across the evidence.
  await page.evaluate(() => window.scrollTo({top:0, behavior:'instant'}));
  await page.screenshot({path:destination,fullPage:true,clip:await handoff.boundingBox()});
}

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
      const handoff = page.locator('#operations-handoff');
      const entry = page.locator('.lab-intro a[href="#operations-handoff"]');
      assert.equal(await entry.count(), 1, 'The installed handoff must be discoverable near the lab intro');
      // Reach the new route through actual keyboard navigation, then follow it.
      for (let attempt = 0; attempt < 30; attempt++) {
        await page.keyboard.press('Tab');
        if (await entry.evaluate(node => node === document.activeElement)) break;
      }
      assert(await entry.evaluate(node => node === document.activeElement), 'Tab reaches the handoff link');
      assert(await entry.evaluate(node => {
        const style = getComputedStyle(node);
        return style.outlineStyle !== 'none' && parseFloat(style.outlineWidth) >= 2;
      }), 'The handoff route has a visible keyboard focus ring');
      await page.keyboard.press('Enter');
      assert.equal(new URL(page.url()).hash, '#operations-handoff');
      assert(await handoff.isVisible(), 'Handoff works with enhancement disabled');
      const table = handoff.getByRole('table', {name:'Learning Lab / 学习计划 · equal 31-day periods'});
      assert.equal(await table.count(), 1, 'Comparison has an accessible caption');
      assert.deepEqual(await table.getByRole('columnheader').allTextContents(), [
        'Measure', 'Current: October 1–31, 2026', 'Prior: August 31–September 30, 2026']);
      const expectedRows = [
        ['Distinct people', '3', '2'], ['Attendance', '4', '3'],
        ['Participant-hours', '7', '3.25'], ['Session-hours', '3.5', '2'],
        ['Actual spend (USD)', '130.25', '131.00']];
      assert.deepEqual(await table.locator('tbody tr').evaluateAll(rows => rows.map(row =>
        [...row.cells].map(cell => cell.textContent.trim()))), expectedRows);
      for (const node of await handoff.locator('li,caption,th,td,pre,a,.lab-contract-note').all()) {
        assert(await node.isVisible(), 'Handoff evidence is available without JavaScript');
      }
      const sourceLinks = handoff.locator('.lab-code-links a');
      await sourceLinks.first().focus();
      await page.keyboard.press('Tab');
      assert(await sourceLinks.nth(1).evaluate(node => node === document.activeElement &&
        getComputedStyle(node).outlineStyle !== 'none'), 'Evidence links retain visible Tab focus');
      const walkthroughs = page.locator('details.lab-walkthrough');
      assert.equal(await walkthroughs.count(), 3, 'Each project needs a runnable review route');
      for (const walkthrough of await walkthroughs.all()) {
        const summary = walkthrough.locator('summary');
        assert.equal(await walkthrough.getAttribute('open'), null);
        await summary.focus();
        await page.keyboard.press('Enter');
        assert.notEqual(await walkthrough.getAttribute('open'), null, 'Keyboard opens native walkthrough');
        assert(await walkthrough.locator('pre code').isVisible(), 'Runnable command stays readable without JavaScript');
        assert(await walkthrough.locator('a[href*="/tests/"]').count() >= 1, 'Walkthrough links to the proving test');
        await page.keyboard.press('Space');
        assert.equal(await walkthrough.getAttribute('open'), null, 'Space closes the native walkthrough');
      }
      for (const width of [320, 360, 768, 1440]) {
        await page.setViewportSize({width, height:1000});
        // Load at each viewport, including when script execution is disabled.
        // This avoids measuring a preceding viewport's transient scroll extent.
        await page.goto(base + '/projects/engineering-lab.html');
        for (const summary of await page.locator('details.lab-walkthrough > summary').all()) await summary.click();
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `Showcase overflow at ${width}`);
        assert.equal(await page.locator('.lab-walkthrough pre,#operations-handoff pre,#operations-handoff table').evaluateAll(nodes => nodes.some(node => node.scrollWidth > node.clientWidth + 1)), false, 'Commands and comparison wrap without clipping');
        assert(await table.isVisible());
        assert(await handoff.locator('pre').isVisible());
      }
      await page.setViewportSize({width:1440, height:1000});
      await page.goto(base + '/projects/engineering-lab.html');
      await page.evaluate(() => document.documentElement.style.zoom = '2');
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'Engineering page fits at 200% zoom');
      assert.equal(await handoff.locator('pre,table').evaluateAll(nodes => nodes.some(node => node.scrollWidth > node.clientWidth + 1)), false, 'Handoff command and table fit at 200% zoom');
      await page.evaluate(() => document.documentElement.style.zoom = '');
      await page.emulateMedia({media:'print'});
      for (const node of await handoff.locator('h2,li,caption,th,td,pre,a,.lab-contract-note').all()) {
        assert(await node.isVisible(), 'Print keeps the handoff explanation and source evidence');
      }
      const printColors = await handoff.locator('caption,th,td,p,li,a,code').evaluateAll(nodes =>
        nodes.map(node => getComputedStyle(node).color));
      for (const color of printColors) assert(contrastOnWhite(color) >= 4.5, `Print text must remain readable on white paper: ${color}`);
      await page.emulateMedia({media:'screen'});
      const out = path.resolve(__dirname, '..', 'test-results');
      fs.mkdirSync(out, {recursive:true});
      if (javaScriptEnabled) {
        await page.screenshot({path:path.join(out, 'engineering-lab-desktop.png'),fullPage:true});
        await captureHandoff(page, handoff, path.join(out, 'operations-handoff-desktop.png'));
        await page.setViewportSize({width:320, height:844});
        await page.goto(base + '/projects/engineering-lab.html');
        const capture = await page.screenshot({path:path.join(out, 'engineering-lab-mobile.png'),fullPage:true});
        assert.equal(capture.readUInt32BE(16), 320, 'Mobile evidence must use the requested viewport');
        await captureHandoff(page, handoff, path.join(out, 'operations-handoff-320.png'));
        await page.emulateMedia({media:'print'});
        await page.pdf({path:path.join(out, 'engineering-lab-print.pdf'),format:'A4',printBackground:true});
      }
      assert.deepEqual(errors, []);
    } finally { await context.close(); }
  }
  const page = await browser.newPage();
  try {
    await page.goto(base);
    await page.getByRole('link', {name:'Engineering lab',exact:true}).click();
    assert.equal(new URL(page.url()).pathname, '/projects/engineering-lab.html');
  } finally { await page.close(); }
  console.log('ENGINEERING_SHOWCASE_PASS: three native keyboard walkthroughs, fixed-evidence handoff, accessible comparison, 320/360/768/1440 widths, 200% zoom, focus, print and no-JavaScript access');
};
