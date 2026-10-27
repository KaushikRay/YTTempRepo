"""Resumable native Cycles animation; progress, exact timing, clean decode QA."""
import bpy, hashlib, json, os, struct, subprocess, time, traceback
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'renders/hybrid_motion';FRAMES=OUT/'frames';FRAMES.mkdir(parents=True,exist_ok=True)

def update(phase,**extra):
    value={'phase':phase,'updated_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'pid':os.getpid(),
           'worker_running':phase not in ['complete','failed'],'variant':'layered_hybrid_motion',**extra}
    (OUT/'status.json').write_text(json.dumps(value,indent=2));(ROOT/'status.json').write_text(json.dumps(value,indent=2))
    print('MOTION STATUS '+json.dumps(value),flush=True)

def intact(path):
    if not path.exists():return False
    data=path.read_bytes()
    return len(data)>32 and data[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',data[16:24])==(1920,1080) and data[-12:-4]==b'\x00\x00\x00\x00IEND'

def main():
    model=ROOT/'rainforest_hybrid_motion.blend'
    signature=hashlib.sha256(model.read_bytes()+Path(__file__).read_bytes()).hexdigest();stamp=OUT/'render_signature.json'
    if not stamp.exists() or json.loads(stamp.read_text())['sha256']!=signature:
        for p in FRAMES.glob('[0-9][0-9][0-9][0-9].png'):p.unlink()
        stamp.write_text(json.dumps({'sha256':signature},indent=2))
    update('validating_motion_rig')
    bpy.ops.wm.open_mainfile(filepath=str(model));s=bpy.context.scene
    assert s.frame_end==144 and s.render.fps==24 and s.render.resolution_x==1920 and s.cycles.samples==24
    assert s['generated_images_not_photographs'] and not s['fully_modeled_scene']
    leaf=bpy.data.objects['Flexible foreground palms — anchored top and right'];basis=leaf.data.shape_keys.key_blocks['Basis']
    keys=[k for k in leaf.data.shape_keys.key_blocks if k!=basis]
    anchors=[i for i,v in enumerate(basis.data) if abs(v.co.x-8)<1e-6 or abs(v.co.y-4.5)<1e-6]
    root_drift=max((k.data[i].co-basis.data[i].co).length for k in keys for i in anchors)
    assert root_drift<1e-6
    states=[]
    for f in [1,37,73,109,144]:
        s.frame_set(f);deps=bpy.context.evaluated_depsgraph_get();rain=bpy.data.objects['Fine rain behind cabin'].evaluated_get(deps).to_mesh()
        centers=[sum(rain.vertices[v].co.y for v in p.vertices)/4 for p in rain.polygons]
        counts=[sum(a<=y<b for y in centers) for a,b in [(-4.5,-1.5),(-1.5,1.5),(1.5,4.5)]]
        assert min(counts)>1200,counts
        states.append({'frame':f,'leaf_key_values':[k.value for k in keys],'rain_counts_bottom_middle_top':counts,'rain_first_center_y':centers[0]})
        bpy.data.objects['Fine rain behind cabin'].evaluated_get(deps).to_mesh_clear()
    assert len(set(round(x['rain_first_center_y'],5) for x in states))==5
    rig={'anchored_vertices':len(anchors),'maximum_root_drift_scene_units':root_drift,'timeline_samples':states,'packed_images':sum(bool(im.packed_file) for im in bpy.data.images if im.source=='FILE')}
    (ROOT/'research/hybrid_motion/rig_checks.json').write_text(json.dumps(rig,indent=2))
    initial=sum(intact(FRAMES/f'{i:04d}.png') for i in range(1,145));start=time.monotonic();done=0
    for f in range(1,145):
        path=FRAMES/f'{f:04d}.png'
        if intact(path):continue
        extra={'current_frame':f,'completed_frames':initial+done,'total_frames':144,'resolution':[1920,1080],'fps':24,'samples':24}
        if done:extra['estimated_seconds_remaining']=round((time.monotonic()-start)/done*(144-initial-done))
        update('rendering_hybrid_motion',**extra)
        s.frame_set(f);s.render.filepath=str(path);bpy.ops.render.render(write_still=True);assert intact(path)
        done+=1
    update('encoding_hybrid_motion',completed_frames=144,total_frames=144)
    movie=OUT/'preview.mp4'
    subprocess.run(['ffmpeg','-y','-v','error','-framerate','24','-start_number','1','-i',str(FRAMES/'%04d.png'),'-frames:v','144','-c:v','libx264','-preset','slow','-crf','16','-g','48','-keyint_min','48','-sc_threshold','0','-x264-params','open-gop=0','-video_track_timescale','12288','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(movie)],check=True)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(movie)]))
    stream=next(x for x in probe['streams'] if x['codec_type']=='video')
    assert stream['nb_read_frames']=='144' and stream['r_frame_rate']=='24/1' and float(probe['format']['duration'])==6
    assert stream['width']==1920 and stream['height']==1080
    subprocess.run(['ffmpeg','-v','error','-i',str(movie),'-f','null','-'],check=True)
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(movie),'-f','framemd5','-'],text=True)
    hashes=[line.rsplit(',',1)[-1].strip() for line in raw.splitlines() if line and not line.startswith('#')]
    assert len(hashes)==144 and len(set(hashes))==144
    # Native pixel crops: no upscaling, interpolation or synthetic motion.
    for name,crop in [('palms_detail','920:780:1000:0'),('water_detail','720:300:960:780')]:
        subprocess.run(['ffmpeg','-y','-v','error','-i',str(movie),'-vf','crop='+crop,'-c:v','libx264','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(OUT/(name+'.mp4'))],check=True)
    import shutil
    shutil.copyfile(FRAMES/'0001.png',OUT/'still.png')
    movements=['deforming foreground palm layer',s.get('river_method','masked water UV advection'),'independently recycling optical rain geometry','falling eave runoff']
    if any(o.name.startswith('Short stream impact ') for o in s.objects):movements.append('expanding stream impact rings')
    qa={'decoded_cleanly':True,'resolution':[1920,1080],'fps':24,'frames':144,'duration_seconds':6,'distinct_decoded_pixel_frames':len(set(hashes)),'native_frames_not_interpolated':True,'cycles_samples':24,'audio':False,'seamless_loop':False,'generated_layered_background':True,'rendered_motion':movements,'static_elements':s['static_elements'],'elapsed_seconds':round(time.monotonic()-start,2),'preview_sha256':hashlib.sha256(movie.read_bytes()).hexdigest()}
    (OUT/'qa.json').write_text(json.dumps(qa,indent=2))
    update('complete',completed_frames=144,total_frames=144,output='renders/hybrid_motion/preview.mp4',elapsed_seconds=qa['elapsed_seconds'])
    print('HYBRID MOTION PREVIEW COMPLETE',flush=True)

try:main()
except BaseException as e:traceback.print_exc();update('failed',error=str(e));os._exit(1)
os._exit(0)
