// Laptop: a dark aluminium shell around a crisp screen. The screen shows one
// window at a time — Claude, a video call, or a recording player — and swaps
// them with a minimize/restore. Sizes are the prototype's ×3.

import React from 'react';
import {Img} from 'remotion';
import {clamp, inOut, lerp, outBack, outCubic} from '../engine/ease';
import type {ObjectDef, RenderProps, State} from './core';
import {asset, C, contactShadow, FONT, SERIF} from './style';
import {Bars, Caret, Dots, SendArrow, Spark} from './ui';

const SX = 111; // screen offset inside the lid box
const SY = 24;
const WX = SX + 18; // window offset
const WY = SY + 18;
const WW = 642;
const WH = 342;
const INPUT = {x: 42, y: 192, w: 558, h: 114};
const CALL_SECONDS = 59 * 60 + 47;

const str = (v: unknown, d = '') => (typeof v === 'string' ? v : d);
const num = (v: unknown, d: number) => (typeof v === 'number' ? v : d);

/** Rough caret position for the input box (22px Onest ≈ 11.5px a character). */
const caretAt = (typed: string) => {
  const perLine = 41;
  const n = typed.length;
  const line = Math.min(2, Math.floor(n / perLine));
  const col = n - line * perLine;
  return {x: INPUT.x + 21 + col * 11.5, y: INPUT.y + 15 + line * 30};
};

const ClaudeWindow: React.FC<{s: State; t: number}> = ({s, t}) => {
  const chat = s.chatP > 0;
  const replyP: number = s.replyP;
  return (
    <>
      <div style={{position: 'absolute', left: 0, right: 0, top: 84, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 12, fontFamily: SERIF, fontSize: 30, color: C.claudeText, opacity: 1 - clamp(s.chatP * 2)}}>
        <Spark size={33} />
        {str(s.greet, 'Добрий день, Руто')}
      </div>
      {chat ? (
        <div style={{position: 'absolute', left: 30, right: 30, top: 54, fontFamily: FONT}}>
          <div style={{display: 'flex', justifyContent: 'flex-end', opacity: clamp(s.chatP * 2), transform: `translateY(${(1 - outCubic(s.chatP)) * 24}px)`}}>
            <div style={{background: C.bubble, borderRadius: 18, padding: '9px 16px', fontSize: 20, color: C.claudeText, maxWidth: 420, lineHeight: 1.3}}>{s.chatUser}</div>
          </div>
          {replyP > 0 && replyP < 0.4 ? (
            <div style={{marginTop: 18}}>
              <Dots t={t} size={9} />
            </div>
          ) : null}
          {replyP >= 0.4 ? (
            <div style={{marginTop: 14, opacity: clamp((replyP - 0.4) * 4)}}>
              <div style={{display: 'flex', alignItems: 'center', gap: 9, fontSize: 21, fontWeight: 700, color: C.claudeText}}>
                <Spark size={22} stroke={3.6} />
                {s.replyTitle}
              </div>
              <div style={{marginTop: 10, width: 420}}>
                <Bars widths={s.replyBars} h={9} gap={9} reveal={clamp((replyP - 0.45) / 0.55)} />
              </div>
            </div>
          ) : null}
        </div>
      ) : null}
      {/* input */}
      <div
        style={{
          position: 'absolute',
          left: INPUT.x,
          top: chat ? INPUT.y + 12 : INPUT.y,
          width: INPUT.w,
          height: chat ? 84 : INPUT.h,
          background: '#fff',
          border: `3px solid ${C.claudeLine}`,
          borderRadius: 24,
          boxSizing: 'border-box',
          padding: '12px 66px 12px 21px',
          fontFamily: FONT,
          fontSize: 22,
          lineHeight: 1.35,
          color: C.claudeText,
          boxShadow: '0 3px 9px rgba(0,0,0,.05)',
          overflow: 'hidden',
        }}
      >
        {s.typed ? (
          <span style={{background: s.sel ? '#CFE3FF' : 'transparent'}}>{s.typed}</span>
        ) : (
          <span style={{color: C.claudeMuted}}>{chat ? 'Відповісти…' : 'Напиши повідомлення…'}</span>
        )}
        <Caret t={t} h={24} />
        <div
          style={{
            position: 'absolute',
            right: 15,
            bottom: 12,
            width: 39,
            height: 39,
            borderRadius: 12,
            background: 'linear-gradient(#E58A6B,#CF6A49)',
            display: 'grid',
            placeItems: 'center',
            boxShadow: '0 3px 6px rgba(150,60,30,.35)',
            transform: `scale(${1 - 0.25 * Math.sin(Math.PI * clamp(s.sendP))})`,
          }}
        >
          <SendArrow size={21} />
        </div>
      </div>
    </>
  );
};

