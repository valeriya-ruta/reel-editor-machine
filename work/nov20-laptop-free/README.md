# 2026-11-20 — "edit without a laptop" (one-take proof reel)

Source: Drive `20261120_142801.mp4` (7:36, 4K HEVC 60fps, 3.47 GB). Output 2:56.

Her brief: no animations, only cuts + subtitles, under 3 min, must not look rigged.

- `plan.json` — [src_start, src_end, speed]. Talk at 1.2x. Upload wait (68–275s) is a 5 s fast-forward.
  Cuts only before she hits send and in the CTA; 346–426s (Claude working, laptop closed) has no cuts,
  pauses are 3x fast-forwards. Fast-forwards are muted.
- `captions.json` — tools/align.py on a large-v3-turbo pass, script spelling from `script.txt`.
- `subs.ass` — Product Sans Black 64px, white, soft dark halo, pos (800,400): small and upper-right,
  clear of the phone she holds up to the lens. Burn: `ffmpeg -i cut.mp4 -vf ass=subs.ass:fontsdir=<dir with ProductSans-Black.ttf>`.
- `tools/` — the cloud-side scripts used (plan / per-segment render / subs / faster-whisper).

## Final look: iced americano captions (her idea, 2026-11-20)
- `cup-layer.png`: a full-frame 1080x1920 overlay with the cup cut out (rembg isnet) from her reference image, which had a fake checkerboard background. Upright, -6° tilt, 270 px tall, top-left at (70,113), soft contact shadow.
- `subs_cup.ass`: Product Sans Black, ASS size 74 (= PIL 58; the ASS size is the win-ascent+descent box, 1.272 em). `\an4` at (130,286), word starts about 30% into the cup and runs out to the right, plus a blurred black shadow layer at 57% opacity.
  The tops of the letters sit right on the 250 px top safe line; the cup pokes above it on purpose.
- Burn: `ffmpeg -i cut.mp4 -i cup-layer.png -filter_complex "[0:v][1:v]overlay,ass=subs_cup.ass:fontsdir=<fonts>"`.
