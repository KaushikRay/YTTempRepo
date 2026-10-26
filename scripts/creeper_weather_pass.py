"""Reference-led interior creeper and storm visibility, run by realism_rebuild.

No reusable free ivy model could be downloaded from the accessible services.
Branches/curved leaf geometry are authored here; actual CC0 leaf photography
supplies surface detail. Original photos and provenance stay in assets/creeper.
"""
from mathutils import Quaternion
print('CREEPER PASS: attached branching ivy, leaf photography and storm layers',flush=True)
rng=random.Random(729)
plant_collection=bpy.data.collections.new('Interior creeper');s.collection.children.link(plant_collection)
stemmat=roughmat('Creeper corky living stems',(.055,.037,.019),38,.0011)
petiolemat=roughmat('Creeper leaf petioles',(.045,.065,.019),26,.00015)
leafmat=bpy.data.materials.new('Creeper CC0 photographed ivy leaf');leafmat.use_nodes=True
n=leafmat.node_tree.nodes;l=leafmat.node_tree.links;p=n.get('Principled BSDF')
photo=n.new('ShaderNodeTexImage');photo.image=bpy.data.images.load(str(r/'assets/creeper/ivy_leaf_2025.jpg'),check_existing=True)
grade=n.new('ShaderNodeHueSaturation');grade.inputs['Saturation'].default_value=.82;grade.inputs['Value'].default_value=.7;l.new(photo.outputs['Color'],grade.inputs['Color'])
objinfo=n.new('ShaderNodeObjectInfo');variation=n.new('ShaderNodeMapRange');variation.inputs['To Min'].default_value=.72;variation.inputs['To Max'].default_value=1.12;l.new(objinfo.outputs['Random'],variation.inputs[0])
multiply=n.new('ShaderNodeMixRGB');multiply.blend_type='MULTIPLY';multiply.inputs[0].default_value=1;l.new(grade.outputs[0],multiply.inputs[1]);l.new(variation.outputs[0],multiply.inputs[2])
green=n.new('ShaderNodeMixRGB');green.blend_type='MULTIPLY';green.inputs[0].default_value=1;green.inputs[2].default_value=(.52,.82,.36,1);l.new(multiply.outputs[0],green.inputs[1]);l.new(green.outputs[0],p.inputs['Base Color'])
p.inputs['Roughness'].default_value=.34;p.inputs['Specular IOR Level'].default_value=.3;p.inputs['Coat Weight'].default_value=.11;p.inputs['Coat Roughness'].default_value=.26;p.inputs['Subsurface Weight'].default_value=.055;p.inputs['Subsurface Scale'].default_value=.001
bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.18;bump.inputs['Distance'].default_value=.00025;l.new(photo.outputs['Color'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
trans=n.new('ShaderNodeBsdfTranslucent');l.new(green.outputs[0],trans.inputs['Color']);mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=.12;l.new(p.outputs[0],mix.inputs[1]);l.new(trans.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],n.get('Material Output').inputs['Surface'])

# A lobed, cupped leaf with 4 radial rings. The photograph is UV sampled from
# within its large central leaf; no background card or flat foliage cloud.
outline=[(0,-.30),(-.25,-.47),(-.55,-.38),(-.49,-.04),(-.78,.13),(-.43,.42),(-.23,.32),(0,1),(.23,.32),(.43,.42),(.78,.13),(.49,-.04),(.55,-.38),(.25,-.47)]
# Round the broad lobe edges; the coarse control polygon read as cut paper.
control=[Vector(v) for v in outline];outline=[]
for k,point in enumerate(control):
    previous=control[(k-1)%len(control)];following=control[(k+1)%len(control)]
    start=previous*.25+point*.75;end=point*.75+following*.25
    for j in range(5):
        t=j/5;q=start*(1-t)**2+point*2*t*(1-t)+end*t*t;outline.append(tuple(q))
leaf_meshes=[]
for variant in range(5):
    verts=[(0,0,.045)];uvs=[(.465,.64)];faces=[]
    for ring in range(1,5):
        t=ring/4
        for k,(x,y) in enumerate(outline):
            xx=x*t*(1+.035*math.sin(k*3+variant));yy=y*t
            zz=.065*(1-t*t)+.12*t*t*math.sin(k*.8+variant)+.022*xx*xx
            verts.append((xx,yy,zz));uvs.append((.465+xx*.225,.64+yy*.285))
    count=len(outline)
    for k in range(count):faces.append((0,1+k,1+(k+1)%count))
    for ring in range(3):
        for k in range(count):
            a0=1+ring*count+k;a1=1+ring*count+(k+1)%count;faces.append((a0,a1,a1+count,a0+count))
    me=bpy.data.meshes.new('Creeper curved lobed leaf '+str(variant));me.from_pydata(verts,[],faces);me.materials.append(leafmat);uv=me.uv_layers.new()
    for lp in me.loops:uv.data[lp.index].uv=uvs[lp.vertex_index]
    for poly in me.polygons:poly.use_smooth=True
    leaf_meshes.append(me)

def tube(name,points,radius,mat):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=2;cu.bevel_depth=radius;cu.bevel_resolution=2
    sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
    for i,(pt,co) in enumerate(zip(sp.points,points)):
        pt.co=(*co,1);pt.radius=max(.12,(1-i/max(1,len(points)-1))**.65)
    cu.materials.append(mat);ob=bpy.data.objects.new('Creeper '+name,cu);plant_collection.objects.link(ob);return ob

leaf_count=0
def grow(label,origin,height,project,normal,tangent,branches):
    global leaf_count
    def axis(t):return origin+.18*math.sin(t*5.3)+.045*math.sin(t*19)
    main=[project(axis(i/75),.08+height*i/75,.022) for i in range(76)]
    tube(label+' woody rooted leader',main,.012,stemmat)
    for k in range(branches):
        base_t=.08+.87*k/branches;z0=.08+height*base_t;u0=axis(base_t);side=-1 if k%2 else 1
        run=rng.uniform(.28,.92)*(.48 if label=='hearth outer cheek' else 1.4);rise=rng.uniform(.3,1.05);phase=rng.random()*6.28
        def sprig(t):return u0+side*run*t+.05*math.sin(t*6+phase)*t,z0+rise*t-.19*t*t
        coords=[project(*sprig(i/22),.025+.025*math.sin(i/22*math.pi)) for i in range(23)]
        tube(label+' tapering branch',coords,.0037,stemmat)
        for j in range(rng.randint(11,17)):
            t=.07+j*.058
            if t>.98:continue
            u,z=sprig(t);sign=1 if j%2 else -1
            leaf_u=u+sign*rng.uniform(.045,.095);leaf_z=z+rng.uniform(-.055,.045)
            attach=project(u,z,.03);centre=project(leaf_u,leaf_z,.075+rng.uniform(0,.035))
            tube(label+' petiole',[attach,(attach+centre)/2+normal*.015,centre],.0013,petiolemat)
            ob=bpy.data.objects.new('Creeper '+label+' leaf',rng.choice(leaf_meshes));plant_collection.objects.link(ob);ob.location=centre
            # Leaf local Y extends toward its tip, local Z faces into the room.
            angle=rng.uniform(-.95,.95)+sign*.45
            rot=normal.to_track_quat('Z','Y')@Quaternion(Vector((0,0,1)),angle)@Quaternion(Vector((1,0,0)),rng.uniform(-.5,.5))
            ob.rotation_mode='QUATERNION';ob.rotation_quaternion=rot
            size=rng.uniform(.08,.145)*(1-.22*t);ob.scale=(size*rng.uniform(.85,1.12),size,size)
            leaf_count+=1

def left_surface(u,z,offset):
    pier=max(math.exp(-((u-p)/.36)**8) for p in [-3,1,5,8.5])
    return Vector((-5.96+.62*pier+offset,u,z))
grow('left foreground pier',1.05,6.0,left_surface,Vector((1,0,0)),Vector((0,1,0)),38)
grow('left rear pier',5.05,6.5,left_surface,Vector((1,0,0)),Vector((0,1,0)),27)
grow('window side',1.82,5.35,lambda u,z,o:Vector((max(1.25,u),8.90-o,z)),Vector((0,-1,0)),Vector((1,0,0)),29)
# Outer cheek only, kept away from the hot firebox and open flames.
def hearth_surface(u,z,offset):
    if z<2.8:x=4.535
    elif z<2.98:x=4.535-(z-2.8)/.18*.38
    elif z<3.5:x=4.155
    elif z<3.67:x=4.155+(z-3.5)/.17*.92
    else:x=5.075
    return Vector((x-offset,min(1.42,max(1.09,u)),z))
grow('hearth outer cheek',1.25,5.65,hearth_surface,Vector((-1,0,0)),Vector((0,1,0)),18)

# Storm at the glass: a continuous population of fine streaks at several depths,
# with tapering transparent edges, not sparse bright rods or an opaque sheet.
remove(['Historic layered exterior rain'])
rainmat=bpy.data.materials.new('Storm fine tapered rain');rainmat.use_nodes=True;n=rainmat.node_tree.nodes;l=rainmat.node_tree.links;n.clear()
out=n.new('ShaderNodeOutputMaterial');tr=n.new('ShaderNodeBsdfTransparent');em=n.new('ShaderNodeEmission');em.inputs['Color'].default_value=(.37,.46,.51,1);em.inputs['Strength'].default_value=.8
uv=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(uv.outputs['UV'],sep.inputs[0]);shape=n.new('ShaderNodeMath');shape.operation='MULTIPLY';shape.inputs[1].default_value=math.pi;l.new(sep.outputs['Y'],shape.inputs[0]);wave=n.new('ShaderNodeMath');wave.operation='SINE';l.new(shape.outputs[0],wave.inputs[0]);strength=n.new('ShaderNodeMath');strength.operation='MULTIPLY';strength.inputs[1].default_value=.42;l.new(wave.outputs[0],strength.inputs[0]);mix=n.new('ShaderNodeMixShader');l.new(strength.outputs[0],mix.inputs[0]);l.new(tr.outputs[0],mix.inputs[1]);l.new(em.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0])
verts=[];faces=[];uvs=[]
for cx in [-2.2,.1]:
    for i in range(1850):
        x=cx+rng.uniform(-.91,.91);z=rng.uniform(1.12,7.45)
        if z>5.8 and abs(x-cx)>.92*(1-math.sqrt((z-5.8)/1.7)):continue
        y=rng.uniform(8.73,11.5);length=rng.uniform(.055,.28);w=rng.uniform(.0015,.0038);slant=length*.14;b=len(verts)
        verts.extend([(x-w,y,z),(x+w,y,z),(x-slant+w*.45,y,z-length),(x-slant-w*.45,y,z-length)]);faces.append((b,b+1,b+2,b+3));uvs.extend([(0,0),(1,0),(1,1),(0,1)])
