# -*- coding: utf-8 -*-
"""Lead magnet: write one HyperFrames project per beat.

    python3 leadmagnet/build.py            # all beats -> leadmagnet/beats/<id>/
    python3 leadmagnet/build.py b04 b05    # just these

A beat is a window [t0, t1] of the cut plate (output seconds) that gets
graphics. Outside the beats the plate plays as is. Each beat carries its own
slice of the plate as <video id=cam>, starts and ends on the full-frame
camera, so the renders drop back into the plate without a seam.
"""
import json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get("LM_SRC", "/home/user/lm-src")
PLATE = os.path.join(SRC, "plate_v.mp4")
REELS = os.path.join(SRC, "reels")
OUT = os.path.join(HERE, "beats")
FPS = 30
PART = 15          # seconds per render part

BEATS = []


def beat(id, t0, t1, bg="paper", cin=False, cout=False):
    """cin/cout: the beat starts/ends already on the screen layout (camera in
    the circle, desktop up) so two screen beats butt-join on a tab switch."""
    def deco(fn):
        BEATS.append(dict(id=id, t0=t0, t1=t1, bg=bg, fn=fn, cin=cin, cout=cout))
        return fn
    return deco


# ===================================================================== markup
BOOKMARKS = [("IG inbox", "#e1306c"), ("Monobank", "#222"), ("Docs", "#4285f4"), ("Meet", "#00897b"),
             ("YouTube", "#ff0000"), ("Wayforpay", "#2c5fd8"), ("ФОП Аксена Валерія", "#21a038"),
             ("SendPulse", "#0aa0c8"), ("RUTA app", "#111"), ("Ruta PRO app", "#111"), ("Local Whisper", "#f08c00")]

TABCOL = {"Claude": "#d97757", "Pinterest": "#e60023", "OpenRouter": "#6467f2", "Telegram": "#2aabee",
          "Instagram": "#e1306c", "Drive": "#1fa463", "Claude Code": "#d97757"}


def chrome(tabs, active, url):
    t = []
    for i, name in enumerate(tabs):
        on = " on" if name == active else ""
        label = {"Claude": "New chat - Claude", "Claude Code": "Claude Code", "Pinterest": "Pinterest",
                 "OpenRouter": "Models | OpenRouter", "Telegram": "Telegram Web", "Instagram": "Instagram"}.get(name, name)
        t.append(f'<div class="tab{on}" data-tab="{name}" style="left:{12 + i * 318}px">'
                 f'<i class="fav" style="background:{TABCOL.get(name, "#999")}"></i>{label}<span class="x">✕</span></div>')
    bm = "".join(f'<span><i style="background:{c}"></i>{n}</span>' for n, c in BOOKMARKS)
    ext = "".join(f'<i style="background:{c}"></i>' for c in ["#d97757", "#f4b400", "#5f6368", "#7b61ff", "#0f9d58", "#5f6368"])
    return f'''<div class="chrome"><div class="tabs">{"".join(t)}</div>
  <div class="urlrow"><span class="nav">←</span><span class="nav">→</span><span class="nav">↻</span>
  <div class="omni"><span id="url">{url}</span></div><div class="ext">{ext}</div>
  <div class="prof"><b>V</b>Work</div></div>
  <div class="bmarks">{bm}</div></div>'''


def taskbar(clock="18:24"):
    icons = "".join(f'<i style="background:{c}"></i>' for c in ["#0078d4", "#f4b400", "#2aabee", "#4285f4", "#d97757", "#e60023"])
    return f'''<div class="taskbar"><div class="wx">29°C<br>Mostly cloudy</div><div class="mid">{icons}</div>
  <div class="clock">{clock}<br>15.10.2026</div></div>'''


def screen(page_html, tabs, active, url, clock="18:24"):
    return f'''<div id="scrwrap"><div id="scr">{chrome(tabs, active, url)}<div class="page">{page_html}</div>{taskbar(clock)}</div>
  <svg id="cur" viewBox="0 0 30 40"><path d="M3 3 L3 31 L10 24.5 L15 35 L19.5 33 L14.6 22.8 L24 22.8 Z" fill="#111" stroke="#fff" stroke-width="2.2" stroke-linejoin="round"/></svg>
  <div class="ripple" id="rip"></div></div>'''


def claude_side(active=None, extra_today=None):
    items = [("New", "+"), ("Projects", None), ("Artifacts", None), ("Scheduled", None), ("Design", None), ("Customize", None), ("More", None)]
    s = ['<div class="side"><div class="logo">Claude</div>']
    for n, _ in items:
        nb = ' <span class="newb">New</span>' if n == "Projects" else ""
        on = " on" if n == active else ""
        s.append(f'<div class="si{on}" data-si="{n}"><i></i>{n}{nb}</div>')
    s.append('<div class="lbl">Pinned</div>')
    for n in ["AI Content System", "Multiversity", "Ruta · content-friend app"]:
        s.append(f'<div class="si"><i style="border-radius:50%"></i>{n}</div>')
    s.append('<div class="lbl">Today</div>')
    today = (extra_today or []) + ["Prushak storytelling", "Lanolin lip balm in Vietnam"]
    for i, n in enumerate(today):
        on = " on" if extra_today and i == 0 else ""
        s.append(f'<div class="si{on}" style="padding-left:14px">{n}</div>')
    s.append('<div class="user"><b>R</b><div>Ruta <small>· Max</small></div></div></div>')
    return "".join(s)


def claude_home(placeholder="How can I help you today?", active="New"):
    return f'''<div class="cl">{claude_side(active)}<div class="main">
  <div class="hello"><span class="ast">✻</span>Back at it, Ruta</div>
  <div class="box" id="box" style="top:310px"><span class="ph" id="ph">{placeholder}</span><span id="typed"></span><div id="atts"></div>
    <div class="tools">+</div><div class="model">Opus 5.5</div><div class="send">↑</div></div></div></div>'''


def ds_preview():
    """Her real design system (RUTA Media, light liquid glass), as the artifact."""
    sw = [("#a81428", "accent #A81428"), ("#7a1020", "red-800"), ("#fadee1", "red-100"), ("#fdf6f6", "blush"),
          ("#f9fafc", "frost-100"), ("#1a1e27", "ink-950")]
    sws = "".join(f'<div style="background:{c}"><span style="color:{"#fff" if c in ("#a81428", "#7a1020", "#1a1e27") else "#1a1e27"}">{n}</span></div>' for c, n in sw)
    return f'''<div class="ds"><div class="eb">ruta.media · design system</div><h1>Light liquid glass</h1>
  <div style="font:400 15px/1.45 Archivo;color:#3c4557;margin-top:8px;max-width:560px">Bright, friendly, low-contrast surfaces with just enough frost. One accent red. Precise, warm, fast.</div>
  <div class="sw" id="ds-sw">{sws}</div>
  <div class="row" id="ds-type" style="align-items:flex-end">
    <div class="gl" style="padding:18px 22px;flex:1"><div class="eb">type</div><div style="font:600 54px/1 Archivo;letter-spacing:-.035em">Aa</div>
      <div style="font:500 13px Archivo;color:#5c6678;margin-top:6px">Archivo 600 · display −0.035em</div></div>
    <div class="gl" style="padding:18px 22px;flex:1.4;position:relative;overflow:hidden"><div class="orb" style="width:180px;height:180px;right:-40px;top:-50px"></div>
      <div class="eb">glass panel</div><div style="font:600 24px/1.1 Archivo;letter-spacing:-.02em">Rooftop film,<br>shipped in 72 hours</div>
      <div class="pill" style="display:inline-block;margin-top:12px;background:#a81428;color:#fff;border-radius:999px;padding:8px 16px;font:600 12px Archivo">Book a window</div></div>
  </div>
  <div class="eb" style="margin-top:20px">examples</div>
  <div class="row" id="ds-ex">
    <div class="slide"><div class="orb" style="width:240px;height:240px;left:-40px;top:-60px"></div><div class="gl"><div class="eb" style="font-size:9px">01 / 05</div><div class="t">Two backgrounds, one panel</div></div></div>
    <div class="slide"><div class="gl" style="top:14px"><div class="eb" style="font-size:9px">numbers</div><div class="n">72h</div><div class="t" style="font-size:15px">from shoot to post</div></div></div>
    <div class="slide" style="background:linear-gradient(180deg,#fdfbf8,#f2efeb)"><div class="gl"><div class="t" style="font-size:18px">Book the window</div><span class="pill">Take a slot</span></div></div>
  </div></div>'''


def carousel_preview():
    def sl(inner, extra=""):
        return f'<div class="slide" style="width:250px;height:312px;{extra}">{inner}</div>'
    slides = [
        sl('<div class="orb" style="width:300px;height:300px;left:-60px;top:-80px"></div><div class="gl"><div class="eb" style="font-size:9px">обкладинка · 01/05</div><div class="t" style="font-family:PS;font-weight:700">5 правил<br>AI-монтажу</div></div>'),
        sl('<div class="gl" style="top:14px"><div class="eb" style="font-size:9px">текст · 02/05</div><div class="t" style="font:700 17px/1.2 PS">Один стиль на все. Кольори, шрифти й анімації — з дизайн-системи.</div></div>'),
        sl('<div style="position:absolute;left:14px;right:14px;top:14px;height:150px;border-radius:14px;background:url(assets/img/p6.jpg) center/cover"></div><div class="gl"><div class="eb" style="font-size:9px">текст + фото · 03/05</div><div class="t" style="font:700 15px/1.2 PS">Фото завжди в склі, ніколи на весь слайд</div></div>'),
        sl('<div class="gl" style="top:14px"><div class="n">10–15</div><div class="t" style="font:700 15px/1.2 PS">рілсів на тиждень без монтажера</div></div>'),
        sl('<div class="gl" style="top:60px;text-align:center"><div class="t" style="font:700 22px/1.1 PS">Забирай промт</div><span class="pill">Пиши «стиль»</span></div>', "background:linear-gradient(165deg,#fff,#fadee1)"),
    ]
    return '<div class="ds" style="padding:24px"><div class="eb">каруселі · 1080×1350</div><h1 style="font-size:30px">Тестова карусель</h1><div class="row" id="car" style="flex-wrap:wrap;gap:14px">' + "".join(slides) + '</div></div>'


# ===================================================================== beats
# Each fn returns (stage_html, js). Times inside js are beat-local seconds.
# `T(x)` converts an output time to beat-local.

@beat("b01", 0.0, 8.4, bg="none")
def _(T):
    html = '<div class="lower" id="lt"><small>технічна продюсерка</small>Рута · AI-монтаж і автоматизація</div>'
    js = f'''LM.rise(tl,"#lt",{T(0.9)}); LM.fadeOut(tl,"#lt",{T(7.6)},0.5);'''
    return html, js


