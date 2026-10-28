"""Decode all delivery clips, verify cache integrity, contacts and join motion."""
import hashlib,io,json,subprocess,zipfile
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.spatial import cKDTree
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'renders/looped_fluid';ASSETS=ROOT/'assets/looped_fluid'

def main():
    clips=[]
    for name,frames,size in [('preview',288,(1920,1080)),('river_detail',288,(1040,400)),('repeat_test',576,(1920,1080))]:
        path=OUT/(name+'.mp4');probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(path)]));v=next(x for x in probe['streams'] if x['codec_type']=='video')
        assert int(v['nb_read_frames'])==frames and v['r_frame_rate']=='24/1' and (v['width'],v['height'])==size
        assert abs(float(probe['format']['duration'])-frames/24)<.002 and not any(x['codec_type']=='audio' for x in probe['streams'])
        decoded=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-f','framemd5','-'],text=True)
        hashes=[line.rsplit(',',1)[-1].strip() for line in decoded.splitlines() if line and not line.startswith('#')]
        assert len(hashes)==frames and len(set(hashes))==288
        if name=='repeat_test':assert hashes[:288]==hashes[288:],'Second repeat does not decode identically'
        clips.append({'file':path.name,'frames':frames,'resolution':size,'duration_seconds':frames/24,'fps':24,'audio':False,'decoded_cleanly':True,'distinct_decoded_frames':len(set(hashes)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    manifest=json.loads((ASSETS/'cache_manifest.json').read_text());geometry=[];states={}
    for name in sorted(set(r['archive'] for r in manifest['archives'])):
        with zipfile.ZipFile(ASSETS/name) as archive:
            assert archive.testzip() is None
            for record in [r for r in manifest['archives'] if r['archive']==name]:
                data=archive.read(record['file']);assert hashlib.sha256(data).hexdigest()==record['sha256']
                if record['file'].startswith('liquid_'):
                    geometry.append(record['sha256']);frame=int(record['file'][7:11])
                    if frame in [1,2,23,24,25,26,287,288]:states[frame]=np.load(io.BytesIO(data))['vertices']
    assert len(geometry)==288 and len(set(geometry))==288
    contacts=[];cfg=json.loads((ASSETS/'channel.json').read_text());yy=np.arange(len(cfg['bed_profile_z']))*.01;rocks=np.array(cfg['solid_ellipsoids']);samples=np.load(ASSETS/'solver_samples.npz')
    for frame in [1,24,144,264,288,312]:
        p=samples[f'positions_{frame:04d}'];v=samples[f'velocity_{frame:04d}'];assert np.isfinite(p).all() and np.isfinite(v).all();live=p[:,1]>0;p=p[live];v=v[live]
        bed=np.interp(p[:,1],yy,cfg['bed_profile_z'])+8*np.maximum(0,np.abs(p[:,0]-np.interp(p[:,1],yy,cfg['center_profile_x']))-np.interp(p[:,1],yy,cfg['half_width_profile']))**2
        penetration=float(np.maximum(0,bed-p[:,2]).max());shell=float(min(np.linalg.norm((p-r[:3])/(r[3:]+.021),axis=1).min() for r in rocks))
        assert penetration<.001 and shell>.9999 and float(v[:,1].mean())>1
        contacts.append({'frame':frame,'active_particles':len(p),'bed_penetration_m':penetration,'minimum_rock_shell_radius':shell,'mean_downstream_velocity_m_s':float(v[:,1].mean())})
    pairs=[(287,288),(288,1),(1,2),(23,24),(24,25),(25,26)];joins=[]
    for a,b in pairs:
        va=states[a][::5];vb=states[b][::5];dist=np.concatenate([cKDTree(va).query(vb)[0],cKDTree(vb).query(va)[0]])
        ia=np.asarray(Image.open(OUT/'frames'/f'{a:04d}.png'),dtype=np.float32);ib=np.asarray(Image.open(OUT/'frames'/f'{b:04d}.png'),dtype=np.float32)
        diff=np.abs(ia-ib);water=diff[680:1080,720:1760]
        joins.append({'from':a,'to':b,'symmetric_surface_distance_mean_m':float(dist.mean()),'pixel_mae_full':float(diff.mean()),'pixel_mae_river':float(water.mean()),'river_pixel_delta_p99':float(np.quantile(water,.99))})
    ordinary=max(x['pixel_mae_river'] for x in joins if x['from']!=288);seam=next(x for x in joins if x['from']==288)
    assert seam['pixel_mae_river']<ordinary*2,'River seam is a motion outlier; inspect before publication'
    qa={'clips':clips,'simulated_geometry_states':288,'all_geometry_states_distinct':True,'cache_sha256_verified':True,'solver_contacts':contacts,'joins':joins,
        'repeat_point_river_mae_ratio_to_largest_sampled_normal_step':seam['pixel_mae_river']/ordinary,
        'loop_conditioning_in_3D_not_image_dissolve':True,'periodic_physics_solution':False,
        'reference_gaps':['static generated cabin and distant forest','approximate camera-projected bank contacts','coarse 3D water and empirical foam','one-second artistic surface transition needs visual review'],
        'does_not_prove_photographic_realism_or_invisible_seam':True}
    (OUT/'qa.json').write_text(json.dumps(qa,indent=2));print(json.dumps({'clips_decoded':3,'geometry_states':288,'solid_contacts_passed':True,'repeat_step_ratio':qa['repeat_point_river_mae_ratio_to_largest_sampled_normal_step']},indent=2))

if __name__=='__main__':main()
