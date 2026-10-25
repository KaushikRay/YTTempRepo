"""Create a three-second 24 fps RGBA fire sequence from the licensed source."""
from pathlib import Path
import subprocess,json,numpy as np
root=Path(__file__).resolve().parents[1];assets=root/'assets/fire';out=assets/'sequence';out.mkdir(exist_ok=True)
w,h=1280,720;fps=24;count=72

def decode(args):
 return subprocess.check_output(['ffmpeg','-threads','2','-loglevel','error',*args,'-f','rawvideo','-pix_fmt','rgb24','-'])
raw=decode(['-i',str(assets/'fire.mp4'),'-vf',f'fps=1,scale={w}:{h}','-frames:v','30'])
frames=np.frombuffer(raw,dtype=np.uint8).reshape(-1,h,w,3)
bg=np.median(frames[:,:,:,1],axis=0).astype(np.float32);del frames,raw
raw=decode(['-ss','2','-i',str(assets/'fire.mp4'),'-t','3','-vf',f'fps={fps},scale={w}:{h}','-frames:v',str(count)])
frames=np.frombuffer(raw,dtype=np.uint8).reshape(-1,h,w,3)
if len(frames)!=count:raise RuntimeError(f'Expected {count} source frames, got {len(frames)}')
flux=[]
# One encoder process writes the entire keyed PNG sequence.
encoder=subprocess.Popen(['ffmpeg','-y','-threads','2','-loglevel','error','-f','rawvideo','-pix_fmt','rgba','-s',f'{w}x{h}','-r',str(fps),'-i','-','-frames:v',str(count),str(out/'fire_%04d.png')],stdin=subprocess.PIPE)
for i,current in enumerate(frames):
 g=current[:,:,1].astype(np.float32);r=current[:,:,0].astype(np.float32)
 dynamic=np.clip((g-bg-14)/60,0,1);core=np.clip((g-120)/75,0,1)*np.clip((g/(r+1)-.30)/.18,0,1)
 alpha=np.maximum(dynamic,core);padded=np.pad(alpha,1,mode='edge')
 alpha=np.median(np.stack([padded[j:j+h,k:k+w] for j in range(3) for k in range(3)]),axis=0)
 flux.append(float(np.mean((.2126*r+.7152*g+.0722*current[:,:,2])*alpha)))
 rgba=np.dstack((current,(alpha*255).astype(np.uint8))).astype(np.uint8)
 encoder.stdin.write(rgba.tobytes())
 if (i+1)%12==0:print(f'FIRE PREPARATION: {i+1}/{count} keyed frames',flush=True)
encoder.stdin.close()
if encoder.wait()!=0:raise RuntimeError('PNG sequence encoding failed')
manifest={'frame_count':count,'fps':fps,'width':w,'height':h,'source_start_seconds':2,'duration_seconds':3,'flux':flux,'loop_validated':False}
(out/'sequence.json').write_text(json.dumps(manifest,indent=2));print('FIRE PREPARATION COMPLETE',flush=True)
