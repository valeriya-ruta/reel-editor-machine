// The prototype's metaphor objects, rebuilt: pink paper (a prompt, or a doc
// like an offer), the yellow folder of saved prompts, and the glossy skill card
// with its «/» stamp. All shaded and a little glossy — never flat.

import React from 'react';
import {clamp, in4, inOut, lerp, outBack} from '../engine/ease';
import type {ObjectDef, RenderProps} from './core';
import {C, FONT} from './style';

const str = (v: unknown, d = '') => (typeof v === 'string' ? v : d);
const num = (v: unknown, d: number) => (typeof v === 'number' ? v : d);

// ---------- paper ----------

const paperSize = (o: {props?: Record<string, unknown>}) => ({w: num(o.props?.w, 360), h: num(o.props?.h, 228)});

/** "+ text" gets a green check, "- text" a red cross. */
const ItemLine: React.FC<{line: string}> = ({line}) => {
  const good = line.startsWith('+');
  const bad = line.startsWith('-') || line.startsWith('−');
  const text = good || bad ? line.slice(1).trim() : line;
  return (
    <div style={{display: 'flex', alignItems: 'center', gap: 12, fontWeight: 700, fontSize: 26, lineHeight: 1.2}}>
      {good || bad ? (
        <svg width={30} height={30} viewBox="0 0 24 24" style={{flex: 'none'}}>
          <circle cx="12" cy="12" r="11" fill={good ? '#2DB47A' : '#FF5A5A'} />
          <path d={good ? 'M6.5 12.5l3.5 3.5 7.5-8' : 'M8 8l8 8M16 8l-8 8'} stroke="#fff" strokeWidth={2.8} fill="none" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      ) : null}
      {text}
    </div>
  );
};

const PaperFace: React.FC<{text: string; title: string; sub: string; bars: number; items: string[]; w: number; h: number; top: number}> = ({text, title, sub, bars, items, w, h, top}) => (
  <div style={{position: 'absolute', left: 0, top, width: w, height: h, padding: '26px 28px', boxSizing: 'border-box', color: C.paperText, fontFamily: FONT}}>
    {title ? (
      <>
        <div style={{fontWeight: 800, fontSize: 44, letterSpacing: -1}}>{title}</div>
        {sub ? <div style={{fontWeight: 600, fontSize: 24, opacity: 0.7, marginTop: 2}}>{sub}</div> : null}
        {items.length ? (
          <div style={{marginTop: 22, display: 'flex', flexDirection: 'column', gap: 16}}>
            {items.map((line, i) => (
              <ItemLine key={i} line={line} />
            ))}
          </div>
        ) : (
          <div style={{marginTop: 22, display: 'flex', flexDirection: 'column', gap: 16}}>
            {Array.from({length: bars}).map((_, i) => (
              <div key={i} style={{height: 13, borderRadius: 7, width: `${[100, 88, 94, 70, 96, 62, 84][i % 7]}%`, background: 'rgba(120,40,70,.18)'}} />
            ))}
          </div>
        )}
      </>
    ) : (
      <div style={{fontWeight: 600, fontSize: 26, lineHeight: 1.32}}>{text}</div>
    )}
  </div>
);

