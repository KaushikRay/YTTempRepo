"""Prepare an anchored wind, creek and rainfall diagnostic from the cleared scene."""
import bpy, json, math, os, random
from pathlib import Path
from mathutils import Vector

root=Path(__file__).resolve().parents[1];out=root/'renders'/'motion';out.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(root/'rainforest_cabin.blend'));s=bpy.context.scene
s.frame_start=1;s.frame_end=96;s.render.fps=24;s.frame_set(1)

def expression(phase):
    return f'.65*(sin((frame-1)*.047+{phase:.9f})-sin({phase:.9f}))+.35*(sin((frame-1)*.083+{phase*1.7:.9f})-sin({phase*1.7:.9f}))'

anchors=[];flexed=[]
for leaf in sorted([o for o in bpy.data.objects if o.name.endswith('curved pinnae')],key=lambda o:o.name):
    prefix=leaf.name.removesuffix(' curved pinnae');rib=bpy.data.objects[prefix+' tapered rachis']
    base=Vector(rib.data.splines[0].points[0].co[:3]);rng=random.Random(prefix);phase=rng.uniform(0,2*math.pi)
    pivot=bpy.data.objects.new(prefix+' wind anchor',None);s.collection.objects.link(pivot);pivot.location=base
    # Both geometries were authored in world coordinates. Rebase without moving
    # any vertex at frame one; the petiole stays at the original stem attachment.
    for v in leaf.data.vertices:v.co-=base
    for sp in rib.data.splines:
        for point in sp.points:
            p=Vector(point.co[:3])-base;point.co=(*p,1)
    leaf.parent=pivot;rib.parent=pivot
    leaf.location=(0,0,0);rib.location=(0,0,0)
    for axis,amp in [(0,.005),(1,.007),(2,.004)]:
        pivot.driver_add('rotation_euler',axis).driver.expression=f'{amp}*({expression(phase+axis*.43)})'
    anchors.append({'object':pivot.name,'base':list(base)})
    # Foreground fronds additionally flex along their length, including the rib.
    if prefix.startswith(('Near right','Large foreground','Low foreground','Overhead')):
        leaf.shape_key_add(name='Basis');key=leaf.shape_key_add(name='Gentle frond flex');key.slider_min=-2;key.slider_max=2
        extent=max(v.co.length for v in leaf.data.vertices)
        for orig,target in zip(leaf.data.vertices,key.data):
            w=(orig.co.length/extent)**1.8;target.co=orig.co+Vector((.035,.012,.010))*w
        key.driver_add('value').driver.expression=expression(phase)
        for sp in rib.data.splines:
            for point in sp.points:
                original=Vector(point.co[:3]);w=min(1,original.length/extent)**1.8
                for axis,amp in [(0,.035),(1,.012),(2,.010)]:
                    point.driver_add('co',axis).driver.expression=f'{original[axis]:.10f}+{amp*w:.10f}*({expression(phase)})'
        flexed.append(leaf.name)

understory=[]
for ob in sorted(bpy.data.objects,key=lambda o:o.name):
    if not ob.name.startswith(('Wet understory','Dense fern bank','Foreground hero fern','Tropical middle canopy')):continue
    if ob.location.y>20:continue
    phase=random.Random(ob.name).uniform(0,2*math.pi)
    for axis,amp in [(0,.004),(1,.003)]:
        initial=ob.rotation_euler[axis];ob.driver_add('rotation_euler',axis).driver.expression=f'{initial:.10f}+{amp}*({expression(phase+axis*.7)})'
    understory.append(ob.name)

# Travelling geometric waves, expressed as sine/cosine deltas from the still.
water=bpy.data.objects['Continuous reflective creek surface'];water.shape_key_add(name='Basis')
refined='Cabin assembly slight oblique view' in bpy.data.objects
for name,amp,ky,kx,omega in [('Broad travelling wave',.003 if refined else .015,8,5,.27),('Fine travelling wave',.002 if refined else .008,17,-4,.39)]:
    for component in ['sine','cosine']:
        key=water.shape_key_add(name=name+' '+component);key.slider_min=-2;key.slider_max=2
        for vertex,target in zip(water.data.vertices,key.data):
            theta=vertex.co.y*ky+vertex.co.x*kx
            delta=amp*(math.sin(theta) if component=='sine' else math.cos(theta))
            target.co.z=vertex.co.z+delta
        key.driver_add('value').driver.expression=(f'cos((frame-1)*{omega})-1' if component=='sine' else f'-sin((frame-1)*{omega})')
mat=bpy.data.materials['Rain-agitated clear stream'];nodes=mat.node_tree.nodes
mapping=next(n for n in nodes if n.type=='MAPPING');mapping.inputs['Location'].driver_add('default_value',1).driver.expression='-(frame-1)*.0003'
noise=next(n for n in nodes if n.type=='TEX_NOISE');noise.noise_dimensions='4D';noise.inputs['W'].driver_add('default_value').driver.expression='(frame-1)*.007'

ripples=[]
for ob in sorted(bpy.data.objects,key=lambda o:o.name):
    if not ob.name.startswith('Rain impact ripple'):continue
    points=ob.data.splines[0].points;center=sum((Vector(p.co[:3]) for p in list(points)[:-1]),Vector())/(len(points)-1)
    for point in points:
        p=Vector(point.co[:3])-center;point.co=(*p,1)
    ob.location=center;rng=random.Random(ob.name);life=rng.randrange(19,38);offset=rng.randrange(life)
    age=f'((frame-1+{offset})%{life})/{life}'
    for axis in [0,1]:ob.driver_add('scale',axis).driver.expression=f'.12+1.65*({age})'
    ob.data.driver_add('bevel_depth').driver.expression=f'.002*(1-({age}))'
    ripples.append(ob.name)

runoff=[]
for ob in sorted(bpy.data.objects,key=lambda o:o.name):
    if not ob.name.startswith('Cabin eave runoff'):continue
    points=ob.data.splines[0].points;top=points[0].co.z;length=top-points[-1].co.z;phase=random.Random(ob.name).uniform(0,6.28)
    points[-1].driver_add('co',2).driver.expression=f'{top}-{length}*(.84+.16*sin((frame-1)*.21+{phase}))'
    runoff.append(ob.name)

s.render.use_motion_blur=False;s.render.use_persistent_data=True;s.cycles.use_animated_seed=False;s.cycles.seed=372
s.cycles.samples=12;s.cycles.adaptive_min_samples=8;s.cycles.adaptive_threshold=.06;s.cycles.sample_clamp_indirect=4
s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.render.threads_mode='FIXED';s.render.threads=4
s.render.filepath='//renders/motion/frames/';s.frame_set(1)
bpy.context.view_layer.update()
assert len(anchors)==51 and len(flexed)==11 and len(ripples) in [0,70] and len(runoff)==25
report={'duration_seconds':4,'fps':24,'frames':96,'resolution':[640,360],'cycles_samples':12,
        'anchored_palm_fronds':len(anchors),'flexible_foreground_fronds':len(flexed),
        'moving_understory_plants':len(understory),'recycling_impact_ripples':len(ripples),
        'variable_eave_runoff_strands':len(runoff),'rain_streaks':len(bpy.data.collections['Continuously replenishing rain'].objects),
        'camera_moves':False,'audio':False,'seamless_loop':False,'physical_fluid_or_wind_simulation':False,
        'anchors':anchors}
(out/'setup.json').write_text(json.dumps(report,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(root/'rainforest_motion.blend'),compress=True)
print('MOTION SETUP COMPLETE',json.dumps({k:v for k,v in report.items() if k!='anchors'}),flush=True)
os._exit(0)