@beat("b02", 8.6, 38.0)
def _(T):
    reels = ["REEL-21", "REEL-26", "REEL-13", "REEL-25"]
    ph = "".join(f'<div class="ph" id="ph{i}" style="position:absolute;left:{70 + i * 300}px;top:170px;width:270px;height:480px;border-radius:30px;overflow:hidden;'
                 f'box-shadow:0 0 0 7px #1a1e27,0 30px 60px -20px rgba(0,0,0,.45);background:#000">'
                 f'<video class="clip" id="rv{i}" src="assets/{r}.mp4" data-start="0" data-duration="{38.0 - 8.6:.2f}" data-media-start="{4 + i * 3}" muted playsinline '
                 f'style="width:270px;height:480px;object-fit:cover"></video></div>' for i, r in enumerate(reels))
    html = f'''<div class="gtitle" style="left:70px;top:70px" id="ti"><span class="dot"></span>Мої останні рілси</div>{ph}
      <div class="chip" id="c1" style="left:70px;top:720px">змонтовані AI</div>
      <div class="chip light" id="c2" style="left:440px;top:720px">каруселі — AI</div>
      <div class="chip light" id="c3" style="left:770px;top:720px">сценарії — AI</div>'''
    js = f'''LM.flash(tl,0.25); LM.cam(tl,0.1,"card",0.9);
      LM.rise(tl,"#ti",0.5);
      [0,1,2,3].forEach(i=>LM.pop(tl,"#ph"+i,0.7+i*0.18));
      LM.pop(tl,"#c1",{T(13.2)}); LM.pop(tl,"#c2",{T(24.6)}); LM.pop(tl,"#c3",{T(29.0)});
      LM.xt(tl,{T(36.4)},70,830,"абсолютно з нуля ✓",44,"#c2253a");
      tl.to(["#ti","#c1","#c2","#c3","#ph0","#ph1","#ph2","#ph3","#d1"],{{opacity:0,duration:0.4}},{T(37.2)});
      LM.cam(tl,{T(37.1)},"full",0.8);'''
    return html, js


def theory_open(title, at=0.5):
    return f'''LM.flash(tl,0.25); LM.cam(tl,0.1,"card",0.9);
      document.getElementById("stage").insertAdjacentHTML("beforeend",'<div class="gtitle" id="gt" style="left:80px;top:70px"><span class="dot"></span>{title}</div>');
      LM.rise(tl,"#gt",{at});'''


def theory_close(end):
    return f'''tl.to(["#gt","#stage svg","#stage div"],{{opacity:0,duration:0.35}},{end - 0.85});
      LM.cam(tl,{end - 0.9},"full",0.8);'''


@beat("b03", 48.0, 56.0, bg="none")
def _(T):
    html = '<div class="lower" id="lt" style="left:auto;right:90px;bottom:150px"><small>щотижня</small>10–15 рілсів</div>'
    return html, f'LM.rise(tl,"#lt",{T(48.6)}); LM.fadeOut(tl,"#lt",{T(55.0)},0.5);'


@beat("b04", 74.0, 139.3)
def _(T):
    E = T(139.3)
    js = theory_open("StyleMD = дизайн-система")
    js += f'''
      LM.xt(tl,{T(77)},90,190,"основа, з якої AI дизайнить і монтує",40,"#5c6678");
      LM.ex(tl,{T(79.5)},"rect",[100,300,330,170],{{fill:"#fadee1",stroke:"#a81428"}}); LM.xt(tl,{T(80)},265,350,"каруселі",44,"#1e1e1e",{{center:1}});
      LM.ex(tl,{T(80.6)},"rect",[480,300,330,170],{{fill:"#a5d8ff",stroke:"#1971c2"}}); LM.xt(tl,{T(81.1)},645,350,"монтаж",44,"#1e1e1e",{{center:1}});
      LM.ex(tl,{T(85.6)},"ellipse",[455,640,520,170],{{stroke:"#a81428",strokeWidth:3}}); LM.xt(tl,{T(85.9)},455,610,"дизайн-система",50,"#a81428",{{center:1}});
      LM.ex(tl,{T(86.5)},"arrow",[300,560,265,480]); LM.ex(tl,{T(86.8)},"arrow",[610,560,645,480]);
      LM.clearScene(tl,{T(88.4)}); LM.scene();
      tl.to("#gt",{{opacity:0,duration:0.3}},{T(88.4)});
      document.getElementById("stage").insertAdjacentHTML("beforeend",'<div class="gtitle" id="gt2" style="left:80px;top:70px;opacity:0"><span class="dot"></span>Що таке .md?</div>');
      LM.flash(tl,{T(88.8)},0.6); LM.rise(tl,"#gt2",{T(88.9)});
      LM.xt(tl,{T(99.5)},90,190,"просто розширення файлу",44,"#5c6678");
      [["xlsx","#2f9e44","#b2f2bb"],["docx","#1971c2","#a5d8ff"],["pdf","#e03131","#ffc9c9"],["md","#a81428","#fadee1"]].forEach((f,i)=>{{
        const x=100+i*290, t={T(108.2)}+i*0.9;
        LM.ex(tl,t,"path","M"+x+" 300 L"+(x+150)+" 300 L"+(x+200)+" 350 L"+(x+200)+" 520 L"+x+" 520 Z",{{fill:f[2],stroke:f[1]}});
        LM.xt(tl,t+0.3,x+100,390,"."+f[0],52,f[1],{{center:1}});
      }});
      LM.ex(tl,{T(113.6)},"ellipse",[1070,410,270,250],{{stroke:"#a81428",strokeWidth:3.4,roughness:2}});
      LM.ex(tl,{T(114.5)},"arrow",[1000,560,780,680],{{bend:-40}});
      LM.xt(tl,{T(115.2)},120,650,"формат, в якому AI сам собі пише",40);
      LM.xt(tl,{T(117)},120,705,"інструкції + пам'ять",52,"#a81428");
      LM.clearScene(tl,{T(126)}); LM.scene();
      LM.ex(tl,{T(126.6)},"rect",[120,300,460,230],{{fill:"#fadee1",stroke:"#a81428",strokeWidth:3}});
      LM.xt(tl,{T(127)},350,370,"StyleMD",64,"#a81428",{{center:1}});
      LM.ex(tl,{T(130.4)},"arrow",[600,415,760,415]);
      LM.ex(tl,{T(130.8)},"rect",[780,300,440,230],{{stroke:"#1e1e1e"}});
      LM.xt(tl,{T(131.2)},1000,345,"брендбук",58,"#1e1e1e",{{center:1}});
      LM.xt(tl,{T(132.9)},1000,425,"мовою агента",40,"#5c6678",{{center:1}});
      LM.xt(tl,{T(136.2)},140,620,"дизайн · монтаж · і так далі",44);'''
    js += f'''tl.to(["#gt2","#stage svg","#stage div"],{{opacity:0,duration:0.35}},{E - 0.85}); LM.cam(tl,{E - 0.9},"full",0.8);'''
    return "", js


@beat("b05", 139.4, 255.6)
def _(T):
    E = T(255.6)
    js = theory_open("Як працює система", 0.4)
    js += f'''
      LM.ex(tl,{T(141.6)},"rect",[90,200,560,420],{{fill:"#fadee1",stroke:"#a81428",strokeWidth:3,hachureGap:12}});
      LM.xt(tl,{T(143.9)},370,225,"Основа · брендбук",48,"#a81428",{{center:1}});
      LM.xt(tl,{T(146.8)},140,320,"• кольори",44); LM.xt(tl,{T(149.8)},140,385,"• шрифти",44);
      LM.xt(tl,{T(151.4)},140,450,"• елементи",44); LM.xt(tl,{T(152.6)},140,515,"• стиль",44);
      LM.xt(tl,{T(155)},720,300,"задає тон\\nвсьому дизайну",44,"#5c6678");
      LM.ex(tl,{T(155.4)},"arrow",[710,380,670,420],{{}});
      LM.clearScene(tl,{T(159.6)}); LM.scene();
      [["#f08c00","#ffd8a8"],["#2f9e44","#b2f2bb"],["#1971c2","#a5d8ff"]].forEach((c,i)=>{{
        LM.ex(tl,{T(162.4)}+i*1.3,"rect",[120+i*360,260,260,400],{{fill:c[1],stroke:c[0]}});
        LM.xt(tl,{T(162.6)}+i*1.3,250+i*360,430,["рілс","карусель","рілс"][i],40,c[0],{{center:1}});
      }});
      LM.ex(tl,{T(166.6)},"line",[90,230,1130,700],{{stroke:"#e03131",strokeWidth:6}});
      LM.ex(tl,{T(166.9)},"line",[1130,230,90,700],{{stroke:"#e03131",strokeWidth:6}});
      LM.clearScene(tl,{T(167.6)}); LM.scene();
      LM.ex(tl,{T(172.9)},"rect",[110,260,420,260],{{fill:"#ffec99",stroke:"#f08c00"}}); LM.xt(tl,{T(173.2)},320,355,"персональний",46,"#1e1e1e",{{center:1}});
      LM.ex(tl,{T(176.3)},"rect",[690,260,420,260],{{fill:"#a5d8ff",stroke:"#1971c2"}}); LM.xt(tl,{T(176.6)},900,355,"експертний",46,"#1e1e1e",{{center:1}});
      LM.xt(tl,{T(179.6)},320,560,"дизайн-система 1",36,"#5c6678",{{center:1}}); LM.xt(tl,{T(179.9)},900,560,"дизайн-система 2",36,"#5c6678",{{center:1}});
      LM.xt(tl,{T(184.2)},610,660,"✓ абсолютно нормально",48,"#2f9e44",{{center:1}});
      LM.clearScene(tl,{T(185.6)}); LM.scene();
      LM.ex(tl,{T(186.2)},"ellipse",[610,430,700,420],{{fill:"#e9ecef",stroke:"#1e1e1e",roughness:2.4}});
      LM.xt(tl,{T(186.6)},610,380,"все в одному стилі",44,"#1e1e1e",{{center:1}});
      LM.xt(tl,{T(190)},610,520,"AI заплутається ?!",54,"#e03131",{{center:1}});
      LM.xt(tl,{T(193.9)},610,720,"кожен стиль = свій брендбук",48,"#a81428",{{center:1}});
      LM.clearScene(tl,{T(196.8)}); LM.scene();
      LM.ex(tl,{T(197.1)},"rect",[440,220,360,150],{{fill:"#fadee1",stroke:"#a81428",strokeWidth:3}}); LM.xt(tl,{T(197.4)},620,265,"основа",50,"#a81428",{{center:1}});
      ["каруселі","рілси","гайди"].forEach((n,i)=>{{
        const x=110+i*380, t={T(199.5)}+i*0.5;
        LM.ex(tl,t,"arrow",[620,380,x+150,520],{{}});
        LM.ex(tl,t+0.3,"rect",[x,540,300,130],{{stroke:"#1e1e1e"}}); LM.xt(tl,t+0.5,x+150,575,n,44,"#1e1e1e",{{center:1}});
      }});
      LM.xt(tl,{T(203)},620,720,"секція на кожен тип результату",40,"#5c6678",{{center:1}});
      LM.clearScene(tl,{T(206.6)}); LM.scene();
      document.getElementById("stage").insertAdjacentHTML("beforeend",
       '<div id="mybb" class="gl" style="position:absolute;left:110px;top:210px;width:1050px;height:520px;border-radius:40px;padding:44px 50px;font-family:PS;opacity:0">'+
       '<div style="font:700 22px PS;letter-spacing:.16em;color:#a81428">МІЙ БРЕНДБУК</div>'+
       '<div style="display:flex;gap:40px;margin-top:30px;align-items:flex-end"><div style="font:700 150px/1 PS;color:#1a1e27">Aa</div>'+
       '<div style="font:500 30px PS;color:#5c6678;padding-bottom:20px">Product Sans<br>без засічок</div></div>'+
       '<div style="display:flex;gap:18px;margin-top:40px"><div style="width:120px;height:120px;border-radius:28px;background:#a81428"></div>'+
       '<div style="width:120px;height:120px;border-radius:28px;background:#7a1020"></div><div style="width:120px;height:120px;border-radius:28px;background:#fadee1"></div>'+
       '<div style="width:120px;height:120px;border-radius:28px;background:#f9fafc;box-shadow:inset 0 0 0 1px #ddd"></div>'+
       '<div style="font:700 34px/1.2 PS;color:#1a1e27;margin-left:30px;align-self:center" id="aplg">Apple / Google<br><span style="color:#a81428">мінімалізм</span></div></div></div>');
      LM.pop(tl,"#mybb",{T(209.1)},0.7); LM.rise(tl,"#aplg",{T(217.5)});
      tl.to("#mybb",{{opacity:0,y:-20,duration:0.4}},{T(224.1)});
      LM.ex(tl,{T(224.4)},"rect",[90,200,330,120],{{fill:"#fadee1",stroke:"#a81428",strokeWidth:3}}); LM.xt(tl,{T(224.6)},255,232,"основа",46,"#a81428",{{center:1}});
      LM.ex(tl,{T(226.6)},"arrow",[430,260,560,260],{{}});
      LM.ex(tl,{T(228.2)},"rect",[580,200,330,120],{{fill:"#a5d8ff",stroke:"#1971c2"}}); LM.xt(tl,{T(228.4)},745,232,"+ каруселі",46,"#1e1e1e",{{center:1}});
      LM.xt(tl,{T(237.0)},120,400,"• скільки тексту на слайд?",42);
      LM.xt(tl,{T(242.8)},120,465,"• який розмір тексту?",42);
      LM.xt(tl,{T(244.6)},120,530,"• як розміщуємо картинки?",42);
      LM.xt(tl,{T(246.3)},120,595,"• як я люблю розставляти елементи?",42);
      LM.xt(tl,{T(249.8)},120,660,"• скільки слайдів?",42);'''
    js += theory_close(E)
    return "", js


