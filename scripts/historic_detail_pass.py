"""Historic interior study; executed in realism_rebuild.py's scene context.

Observed references and artistic departures are recorded in docs/historic-study.md.
CC0 scans supply materials/props; bespoke joinery fills the missing settle asset.
"""
print('HISTORIC PASS: masonry, window depth, soot and seating', flush=True)

def box(name, pos, size, mat, bevel=.008):
    x,y,z=[v/2 for v in size]
    vv=[(-x,-y,-z),(x,-y,-z),(x,y,-z),(-x,y,-z),(-x,-y,z),(x,-y,z),(x,y,z),(-x,y,z)]
    ff=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
    me=bpy.data.meshes.new(name);me.from_pydata(vv,[],ff);me.materials.append(mat)
    uv=me.uv_layers.new()
    for poly in me.polygons:
        normal=poly.normal;axis=max(range(3),key=lambda i:abs(normal[i]));axes=[i for i in range(3) if i!=axis]
        for li in poly.loop_indices:
            co=me.vertices[me.loops[li].vertex_index].co
            uv.data[li].uv=(co[axes[0]],co[axes[1]])
    ob=bpy.data.objects.new('Historic '+name,me);bpy.context.collection.objects.link(ob);ob.location=pos
    if bevel:
        b=ob.modifiers.new('Worn arris','BEVEL');b.width=bevel;b.segments=3
        ob.modifiers.new('Face normals','WEIGHTED_NORMAL')
    return ob

