"""Download a CC0 fir variant by byte ranges, retaining provenance.

The provider's glTF contains three trees in one 478 MB buffer. Only the C
variant is required here. Extract its complete accessor buffer views without
altering geometry; verify each HTTP Content-Range, size and stored SHA256.
Texture and source glTF downloads are checked against provider MD5 entries.
"""
import concurrent.futures,copy,hashlib,json,urllib.request
from pathlib import Path

root=Path(__file__).resolve().parents[1]/'assets/exterior'
agent={'User-Agent':'BlenderInteriorRealism/1.0'}
manifest=json.loads((root/'fir_tree_01-files.json').read_text())['gltf']['2k']['gltf']
source_bytes=(root/'fir_tree_01-source.gltf').read_bytes()
assert hashlib.md5(source_bytes).hexdigest()==manifest['md5']
source=json.loads(source_bytes);mesh=copy.deepcopy(source['meshes'][2]);folder=root/'fir_tree_01_c';folder.mkdir(parents=True,exist_ok=True)
accessor_ids=sorted({i for p in mesh['primitives'] for i in [*p['attributes'].values(),p['indices']]})
view_ids=sorted({source['accessors'][i]['bufferView'] for i in accessor_ids})
bin_entry=manifest['include']['fir_tree_01.bin'];range_records=[]

def read_view(index):
    view=source['bufferViews'][index];start=view.get('byteOffset',0);end=start+view['byteLength']-1
    req=urllib.request.Request(bin_entry['url'],headers={**agent,'Range':f'bytes={start}-{end}'})
    with urllib.request.urlopen(req,timeout=60) as response:
        assert response.status==206 and response.headers['Content-Range']==f'bytes {start}-{end}/{bin_entry["size"]}'
        data=response.read();assert len(data)==view['byteLength']
    return index,data,{'original_view':index,'start':start,'length':len(data),'sha256':hashlib.sha256(data).hexdigest()}

new_views=[];buf=bytearray();view_map={}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for index,data,record in pool.map(read_view,view_ids):
        while len(buf)%4:buf.append(0)
        view=copy.deepcopy(source['bufferViews'][index]);view['byteOffset']=len(buf);view['buffer']=0
        view_map[index]=len(new_views);new_views.append(view);buf.extend(data);range_records.append(record)
        print('Retrieved geometry range',index,len(data),flush=True)
accessor_map={old:new for new,old in enumerate(accessor_ids)};accessors=[]
for index in accessor_ids:
    accessor=copy.deepcopy(source['accessors'][index]);accessor['bufferView']=view_map[accessor['bufferView']];accessors.append(accessor)
for primitive in mesh['primitives']:
    primitive['attributes']={k:accessor_map[i] for k,i in primitive['attributes'].items()};primitive['indices']=accessor_map[primitive['indices']]
gltf=copy.deepcopy(source);gltf.update(meshes=[mesh],nodes=[{'mesh':0,'name':'fir_tree_01_c_LOD0'}],scenes=[{'nodes':[0],'name':'Fir C'}],scene=0,accessors=accessors,bufferViews=new_views,buffers=[{'uri':'fir_tree_01_c.bin','byteLength':len(buf)}])
(folder/'fir_tree_01_c.bin').write_bytes(buf);(folder/'fir_tree_01_c.gltf').write_text(json.dumps(gltf,separators=(',',':')))

def texture_download(job):
    name,entry=job;path=folder/name;path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists() and hashlib.md5(path.read_bytes()).hexdigest()==entry['md5']:return name+' cached'
    data=urllib.request.urlopen(urllib.request.Request(entry['url'],headers=agent),timeout=60).read();assert hashlib.md5(data).hexdigest()==entry['md5'];path.write_bytes(data);return name
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for name in pool.map(texture_download,[(k,v) for k,v in manifest['include'].items() if k!='fir_tree_01.bin']):print('Verified texture',name,flush=True)
provenance={'license':'CC0','source':'https://polyhaven.com/a/fir_tree_01','authors':json.loads((root/'fir_tree_01-info.json').read_text())['authors'],'geometry':'Complete variant C accessor views extracted by HTTP Range; no decimation','original_buffer_bytes':bin_entry['size'],'original_buffer_not_fully_downloaded':True,'subset_buffer_bytes':len(buf),'subset_buffer_sha256':hashlib.sha256(buf).hexdigest(),'range_records':range_records,'textures':'Provider MD5 checked','source_gltf':'Provider MD5 checked'}
(root/'provenance.json').write_text(json.dumps(provenance,indent=2))
print('EXTERIOR SOURCE PREPARATION COMPLETE',flush=True)
