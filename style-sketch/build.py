# -*- coding: utf-8 -*-
"""Style test — Google x Excalidraw (STYLE.md §0b). Static beats over a still of
her, screenshotted at fixed times by shoot.js. Not a reel."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "tools"))
from sketch import Sketch, sketch_css, SKETCH_JS
sk = Sketch(seed=7)

# NEAR — a Material card above her head, sketched content inside
near = ('<div id="n1" class="g" style="top:0;height:700px">'
        '<div class="gcard" id="n1c" style="left:90px;top:110px;width:900px;height:420px">'
        + sk.svg(900, 420,
                 sk.rect(40, 150, 230, 150, fill="blue") +
                 sk.arrow([(290, 230), (370, 200), (450, 230)]) +
                 sk.ellipse(570, 225, 110, 78, fill="yellow", style="hachure") +
                 sk.arrow([(690, 230), (740, 260), (800, 230)], stroke="red") , sid="n1s") +
        '<div class="gs" style="position:absolute;left:44px;top:40px;font-size:30px;font-weight:700;letter-spacing:.14em;color:#5f6368">ДОДАТОК RUTA</div>'
        '<div class="hand" id="n1a" style="position:absolute;left:62px;top:200px;font-size:44px">голосове</div>'
        '<div class="hand" id="n1b" style="position:absolute;left:500px;top:198px;font-size:44px">сценарій</div>'
        '<div class="num" id="n1n" style="position:absolute;left:790px;top:170px;font-size:96px;color:#34A853">$</div>'
        '</div></div>')

# OVER — the whiteboard, a hand-drawn cost table
board = ('<div id="b1" class="g full" style="opacity:0;visibility:hidden"><div class="board"></div>'
         '<div class="hand" id="b1t" style="position:absolute;left:90px;top:190px;font-size:86px">Витрати на місяць</div>'
         + sk.svg(1080, 1300,
                  sk.underline(90, 300, 640, twice=True) +
                  sk.rect(90, 380, 900, 170) + sk.rect(90, 590, 900, 170) +
                  sk.rect(90, 800, 900, 170, fill="green", style="solid") +
                  sk.circle_around(850, 885, 150, 70) + sk.check(120, 410, 70) , sid="b1s") +
         '<div class="gs" style="position:absolute;left:230px;top:430px;font-size:56px;font-weight:500">Supabase</div>'
         '<div class="num" style="position:absolute;left:760px;top:420px;font-size:76px">$35</div>'
         '<div class="gs" style="position:absolute;left:230px;top:640px;font-size:56px;font-weight:500">Vercel</div>'
         '<div class="num" style="position:absolute;left:760px;top:630px;font-size:76px">$20</div>'
         '<div class="hand" style="position:absolute;left:150px;top:840px;font-size:64px">разом</div>'
         '<div class="num" style="position:absolute;left:760px;top:830px;font-size:96px;color:#EA4335">$55</div>'
         '<div class="dots" id="dots" style="left:440px;top:1080px"><i></i><i></i><i></i><i></i></div>'
         '</div>')

# NEAR again — pills and chips, a search bar typing
chips = ('<div id="c1" class="g" style="top:0;height:700px">'
         '<div class="pill" id="srch" style="left:90px;top:120px;width:900px;height:120px;padding:0 44px;font-size:44px">'
         '<svg width="44" height="44" viewBox="0 0 24 24"><path d="M15.5 14h-.8l-.3-.3A6.5 6.5 0 1 0 14 15.5l.3.3v.8l5 5 1.5-1.5-5-5zm-6 0a4.5 4.5 0 1 1 0-9 4.5 4.5 0 0 1 0 9z" fill="#5f6368"/></svg>'
         '<span id="q" data-text="скільки заробляє додаток"></span></div>'
         '<div style="position:absolute;left:90px;top:300px;display:flex;gap:18px;flex-wrap:wrap;width:900px">'
         '<span class="chip on">Claude $100</span><span class="chip g">Supabase $35</span><span class="chip y">Vercel $20</span><span class="chip r">AI</span></div>'
         + sk.svg(1080, 700, sk.arrow([(860, 470), (900, 560), (820, 640)], stroke="white", sw=6), cls="sk over-plate", sid="c1a") +
         '</div>')

html = """<!DOCTYPE html><html><head><meta charset="utf-8">
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<style>* { margin:0; padding:0; box-sizing:border-box }
#root { position:relative; width:1080px; height:1920px; overflow:hidden; background:#000 }
.plate { position:absolute; inset:0; width:1080px; height:1920px; object-fit:cover }
.g { position:absolute; left:0; width:1080px; opacity:0; visibility:hidden } .g.full { top:0; height:1920px }
.cap { position:absolute; left:0; width:1080px; top:1430px; text-align:center; color:#fff; font-size:90px; font-weight:900 }
%s</style></head><body><div id="root"><img class="plate" src="assets/still.jpg">%s%s%s
<div class="cap" id="cap">СКІЛЬКИ</div></div>
<script>%s
var tl = gsap.timeline({paused:true}); var h = sketchHelpers(tl);
h.pop("#n1", 0.2, {s:1, r:0, y:0}); h.pop("#n1c", 0.2); h.draw("#n1s", 0.5, 1.8);
h.write("#n1a", 0.7, 0.5); h.write("#n1b", 1.6, 0.5); h.pop("#n1n", 2.2);
h.fadeOut("#n1", 3.0);
h.boardIn("#b1", 3.2, 540, 300); h.write("#b1t", 3.8, 0.8); h.draw("#b1s", 4.0, 2.4); h.think("#dots", 5, 1.5);
h.boardOut("#b1", 7.0, 540, 1000);
h.pop("#c1", 7.4, {s:1,r:0,y:0}); h.pop("#srch", 7.4); h.type("#q", 7.7, 18); h.draw("#c1a", 9, 0.5);
window.tl = tl; document.fonts.ready.then(function(){ window.ready = true; });
</script></body></html>""" % (sketch_css(), near, board, chips, SKETCH_JS)
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(html)
print("ok")
