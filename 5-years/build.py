# -*- coding: utf-8 -*-
"""5 years together: cut one part from the raw recording and dress it.

    python 5-years/parts.py        # spans -> work/5y/spans.json
    python 5-years/build.py 1      # -> work/5y/out/5-years-part-1-preview.mp4

What it does, all of it her brief for part 1 (2026-10-22):
  * straight cuts from the raw file, each edge moved to where the audio
    actually goes quiet; when in doubt it keeps silence rather than cutting
    into a word ("better to keep a bit more silence that i can cut manually")
  * wide / close (1.3x) alternating per shot, long takes split at a pause
  * a white flash into each new topic question, hard cuts everywhere else
  * Ukrainian subtitles at half her usual size, in her caption band
  * a doodle sticker with the question over their heads (UA big, EN small)
  * 5 s of the take running on, muted, blurred, under a white haze, with
    "2 more parts, follow" on it

Preview quality (540x960) until she approves the edit.
"""
import json, os, subprocess, sys, wave
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cards

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK = os.path.join(ROOT, "work", "5y")
RAW, WAV = os.path.join(WORK, "raw.mp4"), os.path.join(WORK, "audio.wav")
FONTS = os.path.join(ROOT, "assets", "fonts")
OW, OH = 540, 960                       # preview; 1080x1920 for the final
FPS_N, FPS_D = 30000, 1001
FPS = FPS_N / FPS_D
WORDS = json.load(open(os.path.join(WORK, "words.json"), encoding="utf-8"))["words"]

# ------------------------------------------------------------------ cut edges
# Where a span's rough edge lands mid-word, name the word it starts or ends on
# (nearest match), or give the time of the speech edge where Whisper has no
# usable word (the intro's first line; «connasse», heard as one 7 s «of»).
OVR = {25.9: (25.9, "індії"), 79.6: ("where", None), 371.9: (None, "words"),
       385.0: (None, "words"), 412.6: (None, "specifically"), 419.8: ("the", None),
       475.6: (None, 489.2), 238.1: (None, "me"), 257.3: ("i", None),
       280.4: ("i", None), 291.9: (None, "fully"), 331.5: (None, "work"),
       353.8: (353.8, None), 646.9: ("what", "us"), 655.1: (None, "one"),
       680.4: (None, "freedom"), 715.6: (None, "well"), 730.7: (None, "there"),
       741.4: ("there", "eats"), 753.5: ("i", None), 780.2: (None, "crime"),
       873.1: ("she", "like"), 898.5: ("i", None), 935.4: ("i", None),
       987.6: (None, "cuisine"), 991.3: (None, "vareniki"), 995.3: ("i", "fantastic"),
       1042.5: (None, "delicious"), 782.7: ("in", 807.0), 811.4: (None, "months"),
       1082.5: ("say", 1083.4)}

THR = -32.0       # dBFS; her noise floor sits near -40, speech near -19
QUIET = 8         # 80 ms under THR counts as a pause, not a stop consonant
LEAD = 0.22       # silence kept before the first word
TAIL = 0.35       # silence kept after the last word


def envelope():
    with wave.open(WAV) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    hop, win = 160, 480                                  # 10 ms hop at 16 kHz
    n = (len(x) - win) // hop
    frames = np.lib.stride_tricks.sliding_window_view(x, win)[::hop][:n]
    db = 20 * np.log10(np.sqrt((frames ** 2).mean(1)) + 1e-9)
    return np.convolve(db, np.ones(3) / 3, mode="same")


ENV = envelope()


def _tok(w):
    return "".join(c for c in w.lower() if c.isalnum() or c == "'")


def _near(token, t):
    hits = [i for i, w in enumerate(WORDS) if _tok(w["w"]) == token and abs(w["s"] - t) < 4]
    assert hits, (token, t)
    return min(hits, key=lambda i: abs(WORDS[i]["s"] - t))


