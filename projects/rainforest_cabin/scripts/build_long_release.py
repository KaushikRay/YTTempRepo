"""Bounded-memory endurance and 3 h / 8 h masters from approved source assets."""
import csv,hashlib,json,math,os,random,subprocess,time
from pathlib import Path
import numpy as np
from scipy.signal import resample_poly
from mix_rainforest_audio import decode,spatial,tame,SR,loudness
from prepare_long_release import ROOT,OUT,WORK,status
MINUTE=60*SR;OVERLAP=3*SR;GRAIN=MINUTE+OVERLAP

def thunder_events(seconds,seed,dark_after=None):
 rng=random.Random(seed);base=decode(ROOT/'renders/production_test/thunder_solo.flac',sr=SR)[6*SR:round((6+18.4163333333)*SR)]
 variants=[base,resample_poly(base,107,100,axis=0).astype(np.float32),resample_poly(base,103,100,axis=0).astype(np.float32),resample_poly(base,98,100,axis=0).astype(np.float32)]
 events=[];t=75.;previous=-1
 while t<seconds-40:
  variant=rng.choice([i for i in range(4) if i!=previous]);previous=variant;gain_db=rng.uniform(-2,0)
  if dark_after is not None and t>=dark_after:gain_db-=2
  events.append({'start_seconds':round(t,3),'variant':variant,'gain_db':gain_db,'duration_seconds':len(variants[variant])/SR})
  t+=rng.uniform(150,240)
 return events,variants

def audio_track(name,seconds,dark_after=None,correction_db=0):
 target=WORK/(name+'_audio.m4a');report_file=OUT/(name+'_audio.json')
 if target.exists() and report_file.exists():return target,json.loads(report_file.read_text())
 sources=json.loads((OUT/'source_cache.json').read_text())['sources'];maps={s['name']:np.memmap(ROOT/s['file'],dtype=np.float32,mode='r',shape=(s['samples'],2)) for s in sources}
 # Small Mac packages retain the exact approved reference measurements instead
 # of requiring two large FLAC stems solely to measure their RMS again.
 reference_file=OUT/'reference_rms.json'
 if reference_file.exists():
  reference=json.loads(reference_file.read_text());assert reference['sample_rate']==SR
  target_rms=reference['target_rms'];assert all(0<float(target_rms[n])<1 for n in ['rain','stream'])
 else:
  refs={n:decode(ROOT/f'renders/production_test/{n}_solo.flac',sr=SR)[10*SR:110*SR] for n in ['rain','stream']}
  target_rms={n:float(np.sqrt(np.mean(x*x))) for n,x in refs.items()};del refs
 seed={'endurance':6137,'rainforest_3h':6191,'rainforest_8h':6229}[name];rng=random.Random(seed);events,variants=thunder_events(seconds,seed+100,dark_after)
 command=['ffmpeg','-y','-v','error','-f','f32le','-ar',str(SR),'-ac','2','-i','-','-c:a','aac','-b:a','256k','-threads','2','-movflags','+faststart',str(target)]
 process=subprocess.Popen(command,stdin=subprocess.PIPE);tails={};grains=[];peak=0.;limited=0;total_samples=0;started=time.monotonic();correction=10**(correction_db/20)
 blocks=math.ceil(seconds/60)
 try:
  for block in range(blocks):
   absolute=block*MINUTE;count=min(MINUTE,seconds*SR-absolute);parts=[]
   for source in sources:
    n=source['name'];start=rng.choice(source['valid_grain_start_seconds']);x=np.array(maps[n][start*SR:start*SR+GRAIN]);assert len(x)==GRAIN
    swapped=rng.random()<.5
    if swapped:x=x[:,::-1].copy()
    x,_=tame(x,1.6);x=spatial(x,.95 if n=='rain' else .55,0 if n=='rain' else .23)
    rms=float(np.sqrt(np.mean(x*x)));x*=target_rms[n]/max(rms,1e-9)
    if n in tails:
     theta=np.linspace(0,np.pi/2,OVERLAP,dtype=np.float32);head=tails[n]*np.cos(theta)[:,None]+x[:OVERLAP]*np.sin(theta)[:,None]
     output=np.concatenate([head,x[OVERLAP:MINUTE]],axis=0)
    else:output=x[:MINUTE]
    tails[n]=x[MINUTE:MINUTE+OVERLAP].copy();parts.append(output[:count]);grains.append({'output_seconds':block*60,'source':n,'source_start_seconds':start,'lr_swapped_before_pan':swapped})
   mix=parts[0]+parts[1]
   for event in events:
    first=round(event['start_seconds']*SR);wave=variants[event['variant']];last=first+len(wave);lo=max(absolute,first);hi=min(absolute+count,last)
    if hi>lo:mix[lo-absolute:hi-absolute]+=wave[lo-first:hi-first]*10**(event['gain_db']/20)
   t=(absolute+np.arange(count,dtype=np.float32))/SR;fade=np.minimum(np.clip((t-1)/8,0,1),np.clip((seconds-t)/20,0,1));fade=np.sin(fade*np.pi/2)**2
   mix*=fade[:,None]*correction
   # Soft knee, unity below .42, asymptotic .75 sample ceiling.
   magnitude=np.abs(mix);mask=magnitude>.42;limited+=int(mask.sum());total_samples+=mix.size
   mix=np.where(mask,np.sign(mix)*(.42+.33*np.tanh((magnitude-.42)/.33)),mix).astype(np.float32)
   assert np.isfinite(mix).all();peak=max(peak,float(np.abs(mix).max()));process.stdin.write(mix.tobytes())
   status('assembling_long_audio',version=name,completed_minutes=block+1,total_minutes=blocks,estimated_seconds_remaining=round((time.monotonic()-started)/(block+1)*(blocks-block-1)))
  process.stdin.close();assert process.wait()==0
 except BaseException:
  process.kill();target.unlink(missing_ok=True);raise
 report={'duration_seconds':seconds,'sample_rate':SR,'channels':2,'events':events,'grains':grains,'equal_power_crossfade_seconds':3,
  'source_grain_seconds':63,'audio_fade_in_from_second':1,'audio_fade_in_seconds':8,'audio_fade_out_seconds':20,'rain_stream_reference':'approved production-test solo levels',
  'source_screening':'technical signal/spectral screening, not exhaustive human audition','same_thunder_recording_with_four_processed_variations':True,'visual_lightning':False,
  'dark_screen_after_seconds':dark_after,'sample_peak_dbfs':20*math.log10(peak),'soft_knee_affected_sample_fraction':limited/total_samples,'global_correction_db':correction_db,'elapsed_seconds':time.monotonic()-started}
 report_file.write_text(json.dumps(report,indent=2))
 with (OUT/(name+'_events.csv')).open('w',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=['start_seconds','variant','gain_db','duration_seconds']);writer.writeheader();writer.writerows(events)
 return target,report

