"""Container timing, selected full-resolution decode, fade/black and long audio QA."""
import hashlib,json,os,random,subprocess,time
from pathlib import Path
import numpy as np
from PIL import Image
from prepare_long_release import ROOT,OUT,WORK,status
from mix_rainforest_audio import loudness

def frame(path,second,dest):
 subprocess.run(['ffmpeg','-y','-v','error','-ss',str(second),'-i',str(path),'-frames:v','1',str(dest)],check=True)
 return np.asarray(Image.open(dest).convert('RGB'))
def repair_grain_metadata(name):
 p=OUT/(name+'_audio.json');report=json.loads(p.read_text());sources=json.loads((OUT/'source_cache.json').read_text())['sources'];lookup={s['name']:s for s in sources};rng=random.Random({'endurance':6137,'rainforest_3h':6191,'rainforest_8h':6229}[name])
 for grain in report['grains']:
  expected=rng.choice(lookup[grain['source']]['valid_grain_start_seconds']);swap=rng.random()<.5;assert expected==grain['source_start_seconds'];grain['lr_swapped_before_pan']=swap
 p.write_text(json.dumps(report,indent=2))
def main():
 result=[];images=OUT/'qa_frames';images.mkdir(exist_ok=True)
 for name,duration,scene in [('endurance',900,720),('rainforest_3h',10800,10800),('rainforest_8h',28800,3600)]:
  if os.environ.get('ONLY_LONG_VERSION') and os.environ['ONLY_LONG_VERSION']!=name:continue
  path=OUT/(name+'.mp4')
  if not path.exists():continue
  status('checking_long_master',version=name)
  repair_grain_metadata(name)
  probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]));v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
  assert abs(float(probe['format']['duration'])-duration)<.05 and int(v['nb_frames'])==duration*24
  assert (v['width'],v['height'])==(1920,1080) and v['r_frame_rate']=='24/1' and a['sample_rate']=='48000' and a['channels']==2
  times=[.5,3,10,16,59.9,60.1,75,scene-22,scene-10,scene-.5,duration-.5]
  if scene<duration:times += [scene+.5,scene+60,min(duration-1,scene+3600)]
  pictures=[]
  for t in sorted(set(times)):
   dest=images/f'{name}_{t:09.2f}.jpg';rgb=frame(path,t,dest);brightness=float(rgb.mean())
   if t==.5 or t>=scene:assert brightness<1.2,(name,t,brightness)
   if t in [10,16,75]:assert brightness>12,(name,t,brightness)
   pictures.append({'second':t,'mean_rgb_code':brightness,'image':str(dest.relative_to(ROOT))})
  # Decode samples across GOP/piece transitions and near the end, plus all audio
  # for actual integrated loudness and oversampled true peak via loudnorm.
  for t in [58,scene-22,max(0,scene-2),duration-4]:
   subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-t','4','-f','null','-'],check=True)
  status('measuring_full_long_audio',version=name,duration_seconds=duration)
  measured=loudness(path);assert -24.8<float(measured['input_i'])<-23.2 and float(measured['input_tp'])<=-2,(name,measured)
  report={'name':name,'file':path.name,'duration_seconds':duration,'scene_seconds':scene,'dark_screen_seconds':duration-scene,'video_frames':duration*24,'resolution':[1920,1080],'fps':24,
   'integrated_lufs':float(measured['input_i']),'true_peak_dbfs':float(measured['input_tp']),'loudness_range_lu':float(measured['input_lra']),
   'audio_fully_decoded_and_measured':True,'video_transition_and_end_samples_decoded':True,'qa_frames':pictures,'bytes':path.stat().st_size,
   'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'visual_lightning':False,'full_video_not_exhaustively_decoded':True}
  (OUT/(name+'_qa.json')).write_text(json.dumps(report,indent=2));result.append(report)
 reports=[json.loads(p.read_text()) for p in sorted(OUT.glob('*_qa.json'))]
 (OUT/'qa.json').write_text(json.dumps({'masters':reports,'source_and_content_limit':'Technical source screening and sampled video QA, not exhaustive human audition of 11 hours.'},indent=2))
 status('long_master_qa_complete',worker_running=False,versions_checked=[x['name'] for x in result])
if __name__=='__main__':main()
