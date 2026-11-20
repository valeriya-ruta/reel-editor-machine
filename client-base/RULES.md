# Reel editing base — the rules

**BASE LAYER: the same for every client, and it has no design in it.** This
file is the STYLE.md of Ruta's Marina editor (latest version, 2026-11-17),
which started as Ruta's own STYLE.md from `reel-editor-machine`, with every
design choice taken out: no fonts, no colours, no type sizes, no stroke
weights, no element styling, no motion style, no rhythm numbers. What is left
is how a reel is cut, captioned, placed, checked, rendered and delivered.

Every rule here is copied from Ruta's repo or from what Ruta said while
building Marina's editor (2026-11-05 and 2026-11-17). **Nothing here is
invented, and nothing here changes per client.** The quotes are Ruta's.

The client's look lives in `LOOK.md` + `tools/look.py` + `assets/fonts/`:
palette, fonts, caption style and size, type tiers, materials (how each real
element is drawn), stroke weights, motion style, timing lead, rhythm, and
where her own refs put things. `LOOK.md` decides only those things. It never
loosens a rule in this file.

**Anything not settled is asked, not decided** (Ruta's 17 Nov file, confirmed
by Ruta 2026-11-20). What these two files, the transcript and the refs settle,
the run decides and writes into `reel-NN/PLAN.md`. What they don't settle (a
call no rule covers, a missing real asset, a bad take that may be content),
it asks Ruta instead of guessing.

**Transcription:** local whisper (`tools/utt.py`), OpenRouter whisper as the
fallback. **Never ElevenLabs**, and not the video-use skill.

Section numbers match the client's `LOOK.md`.

---

## 1. The delivery model and the cut

Ruta drops the client's **raw take** into `raw/`. This folder cuts it, captions
it, animates it and renders it, with Ruta's raw-take pipeline from
`reel-editor-machine` (reels 21–40): `tools/utt.py` → `tools/cut.py` →
`tools/gapcheck.py` → `tools/align.py` → `build.py` → checks → render →
verify.

**Cutting rule (Ruta, 2026-11-05):** the reel stays **under 3 minutes**. Cut
**only pauses and bad takes**, following Ruta's instructions and the
transcript. **Never cut content.** No length targets. If pauses and bad takes
alone leave it over 3:00, say so with the numbers and let Ruta name the
content cuts (recorded in `work/rNN/cut-fix.json`).