const Tile: React.FC<{left: number; who: 'client' | 'me'; s: State; t: number}> = ({left, who, s, t}) => {
  const speaking = s.speaking === who && s.ended < 1;
  const bars = [0, 1, 2].map((i) => 6 + 12 * Math.abs(Math.sin(t * 9 + i * 1.7)));
  return (
    <div
      style={{
        position: 'absolute',
        left,
        top: 54,
        width: 294,
        height: 204,
        borderRadius: 15,
        overflow: 'hidden',
        background: who === 'client' ? 'linear-gradient(150deg,#C7B6EC,#8F7BC4)' : 'linear-gradient(150deg,#F3D9C8,#D9A88E)',
        boxShadow: speaking ? 'inset 0 0 0 4px #34C759' : 'none',
      }}
    >
      {who === 'client' ? (
        <div style={{position: 'absolute', left: 99, top: 46, width: 96, height: 96, borderRadius: '50%', background: 'linear-gradient(150deg,#FFFFFF,#E9E2F7)', display: 'grid', placeItems: 'center', fontFamily: FONT, fontWeight: 800, fontSize: 44, color: '#6B57A8', boxShadow: '0 6px 14px rgba(40,20,80,.25)'}}>
          О
        </div>
      ) : (
        <Img src={asset(`chibi/${str(s.meFace, 'neutral')}.png`)} style={{position: 'absolute', left: 37, top: -6, width: 220}} />
      )}
      <div style={{position: 'absolute', left: 9, bottom: 9, display: 'flex', alignItems: 'center', gap: 6, padding: '3px 9px', borderRadius: 8, background: 'rgba(0,0,0,.38)', color: '#fff', fontFamily: FONT, fontSize: 14, fontWeight: 600}}>
        {speaking ? (
          <span style={{display: 'flex', gap: 2, alignItems: 'flex-end', height: 16}}>
            {bars.map((h, i) => (
              <i key={i} style={{display: 'block', width: 3, height: h * 0.8, borderRadius: 2, background: '#34C759'}} />
            ))}
          </span>
        ) : null}
        {who === 'client' ? str(s.client, 'Олена') : 'Рута'}
      </div>
    </div>
  );
};

const CallWindow: React.FC<{s: State; t: number}> = ({s, t}) => {
  const recOn = s.rec > 0;
  const recSec = Math.max(0, Math.floor((t - s.recT0) * 1 + 12));
  return (
    <div style={{position: 'absolute', inset: 0, background: '#202124'}}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 36, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#E8EAED', fontFamily: FONT, fontSize: 15, fontWeight: 600}}>
        {str(s.client, 'Олена')} · дзвінок
      </div>
      {recOn ? (
        <div style={{position: 'absolute', left: 12, top: 6, display: 'flex', alignItems: 'center', gap: 7, padding: '3px 10px', borderRadius: 8, background: 'rgba(234,67,53,.18)', transform: `scale(${outBack(clamp(s.rec), 2.4)})`, transformOrigin: '0 50%'}}>
          <i style={{display: 'block', width: 12, height: 12, borderRadius: '50%', background: '#EA4335', opacity: 0.55 + 0.45 * Math.abs(Math.cos(t * 3))}} />
          <span style={{fontFamily: FONT, fontWeight: 800, fontSize: 15, color: '#FF8A80', letterSpacing: 1}}>REC</span>
          <span style={{fontFamily: FONT, fontWeight: 600, fontSize: 14, color: '#E8EAED', fontVariantNumeric: 'tabular-nums'}}>
            00:{String(recSec % 60).padStart(2, '0')}
          </span>
        </div>
      ) : null}
      <Tile left={18} who="client" s={s} t={t} />
      <Tile left={330} who="me" s={s} t={t} />
      <div style={{position: 'absolute', left: 0, right: 0, top: 276, display: 'flex', justifyContent: 'center', gap: 14}}>
        {[0, 1].map((i) => (
          <div key={i} style={{width: 42, height: 42, borderRadius: '50%', background: '#3C4043', display: 'grid', placeItems: 'center'}}>
            <i style={{display: 'block', width: i ? 18 : 10, height: i ? 13 : 18, borderRadius: i ? 3 : 6, background: '#E8EAED'}} />
          </div>
        ))}
        <div style={{width: 72, height: 42, borderRadius: 21, background: '#EA4335', display: 'grid', placeItems: 'center'}}>
          <i style={{display: 'block', width: 30, height: 10, borderRadius: 6, background: '#fff', transform: 'rotate(-8deg)'}} />
        </div>
      </div>
      {s.ended > 0 ? (
        <div style={{position: 'absolute', inset: 0, background: `rgba(32,33,36,${0.92 * clamp(s.ended * 1.5)})`, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: 8, fontFamily: FONT}}>
          <div style={{fontSize: 26, fontWeight: 700, color: '#fff', opacity: clamp(s.ended * 2 - 0.5), transform: `translateY(${(1 - outCubic(s.ended)) * 14}px)`}}>Дзвінок завершено</div>
          <div style={{fontSize: 17, color: '#9AA0A6', opacity: clamp(s.ended * 2 - 0.8)}}>59:47</div>
        </div>
      ) : null}
    </div>
  );
};

