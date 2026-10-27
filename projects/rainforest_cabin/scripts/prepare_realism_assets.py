"""Additional CC0 photographic materials, ground scans and forest illumination."""
from pathlib import Path
import concurrent.futures,hashlib,json,urllib.request
root=Path(__file__).resolve().parents[1];folder=root/'assets'/'realism';research=root/'research'/'realism';folder.mkdir(exist_ok=True);research.mkdir(exist_ok=True)
models=['root_cluster_01','moss_01','bark_debris_01','wooden_bucket_01','wooden_lantern_01']
materials=['weathered_planks','old_planks_02','roof_planks','moss_wood','brown_mud_leaves_01','japanese_camphor_bark','river_small_rocks']
hdris=['rainforest_trail']
def get(url):return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'RainforestRealismStudy/1.0'}),timeout=90).read()
def metadata(name):
    p=research/('files_'+name+'.json')
    if not p.exists():p.write_bytes(get('https://api.polyhaven.com/files/'+name))
    return json.loads(p.read_text())
jobs=[]
for name in models:
    d=metadata(name);e=d['gltf']['2k']['gltf'];jobs.append((folder/name/(name+'.gltf'),e));jobs.extend((folder/name/k,v) for k,v in e['include'].items())
    if 'Alpha' in d:jobs.append((folder/name/'Alpha.png',d['Alpha']['2k']['png']))
for name in materials:
    d=metadata(name)
    for kind in ['Diffuse','Rough','nor_gl','Displacement']:
        if kind in d:jobs.append((folder/name/(kind+'.jpg'),d[kind]['4k']['jpg']))
for name in hdris:
    e=metadata(name)['hdri']['2k']['hdr'];jobs.append((folder/name/(name+'.hdr'),e))
def fetch(job):
    p,e=job;p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists() and hashlib.md5(p.read_bytes()).hexdigest()==e['md5']:return str(p.relative_to(root))+' verified existing'
    data=get(e['url']);assert hashlib.md5(data).hexdigest()==e['md5'],p;p.write_bytes(data)
    return str(p.relative_to(root))+' verified downloaded'
if __name__=='__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as ex:
        for result in ex.map(fetch,jobs):print(result,flush=True)
    (folder/'CREDITS.txt').write_text('Additional Poly Haven CC0 1.0 scans/materials/photographic HDRI.\nhttps://polyhaven.com/license\n'+
        '\n'.join('https://polyhaven.com/a/'+n for n in models+materials+hdris)+'\nProvider MD5 verified; original manifests retained under research/realism.\n')
