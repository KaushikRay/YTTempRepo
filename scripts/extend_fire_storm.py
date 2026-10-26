"""Extend existing fire frames 73–144 without touching approved frames 1–72."""
from pathlib import Path
import json,subprocess,numpy as np,hashlib
root=Path(__file__).resolve().parents[1];assets=root/'assets/fire';out=assets/'sequence';w,h=1280,720
meta=json.loads((out/'sequence.json').read_text())
if meta['frame_count'] not in [72,144]:raise RuntimeError('Unexpected baseline fire sequence')
basehash={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob('fire_*.png'))[:72]}
def decode(args):return subprocess.check_output(['ffmpeg','-threads','2','-loglevel','error',*args,'-f','rawvideo','-pix_fmt','rgb24','-'])
raw=decode(['-i',str(assets/'fire.mp4'),'-vf',f'fps=1,scale={w}:{h}','-frames:v','30']);arr=np.frombuffer(raw,dtype=np.uint8).reshape(-1,h,w,3);bg=np.median(arr[:,:,:,1],axis=0).astype(np.float32);del arr,raw
raw=decode(['-ss','5','-i',str(assets/'fire.mp4'),'-t','3','-vf',f'fps=24,scale={w}:{h}','-frames:v','72']);arr=np.frombuffer(raw,dtype=np.uint8).reshape(-1,h,w,3)
if len(arr)!=72:raise RuntimeError('Source extension does not contain 72 frames')
enc=subprocess.Popen(['ffmpeg','-y','-threads','2','-loglevel','error','-f','rawvideo','-pix_fmt','rgba','-s',f'{w}x{h}','-r','24','-i','-','-frames:v','72','-start_number','73',str(out/'fire_%04d.png')],stdin=subprocess.PIPE);flux=list(meta['flux'][:72])
for i,current in enumerate(arr,73):
 g=current[:,:,1].astype(np.float32);r=current[:,:,0].astype(np.float32);alpha=np.maximum(np.clip((g-bg-14)/60,0,1),np.clip((g-120)/75,0,1)*np.clip((g/(r+1)-.30)/.18,0,1));pad=np.pad(alpha,1,mode='edge');alpha=np.median(np.stack([pad[j:j+h,k:k+w] for j in range(3) for k in range(3)]),axis=0);flux.append(float(np.mean((.2126*r+.7152*g+.0722*current[:,:,2])*alpha)));rgba=np.dstack((current,(alpha*255).astype(np.uint8))).astype(np.uint8);enc.stdin.write(rgba.tobytes())
 if i%12==0:print(f'FIRE EXTENSION: {i}/144',flush=True)
enc.stdin.close()
if enc.wait()!=0:raise RuntimeError('Extension encoding failed')
assert all(hashlib.sha256((out/n).read_bytes()).hexdigest()==v for n,v in basehash.items())
meta.update(frame_count=144,duration_seconds=6,flux=flux);(out/'sequence.json').write_text(json.dumps(meta,indent=2));(root/'assets/fire/storm_baseline_hashes.json').write_text(json.dumps(basehash,indent=2));print('FIRE EXTENSION COMPLETE: approved first 72 images unchanged',flush=True)
