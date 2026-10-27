"""Relocate and test the integrated cached scene and approved palm projection."""
import bpy,json,hashlib,os,shutil,tempfile,traceback
from pathlib import Path
import numpy as np
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
root=Path(__file__).resolve().parents[1]
try:
 with tempfile.TemporaryDirectory(prefix='integrated-fluid-portability-',dir='/tmp') as folder:
  dest=Path(folder)
  paths=['rainforest_integrated_fluid.blend','scripts/integrated_fluid_scene.py','assets/integrated_fluid/channel.json','assets/integrated_fluid/upstream_instance.json','assets/realism/rainforest_trail/rainforest_trail.hdr']
  paths += [f'assets/integrated_fluid/fluid_cache_{i:02d}.zip' for i in range(1,5)]
  for name in paths:
   p=dest/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/name,p)
  (dest/'renders').mkdir(exist_ok=True)
  bpy.ops.wm.open_mainfile(filepath=str(dest/'rainforest_integrated_fluid.blend'));s=bpy.context.scene
  assert s['water_motion_from_images_or_footage']==False and s['background_generated_matte']
  water=bpy.data.materials['True liquid surface with simulation-derived foam'];assert not any(n.bl_idname=='ShaderNodeTexImage' for n in water.node_tree.nodes)
  assert not any(im.users and im.source=='MOVIE' for im in bpy.data.images)
  palm=bpy.data.objects['Flexible foreground palms — anchored top and right'];data={'vertices':[tuple(v.co) for v in palm.data.vertices],'shape_keys':{k.name:{'positions':[tuple(v.co) for v in k.data]} for k in palm.data.shape_keys.key_blocks},'drivers':[d.driver.expression for d in palm.data.shape_keys.animation_data.drivers]}
  fingerprint=hashlib.sha256(json.dumps(data).encode()).hexdigest();assert fingerprint=='0d9fd517e440e5e2c217f4a9d2b8573ddd9cda2b05794fbd2d12d5637b372e64'
  exec(bpy.data.texts['ENABLE_INTEGRATED_FLUID_PLAYBACK.py'].as_string(),{})
  samples=[];errors=[]
  for frame in [1,24,48,72,96]:
   s.frame_set(frame);bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();ev=palm.evaluated_get(dg);m=ev.to_mesh()
   for i in range(0,len(m.vertices),347):
    v=m.vertices[i].co;uv=world_to_camera_view(s,s.camera,palm.matrix_world@v);errors.append(max(abs(uv.x-(v.x/16+.5)),abs(uv.y-(v.y/9+.5))))
   ev.to_mesh_clear();body=bpy.data.objects['Simulated liquid'];far=bpy.data.objects['Upstream instance of simulated liquid'];assert body.data==far.data
   samples.append({'frame':frame,'water_vertices':len(body.data.vertices),'foam_points':len(bpy.data.objects['Simulation foam microbubbles'].data.vertices)})
  assert max(errors)<2e-6,max(errors)
  assert len(set(x['water_vertices'] for x in samples))>=4
  external=[]
  for image in bpy.data.images:
   if image.users and image.source=='FILE' and not image.packed_file:
    path=Path(bpy.path.abspath(image.filepath));assert path.is_relative_to(dest) and path.is_file();external.append(str(path.relative_to(dest)))
  result={'relocated_cached_playback':True,'water_material_image_textures':0,'used_movie_images':0,'approved_palm_geometry_and_drivers_identical':True,'palm_data_sha256':fingerprint,'maximum_palm_screen_projection_error_normalized':max(errors),
   'upstream_is_shared_geometry_instance':True,'timeline_samples':samples,'external_images_resolved':external,'photographic_background_retained':True}
  (root/'research/integrated_fluid/scene_checks.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
except BaseException:traceback.print_exc();os._exit(1)
os._exit(0)
