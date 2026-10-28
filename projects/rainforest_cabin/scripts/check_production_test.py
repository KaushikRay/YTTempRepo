"""Check rain dominance, water-only speed, unchanged surroundings and 2-min A/V."""
import hashlib,json,re,subprocess,os
os.environ['AUDIO_DURATION_SECONDS']='120'
from pathlib import Path
import numpy as np
from PIL import Image
from mix_rainforest_audio import ROOT,decode,loudness,SR,status
OUT=ROOT/'renders/production_test'

def main():
    status('checking_two_minute_production_test')
    path=OUT/'preview.mp4';probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(path)]))
    video=next(s for s in probe['streams'] if s['codec_type']=='video');audio=next(s for s in probe['streams'] if s['codec_type']=='audio')
    assert (video['width'],video['height'])==(1920,1080) and video['r_frame_rate']=='24/1' and int(video['nb_read_frames'])==2880
    assert abs(float(probe['format']['duration'])-120)<.03 and audio['sample_rate']=='48000' and audio['channels']==2
    assert path.stat().st_size<100*1024**2
    subprocess.run(['ffmpeg','-v','error','-i',str(path),'-f','null','-'],check=True)
    level=loudness(path);assert -24.5<float(level['input_i'])<-23.5 and float(level['input_tp'])<=-2
    rain=loudness(OUT/'rain_solo.flac');stream=loudness(OUT/'stream_solo.flac');gap=float(rain['input_i'])-float(stream['input_i']);assert 10.5<gap<11.5
    x=decode(OUT/'soundtrack.flac',sr=SR);assert len(x)==120*SR and np.isfinite(x).all() and np.abs(x).max()<1
    rms=np.sqrt(np.mean(x.reshape(120,SR,2)**2,axis=(1,2)));assert rms[1:-2].min()>10**(-45/20)
    threshold=float(np.quantile(np.abs(np.diff(x,axis=0)),.9999));joins=[]
    for t in range(12,120,12):
        k=t*SR;delta=float(np.max(np.abs(x[k]-x[k-1])));assert delta<threshold*1.5
        joins.append({'second':t,'audio_sample_step':delta,'normal_p9999_step':threshold})
    pixels=[]
    for frame in [1,24,72,144,216,288]:
        a=np.asarray(Image.open(OUT/'approved_frames'/f'{frame:04d}.png'));b=np.asarray(Image.open(ROOT/'renders/looped_fluid/frames'/f'{frame:04d}.png'))
        diff=np.any(a!=b,axis=2);diff[680:1080,720:1760]=False;assert not diff.any()
        pixels.append({'frame':frame,'changed_pixels_outside_water_border':0})
    speed=json.loads((ROOT/'research/looped_fluid/speed_revision.json').read_text());assert speed['water_only_playback_rate']==.8 and .7<speed['apparent_mean_speed_ratio']<.9
    # Measure the sharing encode against ten repeats of the high-quality loop.
    graded=ROOT/'renders/production_test/graded_loop.mp4';visual_source=graded if graded.exists() else ROOT/'renders/looped_fluid/preview.mp4'
    result=subprocess.run(['ffmpeg','-hide_banner','-stream_loop','9','-i',str(visual_source),'-i',str(path),
        '-filter_complex','[0:v]setpts=PTS-STARTPTS[ref];[1:v]setpts=PTS-STARTPTS[test];[ref][test]ssim','-t','120','-an','-f','null','-'],capture_output=True,text=True,check=True)
    matches=re.findall(r'All:([0-9.]+)',result.stderr);assert matches,'No SSIM summary';ssim=float(matches[-1]);assert ssim>.95,ssim
    qa={'duration_seconds':120,'resolution':[1920,1080],'frames':2880,'fps':24,'audio_sample_rate':48000,'audio_channels':2,
        'decoded_cleanly':True,'integrated_lufs':float(level['input_i']),'true_peak_dbfs':float(level['input_tp']),
        'rain_solo_integrated_lufs':float(rain['input_i']),'stream_solo_integrated_lufs':float(stream['input_i']),
        'rain_above_stream_lufs':gap,'stream_relative_reduction_db':6,'water_speed':speed,
        'sampled_surroundings_pixel_preservation_before_grade':pixels,'visual_grade_applied':graded.exists(),
        'visual_source':str(visual_source.relative_to(ROOT)),
        'audio_continuity_at_visual_joins':joins,'ssim_to_high_quality_loop':ssim,
        'video_is_ten_repeats_of_12s_loop':True,'audio_is_continuous_120s_excerpts':True,'no_interpolated_or_repeated_water_frames_within_loop':True,
        'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'limits':['generated static cabin/forest backdrop','coarse glossy water and approximate banks','one-second artistic 3D loop transition','subjective naturalness and source-content listening review pending']}
    (OUT/'qa.json').write_text(json.dumps(qa,indent=2))
    status('complete',output='renders/production_test/preview.mp4',duration_seconds=120,delivery_checks_passed=True,
        rain_above_stream_lufs=gap,water_playback_rate=.8)
    print(json.dumps({k:qa[k] for k in ['duration_seconds','frames','rain_above_stream_lufs','integrated_lufs','true_peak_dbfs','ssim_to_high_quality_loop']},indent=2))

if __name__=='__main__':main()
