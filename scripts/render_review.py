"""Optional clean review render using the official bpy 4.5.3 LTS Python wheel."""
import bpy,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'storm_lounge.blend'))
s=bpy.context.scene;s.render.threads_mode='FIXED';s.render.threads=5;s.cycles.device='CPU';s.cycles.samples=int(os.environ.get('LOUNGE_SAMPLES','96'));s.cycles.use_denoising=True;s.cycles.denoiser='OPENIMAGEDENOISE';s.render.resolution_percentage=int(os.environ.get('LOUNGE_PREVIEW_PERCENT','100'));s.render.filepath=os.path.join(ROOT,'renders','composition.png')
print('PROGRESS: official Blender 4.5.3 CPU render with OpenImageDenoise',flush=True)
bpy.ops.render.render(write_still=True)

# Render a separate view for judging actual candle scale, wick and wax detail.
if os.environ.get('LOUNGE_DETAIL','0')=='1':
 from mathutils import Vector
 cam=s.camera;cam.location=(1.8,-4.65,1.55);cam.rotation_euler=(Vector((.65,-2.15,1.13))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=65
 s.render.resolution_x=960;s.render.resolution_y=720;s.render.resolution_percentage=100;s.cycles.samples=96;s.render.filepath=os.path.join(ROOT,'renders','candle_detail.png');bpy.ops.render.render(write_still=True)
