// Spec → timeline. Mode A: no audio yet, so every part's length comes from its
// voiceover text at Ukrainian narration pace, beats split that time, shots are
// clamped to the doom-scroll range, and transitions eat into the start of each
// shot. The voiceover is a floor: when an episode runs long, gaps, holds and
// transitions shrink first and the narration time is never cut.

import {OBJECTS, verbFor} from '../objects/registry';
import {alignWords} from './align';
import type {ActionCall, Args, Beat, CaptionEv, EpisodeSpec, Ev, Part, PartTiming, Shot, ShotSpec, SubEv, Timeline} from './types';

export const FPS = 30;
export const RATE = 2.5; // words per second of Ukrainian narration
export const LIMIT = 58; // hard ceiling, seconds
export const TARGET: [number, number] = [40, 50];
export const SHOT_MIN = 0.8;
export const SHOT_MAX = 1.6; // longer beats get auto "breath" re-framings in the camera
const GAP = 0.12; // breath between parts
const END_HOLD = 0.7; // the last frame state, so it ends on the result

// Calm on purpose: every move eases over half a second or more (her note: the fast whips read as seizing).
export const VIA: Record<string, number> = {cut: 0, punch: 0.45, whip: 0.55, follow: 0.5, ease: 0.6, pull_back: 0.7};
export const PRESETS = ['room', 'screen', 'input_close', 'object_punch', 'character_close', 'phone_dive'] as const;

