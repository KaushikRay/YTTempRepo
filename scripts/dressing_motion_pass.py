"""Detailed dressing, grounded fuel and persistent replenishing rain.
Run DIAGNOSTIC=1, STILL=1 or the default 48-frame motion test (24 fps).
"""
import bpy,math,os,json,random,hashlib
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
r=Path(__file__).resolve().parents[1];rng=random.Random(341);bpy.ops.wm.open_mainfile(filepath=str(r/'realism_study.blend'));s=bpy.context.scene
# Keep this diagnostic free of inherited lightning visibility/sky keyframes.
s.frame_set(1)
for event in bpy.data.objects:
 if 'lightning' in event.name.lower():
  if event.type=='LIGHT':event.data.animation_data_clear();event.data.energy=0
  else:event.animation_data_clear();event.hide_render=True
sky=bpy.data.materials.get('Moonlit storm cloud bank')
if sky and sky.use_nodes:sky.node_tree.animation_data_clear()
out=r/'renders/dressing_motion';out.mkdir(exist_ok=True);frames=out/'frames';frames.mkdir(exist_ok=True)
with bpy.data.libraries.load(str(r/'assets/dressing/dressing.blend'),link=True) as (src,dst):dst.collections=['metal_jug','wooden_bowl_02','dry_branches_medium_01','food_apple_01','carved_wooden_plate']
collections={c.name:c for c in dst.collections}
def instance(name,asset,pos,height,angle=0):
 o=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(o);o.instance_type='COLLECTION';o.instance_collection=collections[asset];o.location=pos;o.scale=(height,)*3;o.rotation_euler.z=angle;return o

def bvh(objects):
 bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get();v=[];f=[]
 for ob in objects:
  if ob.type!='MESH':continue
  eo=ob.evaluated_get(dep);me=eo.to_mesh();base=len(v);v.extend(eo.matrix_world@p.co for p in me.vertices);f.extend(tuple(base+i for i in p.vertices) for p in me.polygons);eo.to_mesh_clear()
 return BVHTree.FromPolygons(v,f)
table=next(o for o in bpy.data.objects if o.name.startswith('CC0 gothic_coffee_table'));surface=bvh(table.children_recursive)
def top(x,y):
 hit=surface.ray_cast(Vector((x,y,2)),Vector((0,0,-1)),2)[0];assert hit is not None,(x,y);return hit.z+.003
for ob in list(bpy.data.objects):
 if ob.name.startswith(('Torus','Pewter cup','Linen table napkin')) and ob.location.z<1.5:bpy.data.objects.remove(ob,do_unlink=True)
instance('Dressed aged pitcher','metal_jug',(-.38,-1.05,top(-.38,-1.05)),.29,.3)
instance('Dressed wooden serving bowl','wooden_bowl_02',(-.27,-1.85,top(-.27,-1.85)),.13,-.2)
instance('Dressed carved plate','carved_wooden_plate',(.92,-2.25,top(.92,-2.25)),.035,.4)
for i,(x,y,z) in enumerate([(-.32,-1.9,.955),(-.19,-1.84,.96),(-.31,-1.76,.958)]):instance('Dressed apple '+str(i),'food_apple_01',(x,y,z),.075,rng.random()*6.28)
# Runner rests on the measured top, with a hanging edge past y=-2.935.
mat=bpy.data.materials['Aged flax linen'].copy();mat.name='Muted woven table runner'
mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.18,.13,.08,1)
for n in mat.node_tree.nodes:
 if n.type=='MIX_RGB':n.inputs[2].default_value=(.3,.22,.13,1)
verts=[];faces=[]
for j in range(51):
 y=-3.35+j*.05
 for i in range(17):
  x=.28+(i/16-.5)*.40;z=.916+.003*math.sin(i*.7+j*.25)
  if y< -2.93:z=.916-(-2.93-y)*1.2
  verts.append((x,y,z))
for j in range(50):
 for i in range(16):
  k=j*17+i;faces.append((k,k+1,k+18,k+17))
def cloth(name,verts,faces):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.materials.append(mat);uv=me.uv_layers.new()
 for lp in me.loops:
  v=me.vertices[lp.vertex_index].co;uv.data[lp.index].uv=(v.x,v.y)
 for p in me.polygons:p.use_smooth=True
 ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);ob.modifiers.new('Woven thickness','SOLIDIFY').thickness=.003;return ob
