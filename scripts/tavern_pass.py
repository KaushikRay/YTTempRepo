"""Reference-led rustic tavern revision. Real-fire footage required, never fabricated."""
import json
print('PROGRESS: rebuilding rustic tavern masonry and furnishings',flush=True)
# Remove the polished lounge seating and clean modular wall blocks.
remove_prefixes(['Staggered back','Staggered side','Chimney breast limestone','Sofa oak base','Leather sofa back','Rolled leather arm','Soft seat cushion','Slumped back pillow','Procedural hearth gas envelope','Blanket over foreground sofa'])
# Real cut/rough stone: varied course heights and widths, chamfered corners,
# non-planar chipped faces, narrow pale mortar rather than black grid seams.
roughstones=[material('Old tavern rubble limestone %02d'%i,(.19+i*.008,.178+i*.007,.15+i*.006),.94,noise=7) for i in range(9)]
for m in roughstones:
 n=m.node_tree.nodes;l=m.node_tree.links;geo=n.new('ShaderNodeNewGeometry')
 for t in list(n):
  if t.bl_idname=='ShaderNodeTexNoise':l.new(geo.outputs['Position'],t.inputs['Vector']);t.inputs['Scale'].default_value=14;t.inputs['Roughness'].default_value=.8
  if t.bl_idname=='ShaderNodeBump':t.inputs['Strength'].default_value=.65;t.inputs['Distance'].default_value=.025
mortar.diffuse_color=(.16,.15,.125,1);mortar.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.16,.15,.125,1)
# Local stone coordinate system: u is horizontal, v is depth, z is vertical.
def rubble(name,cx,cy,cz,width,height,axis='BACK'):
 cut=random.uniform(.015,.065);w=width/2;h=height/2
 ring=[(-w+cut,-h), (w-cut,-h),(w,-h+cut),(w,h-cut),(w-cut,h),(-w+cut,h),(-w,h-cut),(-w,-h+cut)]
 verts=[]
 for depth in [0,.32]:
  for u,z in ring:
   u+=random.uniform(-.008,.008);z+=random.uniform(-.012,.012);v=depth+random.uniform(-.012,.012)
   verts.append((cx+u,cy+v,cz+z) if axis=='BACK' else (cx+v,cy+u,cz+z))
 # Central front vertex introduces fractured facets rather than a perfect slab.
 verts.append((cx,cy-random.uniform(.006,.035),cz) if axis=='BACK' else (cx-random.uniform(.006,.035),cy,cz))
 faces=[(i,(i+1)%8,16) for i in range(8)]+[(i,i+8,(i+1)%8+8,(i+1)%8) for i in range(8)]+[tuple(range(8,16))]
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.materials.append(random.choice(roughstones));ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob)
 b=ob.modifiers.new('Soft chipped edges','BEVEL');b.width=.008;b.segments=2
 return ob
# Cover the back-wall mortar except the actual window apertures.
for a,b in [(-6.1,-3.25),(-1.15,-.95),(1.15,6.1)]:cube('Back lime mortar',((a+b)/2,9.12,4.5),(b-a,.2,9),mortar)
cube('Back mortar under windows',(-1.05,9.12,.45),(4.4,.2,.9),mortar)
cube('Back mortar above windows',(-1.05,9.12,8.5),(4.4,.2,1.1),mortar)
z=.0;row=0
while z<9:
 height=random.uniform(.25,.48);center=z+height/2;u=-6.1-random.uniform(0,.5)
 while u<6.1:
  width=random.uniform(.36,.95);spans=[(max(-6.1,u),min(6.1,u+width))]
  if .8<center<7.8:
   for lo,hi in [(-3.25,-1.15),(-.95,1.15)]:
    pieces=[]
    for a,b in spans:
     if b<=lo or a>=hi:pieces.append((a,b))
     else:
      if a<lo:pieces.append((a,lo))
      if b>hi:pieces.append((hi,b))
    spans=pieces
  for a,b in spans:
   if b-a>.07:rubble('Irregular back-wall stone',(a+b)/2,8.94,center,b-a-.008,height-.012)
  u+=width
 for side in [-1,1]:
  u=-6.2-random.random()*.6
  while u<9.2:
   width=random.uniform(.38,1.05);ob=rubble('Irregular tavern side stone',side*5.86,u+width/2,center,width-.01,height-.012,'SIDE')
   if side==-1:
    # Mirror the left-wall stone so its chipped face points inward.
    for v in ob.data.vertices:v.co.x=2*side*5.86-v.co.x
   u+=width
 z+=height;row+=1
