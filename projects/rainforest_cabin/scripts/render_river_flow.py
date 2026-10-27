"""Render updated river borders; reuse approved native outside pixels if present.

Without the prior native cache, render whole native frames instead. Movie inputs
are real CC0 footage; no generated video or optical-flow interpolation is used.
"""
import bpy,hashlib,json,os,struct,subprocess,time,traceback,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'renders/river_flow';CROP=OUT/'crop_frames';FULL=OUT/'frames'
for p in [CROP,FULL]:p.mkdir(parents=True,exist_ok=True)
BASE=ROOT/'renders/hybrid_motion/frames'

def update(phase,**extra):
    d={'phase':phase,'updated_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'pid':os.getpid(),'worker_running':phase not in ['complete','failed'],'variant':'revised_directional_river_flow',**extra}
    (ROOT/'status.json').write_text(json.dumps(d,indent=2));(OUT/'status.json').write_text(json.dumps(d,indent=2));print('RIVER STATUS',json.dumps(d),flush=True)

def intact(p,size):
    if not p.exists():return False
    b=p.read_bytes();return len(b)>32 and b[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',b[16:24])==size and b[-12:-4]==b'\0\0\0\0IEND'

def encode(folder,movie):
    subprocess.run(['ffmpeg','-y','-v','error','-framerate','24','-start_number','1','-i',str(folder/'%04d.png'),'-frames:v','144','-c:v','libx264','-preset','slow','-crf','16','-g','48','-keyint_min','48','-sc_threshold','0','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(movie)],check=True)

def main():
    update('preparing_river_render');model=ROOT/'rainforest_hybrid_motion.blend'
    use_cache=all(intact(BASE/f'{i:04d}.png',(1920,1080)) for i in range(1,145))
    digest=hashlib.sha256(model.read_bytes()+Path(__file__).read_bytes()+(ROOT/'assets/river_flow/real_rapids.mp4').read_bytes()).hexdigest()
    stamp=OUT/'render_signature.json'
    if not stamp.exists() or json.loads(stamp.read_text())['sha256']!=digest:
        for folder in [CROP,FULL]:
            for p in folder.glob('[0-9][0-9][0-9][0-9].png'):p.unlink()
        stamp.write_text(json.dumps({'sha256':digest,'uses_approved_native_cache':use_cache},indent=2))
    bpy.ops.wm.open_mainfile(filepath=str(model));s=bpy.context.scene
    assert s.frame_end==144 and s.render.fps==24 and s.render.resolution_x==1920 and s.cycles.samples==24
    assert len([o for o in s.objects if o.name.startswith('Real flowing creek / ')])==10
    if use_cache:
        s.render.use_border=True;s.render.use_crop_to_border=True
        s.render.border_min_x=(720+.001)/1920;s.render.border_max_x=(1760+.001)/1920;s.render.border_min_y=0;s.render.border_max_y=(400+.001)/1080
    folder=CROP if use_cache else FULL;size=(1040,400) if use_cache else (1920,1080)
    start=time.monotonic();done=0;initial=sum(intact(folder/f'{i:04d}.png',size) for i in range(1,145))
    for i in range(1,145):
        path=folder/f'{i:04d}.png'
        if intact(path,size):continue
        update('rendering_river_flow',current_frame=i,completed_frames=initial+done,total_frames=144,resolution=list(size),full_output_resolution=[1920,1080],
               preserved_approved_native_pixels=use_cache,estimated_seconds_remaining=None if done==0 else round((time.monotonic()-start)/done*(144-initial-done)))
        s.frame_set(i);s.render.filepath=str(path);bpy.ops.render.render(write_still=True);assert intact(path,size),path;done+=1
    if use_cache:
        update('compositing_river_region',completed_frames=144,total_frames=144)
        subprocess.run(['ffmpeg','-y','-v','error','-framerate','24','-i',str(BASE/'%04d.png'),'-framerate','24','-i',str(CROP/'%04d.png'),
                        '-filter_complex','[0:v][1:v]overlay=720:680:format=rgb,format=rgb24','-frames:v','144','-start_number','1',str(FULL/'%04d.png')],check=True)
    update('encoding_river_preview',completed_frames=144,total_frames=144)
    movie=OUT/'preview.mp4';encode(FULL,movie)
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(movie),'-vf','crop=720:300:960:780','-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-an','-movflags','+faststart',str(OUT/'water_detail.mp4')],check=True)
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(ROOT/'renders/hybrid_motion/water_detail.mp4'),'-i',str(OUT/'water_detail.mp4'),
                    '-filter_complex',"[0:v]drawtext=text='Previous':x=16:y=12:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6[a];[1:v]drawtext=text='Revised flow':x=16:y=12:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6[b];[a][b]hstack=inputs=2",
                    '-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-an','-movflags','+faststart',str(OUT/'water_comparison.mp4')],check=True)
    shutil.copyfile(FULL/'0001.png',OUT/'still.png')
    result={'frames':144,'duration_seconds':6,'fps':24,'resolution':[1920,1080],'cycles_samples':24,'audio':False,'seamless_loop':False,
            'flow_method':s['river_method'],'approved_palm_data_identical':True,'cached_approved_outside_pixels_used':use_cache,'rerendered_border_pixels':[720,680,1040,400] if use_cache else None,
            'source_footage':'assets/river_flow/source.json','source_video_audio_used':False,'no_frame_interpolation':True,'elapsed_seconds':round(time.monotonic()-start,2),
            'preview_sha256':hashlib.sha256(movie.read_bytes()).hexdigest()}
    (OUT/'render_report.json').write_text(json.dumps(result,indent=2));update('complete',completed_frames=144,total_frames=144,output='renders/river_flow/preview.mp4')
    print('RIVER MOTION COMPLETE',flush=True)

try:main()
except BaseException as e:traceback.print_exc();update('failed',error=str(e));os._exit(1)
os._exit(0)
