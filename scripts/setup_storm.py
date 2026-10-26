"""Six-second lightning test; retain approved scene outside the flash frames."""
import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector
root=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(root/'storm_lounge.blend'));s=bpy.context.scene
if s.frame_end!=72:raise RuntimeError('Expected the approved 72-frame baseline; setup is not run twice')
# Preserve a recoverable baseline scene outside the repository output files.
backup=Path('/workspace/scratch/storm-baseline');backup.mkdir(parents=True,exist_ok=True)
if not (backup/'storm_lounge.blend').exists():(backup/'storm_lounge.blend').write_bytes((root/'storm_lounge.blend').read_bytes())
baseline_sha=hashlib.sha256((root/'storm_lounge.blend').read_bytes()).hexdigest()
fire=bpy.data.objects['Hearth firelight'];baseline_energy={}
for frame in range(1,73):s.frame_set(frame);baseline_energy[frame]=fire.data.energy
seq=json.loads((root/'assets/fire/sequence/sequence.json').read_text());assert seq['frame_count']==144
tex=next(n for n in bpy.data.materials['Licensed filmed fire'].node_tree.nodes if n.type=='TEX_IMAGE');tex.image_user.frame_duration=144
s.frame_end=144;s.render.fps=24
# Extend only the fire-light curve; preserve all original integer-frame values.
mean=sum(seq['flux'][:72])/72;energy=baseline_energy[72]
for frame in range(73,145):
 target=360*max(.7,min(1.3,seq['flux'][frame-1]/mean));energy=.65*energy+.35*target;fire.data.energy=energy;fire.data.keyframe_insert(data_path='energy',frame=frame)
# Cold exterior area light: rays enter through the actual window openings.
data=bpy.data.lights.new('Storm lightning through windows','AREA');data.shape='DISK';data.size=7;data.color=(.73,.84,1);light=bpy.data.objects.new('Storm lightning through windows',data);bpy.context.collection.objects.link(light);light.location=(-1.1,11.5,7.5);light.rotation_euler=(Vector((-1.5,0,1.5))-light.location).to_track_quat('-Z','Y').to_euler();light.visible_camera=False;light.visible_glossy=False;light.visible_transmission=False
pulses={1:0,40:0,41:1200,42:5000,43:16000,44:9000,45:1500,46:0,47:0,48:11000,49:6500,50:1200,51:0,144:0}
for frame,value in pulses.items():data.energy=value;data.keyframe_insert(data_path='energy',frame=frame)
for fc in data.animation_data.action.fcurves:
 for key in fc.keyframe_points:key.interpolation='LINEAR'
# Sky emission follows the flash. Baseline stays exactly at its original value.
sky=bpy.data.materials['Moonlit storm cloud bank'];principled=sky.node_tree.nodes.get('Principled BSDF');base_sky=principled.inputs['Emission Strength'].default_value
for frame,value in pulses.items():principled.inputs['Emission Strength'].default_value=base_sky+2.0*value/16000;principled.inputs['Emission Strength'].keyframe_insert(data_path='default_value',frame=frame)
for fc in sky.node_tree.animation_data.action.fcurves:
 for key in fc.keyframe_points:key.interpolation='LINEAR'
# Small branched bolt beyond the trees; hidden outside the pulse frames.
mat=bpy.data.materials.new('Distant lightning channel');mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links;n.clear();out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');em.inputs['Color'].default_value=(.72,.83,1,1);em.inputs['Strength'].default_value=5;l.new(em.outputs[0],out.inputs[0])
def bolt(name,pts,r):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=2;sp=c.splines.new('POLY');sp.points.add(len(pts)-1)
 for point,co in zip(sp.points,pts):point.co=(*co,1)
 ob=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(ob);ob.data.materials.append(mat);ob.visible_shadow=False
 for frame,hidden in [(1,True),(41,False),(46,True),(48,False),(51,True),(144,True)]:ob.hide_render=hidden;ob.keyframe_insert(data_path='hide_render',frame=frame)
 return ob
bolts=[bolt('Distant main lightning channel',[(-2.25,18,9),(-2.4,18,8.1),(-2.16,18,7.4),(-2.5,18,6.7),(-2.35,18,5.9),(-2.65,18,5.1),(-2.55,18,4.4)],.018),bolt('Distant lightning branch',[(-2.5,18,6.7),(-3.05,18,6.3),(-3.1,18,5.9),(-3.55,18,5.5)],.008)]
# Reuse only baseline frames where the added event has no physical contribution.
reusable=[];render=[]
for frame in range(1,145):
 s.frame_set(frame);bpy.context.view_layer.update()
 if frame<=72:
  if abs(fire.data.energy-baseline_energy[frame])>1e-4:raise RuntimeError(f'Fire-light baseline changed at frame {frame}')
  if data.energy==0 and all(o.hide_render for o in bolts) and abs(principled.inputs['Emission Strength'].default_value-base_sky)<1e-6:reusable.append(frame);continue
 render.append(frame)
s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(root/'storm_lounge.blend'))
report={'duration_seconds':6,'fps':24,'expected_frames':144,'baseline_scene_sha256':baseline_sha,'baseline_reusable_frames':reusable,'frames_to_render':render,'main_flash_frame':43,'main_flash_seconds':42/24,'thunder_start_seconds':3.0,'thunder_delay_seconds':1.25,'flash_frames':[41,42,43,44,45,48,49,50],'seamless_loop':False}
(root/'renders/storm_setup.json').write_text(json.dumps(report,indent=2));print('STORM SETUP COMPLETE: '+json.dumps(report),flush=True)
