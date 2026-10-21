# -*- coding: utf-8 -*-
"""Build the 8 lead-magnet reels as HyperFrames pages (1080x1920).

    python3 leadmagnet/reels/rbuild.py [k ...]   -> reels/rNN/index.html + parts/

Layers, bottom to top: her vertical plate; the takeover (white dot-grid paper
carrying lv.mp4, the long video's own graphics for these words); the hook
card; her usual captions (one word, uppercase, 90px, white on the underlay,
ink over the paper); the full-screen CTA card after her last word.
"""
import json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LM = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from rlv import lv_time, KIND  # noqa: E402

FPS, PART, CTA = 30, 10, 3.6
W = json.load(open(os.path.join(HERE, "words.json")))

HOOK = {1: "Ти переплачуєш за Higgsfield", 2: "Як змусити AI змонтувати рілс як у того блогера",
        3: "Чому твої AI-каруселі виглядають як слоп", 4: "Останні 30 моїх рілсів монтувала не я",
        5: "Чому AI ставить текст під кнопки Instagram", 6: "Як зібрати мудборд, який AI зрозуміє",
        7: "Що таке .md — простими словами", 8: "Claude сам знайшов і вирізав картинки для мого відео"}
CTAK = {1: "dyz", 2: "dyz", 3: "dyz", 4: "dyz", 5: "dyz", 6: "dyz", 7: "sub", 8: "sub"}
# takeover windows, in long-video seconds (where the graphic is on screen there)
TK = {1: [(742.0, 755.0), (764.8, 779.0), (785.0, 796.8)],
      2: [(950.4, 958.8), (980.8, 991.8), (992.4, 1012.0), (1021.4, 1040.5), (1057.5, 1078.0), (1082.0, 1087.0), (1099.4, 1105.3)],
      3: [(389.5, 418.7)], 4: [(13.0, 35.7)], 5: [(258.5, 288.0)],
      6: [(552.0, 592.4), (606.0, 666.5)], 7: [(99.4, 139.2)], 8: [(811.0, 831.0), (841.5, 858.5)]}

FIX = {"етелектом.": "інтелектом.", "телек": "інтелект", "щитує": "зчитує", "Хіксфілд,": "Higgsfield,",
       "нанобанани,": "Nano Banana,", "клінг,": "Kling,", "абіз'яна": "мавпа", "клад-код.": "Claude Code.",
       "клад-коді.": "Claude Code.", "SaveAsbot.": "SaveAsBot.", "пром.": "промт.", "пром": "промт",
       "Субтитери": "Субтитри", "клієнки,": "клієнтки,", "свої": "своєї", "Reels'ю": "рілсах", "часини,": "частини,",
       "субтитру": "субтитри", "польщу": "постю", "побранштормали,": "побрейнштормили,", "Єтнамі,": "В'єтнамі,",
       "скраббук,": "скрапбук,", "Джейсоном,": "JSON-ом,", "Пайтоном,": "Python-ом,", "отай": "отакий",
       "Клод,": "Claude,", "Клод": "Claude", "Клоду,": "Claude,", "чимене,": "мене,", "віду": "відео",
       "впромт,": "в промт,", "опендраутер,": "OpenRouter,", "осюди.": "отут."}


def segs(k):
    return json.load(open(os.path.join(HERE, "r%02d" % k, "cut.json")))


def src_to_reel(cut, t):
    best = None
    for s in cut["segments"]:
        a, d = s["src"], s["nf"] / FPS
        if a <= t < a + d:
            return s["out"] / FPS + (t - a)
        if t < a and best is None:
            best = s["out"] / FPS            # inside a squeezed pause: snap forward
    return best


def captions(k, cut):
    ws = []
    for a, b in cut["ranges"]:
        for i in range(a, b + 1):
            w, s, e = W[i]
            if re.fullmatch(r"[–—-]+", w):
                continue
            rs = src_to_reel(cut, s + 0.03)
            if rs is None:
                continue
            if ws and (w.startswith("-") or w.startswith("'") or w == "%" or (ws[-1]["w"] == "Save" and w.startswith("Asbot"))):
                ws[-1]["w"] += w if not ws[-1]["w"] == "Save" else w.replace("Asbot", "asBot")
                continue
            ws.append({"w": w, "s": rs})
    D = cut["duration"]
    for i, c in enumerate(ws):
        c["w"] = FIX.get(c["w"], c["w"])
        nxt = ws[i + 1]["s"] if i + 1 < len(ws) else D
        c["e"] = min(nxt - 0.085, c["s"] + 1.2)
        if c["e"] <= c["s"]:
            c["e"] = c["s"] + 0.08
    return ws


