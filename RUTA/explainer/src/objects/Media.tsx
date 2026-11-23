// Making and shipping video: an editing timeline that gets its pauses cut and
// subtitles added, a clock that eats hours, a price tag, and the render cloud.

import React from 'react';
import {clamp, inOut, lerp, outBack, outCubic} from '../engine/ease';
import type {ObjectDef, RenderProps} from './core';
import {C, FONT} from './style';

const str = (v: unknown, d = '') => (typeof v === 'string' ? v : d);
const num = (v: unknown, d: number) => (typeof v === 'number' ? v : d);

// ---------- editing timeline ----------

const TW = 780;
const TH = 340;
const CLIPS = [96, 72, 112, 64, 104, 84, 92];
const GAPS = [40, 30, 44, 26, 36, 32];
const FLAGGED = [2, 5];

const TimelineRender: React.FC<RenderProps> = ({s, t}) => {
  const cut = inOut(clamp(s.cut));
  const subs = clamp(s.subs);
  const flag = clamp(s.flag);
  // lay clips out with the pauses between them shrinking as they're cut
  let x = 30;
  const clips = CLIPS.map((w, i) => {
    const c = {x, w};
    x += w + 6 + (i < GAPS.length ? GAPS[i] * (1 - cut) : 0);
    return c;
  });
  const gaps = GAPS.map((g, i) => ({x: clips[i].x + clips[i].w + 3, w: g * (1 - cut)}));
  const end = x;
  const head = 30 + ((t * 120) % Math.max(1, end - 30));
  return (
    <div style={{position: 'absolute', inset: 0, borderRadius: 30, background: 'linear-gradient(#26272D,#1B1C20)', boxShadow: '0 30px 60px rgba(20,22,30,.28), inset 0 2px 0 rgba(255,255,255,.08)', overflow: 'hidden', fontFamily: FONT}}>
      <div style={{position: 'absolute', left: 30, top: 22, display: 'flex', alignItems: 'center', gap: 14}}>
        <svg width={30} height={30} viewBox="0 0 24 24">
          <g fill="none" stroke="#E8EAED" strokeWidth={2.2} strokeLinecap="round">
            <circle cx="6" cy="6" r="3" />
            <circle cx="6" cy="18" r="3" />
            <path d="M8.5 7.5 20 18M8.5 16.5 20 6" />
          </g>
        </svg>
        <span style={{color: '#E8EAED', fontWeight: 700, fontSize: 24, fontVariantNumeric: 'tabular-nums'}}>
          00:00:{String(Math.round(lerp(58, 41, cut))).padStart(2, '0')}
        </span>
      </div>
      {/* video track */}
      {clips.map((c, i) => {
        const fl = FLAGGED.includes(i) ? flag : 0;
        return (
          <div key={i} style={{position: 'absolute', left: c.x, top: 80, width: c.w, height: 72, borderRadius: 10, background: 'linear-gradient(#5AA9E6,#3D7FC4)', boxShadow: fl > 0 ? `0 0 0 ${4 * fl}px #FF5A5A` : 'inset 0 2px 0 rgba(255,255,255,.3)'}}>
            <div style={{position: 'absolute', left: 6, right: 6, top: 6, height: 26, borderRadius: 6, background: 'rgba(255,255,255,.22)'}} />
            {fl > 0 ? (
              <div style={{position: 'absolute', right: -14, top: -20, padding: '2px 10px', borderRadius: 12, background: '#FF5A5A', color: '#fff', fontWeight: 800, fontSize: 20, transform: `scale(${outBack(fl)})`}}>×2</div>
            ) : null}
          </div>
        );
      })}
      {/* pauses: hatched, shrinking away */}
      {gaps.map((g, i) =>
        g.w > 1 ? (
          <div key={i} style={{position: 'absolute', left: g.x, top: 80, width: g.w, height: 72, borderRadius: 8, background: 'repeating-linear-gradient(135deg,#3A3C44 0 6px,#2C2E35 6px 12px)', opacity: 1 - cut}} />
        ) : null,
      )}
      {/* subtitles */}
      {clips.map((c, i) => {
        const p = clamp(subs * CLIPS.length - i);
        if (p <= 0) return null;
        return <div key={i} style={{position: 'absolute', left: c.x + 6, top: 164, width: c.w - 12, height: 30, borderRadius: 8, background: 'linear-gradient(#FFE38F,#F7BF22)', transform: `scale(${outBack(p)})`}} />;
      })}
      {clips.map((c, i) => {
        const p = clamp(subs * CLIPS.length - i - 0.5);
        if (p <= 0 || i % 2) return null;
        return <div key={i} style={{position: 'absolute', left: c.x + c.w / 2 - 10, top: 206, width: 20, height: 20, transform: `rotate(45deg) scale(${outBack(p)})`, borderRadius: 4, background: '#B69CFF'}} />;
      })}
      {/* audio waveform: flat in the pauses */}
      <div style={{position: 'absolute', left: 30, top: 244, width: end - 30, height: 64, display: 'flex', alignItems: 'center', gap: 3, overflow: 'hidden'}}>
        {Array.from({length: Math.floor((end - 30) / 7)}).map((_, k) => {
          const xx = 30 + k * 7;
          const inGap = gaps.some((g) => xx >= g.x && xx <= g.x + g.w);
          const h = inGap ? 3 : 10 + 44 * Math.abs(Math.sin(k * 1.7) * Math.cos(k * 0.6));
          return <i key={k} style={{flex: 'none', width: 4, height: h, borderRadius: 2, background: inGap ? '#4A4C55' : '#4CD39B'}} />;
        })}
      </div>
      <div style={{position: 'absolute', left: head, top: 66, width: 4, height: 252, borderRadius: 2, background: '#FF5A5A'}} />
    </div>
  );
};

