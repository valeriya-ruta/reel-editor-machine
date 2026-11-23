// One camera over the whole world. A framing is "world point (cx, cy) shown at
// frame point (540, ay) at zoom z". Shots move between framings with a named
// transition; while a shot holds, the camera keeps drifting in, and any hold
// longer than ~1.3s gets an automatic punch-in so no framing sits still.

import type {Box, World} from '../objects/core';
import {clamp, inOut, inOutSine, lerp, outCubic, prog} from './ease';
import type {EpisodeSpec, Shot, Timeline} from './types';

export const FRAME_W = 1080;
export const FRAME_H = 1920;

export type Cam = {cx: number; cy: number; z: number; ay: number};
export type CamOut = {tx: number; ty: number; z: number; blurX: number; blurY: number};

type WorldAt = (t: number) => World;

const fit = (b: Box, bw: number, bh: number, ay: number): Cam => ({
  cx: b.x + b.w / 2,
  cy: b.y + b.h / 2,
  z: clamp(Math.min(bw / b.w, bh / b.h), 0.25, 8),
  ay,
});

const firstOfType = (w: World, type: string) => Object.values(w.objects).find((o) => o.type === type)?.id;

/** Shots whose framing tracks the live state of the world every frame. */
const isLive = (s: Shot) => s.via === 'follow' || s.preset === 'input_close';

export const framing = (spec: EpisodeSpec, shot: Shot, w: World): Cam => {
  let cam: Cam;
  const [tid, anchor] = (shot.target ?? '').split('#');
  switch (shot.preset) {
    case 'room': {
      const r = spec.scene.rooms[shot.target ?? 'default'] ?? spec.scene.rooms.default;
      cam = fit({x: r[0], y: r[1], w: r[2] - r[0], h: r[3] - r[1]}, 1020, 860, 940);
      break;
    }
    case 'screen': {
      const b = w.boundsOf(tid || firstOfType(w, 'laptop') || '', anchor || 'screen');
      cam = b ? fit(b, 1010, 1300, 930) : {cx: 540, cy: 960, z: 1, ay: 900};
      break;
    }
    case 'input_close': {
      const b = w.boundsOf(tid || firstOfType(w, 'laptop') || '', 'caret');
      cam = b ? {cx: b.x + b.w / 2, cy: b.y + b.h / 2, z: 2.9, ay: 900} : {cx: 540, cy: 960, z: 1, ay: 900};
      break;
    }
    case 'character_close': {
      const b = w.boundsOf(tid || firstOfType(w, 'chibi') || '', anchor || 'upper');
      cam = b ? fit(b, 980, 900, 960) : {cx: 540, cy: 960, z: 1, ay: 900};
      break;
    }
    case 'phone_dive': {
      const b = w.boundsOf(tid || firstOfType(w, 'phone') || '', anchor || 'screen');
      cam = b ? fit(b, 900, 1560, 980) : {cx: 540, cy: 960, z: 1, ay: 900};
      break;
    }
    case 'object_punch':
    default: {
      const b = w.boundsOf(tid, anchor);
      cam = b ? fit(b, 860, 680, 900) : {cx: 540, cy: 960, z: 1, ay: 900};
    }
  }
  const z = clamp(cam.z * shot.zoom, 0.25, 9);
  return {cx: cam.cx - shot.dx / z, cy: cam.cy - shot.dy / z, z, ay: cam.ay};
};

const EASES: Record<string, (p: number) => number> = {
  cut: () => 1,
  punch: inOutSine,
  whip: inOutSine,
  follow: inOut,
  ease: inOut,
  pull_back: inOutSine,
};

const mix = (a: Cam, b: Cam, e: number): Cam => ({
  cx: lerp(a.cx, b.cx, e),
  cy: lerp(a.cy, b.cy, e),
  z: Math.exp(lerp(Math.log(a.z), Math.log(b.z), e)),
  ay: lerp(a.ay, b.ay, e),
});

const BREATH = 1.25; // seconds per re-framing during a long hold
// Long holds just drift now: the auto punch-ins read as jitter (her note).
const BREATH_ZOOM = 1;

type Cache = {fixed: Map<number, Cam>; start: Map<number, Cam>};
const caches = new WeakMap<Timeline, Cache>();

