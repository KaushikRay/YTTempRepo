"""Real fitted 3D liquid in the approved locked-camera photographic hybrid.

Water motion is a new PBF bake in a curved, varying-width 3D channel. Original
palms/rain are perspective-reprojected without changing their animation. Static
camera-projected rock proxies handle occlusion; a generated, water-free creek
bed prevents the old painted whitewater showing through refractive water.
"""
import bpy,json,math,os,io,zipfile,time,traceback
from pathlib import Path
import numpy as np
from mathutils import Vector,Matrix
from mathutils.geometry import tessellate_polygon
from scipy.spatial import cKDTree
ROOT=Path(__file__).resolve().parents[1];VARIANT=os.environ.get('INTEGRATED_VARIANT','integrated_fluid')
assert VARIANT in ('integrated_fluid','looped_fluid')
CFG=json.loads((ROOT/f'assets/{VARIANT}/channel.json').read_text());CAM=CFG['camera']
CACHE=ROOT/f'assets/{VARIANT}/meshes';OUT=ROOT/f'renders/{VARIANT}';OUT.mkdir(exist_ok=True)
POS=np.array(CAM['camera_location']);FORWARD=np.array(CAM['camera_forward']);RIGHT=np.cross(FORWARD,[0,0,1]);RIGHT/=np.linalg.norm(RIGHT);UP=np.cross(RIGHT,FORWARD)

def status(phase,**extra):
 d={'phase':phase,'worker_running':phase not in ['complete','failed'],'updated_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'pid':os.getpid(),'variant':'integrated_3D_fluid',**extra}
 for p in [ROOT/'status.json',OUT/'status.json']:p.write_text(json.dumps(d,indent=2))
 print('INTEGRATED FLUID STATUS',json.dumps(d),flush=True)
def sample(key,y):return np.interp(y,np.arange(len(CFG[key]))*.01,CFG[key])
def project(points):
 d=np.asarray(points)-POS;depth=d@FORWARD
 return np.stack([.5+CAM['focal_pixels']/1672*(d@RIGHT)/depth,.5+CAM['focal_pixels']/(1672*9/16)*(d@UP)/depth],axis=-1)
def at_pixel(u,v,depth):return POS+FORWARD*depth+RIGHT*((u/1672-.5)*depth*1672/CAM['focal_pixels'])+UP*((.5-v/941)*depth*(1672*9/16)/CAM['focal_pixels'])
def mat(name):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputMaterial');return m,n,m.node_tree.links,out
def mesh(name,verts,faces,material):
 data=bpy.data.meshes.new(name);data.from_pydata(verts,[],faces);data.update();data.materials.append(material);ob=bpy.data.objects.new(name,data);bpy.context.scene.collection.objects.link(ob)
 if len(verts):
  uvs=project(np.asarray(verts));uv=data.uv_layers.new(name='camera_projection')
  for p in data.polygons:
   for li in p.loop_indices:uv.data[li].uv=uvs[data.loops[li].vertex_index]
 return ob
def projected_photo(name,path,edge=False):
 m,n,l,out=mat(name);geo=n.new('ShaderNodeNewGeometry');transform=n.new('ShaderNodeVectorTransform');transform.vector_type='POINT';transform.convert_from='WORLD';transform.convert_to='CAMERA';l.new(geo.outputs['Position'],transform.inputs[0]);sep=n.new('ShaderNodeSeparateXYZ');l.new(transform.outputs[0],sep.inputs[0])
 values=[]
 for axis,scale in [('X',-CAM['focal_pixels']/1672),('Y',-CAM['focal_pixels']/941)]:
  div=n.new('ShaderNodeMath');div.operation='DIVIDE';l.new(sep.outputs[axis],div.inputs[0]);l.new(sep.outputs['Z'],div.inputs[1]);mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY_ADD';mul.inputs[1].default_value=scale;mul.inputs[2].default_value=.5;l.new(div.outputs[0],mul.inputs[0]);values.append(mul)
 uv=n.new('ShaderNodeUVMap');uv.uv_map='camera_projection';tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(path),check_existing=True);tex.image.pack();tex.extension='EXTEND';l.new(uv.outputs[0],tex.inputs[0])
 emit=n.new('ShaderNodeEmission');l.new(tex.outputs['Color'],emit.inputs['Color'])
 physical=n.new('ShaderNodeBsdfPrincipled');physical.inputs['Roughness'].default_value=.32;physical.inputs['Coat Weight'].default_value=.2;l.new(tex.outputs['Color'],physical.inputs['Base Color']);path=n.new('ShaderNodeLightPath');camera_mix=n.new('ShaderNodeMixShader');l.new(path.outputs['Is Camera Ray'],camera_mix.inputs[0]);l.new(physical.outputs[0],camera_mix.inputs[1]);l.new(emit.outputs[0],camera_mix.inputs[2])
 if edge:
  attr=n.new('ShaderNodeVertexColor');attr.layer_name='bank_feather';clear=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');l.new(attr.outputs['Alpha'],mix.inputs[0]);l.new(clear.outputs[0],mix.inputs[1]);l.new(camera_mix.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs[0])
 else:l.new(camera_mix.outputs[0],out.inputs[0])
 return m
