// Things you keep in your head or on paper: a spiral notepad that fills with
// scribbles and loses its question stickies, and "memory" chips that pop out
// of a call and then blur away into question marks.

import React from 'react';
import {clamp, outBack, outCubic} from '../engine/ease';
import type {ObjectDef, RenderProps} from './core';
import {FONT} from './style';

const num = (v: unknown, d: number) => (typeof v === 'number' ? v : d);
const strs = (v: unknown) => (Array.isArray(v) ? v.map(String) : []);

// ---------- notepad ----------

const PW = 360;
const PH = 450;
const LINES = 6;
const lineY = (i: number) => 120 + i * 48;

/** A cursive-looking squiggle along one ruled line, deterministic per line. */
const squiggle = (i: number) => {
  const x0 = 72;
  const len = [230, 200, 240, 170, 220, 150][i % 6];
  const y = lineY(i) - 12;
  let d = `M${x0},${y}`;
  const n = Math.round(len / 22);
  const w = len / n;
  for (let k = 0; k < n; k++) {
    const up = ((k * 7 + i * 3) % 5) * 3 + 10;
    // arches like a quick "mmnm", with a descender every few letters
    d += k % 4 === 3 ? ` q${w / 2},${up * 0.7} ${w},0` : ` q${w / 2},${-up} ${w},0`;
  }
  return {d, x0, x1: x0 + len, y};
};

const NotepadRender: React.FC<RenderProps> = ({o, s}) => {
  const ink = clamp(s.ink) * num(o.props?.lines, LINES);
  const lost = clamp(s.lost);
  const head = Math.min(LINES - 1, Math.floor(ink));
  const headFrac = ink >= LINES ? 1 : ink - head;
  const hs = squiggle(head);
  const penX = hs.x0 + (hs.x1 - hs.x0) * headFrac;
  const penY = hs.y - 6 + Math.sin(headFrac * 40) * 6;
  const writing = s.ink > 0 && s.ink < 1;
  return (
    <div style={{position: 'absolute', inset: 0}}>
      <div style={{position: 'absolute', left: 12, top: 14, width: PW, height: PH, borderRadius: 18, background: 'linear-gradient(#EFEBE0,#E2DCCD)'}} />
      <div style={{position: 'absolute', left: 0, top: 0, width: PW, height: PH, borderRadius: 18, background: 'linear-gradient(#FFFEFA,#F7F2E6)', boxShadow: '0 24px 44px rgba(60,50,30,.22), inset 0 2px 0 #fff', overflow: 'hidden'}}>
        {Array.from({length: LINES}).map((_, i) => (
          <div key={i} style={{position: 'absolute', left: 0, right: 0, top: lineY(i), height: 2, background: '#D8E3F3'}} />
        ))}
        <div style={{position: 'absolute', left: 56, top: 0, bottom: 0, width: 2, background: '#F2B8C2'}} />
        {Array.from({length: 8}).map((_, i) => (
          <div key={i} style={{position: 'absolute', left: 30 + i * 42, top: 16, width: 12, height: 12, borderRadius: '50%', background: '#5B5E66', opacity: 0.8}} />
        ))}
        <svg width={PW} height={PH} style={{position: 'absolute', left: 0, top: 0}}>
          {Array.from({length: LINES}).map((_, i) => {
            const f = clamp(ink - i);
            if (f <= 0) return null;
            return <path key={i} d={squiggle(i).d} pathLength={1} fill="none" stroke="#2C3E7A" strokeWidth={4.5} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={`${f} 2`} />;
          })}
        </svg>
      </div>
      {/* spiral rings */}
      {Array.from({length: 8}).map((_, i) => (
        <div key={i} style={{position: 'absolute', left: 27 + i * 42, top: -20, width: 18, height: 44, borderRadius: 9, border: '5px solid #6B6E76', borderBottomColor: 'transparent', boxSizing: 'border-box', background: 'transparent'}} />
      ))}
      {/* question stickies on the right edge */}
      {[0, 1, 2].map((i) => {
        const q = clamp((lost - i * 0.18) / 0.5);
        const e = outCubic(q);
        const y = 110 + i * 112;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: PW - 70,
              top: y,
              width: 120,
              height: 96,
              borderRadius: 10,
              background: 'linear-gradient(#FFD6E2,#F6B0C5)',
              boxShadow: '0 10px 18px rgba(150,50,85,.25)',
              transform: `translate(${e * 260}px, ${-e * 300 - i * 40 * e}px) rotate(${[6, -4, 8][i] + e * 55}deg) scale(${1 - 0.3 * e})`,
              opacity: 1 - q,
              display: 'grid',
              placeItems: 'center',
              fontFamily: FONT,
              fontWeight: 800,
              fontSize: 60,
              lineHeight: 1,
              color: '#B03A62',
            }}
          >
            ?
          </div>
        );
      })}
      {writing ? (
        <div style={{position: 'absolute', left: penX, top: penY, width: 22, height: 170, transformOrigin: '50% 100%', transform: 'translate(-11px,-170px) rotate(28deg)'}}>
          <div style={{position: 'absolute', left: 0, top: 0, width: 22, height: 140, borderRadius: '11px 11px 4px 4px', background: 'linear-gradient(90deg,#2B2D33,#55585F 45%,#1E2024)'}} />
          <div style={{position: 'absolute', left: 4, top: 138, width: 14, height: 26, background: 'linear-gradient(90deg,#B9BDC3,#E9EBEE,#9EA2A8)', clipPath: 'polygon(0 0,100% 0,60% 100%,40% 100%)'}} />
        </div>
      ) : null}
    </div>
  );
};

