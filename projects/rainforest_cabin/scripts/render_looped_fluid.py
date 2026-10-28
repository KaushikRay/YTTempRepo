"""Render a 12-second native 1080p loop and an explicit two-repeat join test."""
import os
os.environ['INTEGRATED_VARIANT']='looped_fluid'
import bpy,hashlib,json,struct,subprocess,time,traceback,shutil
from pathlib import Path
from integrated_fluid_scene import ROOT,OUT,setup,load_frame,status
TOTAL=288;FRAMES=OUT/'frames';FRAMES.mkdir(parents=True,exist_ok=True)

def intact(path):
    if not path.exists():return False
    d=path.read_bytes()
    return len(d)>32 and d[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',d[16:24])==(1920,1080) and d[-12:-4]==b'\0\0\0\0IEND'

def periodic_rain():
    changes=[]
    for name in ['Fine rain behind cabin','Near rain in front of cabin','Roof runoff falling beads']:
        ob=bpy.data.objects[name];attribute=ob.data.attributes['frequency'];old=[];new=[]
        for datum in attribute.data:
            old.append(float(datum.value));datum.value=max(1,round(datum.value*12))/12;new.append(float(datum.value))
        changes.append({'object':name,'vertices':len(new),'maximum_frequency_change_hz':max(abs(a-b) for a,b in zip(old,new)),
            'integer_cycles_per_loop':True})
    return changes

def setup_loop():
    s=setup();s.frame_end=TOTAL;rain=periodic_rain()
    # Static photographic emitters converge quickly; retain the .01 threshold
    # and 32-sample cap for the actual liquid, while allowing early termination.
    s.cycles.use_adaptive_sampling=True;s.cycles.adaptive_min_samples=8
    s['seamless_loop']='12s periodic rain/palms, approximate 3D scalar-field river transition'
    s['water_loop_is_physics_periodic']=False
    text=bpy.data.texts.get('ENABLE_INTEGRATED_FLUID_PLAYBACK.py')
    text.clear();text.write("import bpy,sys,os\nfrom pathlib import Path\nos.environ['INTEGRATED_VARIANT']='looped_fluid'\nroot=Path(bpy.data.filepath).parent\nsys.path.insert(0,str(root/'scripts'))\nimport integrated_fluid_scene as fluid\n# Reload if another scene variant was imported in the same Blender session.\nif fluid.VARIANT!='looped_fluid':\n    import importlib\n    fluid=importlib.reload(fluid)\ndef integrated_fluid_update(scene): fluid.load_frame((scene.frame_current-1)%288+1)\nfor h in list(bpy.app.handlers.frame_change_pre):\n    if h.__name__=='integrated_fluid_update': bpy.app.handlers.frame_change_pre.remove(h)\nbpy.app.handlers.frame_change_pre.append(integrated_fluid_update)\nintegrated_fluid_update(bpy.context.scene)\n")
    s.render.filepath='//renders/looped_fluid/still.png'
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'rainforest_looped_fluid.blend'),compress=True)
    (ROOT/'research/looped_fluid/rain_periodicity.json').write_text(json.dumps(rain,indent=2))
    return s

def main():
    status('preparing_12_second_native_loop');s=setup_loop()
    key=hashlib.sha256(b''.join(p.read_bytes() for p in [Path(__file__),ROOT/'scripts/integrated_fluid_scene.py',ROOT/'research/looped_fluid/simulation.json',ROOT/'research/looped_fluid/loop.json'])).hexdigest()
    stamp=OUT/'render_signature.json'
    if stamp.exists() and json.loads(stamp.read_text())['sha256']!=key:
        for p in FRAMES.glob('*.png'):p.unlink()
    stamp.write_text(json.dumps({'sha256':key,'frames':TOTAL,'samples':s.cycles.samples,'full_native_frame':True},indent=2))
    initial=sum(intact(FRAMES/f'{f:04d}.png') for f in range(1,TOTAL+1));start=time.monotonic();done=0
    for frame in range(1,TOTAL+1):
        path=FRAMES/f'{frame:04d}.png'
        if intact(path):continue
        s.frame_set(frame);counts=load_frame(frame)
        status('rendering_12_second_native_loop',current_frame=frame,completed_frames=initial+done,total_frames=TOTAL,
            resolution=[1920,1080],samples=s.cycles.samples,geometry_counts=counts,
            estimated_seconds_remaining=None if done==0 else round((time.monotonic()-start)/done*(TOTAL-initial-done)))
        s.render.filepath=str(path);bpy.ops.render.render(write_still=True);assert intact(path);done+=1
        if os.environ.get('BENCHMARK_ONLY'):status('benchmark_complete',render_seconds=time.monotonic()-start);return
    status('encoding_12_second_loop',completed_frames=TOTAL,total_frames=TOTAL)
    common=['-c:v','libx264','-preset','slow','-crf','16','-g','48','-keyint_min','48','-sc_threshold','0','-x264-params','open-gop=0','-r','24','-video_track_timescale','12288','-pix_fmt','yuv420p','-profile:v','high','-level','4.1','-movflags','+faststart','-an']
    movie=OUT/'preview.mp4'
    subprocess.run(['ffmpeg','-y','-v','error','-framerate','24','-i',str(FRAMES/'%04d.png'),'-frames:v',str(TOTAL),*common,str(movie)],check=True)
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(movie),'-vf','crop=1040:400:720:680',*common,str(OUT/'river_detail.mp4')],check=True)
    # Show the seam after twelve seconds and at the start of the second repeat.
    repeats=OUT/'repeat_list.txt';repeats.write_text("file 'preview.mp4'\nfile 'preview.mp4'\n")
    subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(repeats),'-c','copy','-movflags','+faststart',str(OUT/'repeat_test.mp4')],check=True);repeats.unlink()
    shutil.copyfile(FRAMES/'0144.png',OUT/'still.png')
    report={'frames':TOTAL,'fps':24,'duration_seconds':12,'resolution':[1920,1080],'cycles_samples':s.cycles.samples,
        'native_frames':True,'frame_interpolation':False,'rendered_image_dissolve':False,'audio':False,
        'loop_method':'periodic rain and palms; first second of liquid loop-conditioned by 3D scalar-field blending',
        'periodic_physics_solution':False,'hybrid_generated_background':True,'water_motion_from_images_or_footage':False,
        'upstream_uses_spatial_instance_of_same_bake':True,'elapsed_this_run_seconds':time.monotonic()-start,
        'resumed_frames':initial,'preview_sha256':hashlib.sha256(movie.read_bytes()).hexdigest()}
    (OUT/'render_report.json').write_text(json.dumps(report,indent=2))
    status('complete',output='renders/looped_fluid/preview.mp4',completed_frames=TOTAL,total_frames=TOTAL)

if __name__=='__main__':
    try:main()
    except BaseException as exc:traceback.print_exc();status('failed',error=str(exc));os._exit(1)
    os._exit(0)