def _runs(lo, hi):
    """Quiet runs inside [lo, hi] as (start, end) seconds."""
    i0, i1 = max(int(lo * 100), 0), int(hi * 100)
    q = ENV[i0:i1] < THR
    out, k = [], 0
    while k < len(q):
        if q[k]:
            j = k
            while j < len(q) and q[j]:
                j += 1
            if j - k >= QUIET:
                out.append(((i0 + k) / 100, (i0 + j) / 100))
            k = j
        else:
            k += 1
    return out


def _dip(lo, hi):
    i0, i1 = int(lo * 100), max(int(hi * 100), int(lo * 100) + 1)
    return (i0 + int(np.argmin(ENV[i0:i1]))) / 100


def edges(s, e):
    """One kept span -> (start, end) on the raw file, on silence."""
    idx = [i for i, w in enumerate(WORDS) if s <= (w["s"] + w["e"]) / 2 <= e]
    i0, i1 = idx[0], idx[-1]
    f, l = OVR.get(s, (None, None))
    if isinstance(f, str):
        i0 = _near(f, s)
    if isinstance(l, str):
        i1 = _near(l, e)
    fs = f if isinstance(f, float) else WORDS[i0]["s"]
    le = l if isinstance(l, float) else WORDS[i1]["e"]
    # the neighbours a cut must not reach into: the words either side of it
    # (by time where the edge is a hand-set time, Whisper having no word there)
    if isinstance(f, float):
        prev_e = max([w["e"] for w in WORDS if w["e"] <= fs - 0.05] or [0.0])
    else:
        prev_e = WORDS[i0 - 1]["e"] if i0 > 0 else 0.0
    if isinstance(l, float):
        next_s = min([w["s"] for w in WORDS if w["s"] >= le + 0.05] or [le + 2.0])
    else:
        next_s = WORDS[i1 + 1]["s"] if i1 + 1 < len(WORDS) else le + 2.0

    lo, hi = max(prev_e - 0.15, fs - 1.0), fs + 0.10
    runs = [r for r in _runs(lo, hi) if r[1] <= hi]
    a = max(runs[-1][1] - LEAD, runs[-1][0]) if runs else _dip(lo, hi) - 0.06

    # no pause before the next word: cut in the dip between the two, late
    # rather than early (her note: a few word ends still sounded clipped)
    lo, hi = le - 0.10, min(le + 1.2, next_s + 0.10)
    runs = _runs(lo, hi)
    b = min(runs[0][0] + TAIL, runs[0][1]) if runs else _dip(lo, next_s + 0.15) + 0.08
    return round(a, 3), round(b, 3)


def word_clip(token, t):
    """One word on its own, for the cold open: tight, never into a neighbour."""
    i = _near(token, t)
    w, prev_e, next_s = WORDS[i], WORDS[i - 1]["e"], WORDS[i + 1]["s"]
    lo, hi = max(prev_e - 0.10, w["s"] - 0.6), w["s"] + 0.08
    runs = [r for r in _runs(lo, hi) if r[1] <= hi]
    a = max(runs[-1][1] - 0.10, runs[-1][0]) if runs else _dip(lo, hi) - 0.02
    lo, hi = w["e"] - 0.10, min(w["e"] + 0.8, next_s + 0.05)
    runs = _runs(lo, hi)
    b = min(runs[0][0] + 0.20, runs[0][1]) if runs else _dip(lo, hi) + 0.04
    return round(a, 3), round(min(b, next_s - 0.02), 3)


