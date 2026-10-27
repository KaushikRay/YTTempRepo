"""Substantial photographic rebuild of materials, construction, ground and weather.

Executed after the initial camera/framing pass, before the Cycles still render.
Original geometry and CC0 scans only. The photographed HDRI supplies illumination.
"""
from mathutils import Matrix
rng=random.Random(84729)
status('realism_materials')

def remove_prefix(prefixes):
    for ob in list(bpy.data.objects):
        if ob.name.startswith(tuple(prefixes)):bpy.data.objects.remove(ob,do_unlink=True)

def aged_material(name,asset,darkness=.72,coat=.1):
    mat=pbr(name,'realism/'+asset,1,darkness,coat);n=mat.node_tree.nodes;l=mat.node_tree.links;p=n.get('Principled BSDF')
    # Avoid a continuous polished clearcoat. Weathering varies in world space.
    geo=n.new('ShaderNodeNewGeometry');mapping=n.new('ShaderNodeVectorMath');mapping.operation='MULTIPLY';mapping.inputs[1].default_value=(2.8,2.8,.18);l.new(geo.outputs['Position'],mapping.inputs[0])
    noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=2.1;noise.inputs['Detail'].default_value=3;l.new(mapping.outputs[0],noise.inputs['Vector'])
    rough=n.new('ShaderNodeMapRange');rough.inputs['To Min'].default_value=.39;rough.inputs['To Max'].default_value=.77;l.new(noise.outputs['Fac'],rough.inputs['Value']);l.new(rough.outputs[0],p.inputs['Roughness'])
    wet=n.new('ShaderNodeMath');wet.operation='MULTIPLY';wet.inputs[1].default_value=coat;l.new(noise.outputs['Fac'],wet.inputs[0]);l.new(wet.outputs[0],p.inputs['Coat Weight']);p.inputs['Coat Roughness'].default_value=.14
    source=p.inputs['Base Color'].links[0].from_socket;obj=n.new('ShaderNodeObjectInfo');variation=n.new('ShaderNodeMapRange');variation.inputs['To Min'].default_value=.68;variation.inputs['To Max'].default_value=1.05;l.new(obj.outputs['Random'],variation.inputs[0])
    mul=n.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;l.new(source,mul.inputs[1]);l.new(variation.outputs[0],mul.inputs[2]);l.new(mul.outputs[0],p.inputs['Base Color'])
    for tex in n:
        if tex.type=='TEX_IMAGE' and tex.image and tex.image.filepath.endswith('Displacement.jpg'):
            bump=n.new('ShaderNodeBump');bump.inputs['Distance'].default_value=.003;bump.inputs['Strength'].default_value=.35;l.new(tex.outputs[0],bump.inputs['Height'])
            if p.inputs['Normal'].is_linked:l.new(p.inputs['Normal'].links[0].from_socket,bump.inputs['Normal'])
            l.new(bump.outputs[0],p.inputs['Normal'])
    return mat

timber=aged_material('Old rain-stained cabin timber','weathered_planks',.85,.22)
sheltered=aged_material('Sheltered rough porch timber','weathered_planks',.78,.07)
roofwood=aged_material('Uneven dark aged wooden shingles','weathered_planks',.50,.28)
mud=aged_material('Damp leaf litter and soil','brown_mud_leaves_01',.57,.07)
bed=aged_material('Shallow stream rounded gravel','river_small_rocks',.66,.16)
treebark=aged_material('Natural camphor bark relief','japanese_camphor_bark',.65,.07)
for mat in [mud,bed]:
    mapping=next(n for n in mat.node_tree.nodes if n.type=='MAPPING');mapping.inputs['Scale'].default_value=(.62,.62,.62)

def grain_uv(ob):
    if ob.type!='MESH' or not ob.data.uv_layers:return
    dims=ob.dimensions;offset=rng.uniform(0,1);strip=(rng.randrange(7)+.5)/7
    for poly in ob.data.polygons:
        axis=max(range(3),key=lambda i:abs(poly.normal[i]));axes=[i for i in range(3) if i!=axis];axes.sort(key=lambda i:dims[i],reverse=True)
        for li in poly.loop_indices:
            v=ob.data.vertices[ob.data.loops[li].vertex_index].co
            ob.data.uv_layers.active.data[li].uv=(v[axes[1]]*.29+strip,v[axes[0]]*.34+offset)

