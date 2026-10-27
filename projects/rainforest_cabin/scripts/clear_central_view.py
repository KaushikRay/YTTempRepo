"""Relocate bare trunks that cut the central cabin/stream sightline.

Executed after the reference camera is created. Preserve tree geometry and forest
density, but move the central pole-like trunks into the left/right forest banks.
"""
from bpy_extras.object_utils import world_to_camera_view

bpy.context.view_layer.update()
moved=[]
for ob in sorted(bpy.data.objects,key=lambda o:o.name):
    if not ob.name.startswith('Irregular bark mapped forest trunk'):continue
    points=[ob.matrix_world@Vector(p) for p in ob.bound_box]
    lo=Vector([min(v[i] for v in points) for i in range(3)])
    hi=Vector([max(v[i] for v in points) for i in range(3)])
    center=Vector(((lo.x+hi.x)/2,(lo.y+hi.y)/2,lo.z))
    projected=world_to_camera_view(s,s.camera,center)
    if not .43<projected.x<.55:continue
    i=len(moved);target_x=(-13.0-i*.45) if i%2==0 else (13.0+i*.45)
    dz=terrain_z(target_x,center.y)-terrain_z(center.x,center.y)
    ob.location+=Vector((target_x-center.x,0,dz))
    shifted=center+Vector((target_x-center.x,0,dz))
    new=world_to_camera_view(s,s.camera,shifted)
    assert not .43<new.x<.55
    moved.append({'name':ob.name,'old_base_world':list(center),'new_base_world':list(shifted),
                  'old_screen_x':projected.x,'new_screen_x':new.x})
assert len(moved)==5,moved
(ROOT/'research'/'tree_relocation.json').write_text(json.dumps(moved,indent=2))
status('central_view_cleared',relocated_trunks=len(moved))
