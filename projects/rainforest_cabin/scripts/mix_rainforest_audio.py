"""Continuous, spatially restrained rain/stream mix for the approved cabin loop.

Only licensed source audio supplies sound. No generated noise or artificial
thunder is added. Source screening is technical; user audition remains required.
"""
import hashlib,json,math,os,re,subprocess,time
from pathlib import Path
import numpy as np
from scipy.signal import butter,sosfiltfilt
from scipy.ndimage import median_filter,gaussian_filter1d
from prepare_ambience_audio import decode

ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'renders/audiovisual';WORK=OUT/'work';WORK.mkdir(parents=True,exist_ok=True)
SR=48000;DURATION=60;COUNT=SR*DURATION

def status(phase,**extra):
    d={'phase':phase,'worker_running':phase not in ['complete','failed'],'pid':os.getpid(),
        'updated_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'variant':'rainforest_audio_preview',**extra}
    for p in [ROOT/'status.json',OUT/'status.json']:p.write_text(json.dumps(d,indent=2))
    print(json.dumps(d),flush=True)

def write_audio(path,x,codec='flac'):
    subprocess.run(['ffmpeg','-y','-v','error','-f','f32le','-ar',str(SR),'-ac','2','-i','-',
        '-c:a',codec,'-sample_fmt','s32',str(path)],input=x.astype(np.float32).tobytes(),check=True)

def loudness(path):
    result=subprocess.run(['ffmpeg','-hide_banner','-i',str(path),'-af','loudnorm=I=-24:TP=-2:LRA=7:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
    return json.loads(re.findall(r'\{[^{}]+\}',result.stderr)[-1])

def tame(x,ratio):
    hop=960;blocks=len(x)//hop
    level=np.sqrt(np.mean(x[:blocks*hop].reshape(blocks,hop,2)**2,axis=(1,2)))
    reference=median_filter(level,size=251,mode='nearest')
    gain=np.minimum(1,ratio*reference/np.maximum(level,1e-8))
    # Smooth attenuation across natural splashes; no cuts or moving source edits.
    gain=gaussian_filter1d(gain,3)
    smooth=np.interp(np.arange(len(x)),np.arange(blocks)*hop+hop/2,gain).astype(np.float32)
    return x*smooth[:,None],float(smooth.min())

def spatial(x,width,pan):
    mid=x.mean(axis=1);side=(x[:,0]-x[:,1])*.5*width
    y=np.stack([mid+side,mid-side],axis=1)
    y*=np.array([math.cos((pan+1)*math.pi/4),math.sin((pan+1)*math.pi/4)],np.float32)*math.sqrt(2)
    return y

def target_stem(x,target,name):
    path=WORK/(name+'_measurement.flac');write_audio(path,x);m=loudness(path)
    gain_db=target-float(m['input_i']);x=x*10**(gain_db/20)
    return x,{'target_integrated_lufs':target,'input_integrated_lufs':float(m['input_i']),'gain_db':gain_db}

def main():
    status('mixing_continuous_rain_and_stream')
    screening=json.loads((ROOT/'research/audio/signal_screening.json').read_text())
    sources=json.loads((ROOT/'assets/audio/sources.json').read_text());stems={};settings=[]
    for name,target,width,pan,hp,lp in [('rain',-26,.95,0,110,6500),('stream',-31,.55,.23,150,5800)]:
        info=next(x for x in screening['sources'] if x['source']==name);start=info['suggested_continuous_minute_start']
        x=decode(ROOT/f'assets/audio/{name}_source.flac',start,DURATION,sr=SR)[:COUNT]
        assert len(x)==COUNT
        x=sosfiltfilt(butter(3,[hp,lp],btype='bandpass',fs=SR,output='sos'),x,axis=0).astype(np.float32)
        band=sosfiltfilt(butter(2,[650,2400],btype='bandpass',fs=SR,output='sos'),x,axis=0).astype(np.float32)
        tamed_band,band_min=tame(band,1.25);x=x-band+tamed_band;x,wide_min=tame(x,1.6)
        x=spatial(x,width,pan);x,level=target_stem(x,target,name);stems[name]=x
        source=next(s for s in sources if s['name']==name)
        settings.append({'source':name,'prepared_start_seconds':start,'original_start_seconds':source['prepared_source_start_seconds']+start,
            'duration_seconds':DURATION,'highpass_hz':hp,'lowpass_hz':lp,'stereo_width':width,'pan':pan,
            'minimum_band_gain':band_min,'minimum_broadband_gain':wide_min,**level})
    mix=stems['rain']+stems['stream']
    fade_in=int(.75*SR);fade_out=int(1.5*SR)
    envelope=np.ones(COUNT,np.float32);envelope[:fade_in]=np.sin(np.linspace(0,np.pi/2,fade_in))**2
    envelope[-fade_out:]=np.cos(np.linspace(0,np.pi/2,fade_out))**2
    mix*=envelope[:,None]
    pre=WORK/'pre_normalization.flac';write_audio(pre,mix);measured=loudness(pre)
    gain_db=-24-float(measured['input_i']);gain=10**(gain_db/20);mix*=gain
    # Leave 2 dB true-peak headroom. Use a limiter only if measured gain needs it.
    projected_peak=float(measured['input_tp'])+gain_db;limited=projected_peak>-2
    final=OUT/'soundtrack.flac'
    if limited:
        temporary=WORK/'gain_adjusted.flac';write_audio(temporary,mix)
        subprocess.run(['ffmpeg','-y','-v','error','-i',str(temporary),'-af','alimiter=limit=0.76:level=false','-c:a','flac',str(final)],check=True)
    else:write_audio(final,mix)
    for name,stem in stems.items():write_audio(OUT/(name+'_solo.flac'),stem*gain*envelope[:,None])
    final_measure=loudness(final)
    report={'duration_seconds':DURATION,'sample_rate':SR,'channels':2,'target_integrated_lufs':-24,
        'final_integrated_lufs':float(final_measure['input_i']),'final_true_peak_dbfs':float(final_measure['input_tp']),
        'loudness_range_lu':float(final_measure['input_lra']),'final_gain_db':gain_db,'limiter_used':limited,
        'fade_in_seconds':.75,'fade_out_seconds':1.5,'stems':settings,
        'continuous_source_excerpts_not_12_second_audio_loop':True,'music':False,'added_thunder':False,
        'added_wildlife':False,'artificial_rain_noise':False,'original_source_geography_matches_reference':False,
        'listening_review':'Pending user audition; numerical/spectral checks do not certify absence of unwanted content',
        'soundtrack_sha256':hashlib.sha256(final.read_bytes()).hexdigest()}
    (OUT/'mix_report.json').write_text(json.dumps(report,indent=2))
    status('muxing_audiovisual_review',audio_integrated_lufs=report['final_integrated_lufs'])
    visual=ROOT/'renders/looped_fluid/preview.mp4'
    subprocess.run(['ffmpeg','-y','-v','error','-stream_loop','4','-i',str(visual),'-i',str(final),'-map','0:v:0','-map','1:a:0',
        '-t','60','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000','-movflags','+faststart',str(OUT/'preview.mp4')],check=True)
    # A lighter twelve-second link uses the same mix and original video stream.
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(visual),'-i',str(final),'-map','0:v:0','-map','1:a:0',
        '-t','12','-c:v','copy','-af','afade=t=out:st=11:d=1','-c:a','aac','-b:a','256k','-ar','48000',
        '-movflags','+faststart',str(OUT/'quick_preview.mp4')],check=True)
    status('audio_mix_complete_awaiting_delivery_checks',worker_running=False,output='renders/audiovisual/preview.mp4')

if __name__=='__main__':main()
