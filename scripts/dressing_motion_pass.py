"""Supported table linen, hearth integration and short diagnostic motion."""
import bpy,math,os
from pathlib import Path
from mathutils import Vector
r=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(r/'realism_study.blend'));s=bpy.context.scene
# A narrow cloth runner follows the tabletop and hangs over its near edge.
mat=bpy.data.materials['Scanned woven textile'].copy();mat.name='Worn linen table runner'
verts=[];faces=[]
for j in range(45):
 y=-3.25+j*.055
 for i in range(19):
  x=.15+(i/18-.5)*.55;z=.942+.005*math.sin(i*.9+j*.3)
  if y< -2.95:z-=min(.48,(-2.95-y)*1.5)
  verts.append((x,y,z))
for j in range(44):
 for i in range(18):
  k=j*19+i;faces.append((k,k+1,k+20,k+19))
me=bpy.data.meshes.new('Supported woven runner');me.from_pydata(verts,[],faces);me.materials.append(mat);uv=me.uv_layers.new()
for lp in me.loops:
 v=me.vertices[lp.vertex_index].co;uv.data[lp.index].uv=(v.x,v.y)
ob=bpy.data.objects.new('Supported worn table linen',me);bpy.context.collection.objects.link(ob);ob.modifiers.new('Fabric thickness','SOLIDIFY').thickness=.003
# Match the filmed source to its practical and retain its attribution.
fm=bpy.data.materials['Licensed filmed fire'];tex=next(n for n in fm.node_tree.nodes if n.type=='TEX_IMAGE')
tex.image=bpy.data.images.load(str(r/'assets/fire/fire.mp4'));tex.image.source='MOVIE';tex.image.filepath='//assets/fire/fire.mp4';tex.image_user.frame_start=1;tex.image_user.frame_offset=60;tex.image_user.frame_duration=72;tex.image_user.use_auto_refresh=True
s.frame_start=1;s.frame_end=48;s.render.fps=24
fire=bpy.data.objects['Hearth firelight'];fire.data.animation_data_clear();base=fire.data.energy
fire.data.driver_add('energy').driver.expression=f'{base}*(1+.055*sin(frame*.63)+.025*sin(frame*1.17))'
# Small independent leaf flex, with fixed petiole origins.
for i,o in enumerate(bpy.data.collections['Interior creeper'].objects):
 if o.type=='MESH':
  o.rotation_mode='XYZ';base=o.rotation_euler.x;o.driver_add('rotation_euler',0).driver.expression=f'{base}+.018*sin(frame*.11+{i*.73})'
for o in bpy.data.objects:
 if o.name.startswith('Window rain droplet'):
  z=o.location.z;o.driver_add('location',2).driver.expression=f'1.2+(({z-1.2}-(frame-1)*.004)%4.4)'
# Translate the near rain only a small distance over this short test.
o=bpy.data.objects.get('Storm layered tapered rain')
if o:o.driver_add('location',2).driver.expression='-.06*(frame-1)'
s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.cycles.samples=12;s.render.threads_mode='FIXED';s.render.threads=5
bpy.ops.wm.save_as_mainfile(filepath=str(r/'dressing_motion.blend'),compress=True)
out=r/'renders/dressing_motion';out.mkdir(exist_ok=True)
for frame in range(1,49,2):
 s.frame_set(frame);s.render.filepath=str(out/f'{frame:04}.png');bpy.ops.render.render(write_still=True);print('MOTION FRAME',frame,flush=True)
print('DRESSING MOTION COMPLETE',flush=True);os._exit(0)
