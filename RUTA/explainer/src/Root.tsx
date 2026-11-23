import React from 'react';
import {Composition} from 'remotion';
import {Episode} from './components/Episode';
import {FRAME_H, FRAME_W} from './engine/camera';
import {compile, FPS} from './engine/compile';
import {EPISODES} from './episodes';
import {Library, Library2} from './components/Library';

export const Root: React.FC = () => (
  <>
    {EPISODES.map((spec) => (
      <Composition
        key={spec.id}
        id={spec.id}
        component={Episode}
        durationInFrames={compile(spec).frames}
        fps={FPS}
        width={FRAME_W}
        height={FRAME_H}
        defaultProps={{spec}}
      />
    ))}
    <Composition id="library" component={Library} durationInFrames={90} fps={FPS} width={FRAME_W} height={FRAME_H} />
    <Composition id="library-2" component={Library2} durationInFrames={90} fps={FPS} width={FRAME_W} height={FRAME_H} />
  </>
);