def original_layers():
 names={'Static photographic-style background','Cabin rain occlusion — matched photographic projection','Fine rain behind cabin','Near rain in front of cabin','Roof runoff falling beads','Flexible foreground palms — anchored top and right'}
 with bpy.data.libraries.load(str(ROOT/'rainforest_hybrid_motion.blend'),link=False) as (src,dst):dst.objects=[n for n in src.objects if n in names or n.startswith('Dry shelter rain blocker ')]
 assert len(dst.objects)==11,[o.name for o in dst.objects]
 for ob in dst.objects:
  bpy.context.scene.collection.objects.link(ob)
  if ob.name=='Static photographic-style background':depth=40
  elif ob.name.startswith('Cabin rain occlusion'):depth=20
  elif ob.name=='Fine rain behind cabin':depth=24
  elif ob.name=='Near rain in front of cabin':depth=5
  elif ob.name=='Roof runoff falling beads':depth=8
  elif ob.name.startswith('Dry shelter'):depth=3
  else:depth=4
  z=float(ob.data.vertices[0].co.z);scale=depth*36/(CAM['lens_mm']*16)
  basis=np.column_stack([RIGHT*scale,UP*scale,FORWARD*scale]);matrix=Matrix.Identity(4)
  for i in range(3):
   for j in range(3):matrix[i][j]=float(basis[i,j])
  matrix.translation=Vector(POS+FORWARD*(depth-scale*z));ob.matrix_world=matrix@ob.matrix_world
  for slot in ob.material_slots:
   material=slot.material
   if material and not material.get('camera_only_wrapped'):
    n=material.node_tree.nodes;l=material.node_tree.links;out=next(x for x in n if x.bl_idname=='ShaderNodeOutputMaterial');original=out.inputs['Surface'].links[0].from_socket;path=n.new('ShaderNodeLightPath');clear=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');l.new(path.outputs['Is Camera Ray'],mix.inputs[0]);l.new(clear.outputs[0],mix.inputs[1]);l.new(original,mix.inputs[2]);l.new(mix.outputs[0],out.inputs['Surface']);material['camera_only_wrapped']=True
 return [o.name for o in dst.objects]
def creek_bed():
 material=projected_photo('Water-free bed texture — static geometry under refractive liquid',ROOT/'assets/integrated_fluid/clean_creek_bed.png',True)
 verts=[];faces=[];alpha=[];nx,ny=40,180
 for j in range(ny+1):
  y=-.08+(CFG['bounds_m'][1]+.12)*j/ny;c=sample('center_profile_x',y);width=sample('half_width_profile',y);z=sample('bed_profile_z',y)
  for i in range(nx+1):
   fraction=-1+2*i/nx;x=c+fraction*(width+.30);height=z+min(.32,8*max(0,abs(x-c)-width)**2)
   verts.append((x,y,height));alpha.append(min(1,(1-abs(fraction))*10))
 for j in range(ny):
  for i in range(nx):
   k=j*(nx+1)+i;faces.append((k,k+1,k+nx+2,k+nx+1))
 ob=mesh('Fitted physical channel bed',verts,faces,material);color=ob.data.color_attributes.new(name='bank_feather',type='FLOAT_COLOR',domain='POINT')
 for d,a in zip(color.data,alpha):d.color=(1,1,1,a)
 for p in ob.data.polygons:p.use_smooth=True
 return ob
