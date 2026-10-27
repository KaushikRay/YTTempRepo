"""Update just the river in the approved scene; verify palm data stays identical."""
import bpy,hashlib,json,os,traceback
from pathlib import Path
from river_flow import install_river
root=Path(__file__).resolve().parents[1]
def palm_hash():
    ob=bpy.data.objects['Flexible foreground palms — anchored top and right']
    data={'vertices':[tuple(v.co) for v in ob.data.vertices],
          'shape_keys':{k.name:{'positions':[tuple(v.co) for v in k.data]} for k in ob.data.shape_keys.key_blocks},
          'drivers':[d.driver.expression for d in ob.data.shape_keys.animation_data.drivers]}
    return hashlib.sha256(json.dumps(data).encode()).hexdigest()
try:
    bpy.ops.wm.open_mainfile(filepath=str(root/'rainforest_hybrid_motion.blend'));s=bpy.context.scene
    before=palm_hash();report=install_river(root);after=palm_hash();assert before==after
    previous=root/'research/hybrid_motion/setup.json'
    if previous.exists():
        metadata=json.loads(previous.read_text());metadata.update(method=s['render_method'],water_patches=len(report['patches']),impact_rings=0,river_method=s['river_method'],external_movie='assets/river_flow/real_rapids.mp4',static_elements=s['static_elements'])
        previous.write_text(json.dumps(metadata,indent=2))
    report.update(palm_sha256_before=before,palm_sha256_after=after,palm_data_identical=True)
    (root/'research/river_flow/palm_preservation.json').write_text(json.dumps({k:report[k] for k in ['palm_sha256_before','palm_sha256_after','palm_data_identical']},indent=2))
    s.render.use_border=False;s.render.use_crop_to_border=False;s.render.filepath='//renders/river_flow/still.png';s.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=str(root/'rainforest_hybrid_motion.blend'),compress=True)
    if os.environ.get('DIAGNOSTIC'):
        s.render.use_border=True;s.render.use_crop_to_border=True;s.render.border_min_x=(720+.001)/1920;s.render.border_max_x=(1760+.001)/1920;s.render.border_min_y=0;s.render.border_max_y=(400+.001)/1080
        s.frame_set(int(os.environ.get('TEST_FRAME','24')));s.render.filepath=str(root/'renders/river_flow/diagnostic.png');bpy.ops.render.render(write_still=True)
    print('RIVER UPDATE COMPLETE',json.dumps({'palm_data_identical':True,'river_masks':len(report['patches'])}),flush=True)
except BaseException:traceback.print_exc();os._exit(1)
os._exit(0)
