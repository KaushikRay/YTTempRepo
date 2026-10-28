"""Fetch only the two already-licensed full recordings used by the long builder."""
import hashlib,json,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    sources=json.loads((ROOT/'assets/audio/sources.json').read_text())
    for name in ['rain','long_stream']:
        row=next(x for x in sources if x['name']==name);target=ROOT/row['original_file'];target.parent.mkdir(parents=True,exist_ok=True)
        expected=row.get('original_sha256',row.get('download_sha256'))
        if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest()==expected:continue
        temp=target.with_suffix(target.suffix+'.partial')
        with urllib.request.urlopen(urllib.request.Request(row['download_url'],headers={'User-Agent':'RainforestReleaseBuilder/1.0'}),timeout=60) as response,temp.open('wb') as out:
            while data:=response.read(1024*1024):out.write(data)
        assert hashlib.sha256(temp.read_bytes()).hexdigest()==expected,name
        temp.replace(target);print('Verified',name,flush=True)
if __name__=='__main__':main()
