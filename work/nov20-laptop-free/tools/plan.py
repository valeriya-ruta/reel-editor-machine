import json,sys
D=455.80
WAIT=(68.0,274.7)          # silent upload wait -> 5 s
B=(346.3,426.3)            # Claude starts editing: continuous, no cuts
PRE,POST=0.10,0.14
segs=json.load(open(sys.argv[1]))
words=[w for s in segs for w in s['words'] if not (WAIT[0]<w['s']<WAIT[1])]
plan=[]                     # (src_s, src_e, speed)
def add(s,e,sp):
    if e-s>0.01: plan.append([round(s,3),round(e,3),sp])
t=0.0
def gap(a,b):               # a: end of speech, b: start of next speech
    global t
    if a>=WAIT[0]-0.5 and b<=WAIT[1]+0.5 or (a<=WAIT[0]<b):
        add(t,a+POST,1); add(a+POST,b-PRE,(b-PRE-a-POST)/5.0); t=b-PRE; return
    ia,ib=a+POST,b-PRE
    g=ib-ia
    if g<=0: return
    inB=B[0]<=ia<B[1]
    if inB:
        if g>0.8: add(t,ia,1); add(ia,ib,3.0); t=ib
        return
    if g<1.5:                       # dead air between lines: cut
        add(t,ia,1); t=ib
    else:                           # phone action: fast-forward, don't cut
        add(t,ia,1); add(ia,ib,max(2.0,min(6.0,g/0.9))); t=ib
start=max(0,words[0]['s']-0.3)
t=start
for i in range(len(words)-1):
    gap(words[i]['e'],words[i+1]['s'])
add(t,min(D,words[-1]['e']+0.4),1)
# merge adjacent same-speed contiguous
m=[]
for p in plan:
    if m and abs(m[-1][1]-p[0])<1e-3 and m[-1][2]==p[2]: m[-1][1]=p[1]
    else: m.append(p)
glob=float(sys.argv[3]) if len(sys.argv)>3 else 1.0
for p in m:
    if p[2]==1: p[2]=glob
out=sum((e-s)/sp for s,e,sp in m)
json.dump(m,open(sys.argv[2],'w'))
cuts=sum(1 for a,b in zip(m,m[1:]) if abs(a[1]-b[0])>1e-3)
print(f"segments {len(m)}  cuts {cuts}  output {out:.1f}s = {int(out//60)}:{out%60:04.1f}")
for s,e,sp in m:
    if sp>1.5: print(f"  ff {s:7.2f}-{e:7.2f} x{sp:.1f} -> {(e-s)/sp:.1f}s")