# ------------------------------------------------------------------ the parts
# Subtitles: (source time, Ukrainian). Each runs until the next one starts or
# its cut ends. Questions are not subtitled: the sticker says them.
# Stickers: (source time, UA, EN, flash into it, seconds on screen).
PART = {1: dict(
    subs=[
        (25.9, "Привіт-привіт!"), (26.6, "Ви знаєте мене як технічну продюсерку,"),
        (28.4, "але ніколи не бачили мого чоловіка."), (30.9, "Але сьогодні ми 5 років разом,"),
        (33.6, "тому я відповім на ваші питання,"), (36.1, "які ви мені задали в Threads,"),
        (37.6, "про наші відносини."), (39.5, "Хто не знає:"), (40.4, "чистокровний індієць,"),
        (41.9, "прям 100%, 24 на 7,"), (44.8, "народився в Індії, прожив в Індії."),
        (81.2, "Ну, ми познайомились у Барселоні."), (83.0, "Я поїхав з Індії зовсім молодим,"),
        (85.7, "поїхав у Барселону"), (86.5, "на якусь дурну спеціальність"),
        (88.4, "і злив купу грошей."), (89.4, "Але зустрів там тебе."),
        (93.0, "Тож так, Барселона."), (94.3, "Воно було того варте?"), (95.0, "Варте. Мабуть."),
        (102.2, "О боже, складне питання."), (104.0, "Мені подобається в тобі все."),
        (112.5, "Ти добра, ти дбаєш про мене,"), (115.4, "ти мене любиш."), (117.7, "Ти найкраща."),
        (128.9, "Ну, взагалі ми з різних культур,"), (132.5, "але як люди ми дуже схожі."),
        (135.2, "Прям надзвичайно схожі."), (138.5, "Ми зійшлися десь за тиждень,"),
        (140.6, "тож ми мусимо бути схожі."), (142.3, "З'їхались через пів року."),
        (362.0, "Англійською."), (365.8, "Іншої спільної мови в нас немає."),
        (371.8, "Іноді ми переходимо на свою мову,"), (374.5, "щось посередині,"),
        (375.3, "де кожен вставляє свої слова."),
        (385.2, "Ми так і не вивчили мови одне одного."), (387.4, "Не дуже й хотіли."),
        (389.0, "Але кілька слів знаємо."),
        (412.4, "Я знаю кілька слів індійською,"), (414.4, "а точніше гуджараті."),
        (419.4, "Найчастіше ми кажемо"), (421.1, "«арре яар»."), (422.0, "Це від мене."),
        (422.8, "Обожнюю."), (423.7, "Воно так легко злітає з язика."),
        (433.6, "Ти знаєш багато лайливих слів."), (435.4, "Я знаю багато лайливих слів."),
        (437.0, "І побутові, як «чамчі»."), (439.8, "«Чамчі» — це ложка."), (441.0, "Гандарі."),
        (441.8, "Що я ще знаю?"), (443.4, "Знаю багато…"),
        (445.7, "Ти знаєш купу лайливих слів."), (448.5, "Так, вона «гандарі». Дуже «гандарі»."),
        (454.1, "Знаю кілька."), (456.3, "«Бл*ть» — одне з них."), (457.9, "Знаю «п*зда»."),
        (459.4, "Це все погані слова."), (460.7, "Ще знаю «йо* твою мать»."),
        (463.3, "Моє улюблене."), (468.2, "«Господи»."), (468.9, "Знаю «Господи»."),
        (475.5, "Ще я знаю кілька французьких слів."),
        (479.1, "Яке там французьке слово казав твій тато?"), (482.4, "«Connasse»."),
        (483.6, "Обожнюю."), (484.8, "Здається, це моє улюблене іноземне слово."),
        (488.0, "«Connasse»."),
    ],
    stickers=[
        (80.0, "Де ми познайомились?", "Where did we meet?", True, 3.5),
        (97.9, "Що тобі в мені подобається?", "What do you like about me?", True, 3.5),
        (121.7, "Ми з дуже різних світів.\nЩо нас поєднує?",
         "We come from very different backgrounds. What brings us together?", True, 6.0),
        (360.0, "Якою мовою ми говоримо?", "Which language do we speak?", True, 3.5),
        (453.0, "А які слова знаєш ти?", "What words do you know?", False, 3.2),
    ],
    end=("Далі ще 2 частини", "підпишись, щоб не пропустити"),
    # cold open: his «Господи», her «арре яар», then a flash into the intro
    cold=[("hospadé", 469.1, "«Господи»!"), ("areyar", 421.1, "«Арре яар»!")],
    # name tabs while she introduces them: (source time, name, x over the head, s)
    tabs=[(26.6, "Рута", 724, 2.4), (29.3, "Кундж", 292, 2.4)],
    # the one close-up: her face after «5 років разом», chest up
    close=[(33.45, 34.55, 2.3, (0.66, 0.48))],
)}

