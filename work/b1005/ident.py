import whisper, subprocess, glob, os, json
m = whisper.load_model("base")
out = {}
for f in sorted(glob.glob("C:/Users/Ruta/Downloads/20261005_13*.mp4")):
    wav = "id_" + os.path.basename(f)[:-4] + ".wav"
    subprocess.run(["ffmpeg","-nostdin","-v","error","-y","-t","14","-i",f,"-vn","-ac","1","-ar","16000",wav],check=True)
    r = m.transcribe(wav, language="uk", verbose=None)
    out[os.path.basename(f)] = r["text"].strip()
    print(os.path.basename(f), "|", r["text"].strip(), flush=True)
    os.remove(wav)
json.dump(out, open("ident.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
