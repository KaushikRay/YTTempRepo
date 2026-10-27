"""Locked-camera 2.5D Blender animation from explicitly generated image layers.

No video generation or frame interpolation: Cycles renders the deforming palms,
masked stream texture advection, optical rain geometry and runoff every frame.
The detailed cabin/forest remain a generated matte, not modeled architecture.
"""
import bpy, json, math, os, random, time, traceback
from pathlib import Path
from mathutils import Vector
from mathutils.geometry import tessellate_polygon

ROOT=Path(__file__).resolve().parents[1]
W,H=16.,9.
R=random.Random(6142)

def driver(socket,expression):
    d=socket.driver_add('default_value').driver;d.expression=expression

def material(name):
    m=bpy.data.materials.new(name);m.use_nodes=True
    n=m.node_tree.nodes;n.clear()
    out=n.new('ShaderNodeOutputMaterial')
    return m,n,m.node_tree.links,out

def mesh(name,verts,faces,mat,uv=True):
    data=bpy.data.meshes.new(name);data.from_pydata(verts,[],faces);data.update()
    ob=bpy.data.objects.new(name,data);bpy.context.scene.collection.objects.link(ob)
    if mat:data.materials.append(mat)
    if uv:
        layer=data.uv_layers.new(name='Original camera projection')
        for p in data.polygons:
            for li in p.loop_indices:
                v=data.vertices[data.loops[li].vertex_index].co
                layer.data[li].uv=(v.x/W+.5,v.y/H+.5)
    return ob

def polygon(name,points,z,mat):
    verts=[Vector(((u-.5)*W,(.5-v)*H,z)) for u,v in points]
    tris=tessellate_polygon([verts]);idx={tuple(v):i for i,v in enumerate(verts)}
    return mesh(name,verts,[[v if isinstance(v,int) else idx[tuple(v)] for v in tri] for tri in tris],mat)

def photo_material(name,path,alpha=False):
    m,n,l,out=material(name);uv=n.new('ShaderNodeTexCoord');tex=n.new('ShaderNodeTexImage')
    tex.image=bpy.data.images.load(str(path),check_existing=True);tex.image.pack()
    tex.interpolation='Linear';tex.extension='CLIP';l.new(uv.outputs['UV'],tex.inputs['Vector'])
    emit=n.new('ShaderNodeEmission');l.new(tex.outputs['Color'],emit.inputs['Color'])
    if alpha:
        clear=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader')
        l.new(tex.outputs['Alpha'],mix.inputs[0]);l.new(clear.outputs[0],mix.inputs[1]);l.new(emit.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0])
    else:l.new(emit.outputs[0],out.inputs[0])
    return m

def water_material(path):
    m,n,l,out=material('Stream: localized downstream moving texture refraction')
    uv=n.new('ShaderNodeTexCoord');coord=n.new('ShaderNodeVectorMath');coord.operation='MULTIPLY'
    coord.inputs[1].default_value=(85,85,1);l.new(uv.outputs['UV'],coord.inputs[0])
    drift=n.new('ShaderNodeVectorMath');drift.operation='ADD';l.new(coord.outputs[0],drift.inputs[0])
    vector=n.new('ShaderNodeCombineXYZ');driver(vector.inputs['X'],'-frame/24*0.60');driver(vector.inputs['Y'],'frame/24*2.8')
    l.new(vector.outputs[0],drift.inputs[1])
    noise=n.new('ShaderNodeTexNoise');noise.noise_dimensions='4D';noise.inputs['Scale'].default_value=1
    noise.inputs['Detail'].default_value=2.3;noise.inputs['Roughness'].default_value=.62
    driver(noise.inputs['W'],'frame/24*0.45');l.new(drift.outputs[0],noise.inputs['Vector'])
    center=n.new('ShaderNodeVectorMath');center.operation='SUBTRACT';center.inputs[1].default_value=(.5,.5,.5);l.new(noise.outputs['Color'],center.inputs[0])
    amp=n.new('ShaderNodeVectorMath');amp.operation='MULTIPLY';amp.inputs[1].default_value=(.004,.006,0);l.new(center.outputs[0],amp.inputs[0])
    warped=n.new('ShaderNodeVectorMath');warped.operation='ADD';l.new(uv.outputs['UV'],warped.inputs[0]);l.new(amp.outputs[0],warped.inputs[1])
    tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(path),check_existing=True);tex.interpolation='Linear';tex.extension='EXTEND';l.new(warped.outputs[0],tex.inputs['Vector'])
    edge=n.new('ShaderNodeVertexColor');edge.layer_name='Soft water boundary'
    emit=n.new('ShaderNodeEmission');l.new(tex.outputs['Color'],emit.inputs['Color'])
    clear=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader')
    l.new(edge.outputs['Alpha'],mix.inputs[0]);l.new(clear.outputs[0],mix.inputs[1]);l.new(emit.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0])
    return m

