import puppeteer from 'puppeteer-core';
const [url, out, wait, W, H, js] = process.argv.slice(2);
const b = await puppeteer.launch({ executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless:'new', args:['--use-angle=metal','--ignore-gpu-blocklist','--allow-file-access-from-files'] });
const p = await b.newPage(); await p.setViewport({ width: +(W || 1200), height: +(H || 4600) }); const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
await p.goto(url, { waitUntil: 'networkidle0' }); if (js) await p.evaluate(js); await new Promise(r => setTimeout(r, +(wait || 4000)));
await p.screenshot({ path: out, type: 'jpeg', quality: 72, fullPage: true }); console.log(errs.length ? 'ERRORS: ' + errs.join(' | ') : 'no errors'); await b.close();
