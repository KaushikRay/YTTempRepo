"""Render a six-second storm event, reusing only verified unchanged baseline frames."""
import bpy,json,time,hashlib,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'renders/storm_preview';frames=out/'frames';frames.mkdir(parents=True,exist_ok=True)
setup=json.loads((root/'renders/storm_setup.json').read_text());baseline=root/'renders/quality_preview';old=json.loads((baseline/'run.json').read_text());backup=Path('/workspace/scratch/storm-baseline/storm_lounge.blend')
if hashlib.sha256(backup.read_bytes()).hexdigest()!=setup['baseline_scene_sha256']:raise RuntimeError('Baseline scene backup mismatch')
# Verify the exact input fingerprint of the previously approved quality frames.
h=hashlib.sha256(backup.read_bytes()+(root/'scripts/render_quality.py').read_bytes())
for p in sorted((root/'assets/fire/sequence').glob('fire_*.png'))[:72]:h.update(p.read_bytes())
if h.hexdigest()!=old['fingerprint']:raise RuntimeError('Approved baseline inputs no longer match; reuse is unsafe')
bpy.ops.wm.open_mainfile(filepath=str(root/'storm_lounge.blend'));s=bpy.context.scene
assert s.render.fps==24 and s.frame_end==144
s.render.threads_mode='FIXED';s.render.threads=5;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=24;s.cycles.use_adaptive_sampling=True;s.cycles.adaptive_min_samples=8;s.cycles.adaptive_threshold=.05;s.cycles.use_denoising=True;s.cycles.denoiser='OPENIMAGEDENOISE';s.render.use_persistent_data=True;s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
h=hashlib.sha256((root/'storm_lounge.blend').read_bytes()+Path(__file__).read_bytes())
for p in sorted((root/'assets/fire/sequence').glob('fire_*.png')):h.update(p.read_bytes())
fingerprint=h.hexdigest();manifest_path=out/'run.json'
if manifest_path.exists():
 old_run=json.loads(manifest_path.read_text())
 if old_run['fingerprint']!=fingerprint and list(frames.glob('full_*.png')):raise RuntimeError('Different inputs require archiving old storm frames')
reused=set(setup['baseline_reusable_frames'])
for frame in reused:
 source=baseline/'frames'/f'full_{frame:04d}.png'
 if not source.exists():raise RuntimeError(f'Missing approved baseline frame {frame}')
 shutil.copyfile(source,frames/source.name)
manifest={'fingerprint':fingerprint,'width':960,'height':540,'fps':24,'duration_seconds':6,'expected_frames':144,'max_samples':24,'adaptive_min_samples':8,'adaptive_threshold':.05,'reused_frames':sorted(reused),'new_frames_total':len(setup['frames_to_render']),'new_frames_complete':0,'completed':len(reused),'status':'rendering','loop_validated':False}
manifest_path.write_text(json.dumps(manifest,indent=2));started=time.monotonic()
for frame in setup['frames_to_render']:
 target=frames/f'full_{frame:04d}.png'
 if not target.exists() or target.stat().st_size<100:
  s.frame_set(frame);s.render.filepath=str(target);bpy.ops.render.render(write_still=True)
 manifest['new_frames_complete']+=1;manifest['completed']=len(reused)+manifest['new_frames_complete'];manifest['last_source_frame']=frame;manifest['elapsed_seconds']=round(time.monotonic()-started,1);manifest_path.write_text(json.dumps(manifest,indent=2));print(f'STORM PROGRESS: new {manifest["new_frames_complete"]}/{manifest["new_frames_total"]}; total {manifest["completed"]}/144',flush=True)
if len(list(frames.glob('full_*.png')))!=144:raise RuntimeError('Missing final storm frames')
manifest['status']='frames_complete';manifest_path.write_text(json.dumps(manifest,indent=2));print('STORM FRAMES COMPLETE',flush=True)
