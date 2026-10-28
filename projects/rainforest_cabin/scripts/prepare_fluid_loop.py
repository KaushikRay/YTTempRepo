"""Loop the liquid in 3D scalar-field space, never by dissolving rendered images.

The first second blends the continued tail (frames 289..312) into frames 1..24.
Both contributions flow forwards. Smoothstep gives zero endpoint weight slope.
This is an artistic periodic surface, not a periodic solution of fluid dynamics.
Original particle states remain available for reproducibility and contact QA.
"""
import hashlib,json,shutil
from pathlib import Path
import numpy as np
from scipy.ndimage import gaussian_filter,map_coordinates
from scipy.spatial import cKDTree
from skimage.measure import marching_cubes

ROOT=Path(__file__).resolve().parents[1]
CACHE=ROOT/'assets/looped_fluid/meshes'
CFG=json.loads((ROOT/'assets/looped_fluid/channel.json').read_text())
FRAMES=288;OVERLAP=24;SPACING=.02;PARTICLE_SPACING=.03
SHAPE=np.ceil(np.array(CFG['bounds_m'])/SPACING).astype(int)+1

def fields(frame):
    with np.load(CACHE/f'particles_{frame:04d}.npz') as f:
        q=f['positions'];foam=f['foam']
    idx=np.floor(q/SPACING).astype(int)
    valid=np.all((idx>=0)&(idx<SHAPE),axis=1);idx=idx[valid];foam=foam[valid]
    density=np.zeros(SHAPE,np.float32);froth=np.zeros(SHAPE,np.float32)
    np.add.at(density,tuple(idx.T),1);np.add.at(froth,tuple(idx.T),foam)
    return gaussian_filter(density,1.05),gaussian_filter(froth,1.1)

def main():
    records=[]
    for frame in range(1,OVERLAP+1):
        a,fa=fields(FRAMES+frame);b,fb=fields(frame)
        t=(frame-1)/(OVERLAP-1);weight=t*t*(3-2*t)
        density=a*(1-weight)+b*weight;froth=fa*(1-weight)+fb*weight
        vertices,faces,normals,_=marching_cubes(density,.45*(SPACING/PARTICLE_SPACING)**3,
            spacing=(SPACING,)*3,allow_degenerate=False)
        foam=map_coordinates(froth/np.maximum(density,1e-6),(vertices/SPACING).T,order=1,mode='nearest')
        target=CACHE/f'liquid_{frame:04d}.npz'
        np.savez_compressed(target,vertices=vertices.astype(np.float32),faces=faces.astype(np.int32),foam=foam.astype(np.float32))
        # Preserve the original particle-based bubble density at the endpoints.
        # Select a stable weighted subset from each forwards-moving particle set,
        # then project to the newly reconstructed exposed surface.
        normals=np.zeros_like(vertices)
        face_normals=np.cross(vertices[faces[:,1]]-vertices[faces[:,0]],vertices[faces[:,2]]-vertices[faces[:,0]])
        for corner in range(3):np.add.at(normals,faces[:,corner],face_normals)
        normals/=np.maximum(np.linalg.norm(normals,axis=1)[:,None],1e-12)
        sources=[]
        for source,is_head in [(FRAMES+frame,False),(frame,True)]:
            with np.load(CACHE/f'particles_{source:04d}.npz') as f:
                ids=np.flatnonzero(f['foam']>.3)[::2];rank=(ids*0.6180339887498949)%1
                keep=rank<weight if is_head else rank>=weight
                sources.append(f['positions'][ids[keep]])
        positions=np.concatenate(sources);distance,near=cKDTree(vertices).query(positions,workers=1)
        valid=(distance<.04)&(normals[near,2]>0);near=near[valid]
        points=vertices[near]+normals[near]*.002
        np.savez_compressed(CACHE/f'foam_points_{frame:04d}.npz',positions=points.astype(np.float32))
        records.append({'frame':frame,'tail_frame':FRAMES+frame,'head_weight':weight,'vertices':len(vertices),'foam_points':len(points),'sha256':hashlib.sha256(target.read_bytes()).hexdigest()})
    # The input NPZs survive; only rendered meshes 1..24 are loop conditioned.
    simulation=json.loads((ROOT/'research/looped_fluid/simulation.json').read_text())
    report={'frames':FRAMES,'fps':24,'duration_seconds':12,'overlap_frames':OVERLAP,
        'water_playback_rate':simulation.get('water_playback_rate',1),'simulation_sampling_fps':simulation.get('simulation_sampling_fps',24),
        'method':'3D density/froth scalar-field smoothstep blend, remeshed before rendering',
        'rendered_image_crossfade':False,'frame_interpolation':False,
        'periodic_fluid_dynamics_solution':False,'approximate_loop_conditioning':True,
        'physics_bake_frames':312,'unchanged_mesh_frames':[25,288],
        'rain_period_seconds':12,'palm_period_seconds':6,'transition':records}
    (ROOT/'research/looped_fluid/loop.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k!='transition'},indent=2))

if __name__=='__main__':main()
