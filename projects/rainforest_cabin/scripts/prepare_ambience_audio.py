"""Keep licensed source excerpts and inspect signal/spectral events.

This is technical source screening, not speech recognition or a listening pass.
The audiovisual review is the listening gate before a long release.
"""
import hashlib,json,subprocess,time
from pathlib import Path
import numpy as np
from scipy.ndimage import median_filter

ROOT=Path(__file__).resolve().parents[1];ASSETS=ROOT/'assets/audio';RESEARCH=ROOT/'research/audio'
SOURCES={'rain':('rain.oga',120,180),'stream':('stream.wav',0,68.88)}
if (ASSETS/'originals/long_stream.ogg').exists():SOURCES['long_stream']=('long_stream.ogg',60,180)

def decode(path,start=0,duration=None,sr=24000):
    args=['ffmpeg','-v','error','-ss',str(start),'-i',str(path)]
    if duration is not None:args+=['-t',str(duration)]
    return np.frombuffer(subprocess.check_output(args+['-ar',str(sr),'-ac','2','-f','f32le','-']),np.float32).reshape(-1,2).copy()

def inspect(path):
    path=Path(path).resolve()
    sr=24000;x=decode(path,sr=sr);assert np.isfinite(x).all();seconds=len(x)//sr
    windows=x[:seconds*sr].reshape(seconds,sr,2);rms=np.sqrt(np.mean(windows**2,axis=(1,2)))
    mono=windows.mean(axis=2);spectrum=np.abs(np.fft.rfft(mono*np.hanning(sr),axis=1))**2
    hz=np.fft.rfftfreq(sr,1/sr);bands={}
    for name,lo,hi in [('low_25_200',25,200),('mid_500_4000',500,4000),('high_4000_7500',4000,7500)]:
        power=spectrum[:,(hz>=lo)&(hz<hi)].sum(axis=1);bands[name]=(10*np.log10(np.maximum(power,1e-12))).tolist()
    interest=spectrum[:,(hz>=650)&(hz<=6500)]
    # Narrow-band peaks are only review candidates: water itself can be tonal.
    groups=interest[:,:interest.shape[1]//16*16].reshape(seconds,-1,16).mean(axis=2)
    peak_ratio=groups.max(axis=1)/np.maximum(np.median(groups,axis=1),1e-12)
    baseline=median_filter(rms,size=11,mode='nearest');spikes=np.flatnonzero(rms>np.maximum(baseline*1.6,1e-6))
    # Select a stable continuous minute, without chopping out water transients.
    candidates=[]
    for start in range(3,max(4,seconds-61)):
        part=rms[start:start+60]
        if len(part)<60:continue
        score=float(np.std(np.log(np.maximum(part,1e-8)))+.03*np.log1p(peak_ratio[start:start+60].max()))
        candidates.append((score,start))
    chosen=min(candidates)[1] if candidates else 3
    result={'file':str(path.relative_to(ROOT)),'duration_seconds':len(x)/sr,'sample_rate_analyzed':sr,
        'peak_dbfs':float(20*np.log10(max(float(np.abs(x).max()),1e-9))),
        'rms_dbfs':float(20*np.log10(max(float(np.sqrt(np.mean(x*x))),1e-9))),
        'clipped_samples':int((np.abs(x)>=.9999).sum()),'rms_per_second':rms.tolist(),
        'bands_db_relative_fft':bands,'narrow_band_peak_ratio_per_second':peak_ratio.tolist(),
        'rms_spike_seconds':spikes.tolist(),'suggested_continuous_minute_start':chosen,
        'review_candidate_seconds_by_tonality':np.argsort(peak_ratio)[-8:].tolist(),
        'semantic_content_or_speech_absence_verified':False,'listening_review':'pending user audition'}
    return result

def main():
    manifest=json.loads((ASSETS/'sources.json').read_text());results=[]
    for name,(filename,start,duration) in SOURCES.items():
        source=ASSETS/'originals'/filename;target=ASSETS/(name+'_source.flac')
        subprocess.run(['ffmpeg','-y','-v','error','-ss',str(start),'-i',str(source),'-t',str(duration),
            '-ar','48000','-ac','2','-c:a','flac','-compression_level','8',str(target)],check=True)
        row=next(x for x in manifest if x['name']==name)
        row.update(prepared_file=str(target.relative_to(ROOT)),prepared_source_start_seconds=start,
            prepared_duration_seconds=duration,prepared_sha256=hashlib.sha256(target.read_bytes()).hexdigest())
        result=inspect(target);results.append({'source':name,**result})
        print(name,'duration',result['duration_seconds'],'chosen_minute',result['suggested_continuous_minute_start'],
            'peak',round(result['peak_dbfs'],2),'spikes',result['rms_spike_seconds'],flush=True)
    (ASSETS/'sources.json').write_text(json.dumps(manifest,indent=2))
    (RESEARCH/'signal_screening.json').write_text(json.dumps({'sources':results,
        'screening_limit':'Numerical/spectral screening cannot certify absence of voices, wildlife, traffic or baked thunder. User listening review required.',
        'no_new_thunder_or_wildlife_tracks_added':True},indent=2))
    for name in SOURCES:
        subprocess.run(['ffmpeg','-y','-v','error','-i',str(ASSETS/(name+'_source.flac')),
            '-lavfi','showspectrumpic=s=1600x800:legend=1:scale=log:fscale=log','-frames:v','1',
            str(RESEARCH/(name+'_spectrogram.png'))],check=True)

if __name__=='__main__':main()
