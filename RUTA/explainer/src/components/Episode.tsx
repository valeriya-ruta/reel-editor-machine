// One episode: a light room with a desk, every scene object placed in world
// coordinates, a single camera over all of it, and captions on top.

import React, {useMemo} from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {cameraAt, FRAME_H, FRAME_W} from '../engine/camera';
import {compile} from '../engine/compile';
import type {EpisodeSpec, SceneObject} from '../engine/types';
import {worldAt} from '../engine/world';
import type {State, World} from '../objects/core';
import {baseTransform} from '../objects/core';
import {OBJECTS} from '../objects/registry';
import {Captions} from './Captions';
import {useFonts} from './fonts';

export const FLOOR_Y = 1300;

const ObjectView: React.FC<{o: SceneObject; s: State; t: number; world: World}> = ({o, s, t, world}) => {
  const def = OBJECTS[o.type];
  if (!def) return null;
  const {pop, alpha, shake} = baseTransform(s, t);
  if (alpha <= 0.002) return null;
  const R = def.Render;
  if (def.raw) {
    return (
      <div style={{position: 'absolute', left: 0, top: 0, opacity: alpha}}>
        <R o={o} s={s} t={t} world={world} />
      </div>
    );
  }
  const size = def.size(o);
  const ax = size.ax ?? 0.5;
  const ay = size.ay ?? 1;
  return (
    <div style={{position: 'absolute', left: o.x + s.dx, top: o.y + s.dy, width: 0, height: 0}}>
      <div
        style={{
          position: 'absolute',
          left: -ax * size.w,
          top: -ay * size.h,
          width: size.w,
          height: size.h,
          transformOrigin: `${ax * 100}% ${ay * 100}%`,
          transform: `translateX(${shake}px) rotate(${(o.rot ?? 0) + s.rot}deg) scale(${(o.scale ?? 1) * pop})`,
          opacity: alpha,
        }}
      >
        <R o={o} s={s} t={t} world={world} />
      </div>
    </div>
  );
};

const Floor: React.FC<{y: number}> = ({y}) => (
  <div style={{position: 'absolute', left: -5000, top: y, width: 12000, height: 4000, background: 'linear-gradient(#E9ECF1 0,#F5F6F8 450px,#FFFFFF 1050px)'}}>
    <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 3, background: 'rgba(0,0,0,.06)'}} />
  </div>
);

export const Episode: React.FC<{spec: EpisodeSpec}> = ({spec}) => {
  useFonts();
  const frame = useCurrentFrame();
  const tl = useMemo(() => compile(spec), [spec]);
  const t = frame / tl.fps;
  const at = useMemo(() => {
    const cache = new Map<number, World>();
    return (time: number) => {
      const key = Math.round(time * 1000);
      let w = cache.get(key);
      if (!w) {
        w = worldAt(spec, tl, time);
        if (cache.size > 400) cache.clear();
        cache.set(key, w);
      }
      return w;
    };
  }, [spec, tl]);
  const world = at(t);
  const cam = cameraAt(spec, tl, t, at);
  const layer = (name: string) =>
    spec.scene.objects
      .filter((o) => (o.layer ?? (o.type === 'chibi' ? 'back' : 'desk')) === name)
      .map((o) => <ObjectView key={o.id} o={o} s={world.states[o.id]} t={t} world={world} />);
  const blur = cam.blurX > 0 || cam.blurY > 0;
  return (
    <AbsoluteFill style={{width: FRAME_W, height: FRAME_H, overflow: 'hidden', background: 'radial-gradient(120% 70% at 50% 35%,#FFFFFF 0,#F7F8FA 70%,#EEF0F4 100%)'}}>
      <svg width={0} height={0} style={{position: 'absolute'}}>
        <filter id="motion" x="-10%" y="-10%" width="120%" height="120%">
          <feGaussianBlur stdDeviation={`${cam.blurX.toFixed(2)} ${cam.blurY.toFixed(2)}`} />
        </filter>
      </svg>
      <div style={{position: 'absolute', left: 0, top: 0, width: FRAME_W, height: FRAME_H, filter: blur ? 'url(#motion)' : undefined}}>
        <div style={{position: 'absolute', left: 0, top: 0, width: 0, height: 0, transformOrigin: '0 0', transform: `translate(${cam.tx}px, ${cam.ty}px) scale(${cam.z})`}}>
          {layer('back')}
          <Floor y={spec.scene.floorY ?? FLOOR_Y} />
          {layer('desk')}
          {layer('air')}
        </div>
      </div>
      {/* a soft wash under the captions so dark UI or a passing object never fights the text */}
      <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 540, background: 'linear-gradient(rgba(250,251,252,.9) 0,rgba(250,251,252,.78) 320px,rgba(250,251,252,0) 540px)'}} />
      <Captions captions={tl.captions} t={t} />
    </AbsoluteFill>
  );
};
