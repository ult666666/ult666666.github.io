/* Real-browser regression checks: navigation is plain links that work with or without JavaScript. */
const assert = require('node:assert/strict');
const routes = ['/', '/fintech.html', '/projects/engineering-lab.html', '/projects/foundations.html', '/projects/lineageguard.html',
  '/projects/motionx.html', '/projects/trading-research.html',
  '/projects/frontier-ai-valuation-lab.html', '/projects/catalog.html'];

module.exports = async function navigationResilience(browser, base) {
  const results = [];
  for (const javaScriptEnabled of [false, true]) {
    const mode = javaScriptEnabled ? 'enabled' : 'disabled';
    for (const width of [320, 390, 1440]) {
      const context = await browser.newContext({javaScriptEnabled, viewport:{width, height:844}, reducedMotion:'reduce'});
      try {
        const page = await context.newPage();
        await page.route('**/*', route => new URL(route.request().url()).origin === base ? route.continue() : route.abort());
        for (const route of routes) {
          await page.goto(base + route, {waitUntil:'load'});
          const links = page.locator('#primary-nav a');
          const names = await links.allInnerTexts();
          const visible = await Promise.all((await links.all()).map(link => link.isVisible()));
          results.push({name:`${mode} ${width}px: four visible navigation links on ${route}`,
            pass:names.join('|') === 'Work|Index|About|Contact' && visible.every(Boolean)});
          results.push({name:`${mode} ${width}px: no menu button on ${route}`,
            pass:await page.locator('.menu-toggle').count() === 0});
          results.push({name:`${mode} ${width}px: no horizontal overflow on ${route}`,
            pass:await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)});
          const boxes = await Promise.all((await links.all()).map(link => link.boundingBox()));
          results.push({name:`${mode} ${width}px: navigation links are at least 24px tall on ${route}`,
            pass:boxes.every(box => box && box.height >= 24)});
          await links.first().click();
          results.push({name:`${mode} ${width}px: Work link navigates on ${route}`,
            pass:new URL(page.url()).pathname === '/' && new URL(page.url()).hash === '#work'});
        }
      } finally {await context.close();}
    }
  }
  const context = await browser.newContext({viewport:{width:390, height:844}, reducedMotion:'reduce'});
  try {
    const page = await context.newPage();
    await page.route('**/*', route => new URL(route.request().url()).origin === base ? route.continue() : route.abort());
    await page.goto(base, {waitUntil:'load'});
    await page.keyboard.press('Tab');
    results.push({name:'first Tab reaches the skip link',
      pass:await page.locator('.skip-link').evaluate(node => node === document.activeElement)});
    await page.keyboard.press('Tab');
    results.push({name:'second Tab reaches the site name',
      pass:await page.locator('.site-name').evaluate(node => node === document.activeElement)});
    await page.keyboard.press('Tab');
    results.push({name:'third Tab enters the navigation at Work',
      pass:await page.locator('#primary-nav a').first().evaluate(node => node === document.activeElement)});
    await page.keyboard.press('Enter');
    results.push({name:'Enter on Work follows the link', pass:new URL(page.url()).hash === '#work'});
  } finally {await context.close();}
  const failed = results.filter(item => !item.pass);
  console.log('NAVIGATION_RESILIENCE ' + JSON.stringify({checks:results.length, failed}));
  assert.equal(failed.length, 0, 'Navigation regression: ' + failed.map(item => item.name).join('; '));
};