@beat("b06", 255.6, 288.2)
def _(T):
    E = T(288.2)
    js = theory_open("Рілс — інша історія", 0.4)
    js += f'''
      LM.ex(tl,{T(256.4)},"rect",[400,170,400,760],{{stroke:"#1e1e1e",strokeWidth:3.4,roughness:0.8}});
      LM.ex(tl,{T(258.9)},"rect",[400,170,400,150],{{fill:"#ffc9c9",stroke:"#e03131",hachureGap:12}});
      LM.xt(tl,{T(259.4)},830,210,"зверху — нічого",40,"#e03131");
      LM.ex(tl,{T(262.4)},"rect",[400,760,400,170],{{fill:"#ffc9c9",stroke:"#e03131",hachureGap:12}});
      LM.xt(tl,{T(262.8)},830,820,"знизу — нічого",40,"#e03131");
      LM.ex(tl,{T(264.6)},"rect",[400,320,70,440],{{fill:"#ffc9c9",stroke:"#e03131",hachureGap:12}});
      LM.ex(tl,{T(265.0)},"rect",[730,320,70,440],{{fill:"#ffc9c9",stroke:"#e03131",hachureGap:12}});
      LM.xt(tl,{T(265.4)},830,520,"по боках — UI",40,"#e03131");
      LM.ex(tl,{T(273.2)},"rect",[490,350,220,170],{{fill:"#b2f2bb",stroke:"#2f9e44"}});
      LM.xt(tl,{T(273.6)},600,405,"головне",36,"#2f9e44",{{center:1}});
      LM.ex(tl,{T(277.1)},"rect",[490,650,220,70],{{fill:"#ffec99",stroke:"#f08c00"}});
      LM.xt(tl,{T(277.4)},600,660,"субтитри",32,"#1e1e1e",{{center:1}});
      LM.xt(tl,{T(283.4)},110,960,"не пропишеш — AI не знатиме",44,"#a81428");'''
    js += theory_close(E)
    return "", js


@beat("b07", 288.2, 350.4)
def _(T):
    E = T(350.4)
    js = theory_open("Слайди ≠ гайди", 0.4)
    js += f'''
      LM.ex(tl,{T(300.7)},"rect",[120,220,420,520],{{fill:"#fadee1",stroke:"#a81428",strokeWidth:3}});
      LM.xt(tl,{T(301)},330,250,"слайд",56,"#a81428",{{center:1}});
      LM.xt(tl,{T(304.4)},160,360,"коротко",44); LM.xt(tl,{T(305.6)},160,430,"хайпово",44);
      LM.xt(tl,{T(306.8)},160,500,"великий текст",44); LM.xt(tl,{T(308.6)},160,570,"швидко гортаємо →",44);
      LM.ex(tl,{T(311.4)},"rect",[680,220,480,520],{{fill:"#a5d8ff",stroke:"#1971c2",strokeWidth:3}});
      LM.xt(tl,{T(311.7)},920,250,"гайд",56,"#1971c2",{{center:1}});
      LM.xt(tl,{T(315.6)},720,360,"прочитати",44); LM.xt(tl,{T(316.6)},720,430,"зрозуміти",44); LM.xt(tl,{T(317.6)},720,500,"застосувати",44);
      LM.xt(tl,{T(321.4)},720,570,"текст + скріни",40,"#5c6678");
      LM.clearScene(tl,{T(331.0)}); LM.scene();
      LM.ex(tl,{T(334.0)},"rect",[440,200,360,140],{{fill:"#fadee1",stroke:"#a81428",strokeWidth:3}}); LM.xt(tl,{T(334.2)},620,240,"основа",52,"#a81428",{{center:1}});
      ["секція","секція","секція"].forEach((n,i)=>{{ const x=150+i*330, t={T(335.0)}+i*0.4;
        LM.ex(tl,t,"arrow",[620,350,x+120,470]); LM.ex(tl,t+0.2,"rect",[x,490,240,110],{{stroke:"#1e1e1e"}}); LM.xt(tl,t+0.4,x+120,515,n,40,"#1e1e1e",{{center:1}}); }});
      LM.xt(tl,{T(337.8)},620,640,"скільки — вирішуєш ти",40,"#5c6678",{{center:1}});
      LM.xt(tl,{T(340.5)},620,730,"у мене дві: каруселі + монтаж",48,"#a81428",{{center:1}});'''
    js += theory_close(E)
    return "", js


def screen_open(at=0.1):
    return f'''gsap.set("#scrwrap",{{opacity:0}}); LM.flash(tl,{at + 0.15}); LM.cam(tl,{at},"circle",1.0); LM.screenIn(tl,{at + 0.1});'''


def screen_close(end):
    return f'''LM.zoom(tl,{end - 1.6},null,0,1,0.7); LM.screenOut(tl,{end - 0.9},0.5); LM.cam(tl,{end - 0.95},"full",0.85);'''


def chapter_html(num, title):
    return f'''<div id="chap" class="clip" style="z-index:30;opacity:0;background:radial-gradient(1200px 700px at 30% 20%,#b8213a 0%,#8d0d24 45%,#5c0716 100%)">
      <div class="chap"><div class="num">{num}</div><div class="ttl">{title}</div></div></div>'''


def chapter_js(a, b):
    return f'''LM.flash(tl,{a + 0.1}); tl.set("#chap",{{opacity:1}},{a + 0.1}); LM.rise(tl,"#chap .num",{a + 0.25}); LM.rise(tl,"#chap .ttl",{a + 0.4},0.7);
      LM.camHide(tl,{a + 0.1},0.05); tl.to("#chap",{{opacity:0,duration:0.5}},{b - 0.5}); LM.camShow(tl,{b - 0.5},0.01);'''


def claude_thread_view(user, reply_id="rep", panel_html="", card="Design System (migrated)"):
    return f'''<div class="cl" id="clds" style="opacity:0">{claude_side(None, ["Design system"])}<div class="main">
      <div class="thread" style="left:40px;width:520px"><div class="ub">{user}</div>
      <div class="ar" id="{reply_id}"></div>
      <div class="artcard" id="acard" style="opacity:0;width:440px"><i></i><div>{card}<small>Design System · RUTA Media</small></div></div></div>
      <div class="panel" id="pnl" style="opacity:0"><div class="ph">{card} <span class="sh">Share</span></div><div class="pb">{panel_html}</div></div></div></div>'''


@beat("b08", 350.4, 380.6, bg="desk")
def _(T):
    E = T(380.6)
    page = claude_home() + claude_thread_view("open MY design system pls", panel_html=ds_preview())
    html = chapter_html("ЧАСТИНА 02", "Claude чи <em>ChatGPT?</em>") + screen(page, ["Claude", "Pinterest", "OpenRouter"], "Claude", "claude.ai/new")
    html += '<div class="chip" id="fg" style="left:120px;top:70px;z-index:60;opacity:0">«фігма на мінімалках»</div>'
    js = chapter_js(0.0, T(355.6))
    js += f'''gsap.set("#scrwrap",{{opacity:0}}); LM.cursorAt(900,700); LM.cam(tl,{T(355.5)},"circle",0.9); LM.screenIn(tl,{T(355.6)});
      LM.move(tl,{T(361.4)},80,398,1.0); LM.click(tl,{T(362.5)});
      tl.set("#url",{{textContent:"claude.ai/design"}},{T(362.6)});
      tl.to("#clds",{{opacity:1,duration:0.35}},{T(362.7)});
      LM.stream(tl,{T(363.2)},"#rep","Opening your design system. Light liquid glass, one accent red, Archivo.",18);
      tl.to("#acard",{{opacity:1,duration:0.3}},{T(364.2)});
      LM.fadeIn(tl,"#pnl",{T(364.6)},0.5,20);
      LM.move(tl,{T(366)},1200,420,1.0);
      LM.zoom(tl,{T(366.4)},1210,480,1.55,1.4);
      LM.pop(tl,"#fg",{T(372.2)});
      LM.zoom(tl,{T(375.5)},1210,640,1.7,1.4);
      tl.to("#fg",{{opacity:0,duration:0.3}},{E - 1.0});'''
    js += screen_close(E)
    return html, js


