"""Fetch only public CC0 Poly Haven sources; verify provider checksums."""
from pathlib import Path
import concurrent.futures, hashlib, json, urllib.request

ROOT = Path(__file__).resolve().parents[1]
MODELS = ['fern_02', 'calathea_orbifolia_01', 'anthurium_botany_01',
          'pachira_aquatica_01', 'island_tree_02', 'rock_moss_set_01', 'shrub_04']
MATERIALS = ['weathered_plank_siding', 'grey_roof_tiles', 'forest_ground_04', 'palm_bark']

def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={
        'User-Agent': 'RainforestCabinStudy/1.0'}), timeout=90).read()

def metadata(name):
    p = ROOT / 'research' / ('files_' + name + '.json')
    if not p.exists():
        p.write_bytes(fetch('https://api.polyhaven.com/files/' + name))
    return json.loads(p.read_text())

jobs = []
for name in MODELS:
    entry = metadata(name)['gltf']['2k']['gltf']
    jobs.append((ROOT/'assets'/name/(name+'.gltf'), entry))
    jobs.extend((ROOT/'assets'/name/key, value) for key, value in entry['include'].items())
for name in MATERIALS:
    d = metadata(name)
    for kind in ['Diffuse', 'nor_gl', 'Rough', 'Displacement']:
        if kind in d:
            e = d[kind]['2k']['jpg']
            jobs.append((ROOT/'assets'/name/(kind+'.jpg'), e))

# glTF JPEG colour maps cannot carry alpha: separate masks are mandatory.
for name in ['fern_02','calathea_orbifolia_01','anthurium_botany_01','shrub_04']:
    d=metadata(name)
    for kind in ['Alpha','Diffuse','nor_gl','Rough']:
        ext='png' if kind=='Alpha' else 'jpg'
        jobs.append((ROOT/'assets'/name/'hero_maps'/(kind+'.'+ext),d[kind]['4k'][ext]))
for name in ['island_tree_02','pachira_aquatica_01']:
    jobs.append((ROOT/'assets'/name/'hero_maps'/'leaves_alpha.png',metadata(name)['leaves_alpha']['2k']['png']))

def download(job):
    path, entry = job
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and hashlib.md5(path.read_bytes()).hexdigest() == entry['md5']:
        return str(path.relative_to(ROOT)) + ' verified existing'
    data = fetch(entry['url'])
    assert hashlib.md5(data).hexdigest() == entry['md5'], path
    path.write_bytes(data)
    return str(path.relative_to(ROOT)) + ' verified downloaded'

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for result in executor.map(download, jobs):
            print(result, flush=True)
    (ROOT/'assets'/'CREDITS.txt').write_text(
        'Poly Haven CC0 1.0 models and PBR materials.\n'
        'Licence: https://polyhaven.com/license\n' +
        '\n'.join('https://polyhaven.com/a/' + name for name in MODELS+MATERIALS) +
        '\nProvider manifests retained in research; downloaded files MD5 verified.\n'
        'Cabin, terrain, water surface, palm geometry and rain: original procedural geometry.\n'
        'The user supplied the visual reference in chat; it is not used as a render texture.\n')
