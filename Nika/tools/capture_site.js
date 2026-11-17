// Capture the UNLOCK site's product mockups as clean, transparent PNGs at 4x.
//   node Nika/tools/capture_site.js <out dir>
//
// The site draws its "screenshots" in HTML, and in the hero they overlap and clip
// each other. So each one is cloned into an empty "studio" container on its own,
// with everything else on the page hidden, and shot there whole.
const { chromium } = require('playwright');
const path = require('path');

const TARGETS = [            // name, selector, CSS width to lay it out at (0 = as on the site)
  ['products', '.hero .fl--app .ui', 430],
  ['salespage', '.hero .fl--page .ui', 360],
  ['phone', '.hero .phone', 0],
  ['toast-pay', '.hero .fl--pay .toast', 0],
  ['editor', '#card-course .ui', 320],
  ['payments', '#payments .ui', 0],
  ['dashboard', '#analytics .ui.dash', 0],
];

(async () => {
  const out = path.resolve(process.argv[2]);
  const b = await chromium.launch();
  const p = await (await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 4 })).newPage();
  await p.goto('https://unlockexpertise.online/uk', { waitUntil: 'networkidle', timeout: 60000 });
  await p.evaluate(() => document.querySelectorAll('.ucc, header.nav').forEach(e => e.remove()));   // cookie bar, nav
  await p.addStyleTag({ content: `
    .rv{opacity:1!important;transform:none!important} *{animation:none!important;transition:none!important}
    body > *:not([id^=studio]){visibility:hidden!important}
    [id^=studio], [id^=studio] *{visibility:visible!important}
    [id^=studio] .fl, [id^=studio] .stage, [id^=studio] .stage-wrap{opacity:1!important;position:static!important;transform:none!important}` });
  for (const [n, sel, w] of TARGETS) {
    const ok = await p.evaluate(([n, sel, w]) => {
      const src = document.querySelector(sel); if (!src) return false;
      const st = document.createElement('div'); st.id = 'studio-' + n;
      st.style.cssText = 'position:absolute;left:0;top:0;z-index:2147483647;background:transparent;';
      // rebuild the ancestor chain (classes only) so scoped CSS still matches
      let wrap = st; const chain = []; let a = src.parentElement;
      while (a && a !== document.body && chain.length < 4) { chain.unshift(a); a = a.parentElement; }
      for (const anc of chain) {
        const d = document.createElement(anc.tagName); d.className = anc.className;
        d.style.cssText = 'position:static;transform:none;overflow:visible;width:auto;height:auto;min-height:0;' +
          'padding:0;margin:0;background:none;border:0;box-shadow:none;display:block;';
        wrap.appendChild(d); wrap = d;
      }
      const c = src.cloneNode(true);
      Object.assign(c.style, { position: 'relative', left: '0', top: '0', transform: 'none', margin: '0' });
      c.style.width = (w || src.getBoundingClientRect().width) + 'px';
      c.setAttribute('data-shot', n); wrap.appendChild(c); document.body.appendChild(st); window.scrollTo(0, 0);
      return true;
    }, [n, sel, w]);
    if (!ok) { console.log('missing', n); continue; }
    await p.locator(`[data-shot="${n}"]`).screenshot({ path: path.join(out, n + '.png'), omitBackground: true });
    await p.evaluate(n => document.getElementById('studio-' + n).remove(), n);
    console.log('ok', n);
  }
  await b.close();
})();
