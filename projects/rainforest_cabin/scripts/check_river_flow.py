"""Check transport in rendered pixels, not merely nonzero frame differences."""
import hashlib,json,subprocess
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'renders/river_flow'

def track(folder,point,pairs,old=False):
    xx,yy,radius=point;x=round(xx*1920/1672)-720;y=round(yy*1080/941)-680;result=[]
    for af,bf in pairs:
        frames=[]
        for f in [af,bf]:
            a=np.asarray(Image.open(folder/f'{f:04d}.png'),dtype=np.float32)
            if old:a=a[680:1080,720:1760]
            frames.append(a.mean(2))
        a,b=frames;cut=a[y-radius:y+radius+1,x-radius:x+radius+1];cut=cut-cut.mean();norm=np.sqrt((cut*cut).sum());best=(-2,0,0)
        for dy in range(-10,11):
            for dx in range(-10,11):
                part=b[y-radius+dy:y+radius+1+dy,x-radius+dx:x+radius+1+dx];part=part-part.mean()
                score=float((cut*part).sum()/(norm*np.sqrt((part*part).sum())+1e-9))
                if score>best[0]:best=(score,dx,dy)
        result.append({'frames':[af,bf],'correlation':round(best[0],5),'dx_pixels':best[1],'dy_pixels':best[2]})
    return result

def main():
    render=json.loads((OUT/'render_report.json').read_text());assert render['frames']==144 and render['no_frame_interpolation']
    checks=[]
    for name,expected in [('preview',(1920,1080)),('water_detail',(720,300)),('water_comparison',(1440,300))]:
        path=OUT/(name+'.mp4');meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(path)]))
        v=next(s for s in meta['streams'] if s['codec_type']=='video')
        assert v['nb_read_frames']=='144' and v['r_frame_rate']=='24/1' and float(meta['format']['duration'])==6
        assert (v['width'],v['height'])==expected and not any(s['codec_type']=='audio' for s in meta['streams'])
        subprocess.run(['ffmpeg','-v','error','-i',str(path),'-f','null','-'],check=True)
        checks.append({'file':path.name,'frames':144,'duration_seconds':6,'resolution':expected,'decoded_cleanly':True,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    base=ROOT/'renders/hybrid_motion/frames';new=OUT/'frames'
    outside=[]
    if render['cached_approved_outside_pixels_used']:
        for f in [1,37,73,109,144]:
            a=np.asarray(Image.open(base/f'{f:04d}.png'));b=np.asarray(Image.open(new/f'{f:04d}.png'));d=np.any(a!=b,axis=2);d[680:1080,720:1760]=False
            count=int(d.sum());assert count==0,(f,count);outside.append({'frame':f,'changed_pixels_outside_border':count})
    pairs=[(1,4),(4,7),(7,10),(10,13),(49,52),(52,55),(97,100),(100,103)]
    fall=track(OUT/'crop_frames',(952,778,15),pairs) if render['cached_approved_outside_pixels_used'] else track(new,(952,778,15),pairs,True)
    pool=track(OUT/'crop_frames',(1125,911,18),pairs) if render['cached_approved_outside_pixels_used'] else track(new,(1125,911,18),pairs,True)
    fy=float(np.median([x['dy_pixels'] for x in fall]));px=float(np.median([x['dx_pixels'] for x in pool]));py=float(np.median([x['dy_pixels'] for x in pool]))
    assert fy>=2 and px>=3 and py>=1,{'falls':fall,'pool':pool}
    previous=None
    if (base/'0001.png').exists():
        previous=track(base,(1125,911,18),pairs,True)
        assert px>=float(np.median([x['dx_pixels'] for x in previous]))+2
    palm=json.loads((ROOT/'research/river_flow/palm_preservation.json').read_text())
    assert palm['palm_sha256_before']==palm['palm_sha256_after']=='0d9fd517e440e5e2c217f4a9d2b8573ddd9cda2b05794fbd2d12d5637b372e64'
    qa={'clips':checks,'approved_palm_data_identical':True,'outside_border_pixels':outside,'motion_tracking_interval_frames':3,
        'falls_downstream_tracking':fall,'foreground_pool_tracking':pool,'previous_pool_tracking':previous,
        'median_flow_per_three_frames':{'falls_down_pixels':fy,'pool_right_pixels':px,'pool_down_pixels':py},
        'scope':'Rendered-pixel template matching proves local travel in selected regions, not fluid accuracy or perceptual realism.',
        'manual_review_needed':['rock contacts','phase-crossfade ghosting','static bank highlights','repeating transported texture'],'audio':False,'seamless_loop':False}
    (OUT/'qa.json').write_text(json.dumps(qa,indent=2));print(json.dumps({'decoded_clips':3,'palm_data_identical':True,'median_flow_per_three_frames':qa['median_flow_per_three_frames']},indent=2))

if __name__=='__main__':main()
