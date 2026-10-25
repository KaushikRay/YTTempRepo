"""Blender 4.3+: deterministic, asset-independent Gothic storm lounge study."""
import bpy, math, random, os
from mathutils import Vector
random.seed(29)
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)

def material(name,color,rough=.7,noise=0,metal=0):
 m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
 n=m.node_tree.nodes; l=m.node_tree.links; p=n.get('Principled BSDF'); p.inputs['Base Color'].default_value=(*color,1); p.inputs['Roughness'].default_value=rough; p.inputs['Metallic'].default_value=metal
 if noise:
  t=n.new('ShaderNodeTexNoise'); t.inputs['Scale'].default_value=noise; t.inputs['Detail'].default_value=4
  ramp=n.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].color=(*(v*.45 for v in color),1); ramp.color_ramp.elements[1].color=(*color,1)
  l.new(t.outputs['Fac'],ramp.inputs[0]); l.new(ramp.outputs[0],p.inputs['Base Color'])
  b=n.new('ShaderNodeBump'); b.inputs['Strength'].default_value=.3; b.inputs['Distance'].default_value=.06; l.new(t.outputs['Fac'],b.inputs['Height']); l.new(b.outputs[0],p.inputs['Normal'])
 return m
stone=[material('Weathered limestone %s'%i,(.22+i*.012,.205+i*.011,.175+i*.009),noise=7) for i in range(6)]
wood=material('Dark oak grain',(.14,.065,.025),noise=5); leather=material('Worn oxblood leather',(.105,.036,.019),.4,noise=32)
iron=material('Blackened iron',(.035,.028,.02),.35,metal=.7); wax=material('Beeswax',(.69,.49,.24),.55); cloth=material('Woven umber',(.12,.055,.029),noise=100); rug=material('Faded burgundy carpet',(.16,.045,.028),noise=80); leaf=material('Dark green foliage',(.055,.12,.035),noise=13)
def emit(name,col,power):
 m=material(name,col); p=m.node_tree.nodes.get('Principled BSDF'); p.inputs['Emission Color'].default_value=(*col,1); p.inputs['Emission Strength'].default_value=power; return m
flame=emit('Golden flame',(1,.29,.025),6); core=emit('Flame core',(1,.72,.24),10); ember=emit('Hot coals',(.9,.045,.003),3)
def cube(name,loc,scale,mat,bevel=0):
 verts=[(x*scale[0]/2,y*scale[1]/2,z*scale[2]/2) for x,y,z in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)])
 o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.location=loc;o.data.materials.append(mat)
 if bevel: b=o.modifiers.new('Soft worn edges','BEVEL'); b.width=bevel; b.segments=3; o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 return o
def uv(name,loc,scale,mat):
 key='_sphere_geometry'
 if key not in bpy.data.meshes:
  verts=[];faces=[]
  for j in range(9):
   t=math.pi*j/8
   for i in range(16):
    a=math.tau*i/16;verts.append((math.sin(t)*math.cos(a),math.sin(t)*math.sin(a),math.cos(t)))
  for j in range(8):
   for i in range(16):faces.append((j*16+i,j*16+(i+1)%16,(j+1)*16+(i+1)%16,(j+1)*16+i))
  me=bpy.data.meshes.new(key);me.from_pydata(verts,[],faces)
 me=bpy.data.meshes[key].copy();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.location=loc;o.scale=scale;o.data.materials.append(mat)
 for p in o.data.polygons:p.use_smooth=True
 return o
def rod(name,a,b,r,mat):
 d=Vector(b)-Vector(a);verts=[]
 for z in [-.5,.5]:
  for i in range(10):verts.append((r*math.cos(i*math.tau/10),r*math.sin(i*math.tau/10),z*d.length))
 faces=[tuple(range(9,-1,-1)),tuple(range(10,20))]+[(i,(i+1)%10,(i+1)%10+10,i+10) for i in range(10)]
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.location=(Vector(a)+Vector(b))/2;o.rotation_euler=d.to_track_quat('Z','Y').to_euler();o.data.materials.append(mat);return o

def line(name,pts,r,mat):
 c=bpy.data.curves.new(name,'CURVE'); c.dimensions='3D'; c.bevel_depth=r; c.bevel_resolution=2; s=c.splines.new('POLY'); s.points.add(len(pts)-1)
 for p,co in zip(s.points,pts):p.co=(*co,1)
 o=bpy.data.objects.new(name,c); bpy.context.collection.objects.link(o); o.data.materials.append(mat); return o
