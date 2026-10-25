"""Reproduce the keyed review still from retained, licensed footage (NumPy/FFmpeg)."""
from pathlib import Path
import subprocess,numpy as np
root=Path(__file__).resolve().parents[1];assets=root/'assets/fire';w,h=1920,1080
if not (assets/'fire.mp4').exists():
 subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(assets/'source.webm'),'-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p',str(assets/'fire.mp4')],check=True)
def decode(args):return subprocess.check_output(['ffmpeg','-loglevel','error',*args,'-f','rawvideo','-pix_fmt','rgb24','-'])
raw=decode(['-i',str(assets/'fire.mp4'),'-vf','fps=1','-frames:v','30']);frames=np.frombuffer(raw,dtype=np.uint8).reshape(-1,h,w,3)
# Temporal median suppresses the moving flame while estimating stationary masonry.
bg=np.median(frames[:,:,:,1],axis=0).astype(np.float32)
current=np.frombuffer(decode(['-ss','2','-i',str(assets/'fire.mp4'),'-frames:v','1']),dtype=np.uint8).reshape(h,w,3)
g=current[:,:,1].astype(np.float32);r=current[:,:,0].astype(np.float32)
dynamic=np.clip((g-bg-14)/60,0,1)
core=np.clip((g-120)/75,0,1)*np.clip((g/(r+1)-.30)/.18,0,1)
alpha=np.maximum(dynamic,core)
# Remove isolated compression/noise pixels without applying blur to source RGB.
padded=np.pad(alpha,1,mode='edge');alpha=np.median(np.stack([padded[j:j+h,i:i+w] for j in range(3) for i in range(3)]),axis=0)
rgba=np.dstack((current,(alpha*255).astype(np.uint8))).astype(np.uint8)
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgba','-s',f'{w}x{h}','-i','-','-frames:v','1',str(assets/'fire_still.png')],input=rgba.tobytes(),check=True)
print('Temporal fire matte prepared',flush=True)
