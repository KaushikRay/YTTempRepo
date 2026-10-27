"""Replace weak river UV wobble with masked, projected real CC0 water footage.

This is a locked-camera footage composite, not a fluid simulation. Only selected
water pixels are replaced. The approved palm meshes and their animation are not
edited. Water masks use original plate pixels, 1672 x 941, top-left origin.
"""
import bpy,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.geometry import tessellate_polygon

# Traced around the wetted channel; separate footprints leave all large rocks
# exposed. Source crop coordinates use the actual 1920 x 1080 footage frame.
PATCHES=[
 ('Distant riffle',[(649,615),(673,610),(697,616),(708,627),(694,636),(674,630),(660,628)],(1050,375,520,230),.42,0),
 ('Upper creek',[(700,635),(727,635),(750,644),(774,648),(785,660),(759,661),(737,654),(715,649)],(1090,400,490,240),.44,8),
 ('Upper pool',[(895,736),(916,736),(937,745),(970,747),(983,753),(963,762),(943,756),(925,755),(910,749)],(1120,390,470,210),.40,16),
 ('First falling sheets',[(925,751),(945,751),(956,761),(974,758),(984,765),(994,765),(1007,774),(1022,773),(1028,785),(1020,796),(999,800),(978,790),(953,792),(933,783)],(1050,390,600,370),.75,4),
 ('Second falling sheets',[(1025,774),(1042,776),(1058,782),(1073,779),(1088,786),(1094,800),(1107,802),(1119,815),(1116,826),(1097,834),(1075,826),(1056,821),(1040,820),(1027,808),(1014,806),(1017,793)],(1040,395,610,390),.66,20),
 ('Cascade landing pool',[(926,793),(951,798),(980,802),(1008,808),(1037,819),(1063,826),(1097,833),(1103,845),(1089,855),(1062,851),(1035,843),(1016,839),(985,837),(961,840),(947,831),(922,829),(916,816)],(1120,520,500,390),.46,11),
 ('Pool beside large right rock',[(1095,838),(1120,837),(1142,845),(1155,851),(1163,861),(1181,865),(1199,872),(1216,876),(1227,885),(1218,898),(1199,895),(1180,885),(1159,883),(1141,876),(1122,871),(1100,861),(1081,857)],(1150,400,550,260),.32,25),
 ('Foreground left bend',[(938,840),(961,843),(989,842),(1015,848),(1044,854),(1067,861),(1086,873),(1081,884),(1067,895),(1047,900),(1024,891),(1002,880),(979,873),(957,866),(947,854)],(1100,385,590,290),.32,15),
 ('Foreground middle current',[(1083,877),(1106,875),(1131,881),(1155,889),(1176,897),(1204,901),(1217,912),(1242,921),(1254,941),(1110,941),(1091,930),(1073,919),(1056,909),(1071,895)],(1010,375,620,270),.33,32),
 ('Foreground right current',[(1213,882),(1234,887),(1254,896),(1280,898),(1300,907),(1330,918),(1356,924),(1380,934),(1390,941),(1253,941),(1247,929),(1226,917),(1204,911),(1189,902),(1199,892)],(1050,380,620,290),.32,23),
]

