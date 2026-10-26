"""Reference-led still revision using CC0 scans. Preserves the approved motion file."""
import bpy,math,os,random,json
from pathlib import Path
from mathutils import Vector,Matrix
r=Path(__file__).resolve().parents[1];a=r/'assets/realism';random.seed(621)
bpy.ops.wm.open_mainfile(filepath=str(r/'storm_lounge.blend'));s=bpy.context.scene;s.frame_set(1)
def remove(prefixes):
 for o in list(bpy.data.objects):
  if o.name.startswith(tuple(prefixes)):bpy.data.objects.remove(o,do_unlink=True)
def pbr(asset,name,scale=3):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');tex=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='SCALE';mapping.inputs[3].default_value=1/scale;l.new(tex.outputs['UV'],mapping.inputs[0])
 for channel,socket in [('Diffuse','Base Color'),('Rough','Roughness'),('nor_gl','Normal')]:
  img=n.new('ShaderNodeTexImage');img.image=bpy.data.images.load(str(a/asset/(channel+'.jpg')),check_existing=True);l.new(mapping.outputs[0],img.inputs[0])
  if channel!='Diffuse':img.image.colorspace_settings.name='Non-Color'
  if channel=='nor_gl':normal=n.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.7;l.new(img.outputs[0],normal.inputs[1]);l.new(normal.outputs[0],p.inputs[socket])
  else:l.new(img.outputs[0],p.inputs[socket])
 return m
def panel(name,verts,uvs,mat):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],[(0,1,2,3)]);layer=me.uv_layers.new()
 for lp,uv in zip(layer.data,uvs):lp.uv=uv
 me.materials.append(mat);ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);return ob
wall=pbr('stone_wall_05','Scanned aged stone',5.0);floor=pbr('monastery_stone_floor','Scanned monastery flags',3.5)
remove(['Irregular back-wall','Irregular tavern side','Rough chimney face','Uneven flagstone','Left wall mortar','Right wall mortar','Back lime mortar','Back mortar','Heavy split oak bench','Bench splayed','Bench back post','Weathered bench','Oak ale cask','Rusty cask hoop','Cask stave','Cask wooden lid','Tabletop oak plank','Table leg','Trestle','Wind driven tree','Tree trunk','Branch','Foliage cluster','Interior tree','Interior fine branch','Interior foliage','Climbing ivy leaves','Climbing ivy stem','Visible wind-driven storm rain'])
# Rectangular apertures remain backed by the existing shaped Gothic spandrels.
for x in [-6,6]:panel('Scan stone side wall',[(x,-6,0),(x,9,0),(x,9,9),(x,-6,9)],[(0,0),(15,0),(15,9),(0,9)],wall)
for lo,hi in [(-6,-3.25),(-1.15,-.95),(1.15,6)]:panel('Scan stone back wall',[(lo,9,0),(hi,9,0),(hi,9,9),(lo,9,9)],[(lo,0),(hi,0),(hi,9),(lo,9)],wall)
for bottom,top in [(0,1),(7.8,9)]:panel('Scan wall infill',[(-3.25,9,bottom),(1.15,9,bottom),(1.15,9,top),(-3.25,9,top)],[(-3.25,bottom),(1.15,bottom),(1.15,top),(-3.25,top)],wall)
panel('Scan stone floor',[(-6,-6,.065),(6,-6,.065),(6,9,.065),(-6,9,.065)],[(-6,-6),(6,-6),(6,9),(-6,9)],floor)
panel('Scan chimney face',[(5.12,1.1,3.4),(5.12,5.5,3.4),(5.12,5.5,9),(5.12,1.1,9)],[(1.1,3.4),(5.5,3.4),(5.5,9),(1.1,9)],wall)
def scan(asset,pos,height,angle=0):
 before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(a/asset/(asset+'.gltf')));objs=[o for o in bpy.data.objects if o not in before];bpy.context.view_layer.update();mesh=[o for o in objs if o.type=='MESH'];points=[o.matrix_world@Vector(v) for o in mesh for v in o.bound_box];low=Vector(tuple(min(v[i] for v in points) for i in range(3)));high=Vector(tuple(max(v[i] for v in points) for i in range(3)));factor=height/(high.z-low.z);anchor=Vector(((low.x+high.x)/2,(low.y+high.y)/2,low.z))
 parent=bpy.data.objects.new('CC0 '+asset,None);bpy.context.collection.objects.link(parent)
 for o in objs:
  if o.parent not in objs:o.parent=parent
 parent.matrix_world=Matrix.Translation(Vector(pos))@Matrix.Rotation(angle,4,'Z')@Matrix.Scale(factor,4)@Matrix.Translation(-anchor)
 print('SCAN IMPORT',asset,'original dimensions',tuple(high-low),'height',height,flush=True);return parent
scan('gothic_coffee_table',(.4,-1.85,.07),.84)
scan('ArmChair_01',(-2.4,-2.1,.07),1.15,math.radians(60));scan('ArmChair_01',(-2.5,6.8,.07),1.1,math.radians(-10))
scan('wine_barrel_01',(-4.85,5,.07),1.05);scan('wine_barrel_01',(-4.7,6.05,.07),.95)
if (a/'jug_01/jug_01.gltf').exists():
 remove(['Earthenware jug','Jug curved handle']);scan('jug_01',(.9,-.9,.94),.34)
