import bpy,json,hashlib
from pathlib import Path
r=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(r/'storm_lounge.blend'));s=bpy.context.scene
tex=next(n for n in bpy.data.materials['Licensed filmed fire'].node_tree.nodes if n.type=='TEX_IMAGE')
objects={key:next(o for o in bpy.data.objects if o.name.startswith(prefix)) for key,prefix in [('rain','Visible wind-driven storm rain'),('candle','Small volumetric candle flame'),('tree','Wind driven tree')]}
positions={}
for frame in [1,37,72]:
 s.frame_set(frame);bpy.context.view_layer.update();positions[str(frame)]={k:{'location':list(o.location),'rotation':list(o.rotation_euler)} for k,o in objects.items()}
 positions[str(frame)]['image_user_frame']=getattr(tex.image_user,'frame_current',None)
assert tex.image.source=='SEQUENCE' and tex.image_user.frame_duration==72
assert positions['1']['rain']['location']!=positions['72']['rain']['location']
assert positions['1']['tree']['rotation']!=positions['72']['tree']['rotation']
assert positions['1']['candle']['rotation']!=positions['72']['candle']['rotation']
files=sorted((r/'assets/fire/sequence').glob('fire_*.png'));unique=len({hashlib.sha256(f.read_bytes()).hexdigest() for f in files});assert len(files)==unique==72
report={'sequence_frames':72,'unique_fire_source_images':unique,'evaluated_animation_samples':positions,'fire_image_source':tex.image.source,'fire_image_path':tex.image.filepath,'passed':True}
(r/'renders/motion/runtime_checks.json').write_text(json.dumps(report,indent=2));print('ANIMATION RUNTIME CHECKS PASSED',flush=True)
