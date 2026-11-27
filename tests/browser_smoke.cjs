/* Real Chromium checks for navigation, content inventory, accessibility basics and responsive layout. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const {assertProjectLinkNames} = require('./accessibility_assertions.cjs');
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
const publicFiles = new Set(JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'public-files.json'), 'utf8')).files);

async function assertSharePreview(page, kind) {
  const origin = 'https://ult666666.github.io';
  const pagePath = new URL(page.url()).pathname;
  const property = key => page.locator(`head meta[property="og:${key}"]`).getAttribute('content');
  const title = await page.locator('h1').innerText();
  const hero = page.locator('.case-hero-media img');
  const hasScreenshot = await hero.count() > 0;
  const imagePath = hasScreenshot ? await hero.getAttribute('src') : '/assets/portfolio-og.png';
  const imageAlt = hasScreenshot ? await hero.getAttribute('alt') :
    'Charles Dai’s portfolio card introducing his work in finance, data, and tools that check AI systems.';
  assert(publicFiles.has(pagePath.slice(1)) && publicFiles.has(imagePath.slice(1)), pagePath);
  assert.equal(await property('type'), kind);
  assert.equal(await property('title'), kind === 'article' ? `${title}, a case study by Charles Dai` : `${title} | Charles Dai`);
  assert.equal(await property('description'), await page.locator('head meta[name="description"]').getAttribute('content'));
  assert.equal(await property('url'), origin + pagePath);
  assert.equal(await page.locator('head link[rel="canonical"]').getAttribute('href'), origin + pagePath);
  assert.equal(await property('image'), origin + imagePath);
  assert.equal(await property('image:alt'), imageAlt);
  assert.equal(await page.locator('head meta[name="twitter:card"]').getAttribute('content'), 'summary_large_image');
  // Decode the exact advertised path on the staged origin, including the card
  // used by text-led pages where no visible img would otherwise fetch it.
  const size = await page.evaluate(async src => {
    const image = new Image();
    image.src = src;
    await image.decode();
    return [image.naturalWidth, image.naturalHeight];
  }, imagePath);
  assert.deepEqual([Number(await property('image:width')), Number(await property('image:height'))], size, imagePath);
}

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
    await require('./catalog_showcase.cjs')(browser, base);
    await require('./blast_showcase.cjs')(browser, base);
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
    assert.equal(await page.locator('article.work').count(), 5);
    assert.equal(await page.locator('article.work').first().getAttribute('id'), 'frontier-ai-valuation-lab');
    assert.equal(await page.locator('.index-table th[scope="row"]').count(), 21);
    const shortcuts = page.getByRole('navigation', {name:'Featured projects'}).getByRole('link');
    for (const link of await shortcuts.all()) {
      const target = await link.getAttribute('href');
      await link.click();
      assert.equal(new URL(page.url()).hash, target, 'Featured shortcut opens its project');
      assert.equal(await page.locator('article.work' + target).count(), 1);
    }
    await assertProjectLinkNames(page.locator('article.work'), 'h3', '.work-links a');
    await assertProjectLinkNames(page.locator('.index-table tr:has(td.links)'), 'th[scope="row"]', 'td.links a');
    assert.equal(await page.locator('button,[role="button"]').count(), 0, 'The homepage has no scripted controls');
    for (const [label, hash] of [['Work','#work'],['Index','#index'],['About','#about'],['Contact','#contact']]) {
      await page.locator('#primary-nav').getByRole('link',{name:label,exact:true}).click();
      assert.equal(new URL(page.url()).hash, hash);
      assert.equal(await page.locator(hash).count(), 1);
    }
    for (const selector of ['.work-figure img']) {
      const images = page.locator(selector);
      assert.equal(await images.count(), 5);
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
    await page.goto(base + '/projects/catalog.html?area=backend&q=SQLite');
    await assertSharePreview(page, 'website');
    for (const name of ['crossbook','ledgerline','lineageguard','motionx','trading-research','frontier-ai-valuation-lab']) {
      const response = await page.goto(base + '/projects/' + name + '.html');
      assert.equal(response.status(),200);
      assert.equal(await page.locator('h1').count(),1);
      await assertSharePreview(page, 'article');
      // Every case study ends with one Limits section and a Code and docs list.
      const sections = {'frontier-ai-valuation-lab':8, crossbook:9, ledgerline:5, lineageguard:10, 'trading-research':6, motionx:5};
      assert.equal(await page.locator('.case-article section').count(),sections[name],`${name} case study sections`);
      if (name === 'crossbook') {
        const replay = page.locator('#replay-a-session');
        assert.match(await replay.innerText(), /3749b835b0ff0cae and state hash ee0bfb94bbfc39a7/);
        assert.match(await replay.locator('pre').innerText(), /gen --orders 100000 --seed 42/);
        assert.equal(await replay.getByRole('link', {name:'Run the browser comparison'}).getAttribute('href'),
          'https://ult666666.github.io/crossbook/#stress-title');
      }
      if (name === 'frontier-ai-valuation-lab') {
        assert.equal(await page.locator('#review-guide').count(),1);
        assert.equal(await page.locator('#engineering-evidence li').count(),8);
        assert.equal(await page.locator('#review-guide ol li').count(),6,'Try it is a short ordered list');
        assert.equal(await page.getByRole('link',{name:'Try the ownership limit',exact:true}).getAttribute('href'),'https://frontier-ai-valuation-lab.vercel.app/index.html#ownership-example');
        await page.locator('#review-guide').screenshot({path:path.join(out,'fintech-review-desktop.png')});
        assert.equal(await page.locator('.case-detail-media > a').getAttribute('href'),'https://frontier-ai-valuation-lab.vercel.app/index.html#ownership-example');
        assert.equal(await page.locator('#section-3 h2').innerText(),'How it is built');
        assert.equal(await page.locator('#section-4 h2').innerText(),'Limits');
        await captureFinancingCase(page,path.join(out,'financing-case-desktop.png'));
      }
    }
    await page.goto(base);
    await page.getByRole('row').filter({has:page.getByRole('rowheader', {name:'ledgerline',exact:true})})
      .getByRole('link', {name:'Case study'}).click();
    assert.equal(new URL(page.url()).pathname, '/projects/ledgerline.html');
    await page.getByRole('link', {name:'See the wallet balances'}).click();
    const wallet = page.getByRole('table', {name:'Alice’s wallet after each request (USD)'});
    assert.deepEqual(await wallet.getByRole('columnheader').allTextContents(),
                     ['Action','Posted','Held','Available']);
    const rows = await wallet.locator('tbody tr').evaluateAll(nodes =>
      nodes.map(row => [...row.cells].map(cell => cell.textContent)));
    assert.deepEqual(rows, [
      ['Deposit $100','$100.00','$0.00','$100.00'], ['Reserve $40','$100.00','$40.00','$60.00'],
      ['Capture $32','$68.00','$0.00','$68.00'], ['Retry capture','$68.00','$0.00','$68.00'],
      ['Reserve $15','$68.00','$15.00','$53.00'], ['Void the hold','$68.00','$0.00','$68.00'],
    ]);
    for (const width of [320,390,768]) {
      await page.setViewportSize({width,height:850});
      await page.reload();  // Lay out a fresh document at this viewport, as a mobile visit would.
      const layout = await wallet.evaluate(table => ({
        right: table.getBoundingClientRect().right,
        clipped: [...table.querySelectorAll('th,td')]
          .filter(cell => cell.scrollWidth > cell.clientWidth + 1).map(cell => cell.textContent)
      }));
      assert(layout.right <= width && layout.clipped.length === 0,
             `Wallet balances at ${width}px: ${JSON.stringify(layout)}`);
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1),
             `Ledgerline fits the screen at ${width}px`);
      if (width === 320) await wallet.screenshot({path:path.join(out,'ledgerline-balances-mobile.png')});
    }
    await page.setViewportSize({width:1440,height:1000});
    await page.goto(base + '/projects/frontier-ai-valuation-lab.html');
    await page.getByRole('link',{name:'More on the fintech work',exact:true}).click();
    assert.equal(new URL(page.url()).pathname, '/fintech.html');
    assert.equal(await page.locator('h1').count(),1);
    assert.equal(await page.locator('h1').innerText(),'Comparing financing plans for a frontier AI lab');
    assert.equal(await page.locator('.fintech-intro .button-primary').getAttribute('href'),'https://frontier-ai-valuation-lab.vercel.app/capital.html#worked-decision');
    assert.equal(await page.locator('.fintech-doc-list li').count(),4);
    assert.equal(await page.locator('.fintech-journey-card').count(),4);
    assert.equal(await page.locator('#financing-journey').getAttribute('href'),'https://frontier-ai-valuation-lab.vercel.app/capital.html#capital-record');
    // Wait for the decode: under load the image can still be in flight when the page settles.
    const productImage = page.locator('.fintech-product-image img');
    await page.waitForFunction(image => image.complete && image.naturalWidth > 0, await productImage.elementHandle(), {timeout:10000});
    assert.equal(await productImage.evaluate(image => image.complete && image.naturalWidth > 0),true);
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
        const clipped=await page.locator('.capital-example,.case-detail-media,.fintech-journey-card,.fintech-doc-list').evaluateAll(nodes=>nodes.some(node=>node.scrollWidth>node.clientWidth+1));
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
    assert.equal(await staticPage.locator('#engineering-evidence li').count(),8);
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
    console.log('BROWSER_PASS: homepage inventory and anchors, decoded images, local links, 6 case pages, fintech gateway, exact live-demo destination, 4 fintech responsive widths, 200% zoom, keyboard skip link, no-JavaScript entry and no third-party requests');
  } catch (error) { console.error(error); process.exitCode=1; }
  finally { if(browser) await browser.close(); await new Promise(resolve=>server.close(resolve)); }
})();