@beat("b09", 380.6, 418.8)
def _(T):
    E = T(418.8)
    js = theory_open("Claude збирає. ChatGPT генерує.", 0.4)
    js += f'''
      LM.xt(tl,{T(381)},110,190,"Claude",54,"#d97757");
      LM.ex(tl,{T(389.8)},"rect",[110,270,480,520],{{stroke:"#1e1e1e",strokeWidth:3}});
      LM.xt(tl,{T(392)},350,820,"як сайт — по елементах",38,"#5c6678",{{center:1}});
      LM.ex(tl,{T(395.4)},"rect",[150,310,400,120],{{fill:"#fadee1",stroke:"#a81428"}}); LM.xt(tl,{T(395.6)},350,345,"прямокутник",36,"#a81428",{{center:1}});
      LM.xt(tl,{T(396.6)},170,460,"текст текст текст",38);
      LM.ex(tl,{T(397.8)},"ellipse",[260,640,170,170],{{fill:"#a5d8ff",stroke:"#1971c2",fillStyle:"solid"}}); LM.xt(tl,{T(398.1)},350,620,"",10);
      LM.xt(tl,{T(399)},360,690,"кружечок\\n(розблюрений)",30,"#1971c2");
      LM.xt(tl,{T(402.2)},700,190,"ChatGPT",54,"#10a37f");
      LM.ex(tl,{T(402.4)},"rect",[700,270,480,520],{{fill:"#ced4da",stroke:"#495057",fillStyle:"cross-hatch",hachureGap:14}});
      LM.xt(tl,{T(403)},940,500,"одна картинка",42,"#1e1e1e",{{center:1}});
      LM.xt(tl,{T(412.2)},940,820,"= слоп",50,"#e03131",{{center:1}});
      LM.xt(tl,{T(406.8)},700,880,"якщо не попросиш зібрати кодом",34,"#5c6678");'''
    js += theory_close(E)
    return "", js


P1 = ("Ти — арт-директор і дизайнер бренду. Я надсилаю приклади свого стилю (або референси вайбу + реальні сайти й продукти, які мені подобаються).\n\n"
      "Розбери їх і створи мою дизайн-систему:\n— вайб і характер бренду (3–5 слів + опис)\n— кольори: основні, акцентні, фонові, з HEX і правилами використання\n"
      "— типографіка: шрифти, розміри й насиченість\n— елементи: форми, іконки, фото, текстури, тіні, заокруглення\n— композиція: сітка, відступи, скільки повітря\n— що НІКОЛИ не робимо\n\n"
      "Покажи прев'ю: палітру, шрифти і 2–3 приклади дизайну в цьому стилі.")
P1b = ("\n\nПро мене: моя ЦА — блогерки й підприємці, 20–200 тис. підписників. Хочу преміум, не дитячий стиль. "
       "Люблю Google і Apple: мінімалізм, темно-червоний, шрифт без засічок.")
P2 = ("Додай до моєї дизайн-системи окремий розділ «Каруселі». Ось приклади каруселей, які мені подобаються.\n\n"
      "Опиши для формату 4:5 (1080×1350):\n— поля, відступи, безпечні зони\n— розміри тексту на обкладинці й на слайдах\n"
      "— структуру: обкладинка → слайди → фінальний слайд із закликом\n— скільки тексту максимум на слайд\n\n"
      "Основний стиль не змінюй, це доповнення. Покажи тестову карусель на 5 слайдів.")


def js_str(x):
    return json.dumps(x, ensure_ascii=False)


def claude_box_page(extra=""):
    # home page whose box will be moved to the top and filled
    return claude_home() + extra


@beat("b10", 457.6, 551.0, bg="desk", cout=True)
def _(T):
    page = claude_box_page()
    html = chapter_html("ЧАСТИНА 03", "Створюємо <em>базу</em>") + screen(page, ["Claude", "Pinterest", "OpenRouter"], "Claude", "claude.ai/new")
    html += '<div class="chip" id="ca" style="left:120px;top:60px;z-index:60;opacity:0">є брендбук → скріни в чат</div>'
    html += '<div class="chip light" id="cb" style="left:120px;top:60px;z-index:60;opacity:0">немає → мудборд + опис</div>'
    js = chapter_js(0.0, T(463.0))
    js += f'''gsap.set("#scrwrap",{{opacity:0}}); LM.cursorAt(700,650); LM.cam(tl,{T(462.8)},"circle",0.9); LM.screenIn(tl,{T(462.9)});
      LM.move(tl,{T(464.0)},90,246,0.8); LM.click(tl,{T(464.9)});
      LM.move(tl,{T(465.4)},900,500,0.7); LM.click(tl,{T(466.2)});
      tl.to(".hello",{{opacity:0,y:-20,duration:0.4}},{T(466.4)});
      tl.to("#box",{{top:40,duration:0.6,ease:"power3.inOut"}},{T(466.4)});
      tl.set("#ph",{{display:"none"}},{T(467.0)});
      LM.zoom(tl,{T(466.8)},965,330,1.45,1.0);
      let e = LM.type(tl,{T(467.2)},"#typed",{js_str(P1)},34);
      LM.zoom(tl,{T(474)},965,430,1.45,2.0);
      LM.pop(tl,"#ca",{T(482.2)}); tl.to("#ca",{{opacity:0,duration:0.3}},{T(493.6)});
      document.getElementById("atts").innerHTML='<span class="att" id="a1" style="background-image:url(assets/img/p0.jpg)"></span><span class="att" id="a2" style="background-image:url(assets/img/p3.jpg)"></span>';
      LM.pop(tl,"#a1",{T(486.0)}); LM.pop(tl,"#a2",{T(486.4)});
      LM.pop(tl,"#cb",{T(503.0)}); tl.to("#cb",{{opacity:0,duration:0.3}},{T(514.0)});
      const t2 = document.createElement("span"); t2.id="typed2"; document.getElementById("typed").after(t2);
      tl.set("#typed .caret",{{display:"none"}},{T(506.4)});
      LM.type(tl,{T(506.6)},"#typed2",{js_str(P1b)},9);
      LM.zoom(tl,{T(507)},965,440,1.45,1.4);
      LM.zoom(tl,{T(546.5)},null,0,1,1.2);'''
    return html, js


def pinterest_page():
    return '''<div style="position:absolute;inset:0;background:#fff">
      <img id="pg1" src="assets/img/pin1.png" style="position:absolute;left:0;top:0;width:1600px;opacity:0">
      <img id="pg2" src="assets/img/pin2.png" style="position:absolute;left:0;top:0;width:1600px;opacity:0">
      <div id="pghome" style="position:absolute;inset:0;background:#fff"><img src="assets/img/pin2.png" style="width:1600px;filter:blur(14px) saturate(.6);opacity:.55;transform:translateY(40px)"></div>
      <div style="position:absolute;left:115px;top:21px;width:1358px;height:63px;border-radius:32px;background:#e9e9e9;font:400 22px Inter;color:#111;display:flex;align-items:center;padding-left:26px">
        <span id="pq" style="color:#767676">Search</span></div></div>'''


@beat("b11", 551.0, 601.6, bg="desk", cin=True, cout=True)
def _(T):
    pin = pinterest_page()
    cl = claude_home() 
    page = f'<div id="pPin" style="position:absolute;inset:0">{pin}</div><div id="pCl" style="position:absolute;inset:0;opacity:0">{cl}</div>'
    html = screen(page, ["Claude", "Pinterest", "OpenRouter"], "Pinterest", "pinterest.com")
    html += '<div class="chip" id="cs" style="left:120px;top:60px;z-index:60;opacity:0">крадемо, як художники</div>'
    js = f'''LM.move(tl,0.3,560,199,0.9); LM.click(tl,{T(570.6)});
      tl.set("#pq",{{color:"#111",textContent:""}},{T(570.8)});
      LM.type(tl,{T(570.9)},"#pq","carousel design",14);
      tl.set("#url",{{textContent:"pinterest.com/search/pins/?q=carousel%20design"}},{T(572.3)});
      tl.to("#pghome",{{opacity:0,duration:0.3}},{T(572.3)}); tl.to("#pg1",{{opacity:1,duration:0.3}},{T(572.3)});
      LM.zoom(tl,{T(573.0)},620,560,1.5,1.3);
      LM.move(tl,{T(574.0)},480,520,0.8); LM.move(tl,{T(576.0)},860,520,0.9); LM.move(tl,{T(578.4)},1180,560,0.9);
      LM.pop(tl,"#cs",{T(582.4)}); tl.to("#cs",{{opacity:0,duration:0.3}},{T(586.2)});
      LM.zoom(tl,{T(584.4)},null,0,1,0.9);
      LM.move(tl,{T(586.4)},560,199,0.7); LM.click(tl,{T(587.2)});
      tl.set("#pq",{{textContent:""}},{T(587.3)});
      LM.type(tl,{T(587.4)},"#pq","liquid glass",14);
      tl.set("#url",{{textContent:"pinterest.com/search/pins/?q=liquid%20glass"}},{T(588.4)});
      tl.to("#pg1",{{opacity:0,duration:0.3}},{T(588.5)}); tl.to("#pg2",{{opacity:1,duration:0.3}},{T(588.5)});
      LM.zoom(tl,{T(589.6)},800,520,1.4,1.2); LM.move(tl,{T(590)},1300,560,1.0);
      LM.zoom(tl,{T(592.4)},null,0,1,0.8);
      tl.set(".tab[data-tab=Pinterest]",{{attr:{{class:"tab"}}}},{T(593.2)}); tl.set(".tab[data-tab=Claude]",{{attr:{{class:"tab on"}}}},{T(593.2)});
      tl.set("#url",{{textContent:"claude.ai/new"}},{T(593.2)});
      tl.set("#pCl",{{opacity:1}},{T(593.2)}); tl.set("#pPin",{{opacity:0}},{T(593.2)});
      tl.set("#pCl .hello",{{opacity:0}},0); tl.set("#pCl #box",{{top:40}},0); tl.set("#pCl #ph",{{display:"none"}},0);
      document.querySelector("#pCl #typed").textContent = {js_str(P1 + P1b)};
      document.querySelector("#pCl #atts").innerHTML = ["p0","p3","p1","p2","p4","p6"].map((p,i)=>'<span class="att" id="b'+i+'" style="background-image:url(assets/img/'+p+'.jpg)"></span>').join("");
      [2,3,4,5].forEach((i,k)=>LM.pop(tl,"#b"+i,{T(594.6)}+k*0.45));
      LM.zoom(tl,{T(594.0)},965,520,1.35,1.0);
      LM.move(tl,{T(597)},1508,620,0.8); LM.zoom(tl,{T(599.6)},null,0,1,0.8); LM.click(tl,{T(600.8)});'''
    return html, js


