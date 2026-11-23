# -*- coding: utf-8 -*-
"""Instagram cover for reel 12 — her «Тадааам» frame, cut out, on the burgundy
ground, her caption's words as the title, the three marks on a glass shelf.
Key content sits inside the centre 1080x1440 so the profile grid's 3:4 crop
keeps it.   python build.py && ../../hf snapshot --at 0.5 -o out"""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools"))
from glass import Glass
g = Glass(["claude", "openai"])
claude, openai = g.mark("claude"), g.mark("openai")
wall_marks = ["instagram", "facebook", "tiktok", "youtube", "meta", "googleanalytics", "linkedin", "pinterest", "threads", "telegram"]
g2 = Glass(wall_marks)
tiles = []
k = 0
for j in range(-1, 16):
    for i in range(-1, 9):
        x, y = 34 + i * 128 + (64 if j % 2 else 0), 20 + j * 128
        tiles.append('<div class="wt" style="left:%dpx;top:%dpx">%s</div>' % (x, y, g2.mark(wall_marks[(i * 3 + j * 7) % len(wall_marks)], "wm")))
CSS = """
@font-face { font-family: "ProductSans"; src: url("assets/fonts/ProductSans-Black.woff") format("woff"); font-weight: 900; }
* { margin:0; padding:0; box-sizing:border-box; }
#root { position:relative; width:1080px; height:1920px; overflow:hidden; font-family:"ProductSans"; }
#wall { position:absolute; inset:0; opacity:0.16; }
.wt { position:absolute; width:100px; height:100px; border-radius:23px;
  background:linear-gradient(158deg, rgba(255,255,255,0.30), rgba(255,255,255,0.08));
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.6); display:flex; align-items:center; justify-content:center; }
.wm { width:48px; height:48px; fill:#fff; }
#fade { position:absolute; inset:0; background: radial-gradient(ellipse 70% 55% at 50% 52%, rgba(40,4,14,0) 0%, rgba(40,4,14,0.55) 100%); }
#her { position:absolute; left:50px; top:-120px; width:1242px; height:2208px; }
#herGlow { position:absolute; left:230px; top:420px; width:800px; height:800px; border-radius:50%;
  background: radial-gradient(circle, rgba(255,110,156,0.45) 0%, rgba(255,110,156,0) 62%); }
.title { position:absolute; left:66px; width:900px; text-align:left; font-weight:900; line-height:0.92; letter-spacing:-0.035em; }
#t1 { top:262px; font-size:94px; color:#fff; }
#t2 { top:356px; font-size:94px; background:linear-gradient(100deg,#ffd0de 0%,#ff6e9c 55%,#ff9fbd 100%);
  -webkit-background-clip:text; background-clip:text; color:transparent; }
#shelfWrap { position:absolute; left:120px; top:1410px; width:840px; height:230px; }
#shelf { inset:0; border-radius:70px; }
.tile { position:absolute; top:30px; width:170px; height:170px; }
#cab { position:absolute; left:0; top:0; width:840px; height:230px; overflow:visible; }
"""
HTML = u"""<!DOCTYPE html><html lang="uk"><head><meta charset="utf-8"><title>Cover 12</title>
<style>%(glass)s%(css)s</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920" data-duration="1" data-fps="30">
%(defs)s%(defs2)s
<div class="tkg"></div><div class="aur a1"></div><div class="aur a2"></div><div class="aur a3"></div>
<div id="wall">%(tiles)s</div>
<div id="fade"></div>
<div class="title" id="t1">АВТОМАТИЗАЦІЯ</div>
<div class="title" id="t2">СММ-ЗВІТНОСТІ</div>
<div id="herGlow"></div>
<img id="her" src="assets/her.png" alt="">
<div id="shelfWrap">
  <div class="shelf edge" id="shelf"></div>
  <svg id="cab" viewBox="0 0 840 230" class="cab">
    <path class="tube" d="M 225 115 C 280 150 340 150 335 115"/><path class="core" d="M 225 115 C 280 150 340 150 335 115"/>
    <path class="tube" d="M 505 115 C 560 150 620 150 615 115"/><path class="core" d="M 505 115 C 560 150 620 150 615 115"/>
  </svg>
  <div class="tile" style="left:50px"><div class="pearl"><span class="wmark" style="font-size:108px">w<i>.</i></span></div></div>
  <div class="tile" style="left:335px"><div class="jelly">%(claude)s</div></div>
  <div class="tile" style="left:620px"><div class="jelly">%(openai)s</div></div>
</div>
<div class="grain"></div>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script>window.__timelines["main"] = gsap.timeline({paused:true});</script>
</body></html>"""
html = HTML % {"glass": g.css(), "css": CSS, "defs": g.defs(), "defs2": g2.defs(), "tiles": "".join(tiles), "claude": claude, "openai": openai}
io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(html)
print("ok")
