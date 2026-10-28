"""A modest, hue-preserving exposure finish. No spatial or temporal edits."""
import hashlib,json,subprocess
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'renders/production_test'
LUT=ROOT/'assets/colour/storm_dusk.cube'

def grade(rgb):
    linear=np.where(rgb<=.04045,rgb/12.92,((rgb+.055)/1.055)**2.4)
    peak=linear.max(axis=-1,keepdims=True);t=np.clip((peak-.4)/.6,0,1);protect=t*t*(3-2*t)
    gain=2**(-.55)+(0.9-2**(-.55))*protect
    result=linear*gain
    return np.where(result<=.0031308,result*12.92,1.055*np.maximum(result,0)**(1/2.4)-.055)

def main():
    LUT.parent.mkdir(parents=True,exist_ok=True);size=33
    with LUT.open('w') as f:
        f.write('TITLE "Rainforest storm: -0.55 EV with gentle highlight protection"\nLUT_3D_SIZE 33\nDOMAIN_MIN 0 0 0\nDOMAIN_MAX 1 1 1\n')
        for b in np.linspace(0,1,size):
            for g in np.linspace(0,1,size):
                for r in np.linspace(0,1,size):
                    values=grade(np.array([[r,g,b]],np.float64))[0];f.write(' '.join(f'{x:.9f}' for x in values)+'\n')
    frames=ROOT/'renders/looped_fluid/frames';native=all((frames/f'{f:04d}.png').exists() for f in range(1,289))
    inputs=['-framerate','24','-i',str(frames/'%04d.png')] if native else ['-i',str(ROOT/'renders/looped_fluid/preview.mp4')]
    target=OUT/'graded_loop.mp4'
    subprocess.run(['ffmpeg','-y','-v','error',*inputs,'-vf',f'lut3d=file={LUT}:interp=tetrahedral','-frames:v','288',
        '-c:v','libx264','-preset','slow','-crf','16','-g','48','-keyint_min','48','-sc_threshold','0','-x264-params','open-gop=0',
        '-r','24','-video_track_timescale','12288','-pix_fmt','yuv420p','-profile:v','high','-level','4.1','-an','-movflags','+faststart',str(target)],check=True)
    # QA images are direct frames from the finishing pipeline.
    source=frames/'0144.png' if native else ROOT/'renders/looped_fluid/still.png'
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(source),'-vf',f'lut3d=file={LUT}:interp=tetrahedral','-frames:v','1',str(OUT/'darker_still.png')],check=True)
    subprocess.run(['ffmpeg','-y','-v','error','-i',str(source),'-i',str(OUT/'darker_still.png'),
        '-filter_complex','[0:v]scale=960:540[a];[1:v]scale=960:540[b];[a][b]hstack=inputs=2','-frames:v','1','-q:v','2',str(OUT/'brightness_comparison.jpg')],check=True)
    report={'exposure_ev_shadows_and_midtones':-.55,'highlight_max_linear_gain':.9,'method':'sRGB-linear exposure with smooth peak-highlight protection; 33-cube tetrahedral LUT',
        'spatial_edits':False,'temporal_edits':False,'lightning_added':False,'motion_speed_changed':False,'fps':24,'frames':288,
        'input_was_native_png_cache':native,'lut':'assets/colour/storm_dusk.cube','lut_sha256':hashlib.sha256(LUT.read_bytes()).hexdigest(),
        'output':'renders/production_test/graded_loop.mp4','output_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
        'comparison_order':'Previous on left; darker finish on right','blender_source_geometry_materials_unchanged':True}
    (OUT/'grade_report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))

if __name__=='__main__':main()
