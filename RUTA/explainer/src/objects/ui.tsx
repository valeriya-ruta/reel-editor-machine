// Small crisp-UI pieces shared by the laptop and the phone.

import React from 'react';
import {C, FONT} from './style';

export const Spark: React.FC<{size: number; color?: string; stroke?: number}> = ({size, color = C.terracotta, stroke = 3.2}) => (
  <svg width={size} height={size} viewBox="0 0 24 24" style={{display: 'block', flex: 'none'}}>
    <g stroke={color} strokeWidth={stroke} strokeLinecap="round">
      <path d="M12 2v20M2 12h20M4.9 4.9l14.2 14.2M19.1 4.9 4.9 19.1" />
    </g>
  </svg>
);

export const SendArrow: React.FC<{size: number}> = ({size}) => (
  <svg width={size} height={size} viewBox="0 0 10 10" style={{display: 'block'}}>
    <path d="M5 8.5V1.5M2 4.5 5 1.5l3 3" stroke="#fff" strokeWidth={1.6} fill="none" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

/** A blinking caret; `t` is seconds so it blinks the same in every render. */
export const Caret: React.FC<{t: number; h: number; w?: number; color?: string}> = ({t, h, w = 2, color = C.claudeText}) => (
  <span
    style={{
      display: 'inline-block',
      width: w,
      height: h,
      background: color,
      verticalAlign: -h * 0.15,
      marginLeft: 1,
      opacity: Math.floor(t * 2) % 2 === 0 ? 1 : 0,
    }}
  />
);

/** Grey placeholder lines that stand for text we don't need to read. */
export const Bars: React.FC<{widths: number[]; h: number; gap: number; color?: string; reveal?: number}> = ({
  widths,
  h,
  gap,
  color = '#E6E1D8',
  reveal = 1,
}) => (
  <div style={{display: 'flex', flexDirection: 'column', gap}}>
    {widths.map((w, i) => {
      const r = Math.min(1, Math.max(0, reveal * widths.length - i));
      return <div key={i} style={{height: h, width: `${w * r}%`, borderRadius: h / 2, background: color}} />;
    })}
  </div>
);

export const Dots: React.FC<{t: number; size: number; color?: string}> = ({t, size, color = '#C9C3BA'}) => (
  <div style={{display: 'flex', gap: size * 0.6}}>
    {[0, 1, 2].map((i) => (
      <i
        key={i}
        style={{
          display: 'block',
          width: size,
          height: size,
          borderRadius: '50%',
          background: color,
          transform: `translateY(${-Math.max(0, Math.sin((t * 6 - i * 0.7) % (Math.PI * 2))) * size * 0.6}px)`,
        }}
      />
    ))}
  </div>
);

export const uiText: React.CSSProperties = {fontFamily: FONT, color: C.claudeText};