const fmt = (sec: number) => `${String(Math.floor(sec / 60)).padStart(2, '0')}:${String(Math.floor(sec % 60)).padStart(2, '0')}`;

const PlayerWindow: React.FC<{s: State; t: number}> = ({s}) => {
  const p: number = s.scrubP;
  return (
    <div style={{position: 'absolute', inset: 0, background: '#111214'}}>
      <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 36, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#C8CAD0', fontFamily: FONT, fontSize: 15, fontWeight: 600}}>
        запис-дзвінка.mp4
      </div>
      {/* the frozen call, small */}
      <div style={{position: 'absolute', left: 81, top: 48, width: 480, height: 214, borderRadius: 12, background: '#202124', overflow: 'hidden'}}>
        <div style={{position: 'absolute', left: 14, top: 24, width: 218, height: 152, borderRadius: 10, background: 'linear-gradient(150deg,#C7B6EC,#8F7BC4)'}} />
        <div style={{position: 'absolute', left: 248, top: 24, width: 218, height: 152, borderRadius: 10, background: 'linear-gradient(150deg,#F3D9C8,#D9A88E)'}} />
        <div style={{position: 'absolute', left: 216, top: 82, width: 48, height: 48, borderRadius: '50%', background: 'rgba(255,255,255,.88)', display: 'grid', placeItems: 'center'}}>
          <i style={{display: 'block', width: 0, height: 0, borderLeft: '16px solid #202124', borderTop: '10px solid transparent', borderBottom: '10px solid transparent', marginLeft: 5}} />
        </div>
      </div>
      {/* timeline */}
      <div style={{position: 'absolute', left: 24, right: 24, top: 282}}>
        <div style={{position: 'relative', height: 10, borderRadius: 5, background: '#3A3C42'}}>
          <div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: `${p * 100}%`, borderRadius: 5, background: C.terracotta}} />
          <div style={{position: 'absolute', left: `${p * 100}%`, top: -7, width: 24, height: 24, marginLeft: -12, borderRadius: '50%', background: '#fff', boxShadow: '0 2px 6px rgba(0,0,0,.5)'}} />
        </div>
        <div style={{display: 'flex', justifyContent: 'space-between', marginTop: 12, fontFamily: FONT, fontSize: 17, fontWeight: 600, color: '#E8EAED', fontVariantNumeric: 'tabular-nums'}}>
          <span>{fmt(p * CALL_SECONDS)}</span>
          <span style={{color: '#9AA0A6'}}>{fmt(CALL_SECONDS)}</span>
        </div>
      </div>
    </div>
  );
};

const WINDOWS: Record<string, React.FC<{s: State; t: number}>> = {claude: ClaudeWindow, call: CallWindow, player: PlayerWindow};
const TITLES: Record<string, string> = {claude: 'Claude', call: '', player: ''};

