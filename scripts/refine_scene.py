"""Second visual pass, executed inside build_scene.py before saving/rendering."""
# Uses the builder's geometry/material helpers and deterministic random seed.
print('PROGRESS: refinement — masonry, camera, cloth and fireplace', flush=True)
def remove_prefixes(prefixes):
 for ob in list(bpy.data.objects):
  if any(ob.name.startswith(p) for p in prefixes):bpy.data.objects.remove(ob,do_unlink=True)
remove_prefixes(['Back wall ashlar','Side wall masonry','Towering chimney breast','Interior foliage','Interior tree trunk','Dancing hearth flame'])
# Directional wood grain and smaller microstructure on leather/stone.
for m in stone:
 n=m.node_tree.nodes
 for node in n:
  if node.bl_idname=='ShaderNodeBump':node.inputs['Strength'].default_value=.22;node.inputs['Distance'].default_value=.024
for node in leather.node_tree.nodes:
 if node.bl_idname=='ShaderNodeBump':node.inputs['Strength'].default_value=.15;node.inputs['Distance'].default_value=.006
p=leather.node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.48
n=wood.node_tree.nodes;l=wood.node_tree.links;tex=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(3,40,4);l.new(tex.outputs['Generated'],mapping.inputs[0])
for node in n:
 if node.bl_idname=='ShaderNodeTexNoise':l.new(mapping.outputs[0],node.inputs['Vector'])
# Staggered masonry: shallow mortar seams, individual sizes and subtle rotations.
mortar=material('Recessed lime mortar',(.115,.105,.088),noise=16)
cube('Left wall mortar backing',(-6.15,1.4,4.5),(.3,15.8,9),mortar)
cube('Right wall mortar backing',(6.15,1.4,4.5),(.3,15.8,9),mortar)
for row in range(22):
 zz=.2+row*.405
 x=-6.4-(row%2)*.43
 while x<6:
  width=random.uniform(.65,1.1);cx=x+width/2
  # Split around the existing rough window apertures, retaining all other masonry.
  spans=[(x,x+width)]
  if .8<zz<7.8:
   for lo,hi in [(-3.25,-1.15),(-.95,1.15)]:
    out=[]
    for a,b in spans:
     if b<=lo or a>=hi:out.append((a,b))
     else:
      if a<lo:out.append((a,lo))
      if b>hi:out.append((hi,b))
    spans=out
  for a,b in spans:
   if b-a>.07:
    ob=cube('Staggered back limestone',((a+b)/2,9+random.uniform(-.025,.025),zz),(b-a-.016,.55,random.uniform(.375,.39)),random.choice(stone),.018);ob.rotation_euler[1]=random.uniform(-.008,.008)
  x+=width
 for side in [-1,1]:
  yy=-6.3-(row%2)*.45
  while yy<9:
   width=random.uniform(.65,1.12)
   ob=cube('Staggered side limestone',(side*6,yy+width/2,zz),(.55,width-.018,random.uniform(.375,.39)),random.choice(stone),.018);ob.rotation_euler[0]=random.uniform(-.008,.008);yy+=width
# Deeper nested Gothic mouldings.
for cx in [-2.2,.1]:
 for expand,depth,radius in [(.10,8.48,.055),(.21,8.55,.065),(.32,8.64,.07)]:
  w=.92+expand;spring=5.8;top=7.5+expand
  pts=[(cx-w,depth,1),(cx-w,depth,spring)]
  for k in range(25):
   t=k/24;pts.append((cx-w*(1-t)**2,depth,spring+(top-spring)*(2*t-t*t)))
  for k in range(25):
   t=k/24;pts.append((cx+w*t*t,depth,top-(top-spring)*t*t))
  pts.append((cx+w,depth,1));line('Nested Gothic stone moulding',pts,radius,stone[4])
# Chimney breast dressed in actual masonry instead of a plain monolith.
for row in range(16):
 z=3.5+row*.355
 for j in range(5):
  yy=1.15+j*.88+(row%2)*.12
  cube('Chimney breast limestone',(5.32,yy,z),(.36,.86,.338),random.choice(stone),.025)
for z in [3.0,3.17,3.36]:cube('Layered carved mantel',(4.99,3.3,z),(1.5,4.65,.13),wood,.035)
for y in [1.25,5.35]:
 for z in [.35,.8,1.25,1.7,2.15,2.6]:cube('Carved fireplace jamb blocks',(5.13,y,z),(1.1,.48,.43),random.choice(stone),.035)
# Nearby pointed recess gives the rear wall additional architectural depth.
pts=[(3,8.42,.2),(3,8.42,3.5)]
for k in range(33):
 t=k/32;pts.append((3+1.4*t,8.42,3.5+1.3*math.sin(math.pi*t)))
pts.append((4.4,8.42,.2));line('Shadowed arch at rear right',pts,.16,stone[3])
cube('Recessed dark oak door',(3.7,8.59,1.75),(1.15,.1,3.4),wood,.02)
for z in [.7,1.8,2.9]:cube('Door iron strap',(3.7,8.51,z),(1.1,.045,.065),iron,.01)
# Move the complete foreground table ensemble toward the camera.
for ob in list(bpy.data.objects):
 if any(ob.name.startswith(p) for p in ['Tabletop','Table leg','Stacked leather','Rustic bread','Pewter cup','Torus']):ob.location.y-=1.35
 if ob.name.startswith(('Wax candle','Wax puddle','Candle flame','Candle glow')) and ob.location.z<1.7 and ob.location.x<2:ob.location.y-=1.35