def roughmat(name,color,scale=7,depth=.002):
    m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=.88;p.inputs['Specular IOR Level'].default_value=.2
    tc=n.new('ShaderNodeTexCoord');no=n.new('ShaderNodeTexNoise');no.inputs['Scale'].default_value=scale;l.new(tc.outputs['Object'],no.inputs[0])
    bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.32;bump.inputs['Distance'].default_value=depth;l.new(no.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
    ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(*(v*.68 for v in color),1);ramp.color_ramp.elements[1].color=(*(v*1.12 for v in color),1);l.new(no.outputs['Fac'],ramp.inputs[0]);l.new(ramp.outputs[0],p.inputs['Base Color'])
    return m

# Broken coursing and soft lime joints, rather than overscaled regular blocks.
wall=pbr('old_stone_wall_02','Historic lime-pointed masonry',2.7)
lower=pbr('rustic_stone_wall_02','Historic rubble masonry',2.5)
for ob in bpy.data.objects:
    if ob.name.startswith(('Scan stone side wall','Scan stone back wall','Scan wall infill','Scan chimney face','Arch spandrel masonry')):
        ob.data.materials.clear();ob.data.materials.append(wall)
        if ob.name.startswith('Arch spandrel'):
            uv=ob.data.uv_layers.new()
            for lp in ob.data.loops:
                co=ob.data.vertices[lp.vertex_index].co;uv.data[lp.index].uv=(co.x,co.z)
        else:
            sub=ob.modifiers.new('Subtle masonry relief grid','SUBSURF');sub.subdivision_type='SIMPLE';sub.levels=4;sub.render_levels=4
            tx=bpy.data.textures.new('Stone surface relief '+ob.name,type='CLOUDS');tx.noise_scale=.18
            disp=ob.modifiers.new('Small surface relief','DISPLACE');disp.texture=tx;disp.strength=.018;disp.texture_coords='GLOBAL'
    if ob.name.startswith('Scan stone side wall'):
        ob.data.materials[0]=lower

limestones=[roughmat('Historic dressed limestone '+str(i),(.28+i*.009,.26+i*.008,.213+i*.007),30,.003) for i in range(5)]
remove(['Carved lancet surround','Nested Gothic stone moulding','Deep window sill'])
for cx in [-2.2,.1]:
    for side in [-1,1]:
        for i in range(12):
            z0=1+i*.4
            box('jointed window jamb',(cx+side*1.045,8.53,z0+.195),(.25,.66,.386),random.choice(limestones),.009)
        # Individual voussoirs: rectangular cross section, deep returns, visible joints.
        def arc(t):return Vector((cx+side*.92*(1-t)**2,5.8+1.7*(2*t-t*t)))
        for k in range(9):
            t0=(k+.018)/9;t1=(k+.982)/9
            a0=arc(t0);a1=arc(t1);tangent=(a1-a0).normalized();normal=Vector((side*abs(tangent.y),abs(tangent.x)))
            points=[a0,a1,a1+normal*.25,a0+normal*.25]
            vv=[(p.x,y,p.y) for y in [8.2,8.86] for p in points]
            ff=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
            me=bpy.data.meshes.new('Jointed arch block');me.from_pydata(vv,[],ff);me.materials.append(random.choice(limestones));ob=bpy.data.objects.new('Historic arch voussoir',me);bpy.context.collection.objects.link(ob)
            b=ob.modifiers.new('Soft chipped edge','BEVEL');b.width=.009;b.segments=2;ob.modifiers.new('Face normals','WEIGHTED_NORMAL')
    box('broad weathered window sill',(cx,8.47,1.005),(2.4,.93,.18),limestones[2],.018)
    box('sill lower course',(cx,8.59,.86),(2.23,.65,.13),limestones[0],.008)

# Sconces now actually project from a wall mounting plate.
iron=bpy.data.materials['Blackened iron']
for ob in list(bpy.data.objects):
    if ob.name.startswith('Wall sconce bracket'):
        side=1 if ob.location.x>0 else -1;y=ob.location.y
        box('sconce wall plate',(side*5.965,y,2.99),(.05,.16,.36),iron,.015)
        box('sconce projecting arm',(side*5.79,y,2.99),(.34,.055,.045),iron,.008)
        bpy.data.objects.remove(ob,do_unlink=True)
    elif ob.name.startswith(('Detailed beeswax','Dark bent wick','Small volumetric candle','Tiny blue candle','Blackened candle saucer','Wax puddle','Candle glow','Sconce warm pool')) and abs(abs(ob.location.x)-5.4)<.3:
        ob.location.x=(1 if ob.location.x>0 else -1)*5.64

# The deep back and returns are masonry with soot; avoid the clean orange box.
remove(['Fireplace soot recess','Blackened skillet','Iron hearth hook','Wrought iron pot crane'])
soot=roughmat('Historic soot and firebrick',(.031,.023,.018),16,.006)
brickmats=[roughmat('Historic fired brick '+str(i),(.044+i*.007,.029+i*.004,.02+i*.003),24,.004) for i in range(4)]
box('sooted fireback',(5.71,3.3,1.64),(.16,3.84,2.8),soot,0)
for iz in range(14):
    for iy in range(11):
        yy=1.48+iy*.34+(iz%2)*.17
        if yy<5.19:box('fireback brick',(5.607,yy,.32+iz*.19),(.055,.326,.179),random.choice(brickmats),.005)
for yy in [1.49,5.11]:box('blackened hearth return',(5.13,yy,1.64),(1.05,.12,2.75),soot,.008)
box('sloping chimney throat',(5.22,3.3,2.86),(1.02,3.66,.28),soot,.008).rotation_euler.y=-.24
ash=roughmat('Historic hearth ash',(.07,.061,.051),35,.004)
box('ash bed',(4.98,3.3,.255),(1.12,2.9,.075),ash,.018)
# Bring the actual flame into a darker fuel bed. The source remains licensed footage.
for ob in bpy.data.objects:
    if ob.name.startswith(('Carved fireplace jamb blocks','Fireplace carved jamb')):
        ob.data.materials.clear();ob.data.materials.append(limestones[1])
    if ob.name.startswith(('Layered carved mantel','Oak mantel')):
        ob.data.materials.clear();ob.data.materials.append(pbr('wood_table_worn','Historic mantle worn oak '+ob.name,1.1))
fire.data.energy=380;fire.data.color=(1,.51,.23);fire.data.shadow_soft_size=.58
# For the locked camera, retain the filmed fire's actual fuel and dim flame body.
# A hard chroma/luminance cut was deleting orange wisps. Start with the RGB
# frame and use a gentler linear-light key plus feathered edges and retained fuel.
fm=bpy.data.materials['Licensed filmed fire'];fn=fm.node_tree.nodes;fl=fm.node_tree.links
ft=next(n for n in fn if n.type=='TEX_IMAGE');ft.image=bpy.data.images.load(str(a/'fire_rgb_frame.png'),check_existing=True)
mix=next(n for n in fn if n.type=='MIX_SHADER');coords=fn.new('ShaderNodeTexCoord');separate=fn.new('ShaderNodeSeparateXYZ');fl.new(coords.outputs['UV'],separate.inputs[0])
fade_outputs=[]
for axis,lo,hi in [('X',.12,.12),('Y',.065,.18)]:
    low=fn.new('ShaderNodeMath');low.operation='DIVIDE';low.inputs[1].default_value=lo;fl.new(separate.outputs[axis],low.inputs[0])
    inv=fn.new('ShaderNodeMath');inv.operation='SUBTRACT';inv.inputs[0].default_value=1;fl.new(separate.outputs[axis],inv.inputs[1])
    high=fn.new('ShaderNodeMath');high.operation='DIVIDE';high.inputs[1].default_value=hi;fl.new(inv.outputs[0],high.inputs[0])
    minimum=fn.new('ShaderNodeMath');minimum.operation='MINIMUM';minimum.use_clamp=True;fl.new(low.outputs[0],minimum.inputs[0]);fl.new(high.outputs[0],minimum.inputs[1]);fade_outputs.append(minimum.outputs[0])
alpha=fn.new('ShaderNodeMath');alpha.operation='MULTIPLY';fl.new(fade_outputs[0],alpha.inputs[0]);fl.new(fade_outputs[1],alpha.inputs[1])
# A gentle linear-light chroma key rejects only the dark red brick background.
# The independent bottom mask retains the actual burning logs in the photograph.
rgb=fn.new('ShaderNodeSeparateColor');fl.new(ft.outputs['Color'],rgb.inputs[0])
red=fn.new('ShaderNodeMath');red.operation='MULTIPLY';red.inputs[1].default_value=.015;fl.new(rgb.outputs['Red'],red.inputs[0])
green=fn.new('ShaderNodeMath');green.operation='SUBTRACT';fl.new(rgb.outputs['Green'],green.inputs[0]);fl.new(red.outputs[0],green.inputs[1])
key=fn.new('ShaderNodeMapRange');key.inputs['From Min'].default_value=.001;key.inputs['From Max'].default_value=.055;fl.new(green.outputs[0],key.inputs[0])
fuel=fn.new('ShaderNodeMapRange');fuel.inputs['From Min'].default_value=.04;fuel.inputs['From Max'].default_value=.24;fuel.inputs['To Min'].default_value=1;fuel.inputs['To Max'].default_value=0;fl.new(separate.outputs['Y'],fuel.inputs[0])
retain=fn.new('ShaderNodeMath');retain.operation='MAXIMUM';fl.new(key.outputs[0],retain.inputs[0]);fl.new(fuel.outputs[0],retain.inputs[1])
matte=fn.new('ShaderNodeMath');matte.operation='MULTIPLY';fl.new(alpha.outputs[0],matte.inputs[0]);fl.new(retain.outputs[0],matte.inputs[1]);fl.new(matte.outputs[0],mix.inputs[0])
em=next(n for n in fn if n.type=='EMISSION');em.inputs['Strength'].default_value=1.3
fl.new(ft.outputs['Color'],em.inputs['Color'])
plate=bpy.data.objects['Real-fire footage in hearth']
for vertex,co in zip(plate.data.vertices,[(5.3,1.58,.24),(5.3,5.02,.24),(5.3,5.02,2.175),(5.3,1.58,2.175)]):vertex.co=co

# A worn leather sofa is closer to the supplied comfort reference than a rigid bench.
# This Victorian asset is an explicit artistic departure from a strict medieval date.
# Keep architectural inspiration and exact furniture dating distinct.
for root in [o for o in bpy.data.objects if o.name.startswith('CC0 ArmChair')]:
    if root.location.y<0:
        descendants=list(root.children_recursive)
        for child in descendants:bpy.data.objects.remove(child,do_unlink=True)
        bpy.data.objects.remove(root,do_unlink=True)
scan('sofa_03',(-2.35,-.9,.07),1.12,math.radians(25))

# Detailed ready-made wooden and woven props.
remove(['CC0 jug_01']) # descendants removed below; avoid floral modern transfer print.
for ob in list(bpy.data.objects):
    if ob.name.startswith('jug_01'):bpy.data.objects.remove(ob,do_unlink=True)
scan('wooden_bowl_01',(.9,-.9,.94),.16,math.radians(15))
scan('wooden_stool_01',(2.65,1.75,.07),.49,math.radians(17))
scan('wicker_basket_01',(3.8,5.8,.07),.48,math.radians(20))

# Controlled bounce lets the grain and cloth read without a flat orange wash.
d=bpy.data.lights.new('Historic reflected hearth bounce','AREA');d.energy=95;d.color=(1,.65,.4);d.shape='DISK';d.size=3.4
ob=bpy.data.objects.new('Historic reflected hearth bounce',d);bpy.context.collection.objects.link(ob);ob.location=(2.8,.1,2.4);ob.rotation_euler=(Vector((-2,-.6,.65))-ob.location).to_track_quat('-Z','Y').to_euler()
s.view_settings.exposure=.65
# Finer, discontinuous rain outside the glass. Rivulets remain on its exterior face.
rain=bpy.data.materials.new('Historic fine backlit rain');rain.use_nodes=True
rn=rain.node_tree.nodes;rl=rain.node_tree.links;rp=rn.get('Principled BSDF');rp.inputs['Base Color'].default_value=(.31,.39,.43,1);rp.inputs['Roughness'].default_value=.12;rp.inputs['Emission Color'].default_value=(.24,.3,.36,1);rp.inputs['Emission Strength'].default_value=.35
vv=[];ff=[]
for cx in [-2.2,.1]:
    for i in range(220):
        x=cx+random.uniform(-.91,.91);z=random.uniform(1.1,7.4);y=random.uniform(8.94,10.5)
        if z>5.8 and abs(x-cx)>.92*(1-math.sqrt((z-5.8)/1.7)):continue
        length=random.uniform(.055,.18);width=random.uniform(.0015,.0035);b=len(vv)
        vv.extend([(x-width,y,z),(x+width,y,z),(x-.025+width,y,z-length),(x-.025-width,y,z-length)]);ff.append((b,b+1,b+2,b+3))
me=bpy.data.meshes.new('Fine rain streaks outside');me.from_pydata(vv,[],ff);me.materials.append(rain);ob=bpy.data.objects.new('Historic layered exterior rain',me);bpy.context.collection.objects.link(ob)
print('HISTORIC PASS COMPLETE',flush=True)