def bank_proxies():
 material=projected_photo('Original photographic rock occlusion and refraction',ROOT/'assets/hybrid_motion/clean_background.png',True)
 # Visible rock outlines are camera-projected proxies; the new solver collides
 # with the corresponding 3D ellipsoids. Cards mask the photographed silhouette.
 contours=[[(817,736),(850,716),(887,722),(919,745),(924,778),(907,802),(870,794),(840,776)],
           [(963,725),(994,711),(1034,717),(1058,737),(1054,752),(1024,764),(983,757),(963,747)],
           [(1100,760),(1132,751),(1164,769),(1186,797),(1179,829),(1154,841),(1125,838),(1111,824),(1098,799)],
           [(1196,820),(1231,797),(1281,805),(1323,840),(1341,880),(1320,922),(1280,934),(1238,918),(1206,880)],
           [(881,875),(919,857),(963,863),(1006,889),(1034,922),(1023,941),(890,941),(871,913)]]
 for i,(rock,contour) in enumerate(zip(CFG['solid_ellipsoids'],contours)):
  centre=np.array(rock[:3]);depth=float((centre-POS)@FORWARD)-.2
  pts=np.array(contour,float);center=pts.mean(0);inner=pts+(center-pts)/np.linalg.norm(center-pts,axis=1)[:,None]*1.8
  verts=[Vector(at_pixel(u,v,depth)) for u,v in np.vstack([pts,inner])];count=len(contour);faces=[tuple(v+count for v in tri) for tri in tessellate_polygon([verts[count:]])];faces += [(j,(j+1)%count,(j+1)%count+count,j+count) for j in range(count)]
  ob=mesh('Photographic bank contact proxy %d'%i,verts,faces,material);color=ob.data.color_attributes.new(name='bank_feather',type='FLOAT_COLOR',domain='POINT')
  for j,c in enumerate(color.data):c.color=(1,1,1,float(j>=count))
def clear_old_water():
 material=projected_photo('Static dark creek bed behind the actual liquid',ROOT/'assets/integrated_fluid/clean_creek_bed.png')
 outlines=[[(647,607),(688,607),(718,624),(744,637),(786,653),(790,672),(741,667),(701,646),(667,639)],
  [(876,733),(914,730),(940,741),(981,744),(1007,756),(1042,769),(1081,778),(1110,803),(1147,826),(1188,852),(1230,876),(1286,896),(1348,919),(1399,941),(1090,941),(1040,917),(998,887),(955,871),(928,851),(906,826),(905,799),(918,778),(898,758)]]
 for i,outline in enumerate(outlines):
  verts=[Vector(at_pixel(u,v,30)) for u,v in outline];faces=tessellate_polygon([verts]);ob=mesh('Remove frozen source water %d'%i,verts,faces,material)
def water_setup():
 from render_fluid_river import water_material,setup_bubbles
 material=water_material();n=material.node_tree.nodes;l=material.node_tree.links;p=n.get('Principled BSDF');p.inputs['Roughness'].default_value=.11
 coords=n.new('ShaderNodeTexCoord');micro=n.new('ShaderNodeTexNoise');micro.inputs['Scale'].default_value=120;micro.inputs['Detail'].default_value=2.5;l.new(coords.outputs['Object'],micro.inputs[0]);bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.24;bump.inputs['Distance'].default_value=.0014;l.new(micro.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs[0],p.inputs['Normal'])
 absorption=next(x for x in n if x.bl_idname=='ShaderNodeVolumeAbsorption');absorption.inputs['Color'].default_value=(.34,.51,.40,1);absorption.inputs['Density'].default_value=.5
 water=mesh('Simulated liquid',[],[],material);setup_bubbles();return water
def upstream_instance():
 pose=json.loads((ROOT/'assets/integrated_fluid/upstream_instance.json').read_text());source=bpy.data.objects['Simulated liquid'];ob=bpy.data.objects.new('Upstream instance of simulated liquid',source.data);bpy.context.scene.collection.objects.link(ob);matrix=Matrix.Identity(4)
 for i in range(3):
  for j in range(3):matrix[i][j]=pose['matrix'][i][j]
 matrix.translation=Vector(pose['translation']);ob.matrix_world=matrix
 material=projected_photo('Upstream vegetation occlusion',ROOT/'assets/hybrid_motion/clean_background.png')
 for i,outline in enumerate([[(632,594),(662,595),(683,612),(692,633),(704,650),(688,669),(646,657)],[(712,606),(749,602),(788,622),(811,663),(788,680),(752,665),(738,642)]]):
  vertices=[Vector(at_pixel(u,v,21)) for u,v in outline];mesh('Upstream bank vegetation proxy %d'%i,vertices,tessellate_polygon([vertices]),material)
