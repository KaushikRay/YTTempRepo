"""Mux storm audio into checked video outputs and verify actual audiovisual results."""
from pathlib import Path
import subprocess,json,re,numpy as np,shutil
root=Path(__file__).resolve().parents[1];out=root/'renders/storm_preview';setup=json.loads((root/'renders/storm_setup.json').read_text());duration=setup['duration_seconds'];expected=setup['expected_frames']
if not (out/'qa.json').exists():raise RuntimeError('Run video encoding/checks before audio mux')
# Retain the checked video QA; recheck the final audiovisual MP4s separately.
video_qa=json.loads((out/'qa.json').read_text());checks={}
for name in ['full_room','fire_crop','window_crop']:
 path=out/(name+'.mp4');target=out/(name+'_with_audio.mp4')
 subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(path),'-i',str(out/'audio_mix.wav'),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t',str(duration),'-movflags','+faststart',str(target)],check=True)
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','format=duration:stream=codec_type,codec_name,nb_read_frames,r_frame_rate,width,height,sample_rate,channels','-of','json',str(target)],text=True));vs=[s for s in info['streams'] if s['codec_type']=='video'];audio=[s for s in info['streams'] if s['codec_type']=='audio']
 if len(vs)!=1 or len(audio)!=1 or int(vs[0]['nb_read_frames'])!=expected or abs(float(info['format']['duration'])-duration)>.05 or audio[0]['sample_rate']!='48000' or audio[0]['channels']!=2:raise RuntimeError(f'Wrong final streams/timing: {name}')
 subprocess.run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'],check=True);checks[name]=info
analysis=subprocess.run(['ffmpeg','-hide_banner','-i',str(out/'full_room_with_audio.mp4'),'-vn','-af','loudnorm=I=-24:TP=-2:LRA=8:print_format=json','-f','null','-'],capture_output=True,text=True,check=True)
measured=json.loads(re.search(r'\{[^{}]+\}',analysis.stderr).group(0));lufs=float(measured['input_i']);tp=float(measured['input_tp'])
if not (-26<=lufs<=-22) or tp> -1.5:raise RuntimeError(f'Unexpected final AAC levels: {lufs} LUFS, {tp} dBTP')
# Flash brightness is checked on the actual rendered pixels, not only keyframes.
def image(frame):
 raw=subprocess.check_output(['ffmpeg','-loglevel','error','-i',str(out/'frames'/f'full_{frame:04d}.png'),'-f','rawvideo','-pix_fmt','rgb24','-']);return np.frombuffer(raw,np.uint8).reshape(540,960,3).astype(np.float32)
before=image(40);peak=image(43);after=image(52)
def level(a):return float(np.mean(a[70:470,40:650]@np.array([.2126,.7152,.0722],np.float32)))
levels={'before':level(before),'main_flash':level(peak),'after':level(after)}
if levels['main_flash']<levels['before']*1.1:raise RuntimeError('Lightning is not visibly brighter in the render')
shutil.copyfile(out/'frames/full_0043.png',out/'lightning_peak.png')
report={'video_checks':video_qa,'final_av_stream_checks':checks,'audio_integrated_lufs':lufs,'audio_true_peak_dbtp':tp,'flash_render_luma':levels,'flash_seconds':setup['main_flash_seconds'],'thunder_mix_start_seconds':setup['thunder_start_seconds'],'nominal_thunder_delay_seconds':setup['thunder_delay_seconds'],'audio_included':True,'music':False,'seamless_loop':False,'review':'sampled frames, spectral/signal checks and complete decoding passed; human listening/playback review pending'}
(out/'av_qa.json').write_text(json.dumps(report,indent=2));print(json.dumps({'audio_lufs':lufs,'true_peak':tp,'luma':levels,'duration':duration,'frames':expected,'passed':True},indent=2))
