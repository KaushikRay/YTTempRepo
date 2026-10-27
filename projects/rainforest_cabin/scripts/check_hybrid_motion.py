"""Meaningful output checks for this layered motion test, not a realism claim."""
from pathlib import Path
import hashlib, json, subprocess
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'renders/hybrid_motion'
qa=json.loads((OUT/'qa.json').read_text());assert qa['frames']==144 and qa['distinct_decoded_pixel_frames']==144
assert qa['native_frames_not_interpolated'] and not qa['audio'] and not qa['seamless_loop']
movie=OUT/'preview.mp4';assert hashlib.sha256(movie.read_bytes()).hexdigest()==qa['preview_sha256']
for name in ['preview','palms_detail','water_detail']:
    result=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(OUT/(name+'.mp4'))]))
    stream=next(s for s in result['streams'] if s['codec_type']=='video')
    assert stream['nb_read_frames']=='144' and stream['r_frame_rate']=='24/1' and float(result['format']['duration'])==6
    subprocess.run(['ffmpeg','-v','error','-i',str(OUT/(name+'.mp4')),'-f','null','-'],check=True)
frames=[np.asarray(Image.open(OUT/'frames'/f'{i:04d}.png').convert('RGB'),dtype=np.float32) for i in [1,37,73,109,144]]
regions={'sheltered_static_wall':(200,250,300,700),'foreground_palms':(1450,200,1870,780),'stream':(1050,900,1450,1070)}
changes={}
for name,(x0,y0,x1,y1) in regions.items():
    changes[name]=[round(float(np.abs(a[y0:y1,x0:x1]-frames[0][y0:y1,x0:x1]).mean()),5) for a in frames[1:]]
assert max(changes['sheltered_static_wall'])<.6,changes
assert max(changes['foreground_palms'])>1.,changes
assert max(changes['stream'])>.3,changes
means=[float(a.mean()) for a in frames]
assert max(means)-min(means)<.6,means
report={'decoded_all_three_clips':True,'native_sample_frames':[1,37,73,109,144],'mean_absolute_RGB_change_8bit_codes':changes,
        'sample_frame_mean_RGB':means,'maximum_sample_mean_change':max(means)-min(means),
        'does_not_prove_visual_realism':True,'manual_review_needed':['leaf edges while moving','frozen source water highlights','masked-flow coverage','rain legibility at normal playback'],
        'reference_comparison':'Approved generated still/composition in chat; original supplied reference unavailable as local file, no pixel-aligned comparison claimed'}
(OUT/'visual_checks.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
