// Catch a broken spec before it renders: unknown objects, actions and shots,
// missing fields, missing pose art, and an episode that will run too long.

import {OBJECTS, verbFor, verbsOf} from '../objects/registry';
import {compile, countWords, LIMIT, parseShot, PRESETS, splitAction, VIA} from './compile';
import type {ActionCall, EpisodeSpec, Part, Timeline} from './types';
import {initialState} from './world';

export type Report = {errors: string[]; warnings: string[]; timeline?: Timeline};

const KEYWORD = /\*[^*]+\*/;

export const validate = (spec: EpisodeSpec, assetExists?: (path: string) => boolean): Report => {
  const errors: string[] = [];
  const warnings: string[] = [];
  const err = (m: string) => errors.push(m);
  const warn = (m: string) => warnings.push(m);

  if (!spec || typeof spec !== 'object') return {errors: ['spec is not an object'], warnings};
  if (typeof spec.id !== 'string' || !/^[a-z0-9-]+$/.test(spec.id)) err(`id must be lowercase letters, digits and dashes (got ${JSON.stringify(spec.id)})`);
  if (typeof spec.title !== 'string' || !spec.title) err('missing title');
  if (spec.status === 'TODO-TOV') warn('captions and VO are placeholders (TODO-TOV) until Ruta rewrites them');

  const objs = spec.scene?.objects;
  if (!Array.isArray(objs) || objs.length === 0) {
    err('scene.objects is missing or empty');
    return {errors, warnings};
  }
  if (!spec.scene.rooms?.default) err('scene.rooms.default is missing (the room preset needs it)');
  const byId = new Map<string, (typeof objs)[number]>();
  for (const o of objs) {
    if (!o.id) err('an object has no id');
    else if (byId.has(o.id)) err(`duplicate object id "${o.id}"`);
    byId.set(o.id, o);
    if (!OBJECTS[o.type]) err(`object "${o.id}": unknown type "${o.type}" (have: ${Object.keys(OBJECTS).join(', ')})`);
    if (typeof o.x !== 'number' || typeof o.y !== 'number') err(`object "${o.id}": x and y must be numbers`);
    if (o.type === 'cable') {
      for (const end of ['from', 'to']) {
        const ref = o.props?.[end];
        if (typeof ref !== 'string' || !byId.has(ref)) {
          if (!objs.some((x) => x.id === ref)) err(`cable "${o.id}": props.${end} must name another object`);
        }
      }
    }
    for (const a of OBJECTS[o.type]?.assets?.(o) ?? []) {
      if (assetExists && !assetExists(a)) err(`object "${o.id}": missing public/${a}`);
    }
  }

  const checkCall = (call: ActionCall, where: string) => {
    if (typeof call.action !== 'string' || !call.action) return err(`${where}: missing action`);
    const [id, verb] = splitAction(call.action);
    const o = byId.get(id);
    if (!o) return err(`${where}: unknown action "${call.action}" — no object "${id}"`);
    const v = verbFor(o.type, verb);
    if (!v) return err(`${where}: unknown action "${call.action}" — a ${o.type} can: ${verbsOf(o.type).join(', ')}`);
    const args = call.args ?? {};
    for (const r of v.required ?? []) if (args[r] === undefined) err(`${where}: ${call.action} needs args.${r}`);
    const extra = v.check?.(args, o);
    if (extra) err(`${where}: ${call.action}: ${extra}`);
    if (typeof args.to === 'string' && !byId.has(args.to)) err(`${where}: ${call.action}: args.to "${args.to}" is not an object`);
    if (o.type === 'chibi' && verb === 'pose' && typeof args.pose === 'string' && assetExists && !assetExists(`chibi/${args.pose}.png`)) {
      err(`${where}: pose "${args.pose}" has no art — generate public/chibi/${args.pose}.png with the chibi kit`);
    }
    if (call.at !== undefined && (typeof call.at !== 'number' || call.at < 0)) err(`${where}: "at" must be seconds ≥ 0`);
  };

  const checkPart = (part: Part | undefined, where: string) => {
    if (!part) return err(`${where}: missing`);
    if (typeof part.caption !== 'string' || !part.caption.trim()) err(`${where}: missing caption`);
    else if (!KEYWORD.test(part.caption) && !part.beats?.some((b) => b.caption)) warn(`${where}: caption has no *key word* for the marker`);
    if (typeof part.vo !== 'string' || !part.vo.trim()) err(`${where}: missing vo`);
    if (!Array.isArray(part.beats) || part.beats.length === 0) return err(`${where}: needs at least one beat`);
    part.beats.forEach((b, bi) => {
      const bw = `${where} beat ${bi + 1}`;
      checkCall(b, bw);
      (b.also ?? []).forEach((c, ci) => checkCall(c, `${bw} also[${ci}]`));
      if (b.shot === undefined) return err(`${bw}: missing shot`);
      const s = parseShot(b.shot);
      if (!s) return err(`${bw}: can't read shot ${JSON.stringify(b.shot)} (use "via>preset:target", e.g. "whip>object_punch:notepad")`);
      if (!(PRESETS as readonly string[]).includes(s.preset)) err(`${bw}: unknown shot preset "${s.preset}" (have: ${PRESETS.join(', ')})`);
      if (VIA[s.via] === undefined) err(`${bw}: unknown transition "${s.via}" (have: ${Object.keys(VIA).join(', ')})`);
      if (s.preset === 'object_punch' && !s.target) err(`${bw}: object_punch needs a target`);
      if (s.target && s.preset !== 'room') {
        const [tid, anchor] = s.target.split('#');
        const o = byId.get(tid);
        if (!o) err(`${bw}: shot target "${tid}" is not an object`);
        else if (anchor) {
          const anchors = OBJECTS[o.type]?.anchors?.(o, initialState(o)) ?? {};
          if (!anchors[anchor]) err(`${bw}: ${o.type} "${tid}" has no part "#${anchor}" (have: ${Object.keys(anchors).join(', ') || 'none'})`);
        }
      }
      if (s.preset === 'room' && s.target && !spec.scene.rooms?.[s.target]) err(`${bw}: no room "${s.target}" in scene.rooms`);
      if (b.caption !== undefined && (typeof b.caption !== 'string' || !b.caption.trim())) err(`${bw}: caption must be text`);
    });
  };

  if (!Array.isArray(spec.steps) || spec.steps.length === 0) {
    err('no steps');
    return {errors, warnings};
  }
  if (spec.steps.length < 5 || spec.steps.length > 6) warn(`${spec.steps.length} steps — the format is 5–6`);
  spec.steps.forEach((st, i) => {
    checkPart(st, `step ${i + 1}`);
    if (st.minus) checkPart(st.minus, `step ${i + 1} minus`);
    const words = countWords(st.vo ?? '') + countWords(st.minus?.vo ?? '');
    if (words > 26) warn(`step ${i + 1}: ${words} words of VO — keep a step to one or two short sentences (~15–20 words)`);
  });
  const last = spec.steps[spec.steps.length - 1];
  if (last?.minus) err('the last step is the modern setup — it has no minus');

  if (errors.length) return {errors, warnings};

  const tl = compile(spec);
  warnings.push(...tl.warnings);
  if (tl.words < 95 || tl.words > 115) warn(`${tl.words} words of VO — aim for 95–115`);
  if (tl.duration > LIMIT) err(`estimated ${tl.duration.toFixed(1)}s — over the ${LIMIT}s ceiling even after tightening; cut voiceover words`);
  return {errors, warnings, timeline: tl};
};
