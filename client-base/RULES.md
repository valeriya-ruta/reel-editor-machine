# Reel editing base — the rules

**BASE LAYER: the same for every client.** This file is Ruta's STYLE.md from
`reel-editor-machine` with the look taken out: how pauses and bad takes are
found and cut, how text is sourced, the caption machinery, takeovers, safe
zones, the animation rule, what Ruta flags in review, build and render, sound.
Every rule here is copied from her repo or from her answers while building
Marina's editor (2026-11-05). **Nothing here is invented, and nothing here
changes per client.**

The client's look (palette, fonts, caption style, materials, rhythm, where
her refs put things) is in `LOOK.md` + `tools/look.py`. Where the two
disagree, `LOOK.md` wins only on the look, and only for what it names.

The run never stops to ask: it decides from these two files, the transcript
and the refs, and reports its calls at the end.

**Cutting rule (Ruta, 2026-11-05):** the reel stays **under 3 minutes**. Cut
**only pauses and bad takes**, following Ruta's instructions and the
transcript. **Never cut content.** No length targets.

**Transcription:** local whisper (`tools/utt.py`), OpenRouter whisper as the
fallback. **Never ElevenLabs**, and not the video-use skill.

---

## 1. The delivery model and the cut (Ruta's repo, as is)

Ruta drops the client's **raw take** into `raw/`. This folder cuts it, captions
it, animates it and renders it, with Ruta's raw-take pipeline from
`reel-editor-machine` (reels 21–40): `tools/utt.py` → `tools/cut.py` →
`tools/align.py` → `build.py` → cloud check → cloud render → verify.

**Cutting rule (Ruta, 2026-11-05):** the reel stays **under 3 minutes**. Cut
**only pauses and bad takes**, following Ruta's instructions and the
transcript. **Never cut content.**

