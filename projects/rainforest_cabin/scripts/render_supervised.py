"""Build/render with readable progress and an honest terminal status."""
from pathlib import Path
import datetime, json, os, re, subprocess, sys, time

root=Path(__file__).resolve().parents[1]
(root/'logs').mkdir(exist_ok=True)
env=os.environ.copy();env.setdefault('WIDTH','1920');env.setdefault('SAMPLES','128');env.setdefault('OUTPUT','clear_view_still.png')
env.setdefault('OMP_NUM_THREADS','6')
log=root/'logs'/'render.log';status=root/'status.json'
with log.open('w') as out:
    # Failed bpy scripts can also stall during native shutdown. Report the
    # traceback, then exit the worker directly after success OR Python failure.
    launcher="import runpy,os,sys,traceback\ntry:\n runpy.run_path(sys.argv[1],run_name='__main__')\nexcept BaseException:\n traceback.print_exc();sys.stdout.flush();sys.stderr.flush();os._exit(1)\n"
    worker=subprocess.Popen([sys.executable,'-u','-c',launcher,str(root/'scripts'/'build_scene.py')],cwd=root,env=env,stdout=out,stderr=subprocess.STDOUT)
    while worker.poll() is None:
        time.sleep(2)
        text=log.read_text(errors='replace')
        phase='rendering' if "rendering {" in text else 'building'
        if 'RAINFOREST STILL COMPLETE' in text:phase='complete'
        samples=re.findall(r'Sample (\d+)/(\d+)',text)
        progress={'phase':phase,'pid':worker.pid,'updated_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  'output':env['OUTPUT'],'resolution':[int(env['WIDTH']),round(int(env['WIDTH'])*9/16)],'samples':int(env['SAMPLES'])}
        if samples:progress['last_logged_sample']=list(map(int,samples[-1]))
        status.write_text(json.dumps(progress,indent=2))
    complete='RAINFOREST STILL COMPLETE' in log.read_text(errors='replace') and worker.returncode==0
    progress.update(phase='complete' if complete else 'failed',worker_running=False,returncode=worker.returncode)
    status.write_text(json.dumps(progress,indent=2))
    if not complete:raise SystemExit(worker.returncode or 1)
print('SUPERVISED STILL COMPLETE',flush=True)
