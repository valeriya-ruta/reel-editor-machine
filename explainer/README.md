# explainer — "AI evolution" reels

Short vertical explainers (Ukrainian, 1080×1920, 30 fps, 40–50 s, never over
58 s). Each episode is an evolution ladder for one creator task: you do X → but
Y → so you do the next thing, ending on the modern AI setup. Remotion project,
separate from the HyperFrames reel pipeline in the repo root.

The brief is [`explainer-series-prompt.md`](explainer-series-prompt.md); the
approved GSAP prototype it was rebuilt from is
[`reference/prompt-to-skill.html`](reference/prompt-to-skill.html).

```bash
npm install
npm run validate            # check every episode (or: npm run validate -- 5)
npm run episode -- 5        # validate + render out/ep05-calls.mp4 (H.264)
npm run stills -- 5         # contact sheet of frames → out/ep05-calls-sheet.jpg
npm run studio              # preview every episode + the object "library"
```

`episode`, `validate` and `stills` take `5`, `05`, `calls`, `05-calls` or a path.

## A new episode is a new JSON file

`episodes/NN-slug.json`, nothing else. It declares a **scene** (objects placed
in world coordinates; the desk line is y = 1300) and **steps**:

```jsonc
{
  "caption": "Пишеш *нотатки* під час дзвінка",   // *key word* gets the yellow marker
  "vo": "Тоді пишеш нотатки прямо під час розмови.",
  "beats": [
    {"action": "notepad.show", "shot": "whip>object_punch:notepad",
      "also": [{"action": "notepad.scribble", "at": 0.2}]},
    {"action": "ruta.pose", "args": {"pose": "scribbling"}, "shot": "whip>character_close"}
  ],
  "minus": { "caption": "...", "vo": "...", "beats": [ ... ] }   // every step but the last
}
```

- **action** is `<objectId>.<verb>`. Every object understands `show`, `hide`,
  `move`, `fly`, `scale`, `tilt`, `shake`, `pulse`; types add their own (below).
  `also` runs more actions in the same beat, `at` seconds after it starts.
- **shot** is `[transition>]preset[:target][*zoom]`. Presets: `room` (target =
  a named rect in `scene.rooms`), `screen`, `input_close`, `object_punch`
  (target = object id, or `id#part` like `laptop#rec`), `character_close`,
  `phone_dive`. Transitions: `whip` (fast, motion blur), `pull_back`, `punch`,
  `follow` (tracks the target live, e.g. a plug travelling along a cable),
  `cut`, and the default ease.
- A beat may carry its own `caption` to swap the caption mid-part, its own `vo`
  fragment, or a weight `w` for its share of the part's narration time.

The validator rejects unknown objects, actions, shots and parts, missing
fields, pose art that doesn't exist, a minus on the last step, and anything
estimated over 58 s; it warns outside 95–115 words or 40–50 s.

## Timing

**Mode A** (now, no audio): a part lasts as long as its `vo` takes at 2.5
Ukrainian words a second; beats split that time (min 0.8 s each); transitions
eat into the start of a shot. The camera never holds a framing much past 1.5 s:
holds drift in, and longer ones get an automatic punch-in. Over 58 s, gaps,
holds and transitions shrink first and the voiceover is never cut, with a
warning.

**Mode B** (next, once there's a voiceover): `audio.mp3` + word timestamps
(ElevenLabs "with timestamps" or Whisper) pin each part and caption to its
spoken words.

## Objects (`src/objects/`)

| type | verbs |
|---|---|
| `laptop` | `window` (claude · call · player · render), `type`, `select`, `clear`, `send`, `ask`, `reply`, `newchat`, `call`, `speak`, `face`, `rec`, `hangup`, `scrub`, `render`, `overheat`, `cool` — parts: `screen` `window` `input` `caret` `chat` `rec` `tiles` `client` `me` `timeline` |
| `phone` | `screen` (claude · camera · feed), `record`, `post`, `swipe`, `type`, `tap`, `send`, `reply`, `sheet`, `closeSheet` |
| `chibi` | `pose` — squash-and-stretch on change, idle bob, shakes when furious/panicked |
| `paper` | `fold`, `unfold` (+ generic `fly`) — a prompt note, a doc via `title`/`bars`, a report via `items` (`+ …` ✓, `- …` ✗), or a `blank` page |
| `folder` | `open`, `close`, `gulp`, `empty` |
| `skill` | `stamp` (the «/» slam, with camera micro-shake) |
| `notepad` | `scribble`, `lose` (question stickies fly off) |
| `chips` | `pop`, `forget` (blur away into "?") |
| `app` | — a glossy app tile with a label: `fathom`, `claude`, `clickup`, `canva`, `instagram`, `notes`, or `glyph` (`person`, `scissors`, `sparkle`, `chart`) on a `bg` colour |
| `cable` | `plug`, `unplug` between two objects |
| `tasks` | `add`, `type` (slow, by hand), `check` |
| `reels` | `fill`, `scroll`, `mark` (star · q · x · check), `dim` — part: `grid` |
| `sheet` | `fill`, `blur` — part: `grid` |
| `calendar` | `flip` (weeks pass; `mark` Mondays done/miss) |
| `slides` | `build`, `text`, `style` (blank · template · ugly · mine), `shuffle` — part: `front` |
| `dscard` | — the design-system card |
| `notespile` | `grow`, `bury` (the notes graveyard) |
| `timeline` | `cut` (pauses close up), `subs`, `flag` (repeated takes) — part: `tracks` |
| `clock` | `spin` (hours) |
| `price` | — a swinging price tag |
| `cloud` | `upload`, `done` |

Numbers on screen are shape-only (bars, not view counts), per STYLE.md's
"no invented stats". A new object is one `ObjectDef` in `src/objects/`,
registered in `registry.ts`; the `library` and `library-2` compositions show
every object in Studio.

## Chibi Ruta

She's an actor, never a speaker. Poses live in `public/chibi/<pose>.png`
(transparent, head-top to knees, same canvas so they swap in place). Reuse
before generating. To add one: build the prompt from
[`chibi/chibi-ruta-prompt.md`](chibi/chibi-ruta-prompt.md) (FORMAT + STYLE +
CHARACTER word for word, only POSE changes), generate with OpenRouter
`google/gemini-3.1-flash-image` at 2K, check it against the kit's rule 5
(green eyes, two separate hoops per lobe, no other piercings — the model often
adds a helix ring, regenerate), then:

```bash
python scripts/cutout.py <raw.png> public/chibi/<pose>.png
```

Have: neutral, confused, scribbling, panicked, exhausted, furious, ecstatic,
coffee, phone, frustrated, thinking, waterworks, smug, sad, bored. (Shocked
failed the piercing check twice; panicked covers those beats.)

## Layout

| path | what |
|---|---|
| `episodes/` | one spec per episode |
| `src/engine/` | spec types, Mode A compiler, camera, validator, world state |
| `src/objects/` | the object library (`registry.ts` lists every type) |
| `src/components/` | episode stage, captions, fonts, the library sheet |
| `scripts/` | `episode` (render), `validate`, `stills`, `cutout.py` |
| `public/` | fonts (Onest, Lora), chibi poses, app logos |