const PaperRender: React.FC<RenderProps> = ({o, s, t}) => {
  const {w, h} = paperSize(o);
  const half = h / 2;
  const fold = clamp(s.fold); // 0 flat, 1 bottom half folded up behind the top
  const text = str(o.props?.text);
  const title = str(o.props?.title);
  const sub = str(o.props?.sub);
  const bars = num(o.props?.bars, 5);
  const items = Array.isArray(o.props?.items) ? (o.props?.items as unknown[]).map(String) : [];
  if (o.props?.blank) {
    // a blank white page with a blinking cursor: nothing comes
    return (
      <div style={{position: 'absolute', inset: 0, borderRadius: 16, background: 'linear-gradient(#FFFFFF,#FAF8F3)', boxShadow: '0 34px 64px rgba(30,40,80,.24), 0 0 0 2px rgba(30,40,80,.06)', overflow: 'hidden'}}>
        {Array.from({length: 9}).map((_, i) => (
          <div key={i} style={{position: 'absolute', left: 0, right: 0, top: 110 + i * 46, height: 2, background: '#E3E9F3'}} />
        ))}
        <div style={{position: 'absolute', left: 64, top: 0, bottom: 0, width: 2, background: '#F4C3CC'}} />
        <div style={{position: 'absolute', left: 84, top: 58, width: 6, height: 50, borderRadius: 3, background: C.ink, opacity: Math.floor(t * 2) % 2 ? 0 : 1}} />
      </div>
    );
  }
  return (
    <div style={{position: 'absolute', inset: 0, perspective: 1260, filter: 'drop-shadow(0 18px 24px rgba(150,50,85,.28))'}}>
      <div style={{position: 'absolute', left: 0, top: 0, width: w, height: half, overflow: 'hidden', borderRadius: '9px 9px 0 0', background: `linear-gradient(${C.paper[0]},${C.paper[1]})`}}>
        <PaperFace text={text} title={title} sub={sub} bars={bars} items={items} w={w} h={h} top={0} />
      </div>
      <div style={{position: 'absolute', left: 0, top: half, width: w, height: half, transformStyle: 'preserve-3d', transformOrigin: '50% 0%', transform: `rotateX(${fold * 180}deg)`}}>
        <div style={{position: 'absolute', inset: 0, overflow: 'hidden', backfaceVisibility: 'hidden', borderRadius: '0 0 9px 9px', background: `linear-gradient(${C.paper[1]},${C.paper[2]})`}}>
          <PaperFace text={text} title={title} sub={sub} bars={bars} items={items} w={w} h={h} top={-half} />
          <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 9, background: 'linear-gradient(rgba(140,40,80,.18),rgba(140,40,80,0))'}} />
        </div>
        <div style={{position: 'absolute', inset: 0, backfaceVisibility: 'hidden', transform: 'rotateX(180deg)', borderRadius: '9px 9px 0 0', background: `linear-gradient(${C.paperBack[0]},${C.paperBack[1]})`}} />
      </div>
    </div>
  );
};

export const Paper: ObjectDef = {
  size: (o) => ({...paperSize(o), ax: 0.5, ay: 0.5}),
  init: (o) => ({fold: o.props?.folded ? 1 : 0}),
  verbs: {
    fold: {dur: 0.5, apply: (s, _a, c) => ({...s, fold: lerp(s.fold, 1, inOut(c.p))})},
    unfold: {dur: 0.5, apply: (s, _a, c) => ({...s, fold: lerp(s.fold, 0, inOut(c.p))})},
  },
  Render: PaperRender,
};

// ---------- folder ----------

const FolderRender: React.FC<RenderProps> = ({o, s}) => {
  const open = clamp(s.open);
  const gulp = s.gulpP > 0 && s.gulpP < 1 ? Math.sin(Math.PI * s.gulpP) : 0;
  return (
    <div style={{position: 'absolute', inset: 0, transform: `scale(${1 + 0.15 * gulp})`, transformOrigin: '50% 60%'}}>
      <div style={{position: 'absolute', left: 0, top: 24, width: 240, height: 180, borderRadius: 24, background: `linear-gradient(${C.folder[0]},${C.folder[1]})`}}>
        <div style={{position: 'absolute', left: 12, top: -24, width: 96, height: 42, borderRadius: '18px 18px 0 0', background: '#F2AE0C'}} />
      </div>
      <div style={{position: 'absolute', left: 30, top: 36, width: 180, height: 120, borderRadius: 12, background: `linear-gradient(${C.paper[0]},#F7B6C9)`, opacity: s.full ? 1 : 0}} />
      <div
        style={{
          position: 'absolute',
          left: 0,
          top: 72,
          width: 240,
          height: 132,
          borderRadius: '18px 18px 24px 24px',
          background: `linear-gradient(${C.folderFront[0]},${C.folderFront[1]})`,
          boxShadow: '0 6px 12px rgba(120,80,0,.35), inset 0 6px 0 rgba(255,255,255,.6)',
          transformOrigin: '50% 100%',
          transform: `scaleY(${lerp(1, 0.45, open) * (1 - 0.22 * gulp)}) skewX(${-12 * open}deg)`,
        }}
      />
      {str(o.props?.label) ? (
        <div style={{position: 'absolute', left: -36, right: -36, top: 216, textAlign: 'center', fontFamily: FONT, fontSize: 36, fontWeight: 700, color: '#2F3440'}}>{str(o.props?.label)}</div>
      ) : null}
    </div>
  );
};

