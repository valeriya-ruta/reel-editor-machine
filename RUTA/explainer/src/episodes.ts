// Every JSON in episodes/ becomes a composition. webpack resolves this
// require.context at bundle time, so a new episode is just a new file.

import type {EpisodeSpec} from './engine/types';

type Ctx = {keys(): string[]; (key: string): unknown};
const ctx: Ctx = (require as unknown as {context: (dir: string, sub: boolean, re: RegExp) => Ctx}).context('../episodes', false, /\.json$/);

export const EPISODES: EpisodeSpec[] = ctx
  .keys()
  .sort()
  .map((k) => ctx(k) as EpisodeSpec);