# Reassign actual photographic timber with grain following each structural member.
for ob in list(bpy.data.objects):
    if ob.type!='MESH' or ob.library:continue
    if any(m and m.name in ['Rain-darkened weathered timber','Aged cabin boards'] for m in ob.data.materials):
        mat=sheltered if ob.name.startswith(('Foreground','Porch','Exposed porch')) else timber
        ob.data.materials.clear();ob.data.materials.append(mat);grain_uv(ob)
        if ob.name.startswith(('Front vertical weatherboards','Gable board','Entrance gable boards','Side weatherboards')):
            ob.rotation_euler.z+=rng.uniform(-.004,.004);ob.location.y+=rng.uniform(-.006,.006)
            for v in ob.data.vertices:v.co.x+=rng.uniform(-.0015,.0015)
    if ob.name.startswith(('Irregular bark mapped forest trunk','Round tapered palm trunk')):
        ob.data.materials.clear();ob.data.materials.append(treebark)
    if 'individual overlapping shingles' in ob.name:
        ob.data.materials.clear();ob.data.materials.append(roofwood)

# Make the near wall visible and place the camera inside an extended shelter.
for ob in bpy.data.objects:
    if ob.name.startswith('Foreground weathered wall plank'):
        ob.location.x=-3.55
        for v in ob.data.vertices:
            if v.co.z>0:v.co.z+=.36
    if ob.name=='Foreground shelter roof':
        for v in ob.data.vertices:
            if v.co.x>-2:v.co.x=-.30
            if v.co.y<0:v.co.y=-8.8
    if ob.name=='Porch fascia':ob.location.x=-.30
for i in range(10):
    ob=box('Shelter floor continuation',(-3.8,-8.7+i*.37,.66),(4,.355,.12),sheltered,.01);grain_uv(ob)
for i in range(12):
    ob=box('Shelter wall continuation',(-3.55,-8.6+i*.29,2.90),(.12,.278,4.5),sheltered,.008);grain_uv(ob)
for ob in list(bpy.data.objects):
    if not ob.name.startswith(('Foreground weathered wall plank','Shelter wall continuation')):continue
    hx,hy,hz=[d/2 for d in ob.dimensions];verts=[];faces=[];uv=[];strip=(rng.randrange(7)+.5)/7;offset=rng.uniform(0,1)
    for j in range(19):
        t=j/18;z=-hz+2*hz*t;bow=.005*sin(t*pi*1.4+rng.uniform(-.1,.1))
        notch=rng.uniform(.002,.009) if rng.random()<.18 else .001
        for x,y in [(-hx,-hy),(hx,-hy),(hx,hy),(-hx,hy)]:
            y+=(notch if y<0 else -notch);verts.append((x+bow,y,z));uv.append((y*.29+strip,z*.34+offset))
    for j in range(18):
        for a in range(4):b=j*4+a;c=j*4+(a+1)%4;faces.append((b,c,c+4,b+4))
    faces.extend([(3,2,1,0),(72,73,74,75)])
    temp=mesh('Uneven weathered plank geometry',verts,faces,sheltered,uvs=uv,bevel=.002)
    ob.data=temp.data;bpy.data.objects.remove(temp,do_unlink=True)
    for modifier in ob.modifiers:
        if modifier.type=='BEVEL':modifier.width=.002;modifier.segments=1
    ob.scale.y=rng.uniform(.975,1.025)
    for z in [1.18,3.72]:box('Old porch fastening',(ob.location.x+hx+.003,ob.location.y,z),(.003,.010,.010),iron,.002)

# Remove the solid black interior block; the windows now reveal a real room depth.
remove_prefix(['Cabin interior shadow','Attic window recess'])
roomwall=aged_material('Interior aged timber','old_planks_02',.61,.01)
for name,loc,dim in [('Cabin interior rear wall',(3.7,14.25,3.3),(5.85,.15,2.7)),
                     ('Cabin interior floor',(3.7,12,1.99),(5.8,4.5,.10)),
                     ('Cabin interior ceiling',(3.7,12,4.59),(5.8,4.5,.12))]:
    ob=box(name,loc,dim,roomwall);grain_uv(ob)
