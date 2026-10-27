"""Validate the substantially rebuilt still scene and its physical asset contacts."""
from pathlib import Path
import bpy,json,os
from mathutils import Vector
from mathutils.bvhtree import BVHTree

root=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(root/'rainforest_cabin.blend'));s=bpy.context.scene
missing=[];libraries=[]
for lib in bpy.data.libraries:
    path=Path(bpy.path.abspath(lib.filepath));libraries.append(str(path.relative_to(root)))
    if not path.is_file():missing.append(str(path))
for image in bpy.data.images:
    if image.users and image.source=='FILE' and not image.packed_file:
        path=Path(bpy.path.abspath(image.filepath,library=image.library))
        if not path.is_file():missing.append(str(path))
assert not missing,missing
assert len(libraries)==12,libraries
assert s.render.resolution_x==1920 and s.render.resolution_y==1080 and s.cycles.samples==128
assert s.render.filepath=='//renders/realism_still.png'
parent=bpy.data.objects['Cabin assembly slight oblique view'];assert abs(parent.rotation_euler.z-.23)<1e-5
assert not bpy.data.objects.get('Cabin interior shadow')
assert not bpy.data.objects['Warm interior room light'].visible_camera
terrain=bpy.data.objects['Sculpted stream banks and rainforest floor']
bvh=BVHTree.FromPolygons([terrain.matrix_world@v.co for v in terrain.data.vertices],[list(p.vertices) for p in terrain.data.polygons])
supports=[]
for ob in bpy.data.objects:
    if not ob.name.startswith('Cabin timber stilt'):continue
    vertices=[ob.matrix_world@v.co for v in ob.data.vertices];bottom=min(v.z for v in vertices);center=ob.matrix_world.translation
    hit=bvh.ray_cast(Vector((center.x,center.y,20)),Vector((0,0,-1)),40)[0]
    assert hit is not None
    gap=bottom-hit.z
    assert gap<.025,(ob.name,gap)
    supports.append({'object':ob.name,'base_above_actual_terrain_m':gap})
assert len(supports)==9,len(supports)
rain=bpy.data.collections['Continuously replenishing rain'];visible=sum(not ob.hide_render for ob in rain.objects)
assert len(rain.objects)>18000 and visible>14000,(len(rain.objects),visible)
counts={prefix:sum(o.name.startswith(prefix) for o in bpy.data.objects) for prefix in ['Scanned exposed bank roots','Fine bank moss colony','Irregular fallen bark and litter','Broken whitewater over stone ledge','Natural stone creek ledge','Layered forest regrowth']}
assert counts['Broken whitewater over stone ledge']==3 and counts['Natural stone creek ledge']==12,counts
assert counts['Fine bank moss colony']>100 and counts['Scanned exposed bank roots']>15,counts
sizes={str(p.relative_to(root)):p.stat().st_size for p in root.rglob('*.blend')};assert max(sizes.values())<100*1024*1024
result={'missing_files':missing,'linked_libraries':libraries,'render_resolution':[1920,1080],'max_samples':128,
        'support_contact_checks':supports,'scan_and_ground_detail_counts':counts,'rain_streaks_total':len(rain.objects),'rain_streaks_visible':visible,
        'photographic_hdri':'rainforest_trail','cabin_rotation_degrees':13.178,'full_photorealism_approved':False,'still_scene_only':True,'file_sizes':sizes}
(root/'research/realism/scene_checks.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
os._exit(0)
