// Preview frames of a composition in headless Chromium (graphics + plate frame).
//   node tools/shoot.js reel-45/index.html <outprefix> t1 t2 ...
// Note: never return the timeline from page.evaluate — Playwright tries to
// serialise it and the call hangs forever.
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const [,, file, out, ...ts] = process.argv;
  const b = await chromium.launch(); const p = await b.newPage();
  p.on('pageerror', e => console.error('pageerror', e.message));
  // headless Chromium here has no route to the CDN (the agent proxy is not its proxy)
  await p.route(/cdnjs\.cloudflare\.com\/.*gsap\.min\.js/, r => r.fulfill({ path: path.join(__dirname, 'vendor', 'gsap.min.js'), contentType: 'application/javascript' }));
  await p.addInitScript(() => { window.__timelines = {}; });
  await p.setViewportSize({ width: 1080, height: 1920 });
  await p.goto('file://' + path.resolve(file), { timeout: 30000 });
  await p.waitForFunction(() => !!(window.__timelines.main || window.tl), null, { timeout: 30000 });
  for (const t of ts) {
    await p.evaluate(async t => {
      const tl = window.__timelines.main || window.tl; tl.seek(+t, false);
      const v = document.getElementById('vid');
      if (v && v.tagName === 'VIDEO') { await new Promise(r => { v.onseeked = r; v.currentTime = +t; setTimeout(r, 3000); }); }
    }, t);
    await p.waitForTimeout(50);
    await p.screenshot({ path: `${out}-${t}.png` });
  }
  await b.close();
})();
