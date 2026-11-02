/* Verify the exact vendored game through the public catalog route. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
module.exports = async function verifyBlast(browser, base) {
  const context = await browser.newContext({viewport:{width:1280,height:1000},serviceWorkers:'block'});
  const blocked = [], errors = [];
  try {
    await context.route('**/*', async route => {
      const request = route.request();
      const url = new URL(request.url());
      if (url.origin !== new URL(base).origin || request.redirectedFrom()) {
        blocked.push(request.url()); return route.abort();
      }
      // fetch(maxRedirects:0) prevents an allowed response following an external redirect.
      const response = await route.fetch({maxRedirects:0,timeout:15000});
      if (response.status() >= 300 && response.status() < 400) {
        blocked.push(request.url()); return route.abort();
      }
      return route.fulfill({response});
    });
    await context.routeWebSocket('**/*', socket => {blocked.push(socket.url()); socket.close();});
    const page = await context.newPage();
    page.setDefaultTimeout(20000);
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(base + '/projects/catalog.html#blast-radius-daily');
    await page.locator('#blast-radius-daily').getByRole('link',{name:'Play offline demo',exact:true}).click();
    assert.equal(new URL(page.url()).pathname, '/projects/blast-radius-demo.html');
    const status = page.getByRole('status',{name:'Local game status'});
    await status.filter({hasText:'Map ready'}).waitFor();
    const click = async (x,y) => {
      await page.locator('canvas').scrollIntoViewIfNeeded();
      const b = await page.locator('canvas').boundingBox();
      assert(b, 'Real Phaser canvas missing');
      await page.mouse.click(b.x+x*b.width/1100,b.y+y*b.height/720);
    };
    // Identity's coordinates are part of the pinned July14 deterministic fixture.
    await click(270,190);
    await page.getByLabel('Local selected breakers').filter({hasText:'member_stitch'}).waitFor();
    await click(941,653);
    await status.filter({hasText:'Tracing'}).waitFor();
    await status.filter({hasText:'Result ready'}).waitFor();
    assert.equal(await page.getByLabel('Local score').innerText(), '1375');
    await click(884,493);
    await page.getByLabel('Local vote').filter({hasText:'Protect dashboards'}).waitFor();
    assert.equal(await page.getByLabel('Synthetic vote totals').innerText(), '8, 11, 5');
    await click(884,681);
    await status.filter({hasText:'Confirm deletion'}).waitFor();
    await click(884,681);
    await status.filter({hasText:'Local game data deleted'}).waitFor();
    assert.equal(await page.getByLabel('Local best score').innerText(),'None');
    assert.equal(await page.getByLabel('Local streak').innerText(),'0');
    const out=path.resolve(__dirname,'..','test-results');fs.mkdirSync(out,{recursive:true});
    await page.screenshot({path:path.join(out,'blast-game-deleted.png')});
    // Keyboard only, in a fresh tab: the same breaker reaches the same engine score without the mouse.
    const keys = await context.newPage();
    keys.setDefaultTimeout(20000);
    keys.on('pageerror', error => errors.push(error.message));
    await keys.goto(base + '/projects/blast-radius-demo.html');
    const keyStatus = keys.getByRole('status',{name:'Local game status'});
    await keyStatus.filter({hasText:'Map ready'}).waitFor();
    assert.equal(await keys.locator('#game-container').getAttribute('aria-hidden'),'true','The canvas is hidden from assistive technology');
    const focused = keys.locator('[role=option]:focus');
    for (let attempt = 0; attempt < 12 && await focused.count() === 0; attempt++) await keys.keyboard.press('Tab');
    assert.equal(await focused.getAttribute('data-node'),'source','Tab reaches the map at its first asset');
    await keys.keyboard.press('ArrowRight');
    await keys.keyboard.press('ArrowUp');
    assert.equal(await focused.getAttribute('data-node'),'identity','Arrow keys move between assets');
    await keys.keyboard.press('Space');
    assert.equal(await keys.locator('[role=option][data-node="identity"]').getAttribute('aria-selected'),'true');
    await keys.locator('#blast-announcer').filter({hasText:'1 of 2 tokens left'}).waitFor();
    await keys.keyboard.press('d');
    // The live region announces the cascade while it is traced, then replaces it with the incident report.
    await keys.locator('#blast-announcer').filter({hasText:'Cascade complete'}).waitFor();
    await keyStatus.filter({hasText:'Result ready'}).waitFor();
    await keys.locator('#blast-announcer').filter({hasText:'1,375 points.'}).waitFor();
    assert.equal(await keys.getByLabel('Local score').innerText(),'1375','Keyboard play reaches the pointer journey score');
    assert(await keys.locator('#blast-a11y-title').evaluate(node => node === document.activeElement),'Focus moves to the result heading');
    await keys.screenshot({path:path.join(out,'blast-game-keyboard-result.png')});
    assert.deepEqual(errors,[]);assert.deepEqual(blocked,[]);
    console.log('BLAST_SHOWCASE_PASS: catalog route, actual canvas selection/cascade/exact score, synthetic vote and two-step deletion, keyboard-only play to the same score, no external requests or page errors');
  } finally {await context.close();}
};
