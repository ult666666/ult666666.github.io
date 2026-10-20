/* Real-browser regression checks for navigation when enhancement is unavailable. */
const assert = require('node:assert/strict');
const routes = ['/', '/fintech.html', '/projects/lineageguard.html',
  '/projects/motionx.html', '/projects/trading-research.html',
  '/projects/frontier-ai-valuation-lab.html'];

module.exports = async function navigationResilience(browser, base) {
  const results = [];
  for (const mode of ['disabled', 'blocked']) {
    const context = await browser.newContext({javaScriptEnabled: mode !== 'disabled',
      viewport: {width:390, height:844}, reducedMotion:'reduce'});
    try {
      const page = await context.newPage();
      await page.route('**/*', route => {
        const url = new URL(route.request().url());
        if (url.origin !== base) return route.abort();
        if (mode === 'blocked' && url.pathname === '/script.js') return route.abort();
        return route.continue();
      });
      for (const route of routes) {
        await page.goto(base + route, {waitUntil:'load'});
        const links = page.locator('#primary-nav a');
        const visible = await Promise.all((await links.all()).map(link => link.isVisible()));
        results.push({name:`${mode}: primary navigation accessible on ${route}`,
          pass:visible.length > 1 && visible.every(Boolean)});
        results.push({name:`${mode}: no inert menu button on ${route}`,
          pass:!await page.locator('.menu-toggle').isVisible()});
        if (route === '/') {
          results.push({name:`${mode}: no inert filter buttons`,
            pass:!await page.locator('.filters').isVisible()});
          results.push({name:`${mode}: all eight projects remain visible`,
            pass:await page.locator('.project-card:visible').count() === 8});
        }
        results.push({name:`${mode}: no horizontal overflow on ${route}`,
          pass:await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)});
        if (visible.length && visible[0]) {
          await links.first().click();
          results.push({name:`${mode}: Work link navigates on ${route}`,
            pass:new URL(page.url()).pathname === '/' && new URL(page.url()).hash === '#work'});
        }
      }
    } finally {await context.close();}
  }
  const context = await browser.newContext({viewport:{width:390,height:844},reducedMotion:'reduce'});
  try {
    const page = await context.newPage();
    await page.route('**/*', route => new URL(route.request().url()).origin === base ? route.continue() : route.abort());
    await page.goto(base, {waitUntil:'load'});
    const toggle=page.locator('.menu-toggle');
    await toggle.focus(); await page.keyboard.press('Enter'); await page.keyboard.press('Tab');
    results.push({name:'keyboard enters the open navigation',
      pass:await page.locator('#primary-nav').evaluate(nav=>nav.contains(document.activeElement))});
    await page.keyboard.press('Escape');
    results.push({name:'Escape returns focus to the menu trigger',
      pass:await toggle.evaluate(node=>node===document.activeElement)});
    results.push({name:'Escape closes the menu with matching accessibility state',
      pass:await toggle.getAttribute('aria-expanded') === 'false' && !await page.locator('#primary-nav').isVisible()});
    await toggle.click();
    await page.setViewportSize({width:1024,height:844});
    await page.waitForFunction(()=>document.querySelector('.menu-toggle').getAttribute('aria-expanded')==='false');
    await page.setViewportSize({width:390,height:844});
    results.push({name:'resize does not reopen stale mobile state',
      pass:!await page.locator('#primary-nav').isVisible()});
  } finally {await context.close();}
  const failed=results.filter(item=>!item.pass);
  console.log('NAVIGATION_RESILIENCE '+JSON.stringify({checks:results.length,failed}));
  assert.equal(failed.length,0,'Navigation regression: '+failed.map(item=>item.name).join('; '));
};
