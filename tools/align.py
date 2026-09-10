# -*- coding: utf-8 -*-
"""Bind script spelling to ASR timing.

STYLE.md §2: timings come from the delivered audio, spelling comes from
SCRIPTS.md. Whisper mangles every product name, so its text is never shown --
but she also improvises against her own script, so the script is not a
transcript either.

The hard part is telling the two apart, because they look identical in a diff:

    written: вебкодинг     heard: вайп кодинг     <- whisper misheard
    written: коментувала   heard: коментуєш       <- she really said that

A phonetic key settles most of it. If what whisper heard *sounds* like what she
wrote, she said the written word and whisper spelled it badly -> script wins.
If it sounds like a different word, she changed the line -> her wording wins,
because the caption has to match what the viewer hears.

Whatever the phonetic key cannot call is printed as REVIEW for her to settle.

usage: align.py <words.json> <script.txt> <out.json>
"""
import json
import re
import sys
from difflib import SequenceMatcher

APOS = "’ʼ'`"
SURE = 0.82          # sounds the same -> whisper misheard, keep script spelling
UNSURE = 0.55        # below this it is her wording; between the two, ask
MERGE = 0.10         # closer than this apart and two words are one utterance
FLOOR = 0.10         # a caption never shows for fewer than 6 frames at 60fps

# STYLE.md §2: "Whisper mangles every product name." Phonetic ratio cannot
# separate those from a deliberate rewording -- «Cloud Design» for «Клод
# Дизайн» scores 0.63, lower than the genuine «коментуєш» for «коментувала»
# at 0.71. So the brand names are settled by name, ahead of any scoring, and
# only the ordinary words are left to the phonetic key.
BRANDS = ["Клод Дизайн", "Клод Код", "Клод", "Клоді", "Клода", "Фігма", "Фігмі",
          "Фігмою", "фігмі", "Mobbin", "Пінтерест", "Claude", "Codex", "Cursor",
          "скіл", "брейншторм", "брейнштормі", "вайбкодинг", "вайбкодити",
          "Рута", "Руту", "Руті", "Рути"]

# Read by hand off the audio where neither the lexicon nor the phonetic key
# can call it: whisper produced a non-word and she plainly said the script's
# line. Keyed by the ASR start time of the block.
FIXES = {
    5.16:  "мого серіалу",       # «моєї серіали» is not Ukrainian
    22.44: "що почну",           # «пішну» is not a word
    41.98: "саме",               # «сам би» — one word split in two
    90.16: "схожі додатки,",     # «хочуть додаток» inverts her meaning
    # Her script writes «вебкодинг», but she does not say it. Three separate
    # whisper passes over this audio give «вайп-кодинг» / «вайкоди» /
    # «випкодити» -- always /vaj/, never /web/. STYLE.md §2: wording comes from
    # the delivered audio. Spelled as the Ukrainian term, not as whisper wrote it.
    5.92:  "вайбкодинг,",
    8.80:  "вайбкодити.",
}

# One spelling per name for the whole reel, keyed by the normalised token.
CANON = {"brainstorm": "брейншторм", "mobin": "Mobbin", "mobbin": "Mobbin",
         "cloud": "Клод", "claude": "Claude", "skill": "скіл",
         "design": "Дизайн", "code": "Код"}

# whisper writes her Ukrainian product names in English: Cloud, Skill, Mobin
LAT = {"c": "к", "q": "к", "k": "к", "x": "кс", "l": "л", "o": "о", "u": "у",
       "d": "д", "s": "с", "b": "б", "r": "р", "a": "а", "n": "н", "t": "т",
       "m": "м", "e": "е", "g": "г", "h": "х", "p": "п", "v": "в", "w": "в",
       "y": "и", "f": "ф", "j": "й", "z": "з", "i": "і"}

# coarse phonemes: the distinctions whisper actually gets wrong
PHON = {"а": "A", "о": "A", "я": "A", "у": "U", "ю": "U", "е": "E", "є": "E",
        "и": "I", "і": "I", "ї": "I", "б": "P", "п": "P", "в": "V", "ф": "V",
        "д": "T", "т": "T", "з": "S", "с": "S", "ж": "S", "ш": "S", "щ": "S",
        "ц": "C", "ч": "C", "г": "H", "х": "H", "ґ": "H", "к": "K", "л": "L",
        "м": "M", "н": "N", "р": "R", "й": "J"}


def norm(w):
    w = w.lower().replace("ё", "е")
    for a in APOS:
        w = w.replace(a, "'")
    return re.sub(r"[^0-9a-zЀ-ӿ']", "", w)


