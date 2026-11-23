import json,sys
plan=json.load(open(sys.argv[1])); words=json.load(open(sys.argv[2]))['words']
X,Y,SIZE=int(sys.argv[4]),int(sys.argv[5]),int(sys.argv[6])
# audible segments on the output timeline
segs=[];off=0.0
for s,e,sp in plan:
    d=round((e-s)/sp*30)/30
    if sp<=1.6: segs.append((s,e,sp,off))
    off+=d
cap=[]
for w in words:
    for s,e,sp,o in segs:
        if w['s']<e and w['e']>s+0.08:
            a=o+max(0,w['s']-s)/sp; b=o+(min(w['e'],e)-s)/sp
            cap.append([a,b,w['w'].upper()]); break
for i in range(len(cap)-1):
    nxt=cap[i+1][0]
    cap[i][1]=max(cap[i][1], min(nxt, cap[i][0]+0.10))   # never under 3 frames
    if nxt-cap[i][1]<0.25: cap[i][1]=nxt                  # hold until the next word
    cap[i][1]=min(cap[i][1],nxt-0.001)
def ts(t):
    t=max(0,t);h=int(t//3600);m=int(t%3600//60);s=t%60
    return f"{h}:{m:02d}:{s:05.2f}"
hdr=f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: W,Product Sans Black,{SIZE},&H00FFFFFF,&H00FFFFFF,&H90000000,&HA0000000,0,0,0,0,100,100,0,0,1,3,2,5,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
out=[hdr]
for a,b,t in cap:
    out.append(f"Dialogue: 0,{ts(a)},{ts(b)},W,,0,0,0,,{{\\pos({X},{Y})\\blur4}}{t}\n")
open(sys.argv[3],'w').write("".join(out)); print(len(cap),"captions")
