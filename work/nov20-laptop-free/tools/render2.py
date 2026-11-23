import json,sys,subprocess,os
src,plan,out=sys.argv[1:4]
P=json.load(open(plan)); d0=os.path.splitext(out)[0]+"_parts"; os.makedirs(d0,exist_ok=True)
def atempo(sp):
    f=[]
    while sp>2.0: f.append("atempo=2.0"); sp/=2.0
    f.append(f"atempo={sp:.5f}"); return ",".join(f)
lst=[]
for i,(s,e,sp) in enumerate(P):
    d=(e-s)/sp; nf=max(1,round(d*30)); d=nf/30; p=f"{d0}/{i:03d}.mp4"
    v=f"setpts=(PTS-STARTPTS)/{sp},fps=30,trim=end_frame={nf}"
    if sp<=1.6:
        fd=min(0.015,d/4)
        a=f"asetpts=PTS-STARTPTS,{atempo(sp)},apad,atrim=0:{d:.5f},afade=t=in:d={fd},afade=t=out:st={d-fd:.5f}:d={fd}"
        cmd=["ffmpeg","-v","error","-y","-ss",str(s),"-t",str(e-s),"-i",src,"-vf",v,"-af",a,"-ar","48000","-ac","2"]
    else:
        cmd=["ffmpeg","-v","error","-y","-ss",str(s),"-t",str(e-s),"-i",src,"-f","lavfi","-i","anullsrc=r=48000:cl=stereo","-vf",v,"-map","0:v","-map","1:a","-af",f"atrim=0:{d:.5f}"]
    cmd+=["-c:v","libx264","-preset","medium","-crf","18","-pix_fmt","yuv420p","-c:a","pcm_s16le","-f","mov",p]
    subprocess.run(cmd,check=True); lst.append(f"file '{os.path.abspath(p)}'")
open(d0+"/list.txt","w").write("\n".join(lst))
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",d0+"/list.txt","-c:v","copy","-c:a","aac","-b:a","192k","-movflags","+faststart",out],check=True)
