# Rustic Gothic tavern — Blender development scene

Current scene: `storm_lounge.blend` (generated with Blender 4.3.2).
Reference: `reference/original.png`, recovered from repository commit 51e4ad4.

The current hearth uses a keyed frame from actual 1920 × 1080 fireplace
footage, not the rejected procedural flames. The frame is packed into the
Blender file, with attribution embedded as a text block. **CC BY 3.0 credits
are required when distributing the result.** See `assets/fire/CREDITS.txt`.

## Review images

- `renders/composition.png`: current room with downloaded fire footage.
- `renders/real_fire_detail.png`: current hearth close-up.
- `renders/tavern_study.png`: earlier rustic room before real fire integration.
- `renders/masonry_detail.png`: masonry close-up.
- `renders/candle_detail.png`: candle close-up from the earlier lounge iteration.

## Rebuild

Blender 4.3.2 and FFmpeg are used. Retained source material and licence metadata
are under `assets/fire/`. To reproduce the processed still if needed:

```sh
/workspace/tools/fire-venv/bin/python scripts/prepare_fire_asset.py
```

Build the scene without a render:

```sh
LOUNGE_SKIP_RENDER=1 LOUNGE_PREVIEW_PERCENT=100 LOUNGE_SAMPLES=128 \
  blender -b -t 5 --python scripts/build_scene.py
```

The system Blender lacks OpenImageDenoise. An isolated official bpy==4.5.3
runtime (Python 3.11, numpy==1.26.4) renders clean review images without
resaving/upgrading the Blender 4.3 scene:

```sh
OMP_NUM_THREADS=5 LOUNGE_SAMPLES=80 LOUNGE_PREVIEW_PERCENT=100 LOUNGE_FIRE_DETAIL=1 \
  /workspace/tools/fire-venv/bin/python scripts/render_review.py
```

Those paths describe this cloud workspace. On another machine, use a Python
3.11 virtual environment with bpy==4.5.3 and numpy==1.26.4, or render in a
Blender application build with denoising support.

## Limitations

This remains a development scene, not a final photoreal match. The fire is a
video-derived image card intended for the locked camera. Its original 30-second
movie is retained, but animated fire integration and looping are not completed.
Rain and candle motion are provisional and unvalidated. No audio is included.
The animation, lighting integration and scene dressing still require refinement.
See `docs/real-fire-integration.md` for source, processing and validation.
