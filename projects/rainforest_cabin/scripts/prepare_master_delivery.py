"""Describe large master files as resumable release-asset parts, without copies."""
import hashlib,json,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'renders/long_release';PART_BYTES=1_800_000_000

def main():
 files=[]
 for name in ['rainforest_3h','rainforest_8h']:
  p=OUT/(name+'.mp4');qa=json.loads((OUT/(name+'_qa.json')).read_text());assert p.stat().st_size==qa['bytes']
  parts=[]
  with p.open('rb') as f:
   number=0
   while True:
    digest=hashlib.sha256();size=0
    while size<PART_BYTES:
     data=f.read(min(8*1024*1024,PART_BYTES-size))
     if not data:break
     digest.update(data);size+=len(data)
    if not size:break
    number+=1;parts.append({'file':p.name+f'.part{number:03d}','bytes':size,'sha256':digest.hexdigest(),'offset':(number-1)*PART_BYTES})
  files.append({'file':p.name,'bytes':p.stat().st_size,'sha256':qa['sha256'],'parts':parts,'duration_seconds':qa['duration_seconds']})
  command=OUT/f'Join_{name}.command'
  body='#!/bin/bash\nset -euo pipefail\ncd "$(dirname "$0")"\n'
  for part in parts:body+=f'test -f "{part["file"]}" || {{ echo "Missing {part["file"]}"; exit 1; }}\n'
  body+='shasum -a 256 -c '+name+'_parts.sha256\n'
  body+='cat '+' '.join('"'+part['file']+'"' for part in parts)+' > "'+p.name+'.assembling"\n'
  body+=f'echo "{qa["sha256"]}  {p.name}.assembling" | shasum -a 256 -c -\nmv "{p.name}.assembling" "{p.name}"\necho "Verified master ready: {p.name}"\n'
  command.write_text(body);command.chmod(0o755)
  (OUT/(name+'_parts.sha256')).write_text(''.join(part['sha256']+'  '+part['file']+'\n' for part in parts))
 (OUT/'delivery_manifest.json').write_text(json.dumps({'part_bytes':PART_BYTES,'files':files,'parts_are_transport_only_not_reencoded_videos':True},indent=2))
 (OUT/'MASTER_SHA256SUMS.txt').write_text(''.join(x['sha256']+'  '+x['file']+'\n' for x in files))
 print(json.dumps({'masters':len(files),'parts':sum(len(x['parts']) for x in files),'total_bytes':sum(x['bytes'] for x in files)}))
if __name__=='__main__':main()
