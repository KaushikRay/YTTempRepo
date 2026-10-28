"""Make one ordinary-Git-size archive with approved units and Mac launchers."""
import hashlib
import json
from pathlib import Path
import stat
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'downloads/Rainforest_Mac_Rebuild.zip'

def main():
    names = [
        'MAC_REBUILD.md', 'requirements-mac.txt', 'assets/audio/sources.json',
        'renders/production_test/thunder_solo.flac',
        'renders/long_release/AUDIO_CREDITS.txt',
        'renders/long_release/reference_rms.json',
        'renders/long_release/subscribe_badge.png',
        'renders/long_release/units.json',
    ]
    names += ['scripts/' + name for name in [
        'mac_run.sh', 'mac_build.py', 'fetch_long_sources.py',
        'prepare_long_release.py', 'build_long_release.py',
        'check_long_release.py', 'mix_rainforest_audio.py',
        'prepare_ambience_audio.py',
    ]]
    units = json.loads((ROOT / 'renders/long_release/units.json').read_text())['units']
    for unit in units:
        path = ROOT / unit['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == unit['sha256'], path
        names.append(unit['path'])
    entries = {name: (ROOT / name).read_bytes() for name in names}
    for label, stage in [('1_Setup', 'setup'), ('2_Preview', 'preview'),
                         ('3_Build_Both', 'build'), ('4_Check_Videos', 'qa')]:
        entries[label + '.command'] = (
            '#!/bin/bash\nset -euo pipefail\n'
            'ROOT="$(cd "$(dirname "$0")" && pwd)"\n'
            f'bash "$ROOT/scripts/mac_run.sh" {stage}\n'
        ).encode()
    manifest = {'files': [
        {'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        for name, data in sorted(entries.items())
    ], 'purpose': 'Approved pre-rendered scene; local soundtrack and timeline rebuild'}
    entries['MAC_PACKAGE.json'] = json.dumps(manifest, indent=2).encode()
    DEST.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DEST, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, data in sorted(entries.items()):
            info = zipfile.ZipInfo('RainforestCabin/' + name, date_time=(2026, 10, 28, 0, 0, 0))
            info.create_system = 3
            mode = 0o755 if name.endswith(('.command', '.sh')) else 0o644
            info.external_attr = (stat.S_IFREG | mode) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
    assert DEST.stat().st_size < 100 * 1024**2, 'Archive exceeds ordinary Git file limit'
    report = {'file': DEST.name, 'bytes': DEST.stat().st_size,
              'sha256': hashlib.sha256(DEST.read_bytes()).hexdigest(),
              'mac_execution_tested': False,
              'cloud_package_and_smoke_checks': 'See mac_kit_validation.json'}
    DEST.with_suffix('.json').write_text(json.dumps(report, indent=2))
    print(json.dumps(report), flush=True)

if __name__ == '__main__':
    main()
