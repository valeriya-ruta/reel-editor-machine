// Shared by the CLI scripts: find an episode file from a loose id, and check it.

import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import type {EpisodeSpec} from '../src/engine/types';
import {validate, type Report} from '../src/engine/validate';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
export const EPISODES_DIR = path.join(ROOT, 'episodes');

/** `5`, `05`, `calls`, `05-calls`, `ep05-calls` or a path all find episodes/05-calls.json. */
export const findEpisode = (arg: string): string => {
  if (arg.endsWith('.json') && fs.existsSync(arg)) return path.resolve(arg);
  const files = fs.readdirSync(EPISODES_DIR).filter((f) => f.endsWith('.json') && !f.endsWith('.words.json'));
  const key = arg.replace(/^ep/, '');
  const num = /^\d+$/.test(key) ? key.padStart(2, '0') : null;
  const hit = files.find((f) => {
    const base = f.replace(/\.json$/, '');
    return base === key || (num !== null && base.startsWith(`${num}-`)) || base.endsWith(`-${key}`);
  });
  if (!hit) throw new Error(`no episode matches "${arg}" (have: ${files.join(', ')})`);
  return path.join(EPISODES_DIR, hit);
};

export const loadSpec = (file: string): EpisodeSpec => {
  const spec: EpisodeSpec = JSON.parse(fs.readFileSync(file, 'utf8'));
  // Mode B: merge the voiceover's word timings when they exist
  const words = file.replace(/\.json$/, '.words.json');
  if (spec.audio && fs.existsSync(words)) spec.words = JSON.parse(fs.readFileSync(words, 'utf8')).words;
  return spec;
};

export const check = (spec: EpisodeSpec): Report => validate(spec, (p) => fs.existsSync(path.join(ROOT, 'public', p)));

export const printReport = (name: string, r: Report) => {
  for (const w of r.warnings) console.log(`  warn  ${w}`);
  for (const e of r.errors) console.log(`  ERROR ${e}`);
  if (r.timeline) {
    const tl = r.timeline;
    console.log(`  ${name}: ${tl.duration.toFixed(1)}s, ${tl.frames} frames, ${tl.words} words, ${tl.shots.length} shots, mode ${tl.mode}`);
    for (const p of tl.parts) {
      console.log(`    step ${p.step + 1} ${p.kind.padEnd(6)} ${p.t0.toFixed(1).padStart(5)}–${p.t1.toFixed(1).padStart(5)}s  ${String(p.words).padStart(2)} words`);
    }
    const long = tl.shots.filter((s) => s.t1 - s.t0 > 1.6).length;
    if (long) console.log(`    ${long} shot(s) longer than 1.6s get automatic re-framings`);
  }
};
