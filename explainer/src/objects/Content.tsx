// Content objects: a reel grid, a spreadsheet, a calendar, a carousel slide
// stack, a design-system card and a pile of notes. Numbers are never shown as
// hers — cells and counters are shape-only bars (STYLE.md "No invented stats").

import React from 'react';
import {clamp, inOut, lerp, outBack, outCubic} from '../engine/ease';
import type {ObjectDef, RenderProps} from './core';
import {C, FONT} from './style';

const str = (v: unknown, d = '') => (typeof v === 'string' ? v : d);
const num = (v: unknown, d: number) => (typeof v === 'number' ? v : d);
const strs = (v: unknown) => (Array.isArray(v) ? v.map(String) : []);

const TINTS: [string, string][] = [
  ['#FFD6E2', '#F6A9C0'],
  ['#D5E6FF', '#9DBEF2'],
  ['#FFF1C7', '#F7CF5A'],
  ['#D9F3E6', '#8FD9B4'],
  ['#E9DFFF', '#B9A2F2'],
  ['#FFE0CF', '#F4A57D'],
];
const tint = (i: number) => TINTS[((i * 7) % TINTS.length + TINTS.length) % TINTS.length];

// ---------- reel grid ----------

const RW = 480;
const COLS = 3;
const GAP = 8;
const TWD = (RW - 48 - GAP * (COLS - 1)) / COLS;
const THT = TWD * 4 / 3;
const ROWS_VISIBLE = 3;
const RH = 104 + ROWS_VISIBLE * (THT + GAP) + 16;

const MARKS: Record<string, {bg: string; glyph: string}> = {
  star: {bg: '#F7BF22', glyph: '★'},
  q: {bg: '#9AA0AA', glyph: '?'},
  x: {bg: '#FF5A5A', glyph: '×'},
  check: {bg: '#2DB47A', glyph: '✓'},
};

