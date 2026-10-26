# Foliage, lighting and exterior depth iteration

## Reference goals

The original reference has dark overlapping ivy with irregular botanical leaf
shapes, warm pools of practical light, cool light from the wet windows, detailed
foreground materials and layered exterior depth. The previous still repeated
one generic folded leaf shape and had no detailed trees. This pass addresses
those three priorities; the original reference remains the visual target.

## Foliage

Traced three leaves from the retained CC0 ivy growth photograph: different
lobe proportions, broad/rounded outlines and different vein patterns. Leaf
geometry and UVs now use the same measured outline. Nine shallow curvature
variants replace the old star-shaped, heavily corrugated generic mesh. Leaf
size, pose and tint still vary per instance. The atlas is an oriented version
of the actual source photograph, not a generated picture. Original source
metadata and the trace coordinates are retained in `assets/creeper/`.

Leaders and petiole attachment points are ray-projected onto evaluated wall,
pier, jamb and mantel geometry. This replaces the previous analytic surface
approximation. Projection still needs visual checking around abrupt corners;
it is not a biological growth or collision simulation.

## Lighting

Reduced the broad orange point-light wash and the general room fill. Made
window area sources tall and rectangular, lowered their intensity and used
a broad, weak reflected window source across the seating. The hearth remains
warm. Upper firebrick darkens toward the chimney throat. AgX is retained.
This is an art-directed physically based render, not a measured light survey.

## Exterior assets

- [Fir Tree 01](https://polyhaven.com/a/fir_tree_01), CC0, Rob Tuytel
  (photography) / Rico Cilliers (modeling). Two instances of detailed variant C.
- [Shrub 02](https://polyhaven.com/a/shrub_02), CC0, Rico Cilliers. One group
  of foreground vegetation with 2K PBR texture maps.

These are detailed ready-made assets, replacing the former absence of real
tree geometry. The fir source contains three variants in a 478 MB buffer.
Only the complete C variant's accessor ranges were retrieved (about 33 MB),
without simplifying its geometry. HTTP Content-Range and each returned byte
count were checked. Original provider MD5 was checked for the source glTF and
downloaded textures; a whole-file MD5 of the undownloaded 478 MB buffer is not
claimed. Range hashes and the compact buffer hash are retained in provenance.

Both assets are normalized to one metre high in a separate, compressed
`assets/exterior/vegetation.blend` library with packed textures. Scene instances
set the fir heights to 9.2 m and 10.5 m; the shrub group is 1.05 m high. Library
placement matches the elevated exterior ground. A wet sloping apron joins the
window-level ground to the village ground. Rain and mist remain between the
viewer and landscape, with less uniform glass distortion so branches and roof
glimpses remain possible. The village buildings are still simple geometry.

## Reproduce and review

Download the complete branch, including `assets/`. The main Blender file
requires the relative `assets/exterior/vegetation.blend` library and existing
external stone/wood maps. The linked library's own textures are packed.

The source assets and prepared library are supplied. To rebuild the library
from those source files:

```sh
OMP_NUM_THREADS=5 /workspace/tools/fire-venv/bin/python scripts/build_exterior_library.py
```

To recreate the oriented photographic atlas and traces, use system Python
with Pillow; then render using the bpy environment:

```sh
python scripts/prepare_leaf_atlas.py
OMP_NUM_THREADS=5 REALISM_PERCENT=100 REALISM_SAMPLES=96 \
  /workspace/tools/fire-venv/bin/python scripts/render_realism_supervised.py
OMP_NUM_THREADS=5 /workspace/tools/fire-venv/bin/python scripts/check_realism_delivery.py
```

The render updates `realism_study.blend` and `renders/realism_study.png`.
`renders/priority_comparison.png` puts the previous iteration on the left and
the current one on the right. `renders/realism_comparison.png` compares the
original reference on the left with the current render on the right.

## Remaining gaps

The village buildings, foreground dressing and room proportions still differ
from the reference. Fire is licensed footage integrated on a fixed-camera
card. Leaf photos contain baked highlights and only three source specimens;
they are not a measured, fully de-lit botanical PBR scan. New ivy, tree and
weather motion has not been tested. This is a still-development iteration,
not a final photorealism claim or a new video.

## Final still check

The 1280 × 720 still completed at 96 Cycles samples with OpenImageDenoise.
It was inspected against both the original reference and the previous
iteration. Tree branches are visible through the upper window regions, with
a partial view of roofs/windows below. The room has less broad orange fill,
and the ivy has broader, more varied photographed shapes. The reference still
has more natural furnishing, richer dressing and architectural detail; this
pass does not claim that the photorealism target is reached.

Delivery checks found 1,550 interior leaves across four growth patches, three
exterior collection instances, 51 used packed file images and nine existing
external PBR maps with no missing files. The linked vegetation library path
and SHA256 were checked. Both Blender files are below GitHub's individual
100 MiB limit. The original motion scene content hash is unchanged. Render
completion and the known post-render native cleanup stall are recorded
separately in the runtime/status JSON files.
