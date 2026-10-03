// Optional browser smoke using the neighbouring kit's pinned Playwright installation.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
const { chromium } = await import(new URL('../../symplectic-camel/presentation-kit/node_modules/playwright/index.mjs', import.meta.url));
const browser = await chromium.launch({executablePath: process.env.CHROMIUM_PATH || '/home/bluestar/.cache/ms-playwright/chromium-1234/chrome-linux64/chrome', args:['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader'],headless:true});
const page = await browser.newPage({viewport:{width:1440,height:1000},reducedMotion:'reduce',hasTouch:true});
const errors = [], requests = [], comparisonEvidence = [];
const sourceHashes = Object.fromEntries(['live.js', 'live-model.js', 'live-guide.html'].map(name => [name, createHash('sha256').update(readFileSync(new URL('../docs/' + name, import.meta.url))).digest('hex')]));
page.on('pageerror', e => errors.push(String(e)));
page.on('request', r => requests.push(r.url()));
const state = () => page.evaluate(() => SoapLive.getState());
const ready = () => page.waitForFunction(() => SoapLive.getState().ready && !SoapLive.getState().error);
try {
  await page.goto(new URL('../docs/live.html', import.meta.url).href); await ready();
  const evidence = [];
  for (let scene = 0; scene < 4; scene++) {
    const initial = await state(); assert.equal(initial.scene, scene);
    if (scene === 0) { await page.click('#soap-reveal'); assert.equal((await state()).revealed, true); }
    if (scene === 1) {
      await page.click('#soap-compare'); assert.equal((await state()).comparison, true);
      await page.click('#soap-dip'); assert.ok((await state()).model.length < initial.model.length);
      assert.equal((await state()).comparison, false, 'changing dip must clear the competing overlay');
      assert.match(await page.locator('#metric-detail').innerText(), /First dip: 5\.196\. This dip is .* shorter\./);
      assert.match(await page.locator('#soap-compare').innerText(), /^Compare five-side network$/);
      comparisonEvidence.push({dip:(await state()).dip, comparison:(await state()).comparison, readout:await page.locator('#metric-detail').innerText()});
      await page.click('#soap-compare'); assert.equal((await state()).comparison, true);
      assert.match(await page.locator('#metric-detail').innerText(), /equal length within numerical tolerance/);
      assert.doesNotMatch(await page.locator('#metric-detail').innerText(), /0\.00% longer/);
      comparisonEvidence.push({dip:(await state()).dip, comparison:(await state()).comparison, readout:await page.locator('#metric-detail').innerText()});
      await page.click('#soap-dip'); assert.equal((await state()).comparison, false);
    }
    if (scene === 2) { await page.click('#soap-highlight'); assert.equal((await state()).highlighted, true); }
    if (scene === 3) { await page.click('#soap-frame'); await ready(); assert.notEqual((await state()).model.digest, initial.model.digest); }
    if (scene >= 2) {
      const box = await page.locator('#film').boundingBox();
      await page.mouse.move(box.x + box.width*.5, box.y + box.height*.5); await page.mouse.down();
      await page.mouse.move(box.x + box.width*.6, box.y + box.height*.55, {steps:4}); await page.mouse.up();
      await page.mouse.wheel(0,120); await page.waitForTimeout(100);
      assert.notDeepEqual((await state()).camera, initial.camera);
    }
    evidence.push(await state());
    await page.keyboard.press('r'); await ready(); assert.deepEqual(await state(), initial);
    if (scene < 3) { await page.keyboard.press('ArrowRight'); await ready(); }
  }
  for (let scene = 2; scene >= 0; scene--) { await page.locator('#scene-prev').tap(); await ready(); assert.equal((await state()).scene, scene); }
  assert.deepEqual(errors, []); assert.ok(requests.every(url => url.startsWith('file:')));
  console.log(JSON.stringify({status:'PASS', sourceHashes, comparisonEvidence, command:'unshare -rn taskset -c 11 node tests/live-browser-smoke.mjs',source:fileURLToPath(new URL('../docs/live.html',import.meta.url)),networkRequests:requests.filter(url=>!url.startsWith('file:')),errors,scenes:evidence.map(s=>({scene:s.scene,renderer:s.renderer,model:s.model,reset:'full snapshot matched'}))},null,2));
} finally { await browser.close(); }
