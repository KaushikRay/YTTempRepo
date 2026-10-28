import hashlib,json,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'renders/long_release';TAG='rainforest-masters-2026-10-28';REPO='KaushikRay/YTTempRepo'
def gh(*args):return subprocess.check_output(['gh',*args],text=True)
def status(phase,**fields):
 d={'phase':phase,'worker_running':phase not in ['complete','blocked'],'updated_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),**fields};(OUT/'upload_status.json').write_text(json.dumps(d,indent=2));(ROOT/'status.json').write_text(json.dumps(d,indent=2));print(json.dumps(d),flush=True)
def main():
 manifest=json.loads((OUT/'delivery_manifest.json').read_text())
 releases=json.loads(gh('api',f'repos/{REPO}/releases?per_page=100'));release=next((x for x in releases if x['tag_name']==TAG),None)
 if release is None:
  notes=OUT/'release_notes.md';notes.write_text('Draft review masters: 3 h continuous scene; 8 h with one hour scene then seven hours dark, sound continuing. Download the parts for each master together with its joining helper and checksum file. No YouTube upload/publication has been performed.\n')
  gh('release','create',TAG,'--repo',REPO,'--target','codex/rainforest-cabin','--draft','--title','Rainforest cabin — 3 h and 8 h review masters','--notes-file',str(notes))
  release=next(x for x in json.loads(gh('api',f'repos/{REPO}/releases?per_page=100')) if x['tag_name']==TAG)
 assert release['draft'],'Do not overwrite a published release'
 release_id=release['id'];stage=OUT/'work/upload';stage.mkdir(exist_ok=True);completed=[]
 for master in manifest['files']:
  source=OUT/master['file']
  for part in master['parts']:
   assets=json.loads(gh('api',f'repos/{REPO}/releases/{release_id}/assets?per_page=100'));existing=next((a for a in assets if a['name']==part['file']),None)
   expected='sha256:'+part['sha256']
   if existing and existing.get('digest')==expected:completed.append(part['file']);continue
   assert existing is None,'Existing asset digest differs; inspect before replacement'
   temp=stage/part['file'];digest=hashlib.sha256()
   status('preparing_master_part',file=part['file'],completed_parts=len(completed),total_parts=sum(len(x['parts']) for x in manifest['files']))
   with source.open('rb') as src,temp.open('wb') as dst:
    src.seek(part['offset']);remaining=part['bytes']
    while remaining:
     data=src.read(min(8*1024*1024,remaining));assert data;dst.write(data);digest.update(data);remaining-=len(data)
   assert digest.hexdigest()==part['sha256']
   status('uploading_master_part',file=part['file'],completed_parts=len(completed),total_parts=sum(len(x['parts']) for x in manifest['files']))
   subprocess.run(['gh','release','upload',TAG,str(temp),'--repo',REPO],check=True)
   assets=json.loads(gh('api',f'repos/{REPO}/releases/{release_id}/assets?per_page=100'));asset=next(a for a in assets if a['name']==part['file'])
   assert asset['size']==part['bytes'] and asset.get('digest')==expected,'Remote part digest not verified'
   completed.append(part['file']);temp.unlink()
 small=[OUT/'delivery_manifest.json',OUT/'MASTER_SHA256SUMS.txt',OUT/'AUDIO_CREDITS.txt',OUT/'QA_REVIEW.md',OUT/'README.md']+list(OUT.glob('Join_*.command'))+list(OUT.glob('*_parts.sha256'))
 for path in small:subprocess.run(['gh','release','upload',TAG,str(path),'--repo',REPO,'--clobber'],check=True)
 status('complete',draft_release_url=release['html_url'],completed_parts=len(completed),full_master_files_untouched=True,youtube_uploaded=False,public_release_published=False)
if __name__=='__main__':main()
