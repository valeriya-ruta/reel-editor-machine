// The "connected" world: glossy app tiles with a name label, a cable that
// plugs one into another, and task cards popping into a list.

import React from 'react';
import {Img} from 'remotion';
import {bezier} from '../engine/geom';
import {clamp, inOut, outBack, outCubic} from '../engine/ease';
import type {Box, ObjectDef, RenderProps} from './core';
import {asset, C, FONT} from './style';
import {Caret, Spark} from './ui';

const str = (v: unknown, d = '') => (typeof v === 'string' ? v : d);
const num = (v: unknown, d: number) => (typeof v === 'number' ? v : d);

// ---------- app tile ----------

const T = 240;
/** Logos that are a full app icon (cover the tile) vs. a mark on a plate. */
const LOGOS: Record<string, {src?: string; bg: string; mark?: string}> = {
  fathom: {src: 'logos/fathom.jpg', bg: '#000'},
  clickup: {src: 'logos/clickup.jpg', bg: '#fff'},
  canva: {src: 'logos/canva.jpg', bg: '#fff'},
  claude: {bg: C.terracotta, mark: 'claude'},
  instagram: {bg: 'radial-gradient(circle at 30% 107%,#FDF497 0,#FDF497 5%,#FD5949 45%,#D6249F 60%,#285AEB 90%)', mark: 'instagram'},
  notes: {bg: 'linear-gradient(#FFFFFF,#F2F2F2)', mark: 'notes'},
};

/** Simple marks for tiles that aren't a real app: a person, scissors, an AI sparkle, a chart. */
const GLYPHS: Record<string, React.ReactNode> = {
  scissors: (
    <g fill="none" stroke="#fff" strokeWidth={2} strokeLinecap="round">
      <circle cx="6" cy="6" r="3" />
      <circle cx="6" cy="18" r="3" />
      <path d="M8.5 7.5 20 18M8.5 16.5 20 6" />
    </g>
  ),
  sparkle: <path d="M12 2 14.4 9.6 22 12l-7.6 2.4L12 22l-2.4-7.6L2 12l7.6-2.4z" fill="#fff" />,
  person: (
    <g fill="#fff">
      <circle cx="12" cy="8" r="4.2" />
      <path d="M3.5 21c.8-4.6 4.2-7 8.5-7s7.7 2.4 8.5 7z" />
    </g>
  ),
  chart: (
    <g fill="#fff">
      <rect x="3" y="12" width="4" height="9" rx="1.2" />
      <rect x="10" y="7" width="4" height="14" rx="1.2" />
      <rect x="17" y="3" width="4" height="18" rx="1.2" />
    </g>
  ),
};

const Mark: React.FC<{mark: string}> = ({mark}) => {
  if (mark === 'claude') return <Spark size={128} color="#FFF6EE" stroke={3.3} />;
  if (mark === 'instagram')
    return (
      <div style={{width: 130, height: 130, borderRadius: 38, border: '13px solid #fff', boxSizing: 'border-box', position: 'relative'}}>
        <div style={{position: 'absolute', left: 25, top: 25, width: 54, height: 54, borderRadius: '50%', border: '12px solid #fff', boxSizing: 'border-box'}} />
        <div style={{position: 'absolute', right: 12, top: 12, width: 14, height: 14, borderRadius: '50%', background: '#fff'}} />
      </div>
    );
  if (mark === 'notes')
    return (
      <div style={{position: 'absolute', inset: 0}}>
        <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 64, background: 'linear-gradient(#FFD84D,#F7BF22)'}} />
        {[0, 1, 2, 3].map((k) => (
          <i key={k} style={{position: 'absolute', left: 30, right: 30, top: 96 + k * 32, height: 4, borderRadius: 2, background: '#D7D7D7'}} />
        ))}
      </div>
    );
  return null;
};