@beat("b12", 601.6, 666.8, bg="desk", cin=True)
def _(T):
    user = "Ти — арт-директор і дизайнер бренду…  (промт + 6 референсів)"
    page = claude_thread_view(user, panel_html=ds_preview(), card="RUTA Media — design system")
    html = screen(page.replace('id="clds" style="opacity:0"', 'id="clds"'), ["Claude", "Pinterest", "OpenRouter"], "Claude", "claude.ai/chat/design-system")
    html += '<div class="chip" id="c1" style="left:120px;top:60px;z-index:60;opacity:0">приклад каруселі</div>'
    html += '<div class="chip light" id="c2" style="left:120px;top:60px;z-index:60;opacity:0">читабельно? кольори разом?</div>'
    rep = ("Ось твоя дизайн-система: <b>light liquid glass</b>.\n\nВайб: точний, теплий, швидкий. Один червоний акцент #A81428, "
           "все інше — frost і graphite. Скляні панелі з м'яким rim-light.\n\nНижче — палітра, типографіка і приклади: обкладинка, слайд з цифрою, CTA.")
    js = f'''LM.move(tl,0.4,700,600,0.8);
      LM.stream(tl,0.8,"#rep",{js_str(rep)},10);
      tl.to("#acard",{{opacity:1,duration:0.3}},{T(606)});
      LM.fadeIn(tl,"#pnl",{T(606.4)},0.6,20);
      LM.zoom(tl,{T(607.8)},1220,330,1.6,1.4);
      LM.zoom(tl,{T(613.2)},1220,470,1.6,1.4);
      tl.to("#pnl .ds",{{y:-260,duration:1.4,ease:"power3.inOut"}},{T(640.6)});
      LM.zoom(tl,{T(644.6)},1220,560,1.75,1.2);
      LM.pop(tl,"#c1",{T(645.1)}); tl.to("#c1",{{opacity:0,duration:0.3}},{T(652.0)});
      LM.move(tl,{T(647)},1050,540,0.8); LM.move(tl,{T(649)},1260,540,0.8); LM.move(tl,{T(651)},1470,560,0.8);
      LM.pop(tl,"#c2",{T(660.5)}); tl.to("#c2",{{opacity:0,duration:0.3}},{T(665.4)});'''
    js += screen_close(T(666.8))
    return html, js


@beat("b13", 668.8, 725.0, bg="desk")
def _(T):
    page = claude_home() + claude_thread_view("Додай до моєї дизайн-системи окремий розділ «Каруселі»…  (промт + приклади)", reply_id="rep2", panel_html=carousel_preview(), card="Каруселі · 1080×1350")
    page = page.replace('id="clds" style="opacity:0"', 'id="clds" style="opacity:0"')
    html = screen(page, ["Claude", "Pinterest", "OpenRouter"], "Claude", "claude.ai/chat/design-system")
    html += '<div class="chip" id="c1" style="left:120px;top:60px;z-index:60;opacity:0">«риба-текст» теж ок</div>'
    labels = ["обкладинка", "текст", "текст + картинка", "заклик до дії"]
    js = screen_open()
    js += f'''LM.cursorAt(900,650);
      tl.set(".hello",{{opacity:0}},0); tl.set("#box",{{top:40}},0); tl.set("#ph",{{display:"none"}},0);
      LM.zoom(tl,{T(670)},965,300,1.45,1.0);
      LM.type(tl,{T(673.4)},"#typed",{js_str(P2)},30);
      LM.pop(tl,"#c1",{T(689.3)}); tl.to("#c1",{{opacity:0,duration:0.3}},{T(695.0)});
      LM.zoom(tl,{T(694.6)},null,0,1,0.9);
      LM.move(tl,{T(695)},1508,620,0.6); LM.click(tl,{T(695.8)});
      tl.to("#clds",{{opacity:1,duration:0.3}},{T(696.0)});
      LM.stream(tl,{T(696.3)},"#rep2","Додала розділ «Каруселі». Ось тестова карусель на 5 слайдів у твоєму стилі:",14);
      tl.to("#acard",{{opacity:1,duration:0.3}},{T(697.4)});
      LM.fadeIn(tl,"#pnl",{T(697.8)},0.5,20);
      LM.zoom(tl,{T(699.6)},1230,420,1.55,1.2);
      [0,1,2,4].forEach((s,i)=>{{ const t=[{T(700.3)},{T(701.8)},{T(704.3)},{T(708.0)}][i];
        LM.move(tl,t,[990,1260,1500,1260][i],[400,400,400,700][i],0.6); }});
      LM.zoom(tl,{T(712.8)},1230,560,1.5,1.4);
      LM.move(tl,{T(716)},1000,700,1.2);'''
    js += screen_close(T(725.0))
    return html, js


P3 = ("Ти — моушн-дизайнер і монтажер. Я надсилаю рілси, стиль яких хочу повторити.\n\n"
      "1. Розбий кожен на сцени: таймкод, тривалість, що в кадрі, як з'являється текст і елементи, переходи, шрифт, кольори, ритм.\n"
      "2. Виведи закономірності: темп, хук у перші 3 секунди, повторювані прийоми.\n\n"
      "Потім зроби файл reels-style.md — доповнення до моєї дизайн-системи.")


def openrouter_page():
    rows = [("Google: Nano Banana 2.1", "1.48B", "$1.50", "$30", "65,536", "18.0s", "#4285f4"),
            ("Tencent: Hy Image 3.5 Preview", "1.37B", "", "$1.60", "—", "18.9s", "#1e88e5"),
            ("ByteDance Seed: Seedream 5.0 Flash", "1.67B", "", "from $0.018", "—", "16.6s", "#3d7bfd"),
            ("Black Forest Labs: FLUX 3 Image", "376M", "", "from $0.041", "—", "43.8s", "#111"),
            ("Recraft: Recraft V4.1 Flash", "557M", "", "$0.007", "—", "1.5s", "#111"),
            ("OpenAI: GPT Image 2.5 Sunburst", "4.4B", "$8", "$30", "—", "32.6s", "#111"),
            ("OpenAI: GPT Image 2.5 Flare", "1.41B", "$8", "$30", "—", "13.1s", "#111"),
            ("Microsoft AI: MAI-Image-2.6", "57.8M", "$8", "$38", "—", "24.2s", "#555")]
    tr = "".join(f'<tr id="or{i}"><td><i style="background:{r[6]}"></i><u>{r[0]}</u></td><td>{r[1]}</td><td>{r[2]}</td><td class="pr">{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>' for i, r in enumerate(rows))
    side = "".join(f'<div class="f">{n}</div>' for n in ["Discounted", "Context length", "Prompt pricing", "Series", "Categories", "Supported parameters", "Distillable", "Zero data retention"])
    mods = "".join(f'<div class="cb"><b></b>{n}</div>' for n in ["Text", "Image", "File", "Audio", "Video"])
    return f'''<style>
      .orp{{position:absolute;inset:0;background:#fff;font-family:Inter;color:#111}}
      .orp .top{{height:62px;border-bottom:1px solid #eee;display:flex;align-items:center;padding:0 30px;gap:26px;font:500 17px Inter}}
      .orp .top .sr{{margin-left:140px;width:260px;height:38px;border:1px solid #e5e5e5;border-radius:9px;color:#888;font:400 15px Inter;display:flex;align-items:center;padding-left:14px}}
      .orp .top .nv{{margin-left:auto;display:flex;gap:26px;color:#333;font:400 16px Inter}} .orp .top .nv b{{font-weight:600;color:#111}}
      .orp .sd{{position:absolute;left:0;top:62px;width:300px;bottom:0;border-right:1px solid #eee;padding:20px 30px;font:400 16px Inter;color:#333}}
      .orp .sd .h{{font-weight:500;margin-bottom:12px}} .orp .cb{{display:flex;gap:10px;align-items:center;margin:0 0 12px 8px;color:#555}}
      .orp .cb b{{width:16px;height:16px;border:1.5px solid #bbb;border-radius:4px}} .orp .f{{margin:22px 0;font-weight:500}}
      .orp .mn{{position:absolute;left:300px;top:62px;right:0;bottom:0;padding:22px 30px}}
      .orp h2{{font:700 28px Inter;margin-bottom:18px}}
      .orp .tb{{display:flex;gap:30px;font:500 16px Inter;color:#444;border-bottom:1px solid #eee;padding-bottom:12px;margin:18px 0 0}}
      .orp .tb .on{{color:#111;border-bottom:3px solid #6467f2;padding-bottom:10px;margin-bottom:-14px}}
      .orp table{{width:100%;border-collapse:collapse;font:400 16px Inter;margin-top:10px}}
      .orp th{{text-align:left;font-weight:500;color:#333;padding:14px 10px;border-bottom:1px solid #eee}}
      .orp td{{padding:15px 10px;border-bottom:1px solid #f0f0f0;color:#333}}
      .orp td i{{display:inline-block;width:20px;height:20px;border-radius:5px;margin-right:12px;vertical-align:-4px}}
      .orp td u{{text-decoration-color:#bbb;color:#111}}
      .orp tr.hl td{{background:#f4f4ff}}
    </style><div class="orp"><div class="top"><span><b style="color:#e8590c">●</b> Personal</span><span>Default Workspace</span><div class="sr">Search ⌘K</div>
      <div class="nv"><span>Dashboard</span><b>Models</b><span>Benchmarks</span><span>Chat</span><span>Rankings</span><span>Apps</span><span>Docs</span></div></div>
      <div class="sd"><div class="h">Input modalities</div>{mods}{side}</div>
      <div class="mn"><h2>Models</h2><div style="display:flex;gap:12px"><div style="flex:1;height:42px;border:1px solid #e5e5e5;border-radius:9px;color:#999;padding:11px 14px;font:400 15px Inter">Search models...</div>
        <div style="width:220px;height:42px;border:1px solid #e5e5e5;border-radius:9px;padding:11px 14px;font:400 15px Inter">⇅ Newest</div></div>
      <div class="tb"><span>All</span><span>Text 462</span><span class="on">Image 57</span><span>Video 30</span><span>Speech 35</span><span>Embeddings 37</span><span>Rerank 9</span></div>
      <table><tr><th>Model Name</th><th>Weekly Tokens</th><th>Input</th><th>Output</th><th>Context</th><th>Latency</th></tr>{tr}</table></div></div>'''


def code_page(title="Новий рілс", repo="reel-editor-machine"):
    sess = "".join(f'<div class="si" style="padding-left:14px">{n}</div>' for n in ["Reels 30-40 batch", "Reel 22 — fixes", "Carousel templates", "Lead magnet edit"])
    return f'''<div class="cl" id="ccode"><div class="side"><div class="logo">Claude Code</div>
      <div class="si on"><i></i>New session</div><div class="lbl">{repo}</div>{sess}
      <div class="user"><b>R</b><div>Ruta <small>· Max</small></div></div></div>
      <div class="main"><div style="height:54px;border-bottom:1px solid #eeece4;display:flex;align-items:center;padding:0 28px;font:500 15px Inter;color:#3d3d3a">{title}
        <span style="margin-left:12px;font:400 13px Inter;color:#8a8983">valeriya-ruta/{repo}</span></div>
      <div class="thread" id="cth" style="left:60px;width:1080px;top:76px"></div>
      <div class="box" id="cbox" style="left:60px;margin-left:0;width:1080px;top:auto;bottom:24px;min-height:96px"><span class="ph" id="cph">Ask Claude to build…</span><span id="ctyped"></span><div id="catts"></div>
        <div class="tools">+</div><div class="model">Opus 5.5</div><div class="send">↑</div></div></div></div>'''


