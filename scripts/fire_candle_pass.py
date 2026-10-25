"""Replace placeholder flames with baked gas fire and small volumetric candle flames."""
print('PROGRESS: rebuilding candle wax, wicks and volumetric flames',flush=True)
# Capture candle positions before replacing the primitive bodies.
candles=[]
for ob in list(bpy.data.objects):
 if ob.name.startswith('Wax candle'):
  bottom=ob.location.z+min(v.co.z for v in ob.data.vertices);top=ob.location.z+max(v.co.z for v in ob.data.vertices);candles.append((ob.location.x,ob.location.y,bottom,top));bpy.data.objects.remove(ob,do_unlink=True)
remove_prefixes(['Candle flame','Hardened wax drip','Hearth flame tongue'])
p=wax.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.57,.43,.25,1);p.inputs['Roughness'].default_value=.38;p.inputs['Subsurface Weight'].default_value=.13;p.inputs['Subsurface Radius'].default_value=(1,.48,.19);p.inputs['Subsurface Scale'].default_value=.015
wickmat=material('Carbon black candle wick',(.008,.005,.003),.95)
# Emission lives within the flame volume, giving a soft optical edge.
def flame_volume(name,temp,strength):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;n.clear();out=n.new('ShaderNodeOutputMaterial');v=n.new('ShaderNodeVolumePrincipled');v.inputs['Density'].default_value=0;v.inputs['Density Attribute'].default_value='';v.inputs['Blackbody Intensity'].default_value=0;bb=n.new('ShaderNodeBlackbody');bb.inputs['Temperature'].default_value=temp;l.new(bb.outputs[0],v.inputs['Emission Color']);v.inputs['Emission Strength'].default_value=strength;l.new(v.outputs[0],out.inputs['Volume']);return m
candlefire=flame_volume('Candle flame — warm emitting gas',1950,300)
bluefire=flame_volume('Candle flame — blue base',9000,30)
for idx,(x,y,bottom,top) in enumerate(candles):
 r=random.uniform(.032,.046);height=top-bottom;verts=[];faces=[];seg=64
 # Outer wall, uneven rim, molten basin, wick center.
 profiles=[(r*.96,0),(r,.015),(r,height*.5),(r*.98,height-.018),(r*.94,height),(r*.73,height-.008),(r*.5,height-.014),(0,height-.016)]
 for ring,(radius,z) in enumerate(profiles):
  for j in range(seg):
   a=j*math.tau/seg;variation=.0018*math.sin(5*a+idx)+.001*math.sin(11*a)
   zz=z+(variation if ring in [3,4,5] else 0);rr=radius*(1+.018*math.sin(a*7+idx));verts.append((rr*math.cos(a),rr*math.sin(a),zz))
 for k in range(len(profiles)-1):
  for j in range(seg):a=k*seg+j;b=k*seg+(j+1)%seg;faces.append((a,b,b+seg,a+seg))
 faces.append(tuple(range(seg-1,-1,-1)))
 me=bpy.data.meshes.new('Melted candle profile');me.from_pydata(verts,[],faces);me.materials.append(wax);ob=bpy.data.objects.new('Detailed beeswax candle',me);bpy.context.collection.objects.link(ob);ob.location=(x,y,bottom)
 for f in me.polygons:f.use_smooth=True
 rod('Dark bent wick',(x,y,top-.013),(x+.002,y,top+.006),.0014,wickmat)
 # Smooth closed teardrop, 32–43 mm tall, not a glowing 170 mm oval.
 h=random.uniform(.032,.043);verts=[];faces=[];ns=24;nr=16
 for k in range(nr+1):
  t=k/nr;radius=.007*(math.sin(math.pi*t)**.7)*(1-.55*t);cx=.005*t*t
  for j in range(ns):a=j*math.tau/ns;verts.append((cx+radius*math.cos(a),radius*math.sin(a),t*h))
 for k in range(nr):
  for j in range(ns):a=k*ns+j;b=k*ns+(j+1)%ns;faces.append((a,b,b+ns,a+ns))
 me=bpy.data.meshes.new('Candle gas flame envelope');me.from_pydata(verts,[],faces);me.materials.append(candlefire);ob=bpy.data.objects.new('Small volumetric candle flame',me);bpy.context.collection.objects.link(ob);ob.location=(x,y,top+.001)
 uv('Tiny blue candle flame base',(x,y,top+.004),(.0035,.0035,.003),bluefire)
 for frame,angle in [(1,-.06),(25,.08),(49,-.03),(73,.05),(97,-.07),(121,.03),(145,-.06)]:ob.rotation_euler[1]=angle;ob.keyframe_insert(data_path='rotation_euler',frame=frame)
 # Small wax rivulets taper toward the hardened drip.
 for k in range(random.randint(2,4)):
  a=random.random()*math.tau;end=top-random.uniform(.025,min(.13,height*.65));rr=r+.001
  line('Thin hardened wax rivulet',[(x+rr*math.cos(a),y+rr*math.sin(a),top-.005),(x+(rr+.001)*math.cos(a),y+(rr+.001)*math.sin(a),end)],.0025,wax)
 if x<2:
  vessel('Blackened candle saucer',(x,y,bottom-.012),[(0,0),(.055,0),(.074,.009),(.076,.017),(.063,.018),(0,.009)],iron)
