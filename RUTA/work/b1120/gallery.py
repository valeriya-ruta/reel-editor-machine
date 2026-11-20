# -*- coding: utf-8 -*-
"""Build the batch gallery page (an Artifact) from whatever reels are rendered.
    python3 work/b1120/gallery.py <outdir>   -> <outdir>/index.html, <outdir>/v/REEL-NN.mp4 (540p previews)
Prints the video files that are new since the last run, for the publish's `files`."""
import html, json, os, shutil, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = sys.argv[1]
TITLES = {
    57: "Скільки заробляє RUTA", 58: "Автоматизація без бану", 59: "Автоматизації для репетиторки",
    60: "Скільки ти платиш за монтаж", 61: "Щоб АІ-агент нічого не вигадував", 62: "Налаштування агентів SendPulse",
    63: "Автоматизації для викладачки мови", 64: "Автоматизації для коучки", 65: "Автоматизації для фотографки",
    66: "Монтаж як твої референси", 67: "Менеджерка відповідає по 5 годин", 68: "Скіли, щоб Claude монтував",
    69: "Автоматизації для відеографки", 70: "CRM у Notion для малого бізнесу", 71: "Скільки хвилин займає один рілс",
    72: "АІ-агент чи чат-бот з кнопками",
}
SCHED = {57: "20 лис", 58: "20 лис", 59: "21 лис", 60: "21 лис", 61: "21 лис", 62: "22 лис", 63: "22 лис",
         64: "23 лис", 65: "24 лис", 66: "24 лис", 67: "24 лис", 68: "25 лис", 69: "25 лис", 70: "25 лис",
         71: "26 лис", 72: "26 лис"}
os.makedirs(os.path.join(OUT, "v"), exist_ok=True)
new, cards, done = [], [], 0
for n in range(57, 73):
    full = os.path.join(ROOT, "reel-%d" % n, "renders", "REEL-%d.mp4" % n)
    prev = os.path.join(ROOT, "reel-%d" % n, "renders", "REEL-%d-preview.mp4" % n)
    ok = os.path.exists(full)
    dur = ""
    if ok:
        done += 1
        if not os.path.exists(prev):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", full, "-vf", "scale=540:960", "-c:v", "libx264",
                            "-crf", "30", "-preset", "fast", "-c:a", "aac", "-b:a", "96k", prev], check=True)
        dst = os.path.join(OUT, "v", "REEL-%d.mp4" % n)
        if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(prev):
            shutil.copy2(prev, dst); new.append("v/REEL-%d.mp4" % n)
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", full],
                                 capture_output=True, text=True).stdout)
        dur = "%d:%02d" % (int(d) // 60, int(round(d)) % 60)
    t = html.escape(TITLES[n])
    if ok:
        media = ('<video controls playsinline preload="metadata" src="v/REEL-%d.mp4#t=0.5" '
                 'aria-label="REEL-%d, %s"></video>' % (n, n, t))
        state = '<span class="st ok">готово · %s</span>' % dur
    else:
        media = '<div class="wait"><span class="dots"><i></i><i></i><i></i><i></i></span><span>%s</span></div>' % (
            "рендериться" if n == 61 else "в черзі")
        state = '<span class="st">%s</span>' % ("зараз" if n == 61 else "чекає")
    cards.append('<article class="card%s"><div class="frame">%s</div><div class="meta"><div class="row">'
                 '<span class="num">%d</span>%s</div><h2>%s</h2><p class="when">публікація %s</p></div></article>'
                 % ("" if ok else " pending", media, n, state, t, SCHED[n]))
page = open(os.path.join(ROOT, "work", "b1120", "gallery.tpl.html"), encoding="utf-8").read()
page = page.replace("{{CARDS}}", "\n".join(cards)).replace("{{DONE}}", str(done))
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(page)
print(json.dumps(new))
