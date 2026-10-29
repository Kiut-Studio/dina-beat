import sys
from PIL import Image, ImageDraw
import numpy as np
src, out = sys.argv[1], sys.argv[2]
A = Image.open(src).convert('RGBA'); W,H = A.size
PUMP=(255,212,140,255); INK=(14,8,4,255); CANDY=(252,250,244,255)
def poly(pts):
    m=Image.new('L',(W,H),0); ImageDraw.Draw(m).polygon(pts,fill=255); return np.array(m)>0
def circ(cx,cy,r):
    m=Image.new('L',(W,H),0); ImageDraw.Draw(m).ellipse([cx-r,cy-r,cx+r,cy+r],fill=255); return np.array(m)>0
X0=352
SIDE=[(426,199),(431,222),(436,250),(438,282),(436,312),(430,336),(421,356),(410,374),(399,392),(388,401)]
RIM=[(318,213),(345,216),(372,215),(398,209),(426,198)]
left=poly([(0,0),(363,0),(363,128),(X0,136),(X0,H),(0,H)])
body=poly([(X0,206)]+SIDE+[(376,412),(364,418),(X0,422)])
pile=poly([(X0,140),(372,136),(394,144),(410,160),(421,180),(427,198),(398,210),(372,216),(X0,216)])
o=np.array(A).copy()
o[body & poly([(386,0),(W,0),(W,H),(386,H)])]=PUMP     # cuello y patas de Dina -> calabaza
o[pile & ~left]=CANDY
O=Image.fromarray(o)
# golosinas de la misma pila (dibujo de Sofía), recortadas en círculo
cands=[((122,180),24,(349,184)),((180,120),23,(380,158)),((265,117),22,(405,183))]
extra=np.zeros((H,W),bool)
for (sx,sy),r,(tx,ty) in cands:
    p=A.crop((sx-r,sy-r,sx+r,sy+r)); m=Image.new('L',p.size,0); ImageDraw.Draw(m).ellipse([0,0,2*r-1,2*r-1],fill=255)
    a=np.array(p); a[:,:,3]=np.minimum(a[:,:,3],np.array(m))
    bgc=Image.new('RGBA',p.size,(0,0,0,0)); 
    O.alpha_composite(Image.fromarray(a),(tx-r,ty-r)); extra|=circ(tx,ty,r-1)
o=np.array(O)
keep=left|body|pile|extra
o[~keep]=(0,0,0,0)
o[poly([(X0,104),(366,104),(366,141),(X0,141)]) & ~extra]=(0,0,0,0)
O=Image.fromarray(o); d=ImageDraw.Draw(O)
def stroke(pts,w):
    d.line(pts,fill=INK,width=w,joint='curve')
    for p in pts: d.ellipse([p[0]-w/2+.5,p[1]-w/2+.5,p[0]+w/2-.5,p[1]+w/2-.5],fill=INK)
stroke(SIDE,8); stroke(RIM,7)
bb=O.getbbox(); O=O.crop(bb); O.save(out); print(bb,O.size)
