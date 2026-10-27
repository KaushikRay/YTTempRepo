"""Render native 24 fps frames, resume intact PNGs, encode and validate a short test."""
from pathlib import Path
import bpy, datetime, hashlib, json, os, struct, subprocess, time, traceback

root=Path(__file__).resolve().parents[1];out=root/'renders'/'motion';folder=out/'frames';folder.mkdir(parents=True,exist_ok=True)

def update(phase,**extra):
    value={'phase':phase,'updated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'pid':os.getpid(),'worker_running':phase not in ['complete','failed'],**extra}
    (out/'status.json').write_text(json.dumps(value,indent=2))
    (root/'status.json').write_text(json.dumps(value,indent=2))
    print('MOTION STATUS',json.dumps(value),flush=True)

def intact(path):
    if not path.exists():return False
    data=path.read_bytes()
    return len(data)>32 and data[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',data[16:24])==(640,360) and data[-12:-4]==b'\x00\x00\x00\x00IEND'

def main():
    model=root/'rainforest_motion.blend'
    digest=hashlib.sha256(model.read_bytes()+Path(__file__).read_bytes()).hexdigest()
    signature=out/'render_signature.json'
    if not signature.exists() or json.loads(signature.read_text())['sha256']!=digest:
        for p in folder.glob('[0-9][0-9][0-9][0-9].png'):p.unlink()
        signature.write_text(json.dumps({'sha256':digest},indent=2))
    bpy.ops.wm.open_mainfile(filepath=str(model));s=bpy.context.scene
    assert s.render.fps==24 and s.frame_end==96 and s.render.resolution_x==640 and s.cycles.samples==12
    start=time.monotonic();new_frames=0;initial=sum(intact(folder/f'{f:04d}.png') for f in range(1,97))
    for frame in range(1,97):
        path=folder/f'{frame:04d}.png'
        if intact(path):continue
        update('rendering_motion',current_frame=frame,completed_frames=initial+new_frames,total_frames=96,
               resolution=[640,360],fps=24,estimated_seconds_remaining=None if new_frames==0 else round((time.monotonic()-start)/new_frames*(96-initial-new_frames)))
        s.frame_set(frame);s.render.filepath=str(path);bpy.ops.render.render(write_still=True)
        assert intact(path),path
        new_frames+=1
        update('rendering_motion',current_frame=frame,completed_frames=initial+new_frames,total_frames=96,
               resolution=[640,360],fps=24,elapsed_seconds=round(time.monotonic()-start,2),
               estimated_seconds_remaining=round((time.monotonic()-start)/new_frames*(96-initial-new_frames)))
    update('encoding_motion',completed_frames=96,total_frames=96)
    movie=out/'preview.mp4'
    subprocess.run(['ffmpeg','-y','-v','error','-framerate','24','-start_number','1','-i',str(folder/'%04d.png'),
                    '-frames:v','96','-c:v','libx264','-crf','17','-g','48','-pix_fmt','yuv420p','-movflags','+faststart','-an',str(movie)],check=True)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(movie)]))
    v=next(x for x in probe['streams'] if x['codec_type']=='video')
    assert v['nb_read_frames']=='96' and v['r_frame_rate']=='24/1' and float(probe['format']['duration'])==4
    assert not any(x['codec_type']=='audio' for x in probe['streams'])
    subprocess.run(['ffmpeg','-v','error','-i',str(movie),'-f','null','-'],check=True)
    decoded=subprocess.check_output(['ffmpeg','-v','error','-i',str(movie),'-f','framemd5','-'],text=True)
    pixel_hashes=[line.rsplit(',',1)[-1].strip() for line in decoded.splitlines() if line and not line.startswith('#')]
    assert len(pixel_hashes)==96 and len(set(pixel_hashes))==96,'Decoded frames must contain changing pixels'
    hashes=[hashlib.sha256((folder/f'{i:04d}.png').read_bytes()).hexdigest() for i in range(1,97)]
    assert len(set(hashes))==96,'Expected 96 distinct native renders'
    report={'rendered_frames':96,'distinct_frame_hashes':len(set(hashes)),'distinct_decoded_pixel_frames':len(set(pixel_hashes)),'fps':24,'duration_seconds':4,
            'resolution':[640,360],'cycles_samples':12,'native_frames_not_interpolated':True,'audio':False,'seamless_loop':False,
            'decoded_cleanly':True,'preview_sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'frame_sha256':hashes}
    (out/'qa.json').write_text(json.dumps(report,indent=2))
    update('complete',completed_frames=96,total_frames=96,output='renders/motion/preview.mp4',render_elapsed_seconds=round(time.monotonic()-start,2))
    print('MOTION PREVIEW COMPLETE',flush=True)

try:
    main()
except BaseException as exc:
    traceback.print_exc();update('failed',error=str(exc));os._exit(1)
os._exit(0)