def video_master(name,seconds,scene_seconds,audio):
 target=OUT/(name+'.mp4')
 if target.exists():
  try:
   probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-of','json',str(target)],stderr=subprocess.DEVNULL))
   if abs(float(probe['format']['duration'])-seconds)<.05:return target
  except (subprocess.CalledProcessError,KeyError,ValueError):pass
  target.unlink()
 units=json.loads((OUT/'units.json').read_text())['units'];paths={u['name']:ROOT/u['path'] for u in units}
 loops=(scene_seconds-60-24)//12;assert 60+loops*12+24==scene_seconds
 entries=[paths['intro']]+[paths['calm']]*loops+[paths['closing']]
 if seconds>scene_seconds:assert (seconds-scene_seconds)%60==0;entries += [paths['black']]*((seconds-scene_seconds)//60)
 playlist=WORK/(name+'_concat.txt');playlist.write_text(''.join("file '"+str(p)+"'\n" for p in entries))
 status('assembling_long_video',version=name,duration_seconds=seconds,scene_seconds=scene_seconds)
 subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(playlist),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-t',str(seconds),'-c','copy','-movflags','+faststart',str(target)],check=True)
 return target

def main():
 # Twelve minutes of picture and three minutes of dark exercise both release modes.
 audio,_=audio_track('endurance',900,720);test=video_master('endurance',900,720,audio)
 measure=loudness(audio);correction=-24-float(measure['input_i']);assert float(measure['input_tp'])<=-2
 (OUT/'endurance_level.json').write_text(json.dumps({'measurement':measure,'correction_for_masters_db':correction},indent=2))
 for name,seconds,scene in [('rainforest_3h',10800,10800),('rainforest_8h',28800,3600)]:
  audio,_=audio_track(name,seconds,scene if scene<seconds else None,correction)
  video_master(name,seconds,scene,audio)
 status('masters_built_awaiting_qa',worker_running=False,outputs=['rainforest_3h.mp4','rainforest_8h.mp4'])
if __name__=='__main__':main()
