# Screen-recording clips for reel 41: (name, src start, src end, out duration, crop)
# Source is her 36-min desktop recording, 1920x1080@60, silent.
import subprocess, json, sys
SRC = "work/r41/src/screen.mp4"
CHAT = (230, 0, 1460, 1080)      # the Claude chat column + input box
APP = (445, 90, 1336, 990)       # RUTA web app, below her bookmarks bar, sidebar off
CLIPS = [   # durations = the slot each one fills on the cut timeline (build.py SLOTS)
    ("c1_skill",     1.0,   11.0,  2.90, CHAT),
    ("c2_tools",    11.0,   55.0, 10.36, CHAT),
    ("c3_hypo",    128.0,  178.0,  8.20, CHAT),
    ("c3b_leads",  237.0,  245.0,  1.94, CHAT),
    ("c4_calls",    52.0,  100.0,  8.39, CHAT),
    ("c4c_threads",340.0,  362.0,  3.94, CHAT),
    ("c5_ideas",    14.0,   50.0,  7.96, CHAT),
    ("c6_list",    362.0,  420.0,  6.24, CHAT),
    ("c7_pick",    465.0,  515.0,  2.01, CHAT),
    ("c8_14",      661.0,  669.0,  1.50, CHAT),
    ("c9_ruta",    635.0,  660.0,  2.38, CHAT),
    ("c10_app",   1650.0, 1745.0, 12.85, APP),
    ("c11_done",  1745.0, 1790.0,  4.92, APP),
]
if __name__ == "__main__":
    only = sys.argv[1:]
    SL = json.load(open("work/r41/slots.json"))
    CLIPS = [(n, a, b, SL.get(n, d), cr) for n, a, b, d, cr in CLIPS]
    for n, a, b, d, (x, y, w, h) in CLIPS:
        if only and n not in only: continue
        k = (b - a) / d
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", "%.3f" % a, "-t", "%.3f" % (b - a),
                        "-i", SRC, "-an", "-vf",
                        "crop=%d:%d:%d:%d,setpts=PTS/%.5f,fps=30" % (w, h, x, y, k),
                        "-t", "%.3f" % (d + 0.2), "-c:v", "libx264", "-crf", "20", "-preset", "fast",
                        "-pix_fmt", "yuv420p", "reel-41/assets/scr/%s.mp4" % n], check=True)
        print(n, "%.1fx" % k, flush=True)
    json.dump({n: [a, b, d] for n, a, b, d, _ in CLIPS}, open("work/r41/clips.json", "w"), indent=1)