def light(name,loc,color,power,size=.3,kind='POINT',target=None):
 d=bpy.data.lights.new(name,kind); d.energy=power; d.color=color
 if kind=='AREA':d.shape='DISK';d.size=size
 else:d.shadow_soft_size=size
 o=bpy.data.objects.new(name,d); bpy.context.collection.objects.link(o);o.location=loc
 o.visible_camera=False;o.visible_glossy=False;o.visible_transmission=False
 if target:o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
 return o
# Camera looks north; room is 12 m wide, 16 m deep.
for j in range(20):
 for i in range(12): cube('Uneven flagstone',(i-5.5+(j%2)*.12,j*.8-6,.0),( .97,.77,.13),random.choice(stone),.035)
# Back wall: leave two tall lancet openings.
for z in range(17):
 for x in range(16):
  xx=-5.65+x*.75; zz=.27+z*.53
  if any(abs(xx-c)<1.02 and .9<zz<7.5 for c in [-2.2,.1]):continue
  cube('Back wall ashlar',(xx,9,zz),(.72,.5,.5),random.choice(stone),.035)
for side in [-1,1]:
 for z in range(17):
  for j in range(20):
   yy=-5.6+j*.75
   # Fireplace occupies right wall.
   cube('Side wall masonry',(side*6,yy,.27+z*.53),(.5,.72,.5),random.choice(stone),.028)
 for yy in [-3,1,5,8.5]:cube('Stone pier',(side*5.65,yy,4),(.5,.7,8),stone[2],.07)
cube('Dark oak ceiling',(0,1.5,9.0),(12.4,16,.3),wood)
# Lancet windows: pointed silhouette, stone surrounds, leaded panes.
glass=material('Cold rain-streaked glass',(.19,.29,.36),.17,noise=75); p=glass.node_tree.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=.68
for cx in [-2.2,.1]:
 w=.92; bottom=1.0; spring=5.8; top=7.5
 outline=[(cx-w,8.68,bottom),(cx-w,8.68,spring)]
 # Two quadratic curves join at apex.
 for k in range(21):
  t=k/20; outline.append((cx-w*(1-t)**2,8.68,spring+(top-spring)*(2*t-t*t)))
 for k in range(21):
  t=k/20; outline.append((cx+w*t*t,8.68,top-(top-spring)*t*t))
 outline.append((cx+w,8.68,bottom))
 mesh=bpy.data.meshes.new('Lancet pane');mesh.from_pydata(outline,[],[list(range(len(outline)))]);mesh.materials.append(glass);ob=bpy.data.objects.new('Leaded storm window',mesh);bpy.context.collection.objects.link(ob)
 # Spandrel panels close the rectangular rough opening above the arch.
 for side in [-1,1]:
  arc=[]
  for k in range(21):
   t=k/20;arc.append((cx+side*w*(1-t)**2,8.79,spring+(top-spring)*(2*t-t*t)))
  verts=arc+[(cx,8.79,7.95),(cx+side*1.08,8.79,7.95),(cx+side*1.08,8.79,spring)]
  me=bpy.data.meshes.new('Arch spandrel');me.from_pydata(verts,[],[list(range(len(verts)))]);me.materials.append(stone[2]);ob=bpy.data.objects.new('Arch spandrel masonry',me);bpy.context.collection.objects.link(ob)
 line('Carved lancet surround',outline,.13,stone[4]);rod('Deep window sill',(cx-1.07,8.55,1),(cx+1.07,8.55,1),.13,stone[3])
 for direction in [-1,1]:
  for offset in range(-16,23):
   pts=[]
   for k in range(161):
    zz=bottom+(top-bottom)*k/160; xx=cx+offset*.23+direction*(zz-bottom)*.47
    limit=w if zz<=spring else w*max(0,1-math.sqrt((zz-spring)/(top-spring)))
    if abs(xx-cx)<limit:pts.append((xx,8.64,zz))
   if len(pts)>1:line('Diamond lead came',pts,.012,iron)
 light('Window blue fill',(cx,8.15,4.6),(.38,.55,1),110,3,'AREA',(cx,1,1))