# Her note on the first dressed preview: no punch-ins, they crop us and make
# no sense. The only close-up is the one PART[n]["close"] names.
FLASH_OUT, FLASH_IN = 0.10, 0.22
END_HOLD = 5.0


def frames(t):
    return max(1, round(t * FPS))


def plan(cuts, flash_at, close=(), cold=()):
    """Cuts -> shots (source start, frames, zoom, flashes). Cold-open clips go
    first and flash into the rest; a close-up splits the cut it falls in."""
    shots = [dict(a=a, n=frames(b - a), zoom=1.0, centre=None, cold=True, flash_in=False)
             for a, b in cold]
    for a, b in cuts:
        pieces = [(a, b, 1.0, None)]
        for ca, cb, z, c in close:
            if a < ca < b:
                pieces = [(a, ca, 1.0, None), (ca, min(cb, b), z, c)] + \
                         ([(cb, b, 1.0, None)] if cb < b else [])
        for k, (pa, pb, z, c) in enumerate(pieces):
            shots.append(dict(a=pa, n=frames(pb - pa), zoom=z, centre=c, cold=False,
                              flash_in=(k == 0 and any(abs(a - q) < 1.0 for q in flash_at))))
    if cold:
        shots[len(cold)]["flash_in"] = True
    for i, sh in enumerate(shots):
        sh["flash_out"] = i + 1 < len(shots) and shots[i + 1]["flash_in"]
    return shots


def timeline(shots):
    """Source time -> output time, for anything inside a kept shot."""
    marks, t = [], 0.0
    for sh in shots:
        d = sh["n"] / FPS
        if not sh["cold"]:          # the cold open repeats words said later
            marks.append((sh["a"], sh["a"] + d, t))
        t += d
    def out(src):
        for a, b, o in marks:
            if a - 0.05 <= src <= b + 0.05:
                return o + min(max(src - a, 0), b - a)
        raise ValueError(f"{src} is not in any kept shot")
    return out, marks, t


def run(cmd):
    subprocess.run(cmd, check=True)


def vf_shot(zoom, centre, flash_in, flash_out, n):
    f = []
    if zoom != 1.0:
        cw, ch = f"iw/{zoom}", f"ih/{zoom}"
        f.append(f"crop={cw}:{ch}:iw*{centre[0]}-{cw}/2:ih*{centre[1]}-{ch}/2")
    f += [f"scale={OW}:{OH}", f"fps={FPS_N}/{FPS_D}", "format=yuv420p"]
    if flash_in:
        f.append(f"fade=t=in:st=0:d={FLASH_IN}:color=white")
    if flash_out:
        f.append(f"fade=t=out:st={n / FPS - FLASH_OUT:.3f}:d={FLASH_OUT}:color=white")
    return ",".join(f)


ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "28", "-g", "60",
       "-c:a", "aac", "-b:a", "96k", "-ac", "1", "-ar", "48000"]


def ass_time(t):
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


MAXC = 24      # one line, a few words: her note on the first dressed preview


