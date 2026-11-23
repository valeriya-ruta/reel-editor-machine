# Generates index.html for the «Проєкт твого життя» reel.
# Beat table below is the edit; re-run this after changing it.
#   python build.py
import io, sys, json
sys.stdout.reconfigure(encoding="utf-8")

W, H, FPS, DUR = 1080, 1920, 30, 55.0

# ---------------------------------------------------------------- source clips
# index -> (proxy file, source duration). Swap the file to swap the shot.
CLIPS = {
     1: ("c01.mp4",  6.69),   2: ("c02.mp4",  2.04),   3: ("c03.mp4",  3.46),
     4: ("c04.mp4",  2.31),   5: ("c05.mp4",  4.63),   6: ("c06.mp4",  8.13),
     7: ("c07.mp4",  4.22),   8: ("c08.mp4",  9.30),   9: ("c09.mp4", 13.21),
    10: ("c10.mp4", 16.57),  11: ("c11.mp4",  7.57),  12: ("c12.mp4", 14.31),
    13: ("c13.mp4", 25.58),  14: ("c14.mp4",  2.71),  15: ("c15.mp4",  6.35),
    16: ("c16.mp4",  7.75),  17: ("c17.mp4",  7.94),  18: ("c18.mp4", 26.88),
    19: ("c19.mp4",  5.67),  20: ("c20.mp4",  7.01),  21: ("c21.mp4", 24.60),
    22: ("c22.mp4", 69.77),  23: ("c23.mp4",  4.49),  24: ("c24.mp4",  8.58),
    25: ("c25.mp4",  8.13),  26: ("c26.mp4",  7.12),
}

# ------------------------------------------------------------------- the edit
# (clip_index, cut_in, cut_out, media_start)
CUTS = [
    # S1 HOOK 0.00-6.70  «Що буде, якщо поставитись до власного життя…»
    ( 1, 0.00,  2.40, 0.40), (26, 2.40,  4.30, 1.00),
    (10, 4.30,  5.60, 4.00), (11, 5.60,  6.70, 2.00),
    # S2 CHAOS -> SYSTEM 6.70-12.56
    (19, 6.70,  7.55, 0.60), ( 4, 7.55,  8.35, 0.20),
    ( 3, 8.35,  8.96, 0.60), ( 2, 8.96,  9.80, 0.20),
    (22, 9.80, 11.05, 8.00), (10,11.05, 12.56, 9.00),
    # S3 WHERE YOU'RE GOING 12.56-16.42
    (24,12.56, 13.86, 1.20), (17,13.86, 14.90, 1.50),
    (14,14.90, 15.60, 0.30), (19,15.60, 16.42, 2.60),
    # S4 GOALS + PRIORITY 16.42-21.06
    ( 9,16.42, 17.30, 3.00), (13,17.30, 18.20, 6.00),
    (12,18.20, 19.20, 4.00), (20,19.20, 20.20, 1.20),
    (15,20.20, 21.06, 0.80),
    # S5 BALANCE 21.06-25.82
    (21,21.06, 22.10, 5.00), ( 8,22.10, 23.10, 2.00),
    (15,23.10, 23.96, 3.00), ( 7,23.96, 24.90, 0.40),
    (16,24.90, 25.82, 1.50),
    # S6 DISCIPLINE 25.82-29.72
    (22,25.82, 26.80,20.00), (11,26.80, 27.60, 4.00),
    (10,27.60, 28.40,12.00), (13,28.40, 29.72,14.00),
    # S7 NOT LAZY -> MANAGER 29.72-36.64   (the peak)
    ( 6,29.72, 30.90, 1.00), ( 8,30.90, 31.94, 5.00),
    ( 1,31.94, 33.20, 2.60), (22,33.20, 34.30,40.00),
    (10,34.30, 35.50, 0.50), (26,35.50, 36.64, 3.00),
    # S8 LIFE IS A PROJECT 36.64-44.40
    (18,36.64, 37.60, 4.00), ( 2,37.60, 38.40, 0.60),
    (21,38.40, 39.50,14.00), (24,39.50, 40.30, 5.00),
    (12,40.30, 41.60, 9.00), (10,41.60, 42.50, 6.00),
    (18,42.50, 43.40,14.00), (20,43.40, 44.40, 4.00),
    # S9 THE TURN 44.40-48.48
    ( 6,44.40, 45.60, 4.00), (16,45.60, 46.80, 4.00),
    (23,46.80, 47.60, 0.60), (20,47.60, 48.48, 5.60),
    # S10 CTA 48.48-55.00
    (26,48.48, 50.50, 0.20), ( 1,50.50, 52.50, 3.40),
    ( 6,52.50, 55.00, 5.20),
]