# Circular upper window.
line('Oculus stone ring',[( -1.05+.56*math.cos(t*math.tau/64),8.65,8.03+.56*math.sin(t*math.tau/64)) for t in range(65)],.12,stone[4])
uv('Oculus glass',(-1.05,8.8,8.03),(.49,.04,.49),glass)
# Fireplace faces west, large hood and deep black opening.
cube('Fireplace soot recess',(5.68,3.3,1.6),(.1,3.9,3.1),iron)
for y in [1.25,5.35]:cube('Fireplace carved jamb',(5.25,y,1.55),(1.15,.42,3.1),stone[3],.09)
cube('Oak mantel',(5.1,3.3,3.15),(1.65,4.8,.32),wood,.08)
cube('Towering chimney breast',(5.73,3.3,5.9),(.8,4.4,5.1),stone[2],.06)
cube('Raised stone hearth',(4.95,3.3,.18),(1.9,4.6,.3),stone[4],.06)
for i in range(7):
 y=2.35+i*.3; rod('Charred log',(4.8,y,.4),(5.5,y+.45,.6),.12,wood);uv('Ember',(4.95,y,.43),(.2,.16,.07),ember)
for i in range(22):
 y=random.uniform(2.5,4.2);z=random.uniform(.6,1.2);o=uv('Dancing hearth flame',(random.uniform(4.8,5.3),y,z),(.12,.15,random.uniform(.3,.65)),flame if i%3 else core)
 for f in [1,25,49,73,97,121,145]:
  o.scale.z=random.uniform(.25,.65);o.scale.y=random.uniform(.08,.18);o.keyframe_insert(data_path='scale',frame=f)
f=light('Hearth firelight',(4.4,3.3,1.25),(1,.32,.075),420,.65)
for frame in range(1,146,6):f.data.energy=random.uniform(320,470);f.data.keyframe_insert(data_path='energy',frame=frame)
# Sofa runs along left foreground; padded seats and cushions.
def sofa(x,y,length=3.9):
 cube('Sofa oak base',(x,y,.37),(1.75,length,.48),wood,.12)
 cube('Leather sofa back',(x-.72,y,.98),(.38,length,1.35),leather,.18)
 for end in [-1,1]:cube('Rolled leather arm',(x,y+end*(length/2-.15),.94),(1.8,.4,.65),leather,.19)
 for j in range(3):
  yy=y+(j-1)*(length-.7)/3;cube('Soft seat cushion',(x+.08,yy,.72),(1.35,(length-.7)/3-.03,.3),leather,.14)
  o=cube('Slumped back pillow',(x-.42,yy,1.2),(.35,.85,.75),leather,.16);o.rotation_euler[1]=-.2
sofa(-3.55,-1.65,4.6);sofa(-1.6,7,3.3)
# Foreground table with separate oak planks.
for i in range(5):cube('Tabletop oak plank',(-.2+i*.32,-.5,.83),(.31,2.9,.15),wood,.022)
for x in [-.1,1.0]:
 for y in [-1.65,.65]:cube('Table leg',(x,y,.39),(.15,.15,.78),wood,.025)
cube('Carpet beneath seating',(-1,-.5,.09),(5.7,5.5,.025),rug,.01)
# Candles, flame and practical lights.
def candle(x,y,z,h=.3,lit=True):
 rod('Wax candle',(x,y,z),(x,y,z+h),.047,wax)
 uv('Wax puddle',(x,y,z),(.09,.085,.018),wax)
 if lit:
  o=uv('Candle flame',(x,y,z+h+.055),(.025,.025,.085),core)
  for frame in [1,37,73,109,145]:o.scale.x=random.uniform(.018,.03);o.keyframe_insert(data_path='scale',frame=frame)
  light('Candle glow',(x,y,z+h+.1),(1,.48,.17),3,.08)
for i in range(10):candle(random.uniform(-.1,1.05),random.uniform(-1.7,.7),.93,random.uniform(.12,.4))
for i in range(19):candle(random.uniform(4.7,5.3),random.uniform(1.15,5.5),3.32,random.uniform(.15,.45))
for y in [2,6]:
 for x in [-5.4,5.4]:
  cube('Wall sconce bracket',(x,y,2.9),(.22,.18,.3),iron,.025);candle(x,y,3.05,.4);light('Sconce warm pool',(x*.95,y,3.3),(1,.42,.13),16,.2)
# Books, cups, platters, bread.
bookm=[material('Book binding '+str(i),c) for i,c in enumerate([(.12,.022,.015),(.07,.06,.025),(.16,.09,.035)])]
for i in range(4):
 o=cube('Stacked leather-bound volume',(.35,.3,.96+i*.075),(.45,.65,.07),bookm[i%3],.015);o.rotation_euler[2]=random.uniform(-.12,.12)
for x,y in [(.2,-1.3),(.85,-.4),(-.05,-.4)]:
 bpy.ops.mesh.primitive_torus_add(major_radius=.14,minor_radius=.025,location=(x,y,.94));bpy.context.object.data.materials.append(iron)
 uv('Rustic bread',(x,y,.99),(.12,.09,.065),wax)
