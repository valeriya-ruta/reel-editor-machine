// npm run validate [-- <episode>]   — check one episode, or all of them.

import fs from 'node:fs';
import path from 'node:path';
import {check, EPISODES_DIR, findEpisode, loadSpec, printReport} from './lib';

const arg = process.argv[2];
const files = arg ? [findEpisode(arg)] : fs.readdirSync(EPISODES_DIR).filter((f) => f.endsWith('.json')).map((f) => path.join(EPISODES_DIR, f));

let failed = false;
for (const file of files) {
  const name = path.basename(file);
  console.log(name);
  let report;
  try {
    report = check(loadSpec(file));
  } catch (e) {
    console.log(`  ERROR ${(e as Error).message}`);
    failed = true;
    continue;
  }
  printReport(name, report);
  if (report.errors.length) failed = true;
}
process.exit(failed ? 1 : 0);