# ------------------------------------------------------------------ typography
# Each entry: (role, text, start, end, opts)
# roles: hero | paren | caption | spine | strike
T = [
    # --- S1 --------------------------------------------------------------
    ("caption", "що буде,",            0.00,  1.26, {}),
    ("hero",    "ЯКЩО",                1.26,  6.70, {}),
    ("paren",   "(життя)",             2.76,  6.70, {}),
    ("caption", "так само серйозно",   3.64,  5.00, {}),
    # --- S2 --------------------------------------------------------------
    ("caption", "може статись, що",    6.70,  7.54, {}),
    ("hero",    "ХАОС",                7.54, 11.08, {}),
    ("strike",  "коли справ менше",    9.20, 11.02, {}),
    ("hero",    "СИСТЕМА",            11.08, 12.56, {}),
    # --- S3 --------------------------------------------------------------
    ("caption", "може статись, що",   12.56, 13.40, {}),
    ("hero",    "КУДИ ЙДЕШ",          14.34, 16.42, {"size": 138}),
    ("strike",  "просто встигаєш",    15.28, 16.42, {}),
    # --- S4 --------------------------------------------------------------
    ("hero",    "ЦІЛІ",               16.66, 21.06, {}),
    ("caption", "не колись — тепер",  17.28, 18.60, {}),
    ("paren",   "(і себе)",           19.70, 21.06, {}),
    ("spine",   "пріоритет",          20.14, 25.82, {}),
    # --- S5 --------------------------------------------------------------
    ("hero",    "БАЛАНС",             21.20, 25.82, {}),
    ("strike",  "менше роботи",       22.10, 23.90, {}),
    ("paren",   "(твій вибір)",       23.96, 25.82, {}),
    # --- S6 --------------------------------------------------------------
    ("hero",    "ДИСЦИПЛІНА",         26.18, 29.72, {"size": 124}),
    ("strike",  "насильство над собою",27.56, 29.20, {"size": 44}),
    ("paren",   "(опора)",            29.26, 29.72, {}),
    # --- S7  peak --------------------------------------------------------
    ("caption", "і виявляється, що",  30.28, 31.90, {}),
    ("hero",    "ЛІНИВОЮ",            31.94, 33.90, {"strike": True}),
    ("caption", "ти просто ніколи не була",  32.98, 34.20, {}),
    ("hero",    "МЕНЕДЖЕРКОЮ",        34.30, 36.64, {"size": 112}),
    ("paren",   "(власного життя)",   35.04, 36.64, {}),
    # --- S8 --------------------------------------------------------------
    ("hero",    "ЖИТТЯ = ПРОЄКТ",     37.32, 40.28, {"size": 116}),
    ("caption", "найдовший з усіх",   38.72, 40.10, {}),
    ("spine",   "проєкт",             37.32, 44.40, {}),
    ("role",    "замовниця",          41.70, 44.40, {"slot": 0}),
    ("role",    "менеджерка",         42.56, 44.40, {"slot": 1}),
    ("role",    "команда",            43.36, 44.40, {"slot": 2}),
    # --- S9 --------------------------------------------------------------
    ("caption", "а що,",              44.40, 44.88, {}),
    ("hero",    "ЯКЩО",               44.88, 48.48, {}),
    ("strike",  "пообіцяти собі",     46.12, 47.50, {}),
    ("paren",   "(а зробити)",        47.62, 48.48, {}),
    # --- S10 CTA ---------------------------------------------------------
    ("hero",    "ПРОЄКТ",             48.48, 55.00, {"y": 620}),
    ("paren",   "(твого життя)",      49.04, 55.00, {"y": 770}),
    ("caption", "третя група — вересень", 49.86, 51.20, {}),
    ("caption", "анкета в шапці профілю", 51.22, 55.00, {}),
]

# inset cards: (clip_index, start, end, media_start)
INSETS = [
    (10,  4.90,  6.70, 6.0),   # «до робочого проєкту» — work inside the calm shot
    (18, 42.60, 44.40, 8.0),   # «команда» — crowd inside the frame
]

# ------------------------------------------------------------------ emit HTML
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

out = io.StringIO()
w = out.write

