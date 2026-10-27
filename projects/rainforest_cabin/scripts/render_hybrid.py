"""Clearly labelled hybrid Blender variant: generated matte + depth-masked 3D rain.

The plate contains static detailed architecture, foliage and water. This file
does not claim those details are modeled geometry or already animated.
"""
import bpy,json,os,time,traceback
from pathlib import Path

root=Path(__file__).resolve().parents[1]
def status(phase,**extra):
    value={'phase':phase,'pid':os.getpid(),'updated_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
           'variant':'hybrid_generated_matte_and_3D_rain','worker_running':phase not in ['complete','failed'],**extra}
    (root/'status.json').write_text(json.dumps(value,indent=2));print(json.dumps(value),flush=True)

def main():
    status('building_hybrid')
    bpy.ops.wm.open_mainfile(filepath=str(root/'rainforest_cabin.blend'));s=bpy.context.scene
    rain=bpy.data.collections['Continuously replenishing rain'];drops=set(rain.objects);holdouts=0
    for ob in s.objects:
        if ob.type=='CAMERA' or ob in drops:continue
        if ob.type=='LIGHT':ob.hide_render=True;continue
        if ob.name=='Forest depth mist':ob.hide_render=True;continue
        ob.is_holdout=True;holdouts+=1
    s.world.use_nodes=True;n=s.world.node_tree.nodes;n.clear();bg=n.new('ShaderNodeBackground');bg.inputs['Strength'].default_value=0;out=n.new('ShaderNodeOutputWorld');s.world.node_tree.links.new(bg.outputs[0],out.inputs[0])
    s.render.film_transparent=True;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA'
    s.view_settings.view_transform='Standard';s.view_settings.look='None';s.view_settings.exposure=0;s.view_settings.gamma=1
    s.render.engine='CYCLES';s.cycles.samples=int(os.environ.get('SAMPLES','32'));s.cycles.use_denoising=False
    s.cycles.max_bounces=2;s.cycles.transparent_max_bounces=32;s.cycles.use_adaptive_sampling=True;s.cycles.adaptive_threshold=.05;s.cycles.adaptive_min_samples=8
    s.render.threads_mode='FIXED';s.render.threads=4
    s.render.resolution_x=int(os.environ.get('WIDTH','1920'));s.render.resolution_y=round(s.render.resolution_x*9/16);s.render.resolution_percentage=100
    s.use_nodes=True;n=s.node_tree.nodes;l=s.node_tree.links;n.clear()
    plate=n.new('CompositorNodeImage');plate.name='AI-generated static photographic-style matte';plate.image=bpy.data.images.load(str(root/'assets/hybrid/matte_plate.png'),check_existing=True);plate.image.pack()
    scale=n.new('CompositorNodeScale');scale.space='RENDER_SIZE';scale.frame_method='CROP';l.new(plate.outputs['Image'],scale.inputs['Image'])
    rainlayer=n.new('CompositorNodeRLayers');rainlayer.name='Native 3D rain and geometric depth holdouts'
    weather_pass=n.new('CompositorNodeOutputFile');weather_pass.name='Inspect native rain separately from generated plate';weather_pass.base_path='//renders/hybrid_pass/'
    weather_pass.format.file_format='PNG';weather_pass.format.color_mode='RGBA';weather_pass.file_slots[0].path='rain_';l.new(rainlayer.outputs['Image'],weather_pass.inputs[0])
    over=n.new('CompositorNodeAlphaOver');over.inputs[0].default_value=1;l.new(scale.outputs[0],over.inputs[1]);l.new(rainlayer.outputs['Image'],over.inputs[2])
    final=n.new('CompositorNodeComposite');l.new(over.outputs[0],final.inputs[0])
    s['render_method']='Hybrid: AI-generated static matte with separately rendered 3D rain'
    s['camera_locked']=True;s['background_architecture_foliage_water_static']=True
    credit=bpy.data.texts.get('HYBRID_PROVENANCE') or bpy.data.texts.new('HYBRID_PROVENANCE');credit.clear();credit.write((root/'assets/hybrid/CREDITS.txt').read_text())
    output=os.environ.get('OUTPUT','hybrid_still.png');s.render.filepath='//renders/'+output;s.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(root/'rainforest_hybrid.blend'),compress=True)
    report={'generated_matte':True,'camera_photograph':False,'plate_static':True,'rain_rendered_in_3D':True,
            'background_wind_or_water_animated':False,'camera_locked':True,'native_rain_objects':len(drops),'proxy_holdout_objects':holdouts,
            'resolution':[s.render.resolution_x,s.render.resolution_y],'samples':s.cycles.samples,'source_model':'rainforest_cabin.blend'}
    (root/'research/realism/hybrid_setup.json').write_text(json.dumps(report,indent=2));status('rendering_hybrid',**report)
    bpy.ops.render.render(write_still=True)
    status('complete',output='renders/'+output,**report);print('HYBRID STILL COMPLETE',flush=True)

try:main()
except BaseException as exc:traceback.print_exc();status('failed',error=str(exc));os._exit(1)
os._exit(0)