@beat("b14", 725.0, 798.6, bg="desk")
def _(T):
    page = openrouter_page()
    html = chapter_html("ЛАЙФХАК 01", "Claude не генерує картинки.<br><em>OpenRouter</em> — генерує.") + screen(page, ["Claude", "Pinterest", "OpenRouter"], "OpenRouter", "openrouter.ai/models?output_modalities=image")
    html += '<div class="chip" id="c1" style="left:120px;top:60px;z-index:60;opacity:0">усі моделі в одному місці</div>'
    html += '<div class="chip light" id="c2" style="left:120px;top:60px;z-index:60;opacity:0">ціна ринкова — центи за картинку</div>'
    html += '<div class="chip" id="c3" style="left:120px;top:60px;z-index:60;opacity:0">Claude → OpenRouter → картинка в дизайні</div>'
    html += '<div class="chip light" id="c4" style="left:120px;top:60px;z-index:60;opacity:0">магія ✨</div>'
    js = chapter_js(0.0, T(737.4))
    js += f'''gsap.set("#scrwrap",{{opacity:0}}); LM.cursorAt(900,500); LM.cam(tl,{T(737.2)},"circle",0.9); LM.screenIn(tl,{T(737.3)});
      LM.pop(tl,"#c1",{T(742.2)}); tl.to("#c1",{{opacity:0,duration:0.3}},{T(753.6)});
      LM.move(tl,{T(744)},860,300,0.9); LM.click(tl,{T(745)});
      LM.zoom(tl,{T(749.6)},900,430,1.35,1.4);
      [0,1,2,3,4].forEach(i=>{{ LM.move(tl,{T(754)}+i*1.6,600,{376}+i*52,0.6); tl.set("#or"+i,{{attr:{{class:"hl"}}}},{T(754.3)}+i*1.6); tl.set("#or"+i,{{attr:{{class:""}}}},{T(755.8)}+i*1.6); }});
      LM.pop(tl,"#c2",{T(765.0)}); tl.to("#c2",{{opacity:0,duration:0.3}},{T(778.8)});
      LM.zoom(tl,{T(769.4)},1150,470,1.8,1.3); LM.move(tl,{T(770)},1150,480,0.8);
      LM.zoom(tl,{T(778.6)},null,0,1,1.0);
      LM.pop(tl,"#c3",{T(779.4)}); tl.to("#c3",{{opacity:0,duration:0.3}},{T(796.2)});
      LM.pop(tl,"#c4",{T(796.6)});'''
    js += screen_close(T(798.6))
    return html, js


@beat("b15", 798.6, 860.6, bg="desk")
def _(T):
    home = claude_home().replace('<div class="side"><div class="logo">Claude</div>', '<div class="side"><div class="logo">Claude</div><div class="toggle" id="tg"><span class="on" id="tgc">💬</span><span id="tgk">&lt;/&gt;</span></div>')
    home = home.replace("💬", "Chat").replace("&lt;/&gt;", "Code")
    page = f'<div id="pH" style="position:absolute;inset:0">{home}</div><div id="pK" style="position:absolute;inset:0;opacity:0">{code_page("Рілс: моє життя у В’єтнамі")}</div>'
    html = chapter_html("ЛАЙФХАК 02", "Chat ≠ <em>Code</em>") + screen(page, ["Claude", "Pinterest", "OpenRouter"], "Claude", "claude.ai/new")
    html += '<style>.cl .toggle{left:auto;right:14px;top:16px} .cl .toggle span{width:auto;padding:0 12px}</style>'
    for i, (t, light) in enumerate([("Chat — 90% задач", 0), ("монтаж — тільки в Code", 1), ("свій інтернет + термінал", 0), ("сам знайшов · сам вирізав · сам вставив", 1)]):
        html += f'<div class="chip{" light" if light else ""}" id="k{i}" style="left:120px;top:60px;z-index:60;opacity:0">{t}</div>'
    user = "Зроби рілс про моє життя у В'єтнамі в стилі скрапбуку — з реальними фото предметів."
    tools = ["Searching the web: «vietnamese coffee phin png», «banh mi photo», «motorbike saigon»",
             "Downloaded 14 images → assets/scrapbook/", "Removing backgrounds (OpenRouter · image model)",
             "Composing scrapbook layout: tape, torn paper, polaroids", "Rendering beat 1–6 …"]
    tl_html = "".join(f'<div class="tool" id="tl{i}" style="opacity:0">{t}</div>' for i, t in enumerate(tools))
    js = chapter_js(0.0, T(801.8))
    js += f'''gsap.set("#scrwrap",{{opacity:0}}); LM.cursorAt(800,500); LM.cam(tl,{T(801.6)},"circle",0.9); LM.screenIn(tl,{T(801.7)});
      LM.zoom(tl,{T(806.4)},300,190,2.2,1.2); LM.move(tl,{T(807)},300,190,0.8);
      LM.pop(tl,"#k0",{T(811.1)}); tl.to("#k0",{{opacity:0,duration:0.3}},{T(814.4)});
      LM.move(tl,{T(813.6)},322,190,0.4); LM.click(tl,{T(814.4)});
      tl.set("#tgc",{{attr:{{class:""}}}},{T(814.5)}); tl.set("#tgk",{{attr:{{class:"on"}}}},{T(814.5)});
      LM.pop(tl,"#k1",{T(814.8)}); tl.to("#k1",{{opacity:0,duration:0.3}},{T(817.8)});
      LM.zoom(tl,{T(815.2)},null,0,1,1.0);
      tl.to("#pK",{{opacity:1,duration:0.35}},{T(815.6)}); tl.set("#url",{{textContent:"claude.ai/code"}},{T(815.6)});
      LM.pop(tl,"#k2",{T(818.2)}); tl.to("#k2",{{opacity:0,duration:0.3}},{T(824.6)});
      document.getElementById("cth").innerHTML={js_str('<div class="ub">' + user + '</div>' + tl_html)};
      tl.set("#cth .ub",{{opacity:0}},0);
      LM.zoom(tl,{T(825.4)},800,330,1.35,1.2);
      LM.type(tl,{T(825.6)},"#ctyped",{js_str(user)},22);
      tl.set("#ctyped",{{textContent:""}},{T(830.6)}); tl.to("#cth .ub",{{opacity:1,duration:0.3}},{T(830.6)});
      [{T(842.0)},{T(845.5)},{T(849.9)},{T(854.0)},{T(856.2)}].forEach((t,i)=>LM.rise(tl,"#tl"+i,t,0.4));
      LM.pop(tl,"#k3",{T(848.0)}); tl.to("#k3",{{opacity:0,duration:0.3}},{T(858.6)});'''
    js += screen_close(T(860.6))
    return html, js


@beat("b16", 862.0, 880.0, bg="none")
def _(T):
    html = '<div class="lower" id="lt"><small>скоро · передзапис</small>Міні-курс: AI-монтаж + каруселі</div>'
    return html, f'LM.rise(tl,"#lt",0.4); LM.fadeOut(tl,"#lt",{T(879.0)},0.5);'


def phone(i, x, y, src, ms, dur, w=250):
    h = int(w * 16 / 9)
    return (f'<div id="pf{i}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:28px;overflow:hidden;'
            f'box-shadow:0 0 0 7px #1a1e27,0 30px 60px -20px rgba(0,0,0,.45);background:#000;opacity:0">'
            f'<video class="clip" src="assets/{src}.mp4" data-start="0" data-duration="{dur:.2f}" data-media-start="{ms}" muted playsinline style="width:{w}px;height:{h}px;object-fit:cover"></video></div>')


@beat("b17", 899.0, 945.6)
def _(T):
    E = T(945.6)
    d = 945.6 - 899.0
    ph = (phone(0, 90, 230, "REEL-12", 15, d) + phone(1, 380, 230, "REEL-21", 25, d) + phone(2, 670, 230, "REEL-15", 42, d) + phone(3, 960, 230, "REEL-18", 27, d))
    html = chapter_html("ЧАСТИНА 04", "Стиль для <em>рілсів</em>") + ph
    js = chapter_js(0.0, T(904.2))
    js += f'''LM.cam(tl,{T(904.0)},"card",0.9);
      document.getElementById("stage").insertAdjacentHTML("beforeend",'<div class="gtitle" id="gt" style="left:80px;top:70px;opacity:0"><span class="dot"></span>Анімація: де живуть елементи</div>');
      LM.rise(tl,"#gt",{T(904.4)});
      LM.pop(tl,"#pf0",{T(924.0)}); LM.xt(tl,{T(924.4)},199,632,"перед тобою",36,"#a81428",{{center:1}});
      LM.pop(tl,"#pf1",{T(927.2)}); LM.xt(tl,{T(927.6)},458,632,"за тобою",36,"#a81428",{{center:1}});
      LM.pop(tl,"#pf2",{T(930.1)}); LM.xt(tl,{T(930.5)},717,632,"на весь екран",36,"#a81428",{{center:1}});
      LM.pop(tl,"#pf3",{T(937.9)}); LM.xt(tl,{T(938.3)},976,632,"ти в кружечку",36,"#a81428",{{center:1}});
      tl.to(["#gt","#pf0","#pf1","#pf2","#pf3","#stage div"],{{opacity:0,duration:0.35}},{E - 0.85}); LM.cam(tl,{E - 0.9},"full",0.8);'''
    return html, js


def ig_page():
    return '''<div style="position:absolute;inset:0;background:#fff;font-family:Inter">
      <div style="position:absolute;left:0;top:0;bottom:0;width:240px;border-right:1px solid #eee;padding:30px 24px;font:600 26px Lora">Instagram
        <div style="font:400 17px Inter;margin-top:40px;line-height:2.6">Home<br>Search<br>Explore<br><b>Reels</b><br>Messages<br>Notifications<br>Create<br>Profile</div></div>
      <div style="position:absolute;left:600px;top:24px;width:372px;height:662px;border-radius:12px;overflow:hidden;background:#000">
        <video class="clip" src="assets/REEL-22.mp4" data-start="0" data-duration="60" data-media-start="2" muted playsinline style="width:372px;height:662px;object-fit:cover"></video></div>
      <div style="position:absolute;left:992px;top:330px;font:400 15px Inter;color:#111;line-height:2.4;text-align:center">♡<br>12.4k<br>💬<br>318<br><span id="shr">➤</span><br>…</div>
      <div id="menu" style="position:absolute;left:1030px;top:300px;width:300px;background:#fff;border-radius:14px;box-shadow:0 12px 40px rgba(0,0,0,.2);opacity:0;font:400 16px Inter;overflow:hidden">
        <div style="padding:16px 20px;border-bottom:1px solid #eee;font-weight:600;text-align:center">Поділитися</div>
        <div style="padding:14px 20px;border-bottom:1px solid #eee">Надіслати в Direct</div>
        <div id="cpl" style="padding:14px 20px;border-bottom:1px solid #eee">🔗 Копіювати посилання</div>
        <div style="padding:14px 20px">Поділитися в історії</div></div>
      <div id="copied" style="position:absolute;left:640px;bottom:40px;background:#262626;color:#fff;border-radius:10px;padding:12px 22px;font:500 15px Inter;opacity:0">Посилання скопійовано</div></div>'''


