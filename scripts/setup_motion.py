"""Patch the current still scene for a 3 s motion study; keep a 24 fps timeline."""
import bpy,os,json,math,random
from pathlib import Path
from mathutils import Matrix,Vector
root=Path(__file__).resolve().parents[1];random.seed(417)
bpy.ops.wm.open_mainfile(filepath=str(root/'storm_lounge.blend'))
s=bpy.context.scene;sequence=json.loads((root/'assets/fire/sequence/sequence.json').read_text())
if sequence['frame_count']!=72 or sequence['fps']!=24:raise RuntimeError('Unexpected fire sequence timing')
s.render.fps=24;s.frame_start=1;s.frame_end=72;s.frame_set(1)
mat=bpy.data.materials['Licensed filmed fire'];tex=next(n for n in mat.node_tree.nodes if n.type=='TEX_IMAGE')
image=bpy.data.images.load(str(root/'assets/fire/sequence/fire_0001.png'),check_existing=False);image.source='SEQUENCE';image.filepath='//assets/fire/sequence/fire_0001.png';tex.image=image;tex.image_user.frame_duration=72;tex.image_user.frame_start=1;tex.image_user.frame_offset=0;tex.image_user.use_auto_refresh=True;tex.image_user.use_cyclic=False
# Update existing credit text: animation uses processed frames from the same source.
credit=bpy.data.texts.get('FIRE_ASSET_CREDITS.txt')
if credit:credit.write('\nMotion study: frames from source seconds 2–5, temporally keyed and resampled to 24 fps. Not a seamless loop.\n')
# Real source brightness drives gently smoothed illumination, rather than unrelated flicker.
flux=sequence['flux'];mean=sum(flux)/len(flux);energy=360;fire=bpy.data.objects.get('Hearth firelight')
if not fire:raise RuntimeError('Missing hearth practical light')
fire.data.animation_data_clear()
for i,f in enumerate(flux,1):
 target=360*max(.7,min(1.3,f/mean));energy=.65*energy+.35*target;fire.data.energy=energy;fire.data.keyframe_insert(data_path='energy',frame=i)
# Each rain streak wraps at its own phase; no whole-field jump every two seconds.
rain_count=0
for ob in bpy.data.objects:
 if not ob.name.startswith('Visible wind-driven storm rain'):continue
 ob.animation_data_clear();x,y,z=ob.location;cx=-2.2 if abs(x+2.2)<abs(x-.1) else .1
 drv=ob.driver_add('location',2).driver;drv.expression=f'1.05+(({z-1.05:.7f}-(frame-1)*.20)%6.2)'
 drv=ob.driver_add('location',0).driver;drv.expression=f'{cx:.3f}+(({x-cx+.88:.7f}-(frame-1)*.008)%1.76)-.88';rain_count+=1
# Sliding droplets remain on the glass rather than moving into the room.
for ob in bpy.data.objects:
 if ob.name.startswith('Window rain droplet'):
  z=ob.location.z;speed=random.uniform(.002,.006);ob.driver_add('location',2).driver.expression=f'1.2+(({z-1.2:.7f}-(frame-1)*{speed:.7f})%4.45)'
 if ob.name.startswith('Window rain rivulet'):
  phase=random.uniform(0,math.tau);ob.data.driver_add('bevel_factor_end').driver.expression=f'.85+.15*sin(frame*.12+{phase:.6f})'
# Independent candle motion and illumination. No synchronized room-wide pulsing.
candles=0
for ob in bpy.data.objects:
 if ob.name.startswith('Small volumetric candle flame'):
  ob.animation_data_clear();phase=random.uniform(0,math.tau)
  ob.driver_add('rotation_euler',1).driver.expression=f'.07*sin(frame*.36+{phase:.6f})+.025*sin(frame*.79+{phase:.6f})'
  ob.driver_add('rotation_euler',0).driver.expression=f'.035*sin(frame*.29+{phase:.6f})'
  ob.driver_add('scale',2).driver.expression=f'1+.06*sin(frame*.43+{phase:.6f})';candles+=1
 if ob.name.startswith('Candle glow'):
  ob.data.animation_data_clear();phase=random.uniform(0,math.tau);base=ob.data.energy
  ob.data.driver_add('energy').driver.expression=f'{base:.5f}*(1+.12*sin(frame*.37+{phase:.6f})+.04*sin(frame*.83+{phase:.6f}))'
# Correct the inherited parent inverse so exterior trees rotate about their roots,
# not around doubled world translations, then add slower gust-driven sway.
trees=0
for pivot in bpy.data.objects:
 if not pivot.name.startswith('Wind driven tree'):continue
 for child in pivot.children:child.matrix_parent_inverse=Matrix.Translation(-Vector(pivot.location))
 pivot.animation_data_clear();phase=random.uniform(0,math.tau)
 pivot.driver_add('rotation_euler',1).driver.expression=f'.035*sin(frame*.065+{phase:.6f})+.012*sin(frame*.17+{phase:.6f})'
 pivot.driver_add('rotation_euler',0).driver.expression=f'.012*sin(frame*.079+{phase:.6f})';trees+=1
s.frame_set(1);s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100
# Scene stays compatible with Blender 4.3; the separate review renderer denoises.
bpy.ops.wm.save_as_mainfile(filepath=str(root/'storm_lounge.blend'))
report={'scene_fps':24,'scene_frames':72,'duration_seconds':3,'fire_sequence_frames':72,'rain_streaks':rain_count,'animated_candle_flames':candles,'exterior_tree_roots':trees,'seamless_loop':False}
(root/'renders/motion_setup.json').write_text(json.dumps(report,indent=2))
print('MOTION SETUP COMPLETE: '+json.dumps(report),flush=True)
