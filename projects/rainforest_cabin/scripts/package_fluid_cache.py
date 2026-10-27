"""Package the delivered 48 geometry frames; raw solver particles stay local."""
import hashlib,json,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];CACHE=ROOT/'assets/fluid_river/meshes'
records=[]
for chunk in [1,2]:
 target=ROOT/f'assets/fluid_river/fluid_cache_{chunk:02d}.zip'
 with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_STORED) as archive:
  for frame in range((chunk-1)*24+1,chunk*24+1):
   for kind in ['liquid','foam_points']:
    path=CACHE/f'{kind}_{frame:04d}.npz';assert path.is_file(),path
    data=path.read_bytes();archive.writestr(path.name,data);records.append({'archive':target.name,'file':path.name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
 assert target.stat().st_size<100*1024**2
 print(target.name,round(target.stat().st_size/1024**2,2),'MiB')
manifest={'published_geometry_frames':48,'fps':24,'duration_seconds':2,'total_local_simulation_frames_available':96,'archives':records,'water_motion_from_images_or_footage':False,
          'use':'Keep both ZIP files in assets/fluid_river. The provided Blender playback script reads them directly without extraction.'}
(ROOT/'assets/fluid_river/cache_manifest.json').write_text(json.dumps(manifest,indent=2))
