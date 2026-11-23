// Easing and small math helpers. Every animation in the library is a pure
// function of time, so these take a 0..1 progress and return a 0..1 value.

export const clamp = (v: number, lo = 0, hi = 1) => Math.min(hi, Math.max(lo, v));
export const lerp = (a: number, b: number, p: number) => a + (b - a) * p;
export const prog = (t: number, t0: number, dur: number) => (dur <= 0 ? (t >= t0 ? 1 : 0) : clamp((t - t0) / dur));

export const linear = (p: number) => p;
export const inOut = (p: number) => (p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2);
export const inOutSine = (p: number) => -(Math.cos(Math.PI * p) - 1) / 2;
export const outCubic = (p: number) => 1 - Math.pow(1 - p, 3);
export const inCubic = (p: number) => p * p * p;
export const outQuart = (p: number) => 1 - Math.pow(1 - p, 4);
export const in4 = (p: number) => p * p * p * p;
export const outBack = (p: number, s = 1.9) => {
  const c3 = s + 1;
  return 1 + c3 * Math.pow(p - 1, 3) + s * Math.pow(p - 1, 2);
};

/** Damped spring settling from 0 to 1; `p` is seconds since start. Used for pops. */
export const spring = (sec: number, freq = 4.2, damp = 6.5) => {
  if (sec <= 0) return 0;
  return 1 - Math.exp(-damp * sec) * Math.cos(2 * Math.PI * freq * sec);
};

/** Deterministic noise for idle wobble, so every render of a frame is identical. */
export const wobble = (t: number, seed = 0) =>
  Math.sin(t * 1.7 + seed * 12.9898) * 0.6 + Math.sin(t * 2.9 + seed * 78.233) * 0.4;
