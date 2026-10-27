"""Standalone fully 3D fluid proof: simulated meshes, solid channel and PBR light.

The approved cabin/palm scene is not edited. This is a physical-method test before
integration. No water photograph, movie, UV advection or image backdrop is used.
"""
import bpy,json,math,os,time,traceback,subprocess,hashlib,io,zipfile
from pathlib import Path
import numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'renders/fluid_river';FRAMES=OUT/'frames';FRAMES.mkdir(parents=True,exist_ok=True)
DATA=json.loads((ROOT/'research/fluid_river/simulation.json').read_text())
def cache_array(name,frame):
 path=ROOT/f'assets/fluid_river/meshes/{name}_{frame:04d}.npz'
 if path.exists():return np.load(path)
 chunk=(frame-1)//24+1
 with zipfile.ZipFile(ROOT/f'assets/fluid_river/fluid_cache_{chunk:02d}.zip') as archive:
  return np.load(io.BytesIO(archive.read(f'{name}_{frame:04d}.npz')))

def status(phase,**extra):
 d={'phase':phase,'worker_running':phase not in ['complete','failed'],'updated_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'pid':os.getpid(),'variant':'fully_3D_fluid_proof',**extra}
 (ROOT/'status.json').write_text(json.dumps(d,indent=2));(OUT/'status.json').write_text(json.dumps(d,indent=2));print('FLUID RENDER STATUS',json.dumps(d),flush=True)
def material(name,color,rough=.5):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;return m
def bed(y):
 def fall(a,b):
  t=max(0,min(1,(y-a)/(b-a)));return 1-t*t*(3-2*t)
 return .18+.37*fall(1.35,1.7)+.28*fall(2.55,2.8)+.24*fall(3.7,4)
def mesh(name,verts,faces,mat):
 d=bpy.data.meshes.new(name);d.from_pydata(verts,[],faces);d.update();o=bpy.data.objects.new(name,d);bpy.context.scene.collection.objects.link(o);d.materials.append(mat);return o
def aim(ob,point):ob.rotation_euler=(Vector(point)-ob.location).to_track_quat('-Z','Y').to_euler()
def rock_material():
 m=material('Wet photographic river stone',(.08,.09,.07),.35);n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');uv=n.new('ShaderNodeTexCoord');mapping=n.new('ShaderNodeVectorMath');mapping.operation='SCALE';mapping.inputs['Scale'].default_value=.6;l.new(uv.outputs['Object'],mapping.inputs[0])
 for file,socket,colorspace in [('Diffuse.jpg','Base Color','sRGB'),('Rough.jpg','Roughness','Non-Color')]:
  tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(ROOT/'assets/realism/river_small_rocks'/file));tex.image.colorspace_settings.name=colorspace;tex.projection='BOX';tex.projection_blend=.3;l.new(mapping.outputs[0],tex.inputs[0]);l.new(tex.outputs[0],p.inputs[socket])
 normal=n.new('ShaderNodeTexNoise');normal.inputs['Scale'].default_value=80;normal.inputs['Detail'].default_value=3;l.new(uv.outputs['Object'],normal.inputs[0]);bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.25;bump.inputs['Distance'].default_value=.004;l.new(normal.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal']);p.inputs['Coat Weight'].default_value=.25
 return m
def water_material():
 m=material('True liquid surface with simulation-derived foam',(.92,.98,.96),.05);n=m.node_tree.nodes;l=m.node_tree.links;p=n.get('Principled BSDF');p.inputs['Transmission Weight'].default_value=1;p.inputs['IOR'].default_value=1.333
 foam=n.new('ShaderNodeBsdfPrincipled');foam.inputs['Base Color'].default_value=(.66,.72,.71,1);foam.inputs['Roughness'].default_value=.3;foam.inputs['IOR'].default_value=1.333;foam.inputs['Transmission Weight'].default_value=.15
 coord=n.new('ShaderNodeTexCoord');micro=n.new('ShaderNodeTexNoise');micro.inputs['Scale'].default_value=180;micro.inputs['Detail'].default_value=3;l.new(coord.outputs['Object'],micro.inputs[0]);bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.3;bump.inputs['Distance'].default_value=.001;l.new(micro.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],foam.inputs['Normal'])
 attr=n.new('ShaderNodeVertexColor');attr.layer_name='simulation_foam';r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].position=.62;r.color_ramp.elements[1].position=.95;l.new(attr.outputs[0],r.inputs[0])
 mix=n.new('ShaderNodeMixShader');l.new(r.outputs[0],mix.inputs[0]);l.new(p.outputs[0],mix.inputs[1]);l.new(foam.outputs[0],mix.inputs[2]);out=n.get('Material Output');l.new(mix.outputs[0],out.inputs[0])
 absorb=n.new('ShaderNodeVolumeAbsorption');absorb.inputs['Color'].default_value=(.5,.72,.62,1);absorb.inputs['Density'].default_value=.25;l.new(absorb.outputs[0],out.inputs['Volume']);return m
