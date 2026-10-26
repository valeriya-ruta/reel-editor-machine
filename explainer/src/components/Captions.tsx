// Captions on top (top ~8–22% of the frame), Onest 800, dark, with the key
// word on a yellow marker. They pop in when their part starts and lift away
// when it ends. Kept clear of the bottom third.

import React from 'react';
import {clamp, outBack, prog} from '../engine/ease';
import type {CaptionEv} from '../engine/types';
import {C, FONT} from '../objects/style';

const IN = 0.38;
const OUT = 0.2;

const Marked: React.FC<{text: string}> = ({text}) => (
  <>
    {text.split(/(\*[^*]+\*)/g).map((seg, i) =>
      seg.startsWith('*') && seg.endsWith('*') ? (
        <em key={i} style={{fontStyle: 'normal', padding: '0 16px', borderRadius: 24, background: C.marker, boxDecorationBreak: 'clone', WebkitBoxDecorationBreak: 'clone', textShadow: 'none'}}>
          {seg.slice(1, -1)}
        </em>
      ) : (
        <React.Fragment key={i}>{seg}</React.Fragment>
      ),
    )}
  </>
);

export const Captions: React.FC<{captions: CaptionEv[]; t: number}> = ({captions, t}) => (
  <div style={{position: 'absolute', left: 0, right: 0, top: 158, height: 290, pointerEvents: 'none'}}>
    {captions.map((c, i) => {
      if (t < c.t0 || t > c.t1) return null;
      const pin = prog(t, c.t0 + 0.04, IN);
      const isLast = i === captions.length - 1;
      const pout = isLast ? 0 : prog(t, c.t1 - OUT, OUT);
      return (
        <div
          key={i}
          style={{
            position: 'absolute',
            left: 54,
            right: 54,
            top: 0,
            textAlign: 'center',
            fontFamily: FONT,
            fontWeight: 800,
            fontSize: 86,
            lineHeight: 1.12,
            letterSpacing: -1.8,
            color: C.ink,
            textWrap: 'balance',
            textShadow: '0 0 36px #fff, 0 0 12px #fff',
            opacity: clamp(pin * 2.5) * (1 - pout),
            transform: `translateY(${(1 - clamp(pin)) * 42 - pout * 36}px) scale(${0.92 + 0.08 * outBack(pin, 2)})`,
          }}
        >
          <Marked text={c.text} />
        </div>
      );
    })}
  </div>
);
