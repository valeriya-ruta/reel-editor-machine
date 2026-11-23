// Onest for captions and UI, Lora for Claude's serif greeting. Both ship in
// public/fonts so a render never depends on Google Fonts being reachable.

import {continueRender, delayRender, staticFile} from 'remotion';

let loading: Promise<void> | null = null;

const load = () =>
  Promise.all(
    [
      ['Onest', 'fonts/Onest.ttf'],
      ['Lora', 'fonts/Lora.ttf'],
    ].map(async ([family, file]) => {
      const face = new FontFace(family, `url(${staticFile(file)})`, {weight: '100 900'});
      await face.load();
      document.fonts.add(face);
    }),
  ).then(() => undefined);

export const useFonts = () => {
  if (loading) return;
  const handle = delayRender('Loading fonts');
  loading = load()
    .then(() => continueRender(handle))
    .catch((e) => {
      console.error(e);
      continueRender(handle);
    });
};
