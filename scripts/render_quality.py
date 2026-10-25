"""True 24 fps / 960x540 quality preview using the existing 72-frame motion setup."""
import bpy,json,time,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'renders/quality_preview';frames=out/'frames';frames.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'storm_lounge.blend'));s=bpy.context.scene
if s.render.fps!=24 or s.frame_end<72:raise RuntimeError('Expected the approved 24 fps motion scene')
s.render.threads_mode='FIXED';s.render.threads=5;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=24;s.cycles.use_adaptive_sampling=True;s.cycles.adaptive_min_samples=8;s.cycles.adaptive_threshold=.05;s.cycles.use_denoising=True;s.cycles.denoiser='OPENIMAGEDENOISE';s.render.use_persistent_data=True;s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
hash_state=hashlib.sha256((root/'storm_lounge.blend').read_bytes()+Path(__file__).read_bytes())
for path in sorted((root/'assets/fire/sequence').glob('fire_*.png')):hash_state.update(path.read_bytes())
fingerprint=hash_state.hexdigest();manifest_path=out/'run.json'
if manifest_path.exists():
 old=json.loads(manifest_path.read_text())
 if old['fingerprint']!=fingerprint and list(frames.glob('full_*.png')):raise RuntimeError('Existing quality frames belong to different inputs; archive them first')
manifest={'fingerprint':fingerprint,'width':960,'height':540,'fps':24,'duration_seconds':3,'expected_frames':72,'max_samples':24,'adaptive_min_samples':8,'adaptive_threshold':.05,'completed':0,'status':'rendering','loop_validated':False}
manifest_path.write_text(json.dumps(manifest,indent=2));started=time.monotonic()
for index in range(1,73):
 target=frames/f'full_{index:04d}.png'
 if not target.exists() or target.stat().st_size<100:
  s.frame_set(index);s.render.filepath=str(target);bpy.ops.render.render(write_still=True)
 manifest['completed']=index;manifest['elapsed_seconds']=round(time.monotonic()-started,1);manifest_path.write_text(json.dumps(manifest,indent=2));print(f'QUALITY PROGRESS: {index}/72; elapsed {manifest["elapsed_seconds"]} s',flush=True)
manifest['status']='frames_complete';manifest_path.write_text(json.dumps(manifest,indent=2));print('QUALITY FRAMES COMPLETE',flush=True)
