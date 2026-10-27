"""Native 1080p integrated 3D river preview, resumable and cache-aware.

Rerender the lower camera border with the actual water, banks, rain and palms.
Reuse the approved native pixels elsewhere. With no original native cache,
render complete full frames instead. No image-based water motion is used.
"""
import bpy,json,hashlib,os,struct,subprocess,time,traceback,shutil
from pathlib import Path
from integrated_fluid_scene import ROOT,OUT,setup,load_frame,status
BASE=ROOT/'renders/hybrid_motion/frames';CROP=OUT/'crop_frames';FULL=OUT/'frames'
for p in [CROP,FULL]:p.mkdir(parents=True,exist_ok=True)
def intact(path,size):
 if not path.exists():return False
 data=path.read_bytes();return len(data)>32 and data[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',data[16:24])==size and data[-12:-4]==b'\0\0\0\0IEND'
def main():
 status('preparing_integrated_motion');s=setup();total=96;s.frame_end=total
 use_cache=all(intact(BASE/f'{f:04d}.png',(1920,1080)) for f in range(1,total+1));size=(1040,400) if use_cache else (1920,1080);folder=CROP if use_cache else FULL
 key=hashlib.sha256(b''.join(p.read_bytes() for p in [Path(__file__),ROOT/'scripts/integrated_fluid_scene.py',ROOT/'research/integrated_fluid/simulation.json',ROOT/'assets/integrated_fluid/channel.json',ROOT/'assets/integrated_fluid/upstream_instance.json'])).hexdigest();stamp=OUT/'render_signature.json'
 if not stamp.exists() or json.loads(stamp.read_text())['sha256']!=key:
  for directory in [CROP,FULL]:
   for path in directory.glob('*.png'):path.unlink()
  stamp.write_text(json.dumps({'sha256':key,'uses_approved_native_cache':use_cache,'frames':total,'samples':s.cycles.samples},indent=2))
 if use_cache:
  s.render.use_border=True;s.render.use_crop_to_border=True;s.render.border_min_x=(720+.001)/1920;s.render.border_max_x=(1760+.001)/1920;s.render.border_min_y=0;s.render.border_max_y=(400+.001)/1080
 initial=sum(intact(folder/f'{f:04d}.png',size) for f in range(1,total+1));start=time.monotonic();done=0
 for frame in range(1,total+1):
  path=folder/f'{frame:04d}.png'
  if intact(path,size):continue
  s.frame_set(frame);counts=load_frame(frame);status('rendering_integrated_3D_river',current_frame=frame,completed_frames=initial+done,total_frames=total,full_resolution=[1920,1080],render_border_size=list(size),geometry_counts=counts,samples=s.cycles.samples,
      estimated_seconds_remaining=None if done==0 else round((time.monotonic()-start)/done*(total-initial-done)))
  s.render.filepath=str(path);bpy.ops.render.render(write_still=True);assert intact(path,size);done+=1
 if use_cache:
  status('compositing_integrated_native_frames',completed_frames=total,total_frames=total)
  subprocess.run(['ffmpeg','-y','-v','error','-framerate','24','-i',str(BASE/'%04d.png'),'-framerate','24','-i',str(CROP/'%04d.png'),'-filter_complex','[0:v][1:v]overlay=720:680:format=rgb,format=rgb24','-frames:v',str(total),'-start_number','1',str(FULL/'%04d.png')],check=True)
 status('encoding_integrated_preview',completed_frames=total,total_frames=total)
 movie=OUT/'preview.mp4';subprocess.run(['ffmpeg','-y','-v','error','-framerate','24','-i',str(FULL/'%04d.png'),'-frames:v',str(total),'-c:v','libx264','-preset','slow','-crf','16','-g','48','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(movie)],check=True)
 subprocess.run(['ffmpeg','-y','-v','error','-i',str(movie),'-vf','crop=1040:400:720:680','-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(OUT/'river_detail.mp4')],check=True)
 shutil.copyfile(FULL/'0024.png',OUT/'still.png')
 report={'frames':96,'fps':24,'duration_seconds':4,'resolution':[1920,1080],'cycles_samples':s.cycles.samples,'native_frames':True,'no_frame_interpolation':True,'audio':False,'seamless_loop':False,
   'method':s['method'],'water_motion_from_images_or_footage':False,'background_generated_matte':True,'cached_approved_outside_pixels':use_cache,'rendered_border':[720,680,1040,400] if use_cache else None,
   'upstream_uses_spatial_instance_of_same_bake':True,'elapsed_seconds':time.monotonic()-start,'preview_sha256':hashlib.sha256(movie.read_bytes()).hexdigest()}
 (OUT/'render_report.json').write_text(json.dumps(report,indent=2));status('complete',output='renders/integrated_fluid/preview.mp4',completed_frames=total,total_frames=total)
if __name__=='__main__':
 try:main()
 except BaseException as exc:traceback.print_exc();status('failed',error=str(exc));os._exit(1)
 os._exit(0)
