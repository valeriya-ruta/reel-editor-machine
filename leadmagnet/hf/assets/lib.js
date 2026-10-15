// Shared motion helpers for the lead-magnet beats. Everything is driven by
// one paused GSAP timeline (`tl`) so the renderer can seek any frame.
(function () {
  const $ = (s) => document.querySelector(s);
  const L = (window.LM = {});

  // ------------------------------------------------------------ camera
  // The plate is one <video id="cam">, 1920x1080. A state is a scale +
  // offset + an inset clip (in plate px), so "full", "card", "circle" are
  // just numbers and every move between them is one tween.
  const CAM = {
    full:   { s: 1, tx: 0, ty: 0, t: 0, r: 0, b: 0, l: 0, rad: 0, ring: 0 },
    card:   { s: 0.78, tx: 848.6, ty: 170, t: 0, r: 630, b: 160, l: 630, rad: 40, ring: 0 },
    circle: { s: 0.3889, tx: 1308.7, ty: 448, t: 0, r: 420, b: 0, l: 420, rad: 67, ring: 1 },
    small:  { s: 0.34, tx: 1630, ty: 790, t: 60, r: 680, b: 460, l: 680, rad: 280, ring: 1 },
  };
  let camNow = Object.assign({}, CAM.full);
  const camObj = Object.assign({}, CAM.full);
  function camApply() {
    const v = $("#cam"), ring = $("#camring");
    if (!v) return;
    const c = camObj;
    v.style.transform = `translate(${c.tx}px,${c.ty}px) scale(${c.s})`;
    v.style.clipPath = `inset(${c.t}px ${c.r}px ${c.b}px ${c.l}px round ${c.rad}px)`;
    if (ring) {
      const w = (1920 - c.l - c.r) * c.s, h = (1080 - c.t - c.b) * c.s;
      ring.style.left = c.tx + c.l * c.s + "px";
      ring.style.top = c.ty + c.t * c.s + "px";
      ring.style.width = w + "px";
      ring.style.height = h + "px";
      ring.style.opacity = c.ring;
      ring.style.borderRadius = c.rad * c.s + "px";
    }
  }
  // Camera moves are evaluated as a pure function of time (one driver tween
  // reads the keyframe list), so seeking in any order gives the same frame.
  const KEYS = [];
  let camBase = Object.assign({}, CAM.full), driver = false;
  function camEval(t) {
    let st = camBase;
    for (const k of KEYS) {
      if (t >= k.at + k.dur) { st = k.to; continue; }
      if (t > k.at) {
        const p = k.ease((t - k.at) / k.dur), o = {};
        for (const n in k.to) o[n] = k.from[n] + (k.to[n] - k.from[n]) * p;
        st = o;
      }
      break;
    }
    Object.assign(camObj, st);
    camApply();
  }
  L.cam = function (tl, at, state, dur = 0.8, ease = "power3.inOut") {
    const to = Object.assign({}, typeof state === "string" ? CAM[state] : state);
    KEYS.push({ at, dur, from: Object.assign({}, camNow), to, ease: gsap.parseEase(ease) });
    KEYS.sort((a, b) => a.at - b.at);
    camNow = Object.assign({}, to);
    if (!driver) {
      driver = true;
      const tlr = tl;
      tl.to({ v: 0 }, { v: 1, duration: 9999, ease: "none", onUpdate: () => camEval(tlr.time()) }, 0);
    }
  };
  L.restScreen = function () {
    if (document.getElementById("scrwrap")) gsap.set("#scrwrap", { x: REST.x - BASE.x, y: REST.y - BASE.y, scale: REST.k });
  };
  L.camSet = function (state) {
    L.restScreen && L.restScreen();
    camBase = Object.assign({}, CAM[state]);
    Object.assign(camObj, CAM[state]);
    camNow = Object.assign({}, CAM[state]);
    camApply();
  };
  L.camHide = function (tl, at, dur = 0.35) { tl.to("#cam", { opacity: 0, duration: dur }, at); };
  L.camShow = function (tl, at, dur = 0.35) { tl.to("#cam", { opacity: 1, duration: dur }, at); };

  // ------------------------------------------------------------ transitions
  L.flash = function (tl, at, peak = 0.9) {
    tl.fromTo("#flash", { opacity: 0 }, { opacity: peak, duration: 0.07, ease: "none", immediateRender: false }, at - 0.07)
      .to("#flash", { opacity: 0, duration: 0.38, ease: "power2.out" }, at);
  };
  L.fadeIn = function (tl, sel, at, dur = 0.5, y = 0) {
    gsap.set(sel, { opacity: 0 });
    tl.fromTo(sel, { opacity: 0, y: y }, { opacity: 1, y: 0, duration: dur, ease: "power2.out", immediateRender: false }, at);
  };
  L.fadeOut = function (tl, sel, at, dur = 0.4) {
    tl.to(sel, { opacity: 0, duration: dur, ease: "power2.in" }, at);
  };
  L.pop = function (tl, sel, at, dur = 0.55) {
    gsap.set(sel, { opacity: 0 });
    tl.fromTo(sel, { opacity: 0, scale: 0.86, filter: "blur(8px)" },
      { opacity: 1, scale: 1, filter: "blur(0px)", duration: dur, ease: "back.out(1.6)", immediateRender: false }, at);
  };
  L.rise = function (tl, sel, at, dur = 0.6) {
    gsap.set(sel, { opacity: 0 });
    tl.fromTo(sel, { opacity: 0, y: 40, filter: "blur(6px)" },
      { opacity: 1, y: 0, filter: "blur(0px)", duration: dur, ease: "power3.out", immediateRender: false }, at);
  };

  // ------------------------------------------------------------ screen camera
  // #scrwrap holds the 1600x900 desktop. zoom(x,y,k): bring desktop point
  // (x,y) to the frame centre at scale k. zoom(null) returns to the rest pose.
  // BASE is #scrwrap's CSS position; REST the pose it sits in at rest:
  // a little smaller and to the left, leaving the right column for the camera.
  const BASE = { x: 160, y: 62 };
  const REST = { x: 40, y: 76, k: 0.88 };
  let zNow = Object.assign({}, REST);
  L.zoom = function (tl, at, x, y, k = 1.6, dur = 1.1) {
    let to;
    if (x === null) to = Object.assign({}, REST);
    else to = { x: 960 - x * k, y: 520 - y * k, k: k };
    tl.fromTo("#scrwrap", { x: zNow.x - BASE.x, y: zNow.y - BASE.y, scale: zNow.k },
      { x: to.x - BASE.x, y: to.y - BASE.y, scale: to.k, duration: dur, ease: "power3.inOut", immediateRender: false }, at);
    zNow = to;
  };
  L.screenIn = function (tl, at, dur = 0.9) {
    const x = REST.x - BASE.x, y = REST.y - BASE.y;
    tl.fromTo("#scrwrap", { opacity: 0, x: x, y: y + 60, scale: REST.k * 0.94 }, { opacity: 1, x: x, y: y, scale: REST.k, duration: dur, ease: "power3.out", immediateRender: false }, at);
  };
  L.screenOut = function (tl, at, dur = 0.5) {
    tl.to("#scrwrap", { opacity: 0, scale: REST.k * 0.96, duration: dur, ease: "power2.in" }, at);
  };

  // ------------------------------------------------------------ cursor
  let cNow = { x: 900, y: 600 };
  L.cursorAt = function (x, y) { cNow = { x, y }; gsap.set("#cur", { x, y }); };
  L.move = function (tl, at, x, y, dur = 0.8) {
    tl.fromTo("#cur", { x: cNow.x, y: cNow.y }, { x, y, duration: dur, ease: "power2.inOut", immediateRender: false }, at);
    cNow = { x, y };
  };
  L.click = function (tl, at) {
    tl.to("#cur", { scale: 0.82, duration: 0.08, yoyo: true, repeat: 1 }, at);
    tl.fromTo("#rip", { x: cNow.x, y: cNow.y, opacity: 0.9, scale: 0.2 },
      { scale: 1.4, opacity: 0, duration: 0.5, ease: "power2.out", immediateRender: false }, at);
    (window.SFX = window.SFX || []).push({ t: at, n: "click" });
  };

  // ------------------------------------------------------------ text
  // type(el, text): reveal characters at ~cps with a blinking caret.
  L.type = function (tl, at, sel, text, cps = 26, caret = true) {
    const el = typeof sel === "string" ? $(sel) : sel;
    const o = { n: 0 };
    const dur = Math.max(0.2, text.length / cps);
    const draw = () => {
      el.textContent = text.slice(0, Math.round(o.n));
      if (caret) { const c = document.createElement("span"); c.className = "caret"; el.appendChild(c); }
    };
    tl.fromTo(o, { n: 0 }, { n: text.length, duration: dur, ease: "none", onUpdate: draw, immediateRender: false }, at);
    (window.SFX = window.SFX || []).push({ t: at, n: "type", d: dur });
    return at + dur;
  };
  // stream(el, html-ish text): word-by-word reveal, like a model reply.
  L.stream = function (tl, at, sel, text, wps = 14) {
    const el = typeof sel === "string" ? $(sel) : sel;
    const words = text.split(/(\s+)/);
    const o = { n: 0 };
    const dur = Math.max(0.3, words.length / 2 / wps);
    const draw = () => { el.innerHTML = words.slice(0, Math.round(o.n)).join(""); };
    tl.fromTo(o, { n: 0 }, { n: words.length, duration: dur, ease: "none", onUpdate: draw, immediateRender: false }, at);
    return at + dur;
  };

  // ------------------------------------------------------------ excalidraw
  // Shapes are drawn with rough.js (seeded, so deterministic), then revealed
  // by animating stroke-dashoffset: a hand drawing it.
  let seed = 7, G = null, D = null, nScene = 0;
  L.scene = function () {
    nScene++;
    G = document.createElementNS("http://www.w3.org/2000/svg", "g");
    G.setAttribute("id", "g" + nScene);
    $("#ex").appendChild(G);
    D = document.createElement("div");
    D.id = "d" + nScene;
    D.style.cssText = "position:absolute;inset:0";
    $("#stage").appendChild(D);
    return nScene;
  };
  L.clearScene = function (tl, at, dur = 0.45) {
    tl.to(["#g" + nScene, "#d" + nScene], { opacity: 0, y: -20, duration: dur, ease: "power2.in" }, at);
  };
  L.ex = function (tl, at, kind, a, opt = {}) {
    if (!G) L.scene();
    const svg = $("#ex");
    const rc = rough.svg(svg);
    const o = Object.assign({ roughness: 1.4, strokeWidth: 2.6, stroke: "#1e1e1e", bowing: 1.2, seed: seed++,
      fillStyle: "hachure", hachureGap: 9, fillWeight: 1.6 }, opt);
    let node;
    if (kind === "rect") node = rc.rectangle(a[0], a[1], a[2], a[3], o);
    else if (kind === "ellipse") node = rc.ellipse(a[0], a[1], a[2], a[3], o);
    else if (kind === "line") node = rc.line(a[0], a[1], a[2], a[3], o);
    else if (kind === "path") node = rc.path(a, o);
    else if (kind === "curve") node = rc.curve(a, o);
    else if (kind === "arrow") {
      const [x1, y1, x2, y2] = a;
      const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
      const mx = (x1 + x2) / 2 + (opt.bend || 0), my = (y1 + y2) / 2 - (opt.bend || 0) * 0.4;
      g.appendChild(rc.curve([[x1, y1], [mx, my], [x2, y2]], o));
      const ang = Math.atan2(y2 - my, x2 - mx), h = 20;
      g.appendChild(rc.line(x2, y2, x2 - h * Math.cos(ang - 0.45), y2 - h * Math.sin(ang - 0.45), o));
      g.appendChild(rc.line(x2, y2, x2 - h * Math.cos(ang + 0.45), y2 - h * Math.sin(ang + 0.45), o));
      node = g;
    }
    G.appendChild(node);
    const paths = node.querySelectorAll("path");
    const dur = opt.dur || 0.6;
    paths.forEach((p, i) => {
      const len = p.getTotalLength ? p.getTotalLength() : 600;
      p.style.strokeDasharray = len + 1;
      p.style.strokeDashoffset = len + 1;
      const isFill = p.getAttribute("stroke") !== o.stroke && opt.fill;
      tl.to(p, { strokeDashoffset: 0, duration: isFill ? dur * 1.2 : dur, ease: "power1.inOut" }, at + (isFill ? dur * 0.5 : 0) + i * 0.01);
    });
    (window.SFX = window.SFX || []).push({ t: at, n: "draw" });
    return node;
  };
  // hand-written label
  L.xt = function (tl, at, x, y, text, size = 34, color = "#1e1e1e", opt = {}) {
    const d = document.createElement("div");
    d.className = "xt";
    d.style.left = x + "px"; d.style.top = y + "px"; d.style.fontSize = size + "px"; d.style.color = color;
    if (opt.center) { d.style.transform = "translateX(-50%)"; d.style.textAlign = "center"; }
    if (opt.w) { d.style.width = opt.w + "px"; d.style.whiteSpace = "normal"; }
    d.textContent = text;
    if (!D) L.scene();
    D.appendChild(d);
    // reveal left-to-right like writing
    tl.fromTo(d, { clipPath: "inset(0 100% 0 0)", opacity: 1 },
      { clipPath: "inset(0 0% 0 0)", duration: opt.dur || Math.min(1.2, 0.18 + text.length * 0.035), ease: "none", immediateRender: false }, at);
    gsap.set(d, { clipPath: "inset(0 100% 0 0)" });
    return d;
  };

  L.sfx = function (at, n, db) { (window.SFX = window.SFX || []).push({ t: at, n: n, db: db }); };
})();
