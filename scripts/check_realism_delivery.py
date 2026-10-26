"""Validate the rendered still and scene assets; writes review evidence.

Use the bpy Python environment after the supervised render has completed.
Immediate process exit avoids the known bpy native shutdown stall after the
checks have finished. The render's actual outcome is recorded independently.
"""
import bpy,hashlib,json,os,struct,subprocess
from pathlib import Path

root=Path(__file__).resolve().parents[1]
runtime=json.loads((root/'renders/realism_runtime.json').read_text())
assert runtime['render_completed'],runtime
png=(root/'renders/realism_study.png').read_bytes();width,height=struct.unpack('>II',png[16:24]);assert (width,height)==(1280,720)
bpy.ops.wm.open_mainfile(filepath=str(root/'realism_study.blend'));scene=bpy.context.scene
assert scene.render.resolution_percentage==100 and scene.cycles.samples==96
missing=[];external=[];packed=0
for image in bpy.data.images:
    if image.users and image.source=='FILE':
        if image.packed_file:packed+=1
        else:
            path=Path(bpy.path.abspath(image.filepath));external.append(str(path.relative_to(root)))
            if not path.is_file():missing.append(str(path))
assert not missing,missing
collection=bpy.data.collections['Interior creeper']
leaf_count=sum(o.type=='MESH' for o in collection.objects)
assert leaf_count>1000 and sum('woody rooted leader' in o.name for o in collection.objects)==4
blend_bytes=(root/'realism_study.blend').stat().st_size;assert blend_bytes<100*1024*1024
original_hash=subprocess.check_output(['git','-C',str(root),'hash-object','storm_lounge.blend'],text=True).strip()
preserved=original_hash=='09d33d5afa1b03e97ffd8e406885c48548de223a';assert preserved
check={'used_packed_file_images':packed,'external_file_images':external,'missing_images':missing,'blend_bytes':blend_bytes,'interior_creeper_leaves':leaf_count,'rooted_ivy_patches':4,'camera_lens_mm':scene.camera.data.lens,'render_output':scene.render.filepath}
(root/'renders/realism_scene_check.json').write_text(json.dumps(check,indent=2))
review={'width':width,'height':height,'cycles_samples':96,'denoising':'OpenImageDenoise','old_motion_scene_preserved':preserved,'new_scene':'realism_study.blend','new_animation_rendered':False,'realism_target_reached':False,'reference_review':'docs/creeper-iteration.md','scene_check':check,'runtime':runtime,'image_sha256':hashlib.sha256(png).hexdigest(),'remaining_gaps':['Exterior village/trees remain underdeveloped','Leaf repetition and wall attachment need further close-up refinement','Room styling and lighting still differ from the original reference','Fire remains filmed footage integrated on a card','New creeper/weather have not received a motion test']}
(root/'renders/realism_review.json').write_text(json.dumps(review,indent=2))
print(json.dumps(check),flush=True)
os._exit(0)