const TileRender: React.FC<RenderProps> = ({o}) => {
  const app = str(o.props?.app);
  const glyph = str(o.props?.glyph);
  // a glyph tile is coloured by props.bg; a known app by its own logo
  const logo = glyph ? {bg: str(o.props?.bg, '#8E7CF0')} : (LOGOS[app] ?? {src: `logos/${app}.png`, bg: '#fff'});
  return (
    <div style={{position: 'absolute', inset: 0}}>
      <div style={{position: 'absolute', left: 0, top: 0, width: T, height: T, borderRadius: 60, overflow: 'hidden', background: logo.bg, boxShadow: '0 22px 40px rgba(20,30,60,.24), 0 4px 10px rgba(20,30,60,.12)'}}>
        {logo.src ? <Img src={asset(logo.src)} style={{position: 'absolute', inset: 0, width: T, height: T, objectFit: 'cover'}} /> : null}
        {logo.mark ? (
          <div style={{position: 'absolute', inset: 0, display: 'grid', placeItems: 'center'}}>
            <Mark mark={logo.mark} />
          </div>
        ) : null}
        {glyph ? (
          <div style={{position: 'absolute', inset: 0, display: 'grid', placeItems: 'center'}}>
            <svg width={124} height={124} viewBox="0 0 24 24">
              {GLYPHS[glyph]}
            </svg>
          </div>
        ) : null}
        <div style={{position: 'absolute', inset: 0, borderRadius: 60, background: 'linear-gradient(160deg,rgba(255,255,255,.38) 0,rgba(255,255,255,0) 46%)', boxShadow: 'inset 0 3px 0 rgba(255,255,255,.45), inset 0 -6px 12px rgba(0,0,0,.12)'}} />
      </div>
      {str(o.props?.label) ? (
        <div style={{position: 'absolute', left: -60, right: -60, top: T + 16, textAlign: 'center', fontFamily: FONT, fontWeight: 700, fontSize: 36, color: '#2F3440'}}>{str(o.props?.label)}</div>
      ) : null}
    </div>
  );
};

export const APP_NAMES = Object.keys(LOGOS);
export const GLYPH_NAMES = Object.keys(GLYPHS);

export const AppTile: ObjectDef = {
  size: () => ({w: T, h: T + 66, ax: 0.5, ay: 0.4}),
  verbs: {},
  assets: (o) => {
    const app = str(o.props?.app);
    return o.props?.glyph || LOGOS[app] ? [] : [`logos/${app}.png`];
  },
  anchors: () => ({tile: {x: 0, y: 0, w: T, h: T}}),
  Render: TileRender,
};

// ---------- cable ----------

const ends = (a: Box, b: Box) => {
  const ac = a.x + a.w / 2;
  const bc = b.x + b.w / 2;
  const right = bc >= ac;
  const p0 = {x: right ? a.x + a.w : a.x, y: a.y + a.h / 2};
  const p3 = {x: right ? b.x : b.x + b.w, y: b.y + b.h / 2};
  const span = Math.abs(p3.x - p0.x);
  const sag = Math.max(60, span * 0.28);
  const dir = right ? 1 : -1;
  const p1 = {x: p0.x + dir * span * 0.35, y: p0.y + sag};
  const p2 = {x: p3.x - dir * span * 0.35, y: p3.y + sag};
  return {p0, p1, p2, p3, dir};
};

