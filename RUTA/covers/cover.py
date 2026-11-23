# -*- coding: utf-8 -*-
"""One Instagram cover per reel, all from the recipe of the approved reel-12
cover: her, cut out of a hype frame, on the burgundy ground with a faint wall of
marks; a two-line title in her own words; the reel's hero objects on a glass
shelf and/or as extras. Key content stays inside the centre 1080x1440, which is
what the profile grid shows.

    python covers/cover.py 13      # reads covers/reel-13/spec.json, writes index.html
    cd covers/reel-13 && ../../hf snapshot --at 0.5 --no-end -o out
"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from glass import Glass  # noqa: E402

WALL = ["instagram", "facebook", "tiktok", "youtube", "meta", "googleanalytics",
        "linkedin", "pinterest", "threads", "telegram", "notion", "canva"]

BASE_CSS = """
@font-face { font-family: "ProductSans"; src: url("assets/fonts/ProductSans-Black.ttf"); font-weight: 900; }
* { margin:0; padding:0; box-sizing:border-box; }
#root { position:relative; width:1080px; height:1920px; overflow:hidden; font-family:"ProductSans"; }
#wall { position:absolute; inset:0; opacity:0.15; }
.wt { position:absolute; width:100px; height:100px; border-radius:23px;
  background:linear-gradient(158deg, rgba(255,255,255,0.30), rgba(255,255,255,0.08));
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.6); display:flex; align-items:center; justify-content:center; }
.wm { width:48px; height:48px; fill:#fff; }
#fade { position:absolute; inset:0; background: radial-gradient(ellipse 70% 55% at 50% 52%, rgba(40,4,14,0) 0%, rgba(40,4,14,0.55) 100%); }
#her { position:absolute; }
#herGlow { position:absolute; width:800px; height:800px; border-radius:50%;
  background: radial-gradient(circle, rgba(255,110,156,0.45) 0%, rgba(255,110,156,0) 62%); }
.title { position:absolute; font-weight:900; line-height:0.92; letter-spacing:-0.035em; white-space:nowrap; }
.t1 { color:#fff; }
/* solid, not background-clip:text — Chrome drops the breve of Й (and the dots
   of Ї) from gradient-clipped text even with headroom; seen on the reel-15 cover */
.t2 { color:#ff86ad; }
.shelfWrap { position:absolute; }
.shelfWrap .shelf { inset:0; border-radius:70px; }
.tile { position:absolute; top:30px; width:170px; height:170px; }
.cab { position:absolute; left:0; top:0; overflow:visible; }
.chipx { position:absolute; display:flex; align-items:center; gap:12px; height:96px; padding:0 36px;
  border-radius:48px; color:#fff; font-weight:900; font-size:54px; letter-spacing:-0.02em; }
"""


def tile_inner(g, t):
    kind, what = t[0], t[1]
    size = t[2] if len(t) > 2 else None
    if kind == "word":      # pearl tile with an ink wordmark (Windsor «w.», RUTA)
        return '<div class="pearl"><span class="wmark" style="font-size:%dpx">%s</span></div>' % (size or 108, what)
    if kind == "jword":     # jelly tile with a white wordmark
        return '<div class="jelly"><span class="wmark" style="font-size:%dpx">%s</span></div>' % (size or 60, what)
    return '<div class="%s">%s</div>' % (kind, g.mark(what))   # clear / pearl / jelly + a mark


def build(n, spec):
    g = Glass(spec.get("marks", []))
    tiles = spec.get("tiles", [])
    step = 285
    tiles_html, cab = [], []
    for i, t in enumerate(tiles):
        tiles_html.append('<div class="tile" style="left:%dpx">%s</div>' % (50 + i * step, tile_inner(g, t)))
        if i:
            x0, x1 = 50 + (i - 1) * step + 175, 50 + i * step - 5
            d = "M %d 115 C %d 150 %d 150 %d 115" % (x0, x0 + 55, x1 - 55, x1)
            cab.append('<path class="tube" d="%s"/><path class="core" d="%s"/>' % (d, d))
    shelf = ""
    if tiles:
        w = 100 + len(tiles) * 170 + (len(tiles) - 1) * 115
        shelf = ('<div class="shelfWrap" style="left:%dpx;top:%dpx;width:%dpx;height:230px">'
                 '<div class="shelf edge"></div>'
                 '<svg class="cab" viewBox="0 0 %d 230" style="width:%dpx;height:230px">%s</svg>%s</div>'
                 % ((1080 - w) // 2, spec.get("shelf_top", 1410), w, w, w, "".join(cab), "".join(tiles_html)))
    gw = Glass(WALL)
    wall = []
    for j in range(-1, 16):
        for i in range(-1, 9):
            x, y = 34 + i * 128 + (64 if j % 2 else 0), 20 + j * 128
            wall.append('<div class="wt" style="left:%dpx;top:%dpx">%s</div>'
                        % (x, y, gw.mark(WALL[(i * 3 + j * 7) % len(WALL)], "wm")))
    her, t = spec["her"], spec["title"]
    size = t.get("size", 94)
    extra = spec.get("front", "")
    for name in spec.get("front_marks", []):
        extra = extra.replace("{%s}" % name, g.mark(name))
    html = u"""<!DOCTYPE html><html lang="uk"><head><meta charset="utf-8"><title>Cover %(n)s</title>
<style>%(glass)s%(css)s
.t1 { left:%(tl)dpx; top:%(t1y)dpx; font-size:%(ts)dpx; } .t2 { left:%(tl)dpx; top:%(t2y)dpx; font-size:%(ts)dpx; }
#her { left:%(hx)dpx; top:%(hy)dpx; width:%(hw)dpx; height:%(hh)dpx; }
#herGlow { left:%(gx)dpx; top:%(gy)dpx; }
%(extra_css)s</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="1" data-fps="30">
%(defs)s%(defs2)s
<div class="tkg"></div><div class="aur a1"></div><div class="aur a2"></div><div class="aur a3"></div>
<div id="wall">%(wall)s</div><div id="fade"></div>
%(behind)s
<div class="title t1">%(l1)s</div><div class="title t2">%(l2)s</div>
<div id="herGlow"></div>
<img id="her" src="assets/her.png" alt="">
%(front)s
%(shelf)s
<div class="grain"></div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script>window.__timelines["main"] = gsap.timeline({paused:true});</script>
</body></html>""" % {
        "n": n, "glass": g.css(), "css": BASE_CSS, "defs": g.defs(), "defs2": gw.defs(),
        "wall": "".join(wall), "tl": t.get("left", 66), "t1y": t.get("top", 262),
        "t2y": t.get("top", 262) + size, "ts": size, "l1": t["l1"], "l2": t["l2"],
        "hx": her["x"], "hy": her["y"], "hw": int(1080 * her["s"]), "hh": int(1920 * her["s"]),
        "gx": her["x"] + int(540 * her["s"]) - 400, "gy": her["y"] + int(800 * her["s"]) - 400,
        "extra_css": spec.get("css", ""), "behind": spec.get("behind", ""), "front": extra,
        "shelf": shelf}
    io.open(os.path.join(ROOT, "covers", "reel-%s" % n, "index.html"), "w", encoding="utf-8").write(html)


if __name__ == "__main__":
    n = sys.argv[1]
    spec = json.load(io.open(os.path.join(ROOT, "covers", "reel-%s" % n, "spec.json"), encoding="utf-8"))
    build(n, spec)
    print("ok", n)
