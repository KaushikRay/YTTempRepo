# Gothic storm lounge — first composition study

Reference recovered from commit `51e4ad4`, saved in `reference/original.png`.

## Build and render

Blender 4.3.2, no external assets or Python packages required:

```sh
blender -b -t 5 --python scripts/build_scene.py
```

This rebuilds `storm_lounge.blend` and renders `renders/composition.png`.
Open the blend file in Blender and use the saved camera (Numpad 0).
The current preview renders at 1280 × 720 with Cycles, 192 samples and an indirect-light clamp. This Blender build lacks OpenImageDenoise.

## Scope of this iteration

A procedural composition study (second visual pass): stone hall, paired pointed leaded windows,
oculus, large right-hand fireplace, leather seating, table, candles, books,
rugs, exterior cottages and trees. Fire shapes, hearth illumination, candle
shapes and tree sway have preliminary animation over a six-second timeline.

This is not the finished photoreal scene or an approved animation. Materials
are procedural placeholders. Rain is static streak geometry in this still;
glass runoff, physically credible flame animation, detailed upholstery,
reference-quality vegetation, smoke, lightning variations, and seamless loop
validation remain to be developed. No audio is included.

Next: compare the still against the reference, correct architecture and camera,
then replace prominent placeholder surfaces and assets before animation tests.

The build automatically runs `scripts/refine_scene.py` to add staggered masonry,
nested window mouldings, chimney detail, a draped blanket, finer interior
foliage and flame ribbons, and revised camera/table placement.

## Current surface/storm pass

The builder also executes `scripts/detail_scene.py`. A quick diagnostic is
the default (640 × 360, 48 samples). For the larger review still:

```sh
LOUNGE_PREVIEW_PERCENT=100 LOUNGE_SAMPLES=160 blender -b -t 5 --python scripts/build_scene.py
```

Both commands overwrite the same scene and preview; Blender retains its
usual `.blend1` backup. The current scene includes provisional linear falling
rain, not yet an approved seamless loop. Glass and distant landscape are
procedural approximations. No external scanned assets have been downloaded.