const CableRender: React.FC<RenderProps> = ({o, s, t, world}) => {
  const a = world.boundsOf(str(o.props?.from), 'tile');
  const b = world.boundsOf(str(o.props?.to), 'tile');
  if (!a || !b || s.plugP <= 0) return null;
  const {p0, p1, p2, p3, dir} = ends(a, b);
  const e = inOut(clamp(s.plugP));
  const head = bezier(p0, p1, p2, p3, e);
  const ahead = bezier(p0, p1, p2, p3, Math.min(1, e + 0.01));
  const ang = (Math.atan2(ahead.y - head.y, ahead.x - head.x) * 180) / Math.PI;
  const d = `M${p0.x},${p0.y} C${p1.x},${p1.y} ${p2.x},${p2.y} ${p3.x},${p3.y}`;
  const landed = s.plugT >= 0 ? t - (s.plugT + s.plugDur) : -1;
  const flash = landed >= 0 && landed < 0.4 ? landed / 0.4 : -1;
  const color = str(o.props?.color, '#3A3B40');
  const plug = (x: number, y: number, deg: number) => (
    <g transform={`translate(${x},${y}) rotate(${deg})`}>
      <rect x={-44} y={-17} width={44} height={34} rx={9} fill={`url(#alu-${o.id})`} stroke="rgba(0,0,0,.18)" strokeWidth={1.5} />
      <rect x={-6} y={-8} width={16} height={16} rx={3} fill="#9EA2A8" />
    </g>
  );
  const minX = Math.min(p0.x, p3.x) - 80;
  const minY = Math.min(p0.y, p3.y) - 80;
  const w = Math.abs(p3.x - p0.x) + 160;
  const h = Math.abs(p3.y - p0.y) + 400;
  return (
    <svg width={w} height={h} viewBox={`${minX} ${minY} ${w} ${h}`} style={{position: 'absolute', left: minX, top: minY, overflow: 'visible'}}>
      <defs>
        <linearGradient id={`alu-${o.id}`} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#F4F5F7" />
          <stop offset=".5" stopColor="#D1D4D9" />
          <stop offset="1" stopColor="#A9ADB4" />
        </linearGradient>
      </defs>
      <path d={d} pathLength={1} fill="none" stroke="rgba(20,22,30,.16)" strokeWidth={22} strokeLinecap="round" strokeDasharray={`${e} 2`} transform="translate(0,14)" />
      <path d={d} pathLength={1} fill="none" stroke={color} strokeWidth={16} strokeLinecap="round" strokeDasharray={`${e} 2`} />
      <path d={d} pathLength={1} fill="none" stroke="rgba(255,255,255,.28)" strokeWidth={4} strokeLinecap="round" strokeDasharray={`${e} 2`} transform="translate(0,-4)" />
      {plug(p0.x + dir * 8, p0.y, dir > 0 ? 180 : 0)}
      {plug(head.x, head.y, ang)}
      {flash >= 0 ? <circle cx={p3.x} cy={p3.y} r={20 + 70 * outCubic(flash)} fill="none" stroke={C.terracotta} strokeWidth={8 * (1 - flash)} opacity={1 - flash} /> : null}
    </svg>
  );
};

export const Cable: ObjectDef = {
  size: () => ({w: 1, h: 1, ax: 0, ay: 0}),
  raw: true,
  init: () => ({plugP: 0, plugT: -1, plugDur: 0.7}),
  verbs: {
    plug: {dur: 0.7, impact: true, apply: (s, _a, c) => ({...s, plugP: c.p, plugT: c.t0, plugDur: c.dur})},
    unplug: {dur: 0.35, apply: (s, _a, c) => ({...s, plugP: 1 - c.p})},
  },
  worldBounds: (o, s, world) => {
    const a = world.boundsOf(str(o.props?.from), 'tile');
    const b = world.boundsOf(str(o.props?.to), 'tile');
    if (!a || !b) return null;
    const {p0, p3} = ends(a, b);
    const e = inOut(clamp(s.plugP));
    // while plugging, frame the travelling plug; once in, the whole run
    const x1 = p0.x + (p3.x - p0.x) * Math.max(e, 0.2);
    const x0 = Math.min(p0.x, x1);
    return {x: x0 - 120, y: Math.min(p0.y, p3.y) - 160, w: Math.abs(x1 - p0.x) + 240, h: Math.abs(p3.y - p0.y) + 380};
  },
  Render: CableRender,
};

// ---------- task list ----------

type Item = {text: string; due?: string};
const items = (o: {props?: Record<string, unknown>}): Item[] => (Array.isArray(o.props?.items) ? (o.props?.items as Item[]) : []);
const LW = 600;
const ROW = 96;
const listH = (n: number) => 112 + n * ROW + 12;

