// Chibi Ruta: an actor, never a speaker. Swaps pose PNGs from public/chibi/
// with a squash-and-stretch pop, bobs gently at idle, and shakes when the pose
// is an agitated one. She stands behind the desk, so the floor hides her below
// the hips; (x, y) is her hip point on the desk line.

import React from 'react';
import {Img} from 'remotion';
import {clamp, wobble} from '../engine/ease';
import type {ObjectDef, RenderProps} from './core';
import {asset} from './style';

const W = 510;
const H = 765; // the pose canvas is 2:3, head-top to knees
const HIP = 0.62;

/** Poses that shake, and how hard (px, Hz). */
const AGITATED: Record<string, [number, number]> = {
  furious: [5, 11],
  panicked: [7, 7],
  waterworks: [4, 9],
  scribbling: [2, 14],
};

const str = (v: unknown, d: string) => (typeof v === 'string' ? v : d);

const Render: React.FC<RenderProps> = ({o, s, t}) => {
  const pose: string = s.pose;
  const dt = t - s.poseT;
  // squash on the change, then a little spring back up
  let sx = 1;
  let sy = 1;
  let hop = 0;
  if (dt >= 0 && dt < 0.6) {
    const k = Math.exp(-dt * 8) * Math.cos(dt * Math.PI * 2 * 2.6);
    sy = 1 - 0.13 * k;
    sx = 1 + 0.1 * k;
    hop = 22 * Math.sin(Math.PI * clamp(dt / 0.32)) * (dt < 0.32 ? 1 : 0);
  }
  const seed = o.id.length;
  const bob = Math.sin(t * Math.PI * 2 * 0.55 + seed) * 5;
  const breathe = 1 + Math.sin(t * Math.PI * 2 * 0.55 + seed) * 0.008;
  const [amp, hz] = AGITATED[pose] ?? [0, 0];
  const shakeX = amp ? Math.sin(t * Math.PI * 2 * hz) * amp : 0;
  const shakeR = amp ? wobble(t * 6, seed) * amp * 0.25 : 0;
  // ecstatic bounces on her own
  const bounce = pose === 'ecstatic' ? Math.abs(Math.sin(t * Math.PI * 2 * 1.6)) * 16 : 0;
  return (
    <div
      style={{
        position: 'absolute',
        inset: 0,
        transformOrigin: `50% ${HIP * 100}%`,
        transform: `translate(${shakeX}px, ${bob - hop - bounce}px) rotate(${shakeR}deg) scale(${sx}, ${sy * breathe})`,
      }}
    >
      <Img src={asset(`chibi/${pose}.png`)} style={{position: 'absolute', left: 0, top: 0, width: W, height: H}} />
    </div>
  );
};

export const Chibi: ObjectDef = {
  size: () => ({w: W, h: H, ax: 0.5, ay: HIP}),
  init: (o) => ({pose: str(o.props?.pose, 'neutral'), poseT: -10}),
  verbs: {
    pose: {
      dur: 0.05,
      required: ['pose'],
      apply: (s, a, c) => (s.pose === a.pose ? s : {...s, pose: a.pose, poseT: c.t0}),
    },
  },
  anchors: () => ({
    upper: {x: 20, y: 0, w: 470, h: 480},
    head: {x: 95, y: 10, w: 320, h: 310},
  }),
  assets: (o) => [`chibi/${str(o.props?.pose, 'neutral')}.png`],
  Render,
};
