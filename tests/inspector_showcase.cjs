/* Inspect the actual staged case study: no external requests or invented screenshots. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
module.exports = async function inspectorShowcase(browser, base) {
  const out = path.resolve(__dirname, '../test-results'); fs.mkdirSync(out, {recursive:true});
  const context = await browser.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});
  const requests=[],errors=[]; const checks=[];
  await context.route('**/*', route => {
    if(new URL(route.request().url()).origin===base) return route.continue();
    requests.push(route.request().url()); return route.abort();
  });
  try {
    const page=await context.newPage(); page.on('pageerror',e=>errors.push(e.message));
    await page.goto(base+'/projects/lineageguard.html',{waitUntil:'networkidle'});
    assert.equal(await page.locator('#review-inspector').count(),1);
    await page.locator('.case-sidebar a[href="#review-inspector"]').click();
    assert.equal(new URL(page.url()).hash,'#review-inspector');
    const image=page.locator('#review-inspector .case-detail-media img');
    await image.scrollIntoViewIfNeeded();
    await page.waitForFunction(el=>el.complete&&el.naturalWidth>0,await image.elementHandle());
    assert.deepEqual(await image.evaluate(el=>[el.naturalWidth,el.naturalHeight]),[1170,987]);
    assert.equal(await image.evaluate(el=>Number(el.width)<=el.parentElement.clientWidth+1),true);
    checks.push('real public Inspector screenshot loads with correct authored dimensions');
    for(const link of await page.locator('#review-inspector .case-section-links a').all()){
      assert((await link.getAttribute('href')).includes('/blob/6ed607b5c9ff6f46f2bb3214b04d040b04c02c52/'));
      assert.equal(await link.getAttribute('target'),'_blank');
      assert((await link.getAttribute('rel')).includes('noreferrer'));
    }
    checks.push('version-pinned evidence links retain safe external navigation');
    for(const width of [320,360,390,768,1440]){
      await page.setViewportSize({width,height:950});
      await page.waitForFunction(()=>document.documentElement.scrollWidth<=innerWidth+1,null,{timeout:5000});
      assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'case page overflow at '+width);
      assert(await image.evaluate(el=>el.getBoundingClientRect().right<=innerWidth+1),'Inspector image overflow at '+width);
      checks.push('case and Inspector responsive at '+width);
    }
    await page.locator('#review-inspector').screenshot({path:path.join(out,'lineageguard-inspector-case-desktop.png')});
    await page.evaluate(()=>document.documentElement.style.zoom='2');
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
    await page.evaluate(()=>document.documentElement.style.zoom='');checks.push('Inspector case remains readable at 200 percent zoom');
    await page.locator('.case-sidebar a[href="#try-workflow"]').focus();
    await page.keyboard.press('Enter'); assert.equal(new URL(page.url()).hash,'#try-workflow');
    assert.match(await page.locator('#try-workflow').innerText(),/Evidence-source outage/);
    checks.push('keyboard navigation reaches the demonstration instructions');
    await page.setViewportSize({width:390,height:844});
    await page.locator('#review-inspector').screenshot({path:path.join(out,'lineageguard-inspector-case-mobile.png')});
    assert.deepEqual(requests,[]);assert.deepEqual(errors,[]);checks.push('no external loaded resources or JavaScript errors');
  } finally {await context.close();}
  const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
  try{
    const page=await nojs.newPage();
    await page.route('**/*',r=>new URL(r.request().url()).origin===base?r.continue():r.abort());
    await page.goto(base+'/projects/lineageguard.html');
    assert.equal(await page.locator('#review-inspector').isVisible(),true);
    assert.equal(await page.locator('#try-workflow').isVisible(),true);
    assert.equal(await page.locator('.case-sidebar a[href="#review-inspector"]').isVisible(),true);
    checks.push('Inspector story and instructions remain accessible without JavaScript');
  } finally {await nojs.close();}
  console.log('INSPECTOR_SHOWCASE '+JSON.stringify({result:'pass',checks}));
};
