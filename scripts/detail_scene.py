"""Third pass: aged surfaces, soft furnishings, room dressing and storm visibility."""
print('PROGRESS: surface and dressing pass started',flush=True)
# World-space stone grain avoids repeating the same noise on every block.
for m in stone:
 nodes=m.node_tree.nodes;links=m.node_tree.links;geo=nodes.new('ShaderNodeNewGeometry')
 for n in list(nodes):
  if n.bl_idname=='ShaderNodeTexNoise':
   links.new(geo.outputs['Position'],n.inputs['Vector']);n.inputs['Scale'].default_value=11;n.inputs['Roughness'].default_value=.78
  if n.bl_idname=='ShaderNodeBump':n.inputs['Distance'].default_value=.033;n.inputs['Strength'].default_value=.5
 # Fine grain layered over broader weathering.
 fine=nodes.new('ShaderNodeTexNoise');fine.inputs['Scale'].default_value=135;fine.inputs['Detail'].default_value=2;links.new(geo.outputs['Position'],fine.inputs['Vector'])
 bump=nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.22;bump.inputs['Distance'].default_value=.006;links.new(fine.outputs['Fac'],bump.inputs['Height'])
 p=nodes.get('Principled BSDF')
 for n in list(nodes):
  if n.bl_idname=='ShaderNodeBump' and n!=bump:links.new(n.outputs[0],bump.inputs['Normal'])
 links.new(bump.outputs[0],p.inputs['Normal'])
# Small deviations break up mechanically exact edges without changing room scale.
for ob in bpy.data.objects:
 if ob.type=='MESH' and ob.name.startswith(('Staggered','Chimney breast','Carved fireplace jamb','Uneven flagstone')):
  for v in ob.data.vertices:
   v.co.x+=random.uniform(-.014,.014);v.co.y+=random.uniform(-.011,.011);v.co.z+=random.uniform(-.009,.009)
  ob.rotation_euler.z+=random.uniform(-.006,.006)
# Replace block-shaped upholstery with continuous soft, creased surfaces.
def signpow(x,p):return math.copysign(abs(x)**p,x)
for old in list(bpy.data.objects):
 if not old.name.startswith(('Soft seat cushion','Slumped back pillow','Rolled leather arm')):continue
 dims=old.dimensions.copy();loc=old.location.copy();rot=old.rotation_euler.copy();name=old.name;verts=[];faces=[];nu=64;nv=32
 for j in range(nv+1):
  t=-math.pi/2+math.pi*j/nv
  for i in range(nu):
   a=math.tau*i/nu
   xx=signpow(math.cos(t),.35)*signpow(math.cos(a),.36)
   yy=signpow(math.cos(t),.35)*signpow(math.sin(a),.36)
   zz=signpow(math.sin(t),.38)
   wrinkle=.014*math.sin(a*23+t*7)*(abs(math.sin(t))**3)
   verts.append((xx*dims.x/2,yy*dims.y/2,zz*dims.z/2+wrinkle))
 for j in range(nv):
  for i in range(nu):faces.append((j*nu+i,j*nu+(i+1)%nu,(j+1)*nu+(i+1)%nu,(j+1)*nu+i))
 me=bpy.data.meshes.new(name+' sculpt');me.from_pydata(verts,[],faces);me.materials.append(leather);ob=bpy.data.objects.new(name+' soft sculpt',me);bpy.context.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=rot
 for f in me.polygons:f.use_smooth=True
 bpy.data.objects.remove(old,do_unlink=True)
# Rug woven pattern: muted, worn ornamental bands rather than a uniform rectangle.
n=rug.node_tree.nodes;l=rug.node_tree.links;tex=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(tex.outputs['Generated'],sep.inputs[0]);wave=n.new('ShaderNodeTexWave');wave.wave_type='RINGS';wave.rings_direction='SPHERICAL';wave.inputs['Scale'].default_value=12;wave.inputs['Distortion'].default_value=4;l.new(tex.outputs['Generated'],wave.inputs['Vector']);ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.055,.023,.015,1);ramp.color_ramp.elements[1].color=(.16,.071,.037,1);l.new(wave.outputs['Color'],ramp.inputs[0]);l.new(ramp.outputs[0],n.get('Principled BSDF').inputs['Base Color'])
# Deep overhead timbers and stone ribs.
for yy in [-1.5,3.0,7.4]:
 cube('Massive overhead oak beam',(0,yy,8.65),(12,.3,.4),wood,.04)
