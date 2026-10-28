"""Prepare bounded-memory source caches and matching H.264 long-video units."""
import hashlib,json,os,subprocess,time
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'renders/long_release';WORK=OUT/'work';SR=48000
COMMON=['-c:v','libx264','-preset','medium','-crf','18','-maxrate','6400k','-bufsize','12800k','-g','48','-keyint_min','48','-sc_threshold','0','-x264-params','open-gop=0','-r','24','-video_track_timescale','12288','-pix_fmt','yuv420p','-profile:v','high','-level','4.1','-threads','4','-an']
def status(phase,**extra):
 d={'phase':phase,'worker_running':phase not in ['complete','failed'],'pid':os.getpid(),'updated_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),**extra}
 for p in [ROOT/'status.json',OUT/'status.json']:p.write_text(json.dumps(d,indent=2))
 print(json.dumps(d),flush=True)
def run(cmd):subprocess.run(cmd,check=True)
def main():
 WORK.mkdir(parents=True,exist_ok=True);records=[]
 for name,filename,hp,lp in [('rain','rain.oga',110,6500),('stream','long_stream.ogg',150,5800)]:
  target=WORK/(name+'_filtered.f32');original=ROOT/'assets/audio/originals'/filename
  status('preparing_long_audio_source',source=name)
  if not target.exists():run(['ffmpeg','-y','-v','error','-i',str(original),'-af',f'highpass=f={hp},lowpass=f={lp}','-ar',str(SR),'-ac','2','-f','f32le',str(target)])
  samples=target.stat().st_size//8;data=np.memmap(target,dtype=np.float32,mode='r',shape=(samples,2));seconds=samples//SR
  levels=[];peaks=[];tonal=[]
  for start in range(0,seconds,30):
   n=min(30,seconds-start);x=np.array(data[start*SR:(start+n)*SR]);blocks=x.reshape(n,SR,2)
   levels.extend(np.sqrt(np.mean(blocks**2,axis=(1,2))).tolist());peaks.extend(np.max(np.abs(blocks),axis=(1,2)).tolist())
   mono=blocks[:,::4].mean(axis=2);spec=np.abs(np.fft.rfft(mono*np.hanning(mono.shape[1]),axis=1))**2;hz=np.fft.rfftfreq(mono.shape[1],4/SR)
   part=spec[:,(hz>=650)&(hz<5500)];part=part[:,:part.shape[1]//32*32].reshape(n,-1,32).mean(axis=2)
   tonal.extend((part.max(axis=1)/np.maximum(np.median(part,axis=1),1e-15)).tolist())
  levels=np.array(levels);peaks=np.array(peaks);tonal=np.array(tonal);med=np.median(levels)
  bad=(levels>med*2.5)|(levels<med*.22)|(peaks>max(.98,np.quantile(peaks,.999)*1.3))|(tonal>max(80,np.quantile(tonal,.99)*1.5))
  starts=[s for s in range(3,seconds-66,3) if not bad[s:s+63].any()]
  assert len(starts)>10,(name,len(starts))
  records.append({'name':name,'file':str(target.relative_to(ROOT)),'samples':samples,'duration_seconds':samples/SR,'sample_rate':SR,'source_file':str(original.relative_to(ROOT)),
   'highpass_hz':hp,'lowpass_hz':lp,'valid_grain_start_seconds':starts,'excluded_seconds':np.flatnonzero(bad).tolist(),'rms_per_second':levels.tolist(),
   'screening_limit':'Signal/spectral screening only; no claim of complete human audition or semantic-content detection'})
 (OUT/'source_cache.json').write_text(json.dumps({'sources':records,'sample_rate':SR},indent=2))
 # A calm, unobtrusive reusable channel reminder. No brand logo or sound effect.
 badge=Image.new('RGBA',(440,68),(0,0,0,0));draw=ImageDraw.Draw(badge)
 draw.rounded_rectangle((0,0,439,67),radius=16,fill=(8,13,16,145))
 draw.arc((19,17,47,49),180,360,fill=(245,245,240,230),width=2);draw.line([(19,33),(17,48),(49,48),(47,33)],fill=(245,245,240,230),width=2)
 draw.arc((28,46,38,56),0,180,fill=(245,245,240,230),width=2)
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
 draw.text((63,24),'Subscribe for more rain ambience',font=font,fill=(245,245,240,230));badge.save(OUT/'subscribe_badge.png')
 visual=ROOT/'renders/production_test/graded_loop.mp4';units=[]
 for name,seconds,filters in [('calm',12,'null'),('intro',60,'fade=t=in:st=1:d=5'),('closing',24,'fade=t=out:st=4:d=20'),('black',60,'lutyuv=y=16:u=128:v=128')]:
  status('encoding_long_video_unit',unit=name,duration_seconds=seconds);target=WORK/(name+'.mp4')
  if not target.exists():
   args=['ffmpeg','-y','-v','error','-stream_loop',str(seconds//12-1),'-i',str(visual)]
   if name=='intro':
    args+=['-loop','1','-i',str(OUT/'subscribe_badge.png'),'-filter_complex',f'[0:v]{filters}[bg];[1:v]format=rgba,fade=t=in:st=0:d=0.8:alpha=1,fade=t=out:st=7.2:d=0.8:alpha=1,setpts=PTS+6/TB[badge];[bg][badge]overlay=x=W-w-48:y=H-h-48+14*(1-min(max((t-6)/0.8\\,0)\\,1)):enable=between(t\\,6\\,14):eof_action=pass[v]','-map','[v]']
   else:args+=['-vf',filters]
   run(args+['-t',str(seconds),*COMMON,'-movflags','+faststart',str(target)])
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_data_hash','sha256','-of','json',str(target)]));v=probe['streams'][0]
  units.append({'name':name,'path':str(target.relative_to(ROOT)),'duration_seconds':seconds,'frames':int(v['nb_frames']),'extradata_hash':v.get('extradata_hash'),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
 assert len({x['extradata_hash'] for x in units})==1,units
 (OUT/'units.json').write_text(json.dumps({'units':units,'intro_black_seconds':1,'picture_fade_seconds':5,'subscribe_seconds':[6,14],'closing_fade_seconds':20},indent=2))
 status('long_sources_and_units_ready',worker_running=False)
if __name__=='__main__':main()