def tg_page():
    return '''<div style="position:absolute;inset:0;background:#fff;font-family:Inter">
      <div style="position:absolute;left:0;top:0;bottom:0;width:380px;border-right:1px solid #e6e6e6">
        <div style="margin:14px;height:40px;border-radius:20px;background:#f1f1f1;color:#999;padding:10px 18px;font:400 15px Inter">Search</div>
        <div style="display:flex;gap:12px;padding:10px 14px;background:#3390ec;color:#fff"><b style="width:52px;height:52px;border-radius:50%;background:#fff;color:#3390ec;display:flex;align-items:center;justify-content:center;font:700 20px Inter">S</b>
          <div style="font:600 16px Inter">SaveAsBot<div style="font:400 14px Inter;opacity:.85">Send me a link…</div></div></div>
        <div style="display:flex;gap:12px;padding:10px 14px"><b style="width:52px;height:52px;border-radius:50%;background:#e1306c"></b><div style="font:600 16px Inter">Мирослава<div style="font:400 14px Inter;color:#888">дякую! 🙏</div></div></div>
        <div style="display:flex;gap:12px;padding:10px 14px"><b style="width:52px;height:52px;border-radius:50%;background:#21a038"></b><div style="font:600 16px Inter">Saved Messages<div style="font:400 14px Inter;color:#888">photo</div></div></div></div>
      <div style="position:absolute;left:380px;right:0;top:0;bottom:0;background:#e7ebd8 linear-gradient(135deg,#dfe8c9,#c9dcc0)">
        <div style="height:58px;background:#fff;padding:10px 20px;font:600 17px Inter">SaveAsBot<div style="font:400 14px Inter;color:#888">bot</div></div>
        <div id="tgm1" style="position:absolute;right:30px;top:120px;background:#eeffde;border-radius:14px;padding:10px 14px;font:400 16px Inter;color:#2b5;opacity:0">
          <u style="color:#3390ec">instagram.com/reel/DPx2k8sAa1Q/</u></div>
        <div id="tgm2" style="position:absolute;left:30px;top:200px;background:#fff;border-radius:14px;padding:8px;opacity:0;width:300px">
          <div style="width:284px;height:505px;border-radius:10px;overflow:hidden;background:#000;position:relative">
            <video class="clip" src="assets/REEL-22.mp4" data-start="0" data-duration="60" data-media-start="0" muted playsinline style="width:284px;height:505px;object-fit:cover"></video></div>
          <div style="font:400 14px Inter;color:#555;padding:8px 6px 2px">🎬 REEL-22.mp4 · 18.4 MB · ⬇</div></div>
        <div style="position:absolute;left:0;right:0;bottom:0;height:62px;background:#fff;padding:20px;color:#999;font:400 16px Inter" id="tgin">Message</div></div></div>'''


@beat("b18", 945.6, 999.6, bg="desk", cout=True)
def _(T):
    page = (f'<div id="pI" style="position:absolute;inset:0">{ig_page()}</div>'
            f'<div id="pT" style="position:absolute;inset:0;opacity:0">{tg_page()}</div>'
            f'<div id="pK" style="position:absolute;inset:0;opacity:0">{code_page("Стиль рілсів")}</div>')
    html = screen(page, ["Claude Code", "Instagram", "Telegram"], "Instagram", "instagram.com/reel/DPx2k8sAa1Q/")
    for i, (t, light) in enumerate([("секретний промт + телеграм-бот", 0), ("3–5 рілсів, які реально подобаються", 1), ("стиль? анімація? шрифт?", 0), ("@SaveAsBot → відео", 1)]):
        html += f'<div class="chip{" light" if light else ""}" id="k{i}" style="left:120px;top:60px;z-index:60;opacity:0">{t}</div>'
    js = screen_open()
    js += f'''LM.cursorAt(900,600);
      LM.pop(tl,"#k0",0.6); tl.to("#k0",{{opacity:0,duration:0.3}},{T(950.4)});
      LM.move(tl,{T(955.0)},1000,477,0.9); LM.click(tl,{T(956.0)}); tl.to("#menu",{{opacity:1,duration:0.25}},{T(956.1)});
      LM.zoom(tl,{T(956.2)},1100,460,1.6,0.9);
      LM.move(tl,{T(957.2)},1150,496,0.5); LM.click(tl,{T(957.9)}); tl.to("#menu",{{opacity:0,duration:0.2}},{T(958.1)});
      tl.to("#copied",{{opacity:1,duration:0.2}},{T(958.2)}); tl.to("#copied",{{opacity:0,duration:0.3}},{T(960.6)});
      LM.zoom(tl,{T(959.0)},null,0,1,0.9);
      LM.pop(tl,"#k1",{T(959.9)}); tl.to("#k1",{{opacity:0,duration:0.3}},{T(964.6)});
      LM.pop(tl,"#k2",{T(965.0)}); tl.to("#k2",{{opacity:0,duration:0.3}},{T(980.4)});
      tl.set(".tab[data-tab=Instagram]",{{attr:{{class:"tab"}}}},{T(981.0)}); tl.set(".tab[data-tab=Telegram]",{{attr:{{class:"tab on"}}}},{T(981.0)});
      tl.set("#url",{{textContent:"web.telegram.org/k/#@SaveAsBot"}},{T(981.0)}); tl.set("#pT",{{opacity:1}},{T(981.0)});
      LM.pop(tl,"#k3",{T(981.2)}); tl.to("#k3",{{opacity:0,duration:0.3}},{T(991.6)});
      LM.move(tl,{T(981.4)},900,846,0.6); LM.click(tl,{T(982.0)});
      LM.type(tl,{T(982.2)},"#tgin","instagram.com/reel/DPx2k8sAa1Q/",30);
      tl.set("#tgin",{{textContent:"Message"}},{T(984.0)}); LM.pop(tl,"#tgm1",{T(984.0)},0.35);
      LM.pop(tl,"#tgm2",{T(986.4)},0.5); LM.zoom(tl,{T(986.6)},700,500,1.35,1.0);
      LM.move(tl,{T(989.0)},640,820,0.6); LM.click(tl,{T(989.8)});
      LM.zoom(tl,{T(990.6)},null,0,1,0.8);
      tl.set(".tab[data-tab=Telegram]",{{attr:{{class:"tab"}}}},{T(992.5)}); tl.set(".tab[data-tab='Claude Code']",{{attr:{{class:"tab on"}}}},{T(992.5)});
      tl.set("#url",{{textContent:"claude.ai/code"}},{T(992.5)}); tl.set("#pK",{{opacity:1}},{T(992.5)});
      document.getElementById("catts").innerHTML='<span class="att file" id="vf"><b></b>REEL-22.mp4<br>18.4 MB</span>';
      LM.pop(tl,"#vf",{T(995.2)});
      tl.set("#cph",{{display:"none"}},{T(997.6)});
      LM.zoom(tl,{T(996.6)},800,760,1.45,1.0);
      LM.type(tl,{T(997.7)},"#ctyped",{js_str(P3[:150])},75);'''
    return html, js


