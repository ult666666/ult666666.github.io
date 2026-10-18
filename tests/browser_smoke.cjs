/* Real Chromium checks for navigation, filters, accessibility basics and responsive layout. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const root = path.resolve(__dirname, '..');
const types = {'.html':'text/html','.css':'text/css','.js':'text/javascript','.png':'image/png','.jpg':'image/jpeg','.svg':'image/svg+xml'};
const server = http.createServer((req, res) => {
  const relative = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
  const file = path.resolve(root, '.' + (relative === '/' ? '/index.html' : relative));
  if (!file.startsWith(root + path.sep)) { res.writeHead(403); res.end(); return; }
  fs.readFile(file, (error, bytes) => {
    if (error) { res.writeHead(404); res.end(); return; }
    res.setHeader('Content-Type', types[path.extname(file)] || 'application/octet-stream');
    res.end(bytes);
  });
});
(async () => {
  let browser;
  try {
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    const base = `http://127.0.0.1:${server.address().port}`;
    browser = await chromium.launch({headless:true});
    const page = await browser.newPage({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(base, {waitUntil:'networkidle'});
    assert.equal(await page.locator('h1').count(), 1);
    assert.equal(await page.locator('.project-card:visible').count(), 8);
    for (const [filter, count] of [['fintech',1],['ai',3],['web',2],['experimental',2],['all',8]]) {
      await page.locator(`[data-filter="${filter}"]`).click();
      assert.equal(await page.locator('.project-card:visible').count(), count);
      assert.equal(await page.locator('#project-count').innerText(), String(count).padStart(2,'0'));
    }
    const out = path.join(root, 'test-results'); fs.mkdirSync(out,{recursive:true});
    await page.evaluate(()=>window.scrollTo(0,0));
    await page.waitForTimeout(100);
    await page.screenshot({path:path.join(out,'desktop.png'),fullPage:true});
    await page.locator('[data-filter="fintech"]').click();
    await page.locator('#frontier-ai-valuation-lab').screenshot({path:path.join(out,'fintech-desktop.png')});
    for (const name of ['lineageguard','motionx','trading-research','frontier-ai-valuation-lab']) {
      const response = await page.goto(base + '/projects/' + name + '.html');
      assert.equal(response.status(),200);
      assert.equal(await page.locator('h1').count(),1);
      assert.equal(await page.locator('.case-article section').count(),4);
    }
    for (const width of [390,768,1440]) {
      await page.setViewportSize({width,height:900}); await page.goto(base);
      const sizes=await page.evaluate(()=>[document.documentElement.scrollWidth,innerWidth]);
      assert(sizes[0] <= sizes[1]+1, `Horizontal overflow at ${width}: ${sizes}`);
    }
    await page.setViewportSize({width:390,height:844}); await page.goto(base);
    await page.locator('.menu-toggle').click();
    assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'),'true');
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'),'false');
    await page.screenshot({path:path.join(out,'mobile.png'),fullPage:true});
    await page.locator('[data-filter="fintech"]').click();
    await page.locator('#frontier-ai-valuation-lab').screenshot({path:path.join(out,'fintech-mobile.png')});
    await page.goto(base+'/projects/frontier-ai-valuation-lab.html');
    await page.locator('.case-hero').screenshot({path:path.join(out,'fintech-case-mobile.png')});
    assert.deepEqual(errors,[]);
    const og=await browser.newPage({viewport:{width:1200,height:630},deviceScaleFactor:1});
    await og.goto(base+'/assets/portfolio-og.svg');
    if (process.env.RENDER_SOCIAL_IMAGE === '1') {
      await og.screenshot({path:path.join(root,'assets/portfolio-og.png')});
    }
    console.log('BROWSER_PASS: 5 filter states, 4 case pages, 3 responsive widths, mobile menu, no JavaScript errors');
  } catch (error) { console.error(error); process.exitCode=1; }
  finally { if(browser) await browser.close(); await new Promise(resolve=>server.close(resolve)); }
})();