def read_cache(kind,frame):
 path=CACHE/f'{kind}_{frame:04d}.npz'
 if path.exists():return np.load(path)
 with zipfile.ZipFile(ROOT/f'assets/{VARIANT}/fluid_cache_{(frame-1)//24+1:02d}.zip') as archive:return np.load(io.BytesIO(archive.read(path.name)))
def load_frame(frame):
 ob=bpy.data.objects['Simulated liquid'];f=read_cache('liquid',frame);data=bpy.data.meshes.new('Fitted simulated liquid %04d'%frame);data.from_pydata(f['vertices'],[],f['faces']);data.update();data.materials.append(bpy.data.materials['True liquid surface with simulation-derived foam'])
 for face in data.polygons:face.use_smooth=True
 color=data.color_attributes.new(name='simulation_foam',type='FLOAT_COLOR',domain='CORNER');indices=np.empty(len(data.loops),np.int32);data.loops.foreach_get('vertex_index',indices);col=np.ones((len(indices),4),np.float32);col[:,:3]=f['foam'][indices,None];color.data.foreach_set('color',col.ravel());old=ob.data;ob.data=data
 far=bpy.data.objects.get('Upstream instance of simulated liquid')
 if far:far.data=data
 if old.users==0:bpy.data.meshes.remove(old)
 try:points=read_cache('foam_points',frame)['positions']
 except (FileNotFoundError,KeyError):
  particles=read_cache('particles',frame);ids=np.flatnonzero(particles['foam']>.3)[::2];positions=particles['positions'][ids];dist,near=cKDTree(f['vertices']).query(positions,workers=1);normals=np.empty(len(data.vertices)*3,np.float32);data.vertices.foreach_get('normal',normals);normals=normals.reshape(-1,3);valid=(dist<.04)&(normals[near,2]>.0);near=near[valid];points=f['vertices'][near]+normals[near]*.002
  np.savez_compressed(CACHE/f'foam_points_{frame:04d}.npz',positions=points.astype(np.float32))
 cloud=bpy.data.meshes.new('Fitted surface foam points %04d'%frame);cloud.from_pydata(points,[],[]);cloud.update();foam=bpy.data.objects['Simulation foam microbubbles'];old=foam.data;foam.data=cloud
 if old.users==0:bpy.data.meshes.remove(old)
 return len(data.vertices),len(data.polygons),len(points)
