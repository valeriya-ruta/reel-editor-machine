// What every object in the library is made of: a size, a state that is folded
// from its timed events, verbs that change that state, and a renderer.
// Verbs are pure: given the state so far and a 0..1 progress they return the
// next state, so any frame can be rendered on its own (scrub-safe).

import type {FC} from 'react';
import type {Args, SceneObject} from '../engine/types';
import {clamp, inOut, lerp} from '../engine/ease';

export type Base = {
  /** 0..1 appear progress; `visMode` says whether it is popping in or out. */
  vis: number;
  visMode: 'in' | 'out';
  dx: number;
  dy: number;
  sc: number;
  rot: number;
  shakeT: number;
  shakeDur: number;
  shakeAmp: number;
  pulseT: number;
};
export type State = Base & {[k: string]: any};

export type VerbCtx = {t: number; t0: number; dur: number; p: number};

export type Verb = {
  /** Seconds; `args.dur` always overrides. */
  dur: number | ((args: Args, o: SceneObject) => number);
  apply: (s: State, args: Args, c: VerbCtx, o: SceneObject) => State;
  required?: string[];
  /** The camera gets a micro-shake when this lands (stamp slams, plug clicks). */
  impact?: boolean;
  /** Extra validation; return an error message or null. */
  check?: (args: Args, o: SceneObject) => string | null;
};

export type Box = {x: number; y: number; w: number; h: number};

export type World = {
  t: number;
  states: Record<string, State>;
  objects: Record<string, SceneObject>;
  boundsOf: (id: string, anchor?: string) => Box | null;
};

export type RenderProps = {o: SceneObject; s: State; t: number; world: World};

export type Size = {w: number; h: number; /** anchor point as a fraction of w/h; default bottom-centre */ ax?: number; ay?: number};

export type ObjectDef = {
  size: (o: SceneObject) => Size;
  init?: (o: SceneObject) => Record<string, any>;
  verbs: Record<string, Verb>;
  /** Named sub-rectangles in local (unscaled) coordinates, for punch-ins. */
  anchors?: (o: SceneObject, s: State) => Record<string, Box>;
  /** Objects drawn between two others (cables) know their bounds only from the world. */
  worldBounds?: (o: SceneObject, s: State, world: World) => Box | null;
  /** Pose/asset names the validator should check exist. */
  assets?: (o: SceneObject) => string[];
  /** Draws in world coordinates itself (cables); only fades with show/hide. */
  raw?: boolean;
  Render: FC<RenderProps>;
};

export const BASE: Base = {
  vis: 1,
  visMode: 'in',
  dx: 0,
  dy: 0,
  sc: 1,
  rot: 0,
  shakeT: -1,
  shakeDur: 0,
  shakeAmp: 0,
  pulseT: -1,
};

const num = (v: unknown, d: number) => (typeof v === 'number' ? v : d);

/** Verbs every object understands. */
export const GENERIC: Record<string, Verb> = {
  show: {dur: 0.45, apply: (s, _a, c) => ({...s, vis: c.p, visMode: 'in'})},
  hide: {dur: 0.28, apply: (s, _a, c) => ({...s, vis: 1 - c.p, visMode: 'out'})},
  move: {
    dur: 0.6,
    apply: (s, a, c, o) => {
      const e = inOut(c.p);
      const tx = a.x !== undefined ? num(a.x, o.x) - o.x : s.dx + num(a.dx, 0);
      const ty = a.y !== undefined ? num(a.y, o.y) - o.y : s.dy + num(a.dy, 0);
      // A gentle arc reads as "thrown" rather than "slid".
      const arc = num(a.arc, 0) * Math.sin(Math.PI * e);
      return {...s, dx: lerp(s.dx, tx, e), dy: lerp(s.dy, ty, e) - arc};
    },
  },
  /** Fly to a point (x/y, or another object via `to` — the compiler fills toX/toY), shrinking on arrival. */
  fly: {
    dur: 0.6,
    apply: (s, a, c, o) => {
      const e = inOut(c.p);
      const tx = num(a.x, num(a.toX, o.x)) - o.x;
      const ty = num(a.y, num(a.toY, o.y)) - o.y;
      const arc = num(a.arc, 60) * Math.sin(Math.PI * e);
      return {...s, dx: lerp(s.dx, tx, e), dy: lerp(s.dy, ty, e) - arc, sc: lerp(s.sc, num(a.scale, 0.22), e)};
    },
  },
  scale: {dur: 0.4, required: ['to'], apply: (s, a, c) => ({...s, sc: lerp(s.sc, num(a.to, 1), inOut(c.p))})},
  tilt: {dur: 0.4, required: ['to'], apply: (s, a, c) => ({...s, rot: lerp(s.rot, num(a.to, 0), inOut(c.p))})},
  shake: {dur: 0.5, apply: (s, a, c) => ({...s, shakeT: c.t0, shakeDur: c.dur, shakeAmp: num(a.amp, 10)})},
  pulse: {dur: 0.35, apply: (s, _a, c) => ({...s, pulseT: c.t0})},
};

/** Transform for the generic part of the state: pop, move, shake, pulse. */
export const baseTransform = (s: State, t: number) => {
  let pop = 1;
  let alpha = 1;
  if (s.visMode === 'in') {
    // back-out pop with a little squash on the way up
    const v = s.vis;
    pop = v >= 1 ? 1 : 1 + 2.4 * Math.pow(v - 1, 3) + 1.4 * Math.pow(v - 1, 2);
    pop = Math.max(0, pop);
    alpha = clamp(v * 3);
  } else {
    pop = lerp(0.55, 1, s.vis);
    alpha = clamp(s.vis * 1.6);
  }
  let shake = 0;
  if (s.shakeT >= 0 && t >= s.shakeT && t <= s.shakeT + s.shakeDur) {
    const q = (t - s.shakeT) / s.shakeDur;
    shake = Math.sin((t - s.shakeT) * Math.PI * 2 * 13) * s.shakeAmp * (1 - q);
  }
  let pulse = 1;
  if (s.pulseT >= 0 && t >= s.pulseT && t <= s.pulseT + 0.35) {
    pulse = 1 + 0.12 * Math.sin(((t - s.pulseT) / 0.35) * Math.PI);
  }
  return {pop: pop * pulse * s.sc, alpha, shake};
};