def load_water(ob,frame):
 f=cache_array('liquid',frame);d=bpy.data.meshes.new('Simulated liquid frame %04d'%frame);d.from_pydata(f['vertices'],[],f['faces']);d.update();d.materials.append(bpy.data.materials['True liquid surface with simulation-derived foam'])
 for p in d.polygons:p.use_smooth=True
 attr=d.color_attributes.new(name='simulation_foam',type='FLOAT_COLOR',domain='CORNER');values=f['foam'];indices=np.empty(len(d.loops),np.int32);d.loops.foreach_get('vertex_index',indices);col=np.ones((len(indices),4),np.float32);col[:,:3]=values[indices,None];attr.data.foreach_set('color',col.ravel())
 previous=ob.data;ob.data=d
 if previous and previous.users==0:bpy.data.meshes.remove(previous)
 bubbles=bpy.data.objects.get('Simulation foam microbubbles')
 if bubbles:
  try:centers=cache_array('foam_points',frame)['positions']
  except (FileNotFoundError,KeyError):
   from scipy.spatial import cKDTree
   particles=np.load(ROOT/f'assets/fluid_river/meshes/particles_{frame:04d}.npz');ids=np.flatnonzero(particles['foam']>.35)[::3]
   positions=particles['positions'][ids];vertices=f['vertices'];dist,nearest=cKDTree(vertices).query(positions,workers=1)
   normals=np.empty(len(d.vertices)*3,np.float32);d.vertices.foreach_get('normal',normals);normals=normals.reshape(-1,3)
   selected=(dist<.045)&(normals[nearest,2]>.05)
   nearest=nearest[selected];centers=vertices[nearest]+normals[nearest]*.002
   np.savez_compressed(ROOT/f'assets/fluid_river/meshes/foam_points_{frame:04d}.npz',positions=centers.astype(np.float32))
  cloud=bpy.data.meshes.new('Surface foam points frame %04d'%frame);cloud.from_pydata(centers,[],[]);cloud.update();old=bubbles.data;bubbles.data=cloud
  if old and old.users==0:bpy.data.meshes.remove(old)
 return len(d.vertices),len(d.polygons)
def setup_bubbles():
 foam=material('Small aerated foam bubbles',(.72,.78,.77),.26)
 bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=.0045,location=(0,0,-5));source=bpy.context.object;source.name='Foam bubble source';source.data.materials.append(foam)
 obj=mesh('Simulation foam microbubbles',[],[],foam);group=bpy.data.node_groups.new('Actual surface-particle foam instances','GeometryNodeTree');group.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry');group.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
 mod=obj.modifiers.new('Fine 3D foam detail','NODES');mod.node_group=group;n=group.nodes;l=group.links;inp=n.new('NodeGroupInput');out=n.new('NodeGroupOutput');info=n.new('GeometryNodeObjectInfo');info.inputs['Object'].default_value=source;info.transform_space='ORIGINAL';info.inputs['As Instance'].default_value=True
 instance=n.new('GeometryNodeInstanceOnPoints');l.new(inp.outputs[0],instance.inputs['Points']);l.new(info.outputs['Geometry'],instance.inputs['Instance']);l.new(instance.outputs[0],out.inputs[0])