cloth('Supported table runner',verts,faces)
# Static drape follows the actual sofa surface; no cloth simulation is claimed.
sofa=next(o for o in bpy.data.objects if o.name.startswith('CC0 sofa_03'));support=bvh(sofa.children_recursive);rotation=Matrix.Rotation(math.radians(25),3,'Z');centre=Vector((-2.35,-.9,0));verts=[];faces=[]
for j in range(61):
 v=.15-j*.02
 for i in range(25):
  u=-.95+i*.025;point=centre+rotation@Vector((u,v,0));hit=support.ray_cast(Vector((point.x,point.y,2)),Vector((0,0,-1)),2)[0]
  z=hit.z+.006 if hit else max(.15,.59-max(0,-v-.4)*1.0)
  verts.append((point.x,point.y,z+.003*math.sin(i*.8+j*.3)))
for j in range(60):
 for i in range(24):
  k=j*25+i;faces.append((k,k+1,k+26,k+25))
cloth('Sofa surface fitted wool throw',verts,faces)
# Detailed charred branch geometry rests on the ash bed, in front of the flame.
fuel_checks=[]
for i in range(2):
 ob=instance('Grounded charred fuel '+str(i),'dry_branches_medium_01',(0,0,0),.8,0);ob.matrix_world=Matrix.Rotation(math.pi/2,4,'X')@Matrix.Rotation(.4+i*.8,4,'Z')@Matrix.Scale(.8,4)
 fitroot=bpy.data.objects.new('Fuel support fit '+str(i),None);bpy.context.collection.objects.link(fitroot);ob.parent=fitroot
 def actual_points():
  bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();points=[]
  for item in dg.object_instances:
   if item.is_instance and item.parent and item.parent.original.name==ob.name and item.object.type=='MESH':points.extend(item.matrix_world@v.co for v in item.object.data.vertices)
  assert points;return points
 points=actual_points();lo=Vector(tuple(min(p[a] for p in points) for a in range(3)));hi=Vector(tuple(max(p[a] for p in points) for a in range(3)));dims=hi-lo
 fitroot.scale=(.65/dims.x,1.6/dims.y,.28/dims.z);fit=Matrix.Diagonal((*fitroot.scale,1));lo=fit@lo;hi=fit@hi;fitroot.location=Vector((4.98+i*.13,2.9+i*.7,.30))-Vector(((lo.x+hi.x)/2,(lo.y+hi.y)/2,lo.z))
 points=actual_points();lo=[min(p[a] for p in points) for a in range(3)];hi=[max(p[a] for p in points) for a in range(3)];assert abs(lo[2]-.3)<.002 and abs(hi[2]-.58)<.002,(lo,hi)
 fuel_checks.append({'min':lo,'max':hi})
(out/'fuel_check.json').write_text(json.dumps(fuel_checks,indent=2))

fm=bpy.data.materials['Licensed filmed fire'];tex=next(n for n in fm.node_tree.nodes if n.type=='TEX_IMAGE');tex.image=bpy.data.images.load(str(r/'assets/dressing/fire_rgb_24.mp4'));tex.image.source='MOVIE';tex.image.filepath='//assets/dressing/fire_rgb_24.mp4';tex.image_user.frame_start=1;tex.image_user.frame_offset=0;tex.image_user.frame_duration=48;tex.image_user.use_auto_refresh=True
fire=bpy.data.objects['Hearth firelight'];fire.data.animation_data_clear();base=fire.data.energy
flux=json.loads((r/'assets/dressing/fire_flux.json').read_text())['flux'];mean=sum(flux)/len(flux);energy=base
for frame,value in enumerate(flux,1):
 energy=.6*energy+.4*base*max(.78,min(1.22,value/mean));fire.data.energy=energy;fire.data.keyframe_insert(data_path='energy',frame=frame)
# Preserve quaternion poses when enabling small Euler leaf flex.
for i,o in enumerate(bpy.data.collections['Interior creeper'].objects):
 if o.type=='MESH':
  rot=o.rotation_quaternion.to_euler('XYZ') if o.rotation_mode=='QUATERNION' else o.rotation_euler.copy();o.rotation_mode='XYZ';o.rotation_euler=rot;o.driver_add('rotation_euler',0).driver.expression=f'{rot.x}+.01*sin(frame*.11+{i*.73})'
