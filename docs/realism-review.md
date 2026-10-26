# Realism rebuild — reference review and asset-based still

The current [lighting and exterior iteration](lighting-exterior-iteration.md)
refines ivy shapes/attachment and adds detailed CC0 landscape assets.

The latest [creeper and weather iteration](creeper-iteration.md) adds interior
ivy and revises rain visibility. Scene and image paths are updated in place.

The current revision also includes the [historic construction study](historic-study.md):
deep jointed window surrounds, irregular mortar-filled masonry, a dark brick
hearth, revised fire integration and a scanned leather sofa. The image and
scene paths below are updated in place. The original critique remains useful.

## Why the previous video reads as CGI

Direct comparison of reference/original.png and the rendered video frames
reveals structural issues, not a shortage of render samples:

- Rounded clusters stand in for trees and become conspicuously artificial
  during lightning. The exterior needs real vegetation or restrained silhouettes.
- Furniture, bread, books, candle bodies and barrels have simple, repeated
  primitive shapes. Surface noise cannot supply missing construction detail.
- The room is sparsely dressed and the seating sits at the frame edge. The
  reference foreground is occupied by inviting seating, textiles and a large
  dressed table. The reference also has much richer architectural detail.
- Graphic rain streaks and heavy window leads dominate the exterior. The glass
  should carry subtle wetness and reflection, with the landscape behind it.
- The fire matte clips low/mid-tone flame structure and produces an isolated
  luminous cutout rather than a fire with grounded fuel and a coherent glow.
- The striped procedural rug, clean geometry and uniform wear patterns expose
  the procedural construction. More samples improve noise, not those failures.

## This pass

Downloaded detailed CC0 model assets and 2K image-based materials from Poly
Haven. Retained original API manifests and checked downloaded bytes against
provider MD5 values. The licence page is retained. This is the first revision
using this collection of ready-made assets rather than mostly primitive props.

Used Gothic Coffee Table, Arm Chair 01, Wine Barrel 01, Jug 01 and Brass
Candleholders model assets, plus Stone Wall 05, Monastery Stone Floor and
Fabric Pattern 05 materials. Models retain their UVs and PBR textures.
Furniture is normalized from imported bounds, placed at physical scale,
and the table top is aligned with the existing prop height. The woven rug uses an image-based fabric material. A trial throw was removed
after contact/framing review; richer textiles remain necessary.

Replaced the foreground seating, table, casks and prominent candle cluster.
Removed toy-like vegetation clusters and smooth bread placeholders. Scanned
stone patterns are mapped in world-scale UVs; window leadwork is thinner.
Revised the warm/cool light balance and reduced shiny surround highlights.

The existing licensed fire source is retained, with a new review-frame matte
that preserves more of the actual fuel and flame body. The source licence
and attribution are unchanged; see assets/fire/CREDITS.txt. This is still a
video-derived card, not volumetric fire. Original storm animation and audio
remain preserved in storm_lounge.blend and the earlier rendered clips.

## What is not complete

This is a new still-development branch of the art, saved as realism_study.blend.
It is not the finished realistic scene or an approved replacement animation.
The revised furniture/material arrangement has not been animated. Fine-scale
contact, fabric, window surrounds, masonry relief/tiling, foreground dressing,
exterior vegetation/weather and the fire composite need continued visual work.
The asset-based chairs do not duplicate the reference sofa, and room proportions
and architectural ornament are still different. Some old minor props remain.
Do not call this reference-level photorealism without inspecting the new image.

## Reproduce

With the downloaded assets present, using the existing bpy 4.5.3 / Python 3.11
runtime (the script loads the preserved original storm scene):

```sh
OMP_NUM_THREADS=5 REALISM_PERCENT=100 REALISM_SAMPLES=96 \
  /workspace/tools/fire-venv/bin/python scripts/realism_rebuild.py
```

The render writes renders/realism_study.png at 1280 × 720. It saves the new
compressed Blender scene and packs file textures; the original motion scene
is not overwritten. A known bpy cleanup stall can occur after the render.
Completion and actual worker exit/termination are recorded separately in
renders/realism_runtime.json. Source fire still processing is retained in
scripts/prepare_realism_fire.py. No new video is claimed in this pass.

## Final still check

The current review still is 1280 × 720, 96 Cycles samples with OIDN. It was inspected
at full resolution after correcting the camera aim and foreground chair.
The source models and image maps are loaded; most file textures are packed in
realism_study.blend (Blender 4.5.3 LTS). Large stone/wood maps remain relative
external assets; keep assets/ beside the Blender file. A known cleanup stall was stopped
only after render completion, recorded in realism_runtime.json.

The old storm motion scene remains byte-identical to the previous delivered
version. This new still is not an updated animation. Remaining priorities:
exterior/weather realism, architectural proportions/mouldings, secondary
props, more natural dressing and deeper masonry relief. The fire still uses
an image card. The result is not claimed to be indistinguishable from a photo.
