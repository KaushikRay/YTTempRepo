"""Softer practical lighting, natural exterior vegetation and village depth."""
print('LIGHTING/EXTERIOR PASS START',flush=True)
library=r/'assets/exterior/vegetation.blend'
with bpy.data.libraries.load(str(library),link=True) as (source,target):
    target.collections=['Exterior Fir C','Exterior Shrub 02']
collections={collection.name:collection for collection in target.collections}
def plant_instance(name,collection,location,height,angle):
    ob=bpy.data.objects.new(name,None);bpy.context.collection.objects.link(ob);ob.instance_type='COLLECTION';ob.instance_collection=collections[collection];ob.location=location;ob.scale=(height,)*3;ob.rotation_euler.z=math.radians(angle);return ob
plant_instance('Landscape foreground fir','Exterior Fir C',(-4.2,13.6,1.25),9.2,-22)
plant_instance('Landscape distant fir','Exterior Fir C',(2.65,20,1.25),10.5,73)
plant_instance('Landscape wet undergrowth','Exterior Shrub 02',(-1.2,12.9,1.12),1.05,12)
# A wet rising apron joins the room-level ground to the existing village slope.
wet=bpy.data.materials['Scanned monastery flags'].copy();wet.name='Landscape wet stone apron'
nodes=wet.node_tree.nodes;links=wet.node_tree.links;p=nodes.get('Principled BSDF');source=p.inputs['Base Color'].links[0].from_socket
darken=nodes.new('ShaderNodeMixRGB');darken.blend_type='MULTIPLY';darken.inputs[0].default_value=1;darken.inputs[2].default_value=(.25,.3,.29,1);links.new(source,darken.inputs[1]);links.new(darken.outputs[0],p.inputs['Base Color'])
for link in list(p.inputs['Roughness'].links):links.remove(link)
p.inputs['Roughness'].default_value=.24
verts=[];faces=[]
for j in range(13):
    y=9.1+j*.4;z=.03+1.22*min(1,max(0,(y-9.1)/4.4))
    for i in range(17):verts.append((-8+i,y,z))
for j in range(12):
    for i in range(16):
        k=j*17+i;faces.append((k,k+1,k+18,k+17))
me=bpy.data.meshes.new('Landscape sloped wet apron');me.from_pydata(verts,[],faces);me.materials.append(wet);uv=me.uv_layers.new()
for lp in me.loops:
    v=me.vertices[lp.vertex_index].co;uv.data[lp.index].uv=(v.x,v.y)
ob=bpy.data.objects.new('Landscape sloped wet apron',me);bpy.context.collection.objects.link(ob)

# Light is tied to the visible sources and their bounce, with less uniformly
# orange stonework. Keep warm practicals, broad reflected light and a cool sky.
fire.data.energy=255;fire.data.color=(1,.62,.34);fire.data.shadow_soft_size=.46
bounce=bpy.data.objects.get('Historic reflected hearth bounce')
if bounce:bounce.data.energy=58;bounce.data.color=(1,.72,.51);bounce.data.size=3.2
for ob in bpy.data.objects:
    if ob.name.startswith('Window blue fill'):
        ob.data.energy=110;ob.data.color=(.62,.71,.8);ob.data.shape='RECTANGLE';ob.data.size=1.7;ob.data.size_y=4.8
    if ob.name=='Soft cool room bounce':ob.data.energy=18
    if ob.name=='Exterior moonlit rain':ob.data.energy=2200;ob.data.color=(.58,.68,.78)
    if ob.name.startswith('Candle glow') and ob.location.z>3:
        ob.data.energy*=.65
# Broad, weak reflected window light across the floor and leather, rather than
# a second point source washing the entire wall.
data=bpy.data.lights.new('Reflected window on seating','AREA');data.energy=34;data.color=(.65,.72,.78);data.shape='DISK';data.size=4
ob=bpy.data.objects.new('Reflected window on seating',data);bpy.context.collection.objects.link(ob);ob.location=(-.8,5.6,3.8);ob.rotation_euler=(Vector((-1.7,-1.2,.75))-ob.location).to_track_quat('-Z','Y').to_euler()
s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=.48

# Hearth soot fades into the upper brick courses; no flat bright orange box.
for material in bpy.data.materials:
    if material.name.startswith('Historic fired brick'):
        n=material.node_tree.nodes;l=material.node_tree.links;p=n.get('Principled BSDF');old=p.inputs['Base Color'].links[0].from_socket
        geo=n.new('ShaderNodeNewGeometry');sep=n.new('ShaderNodeSeparateXYZ');l.new(geo.outputs['Position'],sep.inputs[0]);fade=n.new('ShaderNodeMapRange');fade.inputs['From Min'].default_value=.3;fade.inputs['From Max'].default_value=2.8;fade.inputs['To Min'].default_value=.8;fade.inputs['To Max'].default_value=.22;l.new(sep.outputs['Z'],fade.inputs[0])
        mult=n.new('ShaderNodeMixRGB');mult.blend_type='MULTIPLY';mult.inputs[0].default_value=1;l.new(old,mult.inputs[1]);l.new(fade.outputs[0],mult.inputs[2]);l.new(mult.outputs[0],p.inputs['Base Color'])

# Village windows should be a few recesses, not repeated self-lit squares.
for ob in bpy.data.objects:
    if ob.name.startswith('Village lamplit'):
        p=ob.data.materials[0].node_tree.nodes.get('Principled BSDF')
        if p:p.inputs['Emission Strength'].default_value=.28
    if ob.name.startswith('Distant village cottage'):
        ob.data.materials.clear();ob.data.materials.append(bpy.data.materials['Historic lime-pointed masonry'])
# Strengthen the sense of layered distance while retaining a glimpse of roofs.
mist=bpy.data.materials['Storm exterior mist']
for node in mist.node_tree.nodes:
    if node.type=='PRINCIPLED_VOLUME':node.inputs['Density'].default_value=.023

# The water distortion was too uniform. Restrict the strongest deformation to
# irregular rivulet regions, leaving glimpses of the trees and village behind.
glass=bpy.data.materials['Cold rain-streaked glass']
for node in glass.node_tree.nodes:
    if node.type=='BUMP' and abs(node.inputs['Distance'].default_value-.018)<.0001:
        node.inputs['Distance'].default_value=.007;node.inputs['Strength'].default_value=.22

# Keep linked libraries portable; used materials/textures live in the library.
for lib in bpy.data.libraries:
    path=Path(bpy.path.abspath(lib.filepath))
    if path==library:lib.filepath='//assets/exterior/vegetation.blend'
(r/'renders/lighting_exterior_build.json').write_text(json.dumps({'tree_instances':2,'shrub_groups':1,'source_library':'assets/exterior/vegetation.blend','source_licence':'CC0','leaf_atlas_variants':3,'lighting':'Warm practicals and broad, restrained window/hearth bounce','animated':False},indent=2))
print('LIGHTING/EXTERIOR PASS COMPLETE',flush=True)