# Every streak wraps independently behind opaque jambs/sills. Driver expressions
# persist in the Blender file; no Python frame handler or auto-run is required.
old=bpy.data.objects.get('Storm layered tapered rain');rainmat=old.data.materials[0];bpy.data.objects.remove(old,do_unlink=True)
me=bpy.data.meshes.new('Shared tapered rain streak');me.from_pydata([(-.5,0,0),(.5,0,0),(.5,0,-1),(-.5,0,-1)],[],[(0,1,2,3)]);me.materials.append(rainmat);uv=me.uv_layers.new()
for lp,co in zip(uv.data,[(0,0),(1,0),(1,1),(0,1)]):lp.uv=co
next(n for n in rainmat.node_tree.nodes if n.type=='EMISSION').inputs['Strength'].default_value=1.3
rain=bpy.data.collections.new('Replenishing exterior rain');s.collection.children.link(rain);seeds=[]
for i in range(2800):
 cx=-2.2 if i<1400 else .1;x=rng.uniform(-1.06,1.06);z=rng.uniform(.65,8.0);speed=rng.uniform(.12,.24);o=bpy.data.objects.new('Recycling rain '+str(i),me);rain.objects.link(o);o.location=(cx+x,rng.uniform(9.15,11.8),z);o.rotation_euler.y=.14;o.scale=(rng.uniform(.004,.009),1,rng.uniform(.07,.24))
 o.driver_add('location',2).driver.expression=f'.65+(({z-.65:.8f}-(frame-1)*{speed:.8f})%7.35)';o.driver_add('location',0).driver.expression=f'{cx}-1.06+(({x+1.06:.8f}-(frame-1)*.008)%2.12)';seeds.append((z,speed))
counts=[sum(5.7<.65+((z-.65-(f-1)*v)%7.35)<7.4 for z,v in seeds) for f in range(1,145)]
assert min(counts)/max(counts)>.75
for lib in bpy.data.libraries:
 if lib.filepath.endswith('/dressing.blend'):lib.filepath='//assets/dressing/dressing.blend'
s.render.use_motion_blur=False
s.frame_start=1;s.frame_end=48;s.render.fps=24;s.render.threads_mode='FIXED';s.render.threads=5;s.frame_set(1)
s.render.resolution_x=1280 if os.getenv('STILL') else 640;s.render.resolution_y=720 if os.getenv('STILL') else 360;s.render.resolution_percentage=100;s.cycles.samples=96 if os.getenv('STILL') else 24 if os.getenv('DIAGNOSTIC') else 12
bpy.ops.wm.save_as_mainfile(filepath=str(r/'dressing_motion.blend'),compress=True)
(out/'build_check.json').write_text(json.dumps({'rain_objects':len(seeds),'upper_band_count_min':min(counts),'upper_band_count_max':max(counts),'tested_timeline_frames':144,'cloth':'Static surface-fitted drape, not simulated','new_assets':'assets/dressing/CREDITS.txt'},indent=2))
if os.getenv('STILL') or os.getenv('DIAGNOSTIC'):
 s.render.filepath=str(out/('still.png' if os.getenv('STILL') else 'diagnostic.png'));bpy.ops.render.render(write_still=True)
else:
 s.render.use_persistent_data=True
 signature=hashlib.sha256(Path(__file__).read_bytes())
 for source in [r/'realism_study.blend',r/'assets/dressing/dressing.blend',r/'assets/exterior/vegetation.blend',r/'assets/dressing/fire_rgb_24.mp4']:signature.update(hashlib.sha256(source.read_bytes()).digest())
 signature=signature.hexdigest();cache=out/'motion_signature.json'
 if not cache.exists() or json.loads(cache.read_text()).get('signature')!=signature:
  for old in frames.glob('0*.png'):old.unlink()
 cache.write_text(json.dumps({'signature':signature,'fps':24,'frames':48,'width':640,'height':360,'samples':12},indent=2))
 for frame in range(1,49):
  if (frames/f'{frame:04}.png').exists():print('RESUMED FRAME',frame,flush=True);continue
  s.frame_set(frame);s.render.filepath=str(frames/f'{frame:04}.png');bpy.ops.render.render(write_still=True);print('MOTION FRAME',frame,flush=True)
s.frame_set(1);s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.cycles.samples=96;s.render.filepath='//renders/dressing_motion/still.png'
bpy.ops.wm.save_as_mainfile(filepath=str(r/'dressing_motion.blend'),compress=True)
print('DRESSING MOTION COMPLETE',flush=True);os._exit(0)
