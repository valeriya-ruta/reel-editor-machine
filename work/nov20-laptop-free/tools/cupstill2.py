import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
frame,word,out=sys.argv[1:4]
X0,Y0,H,SIZE=map(int,sys.argv[4:8])        # cup top-left, cup height, font size
bg=Image.open(frame).convert('RGBA')
cup=Image.open('cup/cup.png'); cup=cup.crop(cup.getbbox()).rotate(-6,expand=True,resample=Image.BICUBIC)
cup=cup.resize((int(cup.width*H/cup.height),H),Image.LANCZOS)
sh=Image.new('RGBA',bg.size,(0,0,0,0)); blk=Image.new('RGBA',cup.size,(0,0,0,255))
blk.putalpha(cup.split()[3].point(lambda v:int(v*0.35))); sh.paste(blk,(X0+8,Y0+14),blk)
bg=Image.alpha_composite(bg,sh.filter(ImageFilter.GaussianBlur(12)))
bg.alpha_composite(cup,(X0,Y0))
f=ImageFont.truetype('fonts/ProductSans-Black.ttf',SIZE)
tx,ty=X0+int(cup.width*0.30),Y0+int(H*0.60)
# barely-there shadow so the part outside the cup still reads on the light wall
t=Image.new('RGBA',bg.size,(0,0,0,0)); ImageDraw.Draw(t).text((tx+2,ty+3),word,font=f,fill=(0,0,0,110),anchor='lm')
bg=Image.alpha_composite(bg,t.filter(ImageFilter.GaussianBlur(4)))
ImageDraw.Draw(bg).text((tx,ty),word,font=f,fill=(255,255,255,255),anchor='lm')
bg.convert('RGB').save(out,quality=95)
