"""Pack individual high-detail CC0 ground scans and practical cabin props."""
import bpy,json,os
from pathlib import Path
from mathutils import Vector,Matrix
root=Path(__file__).resolve().parents[1];folder=root/'assets/realism'
bpy.ops.wm.read_factory_settings(use_empty=True);records=[]
for name in ['root_cluster_01','moss_01','bark_debris_01','wooden_bucket_01','wooden_lantern_01']:
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(folder/name/(name+'.gltf')))
    obs=[o for o in bpy.data.objects if o not in before and o.type=='MESH'];bpy.context.view_layer.update()
    groups=[[o] for o in obs] if name in ['moss_01','bark_debris_01'] else [obs];collections=[]
    for idx,group in enumerate(groups):
        pts=[o.matrix_world@v.co for o in group for v in o.data.vertices]
        lo=Vector([min(p[i] for p in pts) for i in range(3)]);hi=Vector([max(p[i] for p in pts) for i in range(3)])
        mode='height' if name.startswith('wooden_') else 'width';size=hi.z-lo.z if mode=='height' else max(hi.x-lo.x,hi.y-lo.y)
        c=bpy.data.collections.new(name+' specimen '+str(idx));normal=Matrix.Scale(1/size,4)@Matrix.Translation(Vector((-(lo.x+hi.x)/2,-(lo.y+hi.y)/2,-lo.z)))
        for ob in group:
            world=ob.matrix_world.copy();ob.parent=None;ob.matrix_world=normal@world
            for old in list(ob.users_collection):old.objects.unlink(ob)
            c.objects.link(ob)
            for poly in ob.data.polygons:poly.use_smooth=True
        collections.append(c);records.append({'asset':name,'collection':c.name,'normalized_dimension':mode,'source_dimensions':list(hi-lo)})
    for mat in {m for ob in obs for m in ob.data.materials if m}:
        if not mat.use_nodes:continue
        n=mat.node_tree.nodes;l=mat.node_tree.links;p=next((x for x in n if x.type=='BSDF_PRINCIPLED'),None)
        if not p:continue
        alpha=folder/name/'Alpha.png'
        if alpha.exists():
            tex=n.new('ShaderNodeTexImage');tex.name='Verified scan silhouette';tex.image=bpy.data.images.load(str(alpha),check_existing=True);tex.image.colorspace_settings.name='Non-Color';l.new(tex.outputs[0],p.inputs['Alpha'])
        p.inputs['Coat Weight'].default_value=.04;p.inputs['Coat Roughness'].default_value=.27
        if 'glass' in mat.name:
            p.inputs['Transmission Weight'].default_value=.96;p.inputs['IOR'].default_value=1.46;p.inputs['Roughness'].default_value=.14
    for image in bpy.data.images:
        if image.source=='FILE' and not image.packed_file:image.pack()
    dest=folder/(name+'.blend');bpy.data.libraries.write(str(dest),set(collections),compress=True)
    print('REALISM LIBRARY READY',name,'collections',len(collections),'bytes',dest.stat().st_size,flush=True)
(folder/'library.json').write_text(json.dumps(records,indent=2));print('REALISM LIBRARIES COMPLETE',flush=True);os._exit(0)
