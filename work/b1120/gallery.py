# -*- coding: utf-8 -*-
"""Build the batch gallery page (an Artifact) from whatever reels are rendered.
    python3 work/b1120/gallery.py <outdir>   -> <outdir>/index.html, <outdir>/v/REEL-NN.mp4 (540p previews)
Prints the video files that are new since the last run, for the publish's `files`."""
import html, json, os, shutil, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = sys.argv[1]
TITLES = {
    41: "Скільки заробляє RUTA", 42: "Автоматизація без бану", 43: "Автоматизації для репетиторки",
    44: "Скільки ти платиш за монтаж", 45: "Щоб АІ-агент нічого не вигадував", 46: "Налаштування агентів SendPulse",
    47: "Автоматизації для викладачки мови", 48: "Автоматизації для коучки", 49: "Автоматизації для фотографки",
    50: "Монтаж як твої референси", 51: "Менеджерка відповідає по 5 годин", 52: "Скіли, щоб Claude монтував",
    53: "Автоматизації для відеографки", 54: "CRM у Notion для малого бізнесу", 55: "Скільки хвилин займає один рілс",
    56: "АІ-агент чи чат-бот з кнопками",
}
SCHED = {41: "20 лис", 42: "20 лис", 43: "21 лис", 44: "21 лис", 45: "21 лис", 46: "22 лис", 47: "22 лис",
         48: "23 лис", 49: "24 лис", 50: "24 лис", 51: "24 лис", 52: "25 лис", 53: "25 лис", 54: "25 лис",
         55: "26 лис", 56: "26 лис"}
os.makedirs(os.path.join(OUT, "v"), exist_ok=True)
new, cards, done = [], [], 0
for n in range(41, 57):
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
        media = '<div class="wait"><span class="dots"><i></i><i></i><i></i><i></i></span><span>монтується</span></div>'
        state = '<span class="st">в роботі</span>'
    cards.append('<article class="card%s"><div class="frame">%s</div><div class="meta"><div class="row">'
                 '<span class="num">%d</span>%s</div><h2>%s</h2><p class="when">публікація %s</p></div></article>'
                 % ("" if ok else " pending", media, n, state, t, SCHED[n]))
page = open(os.path.join(ROOT, "work", "b1120", "gallery.tpl.html"), encoding="utf-8").read()
page = page.replace("{{CARDS}}", "\n".join(cards)).replace("{{DONE}}", str(done))
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(page)
print(json.dumps(new))
