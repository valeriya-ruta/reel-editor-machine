// Phone with the Claude mobile app: typing, a tap ripple, a bottom sheet and
// chat bubbles. The prototype's phone ×3; `phone_dive` fills the frame with it.

import React from 'react';
import {clamp, outBack, outCubic} from '../engine/ease';
import type {ObjectDef, RenderProps} from './core';
import {C, contactShadow, FONT, SERIF} from './style';
import {Bars, Caret, Dots, Spark} from './ui';

const W = 120;
const H = 234;
const str = (v: unknown, d = '') => (typeof v === 'string' ? v : d);

const Ripple: React.FC<{p: number; side: 'left' | 'right'}> = ({p, side}) =>
  p > 0 && p < 1 ? (
    <div
      style={{
        position: 'absolute',
        [side]: 2.7,
        top: 1.8,
        width: 15,
        height: 15,
        borderRadius: '50%',
        background: 'rgba(217,119,87,.35)',
        transform: `scale(${1 + 2 * outCubic(p)})`,
        opacity: 1 - p,
      }}
    />
  ) : null;

const Render: React.FC<RenderProps> = ({s, t}) => {
  const chat = s.chatP > 0;
  const sheet = clamp(s.sheetP);
  return (
    <div style={{position: 'absolute', inset: 0}}>
      <div style={{position: 'absolute', left: -12, top: H - 6, width: W + 24, height: 18, borderRadius: '50%', background: contactShadow(0.3)}} />
      <div style={{position: 'absolute', inset: 0, borderRadius: 21, background: 'linear-gradient(145deg,#45464C,#141416)', boxShadow: '0 15px 30px rgba(0,0,0,.28), inset 0 0 0 1.8px rgba(255,255,255,.18)'}}>
        <div style={{position: 'absolute', inset: 5.4, borderRadius: 16.2, background: C.cream, overflow: 'hidden', fontFamily: FONT}}>
          <div style={{position: 'absolute', left: 42.6, top: 6, width: 24, height: 7.2, borderRadius: 6, background: '#0B0B0C'}} />
          <div style={{position: 'absolute', left: 0, right: 0, top: 19.5, textAlign: 'center', fontSize: 9.6, fontWeight: 600, color: '#3A3631'}}>Claude</div>
          <div style={{position: 'absolute', left: 9, right: 9, top: 34.5, height: 1, background: C.claudeHair}} />
          <div style={{position: 'absolute', left: 0, right: 0, top: 72, textAlign: 'center', fontFamily: SERIF, fontSize: 11.4, color: C.claudeText, opacity: chat ? 0 : 1}}>
            {str(s.greet, 'Добрий день, Руто')}
          </div>
          {chat ? (
            <>
              <div style={{position: 'absolute', right: 7.2, top: 45, padding: '4.2px 7.2px', borderRadius: 9, background: C.bubble, fontSize: 9.3, color: C.claudeText, opacity: clamp(s.chatP * 2), transform: `translateY(${(1 - outCubic(s.chatP)) * 9}px)`}}>
                {s.chatUser}
              </div>
              {s.replyP > 0 && s.replyP < 0.4 ? (
                <div style={{position: 'absolute', left: 7.8, top: 66}}>
                  <Dots t={t} size={4.2} />
                </div>
              ) : null}
              {s.replyP >= 0.4 ? (
                <div style={{position: 'absolute', left: 7.8, top: 64, width: 90, opacity: clamp((s.replyP - 0.4) * 4)}}>
                  <div style={{display: 'flex', alignItems: 'center', gap: 3, fontSize: 9, fontWeight: 700, color: C.claudeText}}>
                    <Spark size={11} stroke={4} />
                    {s.replyTitle}
                  </div>
                  <div style={{marginTop: 4.8}}>
                    <Bars widths={[100, 86, 92, 60]} h={4.8} gap={4.8} reveal={clamp((s.replyP - 0.45) / 0.55)} />
                  </div>
                </div>
              ) : null}
            </>
          ) : null}
          {/* input pill */}
          <div style={{position: 'absolute', left: 7.2, right: 7.2, bottom: 10.2, height: 21, background: '#fff', border: `1.2px solid ${C.claudeLine}`, borderRadius: 10.5, boxSizing: 'border-box'}}>
            <div style={{position: 'absolute', left: 2.7, top: 1.8, width: 15, height: 15, borderRadius: '50%', background: '#F1EDE6', fontSize: 13, lineHeight: '15px', textAlign: 'center', color: '#6B655E'}}>+</div>
            <span style={{position: 'absolute', left: 21, right: 21, top: 4.2, fontSize: 9.3, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', color: s.typed ? C.claudeText : C.claudeMuted}}>
              {s.typed || 'Напиши повідомлення…'}
              {s.typed ? <Caret t={t} h={10} w={1} /> : null}
            </span>
            <div style={{position: 'absolute', right: 2.7, top: 1.8, width: 15, height: 15, borderRadius: '50%', background: C.terracotta}} />
            <Ripple p={s.tapP} side={s.tapAt === 'plus' ? 'left' : 'right'} />
          </div>
          {/* bottom sheet */}
          {sheet > 0 ? (
            <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 102, background: '#fff', borderRadius: '15px 15px 0 0', boxShadow: '0 -6px 15px rgba(0,0,0,.12)', transform: `translateY(${(1 - outBack(sheet, 1.3)) * 110}%)`}}>
              <div style={{position: 'absolute', left: 42, top: 4.8, width: 24, height: 3, borderRadius: 3, background: '#D6D2CB'}} />
              <div style={{position: 'absolute', left: 9, top: 12, fontSize: 10.8, fontWeight: 700, color: C.claudeText}}>{s.sheetTitle}</div>
              <div style={{position: 'absolute', left: 39, top: 33, width: 30, height: 22.5, borderRadius: 3.6, background: 'linear-gradient(#E4E6EA,#CDD1D7)'}} />
              <p style={{position: 'absolute', left: 0, right: 0, top: 63, margin: 0, textAlign: 'center', fontSize: 9.9, fontWeight: 700, color: C.claudeText}}>{s.sheetBody}</p>
              <p style={{position: 'absolute', left: 0, right: 0, top: 76.5, margin: 0, textAlign: 'center', fontSize: 8.1, color: '#8A847C'}}>{s.sheetSub}</p>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
};

export const Phone: ObjectDef = {
  size: () => ({w: W, h: H}),
  init: () => ({typed: '', chatUser: '', chatP: 0, replyP: 0, replyTitle: '', tapP: 0, tapAt: 'send', sheetP: 0, sheetTitle: '', sheetBody: '', sheetSub: ''}),
  verbs: {
    type: {
      dur: (a) => clamp(str(a.text).length * 0.055, 0.4, 1.6),
      required: ['text'],
      apply: (s, a, c) => ({...s, typed: str(a.text).slice(0, Math.round(c.p * str(a.text).length))}),
    },
    tap: {dur: 0.35, apply: (s, a, c) => ({...s, tapP: c.p, tapAt: str(a.at, 'send')})},
    send: {dur: 0.4, apply: (s, _a, c) => ({...s, chatUser: s.typed || s.chatUser, typed: '', chatP: Math.max(s.chatP, c.p), tapP: c.p, tapAt: 'send'})},
    reply: {dur: 1.0, required: ['title'], apply: (s, a, c) => ({...s, replyTitle: str(a.title), replyP: c.p})},
    sheet: {
      dur: 0.45,
      apply: (s, a, c) => ({...s, sheetP: c.p, sheetTitle: str(a.title, 'Файли'), sheetBody: str(a.body, 'Тут порожньо'), sheetSub: str(a.sub)}),
    },
    closeSheet: {dur: 0.3, apply: (s, _a, c) => ({...s, sheetP: 1 - c.p})},
  },
  anchors: () => ({screen: {x: 5.4, y: 5.4, w: W - 10.8, h: H - 10.8}}),
  Render,
};
