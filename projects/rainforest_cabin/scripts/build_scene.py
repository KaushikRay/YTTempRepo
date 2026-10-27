"""Reference-led rainforest cabin. Real geometry + CC0 scans, rendered in Cycles."""
import bpy, math, random, json, os, time
from pathlib import Path
from mathutils import Vector
from math import sin, cos, pi

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'renders';OUT.mkdir(exist_ok=True)
random.seed(7231)
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene

def status(phase,**values):
    (ROOT/'status.json').write_text(json.dumps({'phase':phase,'updated_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),**values},indent=2))
    print(phase,values,flush=True)

status('building_geometry')

def basic(name,color,rough=.5,metal=0):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1)
    p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=metal
    return m

def pbr(name,asset,scale=1,dark=.55,wet=.3):
    m=basic(name,(.1,.1,.1));n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF')
    tex=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeMapping');mapping.inputs['Scale'].default_value=(scale,scale,scale);l.new(tex.outputs['UV'],mapping.inputs['Vector'])
    for kind in ['Diffuse','Rough','nor_gl','Displacement']:
        path=ROOT/'assets'/asset/(kind+'.jpg')
        if not path.exists():continue
        im=n.new('ShaderNodeTexImage');im.image=bpy.data.images.load(str(path),check_existing=True);l.new(mapping.outputs['Vector'],im.inputs['Vector'])
        if kind!='Diffuse':im.image.colorspace_settings.name='Non-Color'
        if kind=='Diffuse':
            mul=n.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;mul.inputs[2].default_value=(dark,dark,dark,1);l.new(im.outputs['Color'],mul.inputs[1]);l.new(mul.outputs[0],p.inputs['Base Color'])
        elif kind=='Rough':
            mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY_ADD';mul.inputs[1].default_value=.45;mul.inputs[2].default_value=.12;l.new(im.outputs[0],mul.inputs[0]);l.new(mul.outputs[0],p.inputs['Roughness'])
        elif kind=='nor_gl':
            normal=n.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.7;l.new(im.outputs[0],normal.inputs['Color']);l.new(normal.outputs[0],p.inputs['Normal'])
    p.inputs['Coat Weight'].default_value=wet;p.inputs['Coat Roughness'].default_value=.17
    return m

wood=pbr('Rain-darkened weathered timber','weathered_plank_siding',1,.48,.25)
wood_light=pbr('Aged cabin boards','weathered_plank_siding',1,.72,.16)
roofmat=pbr('Wet grey roof shingles','grey_roof_tiles',.55,.45,.45)
groundmat=pbr('Soaked rainforest floor','forest_ground_04',.55,.42,.1)
bark=pbr('Damp palm bark','palm_bark',1,.35,.12)
dark=basic('Dark interior and plank joints',(.009,.012,.01),.85)
iron=basic('Blackened lantern and fasteners',(.022,.027,.025),.36,.75)
moss=basic('Wet fine moss',(.025,.063,.013),.76)

def mesh(name,verts,faces,mat,uvs=None,bevel=0,smooth=False):
    me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new(name,me);s.collection.objects.link(ob)
    if mat:me.materials.append(mat)
    uv=me.uv_layers.new()
    for poly in me.polygons:
        if smooth:poly.use_smooth=True
        normal=poly.normal;axis=max(range(3),key=lambda i:abs(normal[i]));dims=[i for i in range(3) if i!=axis]
        for li in poly.loop_indices:
            v=me.vertices[me.loops[li].vertex_index].co
            uv.data[li].uv=uvs[me.loops[li].vertex_index] if uvs else (v[dims[0]]*.7,v[dims[1]]*.7)
    if bevel:
        mod=ob.modifiers.new('Soft weathered edges','BEVEL');mod.width=bevel;mod.segments=2
    return ob

def box(name,loc,dim,mat,bevel=.012):
    x,y,z=[v/2 for v in dim]
    verts=[(-x,-y,-z),(-x,-y,z),(-x,y,-z),(-x,y,z),(x,-y,-z),(x,-y,z),(x,y,-z),(x,y,z)]
    faces=[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)]
    ob=mesh(name,verts,[tuple(reversed(f)) for f in faces],mat,bevel=bevel)
    if mat in [wood,wood_light,bark]:
        offset=random.uniform(0,1);strip=random.randrange(11)/11+.042
        for poly in ob.data.polygons:
            face_axis=max(range(3),key=lambda i:abs(poly.normal[i]));axes=[i for i in range(3) if i!=face_axis];axes.sort(key=lambda i:dim[i],reverse=True)
            for li in poly.loop_indices:
                v=ob.data.vertices[ob.data.loops[li].vertex_index].co
                ob.data.uv_layers.active.data[li].uv=(v[axes[0]]*.38+offset,v[axes[1]]*.20+strip)
    ob.location=loc;return ob

def curve(name,points,radius,mat):
    cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=2;cu.bevel_depth=radius;cu.bevel_resolution=2
    sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
    for p,v in zip(sp.points,points):p.co=(*v,1)
    ob=bpy.data.objects.new(name,cu);s.collection.objects.link(ob);cu.materials.append(mat);return ob

def beam(name,a,b,width,mat=wood):
    a=Vector(a);b=Vector(b);ob=box(name,(a+b)*.5,(width,width,(b-a).length),mat,.008);ob.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return ob

def creek_x(y):return 1.5-.16*y+sin(y*.3)
def water_z(y):return .15+.025*y+.035*sin(y*.8)
def terrain_z(x,y):
    d=abs(x-creek_x(y));bank=1-math.exp(-(d/1.18)**4)
    return water_z(y)-.22+bank*(.72+.1*sin(x*.4+y*.2))+.055*sin(x*2.1+y*.8)*bank+.04*sin(x*5-y*2.7)*bank

# Continuous stream trough; planting uses the very same surface function.
verts=[];faces=[];nx=180;ny=220
for j in range(ny+1):
    y=-9+j*64/ny
    for i in range(nx+1):
        x=-23+i*46/nx;verts.append((x,y,terrain_z(x,y)))
for j in range(ny):
    for i in range(nx):
        a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
mesh('Sculpted stream banks and rainforest floor',verts,faces,groundmat,smooth=True)

# Front sheltered porch: view is from beneath this roof, not in the rain.
for i in range(20):
    y=-5+i*.39
    box('Foreground porch floorboard',(-3.8,y,.66),(4.0,.375,.12),wood)
for j in range(31):
    y=-5+j*.26
    box('Foreground weathered wall plank',(-5.55,y,2.72),(.12,.249,4.05),wood,.006)
for y in [-4.8,-.7,2.3]:
    box('Porch structural post',(-1.85,y,2.58),(.28,.30,3.95),wood,.018)
    beam('Porch knee brace',(-1.85,y,3.5),(-2.7,y,4.4),.13)
box('Porch header',(-1.85,-1.2,4.5),(.28,7.8,.26),wood)
mesh('Foreground shelter roof',[(-6,-5.8,5.6),(-1.15,-5.8,4.65),(-1.15,3.2,4.65),(-6,3.2,5.6)],[(0,1,2,3)],roofmat)
box('Porch fascia',(-1.15,-1.3,4.63),(.14,9.0,.22),wood)
for y in [-4.6,-3.2,-1.8,-.4,1,2.4]:
    beam('Exposed porch rafters',(-5.6,y,5.52),(-1.1,y,4.6),.12)
box('Porch front rim',(-3.75,2.6,.47),(4.15,.2,.45),wood)

# Main cabin, front veranda and genuine dark recesses behind windows/door.
cx=3.7;front=10.0;back=14.5;floor=1.95;eave=4.65;ridge=7.0
box('Cabin interior shadow',(cx,12.2,3.25),(5.7,4.35,2.65),dark)
for x in [.7,3.7,6.7]:
    for y in [8.6,10.1,14.3]:
        g=terrain_z(x,y);box('Cabin timber stilt',(x,y,(g+floor)/2),(.23,.23,floor-g+.15),wood)
for x in [.68,6.72]:beam('Visible foundation diagonal',(x,8.8,.85),(x,10.1,1.9),.13)
for i in range(26):
    x=.52+i*.247
    box('Cabin veranda deck',(x,11.45,floor),(.236,6.1,.095),wood)
box('Veranda rim joist',(cx,8.42,1.78),(6.5,.19,.32),wood)

# Leave front apertures for 2 windows and an offset door, rather than pasted-on rectangles.
windows=[(1.7,3.25,.75,1.35),(3.5,3.25,.75,1.35)]
doorx=5.5
for i in range(29):
    x=.72+i*.207
    spans=[(floor+.08,eave)]
    holes=[]
    for wx,wz,ww,wh in windows:
        if abs(x-wx)<ww/2+.08:holes.append((wz-wh/2,wz+wh/2))
    if abs(x-doorx)<.51:holes.append((floor,4.22))
    for lo,hi in holes:
        spans=[seg for a,b in spans for seg in [(a,min(b,lo)),(max(a,hi),b)] if seg[1]-seg[0]>.04]
    for a,b in spans:box('Front vertical weatherboards',(x,front,(a+b)/2),(.198,.12,b-a),wood_light,.004)
for side in [.67,6.74]:
    for j in range(22):
        y=10.1+j*.205;box('Side weatherboards',(side,y,3.33),(.12,.196,2.68),wood_light,.005)
for x in [.65,6.75]:box('Cabin corner frame',(x,12.2,3.3),(.18,4.8,.18),wood)
for z in [floor+.13,eave-.08]:box('Front horizontal wall frame',(cx,front-.08,z),(6.3,.16,.16),wood)
for x in [.6,2.65,4.5,6.8]:
    box('Veranda supporting post',(x,8.57,3.13),(.14,.14,2.45),wood)
    beam('Veranda short knee brace',(x,8.57,3.75),(x+.38,8.57,4.3),.075)
# Low railing with irregular slender wooden balusters.
for x1,x2 in [(.65,2.58),(2.72,4.42)]:
    for z in [2.18,2.91]:box('Veranda railing',((x1+x2)/2,8.54,z),(x2-x1,.08,.09),wood)
    for k in range(9):box('Veranda baluster',(x1+.12+k*(x2-x1-.24)/8,8.54,2.55),(.038,.042,.70),wood,.004)

glass=basic('Old window glass',(.14,.19,.16),.13)
pg=glass.node_tree.nodes.get('Principled BSDF');pg.inputs['Transmission Weight'].default_value=.92;pg.inputs['IOR'].default_value=1.46
for wx,wz,ww,wh in windows:
    box('Glazed recessed window',(wx,front-.045,wz),(ww,.012,wh),glass,.001)
    for x in [wx-ww/2-.04,wx,wx+ww/2+.04]:box('Window vertical mullion',(x,front-.12,wz),(.055,.065,wh+.15),wood)
    for z in [wz-wh/2-.04,wz,wz+wh/2+.04]:box('Window crossbar',(wx,front-.13,z),(ww+.15,.07,.055),wood)
    box('Window sill',(wx,front-.18,wz-wh/2-.07),(ww+.24,.3,.09),wood)
for x in [doorx-.55,doorx+.55]:box('Door jamb',(x,front-.08,3.05),(.12,.16,2.3),wood)
box('Door lintel',(doorx,front-.08,4.23),(1.23,.18,.14),wood)
for i in range(5):box('Closed aged door board',(doorx-.42+i*.21,front-.02,3.04),(.20,.13,2.13),wood_light,.005)
for z in [2.3,3.8]:box('Door wrought strap',(doorx-.15,front-.115,z),(.67,.04,.055),iron,.006)

# Gable infill boards, structurally supported ridge and bargeboards.
for i in range(29):
    x=.7+i*.214;top=ridge-abs(x-cx)*(ridge-eave)/3.15
    if top>eave:
        spans=[(eave,top)]
        if abs(x-cx)<.45:spans=[(eave,5.24),(6.22,top)]
        for lo,hi in spans:
            if hi>lo:box('Gable board',(x,front,(hi+lo)/2),(.204,.12,hi-lo),wood_light,.004)
box('Attic window recess',(cx,front+.04,5.73),(.9,.15,.98),dark)
box('Attic window glass',(cx,front-.07,5.73),(.86,.014,.95),glass,.001)
for x in [cx-.47,cx,cx+.47]:box('Attic timber mullion',(x,front-.13,5.73),(.07,.07,1.09),wood)
for z in [5.20,5.73,6.25]:box('Attic window crossbar',(cx,front-.14,z),(1.02,.07,.065),wood)
beam('Gable tie beam',(.45,front-.08,eave),(6.95,front-.08,eave),.18)
beam('Gable center king post',(cx,front-.13,eave),(cx,front-.13,ridge),.14)
for sign in [-1,1]:
    beam('Gable diagonal framing',(cx,front-.12,eave),(cx+sign*1.9,front-.12,eave+.9),.11)

def shingled_roof(name,cx,ya,yb,eavez,ridgez,half):
    vs=[];fs=[]
    for side in [-1,1]:
        mesh(name+' under-roof',[(cx,ya,ridgez),(cx+side*half,ya,eavez),(cx+side*half,yb,eavez),(cx,yb,ridgez)],[(0,1,2,3)],wood)
        steps=int(half/.22)
        for row in range(steps+1):
            ss=min(row*.22,half-.1);length=.32
            for col in range(int((yb-ya)/.32)+1):
                y=ya+col*.32+(row%2)*.16
                if y>yb:continue
                a=ss;b=min(ss+length,half+.03);y2=min(y+.315,yb+.04);jitter=random.uniform(-.012,.012)
                pts=[]
                for dz in [0,.035]:
                    for t,yy in [(a,y),(b,y),(b,y2),(a,y2)]:
                        pts.append((cx+side*t,yy,ridgez-(ridgez-eavez)*t/half+.018+jitter+dz))
                k=len(vs);vs+=pts;fs.extend(tuple(k+i for i in f) for f in [(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)])
        beam('Weathered roof bargeboard',(cx,ya-.025,ridgez),(cx+side*half,ya-.025,eavez),.12)
    mesh(name+' individual overlapping shingles',vs,fs,roofmat,bevel=.006)
    beam(name+' ridge cap',(cx,ya-.06,ridgez+.045),(cx,yb+.05,ridgez+.045),.12,roofmat)

shingled_roof('Cabin pitched roof',cx,9.65,14.9,eave,ridge,3.45)
# Front lean-to over the veranda.
mesh('Veranda lean-to tiled roof',[(.25,8.0,4.2),(7.15,8,4.2),(7.15,10.25,4.95),(.25,10.25,4.95)],[(0,1,2,3)],roofmat)
box('Veranda eave fascia',(cx,8,4.17),(7,.14,.18),wood)
for x in [.5,2.4,4.6,6.9]:beam('Veranda exposed rafters',(x,7.95,4.17),(x,10.2,4.92),.095)
# Small gabled entrance breaks the otherwise uniform veranda silhouette.
shingled_roof('Right entrance gable',5.6,7.65,9.6,3.90,4.92,1.10)
for x in [4.55,6.65]:box('Entrance canopy post',(x,7.82,2.94),(.12,.12,2.10),wood)
for i in range(11):
    x=4.6+i*.2;top=4.92-abs(x-5.6)*1.02/1.1
    if top>3.93:box('Entrance gable boards',(x,7.70,(3.93+top)/2),(.19,.09,top-3.93),wood_light,.004)

# Stone approach steps to the opening at the right end of the rail.
stonemat=basic('Wet cut stepping stones',(.11,.13,.13),.27)
for i in range(7):
    y=6.15+i*.35;top=1.0+i*.145
    ob=box('Worn stone stair',(5.45+random.uniform(-.035,.035),y,top-.10),(1.25+random.uniform(-.1,.1),.48,.20),stonemat,.065);ob.rotation_euler.z=random.uniform(-.03,.03)

# Warm lantern, with a visible shade/frame and internal light, not a glowing cube.
em=basic('Lantern warm wick',(.65,.23,.035),.3);p=em.node_tree.nodes.get('Principled BSDF');p.inputs['Emission Color'].default_value=(1,.43,.10,1);p.inputs['Emission Strength'].default_value=8
lx=4.7;ly=9.68;lz=3.62
box('Lantern wall bracket',(lx,9.91,lz+.24),(.08,.26,.05),iron)
box('Lantern base',(lx,ly,lz-.23),(.28,.24,.06),iron)
box('Lantern cap',(lx,ly,lz+.23),(.34,.30,.08),iron)
for dx in [-.12,.12]:
    for dy in [-.1,.1]:beam('Lantern slender frame',(lx+dx,ly+dy,lz-.22),(lx+dx,ly+dy,lz+.22),.018,iron)
box('Lantern luminous wick',(lx,ly,lz),(.045,.04,.27),em,.01)

def light(name,typ,loc,color,power,size=1,target=None):
    data=bpy.data.lights.new(name,typ);data.energy=power;data.color=color
    ob=bpy.data.objects.new(name,data);s.collection.objects.link(ob);ob.location=loc
    if typ=='AREA':data.shape='DISK';data.size=size
    if typ=='POINT':data.shadow_soft_size=size
    if target:ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler()
    return ob

light('Warm cabin lantern','POINT',(lx,ly-.12,lz),(1,.42,.13),85,.13)
light('Interior reflected warm light','AREA',(2.5,10.25,3.2),(1,.50,.24),22,1.4,(2.5,8.5,3))

status('architecture_ready')

# Load linked normalized specimens. Instance exactly one specimen per planting.
records=json.loads((ROOT/'assets'/'library.json').read_text());specimens={}
for asset in sorted(set(r['asset'] for r in records)):
    names=[r['collection'] for r in records if r['asset']==asset]
    with bpy.data.libraries.load(str(ROOT/'assets'/(asset+'.blend')),link=True) as (src,dst):dst.collections=names
    specimens[asset]=list(dst.collections)

def instance(asset,name,x,y,height,z=None,angle=None):
    ob=bpy.data.objects.new(name,None);ob.instance_type='COLLECTION';ob.instance_collection=random.choice(specimens[asset]);s.collection.objects.link(ob)
    ob.location=(x,y,terrain_z(x,y)-.025 if z is None else z);ob.scale=(height,height,height);ob.rotation_euler.z=random.uniform(0,2*pi) if angle is None else angle
    return ob

# Low rocks are partly buried in both banks. Vary source specimens and shape.
for i in range(78):
    y=random.uniform(-3,28);side=random.choice([-1,1]);x=creek_x(y)+side*random.uniform(.8,1.9)
    ob=instance('rock_moss_set_01','Scanned mossy bank rock',x,y,random.uniform(.18,.58));ob.scale.x*=random.uniform(.9,1.7);ob.scale.y*=random.uniform(.9,1.4);ob.location.z-=.10
for i in range(16):
    y=random.uniform(-2,30);x=creek_x(y)+random.uniform(-.65,.65)
    ob=instance('rock_moss_set_01','Partly submerged creek stone',x,y,random.uniform(.10,.26),water_z(y)-.16)

# Tropical floor. Leave the creek, steps, porch and cabin footprint clear.
planted=0
for i in range(700):
    x=random.uniform(-11,13);y=random.uniform(-3,32)
    if abs(x-creek_x(y))<1.65:continue
    if -.1<x<7.8 and 7.8<y<15.5:continue
    if 4.6<x<6.3 and 5.5<y<8.6:continue
    if x< -1.7 and y<3:continue
    asset=random.choices(['fern_02','calathea_orbifolia_01','anthurium_botany_01','shrub_04'],[.46,.12,.24,.18])[0]
    h=random.uniform(.22,.72)*(1.35 if y>15 else 1)
    instance(asset,'Wet understory '+str(planted),x,y,h);planted+=1
for x,y,h in [(-.15,-.8,1.05),(-.45,2.4,.95),(2.8,1.1,.7),(6.4,4.3,1.2),(-2.6,6.2,1.25),(-3.8,11,1.7),(-.8,6,.75)]:
    if abs(x-creek_x(y))>1.1:instance('fern_02','Foreground hero fern',x,y,h)
for i in range(90):
    y=random.uniform(-1.5,18);side=random.choice([-1,1]);x=creek_x(y)+side*random.uniform(1.35,2.05)
    if .2<x<7.8 and 7.7<y<15.5:continue
    if 4.5<x<6.5 and 5.5<y<8.7:continue
    instance(random.choice(['fern_02','anthurium_botany_01']),'Dense fern bank',x,y,random.uniform(.22,.56))
for i in range(23):
    x=random.uniform(-13,14);y=random.uniform(5,39)
    if -.6<x<8 and 6<y<16:continue
    if abs(x-creek_x(y))<1.6:continue
    if y<15 and -3<x<10:continue
    instance('pachira_aquatica_01','Tropical middle canopy',x,y,random.uniform(2.5,4.5))
for x,y,h in [(-12,25,19),(-7,34,23),(-1,32,25),(5,33,26),(12,27,23),(18,22,21),(-16,38,25),(8,43,26),(18,39,26),(-20,22,23)]:
    ob=instance('island_tree_02','Layered rainforest canopy',x,y,h);ob.scale.x*=.65;ob.scale.y*=.65
# Slender trunks give the deep forest vertical structure without a foreground leaf curtain.
for i in range(38):
    x=random.uniform(-18,19);y=random.uniform(18,49);z=terrain_z(x,y);h=random.uniform(14,23)
    curve('Distant rainforest trunk',[(x,y,z),(x+.1,y+.1,z+h*.45),(x+random.uniform(-.5,.5),y+.25,z+h)],random.uniform(.09,.22),bark)

status('scanned_vegetation_ready',understory_instances=planted)

# Reference-led palms and properly mapped forest trunks.
exec(compile((ROOT/'scripts'/'photographic_foliage.py').read_text(), str(ROOT/'scripts'/'photographic_foliage.py'), 'exec'))

# Stream: genuinely reflective refractive surface over a textured bed.
water=basic('Rain-agitated clear stream',(.025,.055,.06),.11)
p=water.node_tree.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=.86;p.inputs['IOR'].default_value=1.333
n=water.node_tree.nodes;l=water.node_tree.links;tc=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeMapping');mapping.inputs['Scale'].default_value=(2.6,.24,1);l.new(tc.outputs['Generated'],mapping.inputs[0])
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=55;noise.inputs['Detail'].default_value=3;l.new(mapping.outputs[0],noise.inputs['Vector']);b=n.new('ShaderNodeBump');b.inputs['Strength'].default_value=.35;b.inputs['Distance'].default_value=.045;l.new(noise.outputs['Fac'],b.inputs['Height']);l.new(b.outputs[0],p.inputs['Normal'])
vs=[];fs=[]
for j in range(321):
    y=-8+j*47/320
    for i in range(17):
        u=-1.04+i*2.08/16;x=creek_x(y)+u
        z=water_z(y)+.015*sin(y*8+x*5)+.008*sin(y*17-x*4)
        vs.append((x,y,z))
for j in range(320):
    for i in range(16):a=j*17+i;fs.append((a,a+1,a+18,a+17))
mesh('Continuous reflective creek surface',vs,fs,water,smooth=True)

# Gentle optical ripple rings, partly submerged; no opaque white foam discs.
for i in range(70):
    y=random.uniform(-3,25);x=creek_x(y)+random.uniform(-.85,.85);r=random.uniform(.035,.16)
    pts=[(x+r*cos(a*2*pi/36),y+r*sin(a*2*pi/36),water_z(y)+.017) for a in range(37)]
    curve('Rain impact ripple',pts,.0025,water)

# Layered, independently recycling rain. Shared mesh, fixed fractional-frame streak length.
rain=basic('Rain water streaks',(.25,.36,.4),.16)
p=rain.node_tree.nodes.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=.45;p.inputs['Emission Color'].default_value=(.20,.32,.4,1);p.inputs['Emission Strength'].default_value=.12
n=rain.node_tree.nodes;l=rain.node_tree.links;out=n.get('Material Output');mix=n.new('ShaderNodeMixShader');tr=n.new('ShaderNodeBsdfTransparent');emrain=n.new('ShaderNodeEmission');emrain.inputs['Color'].default_value=(.24,.39,.57,1);emrain.inputs['Strength'].default_value=.9;mix.inputs[0].default_value=.35;l.new(tr.outputs[0],mix.inputs[1]);l.new(emrain.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs['Surface'])
me=bpy.data.meshes.new('Shared rain exposure streak');me.from_pydata([(-.5,0,0),(.5,0,0),(.25,0,-1),(-.25,0,-1)],[],[(0,1,2,3)]);me.materials.append(rain)
raincol=bpy.data.collections.new('Continuously replenishing rain');s.collection.children.link(raincol)
for i in range(10000):
    x=random.uniform(-13,15);y=random.uniform(-1,39);bottom=water_z(y)-.05;z=random.uniform(bottom,16)
    if x< -1.1 and y<3:continue
    if .3<x<7.3 and 8<y<15.1:continue
    ob=bpy.data.objects.new('Rain streak '+str(i),me);raincol.objects.link(ob);ob.location=(x,y,z);ob.rotation_euler.y=-.055
    ob.scale=(random.uniform(.003,.007),1,random.uniform(.13,.32))
    speed=random.uniform(.21,.34)
    ob.driver_add('location',2).driver.expression=f'{bottom:.8f}+(({z-bottom:.8f}-(frame-1)*{speed:.8f})%{16-bottom:.8f})'

# Individual eave runoff strands and drips, at gaps beyond the shelter line.
for i in range(25):
    x=random.uniform(.4,7.0);y=7.96
    length=random.uniform(.18,.8)
    curve('Cabin eave runoff',[(x,y,4.2),(x+.005,y,4.2-length)],.0025,water)

status('lighting_and_camera')
s.world=bpy.data.worlds.new('Overcast rainforest night');s.world.use_nodes=True
bg=s.world.node_tree.nodes.get('Background');bg.inputs[0].default_value=(.12,.20,.31,1);bg.inputs[1].default_value=.42
light('Large cloud opening','AREA',(-3,11,17),(.46,.62,.88),4300,16,(1,9,0))
light('Cool rain backlight','AREA',(-1,26,10),(.18,.40,1),4700,11,(0,4,2))
light('Soft canopy fill','AREA',(7,-1,10),(.58,.70,.82),850,9,(1,6,1))

fogmat=bpy.data.materials.new('Subtle depth mist');fogmat.use_nodes=True;n=fogmat.node_tree.nodes;n.clear();o=n.new('ShaderNodeOutputMaterial');v=n.new('ShaderNodeVolumePrincipled');v.inputs['Density'].default_value=.008;v.inputs['Color'].default_value=(.30,.46,.64,1);v.inputs['Anisotropy'].default_value=.23;fogmat.node_tree.links.new(v.outputs['Volume'],o.inputs['Volume'])
box('Forest depth mist',(0,29,10),(48,39,22),fogmat,0)

bpy.ops.object.camera_add(location=(0,-8,2.65));cam=bpy.context.object;cam.name='Sheltered porch reference camera';target=Vector((.8,10,3.3));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=33;cam.data.sensor_width=36;s.camera=cam
cam.data.dof.use_dof=False
exec(compile((ROOT/'scripts'/'clear_central_view.py').read_text(),str(ROOT/'scripts'/'clear_central_view.py'),'exec'))
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=int(os.environ.get('SAMPLES','32'));s.cycles.use_denoising=True
s.cycles.max_bounces=8;s.cycles.diffuse_bounces=3;s.cycles.glossy_bounces=4;s.cycles.transmission_bounces=6;s.cycles.transparent_max_bounces=20;s.cycles.use_adaptive_sampling=True;s.cycles.adaptive_threshold=.035;s.cycles.adaptive_min_samples=16
s.render.threads_mode='FIXED';s.render.threads=6;s.render.resolution_x=int(os.environ.get('WIDTH','960'));s.render.resolution_y=round(s.render.resolution_x*9/16);s.render.resolution_percentage=100
s.render.image_settings.file_format='PNG';s.render.film_transparent=False;s.render.fps=24;s.frame_end=240;s.frame_set(1)
s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=.25
s.render.use_compositing=True;s.use_nodes=True;n=s.node_tree.nodes;n.clear();rl=n.new('CompositorNodeRLayers');gl=n.new('CompositorNodeGlare');gl.glare_type='FOG_GLOW';gl.quality='HIGH';gl.threshold=2.5;gl.mix=-.94;out=n.new('CompositorNodeComposite');s.node_tree.links.new(rl.outputs['Image'],gl.inputs['Image']);s.node_tree.links.new(gl.outputs[0],out.inputs[0])

# Portable paths. Library textures packed; architectural texture files supplied with project.
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(lib.filepath,start=str(ROOT))
for im in bpy.data.images:
    if im.library is None and im.source=='FILE' and not im.packed_file:im.filepath=bpy.path.relpath(im.filepath,start=str(ROOT))
credits=bpy.data.texts.new('ASSET_CREDITS');credits.write((ROOT/'assets'/'CREDITS.txt').read_text())
filename=os.environ.get('OUTPUT','composition.png');s.render.filepath='//renders/'+filename
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'rainforest_cabin.blend'),compress=True)
status('rendering',width=s.render.resolution_x,height=s.render.resolution_y,samples=s.cycles.samples,output=filename)
bpy.ops.render.render(write_still=True)
status('complete',output=filename,animation_rendered=False)
print('RAINFOREST STILL COMPLETE',flush=True)
os._exit(0)
