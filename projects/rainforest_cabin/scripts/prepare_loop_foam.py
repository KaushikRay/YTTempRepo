"""Prepare the exact base-scene surface-particle foam for archive/playback QA.

Independent Blender process; future frames first. Atomic writes allow the native
renderer to keep reading previously completed states during cache preparation.
"""
import bpy,os,traceback
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
ROOT=Path(__file__).resolve().parents[1];CACHE=ROOT/'assets/looped_fluid/meshes'

def main():
    count=0
    for frame in range(288,24,-1):
        target=CACHE/f'foam_points_{frame:04d}.npz'
        if target.exists():continue
        with np.load(CACHE/f'liquid_{frame:04d}.npz') as f:
            vertices=f['vertices'];faces=f['faces']
        mesh=bpy.data.meshes.new('Foam surface query');mesh.from_pydata(vertices,[],faces);mesh.update()
        normals=np.empty(len(vertices)*3,np.float32);mesh.vertices.foreach_get('normal',normals);normals=normals.reshape(-1,3)
        with np.load(CACHE/f'particles_{frame:04d}.npz') as f:
            ids=np.flatnonzero(f['foam']>.3)[::2];positions=f['positions'][ids]
        distance,near=cKDTree(vertices).query(positions,workers=1);valid=(distance<.04)&(normals[near,2]>0);near=near[valid]
        points=vertices[near]+normals[near]*.002
        temp=target.with_name(target.stem+f'.tmp-{os.getpid()}.npz')
        np.savez_compressed(temp,positions=points.astype(np.float32));os.replace(temp,target)
        bpy.data.meshes.remove(mesh);count+=1
    print('Prepared',count,'native foam states.',flush=True)

if __name__=='__main__':
    try:main()
    except BaseException:traceback.print_exc();os._exit(1)
    os._exit(0)