const ReelsRender: React.FC<RenderProps> = ({o, s}) => {
  const scroll = num(s.scroll, 0);
  const total = Math.max(num(o.props?.count, 12), Math.ceil(scroll + ROWS_VISIBLE + 1) * COLS);
  const shown = s.shown;
  return (
    <div style={{position: 'absolute', inset: 0, borderRadius: 36, background: '#fff', boxShadow: '0 30px 60px rgba(30,40,80,.18), inset 0 3px 0 #fff', overflow: 'hidden', filter: s.dim > 0 ? `grayscale(${s.dim})` : undefined}}>
      <div style={{position: 'absolute', left: 24, top: 24, right: 24, height: 60, display: 'flex', alignItems: 'center', gap: 14}}>
        <div style={{width: 56, height: 56, borderRadius: '50%', background: 'linear-gradient(135deg,#FEDA75,#D62976 55%,#4F5BD5)', padding: 4, boxSizing: 'border-box'}}>
          <div style={{width: '100%', height: '100%', borderRadius: '50%', background: '#F3D9C8', border: '3px solid #fff', boxSizing: 'border-box'}} />
        </div>
        <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 28, color: C.ink}}>{str(o.props?.title, 'Мої рілси')}</div>
      </div>
      <div style={{position: 'absolute', left: 24, top: 104, right: 24, bottom: 0, overflow: 'hidden'}}>
        <div style={{position: 'absolute', left: 0, top: -scroll * (THT + GAP), width: RW - 48}}>
          {Array.from({length: total}).map((_, i) => {
            const r = Math.floor(i / COLS);
            const c = i % COLS;
            const v = clamp(shown - i);
            if (v <= 0) return null;
            const [a, b] = tint(i);
            const mark = s.marks?.[i];
            const m = mark ? MARKS[mark.kind] : null;
            return (
              <div key={i} style={{position: 'absolute', left: c * (TWD + GAP), top: r * (THT + GAP), width: TWD, height: THT, borderRadius: 12, background: `linear-gradient(160deg,${a},${b})`, transform: `scale(${outBack(clamp(v * 1.5))})`, opacity: clamp(v * 4)}}>
                <div style={{position: 'absolute', left: 10, bottom: 10, display: 'flex', alignItems: 'center', gap: 6}}>
                  <i style={{display: 'block', width: 0, height: 0, borderLeft: '13px solid rgba(255,255,255,.95)', borderTop: '8px solid transparent', borderBottom: '8px solid transparent'}} />
                  <i style={{display: 'block', width: 34 + (i % 3) * 8, height: 8, borderRadius: 4, background: 'rgba(255,255,255,.85)'}} />
                </div>
                {m ? (
                  <div style={{position: 'absolute', right: -8, top: -8, width: 52, height: 52, borderRadius: '50%', background: m.bg, color: '#fff', display: 'grid', placeItems: 'center', fontFamily: FONT, fontWeight: 800, fontSize: 32, boxShadow: '0 6px 12px rgba(0,0,0,.2)', transform: `scale(${outBack(clamp(mark.p))})`}}>
                    {m.glyph}
                  </div>
                ) : null}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export const Reels: ObjectDef = {
  size: () => ({w: RW, h: RH, ax: 0.5, ay: 0.5}),
  init: (o) => ({shown: o.props?.filled ? num(o.props?.count, 12) : 0, scroll: 0, marks: {}, dim: 0}),
  verbs: {
    fill: {
      dur: (a, o) => 0.3 + num(a.n, num(o.props?.count, 12)) * 0.05,
      apply: (s, a, c, o) => ({...s, shown: Math.floor(s.shown) + num(a.n, num(o.props?.count, 12)) * c.p}),
    },
    scroll: {
      dur: 1.0,
      apply: (s, a, c) => {
        const by = num(a.rows, 3);
        const from = s.scroll;
        // filling the newly revealed rows as it goes
        return {...s, scroll: lerp(from, from + by, inOut(c.p)), shown: Math.max(s.shown, (from + by * c.p + ROWS_VISIBLE + 1) * COLS)};
      },
    },
    mark: {
      dur: 0.35,
      required: ['index'],
      apply: (s, a, c) => ({...s, marks: {...s.marks, [num(a.index, 0)]: {kind: str(a.kind, 'star'), p: c.p}}}),
    },
    dim: {dur: 0.5, apply: (s, _a, c) => ({...s, dim: c.p})},
  },
  anchors: () => ({grid: {x: 24, y: 104, w: RW - 48, h: RH - 120}}),
  Render: ReelsRender,
};

// ---------- spreadsheet ----------

const SW = 640;
const SROWS = 7;
const SheetRender: React.FC<RenderProps> = ({o, s}) => {
  const cols = strs(o.props?.cols).length ? strs(o.props?.cols) : ['Рілс', 'Перегляди', 'Збереження', 'Репости'];
  const cells = SROWS * (cols.length - 1);
  const fill = clamp(s.fill) * cells;
  const cw = (SW - 48 - 90) / (cols.length - 1);
  return (
    <div style={{position: 'absolute', inset: 0, borderRadius: 28, background: '#fff', boxShadow: '0 30px 60px rgba(30,40,80,.18)', overflow: 'hidden', fontFamily: FONT}}>
      <div style={{height: 64, background: 'linear-gradient(#2BA160,#1E8E3E)', display: 'flex', alignItems: 'center', padding: '0 26px', gap: 14}}>
        <div style={{width: 30, height: 36, borderRadius: 5, background: '#fff', position: 'relative'}}>
          {[0, 1, 2].map((k) => (
            <i key={k} style={{position: 'absolute', left: 6, right: 6, top: 9 + k * 8, height: 3, background: '#1E8E3E'}} />
          ))}
        </div>
        <span style={{color: '#fff', fontWeight: 800, fontSize: 28}}>{str(o.props?.title, 'Статистика рілсів')}</span>
      </div>
      <div style={{position: 'absolute', left: 24, top: 88, right: 24}}>
        <div style={{display: 'flex', height: 46, background: '#F1F3F4', borderRadius: 10, alignItems: 'center', fontWeight: 700, fontSize: 20, color: '#5F6368'}}>
          {cols.map((c, i) => (
            <div key={i} style={{width: i === 0 ? 90 : cw, paddingLeft: 12, boxSizing: 'border-box', whiteSpace: 'nowrap', overflow: 'hidden'}}>{c}</div>
          ))}
        </div>
        {Array.from({length: SROWS}).map((_, r) => (
          <div key={r} style={{display: 'flex', height: 42, borderBottom: '2px solid #EEF0F2', alignItems: 'center'}}>
            <div style={{width: 90, paddingLeft: 12, boxSizing: 'border-box', fontWeight: 700, fontSize: 20, color: '#9AA0A6'}}>#{r + 1}</div>
            {cols.slice(1).map((_c, k) => {
              const i = r * (cols.length - 1) + k;
              const v = clamp(fill - i);
              return (
                <div key={k} style={{width: cw, paddingLeft: 12, boxSizing: 'border-box'}}>
                  <i style={{display: 'block', height: 12, borderRadius: 6, width: `${(30 + ((i * 37) % 50)) * outCubic(v)}%`, background: s.blur > 0 ? '#C7CBD1' : '#3C4043', opacity: v > 0 ? 0.8 : 0, filter: s.blur > 0 ? `blur(${s.blur * 3}px)` : undefined}} />
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
};

export const Sheet: ObjectDef = {
  size: () => ({w: SW, h: 88 + 46 + SROWS * 42 + 30, ax: 0.5, ay: 0.5}),
  init: () => ({fill: 0, blur: 0}),
  verbs: {
    fill: {dur: 1.6, apply: (s, a, c) => ({...s, fill: lerp(s.fill, num(a.to, 1), c.p)})},
    /** Numbers without context: they go fuzzy and grey. */
    blur: {dur: 0.6, apply: (s, _a, c) => ({...s, blur: c.p})},
  },
  anchors: () => ({grid: {x: 24, y: 88, w: SW - 48, h: 46 + SROWS * 42}}),
  Render: SheetRender,
};

// ---------- calendar ----------

const DAYS = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд'];
const CalRender: React.FC<RenderProps> = ({o, s}) => {
  const flip = num(s.flip, 0);
  const base = Math.floor(flip);
  const frac = flip - base;
  return (
    <div style={{position: 'absolute', inset: 0, borderRadius: 32, background: 'linear-gradient(#FFFFFF,#F6F7FA)', boxShadow: '0 30px 60px rgba(30,40,80,.18), inset 0 3px 0 #fff', overflow: 'hidden', fontFamily: FONT}}>
      <div style={{height: 70, background: `linear-gradient(${C.skill[0]},${C.skill[1]})`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, fontSize: 30, color: C.ink}}>{str(o.props?.title, 'Календар')}</div>
      <div style={{position: 'absolute', left: 22, right: 22, top: 84, display: 'flex', justifyContent: 'space-between'}}>
        {DAYS.map((d, i) => (
          <div key={d} style={{width: 62, textAlign: 'center', fontWeight: 800, fontSize: 20, color: i === 0 ? C.terracotta : '#9AA0A6'}}>{d}</div>
        ))}
      </div>
      <div style={{position: 'absolute', left: 22, right: 22, top: 122, height: 3 * 76, overflow: 'hidden'}}>
        {[0, 1, 2, 3].map((w) => {
          const week = base + w;
          const y = (w - inOut(frac)) * 76;
          const status: string | undefined = s.mondays?.[week];
          return (
            <div key={week} style={{position: 'absolute', left: 0, right: 0, top: y, height: 68, display: 'flex', justifyContent: 'space-between'}}>
              {DAYS.map((_d, i) => (
                <div key={i} style={{width: 62, height: 62, borderRadius: 16, background: i === 0 ? '#FFE3EC' : '#F1F3F6', display: 'grid', placeItems: 'center', fontWeight: 700, fontSize: 22, color: '#6B6E76', position: 'relative'}}>
                  {((week * 7 + i) % 30) + 1}
                  {i === 0 && status ? (
                    <div style={{position: 'absolute', inset: -4, borderRadius: 18, background: status === 'done' ? '#2DB47A' : '#FF5A5A', display: 'grid', placeItems: 'center', color: '#fff', fontSize: 34, fontWeight: 800}}>{status === 'done' ? '✓' : '×'}</div>
                  ) : null}
                </div>
              ))}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export const Calendar: ObjectDef = {
  size: () => ({w: 520, h: 122 + 3 * 76 + 18, ax: 0.5, ay: 0.5}),
  init: () => ({flip: 0, mondays: {}}),
  verbs: {
    /** Weeks go by; `mark` puts a ✓ or × on each Monday that passes. */
    flip: {
      dur: 1.2,
      apply: (s, a, c) => {
        const weeks = num(a.weeks, 3);
        const flip = s.flip + weeks * c.p;
        const mondays = {...s.mondays};
        const mark = str(a.mark);
        if (mark) for (let w = Math.floor(s.flip); w <= Math.floor(flip + 0.6); w++) mondays[w] = mark;
        return {...s, flip, mondays};
      },
    },
  },
  Render: CalRender,
};

// ---------- carousel slides ----------

const SL_W = 300;
const SL_H = 375;
const N = 5;
const UGLY: React.CSSProperties[] = [
  {background: 'linear-gradient(45deg,#00F5A0,#00D9F5)', fontFamily: 'Georgia,serif', color: '#7A00FF'},
  {background: 'repeating-linear-gradient(90deg,#FF00A8 0 20px,#FFE600 20px 40px)', fontFamily: 'monospace', color: '#000'},
  {background: '#1A1A1A', fontFamily: 'Impact,sans-serif', color: '#39FF14'},
  {background: 'radial-gradient(circle,#FF6B00,#7A0000)', fontFamily: 'cursive', color: '#FFF'},
  {background: '#8DE3FF', fontFamily: 'Times New Roman,serif', color: '#FF1E1E'},
];

const SlideFace: React.FC<{mode: string; i: number; text: number; titles: string[]; variant: number}> = ({mode, i, text, titles, variant}) => {
  const title = titles[i % Math.max(1, titles.length)] ?? '';
  const shown = clamp(text * N - i);
  if (mode === 'blank')
    return (
      <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(#FFFFFF,#F4F5F8)'}}>
        <div style={{position: 'absolute', inset: 18, borderRadius: 14, border: '4px dashed #CBD0DA'}} />
        <div style={{position: 'absolute', left: '50%', top: '50%', width: 64, height: 64, margin: '-32px 0 0 -32px', borderRadius: '50%', background: '#E3E7EE', display: 'grid', placeItems: 'center', fontFamily: FONT, fontWeight: 800, fontSize: 44, color: '#9AA3B2'}}>+</div>
      </div>
    );
  if (mode === 'ugly') {
    const u = UGLY[(i + variant) % UGLY.length];
    return (
      <div style={{position: 'absolute', inset: 0, ...u, padding: 22, boxSizing: 'border-box', transform: `rotate(${((i + variant) % 3) - 1}deg)`}}>
        <div style={{fontSize: 34 + ((i + variant) % 3) * 8, fontWeight: 700, lineHeight: 1.05, textAlign: (i + variant) % 2 ? 'right' : 'left'}}>{title}</div>
        <div style={{position: 'absolute', left: 30 + ((i * 40) % 120), bottom: 40, width: 90, height: 90, borderRadius: (i + variant) % 2 ? '50%' : 0, background: 'rgba(255,255,255,.55)', transform: `rotate(${i * 23}deg)`}} />
      </div>
    );
  }
  const mine = mode === 'mine';
  return (
    <div style={{position: 'absolute', inset: 0, background: mine ? `linear-gradient(160deg,${C.paper[0]},${C.paper[1]})` : 'linear-gradient(#F7F3EA,#EFE9DD)', padding: '26px 24px', boxSizing: 'border-box', fontFamily: FONT}}>
      {shown > 0 ? (
        <div style={{fontWeight: 800, fontSize: 34, lineHeight: 1.08, letterSpacing: -0.8, color: mine ? C.ink : '#2B2925', opacity: shown}}>
          {mine ? <span style={{background: C.marker, borderRadius: 10, padding: '0 6px', boxDecorationBreak: 'clone', WebkitBoxDecorationBreak: 'clone'}}>{title}</span> : title}
        </div>
      ) : (
        <div style={{height: 30, width: '70%', borderRadius: 8, background: '#E4E1DA'}} />
      )}
      <div style={{marginTop: 20, display: 'flex', flexDirection: 'column', gap: 12}}>
        {[90, 74, 84, 56].map((w, k) => (
          <div key={k} style={{height: 12, borderRadius: 6, width: `${shown > 0 ? w * clamp(shown * 4 - k * 0.5) : w}%`, background: shown > 0 ? (mine ? 'rgba(74,39,52,.35)' : '#B9B4AC') : '#ECE9E2'}} />
        ))}
      </div>
      {mine ? <div style={{position: 'absolute', right: 20, bottom: 18, fontWeight: 800, fontSize: 18, color: C.paperText}}>{i + 1}/{N}</div> : null}
      {!shown && mode === 'template' ? <div style={{position: 'absolute', left: 24, bottom: 20, fontSize: 16, fontWeight: 600, color: '#A8A29A'}}>Текст тут</div> : null}
    </div>
  );
};

const SlidesRender: React.FC<RenderProps> = ({o, s}) => {
  const titles = strs(o.props?.titles);
  const styleP = clamp(s.styleP);
  return (
    <div style={{position: 'absolute', inset: 0, perspective: 1600}}>
      {Array.from({length: N}).map((_, i) => {
        const v = clamp(s.shown - i);
        if (v <= 0) return null;
        // each slide flips to the new style in turn
        const flip = clamp(styleP * 1.6 - i * 0.15);
        const mid = flip > 0 && flip < 1;
        const mode = flip >= 0.5 ? s.mode : s.prevMode;
        const rotY = mid ? Math.sin(flip * Math.PI) * 90 * (flip < 0.5 ? 1 : -1) : 0;
        const x = 20 + i * 108;
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: x,
              top: 40 + Math.abs(i - 2) * 10,
              width: SL_W,
              height: SL_H,
              borderRadius: 22,
              overflow: 'hidden',
              boxShadow: '0 22px 40px rgba(30,40,80,.2), 0 2px 0 rgba(255,255,255,.6) inset',
              transform: `rotate(${(i - 2) * 3}deg) rotateY(${rotY}deg) scale(${outBack(clamp(v * 1.4))})`,
              opacity: clamp(v * 4),
            }}
          >
            <SlideFace mode={mode} i={i} text={s.textP} titles={titles} variant={s.variant} />
          </div>
        );
      })}
    </div>
  );
};

export const Slides: ObjectDef = {
  size: () => ({w: 20 + 4 * 108 + SL_W + 20, h: SL_H + 100, ax: 0.5, ay: 0.5}),
  init: (o) => ({shown: o.props?.built ? N : 0, textP: 0, mode: str(o.props?.mode, 'blank'), prevMode: str(o.props?.mode, 'blank'), styleP: 1, variant: 0}),
  verbs: {
    build: {dur: 1.4, apply: (s, a, c) => ({...s, shown: Math.floor(s.shown) + num(a.n, N) * c.p})},
    text: {dur: 1.2, apply: (s, a, c) => ({...s, textP: lerp(s.textP, num(a.to, 1), c.p)})},
    style: {
      dur: 0.9,
      required: ['mode'],
      check: (a) => (['blank', 'template', 'ugly', 'mine'].includes(str(a.mode)) ? null : 'mode is blank, template, ugly or mine'),
      apply: (s, a, c) => (s.mode === a.mode && c.p >= 1 ? s : {...s, prevMode: s.mode === a.mode ? s.prevMode : s.mode, mode: str(a.mode), styleP: c.p}),
    },
    /** A new chat, a new look: the ugly variants reshuffle. */
    shuffle: {dur: 0.6, apply: (s, a, c) => ({...s, variant: Math.floor(num(a.from, s.variant) + c.p * num(a.times, 3))})},
  },
  anchors: () => ({front: {x: 200, y: 40, w: SL_W + 40, h: SL_H}}),
  Render: SlidesRender,
};

// ---------- design-system card ----------

const DsRender: React.FC<RenderProps> = ({o}) => (
  <div style={{position: 'absolute', inset: 0, borderRadius: 36, background: 'linear-gradient(150deg,#FFFFFF,#F4F1F6)', boxShadow: '0 30px 60px rgba(30,40,80,.2), inset 0 3px 0 #fff', fontFamily: FONT, overflow: 'hidden'}}>
    <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: '45%', background: 'linear-gradient(rgba(255,255,255,.6),rgba(255,255,255,0))'}} />
    <div style={{position: 'absolute', left: 30, top: 24, fontWeight: 800, fontSize: 32, color: C.ink}}>{str(o.props?.title, 'Дизайн-система')}</div>
    <div style={{position: 'absolute', left: 30, top: 84, display: 'flex', gap: 12}}>
      {[C.paper[1], C.terracotta, C.ink, C.marker, C.cream].map((c, i) => (
        <div key={i} style={{width: 58, height: 58, borderRadius: 16, background: c, boxShadow: '0 6px 12px rgba(0,0,0,.12), inset 0 0 0 2px rgba(0,0,0,.05)'}} />
      ))}
    </div>
    <div style={{position: 'absolute', left: 30, top: 160, fontWeight: 800, fontSize: 96, lineHeight: 1, color: C.ink, letterSpacing: -3}}>Aa</div>
    <div style={{position: 'absolute', left: 160, top: 176, fontWeight: 600, fontSize: 22, color: '#6B6E76'}}>Onest · 800</div>
    <div style={{position: 'absolute', left: 160, top: 212, padding: '10px 22px', borderRadius: 999, background: C.ink, color: '#fff', fontWeight: 700, fontSize: 20}}>Кнопка</div>
    <div style={{position: 'absolute', right: 30, top: 160, width: 120, height: 110, borderRadius: 24, background: `linear-gradient(${C.paper[0]},${C.paper[1]})`, boxShadow: '0 8px 16px rgba(150,50,85,.2)'}} />
  </div>
);

export const DsCard: ObjectDef = {
  size: () => ({w: 520, h: 300, ax: 0.5, ay: 0.5}),
  verbs: {},
  Render: DsRender,
};

// ---------- pile of notes ----------

const PILE: [number, number, number][] = Array.from({length: 24}).map((_, i) => {
  const ring = Math.floor(i / 6);
  const k = i % 6;
  return [(k - 2.5) * 62 + ((i * 29) % 30) - 15, 330 - ring * 70 - ((k * 17) % 26), ((i * 47) % 40) - 20];
});

const PileRender: React.FC<RenderProps> = ({s}) => {
  const n = s.count;
  const bury = clamp(s.bury);
  return (
    <div style={{position: 'absolute', inset: 0, filter: bury > 0 ? `grayscale(${bury}) brightness(${1 - 0.18 * bury})` : undefined}}>
      {PILE.map(([x, y, r], i) => {
        const v = clamp(n - i);
        if (v <= 0) return null;
        const [a, b] = tint(i + 2);
        const drop = (1 - outCubic(clamp(v * 1.3))) * 160;
        return (
          <div key={i} style={{position: 'absolute', left: 260 + x - 75, top: y - 75 - drop + bury * 18, width: 150, height: 150, borderRadius: 10, background: `linear-gradient(${a},${b})`, transform: `rotate(${r}deg)`, boxShadow: '0 10px 18px rgba(60,50,30,.18)', opacity: clamp(v * 3)}}>
            {[0, 1, 2].map((k) => (
              <i key={k} style={{position: 'absolute', left: 18, top: 34 + k * 30, width: `${[70, 55, 62][k]}%`, height: 7, borderRadius: 4, background: 'rgba(60,40,40,.25)'}} />
            ))}
          </div>
        );
      })}
      {bury > 0 ? (
        <svg width={520} height={420} style={{position: 'absolute', left: 0, top: 0, opacity: bury}}>
          <g stroke="rgba(120,120,130,.7)" strokeWidth={2.5} fill="none">
            {[0, 1, 2, 3, 4].map((k) => (
              <path key={k} d={`M40 60 L${40 + Math.cos((k * Math.PI) / 9) * 170} ${60 + Math.sin((k * Math.PI) / 9) * 170}`} />
            ))}
            {[50, 95, 140].map((r) => (
              <path key={r} d={`M${40 + r} 60 Q ${40 + r * 0.92} ${60 + r * 0.42} ${40 + r * Math.cos(Math.PI / 2.25)} ${60 + r * Math.sin(Math.PI / 2.25)}`} />
            ))}
          </g>
        </svg>
      ) : null}
    </div>
  );
};

export const NotesPile: ObjectDef = {
  size: () => ({w: 520, h: 420, ax: 0.5, ay: 0.5}),
  init: (o) => ({count: num(o.props?.count, 0), bury: 0}),
  verbs: {
    grow: {dur: 1.2, apply: (s, a, c) => ({...s, count: Math.floor(s.count) + num(a.n, 12) * c.p})},
    /** The notes graveyard: everything greys out under cobwebs. */
    bury: {dur: 0.8, apply: (s, _a, c) => ({...s, bury: c.p})},
  },
  Render: PileRender,
};