for ob in bpy.data.objects:
 if ob.name.startswith('Candle glow'):ob.data.energy=1.1;ob.data.shadow_soft_size=.018
 if ob.name.startswith('Wax puddle'):ob.scale.z=.006;ob.scale.x*=.75;ob.scale.y*=.75
# The available fluid solver fails during initialization; use a true 3D shader
# volume for this iteration. This is procedural fire, not a fluid simulation.
pyro=bpy.data.materials.new('Turbulent three-dimensional fire volume');pyro.use_nodes=True;n=pyro.node_tree.nodes;l=pyro.node_tree.links;n.clear()
out=n.new('ShaderNodeOutputMaterial');v=n.new('ShaderNodeVolumePrincipled');v.inputs['Density Attribute'].default_value='';v.inputs['Blackbody Intensity'].default_value=0
tex=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(2.5,5.5,.65);l.new(tex.outputs['Generated'],mapping.inputs[0])
noise=n.new('ShaderNodeTexNoise');noise.noise_dimensions='4D';noise.inputs['Scale'].default_value=3.6;noise.inputs['Detail'].default_value=4;noise.inputs['Roughness'].default_value=.73;noise.inputs['W'].default_value=1.7;l.new(mapping.outputs[0],noise.inputs['Vector'])
for frame,value in [(1,0),(145,3)]:noise.inputs['W'].default_value=value;noise.inputs['W'].keyframe_insert(data_path='default_value',frame=frame)
ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.27;ramp.color_ramp.elements[1].position=.42
sep=n.new('ShaderNodeSeparateXYZ');l.new(tex.outputs['Generated'],sep.inputs[0]);height=n.new('ShaderNodeMapRange');height.inputs['From Min'].default_value=.15;height.inputs['From Max'].default_value=1;height.inputs['To Min'].default_value=1;height.inputs['To Max'].default_value=0;l.new(sep.outputs['Z'],height.inputs[0])
lift=n.new('ShaderNodeMath');lift.operation='MULTIPLY';lift.inputs[1].default_value=.42;l.new(sep.outputs['Z'],lift.inputs[0]);cut=n.new('ShaderNodeMath');cut.operation='SUBTRACT';l.new(noise.outputs['Fac'],cut.inputs[0]);l.new(lift.outputs[0],cut.inputs[1]);l.new(cut.outputs[0],ramp.inputs[0])
mask=n.new('ShaderNodeMath');mask.operation='MULTIPLY';l.new(ramp.outputs[0],mask.inputs[0]);l.new(height.outputs[0],mask.inputs[1]);strength=n.new('ShaderNodeMath');strength.operation='MULTIPLY';strength.inputs[1].default_value=7;l.new(mask.outputs[0],strength.inputs[0]);# Fade all lateral boundaries so the volume container cannot read as a rectangle.
edge=n.new('ShaderNodeMath');edge.operation='MULTIPLY';edge.inputs[0].default_value=1;edge.inputs[1].default_value=1
for axis in ['X','Y']:
 sub=n.new('ShaderNodeMath');sub.operation='SUBTRACT';sub.inputs[1].default_value=.5;l.new(sep.outputs[axis],sub.inputs[0]);ab=n.new('ShaderNodeMath');ab.operation='ABSOLUTE';l.new(sub.outputs[0],ab.inputs[0]);twice=n.new('ShaderNodeMath');twice.operation='MULTIPLY';twice.inputs[1].default_value=2;l.new(ab.outputs[0],twice.inputs[0]);fade=n.new('ShaderNodeMath');fade.operation='SUBTRACT';fade.inputs[0].default_value=1;l.new(twice.outputs[0],fade.inputs[1]);l.new(fade.outputs[0],edge.inputs[0 if axis=='X' else 1])
