import subprocess,numpy as np
from pathlib import Path
r=Path(__file__).resolve().parents[1];w,h=1920,1080
raw=subprocess.check_output(['ffmpeg','-loglevel','error','-ss','2','-i',str(r/'assets/fire/fire.mp4'),'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-']);rgb=np.frombuffer(raw,np.uint8).reshape(h,w,3)
x=np.linspace(0,1,w);y=np.linspace(0,1,h);a=np.minimum(np.clip(x/.14,0,1),np.clip((1-x)/.14,0,1))[None,:]*np.minimum(np.clip(y/.25,0,1),np.clip((1-y)/.08,0,1))[:,None];a=a*a*(3-2*a)
g=rgb[:,:,1].astype(np.float32);red=rgb[:,:,0].astype(np.float32);key=np.clip((g-.2*red-5)/30,0,1);base=np.clip((y-.79)/.13,0,1)[:,None]*np.minimum(np.clip(x/.22,0,1),np.clip((1-x)/.22,0,1))[None,:];a*=np.maximum(key,base);rgba=np.dstack((rgb,(a*255).astype(np.uint8)))
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgba','-s',f'{w}x{h}','-i','-','-frames:v','1',str(r/'assets/realism/fire_soft_plate.png')],input=rgba.tobytes(),check=True)
