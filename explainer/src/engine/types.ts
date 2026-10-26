// The episode spec (what a JSON file in episodes/ holds) and the compiled
// timeline the renderer plays. Everything time-based is in seconds until the
// component turns it into frames.

export type Args = Record<string, unknown>;

/** A shot is `[via>]preset[:target][*zoom]`, e.g. `whip>object_punch:notepad`,
 *  or the same thing spelled out as an object. */
export type ShotSpec =
  | string
  | {preset: string; target?: string; via?: string; zoom?: number; dx?: number; dy?: number};

/** `action` is `<objectId>.<verb>`, e.g. `laptop.type`, `ruta.pose`. */
export type ActionCall = {action: string; args?: Args; at?: number};

export type Beat = ActionCall & {
  shot: ShotSpec;
  /** The words this beat sits under. Mode A times it from them; Mode B aligns to them. */
  vo?: string;
  /** Share of the part's leftover narration time when the beat has no `vo`. */
  w?: number;
  /** Swap the caption from this beat on (key word marked with *stars*). */
  caption?: string;
  /** Actions that run alongside the main one; `at` is seconds after the beat starts. */
  also?: ActionCall[];
};

export type Part = {caption: string; vo: string; beats: Beat[]};
export type Step = Part & {minus?: Part};

export type SceneObject = {
  id: string;
  type: string;
  x: number;
  y: number;
  scale?: number;
  rot?: number;
  /** back = behind the desk (her), desk = on it, air = floating metaphor objects. */
  layer?: 'back' | 'desk' | 'air';
  hidden?: boolean;
  props?: Args;
};

export type Rect = [x0: number, y0: number, x1: number, y1: number];

export type EpisodeSpec = {
  id: string;
  title: string;
  /** TODO-TOV until Ruta rewrites captions and VO in her voice. */
  status?: string;
  scene: {
    /** Named framings for the `room` preset; `default` is used when no target is given. */
    rooms: Record<string, Rect>;
    /** World y of the desk line; her pose PNGs are cut off below it. Default 1300. */
    floorY?: number;
    objects: SceneObject[];
  };
  steps: Step[];
};

// ---- compiled ----

export type Ev = {obj: string; verb: string; args: Args; t0: number; dur: number; impact?: boolean};

export type Shot = {
  t0: number;
  t1: number;
  preset: string;
  target?: string;
  via: string;
  zoom: number;
  dx: number;
  dy: number;
  transDur: number;
};

export type CaptionEv = {t0: number; t1: number; text: string; kind: 'action' | 'minus'};

export type PartTiming = {step: number; kind: 'action' | 'minus'; t0: number; t1: number; voSec: number; words: number};

export type Timeline = {
  fps: number;
  duration: number;
  frames: number;
  events: Ev[];
  byObj: Record<string, Ev[]>;
  shots: Shot[];
  captions: CaptionEv[];
  parts: PartTiming[];
  words: number;
  warnings: string[];
};