const Window: React.FC<{name: string; s: State; t: number; style: React.CSSProperties}> = ({name, s, t, style}) => {
  const Body = WINDOWS[name] ?? ClaudeWindow;
  const light = name === 'claude';
  return (
    <div style={{position: 'absolute', left: 18, top: 18, width: WW, height: WH, borderRadius: 21, overflow: 'hidden', background: light ? C.cream : '#202124', boxShadow: '0 6px 24px rgba(30,40,70,.18)', transformOrigin: '50% 100%', ...style}}>
      {light ? (
        <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: 36, borderBottom: `3px solid ${C.claudeHair}`, display: 'flex', alignItems: 'center', gap: 7, padding: '0 15px', boxSizing: 'border-box'}}>
          {[0, 1, 2].map((i) => (
            <i key={i} style={{display: 'block', width: 12, height: 12, borderRadius: '50%', background: '#E0DBD2'}} />
          ))}
          <b style={{position: 'absolute', left: 0, right: 0, textAlign: 'center', fontFamily: FONT, fontSize: 16, fontWeight: 500, color: '#7A746C'}}>{TITLES[name]}</b>
        </div>
      ) : null}
      <div style={{position: 'absolute', inset: 0}}>
        <Body s={s} t={t} />
      </div>
    </div>
  );
};

const Render: React.FC<RenderProps> = ({s, t}) => {
  const swap = clamp(s.winP);
  const e = inOut(swap);
  return (
    <div style={{position: 'absolute', inset: 0}}>
      <div style={{position: 'absolute', left: -60, top: 466, width: 1020, height: 66, borderRadius: '50%', background: contactShadow()}} />
      {/* lid */}
      <div style={{position: 'absolute', left: 90, top: 0, width: 720, height: 468, borderRadius: '33px 33px 12px 12px', background: C.deviceDark, boxShadow: 'inset 0 0 0 3px rgba(255,255,255,.07), 0 24px 54px rgba(0,0,0,.16)'}}>
        <div style={{position: 'absolute', left: 354, top: 8, width: 12, height: 12, borderRadius: '50%', background: '#0B0B0C', boxShadow: 'inset 0 0 3px rgba(120,160,255,.6)'}} />
      </div>
      {/* screen */}
      <div style={{position: 'absolute', left: SX, top: SY, width: 678, height: 420, overflow: 'hidden', borderRadius: 9, background: 'linear-gradient(160deg,#E8F0FE,#DCE6F8)'}}>
        {s.winPrev && swap < 1 ? (
          <Window name={s.winPrev} s={s} t={t} style={{transform: `translateY(${e * 300}px) scale(${lerp(1, 0.12, e)})`, opacity: 1 - e}} />
        ) : null}
        <Window
          name={s.win}
          s={s}
          t={t}
          style={s.winPrev && swap < 1 ? {transform: `translateY(${(1 - e) * 300}px) scale(${lerp(0.12, 1, outBack(swap, 1.2))})`, opacity: clamp(swap * 2.5)} : {}}
        />
        <div style={{position: 'absolute', left: 219, bottom: 9, width: 240, height: 27, borderRadius: 9, background: 'rgba(255,255,255,.75)', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 12, boxShadow: '0 3px 6px rgba(0,0,0,.08)'}}>
          {['#C9D3E2', C.terracotta, '#202124', '#C9D3E2'].map((c, i) => (
            <i key={i} style={{display: 'block', width: 15, height: 15, borderRadius: 4.5, background: c}} />
          ))}
        </div>
        <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(115deg,rgba(255,255,255,.22) 0,rgba(255,255,255,0) 38%)', pointerEvents: 'none'}} />
      </div>
      {/* base */}
      <div style={{position: 'absolute', left: 0, top: 468, width: 900, height: 36, borderRadius: '6px 6px 36px 36px', background: C.alu, boxShadow: '0 6px 9px rgba(0,0,0,.12)'}}>
        <div style={{position: 'absolute', left: 375, top: 0, width: 150, height: 12, borderRadius: '0 0 15px 15px', background: 'linear-gradient(#B9BDC3,#CDD0D5)'}} />
      </div>
    </div>
  );
};

