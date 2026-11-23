# Ruta — reel animation spec

> **THE LOOK IS LOCKED (2026-11-23).** There is one look: **§00** below,
> including *"Her review of reel 61"* — it wins over every older section.
> Kit `tools/gstyle.py` · worked example **`reel-61/build.py`** · standing brief
> **`BUILD-BRIEF.md`** · render locally, never HeyGen · post via Buffer from a
> Cloudinary link. Any other look lives in `archive/` and is never used unless
> she asks for it by name. If a session starts on a branch without this banner,
> it is on a stale branch — stop and find the current one.

> **Ruta's reels only** (everything under `RUTA/`). Anything under `Nika/` is
> another person with her own contract: read `Nika/README.md` and nothing here.
> If you can't tell whose reel it is, ask before building.

Rewritten 2026-09-09 for the current delivery model. The design process — how
the reference reels work and how to specify a beat — lives in the playbook:
**`ANIMATION-PROCESS.html`** (published artifact). This file is the technical
contract: what to build against, and what her machine will tolerate.

---

## 00. The look — Google style + Excalidraw sketches (her spec 2026-10-21; the default since 2026-10-28)

Her ask with the 2026-10-21 batch: *"change the style a little bit, maybe not
dramatically, but at least make it lighter"*, then this spec. **This is the look for every reel.** Build with
`tools/gstyle.py`; `reel-54/build.py` is the latest worked example. The old
refined-glass look (burgundy ground, glass tiles, iris takeovers — reels 12–40)
is archived in [`archive/STYLE-refined-glass.md`](archive/STYLE-refined-glass.md):
never build in it unless she asks, and never put a burgundy ground anywhere.
Where an older section below mentions glass, burgundy or takeovers, this
section wins.
The approved reference is her 4-layer mock, the artifact **«Reel Layer States»**
(claude.ai/artifact/8goY2j72LvmTdwND9mdvux): keep its motion and timing feel,
with the changes below.

**0 · Memes** — comic-relief reaction memes (max 3 per reel, never in the CTA), picked from
`assets/memes/MEMES.md` and placed with `g.meme()`; see `BUILD-BRIEF.md`. They are the one thing
here that is not "Google style" on purpose.

**1 · No-go zones** — no text, captions or key graphics; background fills and
panels may extend into them.
- top y 0–270 · bottom y 1536–1920 (username, caption, music, progress bar) ·
  right action column x 900–1080 × y 940–1536 · left edge x 0–90, full height.
- The feed/grid preview crops 240 px off top and bottom (3:4): on the cover
  frame the hook sits inside y 240–1680.
- Safe content box ≈ 840 × 1350, centred (top buffer ~250, bottom ~320–450).

**2 · Subtitles** — phrase chunks, one or two lines (the mock: «Вона кидала
відео в [Gemini],»), not word-by-word.
- Band: centred, box bottom ≤ y 1520, top ≈ y 1400; max width 720, never past x 900.
- White box `rgba(255,255,255,.94)`, radius 28, padding 16/30, Google Sans 500
  54 px, `#241919`, shadow `0 2px 10px rgba(36,25,25,.10)`. The key word sits in
  a pill: `#7A1424`, white text, spring pop-in.
- Half-screen layer: never in the bottom zone. Directly under the chin if the
  chin is at or above ≈ y 1380 at that moment; otherwise on the white panel above
  her head (box bottom ≥ 40 px above the hair, never above y 270).

**3 · Layers** (person matte = her cut-out, frame-accurate)
1. **Above me** — cards, chips, pills, the CTA, all inside the safe area. Cards
   `#FFFFFF`, radius 40, shadow `0 1px 3px rgba(36,25,25,.10), 0 10px 30px
   rgba(36,25,25,.10)`. Chips radius 16, 2 px border `#DEBFBF`, fill `#FFF8F7`.