def setup():
 bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=int(os.environ.get('SAMPLES','32'));s.cycles.use_denoising=True;s.cycles.max_bounces=8;s.cycles.transmission_bounces=6;s.cycles.glossy_bounces=3;s.render.threads_mode='FIXED';s.render.threads=4
 width=int(os.environ.get('WIDTH','960'));s.render.resolution_x=width;s.render.resolution_y=round(width*9/16);s.render.resolution_percentage=100;s.render.fps=24;s.frame_end=int(os.environ.get('RENDER_FRAMES','48'));s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast'
 s.world=bpy.data.worlds.new('Real rainforest light');s.world.use_nodes=True;n=s.world.node_tree.nodes;l=s.world.node_tree.links;tex=n.new('ShaderNodeTexEnvironment');tex.image=bpy.data.images.load(str(ROOT/'assets/realism/rainforest_trail/rainforest_trail.hdr'));l.new(tex.outputs[0],n.get('Background').inputs['Color']);n.get('Background').inputs['Strength'].default_value=.65
 rock=rock_material();verts=[];faces=[];nx,ny=56,160
 for j in range(ny+1):
  y=-.15+6.1*j/ny
  for i in range(nx+1):
   x=-.4+3.2*i/nx;z=bed(y)+min(.28,3*max(0,abs(x-1.2)-.76)**2);verts.append((x,y,z))
 for j in range(ny):
  for i in range(nx):
   a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
 ground=mesh('Solid stepped channel — same bed as solver',verts,faces,rock)
 for p in ground.data.polygons:p.use_smooth=True
 for i,r in enumerate(DATA['solid_ellipsoids']):
  bpy.ops.mesh.primitive_uv_sphere_add(segments=48,ring_count=24,location=r[:3]);o=bpy.context.object;o.name='Physical collision rock %d'%i;o.scale=r[3:];o.data.materials.append(rock)
  noise=bpy.data.textures.new('Rock irregularity %d'%i,type='CLOUDS');noise.noise_scale=.15;mod=o.modifiers.new('Small irregularities within collision margin','DISPLACE');mod.texture=noise;mod.strength=.035;mod.mid_level=.5
  for p in o.data.polygons:p.use_smooth=True
 # Dry margin boulders use the existing CC0 scanned rock library.
 with bpy.data.libraries.load(str(ROOT/'assets/rock_moss_set_01.blend'),link=False) as (src,dst):dst.collections=[c for c in src.collections if c.startswith('rock_moss_set_01_specimen_')][:3]
 collections=[c for c in dst.collections if c]
 for i,(x,y,size) in enumerate([(-.05,.7,.8),(2.45,1.4,.9),(-.05,2.7,.7),(2.45,3.5,.9),(-.05,4.6,.9),(2.45,5.2,.8)]):
  o=bpy.data.objects.new('Scanned bank boulder %d'%i,None);s.collection.objects.link(o);o.instance_type='COLLECTION';o.instance_collection=collections[i%len(collections)];o.location=(x,y,bed(y)+.12);o.scale=(size,)*3
 cam=bpy.data.cameras.new('Fluid proof camera');o=bpy.data.objects.new('Fluid proof camera',cam);s.collection.objects.link(o);o.location=(3.8,7.0,3.45);aim(o,(1.2,2.8,.62));cam.lens=40;s.camera=o
 light=bpy.data.lights.new('Soft overcast reflection','AREA');light.energy=700;light.shape='DISK';light.size=4;o=bpy.data.objects.new(light.name,light);s.collection.objects.link(o);o.location=(-2,3.3,5);aim(o,(1.2,2.9,.4))
 water=mesh('Simulated liquid',[],[],water_material());setup_bubbles();load_water(water,1)
 s['method']='Actual 3D position-based fluid mesh sequence, geometry and PBR lighting';s['water_uses_images_or_footage']=False;s['standalone_physics_test']=True;s['integrated_into_approved_cabin_scene']=False
 text=bpy.data.texts.new('ENABLE_FLUID_PLAYBACK.py');text.write("import bpy, sys\nfrom pathlib import Path\nroot=Path(bpy.data.filepath).parent\nsys.path.insert(0,str(root/'scripts'))\nfrom render_fluid_river import load_water\ndef fluid_geometry_update(scene):\n    load_water(bpy.data.objects['Simulated liquid'],max(1,min(scene.frame_end,scene.frame_current)))\nfor old in list(bpy.app.handlers.frame_change_pre):\n    if old.__name__=='fluid_geometry_update': bpy.app.handlers.frame_change_pre.remove(old)\nbpy.app.handlers.frame_change_pre.append(fluid_geometry_update)\nfluid_geometry_update(bpy.context.scene)\nprint('Fluid mesh playback enabled for this session')\n")
 s.render.filepath='//renders/fluid_river/still.png'
 for im in bpy.data.images:
  if im.source=='FILE' and not im.packed_file:im.filepath=bpy.path.relpath(im.filepath,start=str(ROOT))
 bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'rainforest_fluid_study.blend'),compress=True)
 return s,water
