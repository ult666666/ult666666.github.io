const assert = require('node:assert/strict');

// Check the name exposed by the browser, including when links are listed apart from their card or row.
async function assertProjectLinkNames(groups, headingSelector, linkSelector) {
  for (const group of await groups.all()) {
    const project = await group.locator(headingSelector).innerText();
    for (const link of await group.locator(linkSelector).all()) {
      const action = await link.innerText();
      const name = `${action} (${project})`;
      assert.equal(await link.and(group.getByRole('link', {name, exact:true})).count(), 1, name);
    }
  }
}

function luminance(rgb) {
  const channels = rgb.match(/^rgb\((\d+), (\d+), (\d+)\)$/);
  assert(channels, 'Expected an opaque sRGB color, got ' + rgb);
  const linear = channels.slice(1).map(channel => {
    const value = Number(channel) / 255;
    return value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2];
}

function contrastRatio(first, second) {
  const a = luminance(first);
  const b = luminance(second);
  return (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
}

module.exports = {assertProjectLinkNames, contrastRatio};
