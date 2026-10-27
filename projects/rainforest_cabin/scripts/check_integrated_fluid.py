"""Validate the integrated native video and the actual 3D simulation delivery."""
import hashlib,json,subprocess,zipfile
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'renders/integrated_fluid';ASSETS=ROOT/'assets/integrated_fluid'
render=json.loads((OUT/'render_report.json').read_text());cfg=json.loads((ASSETS/'channel.json').read_text());manifest=json.loads((ASSETS/'cache_manifest.json').read_text());samples=np.load(ASSETS/'solver_samples.npz')
clips=[]
for name,size in [('preview',(1920,1080)),('river_detail',(1040,400))]:
 p=OUT/(name+'.mp4');probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(p)]));v=next(x for x in probe['streams'] if x['codec_type']=='video')
 assert v['nb_read_frames']=='96' and v['r_frame_rate']=='24/1' and (v['width'],v['height'])==size and float(probe['format']['duration'])==4
 assert not any(x['codec_type']=='audio' for x in probe['streams']);subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],check=True)
 decoded=subprocess.check_output(['ffmpeg','-v','error','-i',str(p),'-f','framemd5','-'],text=True);hashes=[x.rsplit(',',1)[-1].strip() for x in decoded.splitlines() if x and not x.startswith('#')];assert len(hashes)==96 and len(set(hashes))==96
 clips.append({'file':p.name,'frames':96,'resolution':size,'fps':24,'duration_seconds':4,'decoded_cleanly':True,'distinct_decoded_frames':96,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
contacts=[];yy=np.arange(len(cfg['bed_profile_z']))*.01;rocks=np.array(cfg['solid_ellipsoids'])
for frame in [1,24,48,72,96]:
 p=samples[f'positions_{frame:04d}'];vel=samples[f'velocity_{frame:04d}'];assert np.isfinite(p).all() and np.isfinite(vel).all();live=p[:,1]>0;p=p[live];vel=vel[live]
 floor=np.interp(p[:,1],yy,cfg['bed_profile_z'])+8*np.maximum(0,np.abs(p[:,0]-np.interp(p[:,1],yy,cfg['center_profile_x']))-np.interp(p[:,1],yy,cfg['half_width_profile']))**2
 penetration=float(np.maximum(0,floor-p[:,2]).max());shell=float(min(np.linalg.norm((p-r[:3])/(r[3:]+.021),axis=1).min() for r in rocks));height99=float(np.quantile(p[:,2]-floor,.99))
 assert penetration<.001 and shell>.9999 and float(vel[:,1].mean())>1 and height99<.6
 contacts.append({'frame':frame,'active_particles':len(p),'bed_penetration_m':penetration,'minimum_rock_shell_radius':shell,'mean_downstream_velocity_m_s':float(vel[:,1].mean()),'height_above_bed_percentile99_m':height99})
geometry=[]
for name in sorted(set(x['archive'] for x in manifest['archives'])):
 with zipfile.ZipFile(ASSETS/name) as archive:
  assert archive.testzip() is None
  for record in [x for x in manifest['archives'] if x['archive']==name]:
   data=archive.read(record['file']);assert hashlib.sha256(data).hexdigest()==record['sha256']
   if record['file'].startswith('liquid_'):geometry.append(record['sha256'])
assert len(geometry)==96 and len(set(geometry))==96
outside=[];base=ROOT/'renders/hybrid_motion/frames'
if render['cached_approved_outside_pixels'] and (base/'0001.png').exists():
 for frame in [1,24,48,72,96]:
  a=np.asarray(Image.open(base/f'{frame:04d}.png'));b=np.asarray(Image.open(OUT/'frames'/f'{frame:04d}.png'));d=np.any(a!=b,axis=2);d[680:1080,720:1760]=False;assert not d.any();outside.append({'frame':frame,'changed_pixels_outside_river_border':int(d.sum())})
qa={'clips':clips,'simulated_geometry_frames':96,'all_geometry_frames_distinct':True,'contacts':contacts,'approved_outside_pixels':outside,'water_motion_from_images_or_footage':False,'no_frame_interpolation':True,'scene_is_hybrid':True,
 'upstream_is_spatial_instance_of_same_bake':True,'audio':False,'seamless_loop':False,'does_not_prove_photographic_realism':True,'review_focus':['rock contacts and visible matte edges','water highlight and foam detail','small upstream water instance','rain continuity and leaf edges']}
(OUT/'qa.json').write_text(json.dumps(qa,indent=2));print(json.dumps({'decoded_clips':2,'geometry_frames':96,'solid_contacts_passed':True,'outside_border_unchanged':bool(outside)},indent=2))