for x,y in [(.9,.55),(.8,-1.55)]:rod('Pewter cup',(x,y,.92),(x,y,1.08),.065,iron)
# Exterior visible through glass: hills, tiny village, tree silhouettes.
night=material('Storm landscape',(.018,.034,.041),noise=3)
cube('Exterior ground',(0,18,-.35),(40,20,.3),night)
for i in range(12):
 x=random.uniform(-7,6);y=random.uniform(15,22);h=random.uniform(.6,1.1);cube('Distant village cottage',(x,y,h/2),(1,.9,h),wood,.02)
 # Steep pitched roofs.
 verts=[(x-.65,y-.6,h),(x+.65,y-.6,h),(x,y-.6,h+.65),(x-.65,y+.6,h),(x+.65,y+.6,h),(x,y+.6,h+.65)]
 me=bpy.data.meshes.new('Roof');me.from_pydata(verts,[],[(0,1,2),(3,5,4),(0,2,5,3),(2,1,4,5)]);me.materials.append(iron);ob=bpy.data.objects.new('Village roof',me);bpy.context.collection.objects.link(ob)
 cube('Village lamplit window',(x,y-.46,h*.6),(.15,.01,.2),emit('Distant amber',(.8,.35,.08),2))
for x,y in [(-3.4,12.3),(1.8,13.8),(4,16)]:
 pivot=bpy.data.objects.new('Wind driven tree',None);bpy.context.collection.objects.link(pivot);pivot.location=(x,y,0)
 objs=[rod('Tree trunk',(x,y,0),(x+.1,y,5),.11,wood)]
 for j in range(23):
  a=random.random()*math.tau;z=random.uniform(2.2,5.5);end=(x+math.cos(a)*random.uniform(.4,1.3),y+math.sin(a)*.8,z)
  objs.append(rod('Branch',(x,y,z-.8),end,.025,wood));objs.append(uv('Foliage cluster',end,(.65,.45,.65),leaf))
 for o in objs:o.parent=pivot;o.matrix_parent_inverse=pivot.matrix_world.inverted()
 for frame,angle in [(1,-.025),(37,.035),(73,-.015),(109,.025),(145,-.025)]:pivot.rotation_euler[1]=angle;pivot.keyframe_insert(data_path='rotation_euler',frame=frame)
# Rain streak geometry outside, animated as a group. Preview is a still study.
rain=emit('Rain silver blue',(.24,.36,.5),.45)
for i in range(750):
 x=random.uniform(-4,3);y=random.uniform(9.2,14);z=random.uniform(.5,8)
 rod('Wind slanted rain',(x,y,z),(x-.045,y,z+.19),.003,rain)
# Interior potted tree near window.
rod('Interior tree trunk',(1.5,7.8,.1),(1.5,7.8,3.9),.07,wood)
for i in range(45):
 a=random.random()*math.tau;r=random.uniform(.1,.85);uv('Interior foliage',(1.5+r*math.cos(a),7.8+r*math.sin(a),random.uniform(3,4.4)),(.27,.24,.3),leaf)
# Camera and render.
light('Soft cool room bounce',(-1,-1,5),(.36,.45,.65),35,5,'AREA',(0,4,0))
bpy.ops.object.camera_add(location=(-1.5,-6.0,1.85));cam=bpy.context.object;cam.name='Reference composition camera';cam.rotation_euler=(Vector((.1,4.5,3.2))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=22;bpy.context.scene.camera=cam
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=64;s.cycles.use_denoising=False;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=75;s.render.image_settings.file_format='PNG';s.render.fps=24;s.frame_start=1;s.frame_end=144;s.frame_set(36)
s.world.color=(.035,.035,.035);s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=.1
exec(compile(open(os.path.join(ROOT,'scripts','refine_scene.py')).read(),'refine_scene.py','exec'))
exec(compile(open(os.path.join(ROOT,'scripts','detail_scene.py')).read(),'detail_scene.py','exec'))
exec(compile(open(os.path.join(ROOT,'scripts','fire_candle_pass.py')).read(),'fire_candle_pass.py','exec'))
exec(compile(open(os.path.join(ROOT,'scripts','tavern_pass.py')).read(),'tavern_pass.py','exec'))
s.render.filepath=os.path.join(ROOT,'renders','composition.png');bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'storm_lounge.blend'));
if os.environ.get('LOUNGE_SKIP_RENDER')!='1':bpy.ops.render.render(write_still=True)