final_strength=n.new('ShaderNodeMath');final_strength.operation='MULTIPLY';l.new(strength.outputs[0],final_strength.inputs[0]);l.new(edge.outputs[0],final_strength.inputs[1]);l.new(final_strength.outputs[0],v.inputs['Emission Strength'])
bb=n.new('ShaderNodeBlackbody');temp=n.new('ShaderNodeMapRange');temp.inputs['To Min'].default_value=1400;temp.inputs['To Max'].default_value=2100;l.new(noise.outputs['Fac'],temp.inputs[0]);l.new(temp.outputs[0],bb.inputs[0]);l.new(bb.outputs[0],v.inputs['Emission Color']);v.inputs['Density'].default_value=.001;l.new(v.outputs[0],out.inputs['Volume'])
# Thin asymmetric volumes constrain the silhouette even at low render samples.
# No flat flame surfaces are used.
for link in list(v.inputs['Emission Strength'].links):l.remove(link)
shine=n.new('ShaderNodeMapRange');shine.inputs['To Min'].default_value=1;shine.inputs['To Max'].default_value=3;l.new(noise.outputs['Fac'],shine.inputs[0]);l.new(shine.outputs[0],v.inputs['Emission Strength'])
for i in range(19):
 x=random.uniform(4.86,5.16);y=2.3+i*.105;h=random.uniform(.65,1.15);width=random.uniform(.07,.12);phase=random.uniform(0,math.tau);verts=[];faces=[];ns=24;nr=28
 for k in range(nr+1):
  t=k/nr;radius=width*(math.sin(math.pi*t)**.6)*(1-t)**.8;cx=.09*math.sin(t*6+phase)*t;cy=.1*math.sin(t*4+phase)*t
  for j in range(ns):
   a=j*math.tau/ns;rr=radius*(1+.18*math.sin(3*a+t*13+phase));verts.append((x+cx+rr*math.cos(a),y+cy+rr*math.sin(a),.44+t*h))
 for k in range(nr):
  for j in range(ns):a=k*ns+j;b=k*ns+(j+1)%ns;faces.append((a,b,b+ns,a+ns))
 me=bpy.data.meshes.new('Tapered flame gas shape');me.from_pydata(verts,[],faces);me.materials.append(pyro);ob=bpy.data.objects.new('Procedural hearth gas envelope',me);bpy.context.collection.objects.link(ob)

# Actual charred logs with coarse blackened grain, replacing clean timber.
char=material('Cracked charcoal wood',(.024,.013,.006),.92,noise=18)
for ob in bpy.data.objects:
 if ob.name.startswith('Charred log'):ob.data.materials.clear();ob.data.materials.append(char)
 if ob.name.startswith('Ember'):ob.scale.z*=.4
# Mottled soot above the opening: an irregular stone surface, not flat clean blocks.
for m in stone:
 n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');geo=n.new('ShaderNodeNewGeometry');sep=n.new('ShaderNodeSeparateXYZ');l.new(geo.outputs['Position'],sep.inputs[0])
 # Stones receive broad mineral mottling and fine pits at different frequencies.
 noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=1.7;noise.inputs['Detail'].default_value=5;l.new(geo.outputs['Position'],noise.inputs['Vector']);r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(.18,.17,.15,1);r.color_ramp.elements[1].color=(.55,.52,.45,1);l.new(noise.outputs[0],r.inputs[0]);old=p.inputs['Base Color'].links[0].from_socket;mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.7;l.new(old,mix.inputs[1]);l.new(r.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],p.inputs['Base Color'])
# Tone down precise mortar seams with smaller gaps visually; retain real geometry.
for ob in bpy.data.objects:
 if ob.name.startswith(('Staggered back','Staggered side')):
  ob.scale.z=random.uniform(1.015,1.035)
texture=bpy.data.textures.new('Weathered stone micro relief',type='CLOUDS');texture.noise_scale=.13;texture.noise_depth=2
for ob in bpy.data.objects:
 if ob.name.startswith(('Staggered back','Staggered side','Chimney breast')):
  subdiv=ob.modifiers.new('Stone face tessellation','SUBSURF');subdiv.subdivision_type='SIMPLE';subdiv.levels=1;subdiv.render_levels=1
  displace=ob.modifiers.new('Weathered face relief','DISPLACE');displace.texture=texture;displace.texture_coords='GLOBAL';displace.strength=.018;displace.mid_level=.5
# View the mature fire rather than its ignition frame.
s.frame_set(45);s.cycles.volume_step_rate=.75;s.cycles.transparent_max_bounces=16
s.render.resolution_percentage=int(os.environ.get('LOUNGE_PREVIEW_PERCENT','50'));s.cycles.samples=int(os.environ.get('LOUNGE_SAMPLES','48'))
# Small optical bloom around hot gases; keep the flame core exposed.
s.use_nodes=True;nodes=s.node_tree.nodes;nodes.clear();layers=nodes.new('CompositorNodeRLayers');glare=nodes.new('CompositorNodeGlare');glare.glare_type='FOG_GLOW';glare.quality='HIGH';glare.threshold=2;glare.size=6;glare.mix=-.94;out=nodes.new('CompositorNodeComposite');s.node_tree.links.new(layers.outputs['Image'],glare.inputs[0]);s.node_tree.links.new(glare.outputs[0],out.inputs[0])
print('PROGRESS: volumetric fire and candle replacement complete',flush=True)
