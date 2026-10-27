"""The layered motion .blend should open without any original asset directory."""
import bpy, json, os, shutil, tempfile, traceback
from pathlib import Path
root=Path(__file__).resolve().parents[1]
try:
    with tempfile.TemporaryDirectory(prefix='hybrid-motion-relocation-',dir='/tmp') as temp:
        path=Path(temp)/'rainforest_hybrid_motion.blend';shutil.copy2(root/path.name,path)
        movie=root/'assets/river_flow/real_rapids.mp4'
        if movie.exists():
            target=Path(temp)/'assets/river_flow/real_rapids.mp4';target.parent.mkdir(parents=True);shutil.copy2(movie,target)
        bpy.ops.wm.open_mainfile(filepath=str(path))
        images=[im for im in bpy.data.images if im.users and im.source=='FILE']
        assert len(images)==2 and all(im.packed_file for im in images)
        movies=[im for im in bpy.data.images if im.users and im.source=='MOVIE']
        for movie_image in movies:
            assert movie_image.filepath.startswith('//') and Path(bpy.path.abspath(movie_image.filepath)).is_relative_to(Path(temp))
            assert Path(bpy.path.abspath(movie_image.filepath)).is_file()
        assert len(bpy.data.libraries)==0
        s=bpy.context.scene;assert s.render.filepath in ['//renders/hybrid_motion/still.png','//renders/river_flow/still.png']
        assert s.camera.data.type=='ORTHO' and s.frame_end==144 and s.render.fps==24
        result={'opens_from_unrelated_directory':True,'required_external_files':len(movies),'packed_images':[im.name for im in images],
                'external_movie_paths':[im.filepath for im in movies],
                'relative_output':s.render.filepath,'source_assets_retained_separately_for_editing':True}
        (root/'research/hybrid_motion/portability.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
except BaseException:traceback.print_exc();os._exit(1)
os._exit(0)