@beat("b19", 999.6, 1105.4, bg="desk", cin=True)
def _(T):
    page = code_page("Стиль рілсів")
    html = screen(page, ["Claude Code", "Instagram", "Telegram"], "Claude Code", "claude.ai/code")
    rows = [("01", "0.0–1.2", "хук: текст зверху, pop + blur→sharp", "spring 0.4s"), ("02", "1.2–2.6", "плитка-іконка над головою", "slide ↓ 0.3s"),
            ("03", "2.6–4.1", "предмет за спиною (маска)", "fade + scale"), ("04", "4.1–5.3", "takeover на весь екран, бордо", "iris 0.5s"),
            ("05", "5.3–6.0", "цифра 176px, градієнт", "count-up"), ("06", "6.0–7.4", "повернення до мене, субтитри", "cut на біт")]
    tr = "".join(f'<tr id="sr{i}" style="opacity:0"><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for i, (a, b, c, d) in enumerate(rows))
    thread = (f'<div class="ub" style="max-width:760px">{P3[:150]}…  <span class="att file" style="width:auto;height:auto;margin:6px 0 0;display:inline-block;padding:6px 10px"><b style="display:inline-block;width:12px;height:14px;margin:0 6px -2px 0"></b>REEL-22.mp4</span></div>'
              '<div class="tool" id="t0" style="opacity:0">Bash <code>ffmpeg -i REEL-22.mp4 -vf "select=gt(scene\\,0.3)" scenes/</code> → 38 сцен</div>'
              '<div class="tool" id="t1" style="opacity:0">Read <code>scenes/001.jpg … 038.jpg</code></div>'
              f'<table class="sc" id="tb" style="opacity:0"><tr><th>#</th><th>таймкод</th><th>що в кадрі</th><th>анімація</th></tr>{tr}</table>'
              '<div class="ub" id="u2" style="opacity:0;margin-top:16px">Згенеруй перші 10 секунд у моєму стилі</div>'
              '<div class="tool" id="t2" style="opacity:0">Write <code>reels-style.md</code> · Render <code>preview_10s.mp4</code></div>')
    vid = (f'<div id="pv" style="position:absolute;left:800px;top:80px;width:280px;height:498px;border-radius:16px;overflow:hidden;background:#000;opacity:0;box-shadow:0 20px 50px -10px rgba(0,0,0,.4)">'
           f'<video class="clip" src="assets/REEL-26.mp4" data-start="0" data-duration="{1105.4 - 999.6:.2f}" data-media-start="5" muted playsinline style="width:280px;height:498px;object-fit:cover"></video></div>')
    html = html.replace('<div class="thread" id="cth" style="left:60px;width:1080px;top:76px"></div>',
                        f'<div class="thread" id="cth" style="left:60px;width:980px;top:76px">{thread}</div>{vid}')
    fb = ["вирізай мене краще", "субтитри менше", "ти не використав мої кольори — світліше"]
    html += "".join(f'<div class="chip light" id="f{i}" style="left:{110 + i * 30}px;top:{70 + i * 84}px;z-index:60;opacity:0">«{t}»</div>' for i, t in enumerate(fb))
    for i, (t, x, y) in enumerate([("зверху", 1190, 330), ("за мною", 1190, 420), ("на весь екран", 1190, 510)]):
        html += f'<div class="chip" id="L{i}" style="left:{x}px;top:{y}px;z-index:60;opacity:0;font-size:26px;padding:10px 20px">{t}</div>'
    html += '<div class="chip" id="n1" style="left:120px;top:60px;z-index:60;opacity:0">10–15 спроб до результату</div>'
    html += '<div class="chip light" id="n2" style="left:120px;top:60px;z-index:60;opacity:0">клієнтці — AI-монтаж за 15 хвилин</div>'
    js = f'''tl.set("#ctyped",{{textContent:""}},0); tl.set("#cph",{{display:"block"}},0);
      LM.zoom(tl,0.2,null,0,1,0.6);
      LM.rise(tl,"#t0",{T(1001.0)},0.4); LM.rise(tl,"#t1",{T(1005.6)},0.4);
      tl.to("#tb",{{opacity:1,duration:0.2}},{T(1008.6)});
      [0,1,2,3,4,5].forEach(i=>LM.fadeIn(tl,"#sr"+i,{T(1009.5)}+i*0.9,0.3));
      LM.zoom(tl,{T(1009.8)},560,520,1.45,1.2);
      LM.zoom(tl,{T(1019.4)},null,0,1,0.9);
      LM.rise(tl,"#u2",{T(1021.6)},0.4);
      LM.rise(tl,"#t2",{T(1023.7)},0.4);
      tl.to("#cth",{{y:-240,duration:1.0,ease:"power3.inOut"}},{T(1023.0)});
      LM.pop(tl,"#pv",{T(1025.0)},0.6);
      LM.zoom(tl,{T(1027.6)},1270,470,1.25,1.2);
      LM.pop(tl,"#L0",{T(1031.7)}); LM.pop(tl,"#L1",{T(1034.6)}); LM.pop(tl,"#L2",{T(1036.8)});
      tl.to(["#L0","#L1","#L2"],{{opacity:0,duration:0.3}},{T(1050.8)});
      LM.zoom(tl,{T(1051.2)},null,0,1,1.0);
      LM.pop(tl,"#f0",{T(1060.0)}); LM.pop(tl,"#f1",{T(1064.3)}); LM.pop(tl,"#f2",{T(1073.2)});
      tl.to(["#f0","#f1","#f2"],{{opacity:0,duration:0.3}},{T(1077.4)});
      LM.pop(tl,"#n1",{T(1082.1)}); tl.to("#n1",{{opacity:0,duration:0.3}},{T(1099.0)});
      LM.pop(tl,"#n2",{T(1099.5)});'''
    js += screen_close(T(1105.4))
    return html, js


@beat("b20", 1105.4, 1172.0)
def _(T):
    E = T(1172.0)
    js = theory_open("Що в тебе на руках", 0.4)
    js += f'''
      LM.ex(tl,{T(1109.8)},"rect",[90,200,520,460],{{fill:"#fadee1",stroke:"#a81428",strokeWidth:3}});
      LM.xt(tl,{T(1110)},350,225,"дизайн-система",50,"#a81428",{{center:1}});
      LM.xt(tl,{T(1113.4)},130,320,"• базовий брендбук",42); LM.xt(tl,{T(1115.1)},130,385,"• каруселі",42); LM.xt(tl,{T(1116.9)},130,450,"• інші статичні секції",42);
      LM.ex(tl,{T(1120.7)},"rect",[680,200,520,460],{{fill:"#a5d8ff",stroke:"#1971c2",strokeWidth:3}});
      LM.xt(tl,{T(1121)},940,225,"reels StyleMD",50,"#1971c2",{{center:1}});
      LM.xt(tl,{T(1125.1)},720,320,"• анімація",42); LM.xt(tl,{T(1127.5)},720,385,"• елементи",42); LM.xt(tl,{T(1129.0)},720,450,"• рендер",42);
      LM.xt(tl,{T(1138.2)},120,720,"каруселі — вже можна постити ✓",48,"#2f9e44");
      LM.clearScene(tl,{T(1152.6)}); LM.scene();
      LM.xt(tl,{T(1153)},110,200,"для монтажу ще:",54,"#1e1e1e");
      ["скіли","рендер у хмарі","GitHub","працює з телефону"].forEach((n,i)=>{{
        const t=[{T(1158.6)},{T(1159.4)},{T(1161.0)},{T(1166.9)}][i];
        LM.ex(tl,t,"rect",[120,300+i*110,46,46],{{stroke:"#a81428",strokeWidth:3}});
        LM.ex(tl,t+0.3,"path","M128 "+(322+i*110)+" L142 "+(338+i*110)+" L172 "+(296+i*110),{{stroke:"#2f9e44",strokeWidth:5}});
        LM.xt(tl,t+0.2,200,298+i*110,n,46);
      }});'''
    js += theory_close(E)
    return "", js


@beat("b21", 1172.0, 1201.6, bg="wine")
def _(T):
    E = T(1201.6)
    html = '''<div id="ec" style="position:absolute;left:110px;top:220px;width:1100px;font-family:PS;color:#fff">
      <div id="e0" style="font:700 26px PS;letter-spacing:.2em;color:#ffc2cf;opacity:0">ПЕРЕДПРОДАЖ · МІНІ-КУРС</div>
      <div id="e1" style="font:700 150px/1 PS;letter-spacing:-.03em;margin-top:24px;opacity:0">AI-монтаж</div>
      <div id="e2" style="font:500 46px/1.25 PS;margin-top:30px;opacity:0;color:rgba(255,255,255,.9)">Монтуй рілси з Claude<br>у своєму стилі</div>
      <div id="e3" class="chip light" style="position:relative;display:inline-block;margin-top:56px;opacity:0;font-size:36px">Посилання в описі ↓</div></div>'''
    js = f'''LM.flash(tl,0.25); LM.cam(tl,0.1,"card",0.9);
      LM.rise(tl,"#e0",{T(1174.2)}); LM.rise(tl,"#e1",{T(1177.4)},0.8); LM.rise(tl,"#e2",{T(1181.9)}); LM.pop(tl,"#e3",{T(1198.6)});
      tl.to("#ec",{{opacity:0,duration:0.35}},{E - 0.85}); LM.cam(tl,{E - 0.9},"full",0.8);'''
    return html, js


@beat("b22", 1201.6, 1223.0)
def _(T):
    E = T(1223.0)
    js = theory_open("Твій перший крок", 0.4)
    js += f'''
      LM.xt(tl,{T(1207.4)},110,240,"використай те, що я описала",50);
      LM.ex(tl,{T(1210.5)},"rect",[110,360,330,410],{{fill:"#fadee1",stroke:"#a81428",strokeWidth:3}});
      LM.xt(tl,{T(1210.8)},275,520,"твоя перша\\nкарусель",44,"#a81428",{{center:1}});
      LM.ex(tl,{T(1211.6)},"arrow",[470,560,680,560]);
      LM.xt(tl,{T(1212.0)},700,520,"відміть мене ♡",60,"#a81428");
      LM.xt(tl,{T(1215.3)},700,640,"краще за будь-які лайки",40,"#5c6678");'''
    js += theory_close(E)
    return "", js


# ===================================================================== emit
PAGE = '''<!doctype html>
<html lang="uk"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width=1920, height=1080"/>
<script src="assets/gsap.min.js"></script><script src="assets/rough.js"></script>
<link rel="stylesheet" href="assets/excalifont.css"/><link rel="stylesheet" href="assets/lib.css"/>
<script src="assets/lib.js"></script>
</head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="%(dur).3f" data-width="1920" data-height="1080">
  <div id="bg" class="clip %(bg)s" data-start="0" data-duration="%(dur).3f" style="opacity:0"></div>
  <div id="stage" class="clip" data-start="0" data-duration="%(dur).3f">
    <svg id="ex" width="1920" height="1080"></svg>
    %(html)s
  </div>
  <div id="camring"></div>
  <video id="cam" class="clip" src="cam.mp4" data-start="0" data-duration="%(dur).3f" data-media-start="0" muted playsinline></video>
  <div id="dim" class="clip" data-start="0" data-duration="%(dur).3f"></div>
  <div id="flash" class="clip" data-start="0" data-duration="%(dur).3f"></div>
</div>
<script>
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });
LM.camSet("full");
%(bgin)s
%(js)s
tl.set({}, {}, %(dur).3f);
%(root)s
</script></body></html>
'''


def emit(b):
    d = os.path.join(OUT, b["id"])
    os.makedirs(d, exist_ok=True)
    T = lambda x: round(x - b["t0"], 3)
    html, js = b["fn"](T)
    dur = b["t1"] - b["t0"]
    nf = round(dur * FPS)
    dur = nf / FPS
    bgin = ""
    if b["bg"] != "none":
        bgin = ('gsap.set("#bg",{opacity:1});' if b["cin"] else 'tl.to("#bg",{opacity:1,duration:0.4},0.05);')
        if not b["cout"]:
            bgin += 'tl.to("#bg",{opacity:0,duration:0.5},%.3f);' % (dur - 0.75)
    if b["cin"]:
        bgin += 'LM.camSet("circle"); LM.cursorAt(800,600);'
    page = PAGE % dict(dur=dur, bg=b["bg"], html=html, js=js, bgin=bgin, root='window.__timelines["main"] = tl;')
    open(os.path.join(d, "index.html"), "w").write(page)
    # Rendering wants ~8 MB of temp disk per frame, so a beat renders in parts
    # of PART seconds: same page, the root timeline scrubs a window of `tl`.
    pd = os.path.join(d, "parts")
    shutil.rmtree(pd, ignore_errors=True)
    nparts = -(-nf // (PART * FPS))
    for k in range(nparts):
        f0 = k * PART * FPS
        f1 = min(nf, f0 + PART * FPS)
        off, pdur = f0 / FPS, (f1 - f0) / FPS
        root = ('const root = gsap.timeline({paused:true});'
                'root.add(tl.tweenFromTo(%.4f, %.4f, {ease:"none", duration:%.4f}), 0);'
                'window.__timelines["main"] = root;' % (off, off + pdur, pdur))
        pg = PAGE % dict(dur=dur, bg=b["bg"], html=html, js=js, bgin=bgin, root=root)
        pg = re.sub(r'data-media-start="([0-9.]+)"', lambda m: 'data-media-start="%.4f"' % (float(m.group(1)) + off), pg)
        pg = re.sub(r'data-duration="[0-9.]+"', 'data-duration="%.4f"' % pdur, pg)
        q = os.path.join(pd, "p%02d" % k)
        os.makedirs(q)
        open(os.path.join(q, "index.html"), "w").write(pg)
        for f in ("hyperframes.json", "package.json"):
            shutil.copy(os.path.join(HERE, "hf", f), q)
        json.dump({"id": "lm-%s-%d" % (b["id"], k), "name": "lm-%s-%d" % (b["id"], k)}, open(os.path.join(q, "meta.json"), "w"))
        os.symlink(os.path.join(HERE, "hf", "assets"), os.path.join(q, "assets"))
        os.symlink(os.path.join(d, "cam.mp4"), os.path.join(q, "cam.mp4"))
    for f in ("hyperframes.json", "package.json"):
        shutil.copy(os.path.join(HERE, "hf", f), d)
    json.dump({"id": "lm-" + b["id"], "name": "lm-" + b["id"]}, open(os.path.join(d, "meta.json"), "w"))
    link = os.path.join(d, "assets")
    if not os.path.islink(link):
        os.symlink(os.path.join(HERE, "hf", "assets"), link)
    cam = os.path.join(d, "cam.mp4")
    stamp = f"{b['t0']:.3f}-{nf}"
    st = cam + ".stamp"
    if not (os.path.exists(cam) and os.path.exists(st) and open(st).read() == stamp):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{b['t0']:.3f}", "-i", PLATE, "-frames:v", str(nf),
                        "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-g", "15", cam], check=True)
        open(cam + ".stamp", "w").write(stamp)
    json.dump({"t0": b["t0"], "t1": b["t0"] + dur, "frames": nf}, open(os.path.join(d, "beat.json"), "w"))
    print("built", b["id"], f"{dur:.1f}s")


def prep_reels():
    rd = os.path.join(HERE, "hf", "assets")
    if not os.path.isdir(REELS):
        return
    for f in sorted(os.listdir(REELS)):
        o = os.path.join(rd, f)
        if f.endswith(".mp4") and not os.path.exists(o):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(REELS, f), "-vf", "scale=540:960,fps=30",
                            "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-g", "15", o], check=True)


if __name__ == "__main__":
    prep_reels()
    want = sys.argv[1:]
    for b in BEATS:
        if not want or b["id"] in want:
            emit(b)