def windows(k, D):
    spans, cur = [], None
    t = 0.0
    while t < D:
        lt = lv_time(k, t)
        on = lt is not None and any(a <= lt < b for a, b in TK[k]) and t > 2.4
        if on and cur is None:
            cur = [t, t]
        if on:
            cur[1] = t + 0.05
        if not on and cur is not None:
            spans.append(cur); cur = None
        t += 0.05
    if cur:
        spans.append(cur)
    merged = []
    for a, b in spans:
        if merged and a - merged[-1][1] < 0.8:
            merged[-1][1] = b
        else:
            merged.append([a, b])
    # her rule: the graphic owns the frame, then she does; never one long wall
    out = []
    for a, b in merged:
        b = min(b, D - 0.3)
        while b - a > 11.0:
            out.append((a, a + 8.0))
            a += 11.0
        if b - a > 3.0:
            out.append((a, b))
    return [(round(a, 2), round(b, 2)) for a, b in out]


PAGE = open(os.path.join(HERE, "page.html")).read()


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(k):
    d = os.path.join(HERE, "r%02d" % k)
    cut = segs(k)
    V = cut["duration"]
    D = round((cut["frames"] + int(CTA * FPS)) / FPS, 4)
    caps = captions(k, cut)
    tks = windows(k, V)
    kind = KIND[k]
    inv = lambda t: any(a <= t < b for a, b in tks)
    caphtml = "\n".join('<div class="cap%s" id="cap%d">%s</div>' % (" inv" if inv(c["s"]) else "", i, esc(c["w"].upper()))
                        for i, c in enumerate(caps))
    js = []
    for i, c in enumerate(caps):
        js.append('tl.set("#cap%d",{autoAlpha:1},%.3f);tl.set("#cap%d",{autoAlpha:0},%.3f);' % (i, c["s"], i, c["e"]))
    js.append('tl.to("#scrim",{autoAlpha:1,duration:0.3},0);tl.to("#scrim",{autoAlpha:0,duration:0.3},%.3f);' % (V - 0.1))
    sfx = [(0.15, "pop")]
    for a, b in tks:
        js.append('tl.to("#scrim",{autoAlpha:0,duration:0.15},%.3f);tl.to("#scrim",{autoAlpha:1,duration:0.2},%.3f);' % (a - 0.15, b))
        js.append('LM.flash(tl,%.3f,0.85);tl.set("#tk",{autoAlpha:1},%.3f);tl.fromTo("#tkin",{y:70,scale:0.96},{y:0,scale:1,duration:0.5,ease:"power3.out",immediateRender:false},%.3f);'
                  'tl.to("#tk",{autoAlpha:0,duration:0.25},%.3f);' % (a, a, a, b - 0.25))
        sfx += [(a - 0.2, "whoosh")]
    js.append('LM.pop(tl,"#hook",0.15,0.6);tl.to("#hook",{autoAlpha:0,y:-30,duration:0.35},2.75);')
    # CTA
    js.append('LM.flash(tl,%.3f,0.9);tl.set("#cta",{autoAlpha:1},%.3f);' % (V, V))
    if CTAK[k] == "dyz":
        js.append('LM.rise(tl,"#c1",%.3f,0.5);LM.pop(tl,"#c2",%.3f,0.6);LM.rise(tl,"#c3",%.3f,0.5);'
                  'LM.ex(tl,%.3f,"ellipse",[540,790,920,250],{stroke:"#a81428",strokeWidth:5,roughness:1.8,dur:0.7});' % (V + 0.15, V + 0.45, V + 0.9, V + 0.7))
    else:
        js.append('LM.rise(tl,"#c1",%.3f,0.5);LM.rise(tl,"#c2",%.3f,0.5);'
                  'LM.ex(tl,%.3f,"arrow",[540,820,540,1010],{stroke:"#a81428",strokeWidth:5,bend:0,dur:0.5});' % (V + 0.15, V + 0.5, V + 0.9))
    sfx += [(V - 0.2, "whoosh"), (V + 0.45, "pop")]
    if k == 4:
        lt = [c for c in caps if c["w"].startswith("10")]
        if lt:
            t = lt[0]["s"]
            js.append('LM.pop(tl,"#x4",%.3f);tl.to("#x4",{autoAlpha:0,duration:0.3},%.3f);' % (t, t + 3.2))
            sfx.append((t, "pop"))
    extra = '<div id="x4" class="hook" style="top:300px;opacity:0"><span class="dot"></span>10–15 рілсів на тиждень</div>' if k == 4 else ""
    if kind == "theory":
        lv = '<video id="lv" class="clip" src="lv.mp4" data-start="0" data-duration="%.4f" data-media-start="0" muted playsinline style="left:0;top:290px;width:1080px;height:878px"></video>' % V
        ground = '<div class="paper" style="background-position:0 290px"></div>'
    else:
        lv = '<div class="win"><video id="lv" class="clip" src="lv.mp4" data-start="0" data-duration="%.4f" data-media-start="0" muted playsinline style="left:0;top:0;width:1080px;height:828px"></video></div>' % V
        ground = '<div class="desk"></div>'
    if CTAK[k] == "dyz":
        cta = ('<div id="c1" class="ct1">Напиши</div><div id="c2" class="ct2">ДИЗАЙН</div>'
               '<div id="c3" class="ct3">у коментарях —<br>надішлю повне відео з промтами</div>')
    else:
        cta = ('<div id="c1" class="ct2" style="top:520px;font-size:150px;color:#1a1e27">Підписуйся</div>'
               '<div id="c2" class="ct3" style="top:720px">тут більше про AI для контенту</div>')
    html = PAGE % dict(D=D, V=V, lv=lv, ground=ground, caps=caphtml, js="\n".join(js), hook=esc(HOOK[k]),
                       cta=cta, extra=extra, plate="plate.mp4")
    open(os.path.join(d, "index.html"), "w").write(html)
    json.dump({"duration": D, "voice": V, "takeovers": tks, "sfx": sfx}, open(os.path.join(d, "reel.json"), "w"), indent=1)
    # parts
    pd = os.path.join(d, "parts")
    nf = round(D * FPS)
    for k2 in range(-(-nf // (PART * FPS))):
        f0, f1 = k2 * PART * FPS, min(nf, (k2 + 1) * PART * FPS)
        off, pdur = f0 / FPS, (f1 - f0) / FPS
        root = ('const root=gsap.timeline({paused:true});root.add(tl.tweenFromTo(%.4f,%.4f,{ease:"none",duration:%.4f}),0);'
                'window.__timelines["main"]=root;' % (off, off + pdur, pdur))
        pg = html.replace('window.__timelines["main"] = tl;', root)
        pg = re.sub(r'data-media-start="([0-9.]+)"', lambda m: 'data-media-start="%.4f"' % (float(m.group(1)) + off), pg)
        pg = re.sub(r'data-duration="[0-9.]+"', 'data-duration="%.4f"' % pdur, pg)
        if off >= V - 0.05:          # a CTA-only part: the footage has run out
            pg = re.sub(r'<video id="(plate|lv)"[^>]*></video>', '', pg)
        q = os.path.join(pd, "p%02d" % k2)
        os.makedirs(q, exist_ok=True)
        ip = os.path.join(q, "index.html")
        if not (os.path.exists(ip) and open(ip).read() == pg):   # unchanged parts keep their render
            open(ip, "w").write(pg)
        for f in ("hyperframes.json", "package.json"):
            shutil.copy(os.path.join(LM, "hf", f), q)
        json.dump({"id": "lmr%d-%d" % (k, k2), "name": "lmr%d-%d" % (k, k2)}, open(os.path.join(q, "meta.json"), "w"))
        for ln, tgt in (("assets", os.path.join(LM, "hf", "assets")), ("plate.mp4", os.path.join(d, "plate.mp4")), ("lv.mp4", os.path.join(d, "lv.mp4"))):
            p = os.path.join(q, ln)
            if os.path.lexists(p):
                os.remove(p)
            os.symlink(tgt, p)
    for ln, tgt in (("assets", os.path.join(LM, "hf", "assets")),):
        p = os.path.join(d, ln)
        if not os.path.lexists(p):
            os.symlink(tgt, p)
    for f in ("hyperframes.json", "package.json"):
        shutil.copy(os.path.join(LM, "hf", f), d)
    json.dump({"id": "lmr%d" % k, "name": "lmr%d" % k}, open(os.path.join(d, "meta.json"), "w"))
    print("r%02d  %.1fs  takeovers %s  caps %d" % (k, D, tks, len(caps)))


if __name__ == "__main__":
    for k in [int(a) for a in sys.argv[1:]] or sorted(HOOK):
        build(k)
