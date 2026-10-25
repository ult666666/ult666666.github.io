/* Real Chromium checks for navigation, content inventory, accessibility basics and responsive layout. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const root = path.resolve(process.env.PORTFOLIO_TEST_ROOT || path.resolve(__dirname, '..'));
const evidenceRoot = path.resolve(__dirname, '..', 'test-results');
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
async function captureFinancingCase(page, destination) {
  const image = page.locator('.case-detail-media img');
  await image.scrollIntoViewIfNeeded();
  // Routing deliberately disables cache. Wait for a lazy image's real load
  // before decode; screenshots must not depend on an earlier cached visit.
  const imageNode = await image.elementHandle();
  await page.waitForFunction(node => node.complete && node.naturalWidth > 0,
                            imageNode, {timeout:15000});
  await image.evaluate(node => node.decode());
  assert.equal(await image.evaluate(node => node.complete && node.naturalWidth > 0),true);
  assert.equal(await image.evaluate(node => node.naturalWidth > node.naturalHeight),true,'The ownership case should use a compact landscape application capture');
  assert.equal(await image.evaluate(node => Number(node.getAttribute('width')) === node.naturalWidth && Number(node.getAttribute('height')) === node.naturalHeight),true,'Authored screenshot dimensions must match the decoded asset');
  await page.locator('.case-detail-media').evaluate(figure => {
    const headerHeight = document.querySelector('.site-header').getBoundingClientRect().height;
    window.scrollTo({left:0,top:window.scrollY + figure.getBoundingClientRect().top - headerHeight - 16,behavior:'instant'});
  });
  // A viewport capture avoids compositor height limits on very long case pages.
  await page.screenshot({path:destination});
}
(async () => {
  let browser;
  try {
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    const base = `http://127.0.0.1:${server.address().port}`;
    const launchOptions = {headless:true};
    if (process.env.PORTFOLIO_CHROMIUM_EXECUTABLE) launchOptions.executablePath = process.env.PORTFOLIO_CHROMIUM_EXECUTABLE;
    if (process.env.PORTFOLIO_CHROMIUM_ARGS) {
      const args = JSON.parse(process.env.PORTFOLIO_CHROMIUM_ARGS);
      assert(Array.isArray(args) && args.every(value => typeof value === 'string'), 'Browser launch arguments must be a JSON array of strings');
      launchOptions.args = args;
    }
    browser = await chromium.launch(launchOptions);
    await require('./navigation_resilience.cjs')(browser, base);
    await require('./inspector_showcase.cjs')(browser, base);
    await require('./engineering_showcase.cjs')(browser, base);
    await require('./foundations_showcase.cjs')(browser, base);
    const page = await browser.newPage({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
    const errors = [];
    const externalRequests = [];
    await page.route('**/*', route => {
      if (new URL(route.request().url()).origin === base) return route.continue();
      externalRequests.push(route.request().url()); return route.abort();
    });
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(base, {waitUntil:'networkidle'});
    assert.equal(await page.locator('h1').count(), 1);
    assert.match(await page.locator('h1').innerText(), /^I’m Charles Dai\./);
    assert.equal(await page.locator('article.work').count(), 4);
    assert.equal(await page.locator('article.work').first().getAttribute('id'), 'frontier-ai-valuation-lab');
    assert.equal(await page.locator('.index-table th[scope="row"]').count(), 17);
    assert.equal(await page.locator('button,[role="button"]').count(), 0, 'The homepage has no scripted controls');
    for (const [label, hash] of [['Work','#work'],['Index','#index'],['About','#about'],['Contact','#contact']]) {
      await page.locator('#primary-nav').getByRole('link',{name:label,exact:true}).click();
      assert.equal(new URL(page.url()).hash, hash);
      assert.equal(await page.locator(hash).count(), 1);
    }
    for (const selector of ['.work-figure img']) {
      const images = page.locator(selector);
      assert.equal(await images.count(), 4);
      for (const img of await images.all()) {
        await img.scrollIntoViewIfNeeded();
        await img.evaluate(node => node.decode());
        assert.equal(await img.evaluate(node => node.complete && node.naturalWidth >= 300), true, selector);
        assert.equal(await img.evaluate(node => Number(node.getAttribute('width')) === node.naturalWidth && Number(node.getAttribute('height')) === node.naturalHeight), true, 'Authored image size must match the file');
      }
    }
    const localTargets = await page.locator('a[href^="/"]').evaluateAll(links => [...new Set(links.map(link => link.getAttribute('href').split('#')[0]))]);
    for (const target of localTargets) {
      const response = await page.request.get(base + target);
      assert.equal(response.status(), 200, 'Local link ' + target);
    }
    await page.goto(base);
    assert.equal(await page.locator('#engineering-proof .proof-path').count(),2);
    for(const anchor of await page.locator('#engineering-proof .proof-path').all()){
      assert.equal(await anchor.getAttribute('target'),'_blank');
      assert((await anchor.getAttribute('rel')).includes('noreferrer'));
    }
    const out = evidenceRoot; fs.mkdirSync(out,{recursive:true});
    await page.evaluate(()=>window.scrollTo(0,0));
    await page.waitForTimeout(100);
    await page.screenshot({path:path.join(out,'desktop.png'),fullPage:true});
    await page.locator('#frontier-ai-valuation-lab').screenshot({path:path.join(out,'fintech-desktop.png')});
    for (const name of ['lineageguard','motionx','trading-research','frontier-ai-valuation-lab']) {
      const response = await page.goto(base + '/projects/' + name + '.html');
      assert.equal(response.status(),200);
      assert.equal(await page.locator('h1').count(),1);
      assert.equal(await page.locator('.case-article section').count(),name === 'frontier-ai-valuation-lab' ? 5 : name === 'lineageguard' ? 6 : 4);
      if (name === 'frontier-ai-valuation-lab') {
        assert.equal(await page.locator('#review-guide').count(),1);
        assert.equal(await page.locator('#engineering-evidence tbody tr').count(),4);
        assert.equal(await page.getByRole('link',{name:'Try Ownership Frontier',exact:true}).getAttribute('href'),'https://frontier-ai-valuation-lab.vercel.app/index.html#ownership-example');
        await page.locator('#review-guide').screenshot({path:path.join(out,'fintech-review-desktop.png')});
        assert.equal(await page.locator('.case-detail-media > a').getAttribute('href'),'https://frontier-ai-valuation-lab.vercel.app/index.html#ownership-example');
        assert.equal(await page.locator('#section-3 h2').innerText(),'Make the engineering inspectable');
        assert.equal(await page.locator('#section-4 h2').innerText(),'My role and the project boundaries');
        await captureFinancingCase(page,path.join(out,'financing-case-desktop.png'));
      }
    }
    await page.goto(base + '/projects/frontier-ai-valuation-lab.html');
    await page.getByRole('link',{name:'More on the fintech work',exact:true}).click();
    assert.equal(new URL(page.url()).pathname, '/fintech.html');
    assert.equal(await page.locator('h1').count(),1);
    assert.equal(await page.locator('h1').innerText(),'Comparing financing plans for a frontier AI lab');
    assert.equal(await page.locator('.fintech-intro .button-primary').getAttribute('href'),'https://frontier-ai-valuation-lab.vercel.app/capital.html#worked-decision');
    assert.equal(await page.locator('.fintech-proof').count(),4);
    assert.equal(await page.locator('.fintech-journey-card').count(),4);
    assert.equal(await page.locator('#financing-journey').getAttribute('href'),'https://frontier-ai-valuation-lab.vercel.app/capital.html#capital-record');
    assert.equal(await page.locator('.fintech-product-image img').evaluate(image => image.complete && image.naturalWidth > 0),true);
    await page.screenshot({path:path.join(out,'fintech-gateway-desktop.png'),fullPage:true});
    for (const width of [390,768,1440]) {
      await page.setViewportSize({width,height:900}); await page.goto(base);
      const sizes=await page.evaluate(()=>[document.documentElement.scrollWidth,innerWidth]);
      assert(sizes[0] <= sizes[1]+1, `Horizontal overflow at ${width}: ${sizes}`);
    }
    for (const width of [360,390,768,1440]) {
      await page.setViewportSize({width,height:1000});
      for (const route of ['/fintech.html','/projects/frontier-ai-valuation-lab.html']) {
        await page.goto(base+route);
        const sizes=await page.evaluate(()=>[document.documentElement.scrollWidth,innerWidth]);
        assert(sizes[0] <= sizes[1]+1, `Horizontal overflow on ${route} at ${width}: ${sizes}`);
        const clipped=await page.locator('.capital-example,.case-capital-example,.case-detail-media,.fintech-journey-card').evaluateAll(nodes=>nodes.some(node=>node.scrollWidth>node.clientWidth+1));
        assert.equal(clipped,false,`Clipped example on ${route} at ${width}`);
      }
    }
    await page.setViewportSize({width:1440,height:1000});
    for (const route of ['/fintech.html','/projects/frontier-ai-valuation-lab.html']) {
      await page.goto(base+route);
      await page.evaluate(()=>document.documentElement.style.zoom='2');
      assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`Horizontal page overflow on ${route} at 200% zoom`);
      await page.evaluate(()=>document.documentElement.style.zoom='');
    }
    await page.setViewportSize({width:390,height:844}); await page.goto(base);
    assert.equal(await page.locator('#primary-nav a').evaluateAll(links => links.every(link => {
      const box = link.getBoundingClientRect(); return box.width > 0 && box.right <= innerWidth;
    })), true, 'All navigation links fit on a phone without a menu');
    await page.screenshot({path:path.join(out,'mobile.png'),fullPage:true});
    await page.locator('#frontier-ai-valuation-lab').screenshot({path:path.join(out,'fintech-mobile.png')});
    await page.goto(base+'/projects/frontier-ai-valuation-lab.html');
    await page.locator('.case-hero').screenshot({path:path.join(out,'fintech-case-mobile.png')});
    await page.locator('#review-guide').screenshot({path:path.join(out,'fintech-review-mobile.png')});
    await captureFinancingCase(page,path.join(out,'financing-case-mobile.png'));
    await page.goto(base+'/fintech.html');
    await page.keyboard.press('Tab');
    assert.equal(await page.locator('.skip-link').evaluate(node=>node===document.activeElement),true);
    await page.keyboard.press('Enter');
    assert.equal(new URL(page.url()).hash,'#main');
    await page.screenshot({path:path.join(out,'fintech-gateway-mobile.png'),fullPage:true});
    const noJs=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
    const staticPage=await noJs.newPage();
    await staticPage.goto(base+'/fintech.html');
    assert.equal(await staticPage.locator('h1').isVisible(),true);
    assert.equal(await staticPage.locator('.fintech-intro .button-primary').isVisible(),true);
    assert.equal(await staticPage.locator('.fintech-journey-card').count(),4);
    assert.equal(await staticPage.locator('#financing-journey').isVisible(),true);
    await staticPage.goto(base+'/projects/frontier-ai-valuation-lab.html');
    assert.equal(await staticPage.locator('#review-guide').isVisible(),true);
    assert.equal(await staticPage.locator('#engineering-evidence tbody tr').count(),4);
    await staticPage.goto(base);
    assert.equal(await staticPage.locator('#engineering-proof .proof-path').count(),2);
    await staticPage.locator('#engineering-proof').screenshot({path:path.join(out,'engineering-proof-nojs-mobile.png')});
    await noJs.close();
    assert.deepEqual(errors,[]);
    assert.deepEqual(externalRequests,[], 'The portfolio loaded third-party resources');
    await page.setViewportSize({width:1440,height:1000});await page.goto(base);
    await page.locator('#engineering-proof').screenshot({path:path.join(out,'engineering-proof-desktop.png')});
    const og=await browser.newPage({viewport:{width:1200,height:630},deviceScaleFactor:1});
    await og.goto(base+'/assets/portfolio-og.svg');
    if (process.env.RENDER_SOCIAL_IMAGE === '1') {
      await og.screenshot({path:path.join(root,'assets/portfolio-og.png')});
    }
    console.log('BROWSER_PASS: homepage inventory and anchors, decoded images, local links, 4 case pages, fintech gateway, exact live-demo destination, 4 fintech responsive widths, 200% zoom, keyboard skip link, no-JavaScript entry and no third-party requests');
  } catch (error) { console.error(error); process.exitCode=1; }
  finally { if(browser) await browser.close(); await new Promise(resolve=>server.close(resolve)); }
})();