const cacheFor = (tl: Timeline): Cache => {
  let c = caches.get(tl);
  if (!c) {
    c = {fixed: new Map(), start: new Map()};
    caches.set(tl, c);
  }
  return c;
};

const shotIndex = (tl: Timeline, t: number) => {
  let i = 0;
  while (i < tl.shots.length - 1 && t >= tl.shots[i + 1].t0) i++;
  return i;
};

const targetCam = (spec: EpisodeSpec, tl: Timeline, i: number, t: number, worldAt: WorldAt): Cam => {
  const shot = tl.shots[i];
  if (isLive(shot)) return framing(spec, shot, worldAt(t));
  const c = cacheFor(tl);
  let cam = c.fixed.get(i);
  if (!cam) {
    cam = framing(spec, shot, worldAt(shot.t0 + shot.transDur));
    c.fixed.set(i, cam);
  }
  return cam;
};

const camInShot = (spec: EpisodeSpec, tl: Timeline, i: number, t: number, worldAt: WorldAt): Cam => {
  const shot = tl.shots[i];
  const end = targetCam(spec, tl, i, t, worldAt);
  let cam = end;
  if (i > 0 && shot.via !== 'cut' && t < shot.t0 + shot.transDur) {
    const c = cacheFor(tl);
    let from = c.start.get(i);
    if (!from) {
      from = camInShot(spec, tl, i - 1, shot.t0, worldAt);
      c.start.set(i, from);
    }
    const e = (EASES[shot.via] ?? inOut)(prog(t, shot.t0, shot.transDur));
    cam = mix(from, end, e);
  }
  // hold life: slow push-in, a little sway, and re-framing punches on long holds
  const holdStart = shot.t0 + shot.transDur;
  const hold = t - holdStart;
  if (hold > 0) {
    const total = shot.t1 - holdStart;
    let z = cam.z * (1 + 0.02 * hold);
    if (total > 1.5) {
      const k = Math.floor(hold / BREATH);
      const local = hold - k * BREATH;
      const cur = k % 2 === 1 ? BREATH_ZOOM : 1;
      const prev = k === 0 ? 1 : (k - 1) % 2 === 1 ? BREATH_ZOOM : 1;
      z *= lerp(prev, cur, inOut(clamp(local / 0.3)));
    }
    const sway = Math.sin(hold * 0.7 + i * 1.7) * 5;
    cam = {...cam, z, cx: cam.cx + sway / z};
  }
  return cam;
};

const impactAt = (tl: Timeline, t: number) => {
  let x = 0;
  let y = 0;
  let bump = 1;
  for (const ev of tl.events) {
    if (!ev.impact) continue;
    const land = ev.t0 + ev.dur;
    const q = (t - land) / 0.3;
    if (q < 0 || q > 1) continue;
    const a = 7 * (1 - q);
    x += Math.sin(q * Math.PI * 7) * a;
    y += Math.cos(q * Math.PI * 6) * a * 0.6;
    bump *= 1 + 0.04 * Math.sin(Math.PI * q) * (1 - q);
  }
  return {x, y, bump};
};

const camAt = (spec: EpisodeSpec, tl: Timeline, t: number, worldAt: WorldAt) => camInShot(spec, tl, shotIndex(tl, t), t, worldAt);

export const cameraAt = (spec: EpisodeSpec, tl: Timeline, t: number, worldAt: WorldAt): CamOut => {
  const cam = camAt(spec, tl, t, worldAt);
  const dt = 1 / tl.fps;
  const before = camAt(spec, tl, Math.max(0, t - dt), worldAt);
  // screen-space speed of the frame centre, plus zoom speed, becomes motion blur
  const vx = (cam.cx - before.cx) * cam.z;
  const vy = (cam.cy - before.cy) * cam.z;
  const vz = Math.abs(Math.log(cam.z) - Math.log(before.z)) * 260;
  const bx = Math.abs(vx) * 0.25 + vz;
  const by = Math.abs(vy) * 0.25 + vz;
  const imp = impactAt(tl, t);
  const z = cam.z * imp.bump;
  return {
    tx: FRAME_W / 2 - cam.cx * z + imp.x,
    ty: cam.ay - cam.cy * z + imp.y,
    z,
    // no motion blur: smooth moves read better than smeared ones
    blurX: bx > 1e9 ? bx : 0,
    blurY: by > 1e9 ? by : 0,
  };
};
