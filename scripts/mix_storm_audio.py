"""Six-second licensed ambience mix with thunder delayed from the flash."""
from pathlib import Path
import subprocess,json,numpy as np,hashlib,re
root=Path(__file__).resolve().parents[1];assets=root/'assets/audio';out=root/'renders/storm_preview';out.mkdir(exist_ok=True);sr=48000;duration=6;count=sr*duration

def decode(path,start=0,dur=None,filters='anull'):
 args=['ffmpeg','-loglevel','error','-i',str(path),'-af',filters,'-ar',str(sr),'-ac','2','-f','f32le','-']
 raw=subprocess.check_output(args);decoded=np.frombuffer(raw,dtype=np.float32).reshape(-1,2);first=int(round(start*sr));last=None if dur is None else first+int(round(dur*sr));return decoded[first:last].copy()

def normalize(x,db):
 rms=float(np.sqrt(np.mean(x*x)))
 if rms<1e-7:raise RuntimeError('Silent source audio')
 return x*(10**(db/20)/rms)
def fade(x,head=.05,tail=.25):
 x=x.copy();a=min(len(x),int(head*sr));b=min(len(x),int(tail*sr))
 if a:x[:a]*=np.linspace(0,1,a,dtype=np.float32)[:,None]
 if b:x[-b:]*=np.linspace(1,0,b,dtype=np.float32)[:,None]
 return x
def write(path,x):
 subprocess.run(['ffmpeg','-y','-loglevel','error','-f','f32le','-ar',str(sr),'-ac','2','-i','-','-c:a','pcm_s24le',str(path)],input=x.astype(np.float32).tobytes(),check=True)
rain=decode(assets/'rain.ogg',10,6,'highpass=f=110,lowpass=f=4500');fire=decode(root/'assets/fire/source.webm',2,6,'highpass=f=100,lowpass=f=4500')
if len(rain)<count or len(fire)<count:raise RuntimeError('Rain/fire segment shorter than six seconds')
rain=normalize(rain[:count],-28);fire=normalize(fire[:count],-32);rain*=np.array([1,.9],np.float32);fire*=np.array([.65,1],np.float32)
# Find a strong thunder event with sufficient original tail available.
raw=decode(assets/'thunder.ogg',0,None,'highpass=f=35,lowpass=f=900');block=960;blocks=len(raw)//block;env=np.sqrt(np.mean(raw[:blocks*block].reshape(blocks,block,2)**2,axis=(1,2)))
limit=max(1,len(env)-int(3*sr/block));peak=int(np.argmax(env[:limit]));start=max(0,peak*block/sr-.15);thunder=raw[int(start*sr):int(start*sr)+3*sr];thunder=fade(normalize(thunder,-24),.07,.45)
# Subtle room response on the crackle, without masking the delayed thunder.
wet=fire.copy()
for delay,gain in [(.055,.07),(.11,.035),(.17,.02)]:
 n=int(delay*sr);wet[n:]+=fire[:-n]*gain
fire=wet
thunder_stem=np.zeros((count,2),np.float32);thunder_start=3*sr;n=min(len(thunder),count-thunder_start);thunder_stem[thunder_start:thunder_start+n]=thunder[:n]
mix=fade(rain+fire+thunder_stem,.25,.35)
if not np.isfinite(mix).all():raise RuntimeError('Non-finite audio samples')
write(out/'mix_pre_normalization.wav',mix)
# Integrated loudness and true-peak limiting are measured on the actual output.
analysis=subprocess.run(['ffmpeg','-hide_banner','-i',str(out/'mix_pre_normalization.wav'),'-af','loudnorm=I=-24:TP=-2:LRA=8:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
(out/'audio_loudnorm_analysis.log').write_text(analysis.stderr);measured=json.loads(re.search(r'\{[^{}]+\}',analysis.stderr).group(0))
settings='loudnorm=I=-24:TP=-2:LRA=8:measured_I='+measured['input_i']+':measured_TP='+measured['input_tp']+':measured_LRA='+measured['input_lra']+':measured_thresh='+measured['input_thresh']+':offset='+measured['target_offset']+':linear=true:print_format=json'
with (out/'audio_loudnorm.log').open('w') as log:
 subprocess.run(['ffmpeg','-y','-hide_banner','-i',str(out/'mix_pre_normalization.wav'),'-af',settings,'-ar',str(sr),'-c:a','pcm_s24le',str(out/'audio_mix.wav')],stderr=log,stdout=subprocess.DEVNULL,check=True)
report={'sample_rate':sr,'duration_seconds':6,'rain_source_seconds':[10,16],'fire_source_seconds':[2,8],'thunder_source_start_seconds':start,'thunder_mix_start_seconds':3,'main_flash_seconds':1.75,'thunder_delay_seconds':1.25,'target_integrated_lufs':-24,'target_true_peak_dbfs':-2,'music':False,'sources':'assets/audio/sources.json and assets/fire/source.json','listening_review':'pending user review; source descriptions, spectrum and signal levels checked'}
(out/'audio_mix.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
credits=[]
for item in json.loads((assets/'sources.json').read_text()):
 credits.append(f"{item['title']} — {item['author']}; {item['licence']}; {item['source_url']}; {item['licence_url'] or 'public-domain declaration on source page'}. Modified: selected excerpt, filtered, level-adjusted and mixed.")
credits.append((root/'assets/fire/CREDITS.txt').read_text()+' Fire soundtrack: original source seconds 2–8, filtered and level-adjusted, placed toward the hearth side.')
(assets/'CREDITS.txt').write_text('\n\n'.join(credits)+'\n')
