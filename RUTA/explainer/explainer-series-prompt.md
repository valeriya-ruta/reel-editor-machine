# Build: "AI evolution" explainer reels in ruta-editor

You're working in my ruta-editor repo (Remotion). Build a reusable system that renders short vertical explainer reels from an episode spec file. I attached `prompt-to-skill.html` — a GSAP prototype I approved. Match its look and camera behaviour, but rebuild everything properly as Remotion components (ignore its hand-placed misalignments).

## The format
- Ukrainian-language reels, 9:16, 1080×1920, 30 fps, **target 40–50 seconds, never over 58**. At ~140 words a minute that's 95–115 words of voiceover per episode, so keep each step's VO to one or two short sentences (~15–20 words).
- Each episode is an "evolution ladder" for one specific creator task: 5–6 steps. Each step = an action ("you do X") → a minus ("but Y") → the minus pushes you to the next step. The last step is the modern AI setup, with no minus.
- No intro, no outro. Frame 1 is already the first step in motion. Ends on the final state.
- Doom-scroll pacing: **the camera never holds one framing longer than ~1.5s**. Alternate big/small constantly: close-up → pull back → punch in → whip to another object.

## Visual style (from the prototype)
- Clean, cute, slightly rendered: soft gradients and shadows, rounded shapes. No hand-drawn/sketchy lines.
- White/very light grey background with a subtle floor.
- Two worlds:
  1. **Real UI = crisp:** a simplified Claude interface (cream `#FAF9F5`, terracotta `#D97757` accent, serif greeting, input box with send button), on a laptop and on a phone.
  2. **Metaphor objects = shaded "physical" things:** prompt = pink paper (`#FBC4D4` range), saved prompts = yellow folder (`#F7BF22` range), skill = glossy pink card with a dark round «/» stamp, devices = dark grey/aluminium.
- Captions on top (top ~8–22% of frame), Onest 800, dark text, key word on a yellow marker (`#FDE293`). Keep the bottom third clear.
- Character: a chibi version of me, defined in `chibi-ruta-prompt.md` with reference images `chibi-ref-single.png`, `chibi-ref-sheet.png`, `chibi-ref-over-the-top.png` (ignore the placeholder in the prototype). She is an actor only — she never speaks, no speech bubbles. She appears in "human" beats with big, over-the-top emotions (frustrated, crying waterworks, furious, ecstatic, grabbing the phone, coffee at the end). Generate the poses each episode needs with that kit (OpenRouter, `google/gemini-3.1-flash-image`), cut them out to transparent PNGs in `chibi/<pose>.png`, and reuse existing poses before generating new ones. Build her as a component that swaps pose PNGs and adds a little life (squash-and-stretch pop on pose change, gentle idle bob, shake on angry/crying).

## Architecture
1. **Camera:** one `World` container with a camera (x, y, zoom). Named shot presets: `input_close`, `screen`, `object_punch(target)`, `room`, `character_close`, `phone_dive`. Transitions: `whip` (fast move + short motion blur), `pull_back`, `follow(object)`, `cut`. Ease in-out by default.
2. **Object library:** laptop with Claude window (typing, select, minimize/restore), phone with Claude mobile (typing, tap ripple, bottom sheet, chat bubbles), paper (pop out, fold/unfold, fly to target), folder (open/close, gulp), skill card + «/» stamp slam with micro-shake, cable connector between two app tiles (plug-in animation), app tiles with a name label (Fathom, ClickUp, Canva, Instagram, Notes…), task cards popping into a list, reel thumbnail grid, notes pile, spreadsheet, slide stack (carousel), video timeline with cuts, cloud upload, price tag, design-system card. Add others an episode needs, in the same style.
3. **Episode spec:** one JSON (or TS) file per episode in `episodes/`. Each step has `caption` (short, with the key word marked like `*скіл*`), `vo` (voiceover text), and `beats` (list of `{action, args, shot}`), plus an optional `minus` block with the same fields. Add a validator: unknown actions, missing fields, estimated duration > 58s → error.
4. **Timing is voice-driven:**
   - **Mode A (no audio yet):** estimate each beat's duration from its `vo` text (Ukrainian narration ≈ 2.5 words/sec), clamp shots to 0.8–1.6s, and add transitions.
   - **Mode B:** given `audio.mp3` + a word-timestamps JSON (ElevenLabs "with timestamps" output, or Whisper), align every beat and caption to its words. Captions switch exactly on the spoken words.
   - If an episode runs over 58s, shorten transitions and holds first; never cut the voiceover. Print a warning.
5. **Render:** `npm run episode -- <id>` → MP4, **H.264** (not HEVC). Each episode should also preview in Remotion Studio.

## The 5 episodes
Draft the captions and VO in simple Ukrainian as placeholders (mark them `TODO-TOV` — I'll rewrite them in my voice). Steps:

**1. editing**
1. Record on the phone and post raw → pauses and stumbles, people scroll.
2. Edit by hand: cut pauses, add subtitles and animations → 2 hours per reel, can't post daily.
3. Hire an editor → too expensive while the blog doesn't earn.
4. Set up an AI editor → doesn't know your style, keeps repeated words, the pace is off.
5. Describe your style once as a skill → rendering kills your old laptop.
6. Everything runs in the cloud: record on Monday, reels are ready while you drink coffee.

**2. content-analysis**
1. Scroll your reels and guess what worked → memory lies.
2. Copy the numbers into a spreadsheet → an hour of work, numbers without context.
3. Paste the numbers into Claude → it doesn't know what each reel was about.
4. Connect Instagram stats + your scripts (connectors) → you still have to ask every time.
5. Make it a skill /аналіз → you forget to run it.
6. Weekly routine: every Monday a report on what to repeat and what to drop.

**3. content-ideas**
1. You want to record but stare at a blank page → nothing comes.
2. Save ideas in notes and save reels on Instagram → the notes become a graveyard, the saves get too big to look through.
3. Ask AI for ideas → generic, and it sounds unnatural in Ukrainian.
4. Give it your brand, audience and examples of good reel scripts → better, but it doesn't sound like you.
5. Teach it your voice → you explain the same thing every time.
6. Make it a skill → a reel-script skill that writes in your voice.

**4. carousels**
1. Make the carousel in Canva by hand → takes forever.
2. Make a template → you still write all the text.
3. AI writes the text → doesn't sound like you.
4. Teach it your voice → you still have to do the design.
5. Ask Claude to design it → ugly, different every time, forgets in every new chat.
6. Design system + skill → every carousel in your style, exportable to Canva.

**5. calls**
1. You keep forgetting what you talked about on a call → (problem opens the episode).
2. Take notes during the call → you lose focus and forget your questions.
3. Record the calls → you have to rewatch the whole thing.
4. Connect Fathom to Claude → you still write tasks and offers by hand.
5. Skill: after a call, tasks go into ClickUp and an offer draft is ready.

## Order of work
1. Camera + shot presets + the prototype's objects, rebuilt cleanly.
2. Spec format + validator + Mode A timing.
3. Build **episode 5 (calls)** end to end first and render it. Stop and show me before doing the rest.
4. Then the other four, adding any objects they need.
5. Mode B (audio alignment) once I give you the first voiceover file.

Keep everything data-driven: a new episode should only ever need a new spec file, never new animation code, unless it introduces a new object.
