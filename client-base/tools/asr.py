import whisper, json, sys
m = whisper.load_model(sys.argv[3] if len(sys.argv) > 3 else "base")
r = m.transcribe(sys.argv[1], language="uk", word_timestamps=True, verbose=False)
w = [{"w": x["word"].strip(), "s": round(float(x["start"]),3), "e": round(float(x["end"]),3)}
     for s in r["segments"] for x in s.get("words", [])]
json.dump({"text": r["text"].strip(), "words": w}, open(sys.argv[2],"w",encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("WORDS", len(w))