# Chimney cladding uses the same irregular geology.
z=3.48
while z<8.95:
 h=random.uniform(.26,.43);u=1.1
 while u<5.5:
  w=min(random.uniform(.4,.85),5.5-u)
  if w>.06:rubble('Rough chimney face',5.14,u+w/2,z+h/2,w-.012,h-.012,'SIDE')
  u+=w
 z+=h
# Timber is matte, scratched, and desaturated; no glossy red leather dominates.
rusticwood=material('Split and worn tavern oak',(.105,.066,.033),.88,noise=9)
n=rusticwood.node_tree.nodes;l=rusticwood.node_tree.links;tex=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(4,65,5);l.new(tex.outputs['Generated'],mapping.inputs[0])
for t in list(n):
 if t.bl_idname=='ShaderNodeTexNoise':l.new(mapping.outputs[0],t.inputs['Vector'])
for ob in bpy.data.objects:
 if ob.type=='MESH' and ob.data.materials and ob.data.materials[0]==wood:ob.data.materials[0]=rusticwood
# Left foreground bench and rear benches: thick oak, iron pegs, worn fabric.
def bench(x,y,length):
 for i in range(3):cube('Heavy split oak bench seat',(x+(i-1)*.25,y,.58),(.245,length,.13),rusticwood,.035)
 for yy in [y-length*.4,y+length*.4]:
  for xx in [x-.25,x+.25]:cube('Bench splayed leg',(xx,yy,.27),(.13,.16,.54),rusticwood,.02)
 for yy in [y-length/2+.1,y+length/2-.1]:cube('Bench back post',(x-.43,yy,.95),(.14,.15,1.65),rusticwood,.03)
 for z in [.98,1.24]:cube('Weathered bench back rail',(x-.43,y,z),(.12,length,.19),rusticwood,.035)
bench(-3.25,-1.7,4.8);bench(-2.4,7.3,2.7)
# Foreground trestle table retains the food/candle locations.
for ob in bpy.data.objects:
 if ob.name.startswith('Tabletop oak plank'):
  ob.dimensions.y=3.6;ob.dimensions.x*=1.08;ob.data.materials[0]=rusticwood
for y in [-2.9,-.65]:
 cube('Trestle heavy foot',(.4,y,.16),(1.65,.25,.19),rusticwood,.04)
 cube('Trestle support',(.4,y,.47),(.25,.25,.65),rusticwood,.03)
cube('Trestle cross stretcher',(.4,-1.7,.33),(.16,2.6,.18),rusticwood,.025)
# Old casks, stave seams, iron hoops, crate and stacked split firewood.
def barrel(x,y,z=0,r=.38,h=.95):
 profile=[(r*.85,0),(r,.22*h),(r*1.04,.5*h),(r,.8*h),(r*.85,h)]
 vessel('Oak ale cask',(x,y,z),profile,rusticwood)
 for zz,rr in [(.08,.9),(.3,1.015),(.73,1.015),(.92,.9)]:
  line('Rusty cask hoop',[(x+r*rr*math.cos(i*math.tau/64),y+r*rr*math.sin(i*math.tau/64),z+zz*h) for i in range(65)],.022,iron)
 for i in range(14):
  a=i*math.tau/14;line('Cask stave joint',[(x+r*rr*math.cos(a),y+r*rr*math.sin(a),z+zz*h) for rr,zz in [(.86,.02),(1.04,.5),(.86,.98)]],.004,iron)
 rod('Cask wooden lid',(x,y,z+h-.02),(x,y,z+h),r*.85,rusticwood)
