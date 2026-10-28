"""Check delivered A/V timing, unchanged video packets, audio peaks and joins."""
import hashlib,json,subprocess
from pathlib import Path
import numpy as np
from mix_rainforest_audio import decode,loudness,status,ROOT,OUT,SR

def video_packets(path):
    report=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0',
        '-show_packets','-show_entries','packet=data_hash','-show_data_hash','sha256','-of','json',str(path)]))
    return [p['data_hash'] for p in report['packets']]

def main():
    status('checking_audiovisual_delivery')
    graded=ROOT/'renders/production_test/graded_loop.mp4'
    source=graded if graded.exists() else ROOT/'renders/looped_fluid/preview.mp4'
    original_packets=video_packets(source);assert len(original_packets)==288
    clips=[]
    for name,seconds,repeats in [('preview',60,5),('quick_preview',12,1)]:
        path=OUT/(name+'.mp4');info=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(path)]))
        v=next(s for s in info['streams'] if s['codec_type']=='video');a=next(s for s in info['streams'] if s['codec_type']=='audio')
        assert (v['width'],v['height'])==(1920,1080) and v['r_frame_rate']=='24/1' and int(v['nb_read_frames'])==seconds*24
        assert a['sample_rate']=='48000' and a['channels']==2 and a['codec_name']=='aac'
        assert abs(float(info['format']['duration'])-seconds)<.03
        assert video_packets(path)==original_packets*repeats,'Encoded picture changed or frames were dropped'
        subprocess.run(['ffmpeg','-v','error','-i',str(path),'-f','null','-'],check=True)
        measure=loudness(path);assert -24.5<float(measure['input_i'])<-23.5 and float(measure['input_tp'])<=-2
        clips.append({'file':path.name,'duration_seconds':seconds,'frames':seconds*24,'resolution':[1920,1080],'fps':24,
            'audio_codec':'aac','audio_sample_rate':48000,'audio_channels':2,'integrated_lufs':float(measure['input_i']),
            'true_peak_dbfs':float(measure['input_tp']),'decoded_cleanly':True,'video_packets_identical_to_visual_source':True,
            'visual_source':str(source.relative_to(ROOT)),
            'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    x=decode(OUT/'soundtrack.flac',sr=SR);assert len(x)==60*SR and np.isfinite(x).all() and np.abs(x).max()<1
    block=x.reshape(60,SR,2);rms=np.sqrt(np.mean(block**2,axis=(1,2)));assert rms[1:58].min()>10**(-45/20)
    delta=np.abs(np.diff(x,axis=0));normal=float(np.quantile(delta,.9999));joins=[]
    for second in [12,24,36,48]:
        i=second*SR;jump=float(np.max(np.abs(x[i]-x[i-1])));assert jump<normal*1.5
        before=float(np.sqrt(np.mean(x[i-SR//2:i]**2)));after=float(np.sqrt(np.mean(x[i:i+SR//2]**2)))
        joins.append({'second':second,'sample_step':jump,'p9999_normal_step':normal,'half_second_rms_change_db':20*np.log10(after/before)})
    mono=x.mean(axis=1);mono_ratio=float(10*np.log10(np.mean(mono**2)/np.mean(x**2)));assert mono_ratio>-8
    sources=json.loads((ROOT/'assets/audio/sources.json').read_text());assets=[]
    used={s.get('source_asset',s['source']) for s in json.loads((OUT/'mix_report.json').read_text())['stems']}
    for source in sources:
        if source['name'] not in used:continue
        path=ROOT/source['prepared_file'];assert hashlib.sha256(path.read_bytes()).hexdigest()==source['prepared_sha256']
        assert source['license'] in ['CC BY 3.0','CC0'];assets.append({'source':source['name'],'license':source['license'],'sha256_verified':True})
    qa={'clips':clips,'source_assets':assets,'soundtrack_samples_per_channel':len(x),'sample_rate':SR,
        'sample_peak_dbfs':float(20*np.log10(np.abs(x).max())),'dc_offset':x.mean(axis=0).tolist(),
        'rms_per_second_dbfs':(20*np.log10(np.maximum(rms,1e-10))).tolist(),'visual_loop_audio_continuity':joins,
        'mono_fold_down_power_difference_db':mono_ratio,'no_technical_dropouts_detected':True,
        'human_listening_review':'Pending user audition. Signal tests cannot certify naturalness or absence of unwanted semantic sounds.',
        'visual_limitations_unchanged':'Static generated cabin/forest and approximate glossy 3D water loop remain.'}
    (OUT/'qa.json').write_text(json.dumps(qa,indent=2))
    status('complete',output='renders/audiovisual/preview.mp4',duration_seconds=60,delivery_checks_passed=True,
        audio_integrated_lufs=clips[0]['integrated_lufs'],audio_true_peak_dbfs=clips[0]['true_peak_dbfs'])
    print(json.dumps({'clips_passed':2,'video_packets_unchanged':True,'audio_joins_passed':True,'loudness_lufs':clips[0]['integrated_lufs'],'true_peak_dbfs':clips[0]['true_peak_dbfs']}))

if __name__=='__main__':main()