def water_patch(name,px,mat):
    # Outer edge remains exactly on the unwarped background. A narrow inner ring
    # feathers the animated UV perturbation; no hard rectangular effect boundary.
    points=[Vector(((x/1672-.5)*W,(.5-y/941)*H,.025)) for x,y in px]
    c=sum(points,Vector())/len(points)
    inner=[v+(c-v).normalized()*.026 for v in points]
    verts=points+inner;count=len(points);idx={tuple(v):i+count for i,v in enumerate(inner)}
    faces=[[v+count if isinstance(v,int) else idx[tuple(v)] for v in tri] for tri in tessellate_polygon([inner])]
    faces += [(i,(i+1)%count,(i+1)%count+count,i+count) for i in range(count)]
    ob=mesh(name,verts,faces,mat)
    colors=ob.data.color_attributes.new(name='Soft water boundary',type='FLOAT_COLOR',domain='POINT')
    for i,c in enumerate(colors.data):c.color=(1,1,1,float(i>=count))
    return ob

def rain_material(name,gain):
    m,n,l,out=material(name)
    uv=n.new('ShaderNodeTexCoord');sep=n.new('ShaderNodeSeparateXYZ');l.new(uv.outputs['UV'],sep.inputs[0])
    x=n.new('ShaderNodeMath');x.operation='MULTIPLY_ADD';x.inputs[1].default_value=2;x.inputs[2].default_value=-1;l.new(sep.outputs[0],x.inputs[0])
    ab=n.new('ShaderNodeMath');ab.operation='ABSOLUTE';l.new(x.outputs[0],ab.inputs[0])
    edge=n.new('ShaderNodeMath');edge.operation='SUBTRACT';edge.inputs[0].default_value=1;l.new(ab.outputs[0],edge.inputs[1])
    y=n.new('ShaderNodeMath');y.operation='MULTIPLY';y.inputs[1].default_value=math.pi;l.new(sep.outputs[1],y.inputs[0])
    sine=n.new('ShaderNodeMath');sine.operation='SINE';l.new(y.outputs[0],sine.inputs[0])
    mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';l.new(edge.outputs[0],mul.inputs[0]);l.new(sine.outputs[0],mul.inputs[1])
    alpha=n.new('ShaderNodeMath');alpha.operation='MULTIPLY';alpha.inputs[1].default_value=gain;l.new(mul.outputs[0],alpha.inputs[0])
    clear=n.new('ShaderNodeBsdfTransparent');emit=n.new('ShaderNodeEmission');emit.inputs['Color'].default_value=(.58,.69,.72,1)
    mix=n.new('ShaderNodeMixShader');l.new(alpha.outputs[0],mix.inputs[0]);l.new(clear.outputs[0],mix.inputs[1]);l.new(emit.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0])
    return m