export const Notepad: ObjectDef = {
  size: () => ({w: PW, h: PH, ax: 0.5, ay: 0.5}),
  init: () => ({ink: 0, lost: 0}),
  verbs: {
    scribble: {dur: 1.4, apply: (s, a, c) => ({...s, ink: s.ink + (num(a.to, 1) - s.ink) * c.p})},
    lose: {dur: 1.0, apply: (s, _a, c) => ({...s, lost: c.p})},
  },
  anchors: () => ({page: {x: 0, y: 0, w: PW, h: PH}, stickies: {x: PW - 80, y: 90, w: 150, h: 340}}),
  Render: NotepadRender,
};

// ---------- memory chips ----------

const SPOTS: [number, number, number][] = [
  [-170, -95, -6],
  [150, -120, 5],
  [-120, 35, 3],
  [190, 25, -4],
  [10, 140, -2],
];
const TINTS = [
  ['#FFF4CC', '#FFE38F'],
  ['#FFE3EC', '#FFC7D8'],
  ['#E3EEFF', '#C6DBFF'],
  ['#E0F6EA', '#BFEBD3'],
  ['#F1E8FF', '#DCCBFF'],
];

const ChipsRender: React.FC<RenderProps> = ({o, s}) => {
  const items = strs(o.props?.items).slice(0, SPOTS.length);
  return (
    <div style={{position: 'absolute', inset: 0}}>
      {items.map((text, i) => {
        const [x, y, r] = SPOTS[i];
        const pin = clamp((s.pop - i * 0.14) / 0.42);
        if (pin <= 0) return null;
        const f = clamp((s.forget - i * 0.1) / 0.55);
        const q = clamp((f - 0.35) / 0.45);
        return (
          <React.Fragment key={i}>
            <div
              style={{
                position: 'absolute',
                left: 350 + x,
                top: 160 + y - f * 50,
                transform: `translate(-50%,-50%) rotate(${r}deg) scale(${outBack(pin)})`,
                padding: '18px 30px',
                borderRadius: 40,
                whiteSpace: 'nowrap',
                fontFamily: FONT,
                fontWeight: 700,
                fontSize: 34,
                color: '#2B2925',
                background: `linear-gradient(${TINTS[i][0]},${TINTS[i][1]})`,
                boxShadow: '0 14px 28px rgba(40,40,80,.18), inset 0 2px 0 rgba(255,255,255,.8)',
                filter: f > 0 ? `blur(${f * 16}px) grayscale(${f})` : undefined,
                opacity: clamp(pin * 3) * (1 - f * 0.9),
              }}
            >
              {text}
            </div>
            {q > 0 ? (
              <div
                style={{
                  position: 'absolute',
                  left: 350 + x,
                  top: 160 + y - 30,
                  width: 84,
                  height: 84,
                  borderRadius: '50%',
                  transform: `translate(-50%,-50%) scale(${outBack(q)})`,
                  background: 'linear-gradient(#FFFFFF,#EEF0F4)',
                  boxShadow: '0 12px 24px rgba(40,40,80,.16)',
                  display: 'grid',
                  placeItems: 'center',
                  fontFamily: FONT,
                  fontWeight: 800,
                  fontSize: 52,
                  color: '#9AA0AA',
                }}
              >
                ?
              </div>
            ) : null}
          </React.Fragment>
        );
      })}
    </div>
  );
};

export const Chips: ObjectDef = {
  size: () => ({w: 700, h: 320, ax: 0.5, ay: 0.5}),
  init: () => ({pop: 0, forget: 0}),
  verbs: {
    pop: {dur: 1.0, apply: (s, _a, c) => ({...s, pop: c.p})},
    forget: {dur: 1.1, apply: (s, _a, c) => ({...s, forget: c.p})},
  },
  Render: ChipsRender,
};
