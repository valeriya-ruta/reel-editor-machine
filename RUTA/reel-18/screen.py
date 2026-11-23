# -*- coding: utf-8 -*-
"""Her Telegram Business screen recording, re-timed to her words and blurred.

    python screen.py          -> assets/media/screen.mp4  (run under work/heavy.sh)

Her recording (work/media/r18/telegram-business.mp4) is 1080x2082, variable
frame rate, 28 s, English UI. She says the same path in ~15 s, so it is cut
into segments and each one is played at the constant speed that puts the
screen on the word that names it (SEG). The output's t=0 is composition time
SCR0 and it plays as one plain <video> with data-media-start 0.

Blurred (BLUR, recording coordinates and recording time) — everything personal:
    her phone number and @username under her name on the Settings header;
    her existing chat links and their preset messages (contact names in them);
    the new link's address on the editor card, and in the keyboard's
    clipboard suggestion after she copies it.
Not used at all: her Profile tab (0-1.9 s: phone, username, birthday) and the
link list she scrolls after copying (21.8 s on: link names, her username and
phone in the footer).
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "work", "media", "r18", "telegram-business.mp4")
OUT = os.path.join(HERE, "assets", "media", "screen.mp4")

SCR0 = 22.000          # composition time of the screen clip's first frame
SCR1 = 37.100          # ... and of its end (the matte spans the same)
REC_W, REC_H = 1080, 2082
REC_Y = -162           # the clip sits bottom-aligned: rec y 162-2082 on screen

# (rec_a, rec_b, comp_a, comp_b) — each segment at one constant speed.
SEG = [
    (1.95, 2.80, 22.00, 23.95),    # Settings — «Заходиш в налаштування свого акаунту»
    (2.80, 3.30, 23.95, 24.95),    # the scroll — «скролиш вниз»
    (3.30, 4.15, 24.95, 26.12),    # Premium / Stars / Business; tap Business on «Бізнес»
    (4.15, 5.65, 26.12, 27.10),    # Telegram Business opens, she scrolls
    (5.65, 6.40, 27.10, 28.02),    # Links to Chat; tap on «розмову»
    (6.40, 7.80, 28.02, 29.10),    # Links to Chat page; tap Create on «нове»
    (7.80, 18.20, 29.10, 34.62),   # the editor, «Привіт! Хочу на Мадейру!» typed; ✓ on «Зберігаєш»
    (18.20, 20.35, 34.62, 35.35),  # «Preset message saved.»; tap the link on «береш»
    (20.35, 21.60, 35.35, 36.30),  # «Copied.»
]
FREEZE = (21.58, 36.30, SCR1)       # hold that frame to the end of the clip

# (x, y, w, h, rec_t0, rec_t1) — rec_t1 None = to the end
BLUR = [
    (200, 450, 680, 64, 1.80, 2.85),       # phone + @username under her name
    (150, 190, 760, 340, 2.84, 2.98),      # ... and while the header collapses as she scrolls
    (0, 866, 1080, 1216, 6.52, 8.60),      # her existing links + preset messages
    (0, 700, 1080, 1382, 8.10, 8.60),      # ... while the editor slides up over them
    (330, 766, 420, 72, 8.55, None),       # the new link's address on the card
    (250, 1222, 610, 96, 20.40, None),     # the copied link in the keyboard's clipboard bar
]


def comp(rec_t):
    """Recording time -> composition time (inside the segments)."""
    for a, b, ca, cb in SEG:
        if a <= rec_t <= b:
            return ca + (rec_t - a) * (cb - ca) / (b - a)
    raise ValueError(rec_t)


def rec(comp_t):
    """Composition time -> recording time."""
    for a, b, ca, cb in SEG:
        if ca <= comp_t <= cb:
            return a + (comp_t - ca) * (b - a) / (cb - ca)
    if comp_t >= FREEZE[1]:
        return FREEZE[0]
    raise ValueError(comp_t)


def graph():
    n = len(BLUR)
    parts = ["[0:v]setpts=PTS-STARTPTS,split=%d[m]%s" % (n + 1, "".join("[c%d]" % i for i in range(n)))]
    for i, (x, y, w, h, _, _) in enumerate(BLUR):
        r = min(24, h // 4)
        parts.append("[c%d]crop=%d:%d:%d:%d,boxblur=%d:3:%d:3[b%d]" % (i, w, h, x, y, r, max(2, r // 2), i))
    last = "m"
    for i, (x, y, w, h, t0, t1) in enumerate(BLUR):
        en = "gte(t,%.2f)" % t0 if t1 is None else "between(t,%.2f,%.2f)" % (t0, t1)
        parts.append("[%s][b%d]overlay=%d:%d:enable='%s'[o%d]" % (last, i, x, y, en, i))
        last = "o%d" % i
    # Every segment is resampled to 30 fps and cut to an exact frame count on
    # its own, so the boundaries land on the frames the taps are timed to
    # (resampling the concatenation instead drifted ~5 frames by the end).
    # The held last frame is a tpad on the whole, so the clip is never short.
    k = len(SEG)
    parts.append("[%s]split=%d%s" % (last, k, "".join("[s%d]" % i for i in range(k))))
    for i, (a, b, ca, cb) in enumerate(SEG):
        f = (cb - ca) / (b - a)
        n = int(round(cb * 30)) - int(round(ca * 30))
        parts.append("[s%d]trim=start=%.3f:end=%.3f,setpts=(PTS-STARTPTS)*%.5f,fps=30,"
                     "tpad=stop_mode=clone:stop_duration=0.2,trim=end_frame=%d,setpts=PTS-STARTPTS[v%d]"
                     % (i, a, b + 0.05, f, n, i))
    fr, fa, fb = FREEZE
    parts.append("%sconcat=n=%d:v=1:a=0,tpad=stop_mode=clone:stop_duration=%.3f,format=yuv420p[out]"
                 % ("".join("[v%d]" % i for i in range(k)), k, fb - fa + 0.5))
    return ";".join(parts)


def main():
    frames = int(round((SCR1 - SCR0) * 30))
    if not os.path.isdir(os.path.dirname(OUT)):
        os.makedirs(os.path.dirname(OUT))
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex", graph(),
           "-map", "[out]", "-frames:v", str(frames), "-r", "30", "-an",
           "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-movflags", "+faststart", OUT]
    subprocess.check_call(cmd)
    got = subprocess.check_output(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
                                   "-show_entries", "stream=nb_read_frames,width,height",
                                   "-of", "csv=p=0", OUT]).decode().strip()
    print("screen.mp4  %s  (want %d frames)" % (got, frames))


if __name__ == "__main__":
    if "--graph" in sys.argv:
        print(graph())
    else:
        main()
