"""Rebuild approved long timelines using bundled video units, without Blender."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'renders/long_release'

def verify_bundle():
    manifest = json.loads((ROOT / 'MAC_PACKAGE.json').read_text())
    for row in manifest['files']:
        path = ROOT / row['path']
        digest = hashlib.sha256()
        with path.open('rb') as f:
            while block := f.read(8 * 1024 * 1024):
                digest.update(block)
        if path.stat().st_size != row['bytes'] or digest.hexdigest() != row['sha256']:
            raise RuntimeError(f'Package verification failed: {path}')
    print('Package checksums verified.', flush=True)

def run_script(name):
    subprocess.run([sys.executable, str(ROOT / 'scripts' / name)], check=True)

def prepare():
    run_script('fetch_long_sources.py')
    run_script('prepare_long_release.py')

def export_links():
    for name, folder in [('rainforest_3h', '3h'), ('rainforest_8h', '8h')]:
        source = OUT / (name + '.mp4')
        if source.exists():
            target_dir = ROOT / 'youtube' / folder
            target_dir.mkdir(parents=True, exist_ok=True)
            target = target_dir / source.name
            if not target.exists():
                os.link(source, target)
            elif not os.path.samefile(source, target):
                raise RuntimeError(f'Existing unrelated output: {target}')
            print(f'Video ready: {target}', flush=True)

def main():
    stage = sys.argv[1]
    OUT.mkdir(parents=True, exist_ok=True)
    from prepare_long_release import status
    try:
        if stage == 'verify':
            verify_bundle()
            return
        if stage in ('setup', 'build') and shutil.disk_usage(ROOT).free < 25 * 1024**3:
            # Existing finished masters can be QA'd without this build-space check.
            if not all((OUT / f'{n}.mp4').exists() for n in ('rainforest_3h', 'rainforest_8h')):
                raise RuntimeError('Keep at least 25 GiB free (30 GB recommended) before building.')
        if stage == 'setup':
            verify_bundle()
            prepare()
            status('mac_setup_complete', worker_running=False, next='Run 2_Preview.command')
        elif stage == 'preview':
            if not (OUT / 'source_cache.json').exists():
                raise RuntimeError('Run 1_Setup.command first.')
            from build_long_release import audio_track, video_master
            audio, _ = audio_track('endurance', 900, 720)
            path = video_master('endurance', 900, 720, audio)
            status('mac_preview_complete', worker_running=False, output=str(path), next='Review preview, then run 3_Build_Both.command')
        elif stage == 'build':
            if not (OUT / 'source_cache.json').exists():
                raise RuntimeError('Run 1_Setup.command first.')
            run_script('build_long_release.py')
            export_links()
            status('mac_masters_built', worker_running=False, next='Run 4_Check_Videos.command')
        elif stage == 'qa':
            if not all((OUT / f'{n}.mp4').exists() for n in ('rainforest_3h', 'rainforest_8h')):
                raise RuntimeError('Build both masters before QA.')
            run_script('check_long_release.py')
            export_links()
            status('mac_qa_complete', worker_running=False, next='Review videos in youtube/3h and youtube/8h')
        else:
            raise ValueError(stage)
    except BaseException as error:
        status('failed', worker_running=False, stage=stage, error=str(error))
        raise

if __name__ == '__main__':
    main()
