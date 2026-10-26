"""Create a compact linked CC0 vegetation library, with packed PBR textures."""
import bpy,json,os
from pathlib import Path
from mathutils import Vector,Matrix

root=Path(__file__).resolve().parents[1];folder=root/'assets/exterior'
bpy.ops.wm.read_factory_settings(use_empty=True)
records=[]
for name,path in [('Exterior Fir C',folder/'fir_tree_01_c/fir_tree_01_c.gltf'),('Exterior Shrub 02',folder/'shrub_02/shrub_02.gltf')]:
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
bpy.data.orphans_purge(do_recursive=True)
for image in bpy.data.images:
    if image.source=='FILE' and not image.packed_file:image.pack()
credits=bpy.data.texts.new('CC0_EXTERIOR_CREDITS.txt');credits.write('Poly Haven CC0: Fir Tree 01 — Rob Tuytel / Rico Cilliers; Shrub 02 — Rico Cilliers.\nhttps://polyhaven.com/a/fir_tree_01\nhttps://polyhaven.com/a/shrub_02\nhttps://polyhaven.com/license\n')
bpy.ops.wm.save_as_mainfile(filepath=str(folder/'vegetation.blend'),compress=True)
(folder/'library.json').write_text(json.dumps(records,indent=2));print('EXTERIOR LIBRARY COMPLETE',flush=True);os._exit(0)
