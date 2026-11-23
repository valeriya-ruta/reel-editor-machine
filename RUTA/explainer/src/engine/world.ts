// Fold each object's events up to time t into its state, and answer "where is
// this object (or a named part of it) in the world right now".

import type {Box, State, World} from '../objects/core';
import {BASE} from '../objects/core';
import {OBJECTS, verbFor} from '../objects/registry';
import {prog} from './ease';
import type {EpisodeSpec, Ev, SceneObject, Timeline} from './types';

export const initialState = (o: SceneObject): State => ({...BASE, vis: o.hidden ? 0 : 1, ...(OBJECTS[o.type]?.init?.(o) ?? {})});

export const stateAt = (o: SceneObject, evs: Ev[], t: number): State => {
  let s = initialState(o);
  for (const ev of evs) {
    if (ev.t0 > t) break;
    const v = verbFor(o.type, ev.verb);
    if (!v) continue;
    s = v.apply(s, ev.args, {t, t0: ev.t0, dur: ev.dur, p: prog(t, ev.t0, ev.dur)}, o);
  }
  return s;
};

export const localBounds = (o: SceneObject, s: State, anchor?: string): Box | null => {
  const def = OBJECTS[o.type];
  if (!def) return null;
  const size = def.size(o);
  const ax = size.ax ?? 0.5;
  const ay = size.ay ?? 1;
  const sc = (o.scale ?? 1) * s.sc;
  const left = o.x + s.dx - ax * size.w * sc;
  const top = o.y + s.dy - ay * size.h * sc;
  const a = anchor ? def.anchors?.(o, s)[anchor] : undefined;
  if (a) return {x: left + a.x * sc, y: top + a.y * sc, w: a.w * sc, h: a.h * sc};
  return {x: left, y: top, w: size.w * sc, h: size.h * sc};
};

export const worldAt = (spec: EpisodeSpec, tl: Timeline, t: number): World => {
  const states: Record<string, State> = {};
  const objects: Record<string, SceneObject> = {};
  for (const o of spec.scene.objects) {
    objects[o.id] = o;
    states[o.id] = stateAt(o, tl.byObj[o.id] ?? [], t);
  }
  const world: World = {
    t,
    states,
    objects,
    boundsOf: (id, anchor) => {
      const o = objects[id];
      if (!o) return null;
      const def = OBJECTS[o.type];
      if (def?.worldBounds && !anchor) return def.worldBounds(o, states[id], world);
      return localBounds(o, states[id], anchor);
    },
  };
  return world;
};
