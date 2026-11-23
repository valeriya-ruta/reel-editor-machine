// Is anything readable outside Instagram's safe area?
//
//     node tools/safezone.js reel-01            # every 0.25 s
//     node tools/safezone.js reel-01 0.1        # finer step
//
// Ruta, 2026-11-17 (RULES.md §3a): on a 1080x1920 reel keep clear of the top
// 220-250 px (username, top icons), the bottom 320-450 px (caption, audio, the
// like/comment/share rail) and 60-130 px each side; the safe area is roughly
// 840 x 1350 in the centre. "Some stickers or elements can go out of the safe
// zones, but anything readable has to be inside."
//
// So this measures *text*, not boxes: it loads reel-NN/index.html in Chromium,
// seeks the GSAP timeline, and takes the rendered extent of every visible text
// run (a Range over the text, so a 1080-wide headline box holding a 600-px
// word counts as 600 px). Decoration (ticks, shapes, photos, grounds) is not
// text and is ignored. A run is visible when it and every ancestor is visible
// with opacity > 0.05.
//
// And her face (Ruta, 2026-11-17: "make sure that nothing is going on her
// face ... They should always go under her chin or behind her head"): with
// work/rNN/face.json from tools/facemap.py, every visible text run AND every
// visible graphic (anything drawn: svg, img, a box with a fill or a border) is
// tested against her head at that moment: the face box, raised to the top of
// her hair. A full-frame takeover ground hides her, so nothing is tested while
// one is up. And no graphic may sit on a visible subtitle. Text is measured by
// its ink (the glyphs' own ascent and descent), not the font's line box.
// Exit code 1 if anything readable sits outside the safe area, anything at all
// touches her head, or a graphic covers a subtitle.
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");
const { chromium } = require("playwright");

const SAFE = { left: 130, right: 950, top: 250, bottom: 1470 };

function measure(t) {
  // (inside measure: page.evaluate ships this one function to the page)
  function inkBox(el, txt, range) {
    const cs = getComputedStyle(el);
    const c = (window.__inkCtx = window.__inkCtx || document.createElement("canvas").getContext("2d"));
    c.font = [cs.fontStyle, cs.fontWeight, cs.fontSize, cs.fontFamily].join(" ");
    const m = c.measureText(txt);
    if (!m.fontBoundingBoxAscent) return null;
    const size = parseFloat(cs.fontSize);
    const stroke = parseFloat(cs.webkitTextStrokeWidth || "0") / 2;
    let y0 = Infinity, y1 = -Infinity;
    for (const f of range.getClientRects()) {
      if (f.width < 1) continue;
      // the content area is centred on the line box the same way for every
      // fragment: its top is fontBoundingBoxAscent above the baseline
      const base = f.top + m.fontBoundingBoxAscent;
      y0 = Math.min(y0, base - m.actualBoundingBoxAscent - stroke);
      y1 = Math.max(y1, base + m.actualBoundingBoxDescent + stroke);
    }
    return isFinite(y0) ? [y0, y1] : null;
  }

  const tl = window.__timelines && window.__timelines["main"];
  if (!tl) return null;
  tl.seek(t, false);
  const out = [];
  const seen = new Set();
  const walker = document.createTreeWalker(document.getElementById("root"), NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const n = walker.currentNode;
    const txt = n.textContent.trim();
    if (!txt) continue;
    const el = n.parentElement;
    if (el.closest("script,style,svg")) continue;
    let ok = true, op = 1;
    for (let e = el; e && e.id !== "root"; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.display === "none" || cs.visibility === "hidden") { ok = false; break; }
      op *= parseFloat(cs.opacity);
    }
    if (!ok || op < 0.05) continue;
    const r = document.createRange();
    r.selectNodeContents(n);
    const b = r.getBoundingClientRect();
    if (b.width < 1 || b.height < 1) continue;
    const owner = el.closest("[id]");
    const key = (owner ? owner.id : "?") + "|" + txt;
    if (seen.has(key)) continue;
    seen.add(key);
    // The range's box is the font's whole content area (e.g. Noto Serif: 1.36 em
    // tall), not the letters. Measure the ink: the glyphs' real ascent and
    // descent for this string, hung from the baseline of each line box.
    const ink = inkBox(el, txt, r);
    out.push({ id: owner ? owner.id : "?", text: txt.slice(0, 36),
               x0: b.left, y0: ink ? ink[0] : b.top, x1: b.right, y1: ink ? ink[1] : b.bottom,
               cap: el.closest(".cap") !== null });
  }
  // graphics: drawn things inside the beats (.g), not full-frame grounds
  let takeover = false;
  const shapes = [];
  for (const el of document.querySelectorAll("#root .g *")) {
    const cs = getComputedStyle(el);
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) continue;
    let ok = true, op = 1;
    for (let e = el; e && e.id !== "root"; e = e.parentElement) {
      const c = getComputedStyle(e);
      if (c.display === "none" || c.visibility === "hidden") { ok = false; break; }
      op *= parseFloat(c.opacity);
    }
    if (!ok || op < 0.05) continue;
    const drawn = el.tagName === "svg" || el.tagName === "IMG" ||
                  (cs.backgroundColor && cs.backgroundColor !== "rgba(0, 0, 0, 0)") ||
                  parseFloat(cs.borderTopWidth) > 0;
    if (!drawn) continue;
    if (r.width >= 1000 && r.height >= 1700) { takeover = true; continue; }
    if (el.closest("svg") && el.tagName !== "svg") continue;
    const owner = el.closest("[id]");
    shapes.push({ id: owner ? owner.id : "?", text: "<" + el.tagName.toLowerCase() + (el.className && el.className.baseVal === undefined ? "." + String(el.className).split(" ")[0] : "") + ">",
                  x0: r.left, y0: r.top, x1: r.right, y1: r.bottom });
  }
  return { texts: out, shapes, takeover };
}

