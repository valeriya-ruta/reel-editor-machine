// npm run stills -- <episode> [--every 0.5] [--at 1.2,3.4]
// Renders frames from one bundle into out/<id>-stills/ and tiles them into a
// contact sheet, for reviewing framing and pacing without a full render.

import {execFileSync} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import {compile} from '../src/engine/compile';
import {findEpisode, loadSpec, ROOT} from './lib';

const args = process.argv.slice(2);
const flag = (name: string) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 ? args[i + 1] : undefined;
};
const id = args[0];

const browser = () => {
  if (process.env.REMOTION_BROWSER) return process.env.REMOTION_BROWSER;
  const bin = '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell';
  return fs.existsSync(bin) ? bin : undefined;
};

const main = async () => {
  const spec = loadSpec(findEpisode(id));
  const tl = compile(spec);
  const times = flag('at')
    ? flag('at')!.split(',').map(Number)
    : Array.from({length: Math.floor(tl.duration / Number(flag('every') ?? 1))}, (_, i) => i * Number(flag('every') ?? 1));
  const dir = path.join(ROOT, 'out', `${spec.id}-stills`);
  fs.rmSync(dir, {recursive: true, force: true});
  fs.mkdirSync(dir, {recursive: true});
  const serveUrl = await bundle({entryPoint: path.join(ROOT, 'src', 'index.ts'), publicDir: path.join(ROOT, 'public')});
  const browserExecutable = browser();
  const composition = await selectComposition({serveUrl, id: spec.id, inputProps: {spec}, browserExecutable});
  for (const [i, t] of times.entries()) {
    const frame = Math.min(tl.frames - 1, Math.round(t * tl.fps));
    await renderStill({serveUrl, composition, frame, inputProps: {spec}, output: path.join(dir, `${String(i).padStart(3, '0')}.jpg`), imageFormat: 'jpeg', jpegQuality: 80, scale: 0.25, browserExecutable});
    process.stdout.write(`\r  ${i + 1}/${times.length}`);
  }
  const cols = 8;
  const rows = Math.ceil(times.length / cols);
  const sheet = path.join(ROOT, 'out', `${spec.id}-sheet.jpg`);
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-i', path.join(dir, '%03d.jpg'), '-vf', `tile=${cols}x${rows}:padding=6:color=white`, '-frames:v', '1', sheet]);
  console.log(`\n  → ${path.relative(process.cwd(), sheet)}`);
};

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
