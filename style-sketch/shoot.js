// screenshot a GSAP composition at given times:  node shoot.js <html> <outprefix> t1 t2 ...
const { chromium } = require('playwright');
(async () => {
  const [,, file, out, ...ts] = process.argv;
  const b = await chromium.launch(); const p = await b.newPage();
  p.on('pageerror', e => console.error('err', e.message));
  await p.setViewportSize({ width: 1080, height: 1920 });
  await p.goto('file://' + file, {timeout: 30000}); console.error('c');
  await p.waitForFunction(() => window.ready === true, null, {timeout: 20000});
  for (const t of ts) { await p.evaluate(t => { window.tl.seek(+t, false); }, t); await p.waitForTimeout(60);
    await p.screenshot({ path: `${out}-${t}.png` }); }
  await b.close();
})();
