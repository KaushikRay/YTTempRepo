"""Resumable low-resolution preview: 36 samples from a 24 fps scene, encoded at 12 fps."""
import bpy,os,json,time,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'renders/motion';out.mkdir(exist_ok=True);frames=out/'frames';frames.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'storm_lounge.blend'))
s=bpy.context.scene;s.render.threads_mode='FIXED';s.render.threads=5;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=12;s.cycles.use_denoising=True;s.cycles.denoiser='OPENIMAGEDENOISE';s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
source_frames=list(range(1,73,2));fingerprint=hashlib.sha256((root/'storm_lounge.blend').read_bytes()+Path(__file__).read_bytes()).hexdigest();manifest_path=out/'run.json'
if manifest_path.exists():
 old=json.loads(manifest_path.read_text())
 if old['fingerprint']!=fingerprint and list(frames.glob('full_*.png')):raise RuntimeError('Preview outputs belong to a different scene; archive them before rerendering')
manifest={'fingerprint':fingerprint,'width':640,'height':360,'fps':12,'duration_seconds':3,'expected_frames':36,'source_frames':source_frames,'samples':12,'completed':0,'status':'rendering','loop_validated':False}
manifest_path.write_text(json.dumps(manifest,indent=2));started=time.monotonic()
for index,frame in enumerate(source_frames,1):
 target=frames/f'full_{index:04d}.png'
 if not target.exists() or target.stat().st_size<100:
  s.frame_set(frame);s.render.filepath=str(target);bpy.ops.render.render(write_still=True)
 manifest['completed']=index;manifest['last_source_frame']=frame;manifest['elapsed_seconds']=round(time.monotonic()-started,1);manifest_path.write_text(json.dumps(manifest,indent=2))
 print(f'MOTION PROGRESS: {index}/36 frames; scene frame {frame}; elapsed {manifest["elapsed_seconds"]} s',flush=True)
manifest['status']='frames_complete';manifest_path.write_text(json.dumps(manifest,indent=2));print('MOTION RENDER COMPLETE',flush=True)