def chunks(text, a, b):
    """Split a subtitle into one-line pieces of a few words, timed by length."""
    words = text.split()
    k = -(-len(text) // MAXC)
    target, lines, cur = len(text) / k, [], ""
    for w in words:
        if cur and (len(cur) + 1 + len(w) > MAXC or len(cur) >= target):
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    lines.append(cur)
    total, t, outl = sum(len(x) for x in lines), a, []
    for x in lines:
        d = (b - a) * len(x) / total
        outl.append((t, t + d, x))
        t += d
    return outl


def write_ass(path, subs, cuts, out, extra=()):
    # Her captions are Google Sans 700 at 90px, centred on y 1472 (STYLE.md
    # §2b). These are half that, as she asked. libass sizes by line height, so
    # 56 here lands near a 45px em. No shadow, no stroke: the caption band
    # (assets/caption-band.png) under them carries the contrast.
    head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Product Sans,56,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,0,0,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    timed = list(extra)
    for k, (t, text) in enumerate(subs):
        cut_end = next(b for a, b in cuts if a - 0.3 <= t <= b)
        nxt = subs[k + 1][0] if k + 1 < len(subs) else 1e9
        end = min(nxt, cut_end)
        a, b = out(max(t, next(a for a, b in cuts if a - 0.3 <= t <= b))), out(end)
        timed += chunks(text, a, b)
    lines = [f"Dialogue: 0,{ass_time(a)},{ass_time(b)},Sub,,0,0,0,,"
             f"{{\\an5\\pos(540,1472)}}{text}" for a, b, text in timed]
    open(path, "w", encoding="utf-8").write(head + "\n".join(lines) + "\n")


def build(n, dress_only=False):
    spans = json.load(open(os.path.join(WORK, "spans.json")))[n - 1]["spans"]
    cfg = PART[n]
    cuts = [edges(s, e) for s, e in spans]
    cold = [word_clip(tok, t) for tok, t, _ in cfg.get("cold", [])]
    json.dump({"cold": cold, "cuts": cuts}, open(os.path.join(WORK, f"part{n}-cuts.json"), "w"), indent=1)
    shots = plan(cuts, [q[0] for q in cfg["stickers"] if q[3]], cfg.get("close", []), cold)
    out, marks, dur = timeline(shots)
    t, cold_caps = 0.0, []
    for sh, (_, _, text) in zip(shots, cfg.get("cold", [])):
        cold_caps.append((t, t + sh["n"] / FPS, text))
        t += sh["n"] / FPS
    tmp = os.path.join(WORK, f"p{n}")
    os.makedirs(os.path.join(tmp, "seg"), exist_ok=True)

    joined = os.path.join(tmp, "joined.mp4")
    total = dur + frames(END_HOLD) / FPS
    if not (dress_only and os.path.exists(joined)):
        cut_and_join(cfg, cuts, shots, tmp, joined)
    dress(n, cfg, cuts, out, tmp, joined, total, cold_caps)
    print(f"part {n}: {len(cuts)} cuts, {len(shots)} shots, {dur:.1f}s + {END_HOLD:.0f}s card")


def cut_and_join(cfg, cuts, shots, tmp, joined):
    # shots
    listing = []
    for k, sh in enumerate(shots):
        d = sh["n"] / FPS
        seg = os.path.join(tmp, "seg", f"{k:02d}.mp4")
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{sh['a']:.3f}", "-i", RAW,
             "-vf", vf_shot(sh["zoom"], sh["centre"], sh["flash_in"], sh["flash_out"], sh["n"]),
             "-af", f"atrim=0:{d:.4f},afade=t=in:d=0.008,afade=t=out:st={d - 0.008:.4f}:d=0.008",
             "-frames:v", str(sh["n"]), *ENC, seg])
        listing.append(seg)

    # the follow card: the take runs on, muted, blurred, hazed
    endpng = cards.render(os.path.join(tmp, "end.png"), cfg["end"][0], cfg["end"][1],
                          top=760, tilt=-1.5, uk_px=112, en_px=60, seed=7)
    seg = os.path.join(tmp, "seg", "end.mp4")
    nend = frames(END_HOLD)
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{cuts[-1][1]:.3f}", "-i", RAW, "-i", endpng,
         "-f", "lavfi", "-i", "anullsrc=r=48000:cl=mono",
         "-filter_complex",
         f"[0:v]scale={OW}:{OH},fps={FPS_N}/{FPS_D},gblur=sigma=28,"
         f"drawbox=c=white@0.5:t=fill,format=yuv420p[b];[1:v]scale={OW}:{OH}[c];[b][c]overlay[v]",
         "-map", "[v]", "-map", "2:a", "-frames:v", str(nend), "-t", f"{nend / FPS:.4f}", *ENC, seg])
    listing.append(seg)

    lst = os.path.join(tmp, "list.txt")
    open(lst, "w").write("".join(f"file '{p}'\n" for p in listing))
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined])


