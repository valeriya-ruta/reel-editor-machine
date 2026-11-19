# -*- coding: utf-8 -*-
"""Check + snapshot a reel in the cloud (GitHub Actions `qa.yml` on branch
asr-inbox), so her laptop never runs Chrome for it — 2026-10-05, *"my laptop
is overheating"*.

    python tools/cloudqa.py reel-22 --at 1.0,6.2,9.0     -> reel-22/study/cloud/
    python tools/cloudqa.py reel-22                       -> check only

Uploads the project with tools/hfup.py (the same zip HeyGen renders), runs the
workflow on it, downloads check.log + snap/ (frames and contact sheets). Prints
the check's error lines and the contact-sheet paths. ~3–5 min a call.
"""
import json
import os
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "valeriya-ruta/reel-editor-machine"


def gh(*args, **kw):
    extra = [] if args and args[0] == "api" else ["--repo", REPO]
    return subprocess.run(["gh"] + list(args) + extra, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", **kw)


def main():
    reel = sys.argv[1].rstrip("/\\")
    at = ""
    if "--at" in sys.argv:
        at = sys.argv[sys.argv.index("--at") + 1]
    project = os.path.join(ROOT, reel)
    up = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "hfup.py"), project],
                        capture_output=True, text=True, encoding="utf-8", errors="replace")
    url = next((l[4:].strip() for l in up.stdout.splitlines() if l.startswith("URL ")), None)
    if up.returncode or not url:
        sys.exit("upload failed: " + (up.stderr or up.stdout)[-400:])
    tag = "%s-%d" % (reel, int(time.time()))
    import base64
    body = json.dumps({"url": url, "at": at, "name": reel, "tag": tag})
    for attempt in range(6):
        r = gh("api", "-X", "PUT", "repos/%s/contents/qa/%s.json" % (REPO, tag),
               "-f", "message=qa " + tag, "-f", "branch=asr-inbox",
               "-f", "content=" + base64.b64encode(body.encode()).decode())
        if r.returncode == 0:
            break
        time.sleep(3 + attempt * 3)          # another reel committed at the same moment
    else:
        sys.exit("could not post the qa request: " + (r.stderr or r.stdout)[-300:])
    rid = None
    for _ in range(40):
        time.sleep(5)
        r = gh("run", "list", "--workflow", "qa.yml", "--branch", "asr-inbox", "--limit", "30",
               "--json", "databaseId,displayTitle")
        for run in json.loads(r.stdout or "[]"):
            if tag in run["displayTitle"]:
                rid = run["databaseId"]
                break
        if rid:
            break
    if not rid:
        sys.exit("could not find the qa run for " + tag)
    gh("run", "watch", str(rid), "--exit-status")
    out = os.path.join(project, "study", "cloud-" + tag.split("-")[-1])
    os.makedirs(out, exist_ok=True)
    gh("run", "download", str(rid), "-D", out)
    base = os.path.join(out, "qa-" + tag)
    log = os.path.join(base, "check.log")
    if os.path.exists(log):
        txt = open(log, encoding="utf-8", errors="replace").read()
        summ = re.findall(r"\d+ error\(s\), \d+ warning\(s\)[^\n]*", txt)
        print("check:", summ[-1] if summ else "(no summary)")
        for line in txt.splitlines():
            if "✗" in line:
                print("  " + line.strip()[:220])
    sheets = sorted(os.path.join(dp, f) for dp, _, fs in os.walk(base) for f in fs if f.startswith("contact-sheet"))
    for s in sheets:
        print("sheet:", s)
    if at and not sheets:
        print("no snapshots came back — see", os.path.join(base, "snap.log"))


if __name__ == "__main__":
    main()
