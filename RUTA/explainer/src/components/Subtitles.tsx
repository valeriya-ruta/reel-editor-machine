// Word-by-word subtitles: 1–3 words on one line, on a white pill just above
// the bottom third (clear of Instagram's caption and buttons), the word being
// spoken on the yellow marker. At ~70% of the frame: below her face in close-ups.

import React from 'react';
import {clamp, outBack, prog} from '../engine/ease';
import type {SubEv} from '../engine/types';
import {C, FONT} from '../objects/style';

export const SUB_Y = 1340;

export const Subtitles: React.FC<{subs: SubEv[]; t: number}> = ({subs, t}) => {
  const sb = subs.find((x) => t >= x.t0 && t < x.t1);
  if (!sb) return null;
  const pin = prog(t, sb.t0, 0.16);
  return (
    <div style={{position: 'absolute', left: 0, right: 0, top: SUB_Y, display: 'flex', justifyContent: 'center', pointerEvents: 'none'}}>
      <div
        style={{
          display: 'flex',
          gap: 14,
          alignItems: 'center',
          whiteSpace: 'nowrap',
          padding: '14px 26px',
          borderRadius: 30,
          background: 'rgba(255,255,255,.96)',
          boxShadow: '0 10px 30px rgba(20,22,30,.16)',
          fontFamily: FONT,
          fontWeight: 800,
          fontSize: 70,
          lineHeight: 1.1,
          letterSpacing: -1.2,
          color: C.ink,
          opacity: clamp(pin * 3),
          transform: `translateY(-50%) scale(${0.9 + 0.1 * outBack(pin, 1.6)})`,
        }}
      >
        {sb.words.map((w, i) => {
          const next = sb.words[i + 1]?.t ?? sb.t1;
          const active = t >= w.t && t < next;
          return (
            <span key={i} style={{padding: '0 10px', borderRadius: 16, background: active ? C.marker : 'transparent'}}>
              {w.text}
            </span>
          );
        })}
      </div>
    </div>
  );
};
