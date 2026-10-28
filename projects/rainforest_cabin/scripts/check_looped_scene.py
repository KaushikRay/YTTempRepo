"""Relocated playback and native rain/palm periodicity checks, without raw caches."""
import bpy,json,os,shutil,tempfile,traceback
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def evaluated_positions(ob):
    ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh()
    points=np.empty(len(mesh.vertices)*3,np.float32);mesh.vertices.foreach_get('co',points);ev.to_mesh_clear()
    return points.reshape(-1,3)

def main():
    with tempfile.TemporaryDirectory(prefix='looped-fluid-portability-',dir='/tmp') as folder:
        dest=Path(folder)
        files=['rainforest_looped_fluid.blend','scripts/integrated_fluid_scene.py','assets/looped_fluid/channel.json',
            'assets/integrated_fluid/upstream_instance.json','assets/realism/rainforest_trail/rainforest_trail.hdr']
        files += [f'assets/looped_fluid/fluid_cache_{i:02d}.zip' for i in range(1,13)]
        for name in files:
            target=dest/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/name,target)
        (dest/'renders').mkdir(exist_ok=True)
        bpy.ops.wm.open_mainfile(filepath=str(dest/'rainforest_looped_fluid.blend'));s=bpy.context.scene
        assert s.frame_end==288 and s.render.resolution_x==1920 and s.cycles.samples==32
        exec(bpy.data.texts['ENABLE_INTEGRATED_FLUID_PLAYBACK.py'].as_string(),{})
        names=['Fine rain behind cabin','Near rain in front of cabin','Roof runoff falling beads','Flexible foreground palms — anchored top and right']
        s.frame_set(1);bpy.context.view_layer.update();first={name:evaluated_positions(bpy.data.objects[name]) for name in names}
        s.frame_set(289);bpy.context.view_layer.update();errors={name:float(np.max(np.abs(evaluated_positions(bpy.data.objects[name])-first[name]))) for name in names}
        assert max(errors.values())<.0001,errors
        samples=[]
        for frame in [1,12,24,25,144,264,288,289]:
            s.frame_set(frame);bpy.context.view_layer.update();body=bpy.data.objects['Simulated liquid']
            assert body.data==bpy.data.objects['Upstream instance of simulated liquid'].data
            samples.append({'frame':frame,'liquid_vertices':len(body.data.vertices),'foam_points':len(bpy.data.objects['Simulation foam microbubbles'].data.vertices)})
        water=bpy.data.materials['True liquid surface with simulation-derived foam']
        assert not any(n.bl_idname=='ShaderNodeTexImage' for n in water.node_tree.nodes)
        assert not any(im.users and im.source=='MOVIE' for im in bpy.data.images)
        external=[]
        for im in bpy.data.images:
            if im.users and im.source=='FILE' and not im.packed_file:
                path=Path(bpy.path.abspath(im.filepath));assert path.is_relative_to(dest) and path.is_file();external.append(str(path.relative_to(dest)))
        result={'relocated_playback_from_archives':True,'raw_mesh_files_used':False,'frames':288,'native_resolution':[1920,1080],
            'samples':32,'rain_and_palm_repeat_position_error_local_m':errors,'timeline_samples':samples,
            'water_image_textures':0,'used_movies':0,'upstream_shares_simulation':True,'resolved_external_images':external,
            'water_transition_is_artistic_not_periodic_physics':True}
        (ROOT/'research/looped_fluid/scene_checks.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)

if __name__=='__main__':
    try:main()
    except BaseException:traceback.print_exc();os._exit(1)
    os._exit(0)