for x in [.78,6.60]:box('Cabin room side wall',(x,12.2,3.3),(.10,4.25,2.6),roomwall)
curtain=basic('Unbleached interior curtain',(.19,.145,.085),.91)
for x in [1.34,2.06,3.14,3.86]:
    vs=[];fs=[]
    for j in range(13):
        z=2.62+j*1.27/12
        for i in range(9):vs.append((x-.11+i*.22/8,10.24+.025*sin(i*pi/2),z))
    for j in range(12):
        for i in range(8):a=j*9+i;fs.append((a,a+1,a+10,a+9))
    mesh('Interior gathered linen curtain',vs,fs,curtain,smooth=True)
box('Interior table silhouette',(2.7,12.35,2.7),(1.4,.65,.07),timber)
for x in [2.1,3.3]:box('Interior table leg',(x,12.35,2.34),(.065,.50,.64),timber)
room_light=light('Warm interior room light','AREA',(2.8,12.2,4.35),(1,.56,.27),32,1.2,(2.8,12.0,2.1));room_light.visible_camera=False
light('Warm room bounce','POINT',(3.1,11.5,3.1),(1,.59,.32),5,.32)
glassmat=bpy.data.materials['Old window glass'];pg=glassmat.node_tree.nodes.get('Principled BSDF');pg.inputs['Base Color'].default_value=(.75,.79,.70,1);pg.inputs['Roughness'].default_value=.18

# Practical details and varied joinery at a believable scale.
for ob in list(bpy.data.objects):
    if ob.name.startswith('Worn stone stair'):
        ob.data.materials.clear();ob.data.materials.append(bed)
        for v in ob.data.vertices:
            if v.co.z>0:v.co.z+=rng.uniform(-.009,.009)
    if ob.name.startswith('Front vertical weatherboards'):
        for z in [2.17,4.42]:
            if ob.location.z-ob.dimensions.z/2<z<ob.location.z+ob.dimensions.z/2:
                fastener=box('Recessed dark iron nail',(ob.location.x,9.922,z),(.012,.004,.012),iron,.003)
for i in range(11):
    x=3.65+i*.275;g=terrain_z(x,8.43)
    ob=box('Weathered foundation skirt board',(x,8.44,(g+1.76)/2),(.25,.07,1.76-g),timber,.005);grain_uv(ob)

# A photographed prop is more detailed than the former luminous box lantern.
real_records=json.loads((ROOT/'assets/realism/library.json').read_text());real_collections={}
for asset in sorted(set(v['asset'] for v in real_records)):
    names=[v['collection'] for v in real_records if v['asset']==asset]
    with bpy.data.libraries.load(str(ROOT/'assets/realism'/(asset+'.blend')),link=True) as (src,dst):dst.collections=names
    real_collections[asset]=list(dst.collections)
def scan(asset,name,x,y,size,z=None,angle=None):
    ob=bpy.data.objects.new(name,None);ob.instance_type='COLLECTION';ob.instance_collection=rng.choice(real_collections[asset]);s.collection.objects.link(ob)
    ob.location=(x,y,terrain_z(x,y)-.025 if z is None else z);ob.scale=(size,)*3;ob.rotation_euler.z=rng.uniform(0,2*pi) if angle is None else angle
    return ob
remove_prefix(['Lantern wall bracket','Lantern base','Lantern cap','Lantern slender frame','Lantern luminous wick'])
scan('wooden_lantern_01','Scanned veranda lantern',4.68,9.68,.46,3.34,0)
box('Lantern warm inner diffuser',(4.68,9.66,3.56),(.07,.06,.22),em,.008)
scan('wooden_bucket_01','Old veranda bucket',.96,9.22,.31,2.00,.3)
scan('wooden_bucket_01','Bucket under eave',6.15,8.62,.28,2.00,-.5)

# Rotate the cabin as a complete structure, including attached light and stairs.
prefixes=('Cabin','Veranda','Front vertical','Front horizontal','Side weatherboards','Window','Glazed','Door','Closed aged',
          'Gable','Attic','Weathered roof','Right entrance','Entrance','Worn stone stair','Visible foundation',
          'Interior','Warm cabin','Warm interior','Warm room','Warm room bounce','Lantern','Scanned veranda','Old veranda','Bucket under','Weathered foundation')