export const Laptop: ObjectDef = {
  size: () => ({w: 900, h: 504}),
  init: (o) => ({
    win: str(o.props?.window, 'claude'),
    winPrev: null,
    winP: 1,
    greet: str(o.props?.greet, 'Добрий день, Руто'),
    client: str(o.props?.client, 'Олена'),
    typed: '',
    sel: false,
    sendP: 0,
    chatUser: '',
    chatP: 0,
    replyP: 0,
    replyTitle: '',
    replyBars: [100, 86, 92, 60],
    rec: 0,
    recT0: 0,
    ended: 0,
    speaking: null,
    meFace: 'neutral',
    scrubP: 0,
  }),
  verbs: {
    window: {
      dur: 0.45,
      required: ['name'],
      check: (a) => (WINDOWS[str(a.name)] ? null : `unknown window "${String(a.name)}" (have: ${Object.keys(WINDOWS).join(', ')})`),
      apply: (s, a, c) => (s.win === a.name ? s : {...s, winPrev: s.win, win: a.name, winP: c.p}),
    },
    type: {
      dur: (a) => clamp(str(a.text).length * 0.035, 0.5, 2.6),
      required: ['text'],
      apply: (s, a, c) => {
        const text = str(a.text);
        return {...s, typed: text.slice(0, Math.round(c.p * text.length)), sel: false};
      },
    },
    select: {dur: 0.05, apply: (s) => ({...s, sel: true})},
    clear: {
      dur: 0.25,
      apply: (s, _a, c) => ({...s, typed: s.typed.slice(0, Math.round((1 - c.p) * s.typed.length)), sel: false}),
    },
    send: {
      dur: 0.45,
      // the typed text becomes the sent bubble; the fold re-runs every frame, so s.typed is still the full text here
      apply: (s, _a, c) => ({...s, chatUser: s.typed || s.chatUser, typed: '', sel: false, sendP: c.p, chatP: Math.max(s.chatP, c.p)}),
    },
    ask: {
      // type straight into the chat as a sent message (skips the input box)
      dur: 0.4,
      required: ['text'],
      apply: (s, a, c) => ({...s, chatUser: str(a.text), chatP: c.p, replyP: 0}),
    },
    reply: {
      dur: 1.1,
      required: ['title'],
      apply: (s, a, c) => ({
        ...s,
        replyTitle: str(a.title),
        replyBars: Array.isArray(a.bars) ? (a.bars as number[]) : s.replyBars,
        replyP: c.p,
      }),
    },
    /** (Re)start a call: the "call ended" overlay clears and the call window comes up. */
    call: {
      dur: 0.4,
      apply: (s, a, c) => ({
        ...s,
        ended: Math.min(s.ended, 1 - c.p),
        client: str(a.client, s.client),
        ...(s.win !== 'call' ? {winPrev: s.win, win: 'call', winP: c.p} : {}),
      }),
    },
    rec: {dur: 0.35, apply: (s, _a, c) => ({...s, rec: c.p, recT0: c.t0})},
    hangup: {dur: 0.5, apply: (s, _a, c) => ({...s, ended: c.p})},
    speak: {dur: 0.05, apply: (s, a) => ({...s, speaking: a.who ?? null})},
    face: {dur: 0.05, required: ['pose'], apply: (s, a) => ({...s, meFace: a.pose})},
    scrub: {
      dur: 1.2,
      apply: (s, a, c) => ({...s, scrubP: lerp(num(a.from, s.scrubP), num(a.to, 0.1), c.p)}),
    },
  },
  anchors: (_o, s) => {
    const caret = caretAt(s.typed);
    return {
      screen: {x: SX, y: SY, w: 678, h: 420},
      window: {x: WX, y: WY, w: WW, h: WH},
      input: {x: WX + INPUT.x, y: WY + INPUT.y, w: INPUT.w, h: INPUT.h},
      caret: {x: WX + caret.x - 70, y: WY + caret.y - 18, w: 140, h: 60},
      chat: {x: WX + 20, y: WY + 70, w: 600, h: 190},
      rec: {x: WX, y: WY - 6, w: 220, h: 50},
      tiles: {x: WX + 18, y: WY + 54, w: 606, h: 204},
      client: {x: WX + 18, y: WY + 54, w: 294, h: 204},
      me: {x: WX + 330, y: WY + 54, w: 294, h: 204},
      timeline: {x: WX + 14, y: WY + 262, w: 614, h: 76},
    };
  },
  Render,
};