const WORD_RE = /[\p{L}\p{N}][\p{L}\p{N}'’ʼ-]*/gu;
export const countWords = (s: string) => (s.match(WORD_RE) ?? []).length;
const wordsOf = (s: string) => s.match(WORD_RE) ?? [];
const LEAD = 0.12; // a part (and its caption) starts just before its first word

// The voice reads product names phonetically; subtitles show them as written.
const SUB_MAP: [RegExp, string][] = [
  [/^Клод(а|у|і|ом)?$/i, 'Claude'],
  [/^Фатом$/i, 'Fathom'],
  [/^Баффер$/i, 'Buffer'],
  [/^Ноуше?н(і|а|у)?$/i, 'Notion'],
  [/^Канв(а|і|у|ою)$/i, 'Canva'],
  [/^Клікап(і|у|а)?$/i, 'ClickUp'],
];
const SUB_BREAK = /^[\s»"]*[,.!?:;—…]/;

const buildSubs = (spec: EpisodeSpec, parts: {part: Part}[], starts: number[], audioEnd: number): SubEv[] => {
  const map = spec.subtitleMap ?? {};
  const toks: {text: string; t: number; brk: boolean}[] = [];
  let k = 0;
  for (const {part} of parts) {
    for (const m of part.vo.matchAll(WORD_RE)) {
      const raw = m[0];
      const after = part.vo.slice((m.index ?? 0) + raw.length);
      let text = map[raw] ?? map[raw.toLowerCase()] ?? raw;
      for (const [re, rep] of SUB_MAP) if (re.test(text)) text = rep;
      const brk = SUB_BREAK.test(after) || after.trim() === '';
      if (text) toks.push({text, t: starts[k], brk});
      else if (brk && toks.length) toks[toks.length - 1].brk = true;
      k++;
    }
  }
  const subs: SubEv[] = [];
  let cur: {text: string; t: number}[] = [];
  const flush = () => {
    if (cur.length) subs.push({t0: cur[0].t - 0.05, t1: 0, words: cur});
    cur = [];
  };
  toks.forEach((w) => {
    const len = cur.reduce((a, x) => a + x.text.length + 1, 0) + w.text.length;
    // never leave a short word (в, з, і, на…) hanging at the end of a chunk
    const lastShort = cur.length > 0 && cur[cur.length - 1].text.length <= 2;
    if ((cur.length >= 3 || (cur.length && len > 18)) && !lastShort) flush();
    cur.push({text: w.text, t: w.t});
    if (w.brk) flush();
  });
  flush();
  subs.forEach((sb, i) => {
    const next = subs[i + 1]?.t0 ?? audioEnd;
    // hold to the next chunk, but don't linger over a long pause
    sb.t1 = Math.min(next, sb.words[sb.words.length - 1].t + 1.1);
  });
  return subs;
};

export type ParsedShot = {preset: string; target?: string; via: string; zoom: number; dx: number; dy: number};

const SHOT_RE = /^(?:([a-z_]+)>)?([a-z_]+)(?::([A-Za-z0-9_#-]+))?(?:\*([\d.]+))?$/;

export const parseShot = (spec: ShotSpec): ParsedShot | null => {
  if (typeof spec === 'string') {
    const m = SHOT_RE.exec(spec.trim());
    if (!m) return null;
    return {via: m[1] ?? 'ease', preset: m[2], target: m[3], zoom: m[4] ? Number(m[4]) : 1, dx: 0, dy: 0};
  }
  if (!spec || typeof spec.preset !== 'string') return null;
  return {preset: spec.preset, target: spec.target, via: spec.via ?? 'ease', zoom: spec.zoom ?? 1, dx: spec.dx ?? 0, dy: spec.dy ?? 0};
};

/** `<objectId>.<verb>` */
export const splitAction = (action: string): [string, string] => {
  const i = action.lastIndexOf('.');
  return i < 0 ? ['', action] : [action.slice(0, i), action.slice(i + 1)];
};

type FlatPart = {step: number; kind: 'action' | 'minus'; part: Part};

const flatten = (spec: EpisodeSpec): FlatPart[] =>
  spec.steps.flatMap((st, i) => {
    const out: FlatPart[] = [{step: i, kind: 'action', part: st}];
    if (st.minus) out.push({step: i, kind: 'minus', part: st.minus});
    return out;
  });

/** Seconds each beat of a part gets: its own words if it has `vo`, else a weighted share of what's left. */
const beatDurations = (part: Part, minBeat: number) => {
  const voSec = countWords(part.vo) / RATE;
  const own = part.beats.map((b) => (b.vo ? countWords(b.vo) / RATE : 0));
  const ownSum = own.reduce((a, b) => a + b, 0);
  const free = part.beats.map((b) => (b.vo ? 0 : (b.w ?? 1)));
  const freeSum = free.reduce((a, b) => a + b, 0);
  const left = Math.max(0, voSec - ownSum);
  let base = part.beats.map((_b, i) => own[i] + (freeSum > 0 ? (left * free[i]) / freeSum : 0));
  if (freeSum === 0 && ownSum > 0 && left > 0) base = base.map((d) => d * (voSec / ownSum));
  return {voSec, durs: base.map((d) => Math.max(minBeat, d))};
};

const resolveArgs = (spec: EpisodeSpec, args: Args | undefined): Args => {
  const a: Args = {...(args ?? {})};
  if (typeof a.to === 'string') {
    const target = spec.scene.objects.find((o) => o.id === a.to);
    if (target) {
      a.toX = target.x;
      a.toY = target.y;
    }
  }
  return a;
};

const eventFor = (spec: EpisodeSpec, call: ActionCall, t0: number): Ev | null => {
  const [id, verb] = splitAction(call.action);
  const obj = spec.scene.objects.find((o) => o.id === id);
  if (!obj) return null;
  const v = verbFor(obj.type, verb);
  if (!v) return null;
  const args = resolveArgs(spec, call.args);
  const dur = typeof args.dur === 'number' ? args.dur : typeof v.dur === 'function' ? v.dur(args, obj) : v.dur;
  return {obj: id, verb, args, t0: t0 + (call.at ?? 0), dur, impact: v.impact};
};

type Layout = {total: number; voTotal: number; durs: number[][]; vo: number[]};

const measure = (parts: FlatPart[], minBeat: number, gap: number): Layout => {
  let total = 0;
  let voTotal = 0;
  const durs: number[][] = [];
  const vo: number[] = [];
  for (const fp of parts) {
    const {voSec, durs: d} = beatDurations(fp.part, minBeat);
    durs.push(d);
    vo.push(voSec);
    voTotal += voSec;
    total += Math.max(voSec, d.reduce((a, b) => a + b, 0)) + gap;
  }
  return {total: total + END_HOLD, voTotal, durs, vo};
};

export const compile = (spec: EpisodeSpec): Timeline => {
  const warnings: string[] = [];
  const parts = flatten(spec);

  // Fit under the ceiling: first drop the gaps, then the minimum hold, then the transitions.
  let gap = GAP;
  let minBeat = SHOT_MIN;
  let transScale = 1;
  let lay = measure(parts, minBeat, gap);
  if (lay.total > LIMIT) {
    gap = 0;
    transScale = 0.7;
    lay = measure(parts, minBeat, gap);
    if (lay.total > LIMIT) {
      minBeat = 0.55;
      lay = measure(parts, minBeat, gap);
    }
    warnings.push(`over ${LIMIT}s: tightened gaps, holds and transitions (now ${lay.total.toFixed(1)}s; voiceover untouched)`);
  }

  // Mode B: every part starts on its first spoken word, beats share the part by weight
  let starts: number[] | null = null;
  let wordStarts: number[] = [];
  let audioEnd = 0;
  if (spec.audio && spec.words?.length) {
    const specWords = parts.flatMap((fp) => wordsOf(fp.part.vo));
    const {starts: ws, coverage} = alignWords(specWords, spec.words);
    wordStarts = ws;
    if (coverage < 0.8) warnings.push(`only ${Math.round(coverage * 100)}% of the script's words were found in the voiceover — check the text matches the audio`);
    starts = [];
    let k = 0;
    for (const fp of parts) {
      starts.push(starts.length === 0 ? 0 : Math.max(0, ws[k] - LEAD));
      k += wordsOf(fp.part.vo).length;
    }
    audioEnd = spec.words[spec.words.length - 1].e + 0.25;
    gap = 0;
    if (audioEnd + END_HOLD > LIMIT) warnings.push(`the voiceover is ${audioEnd.toFixed(1)}s — over the ${LIMIT}s ceiling`);
  }

  const events: Ev[] = [];
  const shots: Shot[] = [];
  const captions: CaptionEv[] = [];
  const timings: PartTiming[] = [];
  let t = 0;

  parts.forEach((fp, pi) => {
    const d = lay.durs[pi];
    const beatsSum = d.reduce((a, b) => a + b, 0);
    const isLast = pi === parts.length - 1;
    let stretch: number;
    if (starts) {
      // the part fills exactly the time until the next part's first word
      const end = isLast ? audioEnd : starts[pi + 1];
      t = starts[pi];
      stretch = Math.max(0.05, end - t) / beatsSum;
    } else {
      // a part never ends before its narration does
      stretch = lay.vo[pi] > beatsSum ? lay.vo[pi] / beatsSum : 1;
    }
    const t0 = t;
    let capText = fp.part.caption;
    let capStart = t0;
    fp.part.beats.forEach((b: Beat, bi) => {
      let dur = d[bi] * stretch;
      if (bi === fp.part.beats.length - 1) dur += isLast ? END_HOLD : gap;
      const bt0 = t;
      const bt1 = t + dur;
      const shot = parseShot(b.shot);
      if (shot) {
        const via = shots.length === 0 ? 'cut' : shot.via;
        const trans = Math.min((VIA[via] ?? VIA.ease) * transScale, dur * 0.7);
        shots.push({t0: bt0, t1: bt1, ...shot, via, transDur: trans});
      }
      if (b.caption && bi > 0) {
        captions.push({t0: capStart, t1: bt0, text: capText, kind: fp.kind});
        capText = b.caption;
        capStart = bt0;
      } else if (b.caption && bi === 0) {
        capText = b.caption;
      }
      for (const call of [b as ActionCall, ...(b.also ?? [])]) {
        const ev = eventFor(spec, call, bt0);
        if (ev) events.push(ev);
      }
      t = bt1;
    });
    captions.push({t0: capStart, t1: t, text: capText, kind: fp.kind});
    timings.push({step: fp.step, kind: fp.kind, t0, t1: t, voSec: lay.vo[pi], words: countWords(fp.part.vo)});
  });

  events.sort((a, b) => a.t0 - b.t0);
  const byObj: Record<string, Ev[]> = {};
  for (const ev of events) (byObj[ev.obj] ??= []).push(ev);

  const duration = t;
  const words = timings.reduce((a, p) => a + p.words, 0);
  if (!starts && (duration < TARGET[0] || duration > TARGET[1])) warnings.push(`estimated ${duration.toFixed(1)}s is outside the ${TARGET[0]}–${TARGET[1]}s target`);
  for (const o of spec.scene.objects) if (!OBJECTS[o.type]) warnings.push(`unknown object type "${o.type}"`);

  const subs = starts ? buildSubs(spec, parts, wordStarts, audioEnd) : [];
  return {fps: FPS, duration, frames: Math.ceil(duration * FPS), events, byObj, shots, captions, subs, parts: timings, words, mode: starts ? 'B' : 'A', warnings};
};