for xx in [-4,-2,0,2,4]:cube('Ceiling timber', (xx,1.5,8.8),(.18,15.5,.24),wood,.025)
# Table food and tableware, keeping candles as existing practicals.
pottery=material('Unglazed brown stoneware',(.16,.085,.045),.72,noise=45)
linen=material('Aged flax linen',(.28,.23,.16),.9,noise=170)
page=material('Old parchment',(.40,.30,.16),.85,noise=60)
# Lathed open vessels have a visible rim and interior instead of capped cylinders.
def vessel(name,loc,profile,mat):
 verts=[];faces=[];segments=40
 for r,z in profile:
  for j in range(segments):verts.append((r*math.cos(j*math.tau/segments),r*math.sin(j*math.tau/segments),z))
 for i in range(len(profile)-1):
  for j in range(segments):a=i*segments+j;b=i*segments+(j+1)%segments;faces.append((a,b,b+segments,a+segments))
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.materials.append(mat);ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);ob.location=loc
 for p in me.polygons:p.use_smooth=True
 return ob
for x,y in [(.15,-2.4),(.85,-1.8),(.15,-1.55)]:
 vessel('Hand thrown plate',(x,y,.92),[(0,0),(.12,0),(.21,.025),(.22,.04),(.2,.05),(.12,.025),(0,.025)],pottery)
 vessel('Stoneware drinking cup',(x+.15,y+.32,.92),[(0,0),(.06,0),(.075,.15),(.066,.16),(.05,.035),(0,.035)],pottery)
vessel('Earthenware jug',(.9,-.9,.92),[(0,0),(.09,0),(.14,.1),(.14,.22),(.07,.3),(.06,.4),(.045,.4),(.05,.3),(.11,.22),(.11,.1),(.06,.025),(0,.025)],pottery)
line('Jug curved handle',[(1.01,-.9,1.03),(1.13,-.9,1.07),(1.15,-.9,1.22),(1.04,-.9,1.27)],.022,pottery)
# Folded parchment and leather covers make the book stack legible.
for i in range(4):cube('Visible book page block',(.35,-1.05,.98+i*.075),(.425,.6,.035),page,.006)
# Linen napkin draped across the near table edge.
verts=[];faces=[];nx=22;ny=30
for j in range(ny):
 for i in range(nx):
  x=.2+i*.026;y=-3.15+j*.025;z=.94+.012*math.sin(i*.7+j*.4)
  if y< -3.28:z-=(-3.28-y)*1.8
  verts.append((x,y,z))
for j in range(ny-1):
 for i in range(nx-1):a=j*nx+i;faces.append((a,a+1,a+nx+1,a+nx))
me=bpy.data.meshes.new('Linen folds');me.from_pydata(verts,[],faces);me.materials.append(linen);ob=bpy.data.objects.new('Linen table napkin',me);bpy.context.collection.objects.link(ob)
for p in me.polygons:p.use_smooth=True
# Wax drips follow candle bodies; uneven heights break the cylinder silhouettes.
for ob in list(bpy.data.objects):
 if ob.name.startswith('Wax candle'):
  cx,cy,cz=ob.location;h=max(v.co.z for v in ob.data.vertices)
  for j in range(3):
   a=random.random()*math.tau;rr=.049;top=cz+h*.8;bot=top-random.uniform(.035,.14)
   line('Hardened wax drip',[(cx+rr*math.cos(a),cy+rr*math.sin(a),top),(cx+rr*math.cos(a),cy+rr*math.sin(a),bot)],.009,wax)
