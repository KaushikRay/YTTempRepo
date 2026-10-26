# Interior creeper and storm visibility iteration

This records the previous creeper milestone. The current image is updated by
the [lighting/exterior pass](lighting-exterior-iteration.md), which supersedes
the leaf geometry, attachment method and counts reported below.

## Reference details

The original image shows woody climbing growth on shaded stone piers, irregular
patches and gaps between leaves, greenery beside the tall windows and around
the outside of the hearth. Leaf highlights catch the window light and warm
practicals. It does not show a uniform hedge pasted onto the walls. The main
window view and fire opening should remain readable.

## Asset search and source

Searched Poly Haven's model catalogue: no ready-made ivy asset was found.
BlenderKit's public search returned free ivy generators and wall climbers,
but its asset download endpoint returned HTTP 403; the public thumbnail host
and licence page were also blocked. No account or authenticated access was
used. AmbientCG's atlas API was blocked. Search results/attempts are retained
in `research/creeper/`. None of those unavailable ivy models was imported.

Instead, authored tapered branching vines and curved lobed leaf geometry.
Downloaded actual CC0 ivy photographs through Wikimedia Commons. The large
central leaf in the first photo supplies UV-sampled colour/vein detail. No
background photograph is pasted over the room, and no generated image is
presented as a Blender render. The second photograph was inspected for stem
attachment, alternating leaves, irregular overlap and weathered colour.

- [Hedera helix leaf, Aethonatic](https://commons.wikimedia.org/wiki/File:Hedera_helix_leaf_-_16_June_2025.jpg), CC0.
- [Beginning leaf diphormism in Hedera helix, Zamioculas](https://commons.wikimedia.org/wiki/File:Beginning_leaf_diphormism_in_Hedera_helix.jpg), CC0.

Original photos, licence URLs, author metadata and SHA256 hashes are retained
in `assets/creeper/provenance.json`. This is a photo-textured custom plant,
not a claim that a scanned ivy model was obtained. The material uses colour,
gentle vein bump and translucency; a measured botanical PBR scan is not claimed.

## Implemented

- Four connected growth patches: two left stone piers, the wall beside the
  windows and the outer hearth cheek. Roots begin at floor level. Branches
  taper, petioles join the leaves to stems and leaves have curved surfaces,
  lobed silhouettes, varied scales, angles and colour.
- Keep growth outside the open firebox and the main window apertures.
- Denser, layered exterior rain with tapered opacity, water distortion on the
  glass and a separate exterior mist volume. The room contains no mist volume.
- Reduce the graphic square pattern and warm saturation of the foreground rug.
- Keep the original motion scene unchanged; the new creeper and weather are
  a still-development pass and have not yet received a moving test.

## Build and review

The normal realism build now runs `scripts/creeper_weather_pass.py` after the
historic construction pass. It updates the existing scene and still paths.
The supervisor records actual render progress and handles the known post-render
bpy cleanup stall separately from successful image creation.

```sh
OMP_NUM_THREADS=5 REALISM_PERCENT=100 REALISM_SAMPLES=96 \
  /workspace/tools/fire-venv/bin/python scripts/render_realism_supervised.py
```

Retain the complete assets directory beside `realism_study.blend`; the large
stone/wood maps remain external relative files. Most other image textures,
including the used leaf photograph, are packed.

## Limits

The creeper layout is intentionally composed to the locked camera; the wall
projection is an approximation and fine attachment still needs improvement.
The leaf atlas uses one photographed leaf region with shape/rotation variations;
additional botanical texture variants would reduce repetition in a close-up.
The village remains simple geometry and there are no new detailed exterior
trees in this pass. The fire remains licensed footage integrated on a card.
This is not a finished photoreal scene or an updated storm animation.

## Final review and checks

Rendered 1280 × 720 at 96 Cycles samples with OpenImageDenoise. Compared it
side by side with the original reference (reference left, new still right in
`renders/realism_comparison.png`). Creeper placement and rain visibility are
clearer. The reference still has richer layered dressing, more organic surface
variation, softer light transitions and a more convincing landscape. The new
rain is more legible, but its motion has not been tested. This iteration does
not establish that the scene could pass for a photograph.

The final build contains 1,566 leaves in four connected growth patches and
3,060 tapered rain streaks. Checked a separate foliage close-up; the first
angular lobe outline was revised to curved edges, then the full scene was
rendered. Leaf atlas repetition, approximate wall attachment and fire proximity
still need refinement before a closer or moving camera is used.

Scene checks found 42 used file images packed, nine relative external PBR
maps present, and no missing used file textures. The Blender file remains
below GitHub's 100 MiB file limit. The original `storm_lounge.blend` content
hash is unchanged. `renders/realism_review.json` records the output image hash,
dimensions, sampling and remaining gaps. The render supervisor records the
known native cleanup stall separately from render completion.
