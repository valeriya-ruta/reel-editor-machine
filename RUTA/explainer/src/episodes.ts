// Every JSON in episodes/ becomes a composition. webpack resolves this
// require.context at bundle time, so a new episode is just a new file.

import type {EpisodeSpec} from './engine/types';

type Ctx = {keys(): string[]; (key: string): unknown};
type Req = {context: (dir: string, sub: boolean, re: RegExp) => Ctx};
const specs: Ctx = (require as unknown as Req).context('../episodes', false, /^\.\/\d+-[a-z-]+\.json$/);
const timings: Ctx = (require as unknown as Req).context('../episodes', false, /\.words\.json$/);

// Mode B: an episode with a voiceover gets its word timings from <name>.words.json
export const EPISODES: EpisodeSpec[] = specs
  .keys()
  .sort()
  .map((k) => {
    const spec = specs(k) as EpisodeSpec;
    const w = k.replace(/\.json$/, '.words.json');
    return spec.audio && timings.keys().includes(w) ? {...spec, words: (timings(w) as {words: EpisodeSpec['words']}).words} : spec;
  });
