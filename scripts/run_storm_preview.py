"""Supervise the bpy worker and record the known post-render cleanup hang honestly."""
import subprocess,sys,time,json
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'renders/storm_preview';out.mkdir(exist_ok=True);manifest=out/'run.json'
with (out/'worker.log').open('w') as log:
 proc=subprocess.Popen([sys.executable,str(root/'scripts/render_storm.py')],cwd=root,stdout=log,stderr=subprocess.STDOUT)
 complete_at=None;terminated=False
 while proc.poll() is None:
  try:r=json.loads(manifest.read_text())
  except (FileNotFoundError,json.JSONDecodeError):r={}
  if r.get('status')=='frames_complete' and r.get('completed')==144:
   if complete_at is None:complete_at=time.monotonic()
   if time.monotonic()-complete_at>10:
    proc.terminate();terminated=True
    try:proc.wait(timeout=10)
    except subprocess.TimeoutExpired:proc.kill();proc.wait()
    break
  time.sleep(1)
 result={'worker_returncode':proc.returncode,'terminated_after_frames_complete':terminated}
 (out/'worker_status.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True)
 if terminated:
  print('All frames written; worker stopped during known cleanup hang. Encoding validation still required.',flush=True)
 elif proc.returncode:sys.exit(proc.returncode)
