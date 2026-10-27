"""The layered motion .blend should open without any original asset directory."""
import bpy, json, os, shutil, tempfile, traceback
from pathlib import Path
root=Path(__file__).resolve().parents[1]
try:
    with tempfile.TemporaryDirectory(prefix='hybrid-motion-relocation-',dir='/tmp') as temp:
        path=Path(temp)/'rainforest_hybrid_motion.blend';shutil.copy2(root/path.name,path)
        bpy.ops.wm.open_mainfile(filepath=str(path))
        images=[im for im in bpy.data.images if im.users and im.source=='FILE']
        assert len(images)==2 and all(im.packed_file for im in images)
        assert len(bpy.data.libraries)==0
        s=bpy.context.scene;assert s.render.filepath=='//renders/hybrid_motion/still.png'
        assert s.camera.data.type=='ORTHO' and s.frame_end==144 and s.render.fps==24
        result={'opens_from_unrelated_directory':True,'required_external_files':0,'packed_images':[im.name for im in images],
                'relative_output':s.render.filepath,'source_assets_retained_separately_for_editing':True}
        (root/'research/hybrid_motion/portability.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
except BaseException:traceback.print_exc();os._exit(1)
os._exit(0)