barrel(-4.65,4.5);barrel(-4.6,5.4);barrel(3.6,7.5,r=.3,h=.8)
for i in range(18):
 y=5.65+(i%6)*.18;z=.19+(i//6)*.16;rod('Stacked split hearth fuel',(4.7,y,z),(5.3,y+.04,z+.02),.085,rusticwood)
# Iron hooks, a hanging pan, floor straw, and spilled small debris.
for y in [1.8,2.5]:line('Iron hearth hook',[(5.46,y,2.2),(5.18,y,2.2),(5.18,y,2.0)],.012,iron)
rod('Hanging pan handle',(5.16,2.5,2.08),(5.16,2.5,1.73),.015,iron);uv('Blackened skillet',(5.16,2.5,1.6),(.025,.18,.2),iron)
straw=material('Old dry straw',(.19,.13,.055),.95)
for i in range(150):
 x=random.uniform(-4.3,2);y=random.uniform(-3.5,6);a=random.random()*math.tau
 line('Scattered straw',[(x,y,.085),(x+.11*math.cos(a),y+.11*math.sin(a),.088)],.0014,straw)
print('PROGRESS: rustic room geometry complete',flush=True)
# Blackened masonry around the chimney, with an uneven soot fade.
soot=roughstones[3].copy();soot.name='Soot-stained old chimney stone';n=soot.node_tree.nodes;l=soot.node_tree.links;p=n.get('Principled BSDF');geo=n.new('ShaderNodeNewGeometry');sep=n.new('ShaderNodeSeparateXYZ');l.new(geo.outputs['Position'],sep.inputs[0]);fade=n.new('ShaderNodeMapRange');fade.inputs['From Min'].default_value=3.3;fade.inputs['From Max'].default_value=7;fade.inputs['To Min'].default_value=.12;fade.inputs['To Max'].default_value=.85;l.new(sep.outputs['Z'],fade.inputs[0]);mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=1;old=p.inputs['Base Color'].links[0].from_socket;l.new(old,mix.inputs[1]);l.new(fade.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],p.inputs['Base Color'])
for ob in bpy.data.objects:
 if ob.name.startswith('Rough chimney face'):ob.data.materials[0]=soot
 if ob.name.startswith(('Heavy split','Weathered bench','Tabletop')):
  for v in ob.data.vertices:v.co+=Vector((random.uniform(-.005,.005),random.uniform(-.005,.005),random.uniform(-.004,.004)))
for x in [-.2,1.05]:
 for y in [-3.35,-.3]:uv('Recessed forged tabletop nail',(x,y,.914),(.011,.011,.002),iron)
# Make the exterior storm legible in a still rather than hoping motion fixes it.
remove_prefixes(['Wind slanted rain','Fine rain streak'])
rainmat=bpy.data.materials.new('Backlit heavy rain');rainmat.use_nodes=True;n=rainmat.node_tree.nodes;l=rainmat.node_tree.links;n.clear();out=n.new('ShaderNodeOutputMaterial');tr=n.new('ShaderNodeBsdfTransparent');em=n.new('ShaderNodeEmission');em.inputs['Color'].default_value=(.42,.58,.72,1);em.inputs['Strength'].default_value=1.4;mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=.35;l.new(tr.outputs[0],mix.inputs[1]);l.new(em.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0])
# Slanted streaks at several depths, constrained to visible window openings.
for cx in [-2.2,.1]:
 for i in range(550):
  x=cx+random.uniform(-.88,.88);z=random.uniform(1.15,7.2)
  if z>5.8 and abs(x-cx)>.92*(1-math.sqrt((z-5.8)/1.7)):continue
  y=random.uniform(8.82,10.5);length=random.uniform(.05,.19);ob=rod('Visible wind-driven storm rain',(x,y,z),(x-.035,y,z-length),random.uniform(.0017,.0033),rainmat)
  # A cyclic drift is provisional; the whole animation still requires a moving test.
  origin=ob.location.copy();ob.keyframe_insert(data_path='location',frame=1);ob.location=origin+Vector((-.35,0,-2.6));ob.keyframe_insert(data_path='location',frame=49)
  for fc in ob.animation_data.action.fcurves:
   for key in fc.keyframe_points:key.interpolation='LINEAR'
   fc.modifiers.new('CYCLES')