def setup():
 bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=int(os.environ.get('SAMPLES','24'));s.cycles.use_denoising=True;s.cycles.max_bounces=8;s.cycles.transmission_bounces=6;s.cycles.transparent_max_bounces=32;s.render.threads_mode='FIXED';s.render.threads=4
 s.render.resolution_x=int(os.environ.get('WIDTH','1920'));s.render.resolution_y=round(s.render.resolution_x*9/16);s.render.resolution_percentage=100;s.render.fps=24;s.frame_end=96;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
 cam=bpy.data.cameras.new('Calibrated cabin-view river camera');o=bpy.data.objects.new(cam.name,cam);s.collection.objects.link(o);o.location=POS;o.rotation_euler=Vector(FORWARD).to_track_quat('-Z','Y').to_euler();cam.lens=CAM['lens_mm'];cam.sensor_width=36;cam.sensor_fit='HORIZONTAL';s.camera=o
 s.world=bpy.data.worlds.new('Rainforest storm reflections');s.world.use_nodes=True;n=s.world.node_tree.nodes;l=s.world.node_tree.links;environment=n.new('ShaderNodeTexEnvironment');environment.image=bpy.data.images.load(str(ROOT/'assets/realism/rainforest_trail/rainforest_trail.hdr'));l.new(environment.outputs[0],n.get('Background').inputs['Color']);n.get('Background').inputs['Strength'].default_value=.17
 original_layers();clear_old_water();creek_bed();bank_proxies();water_setup();load_frame(1);upstream_instance()
 # The generated matte is already display-referred. Compress only the HDR liquid
 # highlights before Standard display, avoiding a second grade on the cabin.
 for name in ['Simulated liquid','Upstream instance of simulated liquid','Simulation foam microbubbles','Foam bubble source']:bpy.data.objects[name].pass_index=1
 s.view_layers[0].use_pass_object_index=True;s.use_nodes=True;n=s.node_tree.nodes;l=s.node_tree.links;n.clear();render=n.new('CompositorNodeRLayers');separate=n.new('CompositorNodeSeparateColor');separate.mode='RGB';l.new(render.outputs['Image'],separate.inputs['Image'])
 maximum=n.new('CompositorNodeMath');maximum.operation='MAXIMUM';l.new(separate.outputs['Red'],maximum.inputs[0]);l.new(separate.outputs['Green'],maximum.inputs[1]);maximum2=n.new('CompositorNodeMath');maximum2.operation='MAXIMUM';l.new(maximum.outputs[0],maximum2.inputs[0]);l.new(separate.outputs['Blue'],maximum2.inputs[1]);denom=n.new('CompositorNodeMath');denom.operation='ADD';denom.inputs[1].default_value=1;l.new(maximum2.outputs[0],denom.inputs[0]);combine=n.new('CompositorNodeCombineColor');combine.mode='RGB'
 for channel in ['Red','Green','Blue']:
  div=n.new('CompositorNodeMath');div.operation='DIVIDE';l.new(separate.outputs[channel],div.inputs[0]);l.new(denom.outputs[0],div.inputs[1]);l.new(div.outputs[0],combine.inputs[channel])
 mask=n.new('CompositorNodeIDMask');mask.index=1;mask.use_antialiasing=True;l.new(render.outputs['IndexOB'],mask.inputs[0]);mix=n.new('CompositorNodeMixRGB');l.new(mask.outputs['Alpha'],mix.inputs[0]);l.new(render.outputs['Image'],mix.inputs[1]);l.new(combine.outputs['Image'],mix.inputs[2]);final=n.new('CompositorNodeComposite');l.new(mix.outputs[0],final.inputs[0])
 for name,position,power,color,size in [('Overcast river light',(-2,2.5,6),100,(.72,.84,1),4),('Cabin warmth reflected in foreground water',(-5.4,-4.8,2.2),80,(1,.34,.08),1.3)]:
  light=bpy.data.lights.new(name,'AREA');light.energy=power;light.color=color;light.shape='DISK';light.size=size;ob=bpy.data.objects.new(name,light);s.collection.objects.link(ob);ob.location=position;ob.rotation_euler=(Vector((1.2,3,.5))-ob.location).to_track_quat('-Z','Y').to_euler()
 s['method']='Calibrated 3D PBF river and foam integrated into the approved photographic cabin/palm hybrid';s['water_motion_from_images_or_footage']=False;s['background_generated_matte']=True;s['camera_locked']=True;s['standalone_water_test']=False
 text=bpy.data.texts.new('ENABLE_INTEGRATED_FLUID_PLAYBACK.py');text.write("import bpy,sys\nfrom pathlib import Path\nroot=Path(bpy.data.filepath).parent\nsys.path.insert(0,str(root/'scripts'))\nfrom integrated_fluid_scene import load_frame\ndef integrated_fluid_update(scene): load_frame(max(1,min(scene.frame_end,scene.frame_current)))\nfor h in list(bpy.app.handlers.frame_change_pre):\n    if h.__name__=='integrated_fluid_update': bpy.app.handlers.frame_change_pre.remove(h)\nbpy.app.handlers.frame_change_pre.append(integrated_fluid_update)\nintegrated_fluid_update(bpy.context.scene)\n")
 for image in bpy.data.images:
  if image.source=='FILE' and not image.packed_file:image.filepath=bpy.path.relpath(image.filepath,start=str(ROOT))
 s.render.filepath=f'//renders/{VARIANT}/still.png';s.frame_set(1)
 if VARIANT=='integrated_fluid':bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'rainforest_integrated_fluid.blend'),compress=True)
 return s
def main():
 status('building_integrated_fluid_scene');s=setup();frame=int(os.environ.get('TEST_FRAME','24'));s.frame_set(frame);counts=load_frame(frame);s.render.filepath=str(OUT/'diagnostic.png')
 if os.environ.get('CROP'):
  s.render.use_border=True;s.render.use_crop_to_border=True;s.render.border_min_x=(720+.001)/1920;s.render.border_max_x=(1760+.001)/1920;s.render.border_min_y=0;s.render.border_max_y=(400+.001)/1080
 status('rendering_integrated_diagnostic',frame=frame,geometry_counts=counts);bpy.ops.render.render(write_still=True);status('complete',output='renders/integrated_fluid/diagnostic.png')
if __name__=='__main__':
 try:main()
 except BaseException as e:traceback.print_exc();status('failed',error=str(e));os._exit(1)
 os._exit(0)
