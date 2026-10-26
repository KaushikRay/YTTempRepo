"""Create a compact linked CC0 vegetation library, with packed PBR textures."""
import bpy,json,os
from pathlib import Path
from mathutils import Vector,Matrix

root=Path(__file__).resolve().parents[1];folder=root/'assets/dressing'
bpy.ops.wm.read_factory_settings(use_empty=True)
records=[]
for name,path in [(n,folder/n/(n+'.gltf')) for n in ['metal_jug','wooden_bowl_02','dry_branches_medium_01','food_apple_01','carved_wooden_plate']]:
    before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(path));objects=[o for o in bpy.data.objects if o not in before];bpy.context.view_layer.update()
    points=[o.matrix_world@Vector(v) for o in objects if o.type=='MESH' for v in o.bound_box]
    low=Vector(tuple(min(p[i] for p in points) for i in range(3)));high=Vector(tuple(max(p[i] for p in points) for i in range(3)))
    anchor=Vector(((low.x+high.x)/2,(low.y+high.y)/2,low.z));factor=1/(high.z-low.z)
    collection=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(collection)
    parent=bpy.data.objects.new(name+' normalized root',None);collection.objects.link(parent)
    for ob in objects:
        for old in list(ob.users_collection):old.objects.unlink(ob)
        collection.objects.link(ob)
        if ob.parent not in objects:ob.parent=parent
    parent.matrix_world=Matrix.Scale(factor,4)@Matrix.Translation(-anchor)
    records.append({'collection':name,'source_dimensions_m':list(high-low),'normalized_height':1,'source':str(path.relative_to(root))})
    print('LIBRARY COLLECTION READY',name,'source dimensions',list(high-low),flush=True)
for material in bpy.data.materials:
    if material.name.startswith('dry_branches') and material.use_nodes:
        n=material.node_tree.nodes;l=material.node_tree.links;p=n.get('Principled BSDF')
        if p and p.inputs['Base Color'].is_linked:
            old=p.inputs['Base Color'].links[0].from_socket;mul=n.new('ShaderNodeMixRGB');mul.blend_type='MULTIPLY';mul.inputs[0].default_value=1;mul.inputs[2].default_value=(.055,.04,.028,1);l.new(old,mul.inputs[1]);l.new(mul.outputs[0],p.inputs['Base Color']);p.inputs['Roughness'].default_value=.93
bpy.data.orphans_purge(do_recursive=True)
for image in bpy.data.images:
    if image.source=='FILE' and not image.packed_file:image.pack()
credits=bpy.data.texts.new('DRESSING_CREDITS.txt');credits.write((folder/'CREDITS.txt').read_text())
bpy.ops.wm.save_as_mainfile(filepath=str(folder/'dressing.blend'),compress=True)
(folder/'library.json').write_text(json.dumps(records,indent=2));print('DRESSING LIBRARY COMPLETE',flush=True);os._exit(0)