# Surface rivulets are reflective glass, distinct from the rain beyond it.
water=material('Rainwater on exterior glass',(.18,.27,.32),.06);wp=water.node_tree.nodes.get('Principled BSDF');wp.inputs['Transmission Weight'].default_value=.92;wp.inputs['IOR'].default_value=1.333
for cx in [-2.2,.1]:
 for i in range(30):
  x=cx+random.uniform(-.8,.8);z=random.uniform(1.4,5.3);pts=[]
  for j in range(13):pts.append((x+.009*math.sin(j*.65+i),8.675,z-j*.032))
  line('Window rain rivulet',pts,random.uniform(.0018,.0038),water)
 for i in range(90):uv('Window rain droplet',(cx+random.uniform(-.82,.82),8.675,random.uniform(1.2,5.65)),(.004,.002,random.uniform(.006,.015)),water)
# Softer exterior visibility: village silhouette is subordinate to driving rain.
for ob in bpy.data.objects:
 if ob.name.startswith('Village lamplit'):ob.data.materials[0].node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=.8
 if ob.name.startswith('Window blue fill'):ob.data.energy=300
# Replace all invented hearth flames with real footage, if a verified asset exists.
# Until then only logs/embers remain: never silently substitute another fake flame.
fire_path=os.path.join(ROOT,'assets','fire','fire.mp4');manifest_path=os.path.join(ROOT,'assets','fire','source.json')
if os.path.isfile(fire_path) and os.path.isfile(manifest_path):
 with open(manifest_path) as f:meta=json.load(f)
 if not meta.get('commercial_use_verified') or not meta.get('source_url') or not meta.get('license_url'):raise RuntimeError('Real-fire asset requires verified source and commercial-use licence metadata')
 image=bpy.data.images.load(os.path.join(ROOT,'assets','fire','fire_still.png'));image.pack();bpy.data.texts.new('FIRE_ASSET_CREDITS.txt').write(meta['attribution'])
 mat=bpy.data.materials.new('Licensed filmed fire');mat.use_nodes=True;n=mat.node_tree.nodes;l=mat.node_tree.links;n.clear();out=n.new('ShaderNodeOutputMaterial');tex=n.new('ShaderNodeTexImage');tex.image=image;tex.image_user.use_auto_refresh=True;tex.image_user.use_cyclic=True;tex.image_user.frame_duration=int(meta['frame_count']);tex.image_user.frame_start=1;tex.image_user.frame_offset=0
 tr=n.new('ShaderNodeBsdfTransparent');em=n.new('ShaderNodeEmission');em.inputs['Strength'].default_value=1.5;l.new(tex.outputs['Color'],em.inputs['Color']);mix=n.new('ShaderNodeMixShader');l.new(tex.outputs['Alpha'],mix.inputs[0]);l.new(tr.outputs[0],mix.inputs[1]);l.new(em.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0])
 verts=[(4.7,1.85,.32),(4.7,4.75,.32),(4.7,4.75,1.95125),(4.7,1.85,1.95125)];me=bpy.data.meshes.new('Filmed fire integration card');me.from_pydata(verts,[],[(0,1,2,3)]);uvmap=me.uv_layers.new()
 for loop,uv in zip(uvmap.data,[(0,0),(1,0),(1,1),(0,1)]):loop.uv=uv
 me.materials.append(mat);ob=bpy.data.objects.new('Real-fire footage in hearth',me);bpy.context.collection.objects.link(ob)
 remove_prefixes(['Ember'])
 print('PROGRESS: licensed photographic fire still integrated; animation source retained',flush=True)
else:
 print('BLOCKED: real-fire footage not downloaded; hearth contains logs and embers only',flush=True)
# Save the visible rain phase; warm room remains dark enough to read the window.
s.frame_set(1);s.cycles.transparent_max_bounces=32
print('PROGRESS: tavern and readable-rain pass ready for preview',flush=True)
# Close-up correction: lime mortar must sit just behind the stone face, not
# fourteen centimetres back where it reads as black, empty cavities.
for ob in bpy.data.objects:
 if ob.name.startswith('Left wall mortar backing'):ob.location.x=-5.975;ob.dimensions.x=.2
 if ob.name.startswith('Right wall mortar backing'):ob.location.x=5.975;ob.dimensions.x=.2
 if ob.name.startswith('Back lime mortar'):ob.location.y=9.055;ob.dimensions.y=.2
for node in mortar.node_tree.nodes:
 if node.bl_idname=='ShaderNodeValToRGB':
  node.color_ramp.elements[0].color=(.12,.115,.1,1);node.color_ramp.elements[1].color=(.24,.225,.195,1)
