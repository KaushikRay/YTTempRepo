# Photographic-style layered motion test

This is the next step after the user preferred the photographic hybrid still.
It is a six-second locked-camera, silent 1920×1080 / 24 fps motion diagnostic.
The source images are generated assets, not camera photographs. No video-model
generation or frame interpolation is used: Blender renders every native frame.

## Changes from the static hybrid

- A separate transparent foreground palm layer and a clean background behind it.
  The static source no longer contains duplicate foreground fronds behind the
  moving ones. Both layer-generation originals and checksums are documented in
  `assets/hybrid_motion/provenance.json`.
- The foreground palm image is mapped onto a 10,201-vertex flexible camera-plane
  grid. Two restrained shape-key wind components bend it, with zero displacement
  along the top and right attachment borders. This preserves photographic leaf
  detail but is a 2.5D deformation, not a modeled botanical leaf simulation.
- Seven irregular, feathered stream patches use moving UV perturbation to vary
  the source water texture. Thirty-six small, fading impact rings animate in a
  foreground pool. The effect is localized image-based water animation; it does
  not simulate or replace every whitewater feature in the source image.
- 6,750 independently recycling rain streaks, at two scene depths, use soft
  optical exposure shapes. Photo-projected cabin/porch patches provide occlusion:
  most rain stays behind the cabin and all rain stays outside the sheltered wall,
  posts and roof patches. Forty-two additional eave beads fall along short paths.
- The warm cabin light, timber detail, rocks and distant forest remain stable.

## Review priorities and limits

Compare the first frame and preview to the approved hybrid still, retaining its
porch/cabin framing, wet dense foliage, warm interior and rocky creek. The original
chat reference is not available as a local file, so no pixel-aligned original
reference comparison is claimed.

Inspect the native-pixel palm and water crop clips as well as the full frame:

1. Leaf edges must not reveal duplicates or broad background smearing as they sway.
2. Water should feel locally active; look for frozen highlights beside moving
   patches or a rubber-like distortion of rocks at the masks.
3. Rain should remain visible at normal speed and populated across the upper view.
4. Watch for edge sparkle on thin palm leaflets and abrupt impact-ring resets.

The clean plate inpaint makes small background/detail changes from the approved
still. Generated palm cutout edges are not claimed to be a perfect optical matte.
Most understory and the distant forest are static. Camera movement would reveal
the flat layers. No lightning, soundtrack, long video, or seamless-loop approval
is included. Rain/water/runoff phases do not yet form a common seamless loop.

## Files and rebuild

- `rainforest_hybrid_motion.blend`: self-contained packed animation scene.
- `renders/hybrid_motion/preview.mp4`: full-frame preview after render completion.
- `renders/hybrid_motion/palms_detail.mp4`: native 920×780 crop, no enlargement.
- `renders/hybrid_motion/water_detail.mp4`: native 720×300 crop, no enlargement.
- `renders/hybrid_motion/qa.json`, `visual_checks.json`: output checks.
- `research/hybrid_motion/rig_checks.json`, `portability.json`: scene checks.

```sh
python scripts/setup_hybrid_motion.py
python scripts/render_hybrid_motion.py
python scripts/check_hybrid_motion.py
python scripts/check_hybrid_motion_portability.py
```

Use the supplied Python environment with `bpy` for setup/render/portability, and
Pillow/NumPy for output checks. The renderer writes progress to `status.json` and
`renders/hybrid_motion/status.json`; redirect output to `logs/hybrid_motion.log`.
Rendering resumes from intact native frames if the scene/script signature matches.
Intermediate frame PNGs are ignored by Git. The `.blend` packs both image assets
and uses no external libraries; generated source PNGs are also retained for edits.

Next after visual review: improve any weak water or foliage motion, establish a
common longer loop phase, then develop the rain/stream/thunder soundtrack. Do not
start a long YouTube render before the moving image has been reviewed.