w(f'''<!doctype html>
<html lang="uk" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
  @font-face {{
    font-family: "InterVar";
    src: url("assets/fonts/Inter.ttf") format("truetype-variations");
    font-weight: 100 900;
    font-style: normal;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
  body {{ font-family: "InterVar", Inter, sans-serif; -webkit-font-smoothing: antialiased; }}

  video.base {{
    position: absolute; inset: 0;
    width: {W}px; height: {H}px; object-fit: cover;
  }}

  /* every type layer is a full-frame block; position comes from padding */
  .t {{
    position: absolute; left: 0; width: {W}px;
    text-align: center; color: #fff;
    text-shadow: 0 2px 28px rgba(0,0,0,.34);
  }}
  .hero {{
    font-variation-settings: "wght" 900;
    font-size: 168px; line-height: .96;
    letter-spacing: -.035em; text-transform: uppercase;
  }}
  .paren {{
    font-variation-settings: "wght" 350;
    font-size: 104px; line-height: 1;
    letter-spacing: -.01em;
  }}
  .caption {{
    font-variation-settings: "wght" 500;
    font-size: 46px; line-height: 1.25; letter-spacing: .005em;
  }}
  .strike {{
    font-variation-settings: "wght" 500;
    font-size: 50px; line-height: 1.2;
    text-decoration: line-through;
    text-decoration-thickness: 5px;
    text-underline-offset: 0;
  }}
  .hero.struck {{
    text-decoration: line-through;
    text-decoration-thickness: 14px;
  }}
  .rolerow {{
    font-variation-settings: "wght" 800;
    font-size: 76px; line-height: 1; letter-spacing: -.02em;
    text-transform: lowercase;
  }}
  /* rotated spine — block-level and explicitly sized, per the determinism rules */
  .spine {{
    position: absolute; display: block;
    width: 620px; height: 70px;
    top: 940px; left: 560px;
    transform: rotate(90deg); transform-origin: 50% 50%;
    font-variation-settings: "wght" 650;
    font-size: 44px; line-height: 70px;
    letter-spacing: .16em; text-transform: lowercase;
    color: #fff; text-align: center;
    text-shadow: 0 2px 20px rgba(0,0,0,.4);
  }}
  .inset {{
    position: absolute; left: 132px; top: 700px;
    width: 640px; height: 440px; object-fit: cover;
    box-shadow: 0 26px 70px rgba(0,0,0,.5);
  }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}"
     data-width="{W}" data-height="{H}">

  <audio id="vo" src="assets/VO.wav" data-start="0"></audio>

''')

# --- base track (track 0)
w("  <!-- base footage -->\n")
for i, (ci, a, b, ms) in enumerate(CUTS):
    f, sdur = CLIPS[ci]
    dur = round(b - a, 3)
    ms = min(ms, max(0.0, sdur - dur - 0.05))
    w(f'  <video class="clip base" data-start="{a:.2f}" data-duration="{dur:.2f}" '
      f'data-media-start="{ms:.2f}" data-track-index="0" '
      f'src="assets/clips/{f}" muted></video>\n')

# --- inset cards (track 1)
w("\n  <!-- inset cards -->\n")
for n, (ci, a, b, ms) in enumerate(INSETS):
    f, sdur = CLIPS[ci]
    dur = round(b - a, 3)
    ms = min(ms, max(0.0, sdur - dur - 0.05))
    w(f'  <video class="clip inset" data-start="{a:.2f}" data-duration="{dur:.2f}" '
      f'data-media-start="{ms:.2f}" data-track-index="1" '
      f'src="assets/clips/{f}" muted></video>\n')

# --- typography (tracks 2+)
YS = {"hero": 300, "paren": 452, "caption": 1215, "strike": 1300}
w("\n  <!-- typography -->\n")
for n, (role, text, a, b, o) in enumerate(T):
    dur = round(b - a, 3)
    if dur <= 0:
        continue
    if role == "spine":
        w(f'  <div class="clip spine" data-start="{a:.2f}" data-duration="{dur:.2f}" '
          f'data-track-index="4">{esc(text)}</div>\n')
        continue
    if role == "role":
        top = 1330 + o["slot"] * 96
        w(f'  <div class="clip t rolerow" data-start="{a:.2f}" data-duration="{dur:.2f}" '
          f'data-track-index="5" style="top:{top}px">{esc(text)}</div>\n')
        continue
    cls = f"clip t {role}"
    if o.get("strike"):
        cls += " struck"
    top = o.get("y", YS[role])
    size = o.get("size")
    style = f"top:{top}px"
    if size:
        style += f";font-size:{size}px"
    w(f'  <div class="{cls}" data-start="{a:.2f}" data-duration="{dur:.2f}" '
      f'data-track-index="{2 if role in ("hero","paren") else 3}" '
      f'style="{style}">{esc(text)}</div>\n')

w(f'''
</div>

<script>
  // The reference eases nothing: every element pops in hard on its word and
  // holds. Clip windows do that natively, so the timeline only carries length.
  const tl = gsap.timeline({{ paused: true }});
  tl.to({{}}, {{ duration: {DUR} }});
  window.__timelines["main"] = tl;
</script>
</body>
</html>
''')

open("index.html", "w", encoding="utf-8").write(out.getvalue())
print(f"index.html written: {len(CUTS)} cuts, {len(T)} type events, {len(INSETS)} insets")
print(f"last cut ends {CUTS[-1][2]:.2f}s / duration {DUR}s")
