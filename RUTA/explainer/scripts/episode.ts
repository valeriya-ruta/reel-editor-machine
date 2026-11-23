// npm run episode -- <id> [--out file.mp4] [--frames 0-90]
// Validates the spec, then renders it to out/<id>.mp4 as H.264.

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';
import {check, findEpisode, loadSpec, printReport, ROOT} from './lib';

const args = process.argv.slice(2);
const flag = (name: string) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 ? args[i + 1] : undefined;
};
const id = args.find((a, i) => !a.startsWith('--') && !(i > 0 && ['--out', '--frames'].includes(args[i - 1])));
if (!id) {
  console.error('usage: npm run episode -- <episode> [--out file.mp4] [--frames 0-90] [--preview]');
  process.exit(1);
}

/** A local Chrome to use instead of letting Remotion download one (cloud sandboxes). */
const browser = (): string | undefined => {
  if (process.env.REMOTION_BROWSER) return process.env.REMOTION_BROWSER;
  const pw = '/opt/pw-browsers';
  if (!fs.existsSync(pw)) return undefined;
  for (const d of fs.readdirSync(pw).filter((n) => n.startsWith('chromium_headless_shell'))) {
    const bin = path.join(pw, d, 'chrome-headless-shell-linux64', 'chrome-headless-shell');
    if (fs.existsSync(bin)) return bin;
  }
  return undefined;
};

const preview = args.includes('--preview');

const main = async () => {
  const file = findEpisode(id);
  const spec = loadSpec(file);
  const report = check(spec);
  printReport(path.basename(file), report);
  if (report.errors.length) process.exit(1);

  const out = path.resolve(flag('out') ?? path.join(ROOT, 'out', `${spec.id}${preview ? '-preview' : ''}.mp4`));
  fs.mkdirSync(path.dirname(out), {recursive: true});
  const range = flag('frames')?.split('-').map(Number) as [number, number] | undefined;

  console.log('bundling…');
  const serveUrl = await bundle({entryPoint: path.join(ROOT, 'src', 'index.ts'), publicDir: path.join(ROOT, 'public')});
  const browserExecutable = browser();
  const composition = await selectComposition({serveUrl, id: spec.id, inputProps: {spec}, browserExecutable});
  let last = -1;
  await renderMedia({
    serveUrl,
    composition,
    inputProps: {spec},
    codec: 'h264',
    crf: preview ? 23 : 18,
    scale: preview ? 0.5 : 1,
    pixelFormat: 'yuv420p',
    colorSpace: 'bt709',
    imageFormat: 'jpeg',
    jpegQuality: 92,
    outputLocation: out,
    browserExecutable,
    concurrency: Math.max(1, os.cpus().length),
    frameRange: range,
    onProgress: ({progress}) => {
      const pct = Math.floor(progress * 20) * 5;
      if (pct !== last) {
        last = pct;
        process.stdout.write(`\r  rendering ${pct}%`);
      }
    },
  });
  console.log(`\n  → ${path.relative(process.cwd(), out)}`);
};

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
