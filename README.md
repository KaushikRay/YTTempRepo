# Rustic Gothic tavern — Blender development scene

## Latest art revision: realism still

The newest iteration adds interior climbing ivy on the piers, window-side wall
and outer hearth masonry, plus more visible rain and exterior mist.
See [creeper iteration and source notes](docs/creeper-iteration.md).

The latest pass uses historic photographs of Gainsborough and Penshurst for
window/hearth construction, plus rough CC0 stone and worn leather seating.
See [historic study, sources and artistic departures](docs/historic-study.md).

`renders/realism_study.png` is a new asset-based still, compared with
`renders/realism_before.png`. `realism_study.blend` contains the revised art
with most textures packed (Blender 4.5.3). Keep the assets directory beside it;
the large stone/wood maps use relative paths. The earlier animation is preserved.
This is an unfinished realism study, not a final photoreal scene or a new video.
See [realism review](docs/realism-review.md) and `assets/realism/provenance.json`.


## Latest review: lightning and audio

- `renders/storm_preview/full_room_with_audio.mp4`: six-second 960 × 540 /
  24 fps preview with lightning, rain, fire sound and delayed thunder.
- `renders/storm_preview/lightning_peak.png`: main flash still.
- `renders/storm_preview/audio_mix.wav`: audio-only mix for review.
- `renders/storm_preview/av_qa.json`: final stream, level and flash checks.
- `assets/audio/CREDITS.txt`: source licences and required attribution.

The current scene has 144 frames at 24 fps and 144 external fire images.
The soundtrack is mixed/muxed outside Blender. Earlier three-second setup
commands below describe earlier milestones and can reset the scene: do not
run them on the current file without intending to rebuild. See
[storm preview workflow](docs/storm-preview.md) for the current revision.

For a fresh checkout without the optimized baseline cache, open the current
Blender file with its assets directory and render all frames 1–144 directly,
using 960 × 540, 24 fps, adaptive maximum 24 samples and denoising. The optimized
cloud renderer reuses earlier validated frames and requires that local cache.
This is a prototype, not a final photoreal scene or a seamless long video.

## Earlier workflow notes


Current scene: `storm_lounge.blend` (generated with Blender 4.3.2).
Reference: `reference/original.png`, recovered from repository commit 51e4ad4.

The current hearth uses a 144-frame keyed sequence from downloaded 1920 × 1080
fireplace footage, not the rejected procedural flames. Keep assets/fire/sequence
alongside the Blender file; the animated images are external relative-path
assets. Attribution is embedded as a text block. **CC BY 3.0 credits
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
video-derived image card intended for the locked camera. A three-second motion
study is integrated; final smooth animation and seamless looping are not completed.
Rain and candle motion are provisional and unvalidated. No audio is included.
The animation, lighting integration and scene dressing still require refinement.
See `docs/real-fire-integration.md` for source, processing and validation.

## Current motion preview

The scene now has a three-second 24 fps timeline. The review MP4 samples it
at 12 fps / 640 × 360. See [motion workflow and limits](docs/motion-preview.md).

- `renders/motion/full_room.mp4`: full-room motion study.
- `renders/motion/fire_crop.mp4`: magnified crop of the fire.
- `renders/motion/window_crop.mp4`: magnified crop of the window.
- `renders/motion/qa.json`: duration, frame count and decode checks.

The crops add no detail beyond the full-room render. No audio or seamless
loop is included. Raw preview frames are ignored by Git; they can be regenerated.
Do not rebuild the still scene after motion setup without rerunning
`scripts/setup_motion.py`. Download the whole branch to retain sequence assets.

## Smoother quality preview

The completed quality review uses genuine 24 fps, 960 × 540 and adaptive Cycles sampling
up to 24 samples, with denoising. See [quality preview workflow](docs/quality-preview.md).
The preceding 12 fps clips remain available under `renders/motion/`.

Quality review files: `renders/quality_preview/full_room.mp4`,
`renders/quality_preview/fire_crop.mp4` and `renders/quality_preview/window_crop.mp4`.
Each is three seconds at 24 fps; full room is 960 × 540. Validation is recorded
in `renders/quality_preview/qa.json`. The earlier 12 fps study is preserved.