export const Timeline: ObjectDef = {
  size: () => ({w: TW, h: TH, ax: 0.5, ay: 0.5}),
  init: () => ({cut: 0, subs: 0, flag: 0}),
  verbs: {
    cut: {dur: 1.0, apply: (s, _a, c) => ({...s, cut: c.p})},
    subs: {dur: 1.0, apply: (s, _a, c) => ({...s, subs: c.p})},
    /** Mark the repeated takes the editor left in. */
    flag: {dur: 0.4, apply: (s, _a, c) => ({...s, flag: c.p})},
  },
  anchors: () => ({tracks: {x: 20, y: 60, w: 740, h: 260}}),
  Render: TimelineRender,
};

// ---------- clock ----------

const ClockRender: React.FC<RenderProps> = ({o, s}) => {
  const h = num(s.hours, 0);
  const label = str(o.props?.label);
  const minuteDeg = h * 360;
  const hourDeg = 300 + h * 30;
  return (
    <div style={{position: 'absolute', inset: 0}}>
      {[-1, 1].map((d) => (
        <div key={d} style={{position: 'absolute', left: 150 + d * 92 - 36, top: 2, width: 72, height: 52, borderRadius: '50% 50% 20% 20%', background: `linear-gradient(${C.skill[0]},${C.skill[1]})`, transform: `rotate(${d * 28}deg)`, boxShadow: '0 6px 12px rgba(170,60,95,.2)'}} />
      ))}
      <div style={{position: 'absolute', left: 10, top: 30, width: 280, height: 280, borderRadius: '50%', background: `linear-gradient(145deg,${C.skill[0]},${C.skill[1]})`, boxShadow: '0 26px 44px rgba(170,60,95,.26), inset 0 4px 0 rgba(255,255,255,.7)'}}>
        <div style={{position: 'absolute', inset: 22, borderRadius: '50%', background: 'radial-gradient(circle at 40% 35%,#FFFFFF,#F1F2F6)', boxShadow: 'inset 0 4px 10px rgba(0,0,0,.08)'}}>
          {Array.from({length: 12}).map((_, i) => (
            <i key={i} style={{position: 'absolute', left: 116, top: 6, width: 4, height: i % 3 ? 10 : 18, borderRadius: 2, background: '#B9BDC6', transformOrigin: '2px 112px', transform: `rotate(${i * 30}deg)`}} />
          ))}
          <i style={{position: 'absolute', left: 114, top: 50, width: 8, height: 70, borderRadius: 4, background: C.ink, transformOrigin: '4px 68px', transform: `rotate(${hourDeg}deg)`}} />
          <i style={{position: 'absolute', left: 115, top: 22, width: 6, height: 98, borderRadius: 3, background: '#3B3E46', transformOrigin: '3px 96px', transform: `rotate(${minuteDeg}deg)`}} />
          <i style={{position: 'absolute', left: 106, top: 106, width: 24, height: 24, borderRadius: '50%', background: C.terracotta}} />
        </div>
      </div>
      {label ? (
        <div style={{position: 'absolute', left: -80, right: -80, top: 322, textAlign: 'center', fontFamily: FONT, fontWeight: 800, fontSize: 46, color: C.ink, letterSpacing: -1, opacity: clamp(s.labelP * 2), transform: `scale(${outBack(clamp(s.labelP))})`}}>
          {label}
        </div>
      ) : null}
    </div>
  );
};

export const Clock: ObjectDef = {
  size: () => ({w: 300, h: 380, ax: 0.5, ay: 0.45}),
  init: () => ({hours: 0, labelP: 0}),
  verbs: {
    spin: {
      dur: 1.2,
      apply: (s, a, c) => {
        const from = s.hours;
        return {...s, hours: lerp(from, from + num(a.hours, 2), inOut(c.p)), labelP: clamp((c.p - 0.5) * 2)};
      },
    },
  },
  anchors: () => ({face: {x: 0, y: 0, w: 300, h: 320}}),
  Render: ClockRender,
};

// ---------- price tag ----------