def _mat(root,label,crop,gain,offset):
    mat=bpy.data.materials.new('Real flowing river / '+label);mat.use_nodes=True
    n=mat.node_tree.nodes;l=mat.node_tree.links;n.clear();out=n.new('ShaderNodeOutputMaterial')
    uv=n.new('ShaderNodeTexCoord');uv.name='Mapped water-only source crop'
    tex=n.new('ShaderNodeTexImage');tex.name='CC0 Cbaile19 real rapids — no synthetic pixel motion'
    image=bpy.data.images.get('real_rapids.mp4')
    if image is None:image=bpy.data.images.load(str(root/'assets/river_flow/real_rapids.mp4'))
    image.source='MOVIE';tex.image=image;tex.extension='EXTEND';tex.interpolation='Linear'
    tex.image_user.frame_duration=192;tex.image_user.frame_start=1;tex.image_user.frame_offset=offset;tex.image_user.use_auto_refresh=True;tex.image_user.use_cyclic=False
    l.new(uv.outputs['UV'],tex.inputs['Vector'])
    projection=n.new('ShaderNodeUVMap');projection.uv_map='Original camera projection'
    photo=n.new('ShaderNodeTexImage');photo.image=bpy.data.images.get('clean_background.png');l.new(projection.outputs[0],photo.inputs['Vector'])
    falls='falling' in label.lower() or 'landing' in label.lower()
    vx,vy=(9,38) if falls else (42,18)
    period=1.2
    phases=[];samples=[]
    for j in range(2):
        phase=n.new('ShaderNodeValue');phase.name='Downstream travel phase '+str(j)
        phase.outputs[0].driver_add('default_value').driver.expression=f'(((frame-1)/24/{period}+{j*.5+offset/192})%1)'
        centered=n.new('ShaderNodeMath');centered.operation='SUBTRACT';centered.inputs[1].default_value=.5;l.new(phase.outputs[0],centered.inputs[0])
        dx=n.new('ShaderNodeMath');dx.operation='MULTIPLY';dx.inputs[1].default_value=-vx*period/1672;l.new(centered.outputs[0],dx.inputs[0])
        dy=n.new('ShaderNodeMath');dy.operation='MULTIPLY';dy.inputs[1].default_value=vy*period/941;l.new(centered.outputs[0],dy.inputs[0])
        vector=n.new('ShaderNodeCombineXYZ');l.new(dx.outputs[0],vector.inputs['X']);l.new(dy.outputs[0],vector.inputs['Y'])
        add=n.new('ShaderNodeVectorMath');add.operation='ADD';l.new(projection.outputs[0],add.inputs[0]);l.new(vector.outputs[0],add.inputs[1])
        moving=n.new('ShaderNodeTexImage');moving.image=photo.image;moving.extension='EXTEND';l.new(add.outputs[0],moving.inputs['Vector'])
        phases.append(phase);samples.append(moving)
    angle=n.new('ShaderNodeMath');angle.operation='MULTIPLY';angle.inputs[1].default_value=math.pi;l.new(phases[0].outputs[0],angle.inputs[0])
    sine=n.new('ShaderNodeMath');sine.operation='SINE';l.new(angle.outputs[0],sine.inputs[0])
    weight=n.new('ShaderNodeMath');weight.operation='MULTIPLY';l.new(sine.outputs[0],weight.inputs[0]);l.new(sine.outputs[0],weight.inputs[1])
    transport=n.new('ShaderNodeMixRGB');l.new(weight.outputs[0],transport.inputs[0]);l.new(samples[1].outputs[0],transport.inputs[1]);l.new(samples[0].outputs[0],transport.inputs[2])
    actual=n.new('ShaderNodeRGBToBW');l.new(tex.outputs['Color'],actual.inputs[0])
    turbulence=n.new('ShaderNodeMath');turbulence.operation='MULTIPLY_ADD';turbulence.inputs[1].default_value=2.1;turbulence.inputs[2].default_value=.46;l.new(actual.outputs[0],turbulence.inputs[0])
    modulated=n.new('ShaderNodeMixRGB');modulated.blend_type='MULTIPLY';modulated.inputs[0].default_value=1;l.new(transport.outputs[0],modulated.inputs[1]);l.new(turbulence.outputs[0],modulated.inputs[2])
    emit=n.new('ShaderNodeEmission');l.new(modulated.outputs[0],emit.inputs['Color'])
    edge=n.new('ShaderNodeVertexColor');edge.layer_name='Soft river bank'
    static_luma=n.new('ShaderNodeRGBToBW');l.new(photo.outputs[0],static_luma.inputs[0])
    watermask=n.new('ShaderNodeMapRange');watermask.clamp=True;watermask.interpolation_type='SMOOTHSTEP';watermask.inputs['From Min'].default_value=.022 if falls else .006;watermask.inputs['From Max'].default_value=.19 if falls else .055;l.new(static_luma.outputs[0],watermask.inputs['Value'])
    alpha=n.new('ShaderNodeMath');alpha.operation='MULTIPLY';l.new(watermask.outputs[0],alpha.inputs[0]);l.new(edge.outputs['Alpha'],alpha.inputs[1])
    clear=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');l.new(alpha.outputs[0],mix.inputs[0]);l.new(clear.outputs[0],mix.inputs[1]);l.new(emit.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0])
    return mat

