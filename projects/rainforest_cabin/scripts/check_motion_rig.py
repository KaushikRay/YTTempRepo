"""Check actual evaluated motion, fixed attachment points and the clear sightline."""
import bpy,json,math,os
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view

root=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(root/'rainforest_motion.blend'));s=bpy.context.scene
setup=json.loads((root/'renders/motion/setup.json').read_text());report=[]
trunk=bpy.data.objects['Round tapered palm trunk.004']
assert sum(v.co.x for v in trunk.data.vertices)/len(trunk.data.vertices)<-7
water=bpy.data.objects['Continuous reflective creek surface'];original=None
for frame in [1,24,48,72,96]:
    s.frame_set(frame);bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get()
    max_drift=0;leaf_tip_motion=[]
    for anchor in setup['anchors']:
        pivot=bpy.data.objects[anchor['object']];base=Vector(anchor['base'])
        max_drift=max(max_drift,(pivot.evaluated_get(dep).matrix_world.translation-base).length)
        prefix=anchor['object'].removesuffix(' wind anchor');rib=bpy.data.objects[prefix+' tapered rachis']
        root_point=rib.evaluated_get(dep).matrix_world@Vector(rib.data.splines[0].points[0].co[:3])
        max_drift=max(max_drift,(root_point-base).length)
    assert max_drift<.0001,(frame,max_drift)
    evaluated=water.evaluated_get(dep).data
    z=[v.co.z for v in evaluated.vertices]
    if original is None:original=z
    delta=max(abs(a-b) for a,b in zip(original,z));assert delta<.05,delta
    for ob in bpy.data.objects:
        if not ob.name.startswith('Irregular bark mapped forest trunk'):continue
        points=[ob.matrix_world@Vector(p) for p in ob.bound_box]
        lo=Vector([min(v[i] for v in points) for i in range(3)]);hi=Vector([max(v[i] for v in points) for i in range(3)])
        base=Vector(((lo.x+hi.x)/2,(lo.y+hi.y)/2,lo.z));x=world_to_camera_view(s,s.camera,base).x
        assert not .43<x<.55,(ob.name,x)
    flex=bpy.data.objects['Large foreground arching palm curved pinnae'].data.shape_keys.key_blocks['Gentle frond flex'].value
    report.append({'frame':frame,'maximum_attachment_drift_m':max_drift,'maximum_wave_delta_from_frame_one_m':delta,'hero_frond_flex_value':flex})
assert max(v['maximum_wave_delta_from_frame_one_m'] for v in report[1:])>.002
assert max(v['hero_frond_flex_value'] for v in report)-min(v['hero_frond_flex_value'] for v in report)>.1
missing=[]
for lib in bpy.data.libraries:
    if not Path(bpy.path.abspath(lib.filepath)).is_file():missing.append(lib.filepath)
assert not missing,missing
result={'checks':report,'missing_libraries':missing,'clear_central_tree_sightline':True,'frond_attachment_points_fixed':True}
(root/'renders/motion/rig_checks.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result),flush=True);os._exit(0)
