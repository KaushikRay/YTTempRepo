"""Equal-camera neutral-light inspection of the imported leaf silhouettes."""
import bpy, os
from pathlib import Path
from mathutils import Vector

root=Path(__file__).resolve().parents[1]
before=os.environ.get('BEFORE')=='1'
folder=Path('/tmp/foliage-baseline') if before else root/'assets'
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene
for asset,x,h in [('fern_02',-1.2,.56),('calathea_orbifolia_01',0,.68),('anthurium_botany_01',1.15,.64)]:
    with bpy.data.libraries.load(str(folder/(asset+'.blend')),link=True) as (src,dst):dst.collections=[asset+'_a']
    ob=bpy.data.objects.new(asset,None);ob.instance_type='COLLECTION';ob.instance_collection=dst.collections[0];s.collection.objects.link(ob);ob.location=(x,0,0);ob.scale=(h,h,h)
s.world=bpy.data.worlds.new('Neutral photographic inspection');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.38,.38,.38,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.6
bpy.ops.mesh.primitive_plane_add(size=200);ground=bpy.context.object
m=bpy.data.materials.new('Neutral grey');m.diffuse_color=(.16,.16,.16,1);ground.data.materials.append(m)
data=bpy.data.lights.new('Large softbox','AREA');data.energy=240;data.size=4
ob=bpy.data.objects.new('Large softbox',data);s.collection.objects.link(ob);ob.location=(-1,-2.4,4);ob.rotation_euler=(Vector((0,0,.3))-ob.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.object.camera_add(location=(.0,-4.1,2.0));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,.32))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=3.65;s.camera=cam
s.render.engine='CYCLES';s.cycles.samples=48;s.cycles.use_denoising=True;s.cycles.transparent_max_bounces=20
s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=1200;s.render.resolution_y=520;s.render.resolution_percentage=100
s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast'
s.render.image_settings.file_format='PNG';s.render.filepath=str(root/'renders'/('leaves_before.png' if before else 'leaves_after.png'))
bpy.ops.render.render(write_still=True)
print('LEAF INSPECTION COMPLETE',flush=True);os._exit(0)
