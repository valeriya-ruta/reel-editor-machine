# Captions for reel 41 on the cut timeline. No script exists (freestyle), so
# spelling is whisper's, corrected where it misheard her (STYLE.md §2).
import json
W = json.load(open("better.words.json"))["words"]
SEGS = json.load(open("cut.json"))
FIX = {3: "сплануємо", 17: "звати", 50: "ідеї,", 58: "по колу", 134: "акаунт",
       139: "Мені", 140: "прийшла", 143: "в директ,", 217: "звертає", 220: "останній",
       256: "сценаріїв.", 272: "проаналізувати,", 324: "з Threads,", 335: "супер контент.",
       364: "тижня", 389: "збирає", 400: "ідей", 423: "додаток Рута,", 435: "сценаріїв,",
       511: "сценаріїв", 514: "мені", 566: "Google", 567: "Диск,", 571: "Google", 572: "Диск",
       576: "Claude", 577: "Code.", 582: "Клод", 586: "Клод", 624: "'язково,", 623: "обов",
       639: "налаштувати", 651: "ці рілси,", 687: "ці рілси", 828: "налаштування",
       836: "готово.", 856: "пиши", 858: "в коментарі,", 10: "-продюсеру."}
DROP = {638}
KEEP = set(json.load(open("keep_idx.json")))
# map source time -> cut time
# the plate is per-segment encodes, each rounded to whole frames
# (mkplate.py), so offsets come from the real frame counts
FR = [int(x) for x in open("seg/frames.txt").read().split()]
offs, t = [], 0.0
for (a, b), n in zip(SEGS, FR):
    offs.append((a, b, t)); t += n / 30.0
def tmap(x):
    for a, b, o in offs:
        if a - 1e-6 <= x <= b + 1e-6: return o + (x - a)
    return None
out = []
for i, w in enumerate(W):
    if i in DROP or i not in KEEP: continue
    s = tmap(w["s"])
    if s is None: continue
    e = tmap(min(w["e"], next(b for a, b, o in offs if a - 1e-6 <= w["s"] <= b + 1e-6)))
    txt = FIX.get(i, w["w"])
    if out and (txt.startswith("-") or txt.startswith("'")) and s - out[-1]["e"] < 0.4:
        out[-1]["w"] += txt; out[-1]["e"] = e; continue
    out.append({"w": txt, "s": round(s, 3), "e": round(e, 3)})
for a, b in zip(out, out[1:]):
    a["e"] = round(min(max(a["s"] + 0.12, min(a["e"], b["s"] - 0.085)), b["s"] - 0.02), 3)
json.dump({"words": out}, open("captions.json", "w"), ensure_ascii=False, indent=0)
print(len(out), "words, last ends %.2f / plate %.2f" % (out[-1]["e"], t))
print(" ".join(x["w"] for x in out))
