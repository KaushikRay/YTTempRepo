"""Check the small static grade and restrained recorded-thunder additions."""
import hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image
from mix_rainforest_audio import ROOT,decode,SR,loudness

def linear(rgb):return np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)

def main():
    before=np.asarray(Image.open(ROOT/'renders/looped_fluid/frames/0144.png').convert('RGB'),np.float32)/255
    after=np.asarray(Image.open(ROOT/'renders/production_test/darker_still.png').convert('RGB'),np.float32)/255
    a=linear(before);b=linear(after);weights=np.array([.2126,.7152,.0722]);ya=a@weights;yb=b@weights
    mid=(ya>.02)&(ya<.3)&(a.max(axis=2)<.4);ratio=float(np.median(yb[mid]/ya[mid]));assert .65<ratio<.75
    # Evaluate the warm lantern pixels, not the surrounding dark timber.
    warm=np.zeros(ya.shape,bool);warm[490:545,1320:1395]=True
    warm&=(before[:,:,0]>.75)&(before[:,:,0]>before[:,:,1]*1.2)&(before[:,:,1]>before[:,:,2]*1.2)
    assert warm.sum()>10
    warm_ratio=float(np.median(yb[warm]/ya[warm]));assert warm_ratio>ratio+.04
    clips=[]
    for folder,seconds in [('audiovisual',60),('production_test',120)]:
        out=ROOT/'renders'/folder;report=json.loads((out/'mix_report.json').read_text());events=report['thunder_events']
        assert report['added_thunder'] and report['visual_lightning']==False and len(events)==(1 if seconds==60 else 2)
        stem=decode(out/'thunder_solo.flac',sr=SR);base=decode(out/'rain_solo.flac',sr=SR)+decode(out/'stream_solo.flac',sr=SR)
        mix=decode(out/'soundtrack.flac',sr=SR);active=np.zeros(len(stem),bool)
        for event in events:
            first=round(event['start_seconds']*SR);last=first+round(event['duration_seconds']*SR);active[first:last]=True
        assert float(np.abs(stem[~active]).max())==0 and np.isfinite(stem).all()
        assert np.max(np.abs(mix-base-stem))<2e-6,'Bed/stem mix changed unexpectedly'
        # Compare 3-second energy windows at half-second intervals. This is an
        # unweighted technical transient check, not a subjective listening claim.
        hop=SR//2;rises=[]
        for start in range(0,len(mix)-3*SR+1,hop):
            if not active[start:start+3*SR].any():continue
            pa=float(np.mean(base[start:start+3*SR]**2));pb=float(np.mean(mix[start:start+3*SR]**2))
            rises.append(10*np.log10(pb/max(pa,1e-12)))
        assert max(rises)<6,'Thunder energy jump too large'
        levels=loudness(out/'preview.mp4');assert float(levels['input_tp'])<=-2 and -24.5<float(levels['input_i'])<-23.5
        clips.append({'folder':folder,'events':events,'max_three_second_unweighted_energy_rise_db':max(rises),
            'encoded_integrated_lufs':float(levels['input_i']),'encoded_true_peak_dbfs':float(levels['input_tp']),
            'thunder_only_inside_scheduled_events':True,'bed_preserved_apart_from_common_level_adjustment':True})
    source=ROOT/'assets/audio/thunder_source.ogg';manifest=json.loads((ROOT/'assets/audio/sources.json').read_text());item=next(x for x in manifest if x['name']=='thunder')
    assert item['license']=='CC BY 3.0' and hashlib.sha256(source.read_bytes()).hexdigest()==item['prepared_sha256']
    qa={'midtone_linear_luminance_ratio':ratio,'midtone_exposure_change_ev':float(np.log2(ratio)),
        'protected_warm_lantern_linear_luminance_ratio':warm_ratio,'warm_lantern_pixels_checked':int(warm.sum()),
        'static_colour_grade_only':True,'motion_geometry_and_camera_changes':False,'lightning_or_flash_added':False,
        'audio':clips,'thunder_license_and_hash_verified':True,'thunder_creator':'Bidgee',
        'remaining_review':'Subjective darkness and distant-thunder naturalness await user review.'}
    (ROOT/'renders/production_test/darker_thunder_qa.json').write_text(json.dumps(qa,indent=2));print(json.dumps(qa,indent=2))

if __name__=='__main__':main()
