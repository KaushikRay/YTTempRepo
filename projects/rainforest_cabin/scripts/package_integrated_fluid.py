"""Publish 96 native mesh/foam states in four relative, verified cache archives."""
import hashlib,json,zipfile
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];ASSETS=ROOT/'assets/integrated_fluid';CACHE=ASSETS/'meshes';records=[]
for chunk in range(1,5):
 target=ASSETS/f'fluid_cache_{chunk:02d}.zip'
 with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_STORED) as archive:
  for frame in range((chunk-1)*24+1,chunk*24+1):
   for kind in ['liquid','foam_points']:
    p=CACHE/f'{kind}_{frame:04d}.npz';data=p.read_bytes();archive.writestr(p.name,data);records.append({'archive':target.name,'file':p.name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
 assert target.stat().st_size<100*1024**2
 print(target.name,round(target.stat().st_size/1024**2,2),'MiB')
samples={}
for frame in [1,24,48,72,96]:
 f=np.load(CACHE/f'particles_{frame:04d}.npz');samples[f'positions_{frame:04d}']=f['positions'];samples[f'velocity_{frame:04d}']=f['velocity']
np.savez_compressed(ASSETS/'solver_samples.npz',**samples)
(ASSETS/'cache_manifest.json').write_text(json.dumps({'frames':96,'fps':24,'duration_seconds':4,'water_motion_from_images_or_footage':False,'archives':records,'upstream_instance':'upstream_instance.json','channel':'channel.json','solver_samples':'solver_samples.npz'},indent=2))