(async () => {
  const reel = process.argv[2].replace(/\/$/, "");
  const step = parseFloat(process.argv[3] || "0.25");
  const html = path.join(__dirname, "..", reel, "index.html");
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  // The hyperframes runtime normally provides the timeline registry and the
  // page pulls GSAP from cdnjs; here the registry is injected and GSAP is
  // served from a local copy of the same version (npm, cached in work/_scratch).
  await page.addInitScript(() => { window.__timelines = window.__timelines || {}; });
  const gsapDir = path.join(__dirname, "..", "work", "_scratch", "gsap");
  const gsapFile = path.join(gsapDir, "package", "dist", "gsap.min.js");
  if (!fs.existsSync(gsapFile)) {
    fs.mkdirSync(gsapDir, { recursive: true });
    execSync("npm pack gsap@3.12.5 --silent && tar xzf gsap-3.12.5.tgz", { cwd: gsapDir });
  }
  await page.route(/gsap(\.min)?\.js/, (route) =>
    route.fulfill({ path: gsapFile, contentType: "application/javascript" }));
  await page.goto("file://" + html);
  await page.waitForFunction(() => !!(window.__timelines && window.__timelines["main"]), null, { timeout: 60000, polling: 250 });
  const dur = await page.evaluate(() => parseFloat(document.getElementById("root").dataset.duration));
  const bad = new Map();
  const nn = reel.split("-").pop();
  const facePath = path.join(__dirname, "..", "work", "r" + nn, "face.json");
  const faces = fs.existsSync(facePath) ? JSON.parse(fs.readFileSync(facePath, "utf8")) : null;
  const faceAt = (t) => {
    if (!faces) return null;
    let best = faces[0];
    for (const f of faces) { if (Math.abs(f.t - t) < Math.abs(best.t - t)) best = f; }
    return best;
  };
  const faceBad = new Map();
  const capBad = new Map();
  for (let t = 0; t <= dur + 1e-6; t = Math.round((t + step) * 1000) / 1000) {
    const m = (await page.evaluate(measure, t)) || { texts: [], shapes: [], takeover: false };
    const caps = m.texts.filter((r) => r.cap);
    const gfx = m.texts.filter((r) => !r.cap).concat(m.shapes);
    for (const c of caps) {
      for (const r of gfx) {
        if (r.x1 > c.x0 && r.x0 < c.x1 && r.y1 > c.y0 - 8 && r.y0 < c.y1) {
          const k = r.id + "|" + r.text;
          if (!capBad.has(k)) capBad.set(k, { t0: t, t1: t, id: r.id, text: r.text, why: ["caption «" + c.text.slice(0, 24) + "» y " + Math.round(c.y0)] });
          else capBad.get(k).t1 = t;
        }
      }
    }
    const f = faceAt(t);
    if (f && !m.takeover) {
      // her head, not just the face box: from the top of her hair (estimated
      // from the eye line and chin) down to the chin
      const [fx0, fb0, fx1, fy1] = f.box;
      const fy0 = Math.min(fb0, Math.round(f.eyes - 0.85 * (f.chin - f.eyes)));
      for (const r of gfx) {
        if (r.x1 > fx0 + 4 && r.x0 < fx1 - 4 && r.y1 > fy0 + 4 && r.y0 < fy1 - 4) {
          const k = r.id + "|" + r.text;
          if (!faceBad.has(k)) faceBad.set(k, { t0: t, t1: t, id: r.id, text: r.text, why: ["face " + fx0 + "-" + fx1 + " x " + fy0 + "-" + fy1] });
          else faceBad.get(k).t1 = t;
        }
      }
    }
    for (const r of m.texts) {
      const why = [];
      if (r.x0 < SAFE.left - 0.5) why.push("left " + Math.round(r.x0));
      if (r.x1 > SAFE.right + 0.5) why.push("right " + Math.round(r.x1));
      if (r.y0 < SAFE.top - 0.5) why.push("top " + Math.round(r.y0));
      if (r.y1 > SAFE.bottom + 0.5) why.push("bottom " + Math.round(r.y1));
      if (!why.length) continue;
      const k = r.id + "|" + r.text + "|" + why.map((w) => w.split(" ")[0]).join(",");
      if (!bad.has(k)) bad.set(k, { t0: t, t1: t, id: r.id, text: r.text, why });
      else bad.get(k).t1 = t;
    }
  }
  await browser.close();
  console.log(`SAFEZONE ${reel}: readable text must sit in x ${SAFE.left}-${SAFE.right}, y ${SAFE.top}-${SAFE.bottom}`);
  const rows = [...bad.values()].sort((a, b) => a.t0 - b.t0);
  for (const v of rows) {
    console.log(`  x ${v.t0.toFixed(2).padStart(6)}-${v.t1.toFixed(2).padStart(6)}  ${v.id.padEnd(8)} ${v.text.padEnd(36)} ${v.why.join(", ")}`);
  }
  if (!rows.length) console.log("  ok  nothing readable outside");
  console.log(`CAPTIONS ${reel}: no graphic may sit on a subtitle`);
  const cr = [...capBad.values()].sort((a, b) => a.t0 - b.t0);
  for (const v of cr) {
    console.log(`  x ${v.t0.toFixed(2).padStart(6)}-${v.t1.toFixed(2).padStart(6)}  ${v.id.padEnd(8)} ${v.text.padEnd(36)} ${v.why.join(", ")}`);
  }
  if (!cr.length) console.log("  ok  no graphic on a subtitle");
  if (faces) {
    console.log(`FACE ${reel}: nothing may touch her face box (work/r${nn}/face.json)`);
    const fr = [...faceBad.values()].sort((a, b) => a.t0 - b.t0);
    for (const v of fr) {
      console.log(`  x ${v.t0.toFixed(2).padStart(6)}-${v.t1.toFixed(2).padStart(6)}  ${v.id.padEnd(8)} ${v.text.padEnd(36)} ${v.why.join(", ")}`);
    }
    if (!fr.length) console.log("  ok  nothing on her face");
    process.exit(rows.length || fr.length || cr.length ? 1 : 0);
  }
  process.exit(rows.length || cr.length ? 1 : 0);
})();