def rain_field(name,count,z,mat,width_px,length_px,speed,extent=12.,origins=None):
    verts=[];faces=[];phases=[];freqs=[];spans=[]
    for i in range(count):
        x=R.uniform(-W*.6,W*.6);cy=0;span=extent;freq=R.uniform(*speed)/span
        if origins:
            u,v=origins[i%len(origins)];x=(u-.5)*W;span=R.uniform(.40,.92);cy=(.5-v)*H-span/2;freq=R.uniform(.65,1.3)
        phase=R.random();length=R.uniform(*length_px)/1080*H;half=R.uniform(*width_px)/1920*W/2;tilt=length*.075
        a=len(verts);verts.extend([(x-half-tilt/2,cy-length/2,z),(x+half-tilt/2,cy-length/2,z),(x+half+tilt/2,cy+length/2,z),(x-half+tilt/2,cy+length/2,z)])
        faces.append((a,a+1,a+2,a+3));phases.extend([phase]*4);freqs.extend([freq]*4);spans.extend([span]*4)
    ob=mesh(name,verts,faces,mat,False)
    uv=ob.data.uv_layers.new(name='Optical streak falloff')
    for p in ob.data.polygons:
        for li,coord in zip(p.loop_indices,[(0,0),(1,0),(1,1),(0,1)]):uv.data[li].uv=coord
    for name_,values in [('phase',phases),('frequency',freqs),('fall_extent',spans)]:
        attr=ob.data.attributes.new(name_,type='FLOAT',domain='POINT');attr.data.foreach_set('value',values)
    group=bpy.data.node_groups.new(name+' continuous recycling','GeometryNodeTree')
    group.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry');group.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
    mod=ob.modifiers.new('Independent continuous falling streaks','NODES');mod.node_group=group;n=group.nodes;l=group.links
    inp=n.new('NodeGroupInput');out=n.new('NodeGroupOutput');sp=n.new('GeometryNodeSetPosition');l.new(inp.outputs[0],sp.inputs['Geometry']);l.new(sp.outputs[0],out.inputs[0])
    def attr(name_):
        a=n.new('GeometryNodeInputNamedAttribute');a.data_type='FLOAT';a.inputs['Name'].default_value=name_;return a.outputs['Attribute']
    t=n.new('ShaderNodeValue');driver(t.outputs[0],'(frame-1)/24')
    mult=n.new('ShaderNodeMath');mult.operation='MULTIPLY';l.new(t.outputs[0],mult.inputs[0]);l.new(attr('frequency'),mult.inputs[1])
    add=n.new('ShaderNodeMath');add.operation='SUBTRACT';l.new(attr('phase'),add.inputs[0]);l.new(mult.outputs[0],add.inputs[1])
    frac=n.new('ShaderNodeMath');frac.operation='FRACT';l.new(add.outputs[0],frac.inputs[0])
    half=n.new('ShaderNodeMath');half.operation='SUBTRACT';half.inputs[1].default_value=.5;l.new(frac.outputs[0],half.inputs[0])
    stretch=n.new('ShaderNodeMath');stretch.operation='MULTIPLY';l.new(half.outputs[0],stretch.inputs[0]);l.new(attr('fall_extent'),stretch.inputs[1])
    vec=n.new('ShaderNodeCombineXYZ');l.new(stretch.outputs[0],vec.inputs['Y']);l.new(vec.outputs[0],sp.inputs['Offset'])
    ob['optical_exposure_approximation']=True;ob['independently_recycling_streaks']=count
    return ob