def main():
 status('setting_up_3D_fluid_render');s,water=setup();diag=os.environ.get('DIAGNOSTIC')
 if diag:
  frame=int(os.environ.get('TEST_FRAME','48'));s.frame_set(frame);load_water(water,frame);s.render.filepath=str(OUT/'diagnostic.png');status('rendering_fluid_diagnostic',frame=frame);bpy.ops.render.render(write_still=True);status('complete',output='renders/fluid_river/diagnostic.png');return
 start=time.monotonic();total=int(os.environ.get('RENDER_FRAMES','48'))
 digest=hashlib.sha256(Path(__file__).read_bytes()+(ROOT/'research/fluid_river/simulation.json').read_bytes()).hexdigest();signature=OUT/'render_signature.json'
 if not signature.exists() or json.loads(signature.read_text())['sha256']!=digest:
  for p in FRAMES.glob('*.png'):p.unlink()
  signature.write_text(json.dumps({'sha256':digest,'width':s.render.resolution_x,'samples':s.cycles.samples,'frames':total},indent=2))
 for frame in range(1,total+1):
  path=FRAMES/f'{frame:04d}.png'
  if path.exists():continue
  s.frame_set(frame);nv,nf=load_water(water,frame);status('rendering_3D_fluid',current_frame=frame,completed_frames=frame-1,total_frames=total,mesh_vertices=nv,mesh_faces=nf,estimated_seconds_remaining=None if frame==1 else round((time.monotonic()-start)/(frame-1)*(total+1-frame)))
  s.render.filepath=str(path);bpy.ops.render.render(write_still=True)
 status('encoding_3D_fluid',completed_frames=total,total_frames=total)
 movie=OUT/'preview.mp4';subprocess.run(['ffmpeg','-y','-v','error','-framerate','24','-i',str(FRAMES/'%04d.png'),'-frames:v',str(total),'-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(movie)],check=True)
 import shutil;shutil.copyfile(FRAMES/f'{min(24,total):04d}.png',OUT/'still.png')
 result={'method':s['method'],'real_3D_liquid_geometry':True,'water_images_or_footage':False,'resolution':[s.render.resolution_x,s.render.resolution_y],'frames':total,'fps':24,'duration_seconds':total/24,'cycles_samples':s.cycles.samples,'audio':False,'seamless_loop':False,'standalone_physics_test':True,'integrated_into_approved_scene':False,'elapsed_seconds':time.monotonic()-start,'preview_sha256':hashlib.sha256(movie.read_bytes()).hexdigest()}
 (OUT/'render_report.json').write_text(json.dumps(result,indent=2));status('complete',output='renders/fluid_river/preview.mp4',completed_frames=total,total_frames=total)
if __name__=='__main__':
 try:main()
 except BaseException as exc:traceback.print_exc();status('failed',error=str(exc));os._exit(1)
 os._exit(0)