print('PROGRESS: aged materials, upholstery, tableware and candle wax complete',flush=True)
# Rain glass: mostly clear transmission, restrained blue-grey reflection, thin rivulet bump.
n=glass.node_tree.nodes;l=glass.node_tree.links;n.clear();out=n.new('ShaderNodeOutputMaterial');mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=.14;tr=n.new('ShaderNodeBsdfTransparent');tr.inputs['Color'].default_value=(.77,.85,.91,1);pr=n.new('ShaderNodeBsdfPrincipled');pr.inputs['Base Color'].default_value=(.2,.29,.34,1);pr.inputs['Roughness'].default_value=.14;pr.inputs['Metallic'].default_value=.45
coord=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(15,15,.6);l.new(coord.outputs['Generated'],mapping.inputs[0]);noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=6;noise.inputs['Detail'].default_value=3;l.new(mapping.outputs[0],noise.inputs['Vector']);bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.22;bump.inputs['Distance'].default_value=.008;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],pr.inputs['Normal']);l.new(tr.outputs[0],mix.inputs[1]);l.new(pr.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0])
# A dim, textured storm sky visible only through the window openings.
sky=material('Moonlit storm cloud bank',(.11,.17,.23));n=sky.node_tree.nodes;l=sky.node_tree.links;p=n.get('Principled BSDF');t=n.new('ShaderNodeTexNoise');t.inputs['Scale'].default_value=3;t.inputs['Detail'].default_value=5;r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(.025,.044,.065,1);r.color_ramp.elements[1].color=(.17,.24,.31,1);l.new(t.outputs['Fac'],r.inputs[0]);l.new(r.outputs[0],p.inputs['Emission Color']);p.inputs['Emission Strength'].default_value=.6
cube('Exterior storm sky backdrop',(0,28,8),(45,.1,20),sky)
# Elevate distant terrain/village to place roofs within the seated camera's view.
for ob in bpy.data.objects:
 if ob.name.startswith(('Distant village cottage','Village roof','Village lamplit window')):ob.location.z+=1.4
 if ob.name.startswith('Exterior ground'):
  ob.location.z=1.1;ob.location.y=21;ob.dimensions.y=16
light('Exterior moonlit rain',(0,14,9),(.35,.52,.8),1500,8,'AREA',(0,15,0))
# Gentle hill silhouettes behind the houses.
for x,y,z,sc in [(-7,24,1.2,(8,4,2.2)),(4,25,1.1,(9,4,2.8))]:uv('Distant wooded ridge',(x,y,z),sc,night)
# The village is viewed through refracting rain and leadwork; warm points give scale.
for x,y in [(-2,17),(.3,18),(2.2,19),(-4,19)]:
 light('Village lantern',(x,y,2.25),(1,.42,.12),14,.1)
# Rain geometry now has falling motion over the development timeline.
for ob in bpy.data.objects:
 if ob.name.startswith('Wind slanted rain'):
  origin=ob.location.copy();ob.location=origin;ob.keyframe_insert(data_path='location',frame=1);ob.location=origin+Vector((-1.35,0,-6));ob.keyframe_insert(data_path='location',frame=145)
  for fc in ob.animation_data.action.fcurves:
   for key in fc.keyframe_points:key.interpolation='LINEAR'
   fc.modifiers.new('CYCLES')
# Increase rain density with finer streaks nearer the glass.
for i in range(650):
 x=random.uniform(-3.25,1.15);y=random.uniform(9.2,11);z=random.uniform(1,8)
 ob=rod('Fine rain streak',(x,y,z),(x+.035,y,z-.16),.0017,rain)
# Climbing ivy on shaded stone piers, kept away from the window sightlines.
ivyverts=[];ivyfaces=[]
for xx in [-5.55,2.65]:
 for i in range(12):
  z=.4+i*.58;cx=xx+.12*math.sin(i*.8);line('Climbing ivy stem',[(cx,8.4,z),(cx+.16,8.39,z+.65)],.009,wood)
  for j in range(13):
   p=Vector((cx+random.uniform(-.26,.26),8.32+random.uniform(-.06,.03),z+random.uniform(0,.65)));w=random.uniform(.04,.09);a=len(ivyverts);ivyverts.extend([p+Vector((-w,0,0)),p+Vector((-.3*w,-.02,w)),p+Vector((w,0,0)),p+Vector((0,0,-w))]);ivyfaces.append((a,a+1,a+2,a+3))
me=bpy.data.meshes.new('Ivy leaf mesh');me.from_pydata(ivyverts,[],ivyfaces);me.materials.append(leaf);ob=bpy.data.objects.new('Climbing ivy leaves',me);bpy.context.collection.objects.link(ob)
s.frame_set(36)
# A low-cost diagnostic render precedes the final still of this pass.
s.render.resolution_percentage=int(os.environ.get('LOUNGE_PREVIEW_PERCENT','50'));s.cycles.samples=int(os.environ.get('LOUNGE_SAMPLES','48'))
print('PROGRESS: storm visibility and rain motion configured; launching preview',flush=True)