export const Folder: ObjectDef = {
  size: () => ({w: 240, h: 264}),
  init: (o) => ({open: 0, gulpP: 0, full: !!o.props?.full}),
  verbs: {
    open: {dur: 0.22, apply: (s, _a, c) => ({...s, open: lerp(s.open, 1, c.p)})},
    close: {dur: 0.25, apply: (s, _a, c) => ({...s, open: lerp(s.open, 0, c.p)})},
    gulp: {dur: 0.28, apply: (s, _a, c) => ({...s, gulpP: c.p, full: s.full || c.p > 0.3})},
    empty: {dur: 0.05, apply: (s) => ({...s, full: false})},
  },
  Render: FolderRender,
};

// ---------- skill card + «/» stamp ----------

const SkillRender: React.FC<RenderProps> = ({o, s, t}) => {
  const p = clamp(s.stampP);
  const landed = s.stampT >= 0 ? t - (s.stampT + 0.26) : -1;
  const dip = landed >= 0 && landed < 0.16 ? Math.sin((Math.PI * landed) / 0.16) : 0;
  return (
    <div style={{position: 'absolute', inset: 0, transform: `scale(${1 - 0.06 * dip})`}}>
      <div style={{position: 'absolute', inset: 0, borderRadius: 36, background: `linear-gradient(135deg,${C.skill[0]},${C.skill[1]})`, boxShadow: '0 24px 48px rgba(170,60,95,.26), inset 0 3px 0 rgba(255,255,255,.8)', overflow: 'hidden'}}>
        <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: '50%', background: 'linear-gradient(rgba(255,255,255,.45),rgba(255,255,255,0))'}} />
        <div style={{position: 'absolute', left: 24, top: 24, width: 90, height: 90, borderRadius: '50%', background: 'rgba(160,60,95,.15)', boxShadow: 'inset 0 3px 9px rgba(120,30,60,.25)'}} />
        <div style={{position: 'absolute', left: 138, top: 26, fontFamily: FONT, fontWeight: 800, fontSize: 38, color: C.ink, letterSpacing: -0.6, whiteSpace: 'nowrap'}}>{str(o.props?.name, '/скіл')}</div>
        <div style={{position: 'absolute', left: 138, top: 80, fontFamily: FONT, fontWeight: 500, fontSize: 21, color: '#6A3A4B', whiteSpace: 'nowrap'}}>{str(o.props?.sub, 'скіл · збережено')}</div>
      </div>
      {p > 0 ? (
        <div
          style={{
            position: 'absolute',
            left: 24,
            top: 24,
            width: 90,
            height: 90,
            borderRadius: '50%',
            background: 'radial-gradient(circle at 35% 30%,#4A4B52,#141416 70%)',
            color: '#fff',
            display: 'grid',
            placeItems: 'center',
            fontFamily: FONT,
            fontWeight: 800,
            fontSize: 54,
            lineHeight: 1,
            boxShadow: '0 9px 18px rgba(0,0,0,.35), inset 0 3px 0 rgba(255,255,255,.25)',
            transform: `scale(${lerp(3.2, 1, in4(p))}) rotate(${lerp(-40, -8, p)}deg)`,
          }}
        >
          /
        </div>
      ) : null}
    </div>
  );
};

export const SkillCard: ObjectDef = {
  size: () => ({w: 498, h: 138, ax: 0.5, ay: 0.5}),
  init: () => ({stampP: 0, stampT: -1}),
  verbs: {
    stamp: {dur: 0.26, impact: true, apply: (s, _a, c) => ({...s, stampP: c.p, stampT: c.t0})},
  },
  Render: SkillRender,
};

export const popIn = (p: number) => outBack(clamp(p));
