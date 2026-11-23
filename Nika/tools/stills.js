// Quick look at a composition without a render: seek the timeline, screenshot.
//   node Nika/tools/stills.js <reel dir> <t1,t2,...> <out dir>
// Overlays only are exact; the plate shows whatever frame the <video> has seeked to.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [dir, list, out] = process.argv.slice(2);
  const ts = list.split(',').map(Number);
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const p = await (await b.newContext({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 })).newPage();
  p.on('pageerror', e => console.log('PAGEERR', e.message));
  await p.goto('file://' + path.resolve(dir, 'index.html'), { waitUntil: 'load' });
  await p.waitForFunction(() => !!(window.__timelines && window.__timelines.main), null, { timeout: 60000, polling: 250 });
  for (const t of ts) {
    // Playwright's Chromium has no H.264, so paint her frame in from ffmpeg
    const jpg = path.join(out, `plate_${t.toFixed(2)}.jpg`);
    require('child_process').execFileSync('ffmpeg', ['-v', 'error', '-y', '-ss', String(t), '-i',
      path.resolve(dir, 'assets/base.mp4'), '-frames:v', '1', '-q:v', '3', jpg]);
    await p.evaluate(([t, url]) => {
      const v = document.getElementById('vid'); v.style.visibility = 'hidden';
      const cam = document.getElementById('cam');
      cam.style.background = `url(${url}) center / cover`;
      window.__timelines.main.seek(t, false);
    }, [t, 'file://' + path.resolve(jpg)]);
    await p.waitForTimeout(120);
    await p.screenshot({ path: path.join(out, `s_${t.toFixed(2).padStart(5, '0')}.png`) });
  }
  await b.close();
})();
