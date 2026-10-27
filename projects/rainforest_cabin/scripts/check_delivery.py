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
png=root/'renders'/'first_still.png';data=png.read_bytes()
assert data[:8]==b'\x89PNG\r\n\x1a\n'
width,height=struct.unpack('>II',data[16:24]);assert (width,height)==(1920,1080)
blend_sizes={str(p.relative_to(root)):p.stat().st_size for p in root.rglob('*.blend')}
assert max(blend_sizes.values())<100*1024*1024
report={'resolution':[width,height],'cycles_samples':128,'missing_files':missing,
        'libraries':libraries,'rain_streak_count':len(rain),'rain_driver_spot_checks':checks,
        'render_sha256':hashlib.sha256(data).hexdigest(),'blend_file_bytes':blend_sizes,
        'still_only':True,'rain_is_analytic_geometry_not_fluid_simulation':True,
        'water_and_vegetation_motion_tested':False,'photorealism_target_approved':False,
        'user_reference_available_in_chat_only':True}
(root/'renders'/'qa.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report),flush=True)
os._exit(0)