2. **Behind me** (masked) — big words, Google Sans 700, `#7A1424`, 240–300 px,
   letter-spacing −0.04em, top at y ≥ 290. Readable: her head may cover at most
   the bottom ~25 % of the lowest line (the mock's «чат» was hidden too much).
3. **Half screen** — a white panel from the top to y 1240 slides in (0.85 s,
   `cubic-bezier(.65,0,.25,1)`) while the whole video (plate + matte) pushes down
   330 px, so she is cut at the shoulders and her head matte overlaps the panel
   edge. Both reverse on exit. Panel content is Excalidraw explanation, between
   y 290 and 40 px above the hair.
4. **Full screen** — white slides up from the bottom over everything, head
   included. Only for big explanation / section moments. **Never the CTA.**
5. **CTA** — always in the above-me layer (card or pill in the safe area) with
   her visible.

**4 · Removed** — every star / starburst / cookie / flower / morphing Material
shape. None anywhere.

**5 · Excalidraw sketches** — only for explanations and pointer doodles
(arrows, circles, underlines, boxes).
- rough.js, sloppier than the mock: roughness 2.2–2.6, bowing 2.5, stroke 4–5 px,
  multi-stroke on, slight overshoot at line ends.
- Rectangles are rough *rounded* paths, radius 24–32.
- Ink `#1E1E1E`, emphasis `#7A1424`, hachure fill `#F2C7CA` (gap 14–18, angle
  −41, weight 2.5).
- Handwritten labels in Pangolin 44–56 px (Excalifont only if it renders
  Ukrainian correctly).
- Draw-on: each stroke reveals in 0.6–0.8 s, in sequence; a box's label fades in
  after its box.

**6 · Colour and type** (Material 3, seeded from `#7A1424`)
- primary `#7A1424`, on-primary `#FFFFFF`, surface `#FFFFFF`,
  surface-container-low `#FFF0F0`, outline-variant `#DEBFBF`, on-surface
  `#241919`, on-surface-variant `#574142`.
- White and dark red only — no blue, no other hue.
- UI and captions in **Google Sans** (Ukrainian Cyrillic). Not Google Sans Flex —
  no Cyrillic.

**7 · Motion** (unchanged from the mock)
- Pops 0.5–0.6 s `cubic-bezier(.34,1.56,.64,1)` · rise-ins 0.7 s
  `cubic-bezier(.2,.9,.25,1)` · panel and full-screen slides 0.85 s
  `cubic-bezier(.65,0,.25,1)`.

**Her review of reel 41 (2026-10-21) — amends the spec above:**
- **Captions stay exactly as before §00**: word by word, upper case, Product
  Sans Black 90 px, white on the underlay plaque (kit.py's rail). Over the white
  panel / cover they turn ink; on the panel they sit above her head. Not the
  boxed phrase captions of §00.2.
- **Sketches are calm**: roughness ≈ 1 (Excalidraw's own). §00.5's 2.2–2.6 was
  "too sloppy".
- **Over her footage nothing is a bare line**: white on her light room failed
  even AA. Closed shapes are solid white stickers with the dark outline; arrows,
  lines and free labels are dark ink with a thick white halo.
- **Behind-me words are white** (soft shadow), not #7A1424 — the red read badly.
- **A full screen never opens onto empty white**: its content lands with it.
- **Arrows are long** (≥ 150 px, gentle curve); **no arrowhead on a loop**.
- **A pointer to the comments points down** toward the lower right, never up.
- Her verdict on the result: *"perfect delicious"*.

**Her review of reel 61 (2026-11-23) — natural editing; amends everything above:**
- *"I'm striving for a more natural editing style, where I only show things that
  are really necessary, but we are not animating every single word for the sake
  of animations."* A graphic only where it carries information. «іноді корисно»
  as a chip read as cringe / "Claude vibes". Roughly one meaningful moment per
  sentence group, not per phrase.
- **Scene change every 2–3 s by other means**: her cuts and punch-ins, a
  behind-me word, a full screen, a camera move inside a full screen — not a
  new chip.
- **Behind-me big text is part of every reel** (one or two words, the hook and
  a name).
- **Real UI = a full-screen platform-ad sequence**: the screen floats in 3D,
  tilts, the camera zooms smoothly into the part she names, a control changes
  state on its word, zooms back out. Never a tiny screenshot on a panel. When
  her screenshot is too small to zoom (it blurs past 1.5×), rebuild it 1:1 in
  HTML from the screenshot (same layout, labels, text) — `reel-61/build.py`.
- **Excalidraw only for real highlights and schemes** (the half screen's
  diagram). Never red handwriting with a thick white halo over her footage.
- **Everything else modern Google, slight glass occasionally** (`.glass` in
  reel-61: frosted white, hairline rim, soft cast).
- **Give her head room**: cards small, y 300–560, never crowding her hair or
  the top edge.
- **No decorative pointer arrows** (the CTA arrow "is shit").
- **Shuffle for lists** (her idea, and *"lets use it in general … basically for
  lists, as an option"*): instead of a row/stack of chips, the items pass
  through ONE slot like cards — each rises in from below on its word as the
  previous leaves upward. Less space over her head, more motion. Kit:
  `shuffle(["#a", "#b"], [t1, t2], end)` + `.shuf` (tools/gstyle.py). Each item is a
  plain white card — no glass around it (her note).
- **CTA pill may sit in the subtitle band** (y ≈ 1404) once the blackout from
  its word frees it — keeps the space above her head for the list.
- **ТЕСТ CTA** («якщо ти не впевнена… пиши ТЕСТ… я змонтую твоє відео») is cut
  out of the reel entirely, even if the ending turns abrupt.

Still in force from below: spelling from her script (§2), a graphic lands on
its word and never outstays its sentence (§4, §4a), every object nameable, no
invented stats, proof is a screenshot, her closeups are comedy (NO_PAINT).

---

## 1. The delivery model

**She makes the base edit. I add the animations and render the final video.**
Never re-cut her footage.

**Matte her per beat, never per reel.** Both halves of the old blanket ban have
been retested (2026-09-10). The artifacts are gone: `u2net_human_seg` holds the
flyaway strands at her hairline cleanly with no fringe. The cost has not moved —
**~1.75 s/frame, CPU only** (re-measured 2026-09-15; the 3.3 here before was from 2026-09-10 and roughly doubled the real cost), because her Vega 10 gives ONNX no GPU provider. That
is ~4 minutes for a 2-second beat, and *two hours* for a whole reel, which is
the opposite of the lightness on her machine this pipeline exists to protect.

Her call on when: *"lets do it per few beats, cause its needed only sometimes,
when there are big things behind me."* So the trigger is **size**, not
availability — a brand tile, a big card, a takeover-scale object that wants to
pass behind her head. A chip or a caption does not earn four minutes; those
still follow §3 and sit below her. Use `tools/matte.py` to cut it and
`k.matte()` to place it; the matte layer sits above every graphic and below the
scrim, so one call per beat is enough.

**The matte is her own pixels, repainted** (her catch on 41–52, 2026-10-21:
"my colors change to slightly more orange" whenever a word sat behind her or a
half screen opened). Straight out of remove-background the cut-out rendered
~9 levels short of blue against the plate. `tools/matte.py` now keeps only the
shape and repaints it with the plate's YUV, tagged so the render decodes it the
way it decodes the plate. Its docstring has the three causes and the
measurement; `--repaint` fixes an old matte without re-running removal.

There are **two variants**, and which one applies changes how much freedom the
animation has:

| | **Variant A — she captions** | **Variant B — I caption** |
|---|---|---|
| She delivers | cuts, grade, **subtitles burned in** | cuts, grade, **no subtitles** |
| I deliver | animations only | animations **+ subtitles** |
| Takeovers | inset cards only — a full cover would hide her captions | **full-screen allowed**, captions move with the design |
| Used on | reel 2 | reel 3 onward |

Variant B is the better one and she moved to it herself from reel 3: *"I'm not
gonna put subtitles in… you can put the subtitles whenever you want. So you can
put the animations full screen if you want — you have more choices of what to
do."* It removes the constraint that shaped most of reel 2's compromises.

Two superseded models, do not re-propose:
- *Full edit by me* — rejected, above.
- *Loose overlay clips she blends in Edits with LIGHTEN* — worked, but she
  prefers a finished render now. Its constraint is preserved in §6 in case it
  comes back.

---

## 2. Text: where it comes from

**Spelling** comes from `SCRIPTS.md` (all six scripts, as she wrote and read
them). Never from speech recognition — Whisper mangles every product name:
`Fathom → FATAM`, `офер → ОВ`, `CRM → сірем`, `таск-менеджер → тест-менеджер`.

**Timing and wording** come from the delivered audio. She improvises against her
own script — reel 2's CTA is «система» on paper and «дзвінок» on camera. Run ASR
on her cut for word-level timings only, take spelling from the script, and ask
her wherever the two disagree.

---

## 2b. Captions (variant B)

Measured off her own burned-in captions in reel 2, so mine match across her feed:

```
one word at a time, UPPERCASE, punctuation kept  («БЕЗКОШТОВНО.» «КОНСУЛЬТАЦІЇ,»)
font-size   90px          Google Sans, wght 700 / GRAD 200
colour      #ffffff       flat — no stroke, no drop shadow
align       centred horizontally
position    vertical centre y ≈ 1472  (band 1445–1498)
```

Word timings come from ASR on her delivered cut; **spelling always from
`SCRIPTS.md`**, never from ASR. Known caption bugs to guard against, all hit
before: a word straddling a clip start gets clipped (clamp it), `%` splits off
its number (merge), a leading apostrophe breaks «інтерв'ю» (merge), a leading
hyphen survives into the token (`lstrip("-")`), and consecutive words superimpose
for ~1.5 frames (clamp `end = next.start − 0.085`).

Being the caption's owner is the point of variant B: a caption can **move out of
the way** of a full-screen graphic, or a single word can **lift out of the
caption into the design** on the frame it is spoken. Default to her style; depart
from it only where the design earns it.

### 2b.1 When captions drop, and when they invert

Her rule, 2026-09-15, after the first five-reel batch came back as *"technically
right, but all very typical and homogenous"*:

> *"when there's no text on the animation — the subtitles should still be there,
> basically the no subtitles only affects animations that have text, so that its
> not like subtitles say 10 euros and animation also says 10 euros"*

So the test is **redundancy, not takeover**. A full-screen graphic does not earn
a blackout by being full-screen; it earns one by *saying the word she is saying*.

- **Blackout** the span where a graphic's own text repeats her words. In reel 9
  that is three spans out of five takeovers: the prompt bar typing «зроби
  презентацію на таку тему» while she reads it, the margin notes writing
  «картинка» / «графік» on those two words, and the brandbook page whose header
  says ДИЗАЙН-СИСТЕМА while she says «дизайн-систему».
- **Keep them everywhere else**, including over a takeover with no text in it.
- **Invert to ink** for the whole of any light takeover — `.cap.inv`, via the
  `invert=` argument. White captions on a white page are invisible, which is
  how reel 9's flat-white skeleton beat nearly shipped.

Two mechanical traps, both hit:

1. The scrim's off-spans must be **merged into a union** before emitting. One
   off/on pair per span looks right and is not: a blackout nested inside an
   invert span restores the underlay at its own end, and the dark scrim sits
   behind ink captions for the rest of the takeover as a grey cloud.
2. `blackout` has existed in `kit.py` since the matte commit. Across reels 7–11
   it was passed **zero times**, so every graphic had to survive being stacked
   on a permanent caption rail — which is why every graphic was small, low and
   out of the way. If the reels look samey, check this first.

### 2c. Phrase captions — opt-in (her call, 2026-11-23)

**Default stays §2b: one word at a time.** Switch to phrase captions only when
she says so: "2-3 word / 3-4 word subtitles", "phrase subtitles", "not one word
at a time", or "just put subtitles, nothing else".

Same look as §2b — nothing changes but the grouping and the size:

```
3-4 words at a time, UPPERCASE, punctuation kept
font        Product Sans Black, 68px (≈25% smaller than 90, so the line fits)
colour      #ffffff flat, tracking -0.015em, centred, vertical centre y = 1472
plaque      the usual dark underlay behind them (1040x450 at 20,1247)
grouping    ≤ 4 words, line ≤ 880 px; break after . ? ! and after a comma at 3 words
pauses      gentle: trim dead air at start/end only; mid-gaps over 0.9 s → 0.4 s
```

Not ASS/libass, not Google Sans, not small sentence-case text with an outline —
that was tried and rejected. One command does the whole run and is the reference:

```bash
python3 tools/phrasecaps.py <in.mp4> <out.mp4> [--words words.json] [--fix fix.json]
```

---

## 3. Frame geometry (measured off reel 2, 1080×1920 @ 60fps)

| Zone | Rule |
|---|---|
| **y 1445–1498** | Her burned-in caption band. Never cover it. |
| **y ≈ 575 down** | Her head. She sits **left of centre**; closer on emphasis beats. |
| **y 60–540, full width** | Empty in *every* shot. This is where graphics go. |

**Never put a graphic in a corner.** Her note on v3: *"the animations are now in
the top right corner, and I want them to be centered… better for them to be
centered and, like, wider, basically, more rectangle, instead of it being
small."* Every graphic is horizontally centred and uses most of the frame width —
600–900px wide. Directly above her head is fine; a corner is not.

**Keep graphics off her face — and drop them low rather than cover it.** Her note
on reel 3 v2: *"lets not do it as much on my face, you can put it lower, it's
okay if it's not according to the rules cause nobody cares it's not vital
info."* So the clear band is a default, not a constraint to defend: when a
graphic will not fit above her head, put it **below** her — over her chest or
the counter — instead of over her face. The band rule loses to her face every
time. The exception is a takeover, which owns the whole frame anyway.

She has always wanted graphics **masked behind her head** — *"I would prefer if
you use the mask so that it's actually behind my head, but it's okay, we can
survive without it"* — and as of 2026-09-10 she gets it on the beats that earn
it. See §1: big object behind her, `tools/matte.py`, four minutes. This is now
the better answer to a graphic that will not fit above her head; putting it low
over her chest is the fallback when the object is small enough not to be worth a
matte.

**No full-frame takeovers.** A full cover hides her subtitles while she is still
talking. Use a large **inset card** — reel 2 uses `x 50–1030, y 60–1328`, which
owns the frame visually and leaves the caption band clear. The reference reels
do the same; their panels all carry visible margin.

**Moving her costs caption legibility** — her subtitles are baked in, so scaling
the plate scales the text with it. Reel 2 does this exactly once, for 2.4s at the
emotional peak. More split-screen would need a clean cut without subtitles.

---

## 4. The animation rule

**«Не кажи — покажи» — never say, always show.** A graphic contains **no words
at all**. Exceptions: a **number** (a quantity, not a word), and text **inside a
depicted interface** (a comment box being typed into shows an action).

Test: mute it and hide the subtitles. If you can't tell what the beat is about,
it isn't finished.

- **Pacing: a visual event every 3–5 seconds.** Her delivery is slow and expert;
  the cuts alone deliver no new information. A 51s reel takes 10–17 beats.
- **Write the verb before the noun.** Not "a chart of the cost" — "the cost falls
  to zero". No verb means you have a label, and labels are the subtitle's job.
- **Reuse objects.** Reel 2 uses one task stack for three beats and one diagram
  for two. A returning object costs nothing to read and lands harder.
- **Land it and leave it.** Nothing loops, drifts or breathes — except where the
  loop *is* the meaning (the spinner at 15.3s that never completes).
  (The plate may push in slowly; graphics still land and stay put.)
- **Put every element on its word.** Uneven spacing is correct; even spacing
  reads as automated.
- **Thick.** Strokes ≥12px, wires ≥15px, rules ≥16px. Thin reads as amateur.
- **A graphic must not outlive its sentence.** v3's task stack landed at 9.0s and
  then sat unchanged until 15.3s while she talked about something else. Her note:
  *"it stays there for a very long time… which could have used a different
  animation or, like, remove that animation while I'm saying that."* Either give
  the next sentence its own beat or clear the frame.
- **Match the length of the moment to the length of the word.** v3's stall
  spinner ran 3.2s, but «зависає» is 0.74s long and she is onto the fix by 16.12.
  It now runs ~1.0s and stutters to a dead stop. Her note: *"it's too slow, and
  it's a little bit not as dynamic."*
- **Reach for the obvious literal image when there is one.** She asked for the
  **Ukrainian flag** on «українською мовою» — the one sanctioned departure from
  the red/pink palette, because it is a flag and it has to be its own colours.

---

## 4a. What she flags in review

Her first full pass, on reel 7 (2026-09-14). Every note reduced to one of five
rules, and all five outrank instinct the same way the rest of this file does.

**1 · A graphic lands ON the word, and she counts the seconds.** The
Cal.com→Calendar sync finished about half a second into the *next* sentence and
her note was *"waaaay too late, i would have put it like 3 secs earlier to match
the text"*. Budget the whole beat — arrival, movement, exit — inside the phrase
it illustrates, and clear it before the next phrase starts. §4 already says put
every element on its word; this says the *end* is on the word too.

**2 · When the image is not instantly legible, use the word.**

> *"shitty icon, either do properly or write CRM"*
> *"the points could have been written out properly"*

A drawn database glyph read as nothing, and six blank pills standing in for CRM
fields read as nothing. Both became type: `CRM` as a wordmark, and the fields
written out (ХТО / ЗВІДКИ / ЧИМ ЗАЙМАЄТЬСЯ / ЩО ХОТІЛА / ЩО ЗРОБЛЕНО /
НАСТУПНИЙ КРОК). This does **not** contradict §4 — a wordmark *is* the logo
when no icon exists (§5b already ships Fathom and Gamma that way), and field
names are text inside a depicted interface, which §4 exempts by name. A CRM
with no field names is not a depicted CRM.

**3 · A graphic must not outstay its sentence — and she can see four seconds.**
Both directions, in the same review: *"took too long too"* (a waveform held 4 s
across two sentences it had nothing to do with) and *"literally one second wtf"*
(a tile that flashed and left). The fix is never to stretch one object across a
section; it is more, shorter events on the actual phrases.

**4 · Every object has to be nameable.** *"whats that little glowing dot?"* — a
dot travelling a wire to mean a booking is not an object, it is a dot. It became
a small event card with a header bar and a body line, which reads as an
appointment at 90 px. If a viewer would ask *what is that*, it is not finished.

**5 · A blank plaque says nothing.** §5a.9 likes an empty frosted slot before
the filled state, and that is still true *once the viewer knows what the slot
is for*. Six empty slots opening a reel got *"this is not really
understandable, at least add some logos/icons in"*. They now carry greyed-out
ghosts of the marks that will land in them: the board is readable from the
first frame and the reveal still happens, grey to lit.

**Greenscreen cutouts stay big.** Her call, 2026-09-29, on reel 18: when she is
cut out over a screen recording, keep her at ~60–70 % on the left, face above
y ≈ 1500 and left of x ≈ 880 — at 45 % in the bottom-right corner she was
*"eated by the buttons from ig interface"* (the like/comment/share rail and the
caption block).

**Proof is a screenshot.** Her call, 2026-09-29: Instagram stats, DMs, comments,
reviews go on screen as her real screenshots (cropped, blurred where personal),
never redesigned as glass cards — *"then people trust it more and dont think
that we came up with the numbers"*. Animate around the screenshot, don't retype it.

**No invented stats.** A view count, follower number or sum shown as *hers* must
be hers (from her screenshots or her words). Reel 20 shipped «1,2M» views on a
hype curve and on three reel cards; they were made up and would have read as her
real numbers, so they came out before delivery. Shape-only charts, or a clearly
labelled demo card (CRM, report), are fine.

And one literal, which is the kind of note she gives and means exactly: *"tasks
are always checks and lines like a checklist"* — a checkbox and a rule, never
three coloured bars.

### Her editing is not filler

> *"when you see some funny editing (extra closeup, extra far away) those are
> funny bits and dont paint over them"*
> *"i made it funne with editing there"*

A shot change in her delivered cut is an instruction. Those spans get captions
and nothing else. Two detectors run before authoring, because the two kinds look
nothing alike in the file:

| | |
|---|---|
| `tools/shots.py` | hard cuts, by scene detection, plus a contact sheet of one frame per shot. Her comedy inserts are the short ones — on reel 7, five gags of 0.6–1.5 s against a 4–44 s baseline |
| `tools/pullouts.py` | *zooms*, which scene detection cannot see at all. When she pushes the plate back, black appears at the frame edge, so border luminance against the reel's own median finds them |

The second exists because reel 7 had a 3.75 s pull-out at 11.0–14.7 s with a
beat sitting on top of it. Put every span in the build's `NO_PAINT` list, and
**delete** the beats that fall inside rather than nudging them — the words those
beats illustrated are inside the gag too.

---

## 5. Palette and type

```
--red       #b4122f    deep red, the workhorse
--red-deep  #8d0d24
--pink      #ff6e9c    the pop, and every glow
--ink       #17141c
--paper     #fdf1f4    card / takeover ground
```

Card and takeover backgrounds: **white → very light pink**. Never beige, never a
dark ground. Nothing outside this palette.
**Current palette: §00.6** — white and dark red `#7A1424` only. The burgundy
takeover ground of 2026-09-28 is archived (archive/STYLE-refined-glass.md); no
dark ground anywhere.

Font: **Google Sans** variable, self-hosted from `assets/fonts/GoogleSans.ttf`.
`wght 700` + `GRAD 200` is the heavy setting. Ukrainian coverage verified.

Glow, used on bright elements over footage:
```css
box-shadow: 0 0 64px rgba(255,110,156,0.5), 0 24px 54px rgba(8,6,12,0.5);
```
A `box-shadow` on a **transparent** div paints inside its own box and reads as a
muddy grey panel. For a real halo use a radial gradient instead.

---

## 5a. Surfaces — what makes a shape read as 2026 and not 2013

Added after reel 3 v1, which was correct in palette and layout and still read as
flat vector. The palette above says *which* colours; this section says how a
surface is built. It is the difference between a filled rectangle and a lit
object, and almost none of it is consciously visible.

**1 · Continuous-curvature corners.** The biggest invisible tell. `border-radius`
bolts a quarter-circle onto a straight edge and there is a break where they
meet. Use `tools/squircle.py` → `clip(w, h, r)`, which emits Figma's corner
smoothing at 60% as a `clip-path`. Verified to render, and `filter:
drop-shadow()` survives the clip where `box-shadow` would not — so a clipped
card takes its shadow from `filter`, not `box-shadow`.

> ⚠ **There is a budget, and blowing it turns the render black.** `lint` counts
> every element carrying `clip-path`, `filter: blur` or a `radial-gradient` —
> including hidden ones — and warns near ~36. Its field note: a composition with
> ~40 *"captures solid-black for the first ~half of the render, recovering near
> the end"*, identically across every capture path. Reel 4 hit 36 by squircling
> everything and had to be pulled back.
>
> So squircle the **large** surfaces only — cards, tiles, phones, panes, roughly
> `r ≥ 50` — and give small or repeated elements (bars, chips, list cells, wall
> tiles) a plain `border-radius`. At 138px wide with `r=34` the two are
> indistinguishable anyway, which §5a.2 already implies.

**2 · Concentric radii.** `inner = outer − padding`. A card at 44 with 16px
padding puts its children at 28, never at 44. Radius also scales with size: a
26px-tall bar and a 360px tile must not share one.

**3 · Bar rhythm.** Placeholder bars are the right abstraction for a reel, but
uniform width, height and spacing read as a *loading state*. Real text has
rhythm: one thick short heading bar at ~1.6× body height, then 3–4 thinner bars
at ragged lengths — 100%, 94%, 71%, 43%.

**4 · A tonal ladder, not two values.** Red-on-white is two values and reads
flat. Every card carries at least three steps of the same hue at low chroma,
with the true accent appearing **once**:

```
--surface         #fdf6f6    blush white, the card ground
--container       #f4dde2    a step down, for blocks inside it
--container-high  #ecc8d0    a step further, for nesting
--graphite        rgba(23,20,28,0.13)   body bars, cool and low
--accent          #b4122f    once per card, never twice
```

**5 · Never a flat fill.** A solid `#ffffff` reads as vector. Put a 2–4%
gradient across it at ~115° (`#ffffff → #fafafb`). Barely perceptible,
completely different feel.

**6 · Edge light, not an outline.** A uniform 1px stroke all the way round is
2013. Use a specular rim: bright on the top edge, almost gone at the bottom.

```css
box-shadow: inset 0 1.5px 0 rgba(255,255,255,0.92),
            inset 0 -1.5px 0 rgba(255,255,255,0.14),
            inset 0 0 0 1px rgba(255,255,255,0.28);
```

**7 · Ambient shadow, not drop shadow.** `0 4px 8px rgba(0,0,0,.15)` is Material
2013 — small, tight, dark. Modern is huge, soft and almost invisible, in two
layers:

```
contact  0 1px 2px  rgba(26,30,39,0.04)
ambient  0 24px 48px rgba(26,30,39,0.06)
```

Those alphas are for a light ground. Over her footage roughly double them or the
card detaches from nothing.

**8 · Break the rounded-rect monotony.** In a set of eight, one full circle, one
pill, one wide squircle. All-same-shape-different-length is why a grid reads as
texture instead of composition.

**10 · Glow sits *around* the object, not under it.** Her note on reel 4: *"it's
an overglow, not underglow, and i want it a bit stronger, not just as a
shadow."* A drop-shadow with an offset reads as the object sitting on a surface;
a glow is light coming **off** it, so the offset is zero and it wraps the whole
silhouette. Layer three — a tight core, a mid bloom and a wide falloff — or it
reads as a blurry outline rather than light:

```css
--glow: drop-shadow(0 0 10px rgba(255,196,218,0.95))   /* hot core */
        drop-shadow(0 0 26px rgba(255,110,156,0.85))   /* bloom    */
        drop-shadow(0 0 64px rgba(255,110,156,0.55))   /* mid      */
        drop-shadow(0 0 120px rgba(255,110,156,0.32)); /* falloff  */
```

The first layer is near-white on purpose. A glow that is the same pink all the
way through reads as a coloured outline; the thing that makes an object read as
*emitting* is a core hotter than its own colour. Four layers, not three: the
extra one is paying back the contrast that `var(--cast)` used to fake.

**Never chain `var(--cast)` after it.** That was the reel 4 mistake, and she
caught it twice: the cast is a dark pool 24px *below* the object, so the eye
reads the dark half first and the whole thing goes back to being an underglow no
matter how bright the light is. An object that emits light does not also sit on
a surface — pick one. `filter: var(--glow)`, full stop.

**Put the glow on a wrapper, never on the clipped element.** `clip-path` is
applied *after* `filter`, so a `drop-shadow` declared on the same element as the
clip is cut away with everything else outside the silhouette — the object ends
up with no light at all, and the beat looks like the glow simply failed. It did.
Clip the shape, filter its parent:

```html
<div class="lit">                       <!-- filter: var(--glow) -->
  <div class="tile brand">…</div>        <!-- clip-path: path(…)   -->
</div>
```

The parent filters the already-clipped bitmap, so the light traces the squircle
and survives. `.lit` is in the kit. Reserve it for the beat's subject —
everything glowing is nothing glowing.

**And never fake it with a `.halo` div.** A radial-gradient placed after the
element paints *over* it, washing the mark pink and reading as a soft blob
rather than emitted light. Reel 4's Mobbin tile had one, and it was doing all
the visible work while the real glow sat clipped and invisible underneath —
which is why removing the cast shadow alone did not fix her note.

The old `.halo` (a radial-gradient behind the element) is weaker and squarer;
prefer the filter. Keep the radial only where the light needs to exist
independently of an object, like a burst.

**11 · Emoji are images, never glyphs.** A literal `💩` in the HTML renders in
whatever emoji font the *render machine* has — Noto Color Emoji on the cloud
renderer, which is the Android look. Ruta wants the Apple set. So the artwork
lives in `assets/emoji/` as PNG and goes in through `Kit.emoji("poop")`, sized
by `height` in the beat's CSS rather than by `font-size`. Reel 5 shipped with
the glyph; that is the whole reason this rule exists.

**12 · A takeover pane has corners.** §5a.9 gives the frosted pane a 44/64px
margin so the footage reads past it — and then the corners have to be rounded or
it is just a rectangle laid over her, which is what reel 4 shipped. `.ground` is
squircled by `Kit.__init__` now, so no build can forget it. The general form:
the bigger the surface, the more a square corner costs, so the *largest* thing
on screen is the last place to economise on the clip-path budget.

**Motion.** The material has to react, or it is a flat fill that happens to be
moving. Glass picks up tint from whatever passes behind it; the specular streak
travels along the edge as a panel moves; radii stretch slightly on fast motion
and settle back.

**9 · Frost, and lots of it.** `backdrop-filter: blur() saturate()` renders
correctly, and it is the house look. Her note on reel 3 v2, about the two empty
plaques at 73s: *"I absolutely love when it was during the design skill / Mobbin
2 plaques."* Those are glass **over her live footage** — the kitchen blurring
softly inside the panel, with the rim catching light along the top edge. Use it
widely: empty slots, panels, cards, anything waiting to be filled.

```css
background: rgba(255,255,255,0.15);
-webkit-backdrop-filter: blur(24px) saturate(1.4);
backdrop-filter: blur(24px) saturate(1.4);
box-shadow: var(--rim);          /* §5a.6 — the rim is what sells it */
filter: var(--cast);             /* §5a.7 */
clip-path: <squircle>;           /* §5a.1 — clips the blur too */
```

**Margin is the whole distinction, not size or substrate:**

| | |
|---|---|
| a glass **panel** over footage | the house look — use it freely |
| an **inset glass pane** for a takeover | correct. Leave a real margin — 44px left/right, 64px top/bottom — so the room shows around it |
| an **edge-to-edge** frosted ground | **rejected.** With no margin it reads as a blur applied to the video, and it erases her (reel 3 v2) |

Her note: *"instead of bright red screen lets do glass, you can even let a bit of
margin on the sides show to really show that it's a glass on top and not just a
blur."* So a takeover is a **tinted** pane — the palette at ~0.62–0.70 alpha over
`blur(30px) saturate(1.5)` — not a fill. She stays visible moving behind it, and
white captions still read on the tint.

The pane needs a **lit rim** or it reads as a tinted rectangle rather than glass:

```css
box-shadow: inset 0 2px 0 rgba(255,255,255,0.70),
            inset 0 -2px 0 rgba(255,255,255,0.10),
            inset 0 0 0 1.5px rgba(255,255,255,0.30);
```

And drop the caption scrim while a pane is up (`SCRIM_OFF` in `build.py`) — the
caption already has a clean ground, so the scrim only shows through as a halo.

An empty frosted plaque is often better than the filled state that follows it —
so let it sit empty for a beat before the colour lands, rather than filling it
on arrival.

## 5b. Logos

She keeps brand marks in `assets/` (Fathom, Google Meet, Claude, ChatGPT, Notion,
Zoom, Reddit, Telegram — most in a `big` and a `short` variant). **Use the real
marks**; the abstract glyphs in v3 were a stopgap before she supplied them.

**Superseded 2026-09-28 (§0.2):** real marks, but **monochrome**, in the tile
family — `assets/icons/<slug>.svg` from simple-icons, set in `.clear`, `.pearl`
or `.jelly`. The colour PNGs below are for a beat where the brand colour *is*
the point, which is rare.

Handling notes, all learned the hard way:

- Most are **black-on-white, opaque**. That is fine — put them on **white node
  tiles** and the backgrounds disappear into the tile. Claude's is a coral
  rounded square and reads as its own brand tile; leave it.
- `fathom` and `meet` are **wordmarks**, not square icons — aspect 5:1 and 6.6:1.
  Their PNGs carry huge whitespace margins (Fathom's ink is only 403×80 inside a
  447×447 canvas). **Trim before use**, then build a wide node card around the
  wordmark rather than squeezing it into a square.
- To find the trim box, scan for non-white, non-transparent pixels — ffmpeg's
  `cropdetect` gives nothing useful on a single still.
- No CRM logo exists, and her script says «CRM-системи, що в тебе там є», so a
  drawn database glyph is correct there rather than a wrong brand.

## 5c. Shape rules that bit

- **A wide card tolerates almost no rotation.** At 620px wide, 5° throws the far
  end 54px and three stacked cards stop reading as a stack. Keep wide-card
  rotation under 3°.
- **A stack needs ~90px of offset per card** to read as separate objects. At 60px
  they merge into one white blob, especially with rotation.
- **White on grey needs a colour change, not more opacity.** The stall spinner
  was white on a grey wash and vanished; pink on a dark track reads instantly.

## 6. Superseded: the Edits + LIGHTEN constraint

Kept only in case loose overlay clips return. Edits cannot read alpha and fills
transparency with black; she composited with **LIGHTEN**, which keeps only pixels
brighter than the footage. White and pink survive; deep red goes translucent
(she liked that); dark fills and dark-on-light text vanish entirely.

---

## 7. Build and render

```bash
npx hyperframes check                 # must pass before rendering
npx hyperframes snapshot --at <times> --no-end -o study/snap
npx hyperframes cloud render          # the wallet; ~4-7 min
```

**Render in the cloud, on the API wallet.** The free HeyGen pool is 5 renders a
calendar month and it ran out on 2026-09-14 (HTTP 402 `insufficient_credit`).
Her call: *"why are we not using cloud? i put money in API"* — so the wallet is
the default path now, not a fallback. A render costs **$0.23-0.47** and takes
4-7 min against ~17 min locally. The CLI prefers an `oauth` block over the
stored `api_key`, which is why it was billing the free plan; park that block
under another name in `~/.heygen/credentials` and `auth status` reports
`Billing: wallet`. Local `render --low-memory-mode` is only for an empty wallet
or no network.

Always snapshot before rendering — a render is ~17 minutes and a snapshot pass is
under one. Verify the first frame, each beat's proof pose, and the exact final
frame.

**Machine limits** — Ryzen 7 3700U, no usable GPU, 15 GB RAM, disk usually near
full:
- `--low-memory-mode` is **mandatory**; default disk capture wants ~25 GB of temp
  frames and fails outright.
- Whisper `medium` is cached and handles Ukrainian well (~15 min per 2.5 min).
  `large-v3` is not cached and there is no disk for it.
- Never run heavy jobs in parallel — RAM pressure makes throughput worse than
  sequential.
- ffmpeg in this environment has **no glob support**; use numbered inputs.

---

## 8. How she gives feedback

Fast, specific and blunt — take it literally. She spots real bugs (a
mispositioned currency symbol, a hand that reads as detaching, a graphic that
duplicates her own subtitle). "A bit thin" means roughly double it. Show work
early; snapshots beat a long silent build.
