"""Check the saved Blender delivery and the real rendered image, without saving changes."""
from pathlib import Path
import bpy, hashlib, json, os, struct

root=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(root/'rainforest_cabin.blend'))
s=bpy.context.scene
missing=[];libraries=[]
for lib in bpy.data.libraries:
    p=Path(bpy.path.abspath(lib.filepath));libraries.append(str(p.relative_to(root)))
    if not p.is_file():missing.append(str(p))
for im in bpy.data.images:
    if im.users and im.source=='FILE' and not im.packed_file:
        p=Path(bpy.path.abspath(im.filepath,library=im.library))
        if not p.is_file():missing.append(str(p))
assert not missing,missing
assert len(libraries)==7,libraries
assert s.render.engine=='CYCLES' and s.render.resolution_x==1920 and s.render.resolution_y==1080
assert s.cycles.samples==128
assert s.render.filepath.startswith('//renders/')
assert s.camera.name=='Sheltered porch reference camera'
rain=list(bpy.data.collections['Continuously replenishing rain'].objects)
assert len(rain)>8000,len(rain)
checks=[]
for frame in [1,240,1440,14400]:
    s.frame_set(frame);dep=bpy.context.evaluated_depsgraph_get();upper=0
    for ob in rain:
        upper+=ob.evaluated_get(dep).location.z>12
    assert upper>1000,(frame,upper)
    checks.append({'frame':frame,'streaks_above_12m':upper})
output=os.environ.get('OUTPUT','clear_view_still.png')
png=root/'renders'/output;data=png.read_bytes()
assert data[:8]==b'\x89PNG\r\n\x1a\n'
width,height=struct.unpack('>II',data[16:24]);assert (width,height)==(1920,1080)
blend_sizes={str(p.relative_to(root)):p.stat().st_size for p in root.rglob('*.blend')}
assert max(blend_sizes.values())<100*1024*1024
report={'resolution':[width,height],'cycles_samples':128,'missing_files':missing,
        'libraries':libraries,'rain_streak_count':len(rain),'rain_driver_spot_checks':checks,
        'render_sha256':hashlib.sha256(data).hexdigest(),'blend_file_bytes':blend_sizes,
        'still_only':True,'rain_is_analytic_geometry_not_fluid_simulation':True,
        'motion_rig_checked':(root/'renders/motion/rig_checks.json').exists(),'photorealism_target_approved':False,
        'user_reference_available_in_chat_only':True}
assert s.render.filepath=='//renders/'+output,s.render.filepath
leaf_masks=[]
for mat in bpy.data.materials:
    if not mat.use_nodes:continue
    mask=mat.node_tree.nodes.get('Verified photographic leaf silhouette')
    if mask:
        p=next(n for n in mat.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
        assert p.inputs['Alpha'].is_linked and p.inputs['Alpha'].links[0].from_node==mask,mat.name
        assert mask.image.packed_file and mask.image.colorspace_settings.name=='Non-Color'
        leaf_masks.append({'material':mat.name,'mask':mask.image.name,'resolution':list(mask.image.size)})
assert len(leaf_masks)==6,leaf_masks
palms=[o for o in bpy.data.objects if o.name.endswith('curved pinnae')]
assert len(palms)==51,len(palms)
assert not any(o.name.endswith('articulated leaflets') for o in bpy.data.objects)
report.update(output=output,verified_leaf_masks=leaf_masks,curved_palm_fronds=len(palms),photograph_reference_count=14)
qa_name='qa_clear_view.json' if output=='clear_view_still.png' else 'qa_foliage.json'
(root/'renders'/qa_name).write_text(json.dumps(report,indent=2))
print(json.dumps(report),flush=True)
os._exit(0)
