"""Palm geometry informed by the real photographic reference board.

Executed in build_scene's namespace; no photographs are used as textures.
Narrow lanceolate pinnae, staggered insertion, gentle V-section, drooping tips,
varying lengths and leaf age replace the wide, regularly paired original strips.
"""
palm=basic('Photograph guided palm cuticle',(.025,.075,.014),.36)
n=palm.node_tree.nodes;l=palm.node_tree.links;p=n.get('Principled BSDF')
p.inputs['Coat Weight'].default_value=.16;p.inputs['Coat Roughness'].default_value=.18
p.inputs['Subsurface Weight'].default_value=.045;p.inputs['Subsurface Radius'].default_value=(.035,.08,.025)
tc=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(tc.outputs['UV'],sep.inputs[0])
mapping=n.new('ShaderNodeMapping');mapping.inputs['Scale'].default_value=(3,45,1);l.new(tc.outputs['UV'],mapping.inputs[0])
veins=n.new('ShaderNodeTexNoise');veins.inputs['Scale'].default_value=2;veins.inputs['Detail'].default_value=2;l.new(mapping.outputs[0],veins.inputs[0])
color=n.new('ShaderNodeValToRGB');color.color_ramp.elements[0].color=(.018,.062,.009,1);color.color_ramp.elements[1].color=(.075,.165,.024,1);l.new(veins.outputs['Fac'],color.inputs[0])
attr=n.new('ShaderNodeAttribute');attr.attribute_name='LeafAge'
age=n.new('ShaderNodeMixRGB');age.inputs[2].default_value=(.10,.085,.017,1);l.new(attr.outputs['Fac'],age.inputs[0]);l.new(color.outputs[0],age.inputs[1]);l.new(age.outputs[0],p.inputs['Base Color'])
bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.10;bump.inputs['Distance'].default_value=.0007;l.new(veins.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
rough=n.new('ShaderNodeMapRange');rough.inputs['To Min'].default_value=.24;rough.inputs['To Max'].default_value=.42;l.new(veins.outputs['Fac'],rough.inputs['Value']);l.new(rough.outputs[0],p.inputs['Roughness'])

def frond(name,base,angle,length,rise,droop):
    rng=random.Random(name);base=Vector(base);forward=Vector((cos(angle),sin(angle),0));side=Vector((-sin(angle),cos(angle),0))
    curve_bias=rng.uniform(-.16,.16)
    def center(t):return base+forward*(length*t)+side*(curve_bias*sin(t*pi))+Vector((0,0,rise*sin(t*pi*.8)-droop*t*t))
    curve(name+' tapered rachis',[center(i/64) for i in range(65)],.0065,palm)
    vs=[];fs=[];uv=[];ages=[];count=int(length*13)+5
    for i in range(count):
        for sign in [-1,1]:
            if rng.random()<.035:continue
            t=.09+i*.86/count+rng.uniform(-.003,.003)+(0.006 if sign==1 else 0)
            root=center(t);lng=(sin(t*pi)**.72)*length*.245*(1-.22*t)*rng.uniform(.74,1.16)
            half_width=(.014+lng*.025)*rng.uniform(.84,1.18)
            sweep=rng.uniform(.28,.64);bend=rng.uniform(.19,.52);twist=rng.uniform(-.22,.22)
            aged=rng.uniform(0,.12) if rng.random()>.06 else rng.uniform(.18,.42)
            damaged=rng.random()<.07;damage_pos=rng.uniform(.45,.88)
            k=len(vs);along=25;across=7
            for j in range(along):
                u=j/(along-1)
                middle=root+side*(sign*lng*u)+forward*(lng*(sweep*u+.05*sin(pi*u)))+Vector((0,0,-lng*bend*u*u+.035*sin(u*pi)))
                width=half_width*(sin(pi*u)**.62)*(1-.25*u)
                for a in range(across):
                    v=-1+2*a/(across-1);edge_damage=(1-.45*math.exp(-((u-damage_pos)/.035)**2)) if damaged and v>.3 else 1
                    fold=half_width*.27*(1-abs(v)**1.6)*sin(pi*u)
                    flutter=half_width*.10*sin(u*pi*3+i*.7)*v
                    pos=middle+forward*(v*width*edge_damage)+Vector((0,0,fold+flutter+twist*v*width*u))
                    vs.append(pos);uv.append((u,(v+1)/2));ages.append(aged+max(0,u-.85)*.4)
            for j in range(along-1):
                for a in range(across-1):b=k+j*across+a;fs.append((b,b+1,b+across+1,b+across))
    ob=mesh(name+' curved pinnae',vs,fs,palm,uvs=uv,smooth=True)
    age=ob.data.attributes.new('LeafAge','FLOAT','POINT')
    for elem,value in zip(age.data,ages):elem.value=value
    return ob

def organic_trunk(name,x,y,z,height,radius,seed):
    rng=random.Random(seed);leanx=rng.uniform(-.7,.7);leany=rng.uniform(-.6,.6)
    vs=[];fs=[];uv=[];rings=25;sides=14
    for j in range(rings):
        t=j/(rings-1);cx=x+leanx*t*t+.06*sin(t*pi*2);cy=y+leany*t*t;rad=radius*(1-.36*t)*(1+.028*sin(t*50))
        for i in range(sides+1):
            a=i*2*pi/sides;r=rad*(1+.035*sin(a*5+seed))
            vs.append((cx+r*cos(a),cy+r*sin(a),z+height*t));uv.append((i/sides,t*height/1.4))
    for j in range(rings-1):
        for i in range(sides):a=j*(sides+1)+i;fs.append((a,a+1,a+sides+2,a+sides+1))
    return mesh(name,vs,fs,bark,uvs=uv,smooth=True)

for i,(ang,lng,rise,droop) in enumerate([(2.6,3.1,.9,1.6),(2.05,3.5,1.0,1.8),(3.18,2.4,.6,1.3),(1.5,3.1,1.1,.9),(3.6,2.5,.5,1.5)]):
    frond('Near right palm '+str(i),(6.0,.9,2.0),ang,lng,rise,droop)
frond('Large foreground arching palm',(6.4,-.5,1.2),2.15,4.5,3.0,1.2)
frond('Low foreground palm',(6.0,-.5,1.2),2.8,3.0,1.3,1.4)
for i,ang in enumerate([3.5,3.85,4.1,4.45]):frond('Overhead palm '+str(i),(5.5,4,6.5),ang,4.3,.25,1.7)
for i,(x,y) in enumerate([(-5,8),(9,10),(-6,16),(10,20),(-8,22)]):
    z=terrain_z(x,y);organic_trunk('Round tapered palm trunk',x,y,z,6.5-z,.13,100+i)
    rng=random.Random(540+i)
    for j in range(8):
        frond('Midground palm '+str(i)+' '+str(j),(x,y,6.5),j*2*pi/8+rng.uniform(-.24,.24),rng.uniform(2.2,3.4),rng.uniform(.4,1.0),rng.uniform(1.0,2.1))
(ROOT/'research'/'palm_relocation.json').write_text(json.dumps({'palm':'Midground palm 4','old_base_xy':[-2,22],'new_base_xy':[-8,22],
    'reason':'Move the isolated bright palm out of the central opening, with its trunk and all eight fronds.'},indent=2))

# The earlier cylinders had no useful bark UVs and read as blue plastic poles.
for ob in list(bpy.data.objects):
    if ob.name.startswith('Distant rainforest trunk'):bpy.data.objects.remove(ob,do_unlink=True)
rng=random.Random(7381)
for i in range(34):
    x=rng.uniform(-18,19);y=rng.uniform(18,49);z=terrain_z(x,y)
    organic_trunk('Irregular bark mapped forest trunk',x,y,z,rng.uniform(14,23),rng.uniform(.10,.25),800+i)