# Continuous draped blanket, with waves and a hanging edge instead of a rigid slab.
verts=[];faces=[];nx=36;ny=48
for j in range(ny):
 y=-3.95+2.75*j/(ny-1)
 for i in range(nx):
  t=i/(nx-1);x=-4.25+2.0*t
  z=.91+.055*math.sin(t*23+j*.38)+.025*math.sin(j*.9)
  if t<.15:z+=.5*(1-t/.15)
  if t>.8:z-=.65*((t-.8)/.2)**.65
  verts.append((x,y,z))
for j in range(ny-1):
 for i in range(nx-1):
  a=j*nx+i;faces.append((a,a+1,a+nx+1,a+nx))
me=bpy.data.meshes.new('Woven blanket drape');me.from_pydata(verts,[],faces);me.materials.append(cloth);ob=bpy.data.objects.new('Blanket over foreground sofa',me);bpy.context.collection.objects.link(ob)
for p in me.polygons:p.use_smooth=True
ob.modifiers.new('Blanket thickness','SOLIDIFY').thickness=.012
# Thin curved flame tongues replace the conspicuous glowing ellipsoids.
firemat=bpy.data.materials.new('Layered fire tongues');firemat.use_nodes=True;n=firemat.node_tree.nodes;l=firemat.node_tree.links;n.clear()
out=n.new('ShaderNodeOutputMaterial');mix=n.new('ShaderNodeMixShader');tr=n.new('ShaderNodeBsdfTransparent');em=n.new('ShaderNodeEmission');em.inputs['Color'].default_value=(1,.22,.008,1);em.inputs['Strength'].default_value=3
coord=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(coord.outputs['Generated'],sep.inputs[0]);ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.1;ramp.color_ramp.elements[0].color=(.9,.9,.9,1);ramp.color_ramp.elements[1].position=1;ramp.color_ramp.elements[1].color=(0,0,0,1);l.new(sep.outputs['Z'],ramp.inputs[0]);l.new(ramp.outputs[0],mix.inputs[0]);l.new(tr.outputs[0],mix.inputs[1]);l.new(em.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0])
for i in range(32):
 x=random.uniform(4.72,5.3);y=random.uniform(2.25,4.45);h=random.uniform(.3,1.0);w=random.uniform(.035,.12);phase=random.random()*6.28;verts=[];faces=[]
 for j in range(13):
  t=j/12;xx=x+math.sin(t*7+phase)*.1*t;yy=y+math.sin(t*5+phase)*.12*t;ww=w*(1-t)**.65
  verts.extend([(xx,yy-ww,.48+t*h),(xx,yy+ww,.48+t*h)])
 for j in range(12):faces.append((j*2,j*2+1,j*2+3,j*2+2))
 me=bpy.data.meshes.new('Curved flame ribbon');me.from_pydata(verts,[],faces);me.materials.append(firemat);ob=bpy.data.objects.new('Hearth flame tongue',me);bpy.context.collection.objects.link(ob)
# Fireplace grate.
for yy in [2.1,2.5,2.9,3.3,3.7,4.1,4.5]:rod('Fire iron grate',(4.55,yy,.25),(4.55,yy,.68),.018,iron)
rod('Fire grate top rail',(4.55,2.05,.65),(4.55,4.55,.65),.025,iron)
# More believable foliage: fine branches carrying small individual leaf surfaces.
rod('Interior tree trunk',(1.5,7.8,.1),(1.5,7.8,4),.065,wood)
verts=[];faces=[]
for j in range(65):
 a=random.random()*math.tau;r=random.uniform(.3,1);z=random.uniform(3.1,4.45);end=Vector((1.5+r*math.cos(a),7.8+r*math.sin(a),z));rod('Interior fine branch',(1.5,7.8,z-.6),end,.009,wood)
 for k in range(14):
  p=end+Vector((random.uniform(-.22,.22),random.uniform(-.22,.22),random.uniform(-.18,.18)));a=random.random()*math.tau;u=Vector((math.cos(a),math.sin(a),random.uniform(-.4,.4)))*.09;v=Vector((-math.sin(a),math.cos(a),.2))*.035;n0=len(verts);verts.extend([p-u,p+v,p+u,p-v]);faces.append(tuple(range(n0,n0+4)))
me=bpy.data.meshes.new('Individual leaves');me.from_pydata(verts,[],faces);me.materials.append(leaf);ob=bpy.data.objects.new('Interior tree individual leaves',me);bpy.context.collection.objects.link(ob)
# Better readability outside without the former bands of visible area lights.
for ob in bpy.data.objects:
 if ob.name.startswith('Window blue fill'):ob.data.energy=220
# Longer focal length, lower target: foreground objects gain importance.
cam.location=(-1.5,-5.6,1.8);cam.rotation_euler=(Vector((.45,5.7,2.8))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=24
s.cycles.samples=192;s.cycles.sample_clamp_indirect=2;s.cycles.max_bounces=8;s.render.resolution_percentage=100
print('PROGRESS: refinement complete; saving and starting 1280x720 Cycles render at 192 samples',flush=True)
