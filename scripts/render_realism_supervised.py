"""Render the realism study and distinguish completion from bpy cleanup stalls.

Run with the Python interpreter that has bpy installed. Progress is written
to renders/realism_status.json; the actual render log stays local/ignored.
"""
import datetime,json,os,subprocess,sys,time
from pathlib import Path

root=Path(__file__).resolve().parents[1]
log=root/'renders/realism_worker.log'
status=root/'renders/realism_status.json'
env=os.environ.copy();env.setdefault('REALISM_PERCENT','100');env.setdefault('REALISM_SAMPLES','96');env.setdefault('OMP_NUM_THREADS','5')

def update(phase,**kwargs):
    status.write_text(json.dumps({'updated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'phase':phase,**kwargs},indent=2))

with log.open('w') as output:
    worker=subprocess.Popen([sys.executable,str(root/'scripts/realism_rebuild.py')],cwd=root,env=env,stdout=output,stderr=subprocess.STDOUT)
    completed_at=None;stopped=False
    while worker.poll() is None:
        content=log.read_text(errors='replace')
        finished='REALISM PREVIEW COMPLETE' in content
        if finished and completed_at is None:completed_at=time.monotonic()
        lines=[line for line in content.splitlines() if 'Sample ' in line]
        update('render_complete_cleanup' if finished else 'rendering' if 'REALISM PREVIEW RENDER START' in content else 'building',pid=worker.pid,last_sample=lines[-1] if lines else None)
        if completed_at is not None and time.monotonic()-completed_at>8:
            worker.terminate();stopped=True
            try:worker.wait(timeout=10)
            except subprocess.TimeoutExpired:worker.kill();worker.wait()
            break
        time.sleep(1)
    finished='REALISM PREVIEW COMPLETE' in log.read_text(errors='replace')
    result={'render_completed':finished,'worker_returncode':worker.returncode,'stopped_during_cleanup':stopped}
    (root/'renders/realism_runtime.json').write_text(json.dumps(result,indent=2))
    update('complete' if finished else 'failed',**result)
    if not finished:sys.exit(worker.returncode or 1)
print('Realism still complete; actual runtime outcome recorded.',flush=True)