members=[o for o in bpy.data.objects if o.name.startswith(prefixes)]
parent=bpy.data.objects.new('Cabin assembly slight oblique view',None);s.collection.objects.link(parent);parent.location=(3.7,11.5,0)
bpy.context.view_layer.update()
for ob in members:
    world=ob.matrix_world.copy();ob.parent=parent;ob.matrix_world=world
parent.rotation_euler.z=.23
bpy.context.view_layer.update()
for ob in members:
    if ob.name.startswith('Cabin timber stilt'):
        center=ob.matrix_world.translation;bottom=min((ob.matrix_world@v.co).z for v in ob.data.vertices)
        correction=terrain_z(center.x,center.y)-.04-bottom
        for v in ob.data.vertices:
            if v.co.z<0:v.co.z+=correction

status('realism_stream_and_ground')
terrain=bpy.data.objects['Sculpted stream banks and rainforest floor'];terrain.data.materials.clear();terrain.data.materials.append(mud);terrain.data.materials.append(bed)
for poly in terrain.data.polygons:
    center=poly.center;poly.material_index=1 if abs(center.x-creek_x(center.y))<1.17 else 0
# Clear, shallow water over a visible rounded gravel bed, with millimetre ripples.
water_ob=bpy.data.objects['Continuous reflective creek surface']
riffles=[(4.9,.075),(8.0,.065),(12.2,.07)]
def surface_raise(y):return sum(height*(.5+.5*math.tanh((y-site)*6)) for site,height in riffles)
def surface_z(y):return water_z(y)+surface_raise(y)
for v in water_ob.data.vertices:
    x,y=v.co.x,v.co.y;u=(x-creek_x(y))/1.04;x=creek_x(y)+u*(1.04+.85*surface_raise(y));v.co.x=x;v.co.z=surface_z(y)+.003*sin(y*8+x*5)+.002*sin(y*17-x*4)
wp=water.node_tree.nodes.get('Principled BSDF');wp.inputs['Base Color'].default_value=(.48,.56,.51,1);wp.inputs['Transmission Weight'].default_value=1;wp.inputs['Roughness'].default_value=.07
for node in water.node_tree.nodes:
    if node.type=='BUMP':node.inputs['Distance'].default_value=.007;node.inputs['Strength'].default_value=.27
remove_prefix(['Rain impact ripple'])
for i in range(46):
    y=rng.uniform(-3,20);x=creek_x(y)+rng.uniform(-.85,.85)
    ob=instance('rock_moss_set_01','Submerged rounded creek pebble',x,y,rng.uniform(.025,.09),terrain_z(x,y)-.015);ob.scale.x*=1.3
for ob in bpy.data.objects:
    if ob.name.startswith('Partly submerged creek stone'):ob.location.z=terrain_z(ob.location.x,ob.location.y)-.025
foam=basic('Aerated water at shallow stone riffles',(.52,.56,.52),.38)
fp=foam.node_tree.nodes.get('Principled BSDF');fp.inputs['IOR'].default_value=1.333;fp.inputs['Transmission Weight'].default_value=.15
fn=foam.node_tree.nodes;fl=foam.node_tree.links;tc=fn.new('ShaderNodeTexCoord');mapping=fn.new('ShaderNodeMapping');mapping.inputs['Scale'].default_value=(5,17,1);fl.new(tc.outputs['UV'],mapping.inputs[0]);noise=fn.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=4.5;noise.inputs['Detail'].default_value=3;fl.new(mapping.outputs[0],noise.inputs[0]);alpha=fn.new('ShaderNodeMapRange');alpha.inputs['From Min'].default_value=.40;alpha.inputs['From Max'].default_value=.70;alpha.inputs['To Min'].default_value=0;alpha.inputs['To Max'].default_value=.67;alpha.clamp=True;fl.new(noise.outputs['Fac'],alpha.inputs['Value']);fl.new(alpha.outputs[0],fp.inputs['Alpha'])
for site,height in riffles:
    for offset in [-.9,-.3,.35,.9]:
        x=creek_x(site)+offset;y=site+rng.uniform(-.035,.035);base=terrain_z(x,y)-.025;h=max(.12,surface_z(y)+.035-base)
        instance('rock_moss_set_01','Natural stone creek ledge',x,y,h,base)
    verts=[];faces=[];uv=[]
    for j in range(23):
        y=site-.42+j*.78/22
        for i in range(29):
            u=-1+i*2/28;x=creek_x(y)+u*.98;verts.append((x,y,surface_z(y)+.006+.003*sin(x*18+y*23)));uv.append((i/28,j/22))
    for j in range(22):
        for i in range(28):a=j*29+i;faces.append((a,a+1,a+30,a+29))
    mesh('Broken whitewater over stone ledge',verts,faces,foam,uvs=uv,smooth=True)