def main():
    bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene
    s.render.engine='CYCLES';s.cycles.samples=int(os.environ.get('SAMPLES','24'));s.cycles.use_denoising=False;s.cycles.max_bounces=1;s.cycles.transparent_max_bounces=24
    s.cycles.use_adaptive_sampling=False;s.render.threads_mode='FIXED';s.render.threads=4
    s.render.resolution_x=int(os.environ.get('WIDTH','1920'));s.render.resolution_y=round(s.render.resolution_x*9/16);s.render.resolution_percentage=100
    s.render.fps=24;s.frame_start=1;s.frame_end=144;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
    s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
    s.world=bpy.data.worlds.new('Black unlit composite world');s.world.use_nodes=True;s.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=0
    cam=bpy.data.cameras.new('Locked photographic plate camera');ob=bpy.data.objects.new('Locked photographic plate camera',cam);s.collection.objects.link(ob);ob.location=(0,0,10);cam.type='ORTHO';cam.ortho_scale=W;s.camera=ob
    path=ROOT/'assets/hybrid_motion/clean_background.png'
    bg=photo_material('Generated clean background — static architecture and forest',path)
    polygon('Static photographic-style background',[(0,0),(1,0),(1,1),(0,1)],0,bg)
    water=water_material(path)
    water_polygons=[
      [(679,619),(699,611),(727,622),(728,631),(709,640),(694,635)],
      [(721,638),(747,633),(774,642),(775,652),(752,655),(730,650)],
      [(888,749),(913,753),(929,758),(955,768),(956,784),(940,793),(923,785),(907,772),(891,765)],
      [(953,780),(979,779),(996,791),(1017,795),(1030,810),(1024,824),(997,820),(982,806),(961,802)],
      [(995,823),(1027,821),(1051,825),(1075,838),(1116,847),(1121,862),(1105,873),(1068,857),(1041,850),(1009,844)],
      [(1069,879),(1110,874),(1141,889),(1180,898),(1221,910),(1247,926),(1280,942),(1122,947),(1086,929),(1042,912)],
      [(1180,879),(1209,874),(1228,883),(1258,890),(1281,907),(1303,922),(1301,941),(1274,942),(1245,921),(1222,909),(1194,900)]
    ]
    for i,poly in enumerate(water_polygons):water_patch('Localized creek flow patch '+str(i+1),poly,water)
    # Native rain at two depths; generated architecture is replicated as exact
    # image patches between the fields to provide explicit screen-space occlusion.
    rain_field('Fine rain behind cabin',6000,1,rain_material('Soft fine rain',.21),(.30,.65),(7,18),(4,7))
    cabin=[(.442,.402),(.633,.165),(.667,.157),(.868,.429),(.857,.674),(.836,.737),(.475,.742)]
    polygon('Cabin rain occlusion — matched photographic projection',cabin,2,bg)
    rain_field('Near rain in front of cabin',750,3,rain_material('Sparse foreground rain',.23),(.55,1.10),(18,33),(7,10))
    # Sheltered roof, wall and porch posts occlude both depths of rain.
    porch=[[(0,0),(.485,0),(.447,.281),(.268,.239),(.229,.195),(.096,.14),(0,.13)],
      [(0,0),(.094,0),(.101,.15),(.148,.224),(.145,.87),(0,.96)],
      [(.217,.173),(.250,.203),(.244,.966),(.210,.973)],
      [(.266,.239),(.295,.269),(.292,.891),(.266,.913)],
      [(0,.93),(.290,.860),(.290,.912),(.230,1),(0,1)]]
    for i,poly in enumerate(porch):polygon('Dry shelter rain blocker '+str(i+1),poly,4.5,bg)
    palms=photo_material('Generated foreground wet palms — actual transparent layer',ROOT/'assets/hybrid_motion/foreground_palms.png',True)
    nx,ny=100,100;verts=[];faces=[]
    for j in range(ny+1):
        v=j/ny
        for i in range(nx+1):
            u=.54+.46*i/nx;verts.append(((u-.5)*W,(v-.5)*H,4))
    for j in range(ny):
        for i in range(nx):
            a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
    leaf=mesh('Flexible foreground palms — anchored top and right',verts,faces,palms)
    leaf.shape_key_add(name='Basis')
    for keyname,phase in [('Slow flexible breeze',0),('Small secondary gust',1)]:
        key=leaf.shape_key_add(name=keyname);key.slider_min=-1
        for i,vertex in enumerate(key.data):
            u=verts[i][0]/W+.5;v=verts[i][1]/H+.5
            weight=min(1,max(0,(1-u)/.30))**1.4*min(1,max(0,(1-v)/.12))**.8
            a=.004 if phase==0 else .0012
            vertex.co.x+=W*a*weight*(.8+.2*math.sin(v*9+phase))
            vertex.co.y+=H*a*1.1*weight*math.cos(v*4+phase)
        d=key.driver_add('value').driver;d.expression='sin(2*pi*(frame-1)/144)' if phase==0 else 'sin(4*pi*(frame-1)/144+0.55)'
    leaf['anchored_borders']='top and right';leaf['maximum_main_displacement_pixels']=8.5
    eaves=[(.30+i*.0105,.244+i*.0017) for i in range(13)]
    eaves += [(.467+i*.0135,.424+math.sin(i*.15)*.006) for i in range(29)]
    rain_field('Roof runoff falling beads',len(eaves),3.5,rain_material('Intermittent eave runoff',.43),(.5,1.0),(3,7),(1,2),origins=eaves)
    # Small expanding impact rings are placed only inside clearly visible pools.
    splashmat,n,l,out=material('Soft short-lived stream impacts')
    clear=n.new('ShaderNodeBsdfTransparent');emit=n.new('ShaderNodeEmission');emit.inputs['Color'].default_value=(.34,.43,.44,1)
    mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=.18;l.new(clear.outputs[0],mix.inputs[1]);l.new(emit.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0])
    for i in range(36):
        u=R.uniform(.655,.715);v=R.uniform(.936,.986);x=(u-.5)*W;y=(.5-v)*H
        vs=[];fs=[];segs=20
        for j in range(segs):
            theta=2*math.pi*j/segs
            for radius in [.013,.015]:vs.append((radius*math.cos(theta),radius*.34*math.sin(theta),0))
        for j in range(segs):fs.append((j*2,((j+1)%segs)*2,((j+1)%segs)*2+1,j*2+1))
        ob=mesh('Short stream impact %02d'%i,vs,fs,splashmat,False);ob.location=(x,y,.06)
        phase=R.random();period=R.uniform(.55,1.0)
        for axis in [0,1]:ob.driver_add('scale',axis).driver.expression=f'0.08+1.25*((((frame-1)/24+{phase})%{period})/{period})'
        # Fade each ring through a private material, so it cannot pop at full size.
        private=splashmat.copy();ob.data.materials[0]=private
        factor=next(a for a in private.node_tree.nodes if a.bl_idname=='ShaderNodeMixShader').inputs[0]
        driver(factor,f'0.19*sin(pi*((((frame-1)/24+{phase})%{period})/{period}))**2')
    s['render_method']='Generated layered matte, camera-plane deforming palms, masked animated water UV, native 3D optical rain and runoff'
    s['generated_images_not_photographs']=True;s['camera_locked']=True;s['fully_modeled_scene']=False;s['seamless_loop']=False
    s['static_elements']='Cabin, distant forest, rocks and most understory; source textures contain some residual static water highlights'
    text=bpy.data.texts.new('METHOD_AND_LIMITS');text.write(s['render_method']+'\n'+s['static_elements']+'\n6-second silent motion diagnostic, not a final long ambience video.\n')
    s.render.filepath='//renders/hybrid_motion/still.png';s.frame_set(1)
    for im in bpy.data.images:
        if im.source=='FILE' and im.filepath:im.filepath=bpy.path.relpath(im.filepath,start=str(ROOT))
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'rainforest_hybrid_motion.blend'),compress=True)
    report={'method':s['render_method'],'generated_layers':True,'fully_modeled_scene':False,'camera_locked':True,'resolution':[s.render.resolution_x,s.render.resolution_y],'fps':24,'frames':144,'duration_seconds':6,'samples':s.cycles.samples,'rain_streaks':6750,'runoff_beads':42,'water_patches':len(water_polygons),'impact_rings':36,'foliage_grid_vertices':len(verts),'static_elements':s['static_elements'],'seamless_loop':False,'audio':False}
    (ROOT/'research/hybrid_motion/setup.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2),flush=True)
    if os.environ.get('DIAGNOSTIC'):
        s.render.resolution_x=960;s.render.resolution_y=540;s.cycles.samples=8
        s.frame_set(int(os.environ.get('TEST_FRAME','24')));s.render.filepath=str(ROOT/'renders/hybrid_motion/diagnostic.png');bpy.ops.render.render(write_still=True)
    print('HYBRID MOTION SETUP COMPLETE',flush=True)

try:main()
except BaseException:traceback.print_exc();os._exit(1)
os._exit(0)