def dress(n, cfg, cuts, out, tmp, joined, total, cold_caps=()):
    """Caption band, subtitles, name tabs and question stickers over the cut."""
    ass = os.path.join(tmp, "subs.ass")
    write_ass(ass, cfg["subs"], cuts, out, cold_caps)
    talk_end = total - frames(END_HOLD) / FPS
    loop = ["-loop", "1", "-framerate", f"{FPS_N}/{FPS_D}", "-t", f"{total:.3f}"]
    # her usual blurred underlay, stretched and thin, on for the whole talk
    band_h = round(260 * OH / 1920 / 2) * 2
    inputs = ["-i", joined, *loop, "-i", os.path.join(ROOT, "assets", "caption-band.png")]
    graph = [f"[1:v]scale={OW}:{band_h}[band]",
             f"[0:v][band]overlay=x=0:y={round(1472 * OH / 1920 - band_h / 2)}"
             f":enable='lte(t,{talk_end:.3f})'[b0]",
             f"[b0]subtitles={ass}:fontsdir={FONTS}[v0]"]
    last, k = "v0", 0
    over = []
    for j, (t, name, cx, hold) in enumerate(cfg.get("tabs", [])):
        png = cards.tab(os.path.join(tmp, f"tab{j}.png"), name, cx, 470,
                        tilt=2.5 if j % 2 == 0 else -3.0, seed=11 + j)
        over.append((png, out(t), hold))
    for j, (t, uk, en, flash, hold) in enumerate(cfg["stickers"]):
        png = cards.render(os.path.join(tmp, f"q{j}.png"), uk, en, seed=3 + j,
                           tilt=-2.0 if j % 2 == 0 else 1.6)
        over.append((png, out(t), hold))
    for png, a, hold in over:
        # a still has one frame; looped, overlay has it for every frame of the cut
        inputs += [*loop, "-i", png]
        idx = 2 + k
        graph.append(f"[{idx}:v]scale={OW}:{OH}[o{k}];"
                     f"[{last}][o{k}]overlay=enable='between(t,{a:.3f},{a + hold:.3f})'[v{k + 1}]")
        last, k = f"v{k + 1}", k + 1
    dst_dir = os.path.join(WORK, "out")
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, f"5-years-part-{n}-preview.mp4")
    # the looped stills tick at their own clock; pin the output to the cut's
    # frame rate and frame count so the picture can't outrun the sound
    graph.append(f"[{last}]fps={FPS_N}/{FPS_D}[vout]")
    nframes = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
                                  "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", joined],
                                 capture_output=True, text=True, check=True).stdout.strip())
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(graph),
         "-map", "[vout]", "-map", "0:a", "-frames:v", str(nframes), "-c:v", "libx264", "-preset", "veryfast",
         "-crf", "28", "-c:a", "copy", "-movflags", "+faststart", dst])
    print(dst)


if __name__ == "__main__":
    # --dress: keep the cut already joined, redo only subtitles and stickers
    build(int(sys.argv[1]), dress_only="--dress" in sys.argv)