# Ground scans are clustered, grounded and scaled by width instead of moss height.
for i in range(30):
    y=rng.uniform(-1,24);x=creek_x(y)+rng.choice([-1,1])*rng.uniform(1.4,3.0)
    if .3<x<8 and 7<y<16:continue
    scan('root_cluster_01','Scanned exposed bank roots',x,y,rng.uniform(.65,1.6),terrain_z(x,y)-.12)
for i in range(90):
    y=rng.uniform(-2,18);x=creek_x(y)+rng.choice([-1,1])*rng.uniform(1.35,3.0)
    if .3<x<8 and 7<y<16:continue
    scan('bark_debris_01','Irregular fallen bark and litter',x,y,rng.uniform(.10,.35),terrain_z(x,y)-.01)
for i in range(210):
    y=rng.uniform(-2,24);x=creek_x(y)+rng.choice([-1,1])*rng.uniform(1.2,2.7)
    if .3<x<8 and 7<y<16:continue
    scan('moss_01','Fine bank moss colony',x,y,rng.uniform(.14,.45),terrain_z(x,y)-.012)

# Denser, layered understory: avoid a uniformly spaced nursery/garden appearance.
for i in range(220):
    x=rng.uniform(-9,12);y=rng.uniform(4,31)
    if abs(x-creek_x(y))<1.45 or (-.5<x<8.5 and 6.8<y<16.2):continue
    asset=rng.choice(['anthurium_botany_01','fern_02','shrub_04']);instance(asset,'Layered forest regrowth',x,y,rng.uniform(.25,.85))

# Distant mist should soften depth without making a solid luminous blue backdrop.
fm=bpy.data.materials['Subtle depth mist'];n=fm.node_tree.nodes;l=fm.node_tree.links;volume=next(v for v in n if v.type=='PRINCIPLED_VOLUME')
volume.inputs['Color'].default_value=(.68,.72,.75,1);volume.inputs['Anisotropy'].default_value=.16
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=3.4;noise.inputs['Detail'].default_value=2
density=n.new('ShaderNodeMapRange');density.inputs['To Min'].default_value=.0025;density.inputs['To Max'].default_value=.009;l.new(noise.outputs['Fac'],density.inputs['Value']);l.new(density.outputs[0],volume.inputs['Density'])

status('realism_photographic_lighting')
w=s.world;nodes=w.node_tree.nodes;links=w.node_tree.links;nodes.clear()
env=nodes.new('ShaderNodeTexEnvironment');env.image=bpy.data.images.load(str(ROOT/'assets/realism/rainforest_trail/rainforest_trail.hdr'),check_existing=True)
coord=nodes.new('ShaderNodeTexCoord');mapping=nodes.new('ShaderNodeMapping');mapping.inputs['Rotation'].default_value[2]=1.9;links.new(coord.outputs['Generated'],mapping.inputs[0]);links.new(mapping.outputs[0],env.inputs[0])
bg=nodes.new('ShaderNodeBackground');bg.inputs['Strength'].default_value=.16;links.new(env.outputs[0],bg.inputs[0]);output=nodes.new('ShaderNodeOutputWorld');links.new(bg.outputs[0],output.inputs['Surface'])
for name,power,color in [('Large cloud opening',1300,(.64,.73,.86)),('Cool rain backlight',1750,(.42,.57,.78)),('Soft canopy fill',180,(.70,.78,.86))]:
    lamp=bpy.data.objects[name].data;lamp.energy=power;lamp.color=color
bpy.data.objects['Warm cabin lantern'].data.energy=52

