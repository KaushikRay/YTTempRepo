import urllib.request,json,hashlib,concurrent.futures
from pathlib import Path
r=Path(__file__).resolve().parents[1]/'assets/dressing';names=['metal_jug','wooden_bowl_02','dry_branches_medium_01','food_apple_01','carved_wooden_plate'];jobs=[]
def get(url):return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'TavernDetailStudy/1.0'}),timeout=60).read()
for name in names:
 p=r/(name+'.json');d=json.loads(p.read_text()) if p.exists() else json.loads(get('https://api.polyhaven.com/files/'+name));p.write_text(json.dumps(d,indent=2));e=d['gltf']['2k']['gltf'];jobs.append((r/name/(name+'.gltf'),e));jobs.extend((r/name/k,v) for k,v in e['include'].items())
def dl(job):
 p,e=job;p.parent.mkdir(parents=True,exist_ok=True);data=get(e['url']);assert hashlib.md5(data).hexdigest()==e['md5'];p.write_bytes(data);return str(p.relative_to(r))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for p in pool.map(dl,jobs):print('Verified',p,flush=True)
(r/'CREDITS.txt').write_text('Poly Haven CC0 assets: '+', '.join(names)+'\nhttps://polyhaven.com/license\nAsset pages: https://polyhaven.com/a/<asset-id>\nOriginal manifests retained; provider MD5 checked on download.\n')

(r/'CREDITS.txt').write_text((r/'CREDITS.txt').read_text()+'\nDerived fire_rgb_24.mp4 is CC BY 3.0, not CC0. Required original attribution:\n'+(r.parent/'fire/CREDITS.txt').read_text())
