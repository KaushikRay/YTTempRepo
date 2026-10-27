"""Relocate the study and enable its embedded geometry playback from ZIPs."""
import bpy,hashlib,json,os,shutil,tempfile,traceback
from pathlib import Path
root=Path(__file__).resolve().parents[1]
try:
 with tempfile.TemporaryDirectory(prefix='fluid-study-portability-',dir='/tmp') as folder:
  dest=Path(folder)
  paths=['rainforest_fluid_study.blend','scripts/render_fluid_river.py','research/fluid_river/simulation.json','assets/fluid_river/fluid_cache_01.zip','assets/fluid_river/fluid_cache_02.zip',
         'assets/realism/river_small_rocks/Diffuse.jpg','assets/realism/river_small_rocks/Rough.jpg','assets/realism/rainforest_trail/rainforest_trail.hdr']
  for name in paths:
   target=dest/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/name,target)
  bpy.ops.wm.open_mainfile(filepath=str(dest/'rainforest_fluid_study.blend'));s=bpy.context.scene
  assert s['standalone_physics_test'] and not s['water_uses_images_or_footage']
  mat=bpy.data.materials['True liquid surface with simulation-derived foam'];assert not any(n.bl_idname in ['ShaderNodeTexImage','ShaderNodeTexEnvironment'] for n in mat.node_tree.nodes)
  bpy.context.view_layer.update();bpy.data.texts['ENABLE_FLUID_PLAYBACK.py'].use_module=False
  exec(bpy.data.texts['ENABLE_FLUID_PLAYBACK.py'].as_string(),{})
  samples=[]
  for frame in [1,24,48]:
   s.frame_set(frame);ob=bpy.data.objects['Simulated liquid'];samples.append({'frame':frame,'vertices':len(ob.data.vertices),'triangles':len(ob.data.polygons),'foam_geometry_points':len(bpy.data.objects['Simulation foam microbubbles'].data.vertices)})
  assert len(set(x['vertices'] for x in samples))==3 and all(x['foam_geometry_points']>100 for x in samples)
  external=[]
  for image in bpy.data.images:
   if image.users and image.source=='FILE' and not image.packed_file:
    p=Path(bpy.path.abspath(image.filepath));assert p.is_relative_to(dest) and p.is_file(),p;external.append(str(p.relative_to(dest)))
  result={'relocated_cache_playback_success':True,'raw_npz_files_required':False,'foam_derived_geometry_loaded':True,'water_material_image_textures':0,'timeline_samples':samples,'external_textures_resolved':external,'approved_scene_modified':False}
  (root/'research/fluid_river/playback_checks.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
except BaseException:traceback.print_exc();os._exit(1)
os._exit(0)