How the cut finds them (Ruta's `tools/cut.py`, plus the voice guard):

- **Pauses — from the audio and from the transcript** (Ruta, 2026-11-05:
  "both audio and transcript, because if there's wind there might not
  necessarily be actual audio silence"). `tools/utt.py` runs ffmpeg
  `silencedetect` (−30 dB, 0.18 s) and transcribes each spoken span on its
  own. Inside a span, `cut.py` also splits wherever the transcript shows a gap
  between two words longer than 0.30 s, so a pause full of wind still goes.
  Whisper stretches a word over a pause; a word much longer than it takes to
  say is trimmed the same way the clip edges are. Every utterance keeps
  0.07 s before / 0.10 s after, and a removed pause leaves 0.16 s of air
  (0.30 s after a full stop).
- **...but only where the audio agrees.** In wind, Whisper's word times
  drift (on Marina's reel 01 a transcript gap cut through a sentence). A
  transcript gap or a stretched-word trim is cut only if the audio there is
  below voice level (RMS −26 dBFS). `tools/gapcheck.py NN` must report 0
  before `--render`.
- **Bad takes — the transcript is the script** (Ruta, 2026-11-05). Last take
  wins (Ruta's rule, 2026-10-05): when a line is fumbled and said again, every
  earlier attempt goes. `tools/takes.py NN` lists every place she starts the
  same words again; read them against the transcript (many are her repeating
  on purpose, which is content and stays), then write `work/rNN/script.txt` =
  the transcript with the fumbled earlier attempts deleted. `cut.py` aligns
  every word to it with a Viterbi pass that may jump back; a backward jump is
  a restart and the earlier attempt is dropped. A restart that would drop more
  than 40 words is flagged in `cut.txt`, not cut. In wind one utterance can
  hold a whole fumble; then the drop goes in `cut-fix.json`.
- **Manual calls:** `work/rNN/cut-fix.json` — `drops` / `keeps` (raw seconds),
  `punch` (a closeup), `face`, `wide`. Ruta's instructions go here.
- **Framing:** pure scale steps centred on her (base 1.00 / in 1.10), never
  the same crop twice across a cut. A clip over 5.5 s gets a zoom cut inside.
- **...but never zoomed in under a graphic** (Ruta, 2026-11-17: *"Don't zoom in
  and then put things somewhere where they can go on her face. Zoom out, it's
  okay"*). Zooming in pushes her chin down into the band where the graphics
  live. Every clip a graphic sits on stays at base framing: `cut-fix.json`
  `"wide"` lists those clips (raw seconds) and `cut.py` frames them base.
- **The big punch-in is only for a reaction, an aside or a joke.** Use
  `punch` at 1.50. Punch spans become `no_paint`: captions only.

**Matte her per beat, never per reel** (Ruta's repo): `tools/matte.py` for a
big object behind her, one beat at a time. On this machine a matte costs
about 0.6 s a frame (a 10 s half-screen: 3 min).

**A cut-out never goes over her in the browser; it is baked into the plate**
(Ruta, 2026-11-17: *"on the cutout, the color of the face changes into a more
warm orange one ... there is a clear difference where it's natural and then
there's more yellow"*). The renderer converts a transparent video's colours
differently from the plate's (measured on skin: red +5, blue −14), so a
cut-out laid over her own frame comes out warmer than she is.
`tools/halfscreen.py` composes the half-screens in ffmpeg instead: her head is
her own plate pixels, the matte is used only as a mask, so nothing can differ.
The page adds only the panel's content.

---

## 2. Text: where it comes from (Ruta's repo)

**Spelling** comes from her transcript / script in `work/rNN/script.txt`,
never from speech recognition alone. **Captions are what she said,
verbatim**, in her own language and words. Whisper supplies timing; its
mishearings are fixed in `build.py` (a `FIX_AT` list keyed by plate time).

---

## 2b. Captions: the machinery

How a caption looks (font, size, colour, case, height, chunk length, how it
appears) is the client's: `LOOK.md §2b`, `tools/look.py` `CAPTION_CSS` and
`LOOK`. The machinery is the same for everyone. `Kit.captions()` groups the
aligned words into blocks in one of three modes (`LOOK["caption_mode"]`):
`phrase` (a phrase to its comma), `type` (each block types on letter by
letter with a cursor) or `word` (word by word).

Known caption bugs to guard against (Ruta's repo):
- a word straddling a clip start gets clipped (clamp it);
- `%` splits off its number (merge);
- a leading apostrophe breaks «інтерв'ю» (merge);
- a leading hyphen survives into the token (`lstrip("-")`);
- consecutive blocks superimpose for ~1.5 frames (clamp
  `end = next.start − 0.085`). Two short blocks can still overlap; merge a
  block under 0.30 s into its neighbour (`MERGE_PREV` / `MERGE_NEXT`).

**When a graphic needs the subtitle's place**, move the subtitle out of its
way for that span rather than stacking type on type.

### 2b.1 When captions drop, and when they invert (Ruta's repo)

Ruta's rule, 2026-09-15:

> *"when there's no text on the animation — the subtitles should still be there,
> basically the no subtitles only affects animations that have text, so that its
> not like subtitles say 10 euros and animation also says 10 euros"*

So the test is **redundancy, not takeover**. A full-screen graphic does not earn
a blackout by being full-screen; it earns one by *saying the word she is saying*.

- **Blackout** the span where a graphic's own text repeats her words. A
  graphic that carries the whole phrase *replaces* the subtitle for that
  phrase.
- **Keep them everywhere else**, including over a takeover with no text in it.
- **Invert** for the whole of any light takeover — `.cap.inv`, via the
  `invert=` argument. Light captions on a light page are invisible.

Two mechanical traps, both hit:

1. The scrim's off-spans must be **merged into a union** before emitting. One
   off/on pair per span looks right and is not: a blackout nested inside an
   invert span restores the underlay at its own end, and the scrim sits
   behind inverted captions for the rest of the takeover as a grey cloud.
2. `blackout` has existed in `kit.py` since the matte commit. Across Ruta's
   reels 7–11 it was passed **zero times**, so every graphic had to survive
   being stacked on a permanent caption rail — which is why every graphic was
   small, low and out of the way. If the reels look samey, check this first.

---

## 2c. Takeovers and half-screens: the mechanics

**The graphic owns the frame or it is not there** (Ruta's repo). A takeover is
a `.g.full` whose first child is an opaque ground (`.tk.<name>`, the grounds
are the client's: `LOOK.md §5a`). The plate is gone, so none of the
over-footage rules apply. How long a takeover lasts, how it is built and what
its grounds are come from the client's refs (`LOOK.md §2c`).

Rules learned building Ruta's reel 9 (Ruta's repo):

- **Bleed off at least two edges.** A takeover composed inside the frame with
  margins reads as a slide, not a takeover. Decoration may bleed; readable
  text stays in the safe area (§3a). Mark bleeding elements
  `data-layout-allow-overflow`.
- **The ground belongs to the beat that starts first and must outlive every
  other part of the takeover.** Fade the *children*, keep the ground.
- **Transforms only.** `width`, `height` and `margin` are layout properties:
  the linter rejects them and they snap to integer device pixels mid-tween. A
  typing reveal is `clipPath: inset(...)`; a band that fills the frame sits at
  its *resting* size and scales **up**.
- **Solve push-ins, don't eyeball them.** To bring point `p` to centre `c` at
  scale `k`, the wrapper offset is `c - (c + (p - c)k)`.
- **Use the whole frame when captions are blacked out.**

**The half-screen** (Ruta's mockup, 2026-11-17, `refs/mockups/half-screen.jpg`
in Marina's editor). Use it for a list or a how-to that needs reading time,
and for anything that does not fit under her chin (§3b):

- **She goes down to make space on top.** Her video slides down in 5 frames,
  ease-out, and comes back up the same way when the beat ends, on the jump
  cut. How far is measured: far enough that the top of her hair, at its
  highest over the beat (`face_flat.json`), clears the panel's content by
  40 px, and never less than 480 px.
- **The panel fills the top**, a flat ground from y 0 down to y 1080. It comes
  down with her move. (The ground is the client's.)
- **Her head is cut out** and sits in *front* of the panel's bottom edge, so
  the edge meets her hair and never crosses her face. Baked, not overlaid
  (§1): the build writes `reel-NN/halves.json`, then `tools/matte.py` (one
  per half-screen, the build prints the commands) and
  `tools/halfscreen.py NN`.
- **Content goes in the top**, inside the safe area and above her hair
  (from y 262): a real element (§4). Its content appears once she has moved
  and goes before she moves back.
- **No subtitles under it.** Her mouth now sits where the subtitle would.
  The build stands the subtitles down for the span (a block that started
  before it is cut short, one that runs past it starts late).
- **A panel over her never covers her face** (Ruta, 2026-11-17: *"rn its
  covering her face until the eyes, thats stupid"*): never a straight edge
  across her chin, mouth or nose. That is what the half-screen is for.

---

## 3. Frame geometry

Ruta's placement rules: **never put a graphic in a corner**; **under her
chin or behind her head, never on it** (§3b); a big object can go **behind
her head** on a half-screen (§2c); a takeover owns the whole frame.

**Nothing on her head, ever: not text, not a shape, not a card** (Ruta,
2026-11-17: *"make sure that nothing is going on her face ... a lot of things
are going over her lips and her chin, and that's not okay. They should always
go under her chin or behind her head"*).

| Zone | |
|---|---|
| **Eyes to chin** | nothing, ever |
| **Under her chin**, down to the subtitle | measured per frame (§3b) |
| **Behind her head** | only on a half-screen, baked (§2c) |
| **Above / beside her head** | only where the plate has room, inside the safe area |

What goes in each zone for this client is in `LOOK.md §3` (from her refs).
Measure every new client's plates first: where her chin moves and how much
headroom there is decides how much goes under the chin and how much on
half-screens.

### 3a. Instagram safe area (Ruta, 2026-11-17)

```
canvas      1080 x 1920
avoid       top 220-250 px      (username, top icons)
            bottom 320-450 px   (caption, audio, like/comment/share rail)
            sides 60-130 px     (left and right)
safe area   about 840 x 1350 in the centre
rule        x 130-950, y 250-1470 for anything readable
```

**"Some stickers or elements can go out of the safe zones, but anything
readable has to be inside."** Decoration (stickers, photos, shapes, grounds,
cards' edges) may bleed out and off the frame. Every readable word, number
and subtitle stays inside. So a readable line is at most 820 px wide: size it
to fit, or break it onto two lines. Where a client's refs bleed type off the
frame, Ruta's rule wins.

`node tools/safezone.js reel-NN` loads the composition, steps the timeline
and measures every visible text run by its ink (the glyphs' own ascent and
descent, not the font's line box). It must report nothing before a render; a
text run caught only while it slides in or out is fine.

### 3b. Under her chin, measured (Ruta, 2026-11-17)

Headlines placed at fixed heights from one measurement of her chin sat on her
lips once she leaned in. So:

1. `python tools/facemap.py NN --flat` finds her face on every frame of the
   plate as cut (OpenCV YuNet at 10 fps) and writes `work/rNN/face_flat.json`:
   face box, eye line, mouth, chin, top of hair.
2. The build places every beat with `under(t_in, t_out)`: the lowest her chin
   goes while the beat is on screen, plus 30 px. Nothing is placed by eye.
3. The band ends at the top of the subtitle or, where the graphic has taken
   the subtitle's words (§2b.1), at the safe area's bottom (y 1470). The build
   checks every beat against the subtitle blocks on screen with it and prints
   any that run into one (`fit:`).
4. What does not fit: shrink to the client's smallest display size, split the
   subtitle so the graphic takes one word (`split_cap`), drop the line the
   subtitle already carries, or move the beat to a half-screen.
5. After the bake, `python tools/facemap.py NN` maps the plate as rendered and
   `node tools/safezone.js reel-NN` tests every visible graphic against her
   head (face box raised to the top of her hair) at every step, and against
   every visible subtitle. It must report nothing.

**Greenscreen cutouts stay big** (Ruta, 2026-09-29): when she is cut out over
a screen recording, keep her at ~60–70 % on the left, face above y ≈ 1500 and
left of x ≈ 880 — at 45 % in the bottom-right corner she was *"eated by the
buttons from ig interface"*.

---

## 4. What to show (Ruta's repo + Ruta, 2026-11-17)

Whether words are allowed in graphics, and how graphics move, are the
client's (`LOOK.md §4`, from her refs). What applies to every client:

- **No graphic repeats a whole subtitle**, and a graphic that says the word
  she is saying replaces the caption for that span (§2b.1).
- **The literal thing, shown as itself:** the app she opens as its real
  screen recording, her follower count as her real profile, her views as her
  real Insights card. When the real asset is missing, don't draw a stand-in:
  ask Ruta for it.
- **Every element is a real element** (Ruta, 2026-11-17: *"I don't like the
  style of these um, like message button icons or the sort of sending line.
  Everything is always, according to our design system ... a real element. So
  it could be a real Google-esque kind of search bar. It could be some other
  stylized messages, but it cannot be just this. It has to have some kind of
  real life texture to it"*). An object is drawn as the interface people
  actually use, with its real proportions and real behaviour (a caret that
  types, a check that fills, a bubble with its tail). Never an icon standing in
  for it: no circle with an arrow for "send", no three dots for "message".
  The kinds built so far: to-do card, struck list, search box, messages,
  chips, chart card, spreadsheet, viewfinder. How each is drawn (colours,
  type, line weights) is the client's (`LOOK.md §5a`). No invented content in
  them: her words, or empty and skeleton states.
- **Write the verb before the noun.** Not "a chart of the cost" — "the cost
  falls to zero". No verb means you have a label, and labels are the
  subtitle's job.
- **Reuse objects.** A returning object costs nothing to read and lands
  harder.
- **A graphic must not outlive its sentence; match the length of the moment
  to the length of the word; reach for the obvious literal image when there
  is one.**
- **Memes and reaction stills** only real ones Ruta provides.

---

## 4a. What she flags in review (Ruta's repo)

Her first full pass, on reel 7 (2026-09-14). Every note reduced to one of five
rules, and all five outrank instinct the same way the rest of this file does.

**1 · A graphic lands ON the word, and she counts the seconds.** The
Cal.com→Calendar sync finished about half a second into the *next* sentence and
her note was *"waaaay too late, i would have put it like 3 secs earlier to match
the text"*. Budget the whole beat — arrival, movement, exit — inside the phrase
it illustrates, and clear it before the next phrase starts.

**2 · When the image is not instantly legible, use the word.**

> *"shitty icon, either do properly or write CRM"*
> *"the points could have been written out properly"*

A drawn glyph that reads as nothing becomes type: a wordmark *is* the logo when
no icon exists, and field names are text inside a depicted interface.

**3 · A graphic must not outstay its sentence — and she can see four seconds.**
Both directions: *"took too long too"* (held 4 s across two sentences) and
*"literally one second wtf"* (a tile that flashed and left). The fix is never
to stretch one object across a section; it is more, shorter events on the
actual phrases.

**4 · Every object has to be nameable.** *"whats that little glowing dot?"* If
a viewer would ask *what is that*, it is not finished.

**5 · A blank plaque says nothing.** An empty slot is readable only once the
viewer knows what it is for; give it ghosts of what will land in it.

**Proof is a screenshot.** Her call, 2026-09-29: Instagram stats, DMs, comments,
reviews go on screen as her real screenshots (cropped, blurred where personal),
never redesigned as cards — *"then people trust it more and dont think that we
came up with the numbers"*. Animate around the screenshot, don't retype it.

**No invented stats.** A view count, follower number or sum shown as *hers*
must be hers. Shape-only charts, or a clearly labelled demo card, are fine.

And one literal: *"tasks are always checks and lines like a checklist"* — a
checkbox and a rule, never three coloured bars.

### Her editing is not filler

> *"when you see some funny editing (extra closeup, extra far away) those are
> funny bits and dont paint over them"*

A shot change in her delivered cut is an instruction. `tools/shots.py` finds
hard cuts, `tools/pullouts.py` finds zooms; every such span goes in the
build's `NO_PAINT` list, and beats that fall inside are **deleted**, not
nudged.

---

## 7. Build and render

```bash
python build.py                         # prints fit: and the matte commands for each half-screen
python ../tools/sfx.py mix NN           # base.mp4 = the plate as cut + sfx
python ../tools/matte.py reel-NN ...    # one per half-screen, from build.py's output
python ../tools/halfscreen.py NN        # bakes the half-screens into base.mp4
python ../tools/facemap.py NN           # her face on the plate as rendered
python ../tools/review.py reel-NN       # timeline: holds, flashes, gaps, drift
node ../tools/safezone.js reel-NN       # safe area, nothing on her head, nothing on a subtitle
node ../tools/frames.js reel-NN --beats # a still per beat over the real plate, + contact sheets
npx hyperframes check                   # must pass before rendering
npx hyperframes snapshot --at <times> --no-end -o study/snap
npx hyperframes render                  # on the machine (below)
```

**Render on the machine, not HeyGen** (Ruta, 2026-11-17: "can you use the
machine, no heygen pls"). Render with `npx hyperframes render` in the cloud
session. `tools/hfrender.py` stays for when she asks for HeyGen again.

Always snapshot before rendering — a render takes many minutes and a snapshot
pass is under one. Verify the first frame, each beat's proof pose, and the
exact final frame: frames = DUR×30, no black tail, audio present.

**Deliver** (2026-11-17): the render is checked (frames = DUR×30, audio, no
black tail), then two copies go out:
- an 8 Mbps Instagram copy (`REEL-NN_vN_instagram.mp4`), sent to Ruta in chat;
- a copy under 100 MB for Cloudinary, which refuses anything larger on this
  plan ("Maximum is 104857600"). Two-pass at 4.2 Mbps with 160k audio comes
  to ~96 MB for a 2:56 reel. It goes in the `reels` folder as
  `IMG_<raw>_reel_vN`, tagged with the raw name, `reel` and the version.
  Upload it signed (Cloudinary `sign-upload`), in 20 MB chunks
  (`Content-Range` + `X-Unique-Upload-Id`).

Machine notes (Ruta's repo): never run heavy jobs in parallel; ffmpeg here has
no glob support, use numbered inputs; Whisper `medium` handles Ukrainian
well.

---

## 8. How she gives feedback (Ruta's repo)

Fast, specific and blunt — take it literally. She spots real bugs (a
mispositioned currency symbol, a hand that reads as detaching, a graphic that
duplicates her own subtitle). "A bit thin" means roughly double it. Show work
early; snapshots beat a long silent build.

---

## 9. B-roll and sound

**B-roll** (Ruta, 2026-11-05): the client's b-roll is catalogued once, in
`broll/CATALOG.md` (what each clip shows, where it is, length, orientation),
so a reel run picks from the catalogue instead of sorting footage every time.
Only her real footage and photos; if nothing fits, ask Ruta. How her
refs use b-roll is in `LOOK.md §9`.

**Music: none for now** (Ruta, 2026-11-17). Voice plus sound effects only.

**Sound effects** (Ruta, 2026-11-05: "basic sound effects should be
included (typing, whooshing etc)"): the kit is in `assets/sfx/`
(`tools/sfxkit.py` made it: click-soft, click, key-press, typing, pop,
whoosh-short, whoosh, ping, notification, sparkle, kaching). Cues and levels
are Ruta's (`tools/sfx.py`): quiet, on the event, never on a closeup, about
0.5 cues a second at most. Put the cue on the frame the graphic appears. A
recorded file with the same name dropped into `assets/sfx/` replaces the
synthesised one.