# A denser optical rain field with soft edges, not identical bright hard strips.
rainmat=basic('Soft photographic rain exposure',(.5,.6,.7),.2);n=rainmat.node_tree.nodes;l=rainmat.node_tree.links;n.clear()
outnode=n.new('ShaderNodeOutputMaterial');transparent=n.new('ShaderNodeBsdfTransparent');emitter=n.new('ShaderNodeEmission');emitter.inputs[0].default_value=(.48,.57,.68,1);emitter.inputs[1].default_value=.85
tc=n.new('ShaderNodeTexCoord');separate=n.new('ShaderNodeSeparateXYZ');l.new(tc.outputs['Generated'],separate.inputs[0])
sub=n.new('ShaderNodeMath');sub.operation='SUBTRACT';sub.inputs[1].default_value=.5;l.new(separate.outputs['X'],sub.inputs[0]);absolute=n.new('ShaderNodeMath');absolute.operation='ABSOLUTE';l.new(sub.outputs[0],absolute.inputs[0]);edge=n.new('ShaderNodeMapRange');edge.inputs['From Max'].default_value=.5;edge.inputs['To Min'].default_value=.68;edge.inputs['To Max'].default_value=0;l.new(absolute.outputs[0],edge.inputs['Value'])
mix=n.new('ShaderNodeMixShader');l.new(edge.outputs[0],mix.inputs[0]);l.new(transparent.outputs[0],mix.inputs[1]);l.new(emitter.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],outnode.inputs[0])
length=n.new('ShaderNodeMath');length.operation='MULTIPLY';length.inputs[1].default_value=pi;l.new(separate.outputs['Z'],length.inputs[0]);fade=n.new('ShaderNodeMath');fade.operation='SINE';l.new(length.outputs[0],fade.inputs[0]);soft=n.new('ShaderNodeMath');soft.operation='MULTIPLY';l.new(fade.outputs[0],soft.inputs[0]);l.new(edge.outputs[0],soft.inputs[1]);l.new(soft.outputs[0],mix.inputs[0])
for ob in list(raincol.objects):
    local=parent.matrix_world.inverted()@Vector((ob.location.x,ob.location.y,0))
    if (-3.6<local.x<3.6 and -3.9<local.y<3.8) or (ob.location.x<.4 and ob.location.y<3.4):ob.hide_render=True
rainmesh=bpy.data.meshes['Shared rain exposure streak'];rainmesh.materials.clear();rainmesh.materials.append(rainmat)
added=0
for i in range(12000):
    x=rng.uniform(-10,14);y=rng.uniform(-1,32)
    if x<.4 and y<3.4:continue
    local=parent.matrix_world.inverted()@Vector((x,y,0))
    if -3.6<local.x<3.6 and -3.9<local.y<3.8:continue
    bottom=water_z(y)-.08;z=rng.uniform(bottom,14.5);speed=rng.uniform(.21,.35)
    ob=bpy.data.objects.new('Dense storm rain '+str(i),rainmesh);raincol.objects.link(ob);ob.location=(x,y,z);ob.rotation_euler.y=-.065;ob.scale=(rng.uniform(.004,.011),1,rng.uniform(.13,.35))
    ob.driver_add('location',2).driver.expression=f'{bottom:.8f}+(({z-bottom:.8f}-(frame-1)*{speed:.8f})%{14.5-bottom:.8f})';added+=1

# Slightly shifted sheltered camera; the central tree clearing is preserved.
cam.location.x=-.45;cam.rotation_euler=(Vector((.8,10,3.3))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.dof.use_dof=True;cam.data.dof.focus_distance=20;cam.data.dof.aperture_fstop=9
light('Soft reflected porch opening light','AREA',(0,-3,3.2),(.58,.66,.73),24,3.0,(-3.5,-1.8,2.6))
(ROOT/'research/realism'/'build_report.json').write_text(json.dumps({'new_scan_libraries':list(real_collections),'additional_rain_streaks':added,'cabin_rotation_degrees':math.degrees(.23),'hdr_lighting':'rainforest_trail CC0 photographic HDRI','full_photorealism_claimed':False},indent=2))
status('heavy_realism_pass_ready',new_rain_streaks=added)