How the cut finds them (Ruta's `tools/cut.py`, as is):

- **Pauses — from the audio and from the transcript** (Ruta, 2026-11-05:
  "both audio and transcript, because if there's wind there might not
  necessarily be actual audio silence"). `tools/utt.py` runs ffmpeg
  `silencedetect` (−30 dB, 0.18 s) and transcribes each spoken span on its
  own. Inside a span, `cut.py` also splits wherever the transcript shows a gap
  between two words longer than 0.30 s, so a pause full of wind still goes.
  Whisper stretches a word over a pause; a word much longer than she takes to
  say it is trimmed the same way the clip edges are. Every utterance keeps
  0.07 s before / 0.10 s after, and a removed pause leaves 0.16 s of air
  (0.30 s after a full stop).
- **Bad takes — the transcript is the script** (Ruta, 2026-11-05). Last take
  wins (Ruta's rule, 2026-10-05): when a line is fumbled and said again, every
  earlier attempt goes. `tools/takes.py NN` lists every place she starts the
  same words again; read them against the transcript (many are her repeating
  on purpose, which is content and stays), then write `work/rNN/script.txt` =
  the transcript with the fumbled earlier attempts deleted. `cut.py` aligns
  every word to it with a Viterbi pass that may jump back; a backward jump is
  a restart and the earlier attempt is dropped. A restart that would drop more
  than 40 words is flagged in `cut.txt`, not cut.
- **Manual calls:** `work/rNN/cut-fix.json` — `drops` / `keeps` (raw seconds),
  `punch` (a closeup), `face`. Ruta's instructions go here.
- **Framing:** never the same crop twice across a cut, pure scale steps
  centred on her (base 1.00 / in 1.10), a clip over 5.5 s gets a zoom cut
  inside, `punch` 1.50 for a joke.
  Punch spans become `no_paint`: captions only.

**Matte her per beat, never per reel** (Ruta's repo, as is): `tools/matte.py`
for a big object behind her, one beat at a time.

---

## 2. Text: where it comes from (Ruta's repo, as is)

**Spelling** comes from her transcript / script in `work/rNN/script.txt`,
never from speech recognition alone. **Captions are what the client said,
verbatim**, her surzhyk kept. Whisper supplies timing; its mishearings are
fixed through a `FIX` dict in `build.py`, as in Ruta's reels.

---

## 2b. Captions: the machinery (Ruta's repo, as is)

How a caption *looks* (font, size, height, case, one word / a phrase / typing
on) is the client's, in `LOOK.md` §2b and `tools/look.py`. How captions are
timed, dropped and inverted is the base, below, and the same for everyone.

Known caption bugs to guard against (Ruta's repo, as is): a word straddling a clip start gets clipped (clamp it), `%` splits off its number (merge), a leading apostrophe breaks «інтерв'ю» (merge), a leading hyphen survives into the token (`lstrip("-")`), and consecutive blocks superimpose for ~1.5 frames (clamp `end = next.start − 0.085`).

### 2b.1 When captions drop, and when they invert (Ruta's repo, as is)

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

---


## 2c. Takeovers (Ruta's repo, as is; the grounds are the client's)

Her four reference reels (`Examples/`) all make the same structural argument,
and it is not about polish: **the graphic owns the frame or it is not there.**
None of them float a card over footage. They alternate — footage with a short
phrase on it, then no footage at all.

What a takeover is, mechanically: a `.g.full` whose first child is an opaque
ground (`.tk.*`, the client's grounds from `LOOK.md` §5a). The plate is gone, so **none of the over-footage rules apply** —
no glow budget, no band discipline, ink type on a light ground, and the
heavy-overlay element ceiling does not bite.

Rules learned building reel 9's five:

- **Bleed off at least two edges.** A takeover composed inside the frame with
  margins reads as a slide, not a takeover. Mark the elements
  `data-layout-allow-overflow` so the layout checker stops flagging them.
- **The ground belongs to the beat that starts first and must outlive every
  other part of the takeover.** Reel 9's paper lived on the wrapper carrying
  the Canva/Slides marks; fading that wrapper when the marks had said their
  piece put her footage back behind the wall for the whole push-in. Fade the
  *children*, keep the ground.
- **Transforms only.** `width`, `height` and `margin` are layout properties:
  the linter rejects them and they snap to integer device pixels mid-tween. A
  typing reveal is `clipPath: inset(...)`; a band that fills the frame sits at
  its *resting* size and scales **up**, so a 26px radius stays 26px instead of
  stretching into a 260px ellipse.
- **Solve push-ins, don't eyeball them.** To bring point `p` to centre `c` at
  scale `k`, the wrapper offset is `c - (c + (p - c)k)`.
- **Use the whole frame when captions are blacked out.** TK4's brandbook first
  sat in the top half with 800px of dead paper under it, because it had been
  laid out around a caption band that was not going to be there.



## 3. Safe zones: where nothing goes (Ruta's rules, as is)

Collected from Ruta's repo and the client builds. These hold for every client;
the client's `LOOK.md` §3 only adds where *her* refs put things.

- **Never on her face.** Ruta: *"lets not do it as much on my face, you can
  put it lower"*. Text and graphics never cover her face or hands; when a
  graphic will not fit above her head, drop it **low over her chest** instead.
  The band rule loses to her face every time. Her head position is measured
  on the first cut (`cut.json` `face`), never assumed.
- **Behind her head, with a matte**, for a big object (§1, `tools/matte.py`),
  one beat at a time.
- **Never in a corner.** Every graphic is horizontally centred and wide,
  600–900 px (*"I want them to be centered… and wider, more rectangle"*).
- **Instagram's own UI.** The like/comment/share rail on the right and the
  caption block at the bottom eat whatever sits there (*"eated by the buttons
  from ig interface"*). Greenscreen cutouts: keep her ~60–70 % big, face above
  y ≈ 1500 and left of x ≈ 880.
- **Captions sit on her chest**, off her face and hands, at the height the
  client's refs use (`LOOK.md` §2b).
- **A takeover owns the whole frame**, so none of the over-footage zones
  apply to it (§2c).
- **Her editing is not filler**: closeups / pull-outs are `NO_PAINT`,
  captions only (§4a).

---

## 4. The animation rule (Ruta's repo, as is)

**Where a client's refs differ, the client's `LOOK.md` §4 says so.** For
Marina, Ruta's answer (2026-11-05) was "Marina's refs win": words allowed in
graphics, something new every ~2–4 s. A client's LOOK.md §4 may only override
this section with what Ruta or the client said, or what the client's own refs
measurably do; otherwise everything below stands as Ruta wrote it.

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
  (Since §0.8 the plate may push in slowly and the burgundy ground's light
  pools may drift; graphics still land and stay put.)
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

## 4a. What she flags in review (Ruta's repo, as is)

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


## 7. Build and render (Ruta's repo, as is)

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


## 8. How she gives feedback (Ruta's repo, as is)

Fast, specific and blunt — take it literally. She spots real bugs (a
mispositioned currency symbol, a hand that reads as detaching, a graphic that
duplicates her own subtitle). "A bit thin" means roughly double it. Show work
early; snapshots beat a long silent build.

---

## 9. B-roll and sound (Ruta's rules, as is)

**B-roll** (Ruta, 2026-11-05): the client's b-roll (usually her Google Drive)
is catalogued once, in `broll/CATALOG.md` (what each clip shows, where it
is, length, orientation), so a reel run picks from the catalogue instead of
sorting footage every time. How the client's refs use b-roll is in `LOOK.md` §9.
Only her real footage and photos; if nothing fits, the beat is type, not b-roll.

**Sound effects** (Ruta, 2026-11-05: "basic sound effects should be
included (typing, whooshing etc)"): the kit is in `assets/sfx/`
(`tools/sfxkit.py` made it: click-soft, click, key-press, typing, pop,
whoosh-short, whoosh, ping, notification, sparkle, kaching). Cues and levels
are Ruta's (`tools/sfx.py`, her batch brief): quiet, on the event, never on a
closeup, about 0.5 cues a second at most. A recorded file with the same name
dropped into `assets/sfx/` replaces the synthesised one.