def _patch(root,label,px,crop,gain,offset):
    mat=_mat(root,label,crop,gain,offset)
    outer=[Vector(((x/1672-.5)*16,(.5-y/941)*9,.028)) for x,y in px]
    c=sum(outer,Vector())/len(outer);inner=[v+(c-v).normalized()*.065 for v in outer]
    count=len(outer);verts=outer+inner
    faces=[tuple(i+count for i in tri) for tri in tessellate_polygon([inner])]
    faces += [(i,(i+1)%count,(i+1)%count+count,i+count) for i in range(count)]
    data=bpy.data.meshes.new('River footprint / '+label);data.from_pydata(verts,[],faces);data.update();data.materials.append(mat)
    ob=bpy.data.objects.new('Real flowing creek / '+label,data);bpy.context.scene.collection.objects.link(ob)
    source_uv=data.uv_layers.new(name='Real footage water crop');projection=data.uv_layers.new(name='Original camera projection')
    xmin,xmax=min(x for x,y in px),max(x for x,y in px);ymin,ymax=min(y for x,y in px),max(y for x,y in px)
    cx,cy,cw,ch=crop
    for p in data.polygons:
        for li in p.loop_indices:
            v=data.vertices[data.loops[li].vertex_index].co;u=v.x/16+.5;vv=v.y/9+.5
            x=u*1672;y=(1-vv)*941
            # Horizontal mirror turns the source's down-left current down-right.
            su=1-(x-xmin)/(xmax-xmin);sv=(y-ymin)/(ymax-ymin)
            source_uv.data[li].uv=((cx+su*cw)/1920,1-(cy+sv*ch)/1080)
            projection.data[li].uv=(u,vv)
    data.uv_layers.active_index=0
    color=data.color_attributes.new(name='Soft river bank',type='FLOAT_COLOR',domain='POINT')
    for i,v in enumerate(color.data):v.color=(1,1,1,float(i>=count))
    ob['source_licence']='CC0 1.0';ob['source_frame_offset']=offset;ob['screen_pixel_bounds']=[xmin,ymin,xmax,ymax]
    return ob

def install_river(root):
    root=Path(root)
    assert (root/'assets/river_flow/real_rapids.mp4').is_file()
    removed=[]
    for ob in list(bpy.data.objects):
        if ob.name.startswith(('Localized creek flow patch ','Real flowing creek / ','Short stream impact ')):
            removed.append(ob.name);bpy.data.objects.remove(ob,do_unlink=True)
    for patch in PATCHES:_patch(root,*patch)
    s=bpy.context.scene
    s['render_method']='Generated static forest/cabin, approved deforming palms, projected real CC0 rapids footage, native optical rain/runoff'
    s['static_elements']='Cabin, distant forest, rocks and most understory. River edges outside the traced masks retain some source reflections.'
    s['river_method']='Directional photographic water advection at 38 px/s falls and 42 px/s pools, modulated by real CC0 whitewater footage through feathered/luminance masks'
    txt=bpy.data.texts.get('METHOD_AND_LIMITS');txt.clear();txt.write(s['render_method']+'\n'+s['river_method']+'\nLocked camera; projected footage, not a fluid simulation. Silent 6 s test; not a seamless loop.\n')
    for image in bpy.data.images:
        if image.source=='MOVIE':image.filepath='//assets/river_flow/real_rapids.mp4'
    report={'method':s['river_method'],'source':'assets/river_flow/source.json','patches':[{'name':p[0],'outline_source_pixels':p[1],'footage_crop':p[2],'gain':p[3],'frame_offset':p[4]} for p in PATCHES],
            'old_wobble_removed':True,'synthetic_impact_rings_removed':True,'approved_palm_animation_edited':False,'fully_modeled_water':False,'external_movie_relative':True,'mask_feather_source_pixels':6.8,'directional_advection_pixels_per_second':{'falls':[9,38],'pools':[42,18]},'real_footage_role':'Dynamic turbulence modulation of transported photographic water colour'}
    (root/'research/river_flow/setup.json').write_text(json.dumps(report,indent=2));return report
