# Furnishings, grounded fire and replenishing rain

This revision replaces the earlier translating-rain diagnostic. It retains
realism_study.blend and storm_lounge.blend unchanged and saves the new work in
dressing_motion.blend, with the complete assets folder required alongside it.

## Dressing

Added CC0 Poly Haven Metal Jug, Wooden Bowl 02, Carved Wooden Plate, Food Apple
01 and Dry Branches Medium 01. Original API manifests are retained under
assets/dressing; all downloaded source bytes were checked against provider MD5.
Models retain 2K PBR textures in the linked assets/dressing/dressing.blend
library. Asset pages: https://polyhaven.com/a/<asset-id>; licence:
https://polyhaven.com/license. See assets/dressing/CREDITS.txt.

Table items use the actual table surface height obtained by ray casting, and
normalized model bounds. The runner rests on the tabletop and hangs past the
measured front edge. The sofa throw follows vertical surface samples of the
actual sofa mesh. These textiles are static drapes, not a cloth simulation.
The room remains historically inspired rather than a dated archaeological
reconstruction; finer object arrangement and textile folds remain art tasks.

## Fire and fuel

The detailed branch asset is darkened while retaining its surface maps and
fitted to low heaps inside the grate. Heap bases meet the ash bed; source
branch proportions were compressed for kindling, not presented as split logs.
The first oversized branch fitting was rejected during diagnostic rendering.

The licensed source video is resampled from source seconds 2–4 into a 48-frame,
24 fps RGB movie. Firelight energy is gently smoothed from measured footage
brightness, replacing unrelated sine-wave flicker. Credits remain required:
assets/fire/CREDITS.txt. The derived movie is CC BY 3.0, not CC0. Flame rendering
remains a keyed photographic card for this fixed camera, not volumetric fire.
Its matte and fuel integration still have limitations at close range.

## Rain and foliage

Removed the translating rain mesh. There are 2,800 shared-mesh streak instances
with independent vertical and horizontal cyclic drivers. Each streak returns
above the aperture and behind opaque wall/sill/jamb geometry; the field does
not progressively leave the upper window empty. Drivers persist in the Blender
file without a Python frame-change handler or enabling script auto-run.

The upper-height population was checked over 144 timeline frames: 614–692
streaks, demonstrating stationary population rather than depletion. This count
is before aperture occlusion, not a pixel-level rain measurement. Actual first,
middle and last rendered frames also need visual comparison. Analytic streak
geometry represents exposure blur; render motion blur is disabled to avoid
artifacts when particles wrap. No final seamless loop is claimed.

Leaf orientation is converted from its quaternion pose before adding tiny
independent flex; this corrects the previous test's unsafe rotation-mode change.
The exterior trees remain static in this test.

## Reproduce

Use Python with bpy 4.5.3 and the full source assets:

    OMP_NUM_THREADS=5 /workspace/tools/fire-venv/bin/python scripts/build_dressing_library.py
    DIAGNOSTIC=1 OMP_NUM_THREADS=5 /workspace/tools/fire-venv/bin/python scripts/dressing_motion_pass.py
    STILL=1 OMP_NUM_THREADS=5 /workspace/tools/fire-venv/bin/python scripts/dressing_motion_pass.py
    OMP_NUM_THREADS=5 /workspace/tools/fire-venv/bin/python scripts/dressing_motion_pass.py

The full still uses 1280x720, 96 Cycles samples and denoising. The two-second
motion test uses 640x360, 24 fps, 12 samples and denoising. This is a genuine
24 fps diagnostic, not a final-resolution video. It has no audio and is not
seamless. At completion the saved scene is restored to 1280x720 / 96 samples.

The worker exits immediately after successful rendering/saving to avoid the
known bpy native shutdown stall. Completion is determined from outputs and
checks, not an assertion that native cleanup is fixed.

## Final review and checks

Evaluated fuel vertices (not just source bounding boxes) are checked after
instancing: both heaps start at z=0.30 m and end at z=0.58 m, within the grate
footprint. A transform error found during review was corrected and affected
renders were discarded. The first, middle and last rain crops are retained
in rain_contact.png (frames 1, 24 and 48, left to right).

Actual evaluated drivers were checked at frames 1, 12, 24, 36, 48, 96 and 144.
The rectangular upper-aperture population stays between 548 and 607 streaks;
there is no progressive depletion. These are particle counts, not a claim
that every streak is separately visible through the wet glass.

Inherited lightning visibility/sky keyframes were removed from this focused
motion test; proper lightning events remain a separate integration task. The
original storm scene and previous realism scene are preserved byte-for-byte.

The clip is 48 distinct rendered timeline frames, 24 fps, exactly two seconds.
Decode, library/texture paths, fuel bounds, saved render settings and source
scene hashes are checked by scripts/check_dressing_delivery.py; qa.json retains
results. The completed scene is saved at 1280x720 / 96 samples for still work.
The preview remains 640x360 / 12 samples, silent and not seamless.

The full still was compared with the original reference. Furnishing detail,
textile contact and fire grounding improve this pass, but the architecture,
rear room dressing, candle fidelity and overall photographic realism still
need further work. No final photorealism or finished long-video claim is made.
