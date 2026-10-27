"""Normalize individual CC0 specimens into packed, reusable libraries."""
import bpy, json, os, re
from pathlib import Path
from mathutils import Vector, Matrix

ROOT=Path(__file__).resolve().parents[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
records=[]
names=['fern_02','calathea_orbifolia_01','anthurium_botany_01',
       'pachira_aquatica_01','rock_moss_set_01','shrub_04','island_tree_02']
for name in names:
    before=set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=str(ROOT/'assets'/name/(name+'.gltf')))
    obs=[o for o in bpy.data.objects if o not in before and o.type=='MESH']
    bpy.context.view_layer.update()
    groups={}
    for index,o in enumerate(obs):
        suffix=o.name.rsplit('_',1)[-1].split('.')[0]
        if len(suffix)!=1 or not suffix.isalpha(): suffix='all'
        if name=='rock_moss_set_01':suffix='specimen_'+str(index)
        groups.setdefault(suffix,[]).append(o)
    collections=[]
    for suffix,objects in groups.items():
        pts=[o.matrix_world@v.co for o in objects for v in o.data.vertices]
        lo=Vector([min(p[i] for p in pts) for i in range(3)])
        hi=Vector([max(p[i] for p in pts) for i in range(3)])
        height=hi.z-lo.z
        if height<.001: continue
        c=bpy.data.collections.new(name+'_'+suffix)
        norm=Matrix.Scale(1/height,4)@Matrix.Translation(Vector((-(lo.x+hi.x)/2,-(lo.y+hi.y)/2,-lo.z)))
        for ob in objects:
            world=ob.matrix_world.copy();ob.parent=None;ob.matrix_world=norm@world
            for old in list(ob.users_collection):old.objects.unlink(ob)
            c.objects.link(ob)
        collections.append(c)
        records.append({'asset':name,'collection':c.name,'height_normalized':1,
                        'source_dimensions':list(hi-lo),'triangles':sum(len(o.data.polygons) for o in objects)})
    for ob in obs:
        for poly in ob.data.polygons:poly.use_smooth=True
    for mat in {m for o in obs for m in o.data.materials if m}:
        if not mat.use_nodes:continue
        n=mat.node_tree.nodes;l=mat.node_tree.links;p=next((v for v in n if v.type=='BSDF_PRINCIPLED'),None)
        if p is None:continue
        # The provider glTF uses JPEG colour maps: their alpha channel is always 1.
        # Alpha mode MASK alone cannot cut leaf cards. Load the separate scan mask.
        maps=ROOT/'assets'/name/'hero_maps'
        leafy=(maps/'Alpha.png').exists() or ('leaves' in mat.name.lower() and (maps/'leaves_alpha.png').exists())
        if leafy:
            alpha_path=maps/('Alpha.png' if (maps/'Alpha.png').exists() else 'leaves_alpha.png')
            alpha=n.new('ShaderNodeTexImage');alpha.name='Verified photographic leaf silhouette';alpha.image=bpy.data.images.load(str(alpha_path),check_existing=True);alpha.image.colorspace_settings.name='Non-Color';alpha.interpolation='Linear'
            l.new(alpha.outputs['Color'],p.inputs['Alpha'])
            for kind,socket in [('Diffuse','Base Color'),('Rough','Roughness'),('nor_gl','Normal')]:
                path=maps/(kind+'.jpg')
                if not path.exists():continue
                tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(path),check_existing=True)
                if kind!='Diffuse':tex.image.colorspace_settings.name='Non-Color'
                if kind=='nor_gl':
                    normal=n.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=.55;l.new(tex.outputs[0],normal.inputs['Color']);l.new(normal.outputs[0],p.inputs[socket])
                else:l.new(tex.outputs[0],p.inputs[socket])
        if p.inputs['Roughness'].is_linked:
            source=p.inputs['Roughness'].links[0].from_socket
            math=n.new('ShaderNodeMath');math.operation='MULTIPLY_ADD';math.inputs[1].default_value=.48;math.inputs[2].default_value=.20 if leafy else .1
            l.new(source,math.inputs[0]);l.new(math.outputs[0],p.inputs['Roughness'])
        p.inputs['Coat Weight'].default_value=.10 if leafy else .12;p.inputs['Coat Roughness'].default_value=.18 if leafy else .24
        if leafy:
            p.inputs['Subsurface Weight'].default_value=.035;p.inputs['Subsurface Radius'].default_value=(.035,.08,.02)
            if p.inputs['Base Color'].is_linked:
                source=p.inputs['Base Color'].links[0].from_socket
                tint=n.new('ShaderNodeMixRGB');tint.blend_type='MULTIPLY';tint.inputs[0].default_value=1;tint.inputs[2].default_value=(.58,.68,.42,1)
                l.new(source,tint.inputs[1]);l.new(tint.outputs[0],p.inputs['Base Color'])
        for node in n:
            if node.type=='NORMAL_MAP':node.inputs['Strength'].default_value=.65
    for image in bpy.data.images:
        if image.source=='FILE' and not image.packed_file:image.pack()
    dest=ROOT/'assets'/(name+'.blend')
    bpy.data.libraries.write(str(dest),set(collections),compress=True)
    print('LIBRARY READY',name,[(c.name,len(c.objects)) for c in collections],dest.stat().st_size,flush=True)
(ROOT/'assets'/'library.json').write_text(json.dumps(records,indent=2))
print('ALL LIBRARIES COMPLETE',flush=True)
os._exit(0)
