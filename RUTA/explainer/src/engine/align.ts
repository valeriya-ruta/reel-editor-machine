// Mode B: pin the spec's words to the voiceover's word timings. The spelling
// comes from the spec, the timing from Whisper; the two are matched letter by
// letter (longest common subsequence), so ASR spelling slips, split words and
// numbers written as digits don't throw the alignment off.

import type {SpokenWord} from './types';

const letters = (s: string) => s.toLowerCase().replace(/[^\p{L}]/gu, '');

/** Start time of each spec word, in order. Words the ASR missed are interpolated. */
export const alignWords = (specWords: string[], spoken: SpokenWord[]): {starts: number[]; coverage: number} => {
  // spec letters, remembering which word each letter belongs to
  let a = '';
  const aWord: number[] = [];
  specWords.forEach((w, i) => {
    const l = letters(w);
    a += l;
    for (let k = 0; k < l.length; k++) aWord.push(i);
  });
  // spoken letters with a time each, spread evenly across their word
  let b = '';
  const bTime: number[] = [];
  for (const sw of spoken) {
    const l = letters(sw.w);
    b += l;
    for (let k = 0; k < l.length; k++) bTime.push(sw.s + ((sw.e - sw.s) * k) / Math.max(1, l.length));
  }
  const n = a.length;
  const m = b.length;
  const dp = new Uint16Array((n + 1) * (m + 1));
  const at = (i: number, j: number) => i * (m + 1) + j;
  for (let i = n - 1; i >= 0; i--) {
    for (let j = m - 1; j >= 0; j--) {
      dp[at(i, j)] = a[i] === b[j] ? dp[at(i + 1, j + 1)] + 1 : Math.max(dp[at(i + 1, j)], dp[at(i, j + 1)]);
    }
  }
  const charTime: (number | null)[] = new Array(n).fill(null);
  for (let i = 0, j = 0; i < n && j < m; ) {
    if (a[i] === b[j]) {
      charTime[i] = bTime[j];
      i++;
      j++;
    } else if (dp[at(i + 1, j)] >= dp[at(i, j + 1)]) i++;
    else j++;
  }
  const starts: (number | null)[] = specWords.map(() => null);
  let hit = 0;
  for (let c = 0; c < n; c++) {
    const w = aWord[c];
    if (starts[w] === null && charTime[c] !== null) {
      // the first matched letter of the word, nudged back to the word's start
      starts[w] = charTime[c];
      hit++;
    }
  }
  // fill the gaps by interpolating between known neighbours
  const end = spoken.length ? spoken[spoken.length - 1].e : 0;
  const out = starts.slice();
  for (let i = 0; i < out.length; i++) {
    if (out[i] !== null) continue;
    let p = i - 1;
    while (p >= 0 && starts[p] === null) p--;
    let q = i + 1;
    while (q < out.length && starts[q] === null) q++;
    const t0 = p >= 0 ? (starts[p] as number) : 0;
    const t1 = q < out.length ? (starts[q] as number) : end;
    out[i] = t0 + ((t1 - t0) * (i - p)) / (q - p);
  }
  return {starts: out as number[], coverage: specWords.length ? hit / specWords.length : 0};
};
