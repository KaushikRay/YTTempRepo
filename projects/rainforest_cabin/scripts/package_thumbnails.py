"""Format image-generation results for delivery; no scene content is synthesized here."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'renders/long_release/thumbnails'
FONT = '/usr/share/fonts/truetype/open-sans/OpenSans-Semibold.ttf'

def run(args):
    subprocess.run(args, check=True)

def main():
    rows = json.loads((OUT / 'generation_sources.json').read_text())['variants']
    sources = OUT / 'generation_originals'
    sources.mkdir(parents=True, exist_ok=True)
    for row in rows:
        source = Path(row['generated_file'])
        retained = sources / f"{row['key']}.png"
        shutil.copyfile(source, retained)
        target = OUT / row['file']
        # Mechanical delivery sizing/encoding only; the image tool did all design edits.
        run(['magick', str(source), '-resize', '1280x720!', '-colorspace', 'sRGB',
             '-strip', '-sampling-factor', '4:4:4', '-quality', '94', str(target)])
        geometry = subprocess.check_output(['magick', 'identify', '-format', '%wx%h', str(target)], text=True)
        assert geometry == '1280x720' and target.stat().st_size < 2 * 1024**2
        row['bytes'] = target.stat().st_size
        row['sha256'] = hashlib.sha256(target.read_bytes()).hexdigest()
        row['resolution'] = [1280, 720]
        row['retained_generation'] = str(retained.relative_to(ROOT))
    for size, name in [('480x270', 'comparison.jpg'), ('320x180', 'small_size_review.jpg')]:
        args = ['magick', 'montage', '-font', FONT, '-pointsize', '20',
                '-background', '#10191a', '-fill', '#f1eddf']
        for row in rows:
            args += ['-label', row['key'].replace('_', ' '), str(OUT / row['file'])]
        run(args + ['-tile', '3x2', '-geometry', size + '+12+12', '-quality', '92', str(OUT / name)])
    # Source versus representative final cover: make visual differences reviewable.
    run(['magick', 'montage', '-font', FONT, '-pointsize', '22', '-background', '#10191a',
         '-fill', '#f1eddf', '-label', 'Approved video scene',
         str(ROOT / 'renders/production_test/darker_still.png'),
         '-label', 'Thumbnail 3h A', str(OUT / rows[0]['file']),
         '-tile', '2x1', '-geometry', '640x360+12+12', '-quality', '92',
         str(OUT / 'source_comparison.jpg')])
    review_path = OUT / 'visual_review.json'
    review = json.loads(review_path.read_text()) if review_path.exists() else None
    manifest = {
        'source_scene': 'renders/production_test/darker_still.png',
        'method': 'Image-generation edits of approved scene; delivery-only resizing/JPEG encoding with ImageMagick.',
        'literal_video_frame_exports': False,
        'video_modified': False,
        'ad_free_claim': False,
        'variants': rows,
        'recommended_initial_choices': {'3h': '3h_A', '8h': '8h_B'},
        'qa': {'all_six_1280x720': True, 'all_six_under_2_MiB': True,
               'small_size_sheet': 'small_size_review.jpg',
               'manual_visual_review': review if review else 'pending'},
    }
    (OUT / 'manifest.json').write_text(json.dumps(manifest, indent=2))
    archive = ROOT / 'downloads/Rainforest_YouTube_Thumbnails.zip'
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for row in rows:
            z.write(OUT / row['file'], 'Rainforest_YouTube_Thumbnails/' + row['file'])
        for name in ['README.md', 'comparison.jpg', 'small_size_review.jpg', 'manifest.json']:
            z.write(OUT / name, 'Rainforest_YouTube_Thumbnails/' + name)
    assert archive.stat().st_size < 100 * 1024**2
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
    print(json.dumps({'archive': str(archive.relative_to(ROOT)), 'bytes': archive.stat().st_size,
                      'sha256': hashlib.sha256(archive.read_bytes()).hexdigest(), 'images': len(rows)}))

if __name__ == '__main__':
    main()
