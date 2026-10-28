"""Package the 12-second loop's native mesh/foam states and QA samples."""
import hashlib,json,zipfile
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];ASSETS=ROOT/'assets/looped_fluid';CACHE=ASSETS/'meshes'

def main():
    records=[]
    for chunk in range(1,13):
        target=ASSETS/f'fluid_cache_{chunk:02d}.zip'
        with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_STORED) as archive:
            for frame in range((chunk-1)*24+1,chunk*24+1):
                for kind in ['liquid','foam_points']:
                    path=CACHE/f'{kind}_{frame:04d}.npz';data=path.read_bytes();archive.writestr(path.name,data)
                    records.append({'archive':target.name,'file':path.name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
        assert target.stat().st_size<100*1024**2
    samples={}
    for frame in [1,24,144,264,288,312]:
        with np.load(CACHE/f'particles_{frame:04d}.npz') as f:
            samples[f'positions_{frame:04d}']=f['positions'];samples[f'velocity_{frame:04d}']=f['velocity']
    np.savez_compressed(ASSETS/'solver_samples.npz',**samples)
    (ASSETS/'cache_manifest.json').write_text(json.dumps({'frames':288,'fps':24,'duration_seconds':12,
        'water_motion_from_images_or_footage':False,'archives':records,
        'first_24_meshes_loop_conditioned':True,'particles_are_unmodified_solver_samples':True},indent=2))
    print('Packaged 288 liquid and foam states in 12 verified-size archives.')

if __name__=='__main__':main()