me=bpy.data.meshes.new('Storm rain at layered depths');me.from_pydata(verts,[],faces);me.materials.append(rainmat);layer=me.uv_layers.new()
for lp in me.loops:layer.data[lp.index].uv=uvs[lp.vertex_index]
ob=bpy.data.objects.new('Storm layered tapered rain',me);bpy.context.collection.objects.link(ob)

# Distort the landscape through water instead of reading a clean flat pane.
glass=bpy.data.materials['Cold rain-streaked glass'];n=glass.node_tree.nodes;l=glass.node_tree.links
watercoord=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(3.5,2,.22);l.new(watercoord.outputs['Object'],mapping.inputs[0])
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=22;noise.inputs['Detail'].default_value=3;l.new(mapping.outputs[0],noise.inputs[0]);bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.3;bump.inputs['Distance'].default_value=.018;l.new(noise.outputs['Fac'],bump.inputs['Height'])
for p in n:
    if p.type in ['BSDF_PRINCIPLED','BSDF_GLASS']:
        l.new(bump.outputs[0],p.inputs['Normal'])
        if p.type=='BSDF_PRINCIPLED':p.inputs['Roughness'].default_value=.12
# Separate cold air depth behind the near rain, leaving the room volume clear.
fog=bpy.data.materials.new('Storm exterior mist');fog.use_nodes=True;n=fog.node_tree.nodes;l=fog.node_tree.links;n.clear();out=n.new('ShaderNodeOutputMaterial');vol=n.new('ShaderNodeVolumePrincipled');vol.inputs['Density'].default_value=.032;vol.inputs['Color'].default_value=(.33,.42,.48,1);vol.inputs['Anisotropy'].default_value=.25;l.new(vol.outputs[0],out.inputs['Volume'])
box('exterior mist only',(-1,17,5),(15,13,13),fog,0)
for ob in bpy.data.objects:
    if ob.name.startswith('Window blue fill'):ob.data.energy=175;ob.data.color=(.55,.66,.77)
    if ob.name.startswith('Village lamplit'):ob.scale*=.75
    if ob.name=='Soft cool room bounce':ob.data.energy=38

# Wider patterned rug was reading as square floor tiles. Move it to a quieter
# wool surface and expose the actual stone walkway toward the hearth.
rg=bpy.data.objects.get('Woven seating rug')
if rg:
    for v in rg.data.vertices:v.co.x=-1.5+(v.co.x+1.5)*.83
    m=rg.data.materials[0];p=m.node_tree.nodes.get('Principled BSDF');tint=next((n for n in m.node_tree.nodes if n.type=='MIX_RGB'),None)
    if tint:tint.inputs[2].default_value=(.105,.058,.028,1)
    p.inputs['Roughness'].default_value=.97

summary={'leaf_count':leaf_count,'rooted_ivy_patches':4,'rain_streaks':len(faces),'leaf_source':'assets/creeper/provenance.json','animated':False,'asset_fallback':'Public ivy downloads blocked; authored branching/leaf geometry, CC0 photo surface detail'}
(r/'renders/creeper_build.json').write_text(json.dumps(summary,indent=2))
print('CREEPER PASS COMPLETE '+json.dumps(summary),flush=True)