def phon(w):
    """Coarse sound key; collapses runs so доп/додоп compare equal."""
    w = "".join(LAT.get(c, c) for c in norm(w))
    out = []
    for c in w:
        p = PHON.get(c)
        if p and (not out or out[-1] != p):
            out.append(p)
        elif c.isdigit():
            out.append(c)
    return "".join(out)


def sounds_alike(written, heard):
    a, b = phon(" ".join(written)), phon(" ".join(heard))
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b, autojunk=False).ratio()


def main():
    asr = json.load(open(sys.argv[1], encoding="utf-8"))["words"]

    # script tokens, minus standalone punctuation (an em dash is not a caption)
    raw = re.split(r"\s+", open(sys.argv[2], encoding="utf-8").read().strip())
    script = [t for t in raw if norm(t)]

    # whisper splits tokens STYLE.md lists as known caption bugs
    fixed = []
    for w in asr:
        t = w["w"].strip().lstrip("-").strip()
        if not t:
            continue
        if fixed and (t[0] in APOS or re.fullmatch(r"%\w*", t)):
            fixed[-1]["w"] += t
            fixed[-1]["e"] = w["e"]
            continue
        fixed.append({"w": t, "s": w["s"], "e": w["e"]})
    asr = fixed

    sm = SequenceMatcher(None, [norm(w["w"]) for w in asr],
                         [norm(t) for t in script], autojunk=False)

    out, review, mishear, improv = [], [], [], []
    pending = []          # script words with no ASR timing, awaiting a host
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                w = {"w": script[j1 + k], "s": asr[i1 + k]["s"],
                     "e": asr[i1 + k]["e"], "src": "script"}
                if pending:
                    w["pre"] = " ".join(pending); w["src"] = "script-fixed"
                    del pending[:]
                out.append(w)
            continue

        heard, written = asr[i1:i2], script[j1:j2]
        if not heard:
            # No ASR word to hang these on. A one- or two-letter preposition is
            # almost always there in the audio and merely swallowed by the next
            # word -- «працювати в фігмі» came back as «працювати фігмі», which
            # is not Ukrainian. Carry those into the next caption. Anything
            # longer she genuinely cut, so it goes.
            if written and all(len(norm(x)) <= 2 for x in written):
                pending.extend(written)
            else:
                improv.append({"at": None, "written": " ".join(written),
                               "heard": "— (cut)"})
            continue

        r = sounds_alike(written, [w["w"] for w in heard]) if written else 0.0
        rec = {"at": round(heard[0]["s"], 2), "written": " ".join(written) or "—",
               "heard": " ".join(w["w"] for w in heard), "ratio": round(r, 2)}

        # A brand name in the written side settles the block outright.
        brand = next((b for b in BRANDS
                      if phon(b) and phon(b) in phon(" ".join(written))), None)
        rec["brand"] = brand

        # Whole block sounds like the script line: she said it as written and
        # whisper split or merged it («фільмі» for «у Фігмі», «вайп кодинг» for
        # one word). Word counts differ, so re-spread the script words across
        # the block's span, proportional to length -- longer words take longer
        # to say than «у».
        pin = next((v for k, v in FIXES.items() if abs(k - heard[0]["s"]) < 0.05),
                   None)
        if pin is not None:
            written = pin.split()
            rec["written"] = pin

        # A brand name settles the block only when the two sides are roughly
        # the same length. Otherwise she added words around it («брейнштормі,
        # як я розказала тут») and redistributing would delete them.
        close = abs(len(heard) - len(written)) <= 1 or r >= UNSURE
        if written and (pin or (brand and close) or r >= SURE):
            t0, t1 = heard[0]["s"], heard[-1]["e"]
            widths = [max(len(norm(t)), 1) for t in written]
            total = sum(widths)
            acc = 0.0
            for t, wd in zip(written, widths):
                s = t0 + (t1 - t0) * (acc / total)
                acc += wd
                e = t0 + (t1 - t0) * (acc / total)
                out.append({"w": t, "s": round(s, 3), "e": round(e, 3),
                            "src": "script-fixed"})
            rec["result"] = " ".join(written)
            mishear.append(rec)
            continue

        # Otherwise resolve word by word. Inside one divergent block she may
        # both improvise *and* be misheard -- «Cloud Code. І сказати» is «Клод
        # Код» misspelled plus «І сказати» genuinely added. Her word choice is
        # kept; a word that merely *sounds* like the script's takes the
        # script's spelling.
        resolved, fixed_any, kept_any = [], False, False
        wsm = SequenceMatcher(None, [phon(w["w"]) for w in heard],
                              [phon(t) for t in written], autojunk=False)
        for wt, a1, a2, b1, b2 in wsm.get_opcodes():
            if wt == "equal":
                for k in range(a2 - a1):
                    resolved.append((written[b1 + k], "script-fixed"))
                    fixed_any = True
            elif wt == "replace" and (a2 - a1) == (b2 - b1):
                for k in range(a2 - a1):
                    h, s = heard[a1 + k]["w"], written[b1 + k]
                    if sounds_alike([s], [h]) >= SURE:
                        resolved.append((s, "script-fixed")); fixed_any = True
                    else:
                        resolved.append((h, "asr")); kept_any = True
            else:
                for k in range(a1, a2):
                    resolved.append((heard[k]["w"], "asr")); kept_any = True

        for w, (text, src) in zip(heard, resolved):
            out.append({"w": text, "s": w["s"], "e": w["e"], "src": src})

        rec["result"] = " ".join(t for t, _ in resolved)
        if fixed_any and not kept_any:
            mishear.append(rec)
        elif r >= UNSURE and fixed_any:
            review.append(rec)
        else:
            improv.append(rec)

    # A preposition with no timing rides on the caption that follows it.
    for i, w in enumerate(out):
        if w.get("pre"):
            w["w"] = w.pop("pre") + " " + w["w"]

    # Final sweep, over every caption whatever its source. Two things survive
    # the block logic: a brand inside a block kept for her wording («brainstorm,
    # як і розказала тут» -- the addition is real, the Latin spelling is not),
    # and a brand her own script spells inconsistently. She writes «платформа
    # Mobin» in one sentence and «про Mobbin» in the next; the product is
    # Mobbin, and the same name must not change spelling mid-reel.
    for w in out:
        stem = re.match(r"^[\w'’ʼ-]*", w["w"]).group(0)
        canon = CANON.get(norm(stem))
        if canon and canon != stem:
            w["w"] = canon + w["w"][len(stem):]
            w["src"] = "script-fixed"

    out.sort(key=lambda w: w["s"])

    # Whisper puts 35 ms around a word like «щоб». Held only for its own
    # duration that is two frames -- a flash, not a caption. Words this close
    # together are one utterance, so merge them and let the pair share a slot.
    merged = [out[0]]
    for w in out[1:]:
        if w["s"] - merged[-1]["s"] < MERGE:
            merged[-1]["w"] += " " + w["w"]
            merged[-1]["e"] = max(merged[-1]["e"], w["e"])
            if w["src"] != merged[-1]["src"]:
                merged[-1]["src"] = "script-fixed"
        else:
            merged.append(w)
    out = merged

    # Each caption holds until the next one replaces it, so the band is never
    # empty mid-sentence and a fast word is still readable. STYLE.md: back the
    # end off by 85 ms or consecutive words superimpose for ~1.5 frames.
    for i in range(len(out) - 1):
        out[i]["e"] = max(out[i]["s"] + FLOOR, out[i + 1]["s"] - 0.085)
    out[-1]["e"] = max(out[-1]["e"], out[-1]["s"] + 0.30)

    json.dump({"words": out, "review": review, "improvised": improv,
               "misheard": mishear},
              open(sys.argv[3], "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    n = len(out)
    print("CAPTIONS %d   script %d | whisper-corrected %d | her wording %d"
          % (n, sum(1 for w in out if w["src"] == "script"),
             sum(1 for w in out if w["src"] == "script-fixed"),
             sum(1 for w in out if w["src"] == "asr")))
    print("\nWHISPER MISHEARD -> script spelling restored (%d)" % len(mishear))
    for d in mishear:
        print("  %7.2fs  %.2f  %-32s <- %s" % (d["at"], d["ratio"], d["written"][:32], d["heard"][:34]))
    print("\nSHE IMPROVISED -> her wording kept (%d)" % len(improv))
    for d in improv:
        at = "%7.2fs" % d["at"] if d["at"] is not None else "      -"
        print("  %s  script: %-28s said: %s" % (at, d["written"][:28], d["heard"][:40]))
    print("\nREVIEW -- could go either way (%d)" % len(review))
    for d in review:
        print("  %7.2fs  script: %-26s said: %-26s (%.2f)"
              % (d["at"], d["written"][:26], d["heard"][:26], d["ratio"]))


main()