const PriceRender: React.FC<RenderProps> = ({o, t}) => {
  const sway = Math.sin(t * 2.2) * 5;
  return (
    <div style={{position: 'absolute', inset: 0, transformOrigin: '50% 0%', transform: `rotate(${sway}deg)`}}>
      <svg width={380} height={90} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
        <path d="M190 0 C 170 40, 120 50, 96 92" stroke="#9A8F86" strokeWidth={4} fill="none" strokeLinecap="round" />
      </svg>
      <div
        style={{
          position: 'absolute',
          left: 40,
          top: 80,
          width: 320,
          height: 160,
          background: 'linear-gradient(#FFE9A6,#F7BF22)',
          clipPath: 'polygon(18% 0,100% 0,100% 100%,18% 100%,0 50%)',
          borderRadius: 18,
          filter: 'drop-shadow(0 18px 24px rgba(150,100,0,.3))',
        }}
      >
        <div style={{position: 'absolute', left: 30, top: 66, width: 26, height: 26, borderRadius: '50%', background: '#F6F7FA', boxShadow: 'inset 0 2px 4px rgba(0,0,0,.25)'}} />
        <div style={{position: 'absolute', left: 76, right: 14, top: 18, textAlign: 'center', fontFamily: FONT, fontWeight: 800, fontSize: 70, lineHeight: 1, color: C.ink, letterSpacing: -2}}>{str(o.props?.text, '€€€')}</div>
        <div style={{position: 'absolute', left: 76, right: 14, top: 102, textAlign: 'center', fontFamily: FONT, fontWeight: 700, fontSize: 28, color: '#6B4E00'}}>{str(o.props?.sub, 'щомісяця')}</div>
      </div>
    </div>
  );
};

export const Price: ObjectDef = {
  size: () => ({w: 380, h: 250, ax: 0.5, ay: 0.5}),
  verbs: {},
  Render: PriceRender,
};

// ---------- cloud ----------

const PUFFS: [number, number, number][] = [
  [130, 170, 110],
  [250, 120, 140],
  [380, 160, 115],
  [190, 210, 100],
  [320, 215, 105],
];

const CloudRender: React.FC<RenderProps> = ({s, t}) => {
  const up = clamp(s.up);
  const done = clamp(s.done);
  const bob = Math.sin(t * 1.6) * 8;
  return (
    <div style={{position: 'absolute', inset: 0, transform: `translateY(${bob}px)`}}>
      <div style={{position: 'absolute', inset: 0, filter: 'drop-shadow(0 26px 34px rgba(60,80,140,.22))'}}>
        {PUFFS.map(([x, y, r], i) => (
          <div key={i} style={{position: 'absolute', left: x - r, top: y - r, width: r * 2, height: r * 2, borderRadius: '50%', background: 'linear-gradient(#FFFFFF,#E3EAF7)'}} />
        ))}
        <div style={{position: 'absolute', left: 60, top: 190, width: 400, height: 126, borderRadius: 63, background: 'linear-gradient(#F5F8FD,#E3EAF7)'}} />
      </div>
      {/* upload arrow, then a check */}
      <div style={{position: 'absolute', left: 205, top: 120, width: 110, height: 110, borderRadius: '50%', background: done > 0 ? '#2DB47A' : C.terracotta, display: 'grid', placeItems: 'center', boxShadow: '0 10px 20px rgba(150,60,30,.25)', transform: `translateY(${done > 0 ? 0 : -Math.abs(Math.sin(t * 4)) * 10}px) scale(${done > 0 ? outBack(done) : 1})`}}>
        <svg width={56} height={56} viewBox="0 0 24 24">
          {done > 0 ? (
            <path d="M5 12.5l4.5 4.5L19 7.5" stroke="#fff" strokeWidth={3.2} fill="none" strokeLinecap="round" strokeLinejoin="round" />
          ) : (
            <path d="M12 19V5M5.5 11.5 12 5l6.5 6.5" stroke="#fff" strokeWidth={3.2} fill="none" strokeLinecap="round" strokeLinejoin="round" />
          )}
        </svg>
      </div>
      <div style={{position: 'absolute', left: 130, top: 262, width: 260, height: 18, borderRadius: 9, background: '#D5DDEC', overflow: 'hidden'}}>
        <div style={{width: `${Math.max(up, done) * 100}%`, height: '100%', borderRadius: 9, background: done > 0 ? '#2DB47A' : C.terracotta}} />
      </div>
    </div>
  );
};

export const Cloud: ObjectDef = {
  size: () => ({w: 520, h: 330, ax: 0.5, ay: 0.5}),
  init: () => ({up: 0, done: 0}),
  verbs: {
    upload: {dur: 1.2, apply: (s, _a, c) => ({...s, up: outCubic(c.p)})},
    done: {dur: 0.4, apply: (s, _a, c) => ({...s, done: c.p, up: 1})},
  },
  Render: CloudRender,
};