if (a/'decorative_book_set_01/decorative_book_set_01.gltf').exists():
 remove(['Stacked leather-bound','Visible book page']);scan('decorative_book_set_01',(.3,-1.02,.94),.22)
# Reduce graphic effects: leadwork is fine iron, not a dominant black lattice.
for o in bpy.data.objects:
 if o.name.startswith('Diamond lead came'):o.data.bevel_depth=.0045
 if o.name.startswith('Window blue fill'):o.data.energy=125
 if o.name.startswith('Soft cool room bounce'):o.data.energy=65
 if o.name.startswith('Storm lightning'):o.data.animation_data_clear();o.data.energy=0
 if o.name.startswith('Distant lightning'):o.hide_render=True
 if o.name.startswith('Carpet beneath'):
  o.scale.x*=1.15
# Atmospheric window glass, retaining a partial view but hiding crude distant village detail.
m=bpy.data.materials['Cold rain-streaked glass'];nodes=m.node_tree.nodes
for n in nodes:
 if n.type=='MIX_SHADER':n.inputs[0].default_value=.26
 if n.type=='BSDF_TRANSPARENT':n.inputs['Color'].default_value=(.46,.55,.61,1)
# Fire: retain original filmed low/mid tones rather than cutting them into bright fragments.
mat=bpy.data.materials['Licensed filmed fire'];tex=next(n for n in mat.node_tree.nodes if n.type=='TEX_IMAGE');im=bpy.data.images.load(str(a/'fire_soft_plate.png'));im.pack();tex.image=im
for n in mat.node_tree.nodes:
 if n.type=='EMISSION':n.inputs['Strength'].default_value=.85
remove(['Charred log'])
fabric=pbr('fabric_pattern_05','Scanned woven textile',.8)
n=fabric.node_tree.nodes;l=fabric.node_tree.links;p=n.get('Principled BSDF');source=p.inputs['Base Color'].links[0].from_socket;tint=n.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;tint.inputs[2].default_value=(.28,.075,.035,1);l.new(source,tint.inputs[1]);l.new(tint.outputs[0],p.inputs['Base Color'])
remove(['Carpet beneath'])
panel('Woven seating rug',[(-4.7,-3.8,.08),(1.9,-3.8,.08),(1.9,2.2,.08),(-4.7,2.2,.08)],[(0,0),(2.5,0),(2.5,2.8),(0,2.8)],fabric)
for material in bpy.data.materials:
 if material.use_nodes and 'limestone' in material.name.lower():
  principled=material.node_tree.nodes.get('Principled BSDF')
  if principled:principled.inputs['Roughness'].default_value=.95;principled.inputs['Specular IOR Level'].default_value=.18

# Replace the most visible candle cluster with a scanned, worn brass set.
for ob in list(bpy.data.objects):
 if ob.name.startswith(('Detailed beeswax candle','Dark bent wick','Small volumetric candle flame','Tiny blue candle flame base','Blackened candle saucer','Wax puddle','Candle glow')) and ob.location.x<2 and ob.location.z<1.7:bpy.data.objects.remove(ob,do_unlink=True)
remove(['Thin hardened wax rivulet','Rustic bread'])
scan('brass_candleholders',(.45,-2.4,.925),.4)
d=bpy.data.lights.new('Scanned candle practical','POINT');d.energy=4;d.color=(1,.5,.2);d.shadow_soft_size=.05;ob=bpy.data.objects.new('Scanned candle practical',d);bpy.context.collection.objects.link(ob);ob.location=(.45,-2.4,1.28)

# More restrained warm lighting, with a broad diffuse hearth fill.
fire=bpy.data.objects['Hearth firelight'];fire.data.animation_data_clear();fire.data.energy=650;fire.data.shadow_soft_size=.7
cam=s.camera;cam.location=(-1.25,-5.2,1.65);cam.rotation_euler=(Vector((.3,4.9,1.65))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=22
s.view_settings.view_transform='AgX';s.view_settings.exposure=.45;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=int(os.environ.get('REALISM_PERCENT','50'));s.cycles.samples=int(os.environ.get('REALISM_SAMPLES','48'));s.cycles.use_denoising=True;s.cycles.denoiser='OPENIMAGEDENOISE';s.render.threads_mode='FIXED';s.render.threads=5;s.render.use_persistent_data=False
# Textures travel in the scene; source models/maps are retained separately with CC0 provenance.
for image in bpy.data.images:
 if image.source=='FILE' and image.filepath and not image.packed_file:
  try:image.pack()
  except RuntimeError:pass
bpy.data.texts.new('REALISM_ASSET_CREDITS.txt').write((a/'CREDITS.txt').read_text())
bpy.ops.wm.save_as_mainfile(filepath=str(r/'realism_study.blend'),compress=True);s.render.filepath=str(r/'renders/realism_study.png');print('REALISM PREVIEW RENDER START',flush=True);bpy.ops.render.render(write_still=True);print('REALISM PREVIEW COMPLETE',flush=True)
