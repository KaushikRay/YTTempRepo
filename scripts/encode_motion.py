"""Encode the motion study and validate duration, frame count and changing regions."""
from pathlib import Path
import os,subprocess,json,hashlib,numpy as np
root=Path(__file__).resolve().parents[1];out=root/'renders'/os.environ.get('LOUNGE_REVIEW_DIR','motion');run=json.loads((out/'run.json').read_text());expected=run['expected_frames'];fps=run['fps'];width=run['width'];height=run['height'];duration_expected=expected/fps
if run['status']!='frames_complete' or run['completed']!=expected:raise RuntimeError('Motion rendering has not completed')
files=sorted((out/'frames').glob('full_*.png'))
if len(files)!=expected or len({hashlib.sha256(p.read_bytes()).hexdigest() for p in files})!=expected:raise RuntimeError('Missing or duplicate rendered frames')
def cmd(args):subprocess.run(args,check=True)
base=['ffmpeg','-y','-loglevel','error']
cmd(base+['-framerate',str(fps),'-i',str(out/'frames/full_%04d.png'),'-frames:v',str(expected),'-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'full_room.mp4')])
base_regions={'fire_crop':(448,176,192,160),'window_crop':(152,32,192,280)}
regions={name:tuple(int(round(v*width/640/2))*2 for v in rect) for name,rect in base_regions.items()}
for name,(x,y,w,h) in regions.items():
 cmd(base+['-i',str(out/'full_room.mp4'),'-vf',f'crop={w}:{h}:{x}:{y},scale={w*2}:{h*2}:flags=lanczos','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out/(name+'.mp4'))])
# Decode all frames, rather than trusting that an encoder emitted a file.
raw=subprocess.check_output(['ffmpeg','-loglevel','error','-i',str(out/'full_room.mp4'),'-f','rawvideo','-pix_fmt','rgb24','-'])
frames=np.frombuffer(raw,dtype=np.uint8).reshape(-1,height,width,3)
if len(frames)!=expected:raise RuntimeError(f'Unexpected decoded frame count: {len(frames)}')
diff=np.abs(np.diff(frames.astype(np.int16),axis=0));motion={}
for name,(x,y,w,h) in regions.items():motion[name]=float(diff[:,y:y+h,x:x+w].mean())
if any(v<=.05 for v in motion.values()):raise RuntimeError('A motion review region appears static')
checks={}
for name in ['full_room','fire_crop','window_crop']:
 path=out/(name+'.mp4');probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','format=duration:stream=codec_type,codec_name,nb_read_frames,r_frame_rate,width,height','-of','json',str(path)],text=True))
 video=[s for s in probe['streams'] if s['codec_type']=='video'];duration=float(probe['format']['duration'])
 if len(video)!=1 or int(video[0]['nb_read_frames'])!=expected or abs(duration-duration_expected)>.02 or len(probe['streams'])!=1:raise RuntimeError(f'Unexpected encoding result: {name}')
 cmd(['ffmpeg','-v','error','-i',str(path),'-f','null','-'])
 checks[name]={'duration':duration,'frames':expected,'fps':video[0]['r_frame_rate'],'width':video[0]['width'],'height':video[0]['height'],'bytes':path.stat().st_size}
cmd(base+['-i',str(out/'full_room.mp4'),'-vf',f'select=eq(n\\,{expected//2-1})','-frames:v','1',str(out/'poster.png')])
report={'checks':checks,'region_mean_absolute_frame_difference_8bit':motion,'unique_rendered_frames':expected,'audio_included':False,'crops_are_magnified_from_full_room':True,'seamless_loop':False,'visual_review':'sampled frames and motion-region differences; user playback review pending'}
(out/'qa.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