const TaskRender: React.FC<RenderProps> = ({o, s, t}) => {
  const list = items(o);
  const logo = str(o.props?.logo);
  return (
    <div style={{position: 'absolute', inset: 0, borderRadius: 40, background: 'linear-gradient(#FFFFFF,#F4F6FA)', boxShadow: '0 30px 60px rgba(30,40,80,.18), inset 0 3px 0 #fff'}}>
      <div style={{position: 'absolute', left: 26, top: 26, right: 26, height: 60, display: 'flex', alignItems: 'center', gap: 16}}>
        {logo ? <Img src={asset(`logos/${logo}.jpg`)} style={{width: 56, height: 56, borderRadius: 16, boxShadow: '0 4px 10px rgba(30,40,80,.15)'}} /> : null}
        <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 32, color: C.ink, letterSpacing: -0.5}}>{str(o.props?.title, 'Задачі')}</div>
      </div>
      {list.map((it, i) => {
        const typing = s.typing === i;
        const v = typing ? 1 : clamp(s.shown - i);
        if (v <= 0) return null;
        const pop = typing ? 1 : outBack(clamp(v * 1.6), 2.2);
        const text = typing ? it.text.slice(0, Math.round(clamp(s.typedP) * it.text.length)) : it.text;
        const check = clamp(s.checks?.[i] ?? 0);
        return (
          <div
            key={i}
            style={{
              position: 'absolute',
              left: 24,
              top: 112 + i * ROW,
              width: LW - 48,
              height: ROW - 16,
              borderRadius: 22,
              background: '#fff',
              border: '2px solid #EEF0F4',
              boxSizing: 'border-box',
              boxShadow: '0 8px 18px rgba(30,40,80,.08)',
              display: 'flex',
              alignItems: 'center',
              gap: 16,
              padding: '0 18px',
              transform: `scale(${pop})`,
              opacity: clamp(v * 4),
            }}
          >
            <div style={{flex: 'none', width: 32, height: 32, borderRadius: '50%', border: `3px solid ${check > 0 ? '#2DB47A' : '#C9CED6'}`, boxSizing: 'border-box', background: check > 0 ? `rgba(45,180,122,${check})` : 'transparent'}} />
            <div style={{flex: 1, minWidth: 0, fontFamily: FONT, fontWeight: 600, fontSize: 26, color: C.claudeText, whiteSpace: 'nowrap', overflow: 'hidden'}}>
              {text}
              {typing && s.typedP < 1 ? <Caret t={t} h={28} w={3} /> : null}
            </div>
            {it.due && (!typing || s.typedP >= 1) ? (
              <div style={{flex: 'none', fontFamily: FONT, fontWeight: 700, fontSize: 21, color: '#8A6400', background: '#FFF1C7', padding: '6px 14px', borderRadius: 14}}>{it.due}</div>
            ) : null}
          </div>
        );
      })}
    </div>
  );
};

export const TaskList: ObjectDef = {
  size: (o) => ({w: LW, h: listH(items(o).length), ax: 0.5, ay: 0.5}),
  init: () => ({shown: 0, typing: -1, typedP: 0, checks: {}}),
  verbs: {
    add: {
      dur: (a, o) => 0.25 + num(a.n, items(o).length) * 0.16,
      apply: (s, a, c, o) => {
        const n = num(a.n, items(o).length - Math.floor(s.shown));
        return {...s, shown: Math.floor(s.shown) + n * c.p};
      },
    },
    /** Hand-typing one card, slowly: the "you still write tasks yourself" beat. */
    type: {
      dur: (a, o) => {
        const i = num(a.index, 0);
        return clamp((items(o)[i]?.text.length ?? 10) * 0.07, 0.8, 2.4);
      },
      apply: (s, a, c) => {
        const i = num(a.index, Math.floor(s.shown));
        return c.p >= 1 ? {...s, typing: -1, shown: Math.max(s.shown, i + 1)} : {...s, typing: i, typedP: c.p};
      },
    },
    check: {dur: 0.3, apply: (s, a, c) => ({...s, checks: {...s.checks, [num(a.index, 0)]: c.p}})},
  },
  anchors: (o, s) => {
    const n = Math.max(1, Math.ceil(s.typing >= 0 ? s.typing + 1 : s.shown));
    return {
      filled: {x: 0, y: 0, w: LW, h: Math.min(listH(items(o).length), 112 + n * ROW + 12)},
      last: {x: 0, y: 112 + (n - 1) * ROW - 30, w: LW, h: ROW + 60},
    };
  },
  Render: TaskRender,
};
