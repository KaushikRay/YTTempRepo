# Smoother quality preview

Purpose: preserve the motion approved in the 12 fps study and render every
frame, with higher spatial resolution and more sampling capacity.

- Three seconds, 72 genuinely rendered frames at 24 fps (no frame interpolation).
- 960 × 540, compared with the preceding 640 × 360 study.
- Cycles CPU, five threads, adaptive sampling: maximum 24, minimum 8,
  threshold 0.05; OpenImageDenoise; persistent scene data enabled.
- Existing fire image sequence, rain/candle/tree animation and camera retained.
- No audio, lightning pass or seamless-loop claim.

## Commands

```sh
OMP_NUM_THREADS=5 /workspace/tools/fire-venv/bin/python scripts/run_quality_preview.py
LOUNGE_REVIEW_DIR=quality_preview /workspace/tools/fire-venv/bin/python scripts/encode_motion.py
```

The supervisor records the actual worker return code. If all 72 images are
written but the known bpy cleanup stall recurs, it stops that finished worker
after ten seconds and records the termination. This is not described as a clean
renderer exit. The encoder separately verifies and decodes the resulting MP4s.
An error before frame completion remains a failure.

`renders/quality_preview/run.json` records progress and settings. Input hashing
includes the Blender scene, renderer script and every fire-sequence image.
Existing completed frames are reused only when these inputs match. The raw
frames and verbose worker log are ignored by Git; videos, QA and a poster are
retained. Rendered fire/window close-ups are magnified crops, not independent
camera renders. The scene still has the visual limitations of the approved
study; this pass improves rendering, not the underlying art or fire matte.

## Completed run

All 72 frames rendered in 1684.9 seconds (28 min 5 sec). The supervisor stopped
the worker after the known post-completion cleanup stall; actual worker return
code -15 is recorded in worker_status.json. No clean worker exit is claimed.
The encoder then passed full decoding, duration and frame-count checks for all
three MP4s. Each is 3.0 seconds and 72 frames at 24 fps. Full room is 960 × 540;
fire and window crops are magnified from that render. First, midpoint and end
frames inspected. Motion regions change; user playback review is pending.
