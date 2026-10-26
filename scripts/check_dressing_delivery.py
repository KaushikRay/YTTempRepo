"""Artifact and driver checks for the detailed dressing/motion pass."""
import bpy,json,os,hashlib,subprocess
from pathlib import Path
r=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(r/'dressing_motion.blend'));s=bpy.context.scene
missing=[];libraries=[]
for lib in bpy.data.libraries:
 p=Path(bpy.path.abspath(lib.filepath));libraries.append(str(p.relative_to(r)))
 if not p.is_file():missing.append(str(p))
for im in bpy.data.images:
 if im.users and im.source in ['FILE','MOVIE'] and not im.packed_file:
  p=Path(bpy.path.abspath(im.filepath,library=im.library))
  if not p.is_file():missing.append(str(p))
assert not missing,missing
fuel=[];s.frame_set(1);dep=bpy.context.evaluated_depsgraph_get()
from mathutils import Vector
for name in ['Grounded charred fuel 0','Grounded charred fuel 1']:
 points=[]
 for item in dep.object_instances:
  if item.is_instance and item.parent and item.parent.original.name==name and item.object.type=='MESH':points.extend(item.matrix_world@v.co for v in item.object.data.vertices)
 assert points
 lo=[min(p[i] for p in points) for i in range(3)];hi=[max(p[i] for p in points) for i in range(3)]
 assert abs(lo[2]-.3)<.002 and abs(hi[2]-.58)<.002 and lo[0]>4.5 and hi[0]<5.7 and lo[1]>=2 and hi[1]<=4.5,(lo,hi)
 fuel.append({'name':name,'min':lo,'max':hi})
rain=[o for o in bpy.data.objects if o.name.startswith('Recycling rain ')]
assert len(rain)==2800
counts=[]
for frame in [1,12,24,36,48,96,144]:
 s.frame_set(frame);dep=bpy.context.evaluated_depsgraph_get();count=0
 for ob in rain:
  x,y,z=ob.evaluated_get(dep).location;cx=-2.2 if int(ob.name.rsplit(' ',1)[1])<1400 else .1
  count+=3.8<z<5.6 and abs(x-cx)<.9
 counts.append({'frame':frame,'upper_rectangular_aperture_population':count})
for event in bpy.data.objects:
 if 'lightning' in event.name.lower():
  assert (event.data.energy==0 if event.type=='LIGHT' else event.hide_render),event.name
values=[c['upper_rectangular_aperture_population'] for c in counts];assert min(values)/max(values)>.7
assert s.render.resolution_x==1280 and s.cycles.samples==96
for path in ['dressing_motion.blend','assets/dressing/dressing.blend']:assert (r/path).stat().st_size<100*1024*1024
for path in ['storm_lounge.blend','realism_study.blend']:
 actual=subprocess.check_output(['git','-C',str(r),'hash-object',path],text=True).strip();previous=subprocess.check_output(['git','-C',str(r),'rev-parse','FETCH_HEAD:'+path],text=True).strip();assert actual==previous,path
movie=r/'renders/dressing_motion/preview.mp4';probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(movie)]))
video=next(x for x in probe['streams'] if x['codec_type']=='video');assert video['nb_read_frames']=='48' and video['r_frame_rate']=='24/1' and abs(float(probe['format']['duration'])-2)<.01
subprocess.run(['ffmpeg','-v','error','-i',str(movie),'-f','null','-'],check=True)
report={'fuel_evaluated_geometry_bounds':fuel,'missing_files':missing,'linked_libraries':libraries,'rendered_frames':48,'fps':24,'duration_seconds':2,'upper_window_actual_driver_checks':counts,'source_storm_and_realism_scenes_preserved':True,'seamless_loop':False,'audio':False,'photorealism_target_reached':False,'preview_sha256':hashlib.sha256(movie.read_bytes()).hexdigest()}
(r/'renders/dressing_motion/qa.json').write_text(json.dumps(report,indent=2));print(json.dumps(report),flush=True);os._exit(0)
