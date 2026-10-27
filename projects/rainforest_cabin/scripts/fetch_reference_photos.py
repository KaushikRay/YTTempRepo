"""Re-download the curated real photograph references using retained metadata."""
from pathlib import Path
import hashlib,json,urllib.request
folder=Path(__file__).resolve().parents[1]/'research'/'forest_photographs'
for rec in json.loads((folder/'sources.json').read_text()):
    p=folder/rec['path']
    if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==rec['sha256']:continue
    errors=[]
    for key in ['image_url','original_url']:
        try:
            data=urllib.request.urlopen(urllib.request.Request(rec[key],headers={'User-Agent':'RainforestReferenceStudy/1.0'}),timeout=90).read()
            # A different-sized thumbnail is a valid new source, but never silently
            # replace the documented bytes in this reproducible collection.
            assert hashlib.sha256(data).hexdigest()==rec['sha256'],'Downloaded variant does not match retained source hash'
            p.write_bytes(data);break
        except Exception as exc:errors.append(str(exc))
    else:raise RuntimeError((rec['source_page'],errors))
    print('Verified reference',rec['id'],rec['title'])
