"""Validate actual 3D geometry motion, solid contacts and rendered delivery."""
import hashlib,json,subprocess,zipfile
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'renders/fluid_river';CACHE=ROOT/'assets/fluid_river/meshes'
sim=json.loads((ROOT/'research/fluid_river/simulation.json').read_text());report=json.loads((OUT/'render_report.json').read_text())
assert sim['particles']==51286 and sim['geometry_from_simulated_particles'] and not sim['image_or_stock_footage_motion']
mesh_hashes=[];contacts=[];rocks=np.array(sim['solid_ellipsoids'])
for frame in range(1,49):
 mesh=np.load(CACHE/f'liquid_{frame:04d}.npz');vertices=mesh['vertices'];faces=mesh['faces'];assert np.isfinite(vertices).all() and len(vertices)>80000 and len(faces)>150000
 assert faces.min()>=0 and faces.max()<len(vertices)
 mesh_hashes.append(hashlib.sha256(vertices.tobytes()+faces.tobytes()).hexdigest())
assert len(set(mesh_hashes))==48
for frame in [1,24,48]:
 f=np.load(CACHE/f'particles_{frame:04d}.npz');p=f['positions'];v=f['velocity'];assert p.shape==(51286,3) and np.isfinite(p).all() and np.isfinite(v).all();y=p[:,1]
 def drop(a,b):
  t=np.clip((y-a)/(b-a),0,1);return 1-t*t*(3-2*t)
 floor=.18+.37*drop(1.35,1.7)+.28*drop(2.55,2.8)+.24*drop(3.7,4)+3*np.maximum(0,np.abs(p[:,0]-1.2)-.76)**2
 penetration=float(np.maximum(0,floor-p[:,2]).max());rock_distance=float(min(np.linalg.norm((p-r[:3])/(r[3:]+.021),axis=1).min() for r in rocks))
 assert penetration<1e-5 and rock_distance>.9999
 contacts.append({'frame':frame,'particles':len(p),'maximum_bed_penetration_m':penetration,'minimum_normalized_rock_distance':rock_distance,'mean_downstream_velocity_m_s':float(v[:,1].mean())})
 assert float(v[:,1].mean())>.3
movie=OUT/'preview.mp4';probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(movie)]));s=next(x for x in probe['streams'] if x['codec_type']=='video')
assert s['nb_read_frames']=='48' and s['r_frame_rate']=='24/1' and (s['width'],s['height'])==(960,540) and float(probe['format']['duration'])==2
assert not any(x['codec_type']=='audio' for x in probe['streams']);subprocess.run(['ffmpeg','-v','error','-i',str(movie),'-f','null','-'],check=True)
decoded=subprocess.check_output(['ffmpeg','-v','error','-i',str(movie),'-f','framemd5','-'],text=True);hashes=[line.rsplit(',',1)[-1].strip() for line in decoded.splitlines() if line and not line.startswith('#')];assert len(hashes)==48 and len(set(hashes))==48
manifest=json.loads((ROOT/'assets/fluid_river/cache_manifest.json').read_text())
for name in set(x['archive'] for x in manifest['archives']):
 with zipfile.ZipFile(ROOT/'assets/fluid_river'/name) as archive:
  assert archive.testzip() is None
  for x in [r for r in manifest['archives'] if r['archive']==name]:assert hashlib.sha256(archive.read(x['file'])).hexdigest()==x['sha256']
qa={'distinct_simulated_geometry_frames':len(set(mesh_hashes)),'distinct_decoded_video_frames':len(set(hashes)),'solid_contact_checks':contacts,'resolution':[960,540],'fps':24,'frames':48,'duration_seconds':2,'decoded_cleanly':True,'cache_archives_verified':True,
    'water_motion_from_images_or_footage':False,'no_frame_interpolation':True,'standalone_physics_study':True,'integrated_into_approved_cabin_scene':False,'photorealism_approved':False,
    'limits':['coarse particle/mesh resolution remains visible','test rocks and channel are not the final photographed creek geometry','foam is empirical, not a two-phase air/water simulation','not a seamless loop'],
    'preview_sha256':hashlib.sha256(movie.read_bytes()).hexdigest()}
(OUT/'qa.json').write_text(json.dumps(qa,indent=2));print(json.dumps(qa,indent=2))
