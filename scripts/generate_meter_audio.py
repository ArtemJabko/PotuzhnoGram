"""Original procedural sound effects; no recordings or third-party audio."""
from pathlib import Path
import math,random,struct,wave
out=Path(__file__).resolve().parents[1]/'overlay/TMessagesProj/src/main/res/raw'
rng=random.Random(42);sr=22050
for name,duration in [('tick',.045),('boom',1.4)]:
 samples=[];low=0.
 for i in range(int(sr*duration)):
  t=i/sr;n=rng.uniform(-1,1);low=.92*low+.08*n
  if name=='tick':v=.45*n*math.exp(-t*150)
  else:v=(.65*low+.18*n*math.exp(-t*8)+.2*math.sin(2*math.pi*(70*t-15*t*t)))*math.exp(-t*3.8)
  v*=min(1,t/.001)*min(1,(duration-t)/.02)
  samples.append(struct.pack('<h',int(max(-.9,min(.9,v))*32767)))
 with wave.open(str(out/f'potuzno_{name}.wav'),'wb') as f:
  f.setparams((1,2,sr,0,'NONE','not compressed'));f.writeframes(b''.join(samples))
