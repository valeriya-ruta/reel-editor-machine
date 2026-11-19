// Stills of the composition at chosen times, over the real plate frame.
//
//     node tools/frames.js reel-01 3.5 12 61.5        # -> work/r01/frames/t003.50.jpg ...
//     node tools/frames.js reel-01 --beats            # one still per beat, mid-beat, + a sheet
//
// Faster than a render for checking a layout: the plate frame at t comes from
// ffmpeg (base.mp4, so a baked half-screen shows as it will), the graphics
// from the page with the GSAP timeline seeked to t. Same local GSAP and
// timeline registry as tools/safezone.js.
const fs = require("fs");
const path = require("path");
const { execFileSync, execSync } = require("child_process");
const { chromium } = require("playwright");

(async () => {
  const reel = process.argv[2].replace(/\/$/, "");
  const root = path.join(__dirname, "..");
  const nn = reel.split("-").pop();
  const html = path.join(root, reel, "index.html");
  const plate = path.join(root, reel, "assets", "base.mp4");
  const out = path.join(root, "work", "r" + nn, "frames");
  fs.mkdirSync(out, { recursive: true });
  let times = process.argv.slice(3).filter((a) => !a.startsWith("--")).map(parseFloat);
  const src = fs.readFileSync(html, "utf8");
  const labels = {};
  if (process.argv.includes("--beats")) {
    // mid-point of every beat's show/hide pair, plus a late point for the long ones
    const on = {}, off = {};
    for (const m of src.matchAll(/tl\.set\("#(b\d+)", \{autoAlpha: 1\}, ([\d.]+)\)/g)) on[m[1]] = parseFloat(m[2]);
    for (const m of src.matchAll(/tl\.set\("#(b\d+)", \{autoAlpha: 0\}, ([\d.]+)\)/g)) off[m[1]] = parseFloat(m[2]);
    for (const b of Object.keys(on)) {
      const a = on[b], z = off[b] || a + 1;
      const t = Math.round((a + (z - a) * 0.8) * 30) / 30;
      times.push(t);
      labels[t.toFixed(2)] = b;
    }
    times.sort((x, y) => x - y);
  }
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.addInitScript(() => { window.__timelines = window.__timelines || {}; });
  const gsapFile = path.join(root, "work", "_scratch", "gsap", "package", "dist", "gsap.min.js");
  await page.route(/gsap(\.min)?\.js/, (route) => route.fulfill({ path: gsapFile, contentType: "application/javascript" }));
  await page.goto("file://" + html);
  await page.waitForFunction(() => !!(window.__timelines && window.__timelines["main"]), null, { timeout: 60000, polling: 250 });
  await page.addStyleTag({ content: "#vid, video { visibility: hidden !important; } #root { background-size: cover !important; }" });
  const shots = [];
  for (const t of times) {
    const png = path.join(out, "_plate.png");
    execFileSync("ffmpeg", ["-nostdin", "-v", "error", "-y", "-ss", t.toFixed(3), "-i", plate, "-frames:v", "1", png]);
    const b64 = fs.readFileSync(png).toString("base64");
    await page.evaluate(([t, b64]) => {
      document.getElementById("root").style.backgroundImage = "url(data:image/png;base64," + b64 + ")";
      window.__timelines["main"].seek(t, false);
    }, [t, b64]);
    const f = path.join(out, "t" + t.toFixed(2).padStart(6, "0") + ".jpg");
    await page.screenshot({ path: f, type: "jpeg", quality: 85, clip: { x: 0, y: 0, width: 1080, height: 1920 } });
    shots.push([t, f]);
  }
  await browser.close();
  if (process.argv.includes("--beats") || times.length > 1) {
    // contact sheet: 8 across at 270x480, the time (and beat) burnt in
    const list = path.join(out, "_list.txt");
    const per = 8;
    const sheets = [];
    for (let i = 0; i < shots.length; i += per * 3) {
      const chunk = shots.slice(i, i + per * 3);
      const args = [];
      chunk.forEach(([t, f]) => args.push("-i", f));
      const n = chunk.length;
      const lab = chunk.map(([t], j) => `[${j}:v]scale=270:480,drawtext=text='${(labels[t.toFixed(2)] || "") + " " + t.toFixed(2)}':x=6:y=6:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6[v${j}]`).join(";");
      const cols = Math.min(per, n), rows = Math.ceil(n / per);
      const layout = chunk.map((_, j) => `${(j % per) * 270}_${Math.floor(j / per) * 480}`).join("|");
      const sheet = path.join(out, `sheet_${String(sheets.length + 1).padStart(2, "0")}.jpg`);
      execFileSync("ffmpeg", ["-nostdin", "-v", "error", "-y", ...args, "-filter_complex",
        `${lab};${chunk.map((_, j) => `[v${j}]`).join("")}xstack=inputs=${n}:layout=${layout}:fill=black`,
        "-frames:v", "1", "-q:v", "3", sheet]);
      sheets.push(sheet);
    }
    console.log(sheets.join("\n"));
  } else {
    console.log(shots.map((s) => s[1]).join("\n"));
  }
})();
