"""Relocate the scene/libraries/maps and check that no original root is required."""
from pathlib import Path
import bpy, json, os, shutil, tempfile

root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='rainforest-portability-',dir='/tmp') as temp:
    dest=Path(temp)
    shutil.copy2(root/'rainforest_cabin.blend',dest/'rainforest_cabin.blend')
    for path in (root/'assets').rglob('*'):
        if path.is_file() and path.suffix in ['.blend','.jpg','.png']:
            target=dest/path.relative_to(root);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,target)
    bpy.ops.wm.open_mainfile(filepath=str(dest/'rainforest_cabin.blend'))
    checked=[]
    for lib in bpy.data.libraries:
        path=Path(bpy.path.abspath(lib.filepath));assert path.is_relative_to(dest) and path.is_file(),path
        checked.append(str(path.relative_to(dest)))
    images=0
    for image in bpy.data.images:
        if image.users and image.source=='FILE' and not image.packed_file:
            path=Path(bpy.path.abspath(image.filepath,library=image.library))
            assert path.is_relative_to(dest) and path.is_file(),path
            images+=1
    output=bpy.context.scene.render.filepath;assert output=='//renders/foliage_still.png',output
    result={'relocated_libraries':checked,'relocated_external_images':images,'render_output_relative':True,'original_root_required':False}
    (root/'research'/'portability.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
os._exit(0)
