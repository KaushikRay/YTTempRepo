# Heavy refinement and two explicitly labelled Blender variants

This document records the still-render stage. The subsequent layered motion work
is documented in [the motion review](../hybrid_motion/review.md); it uses its own
`rainforest_hybrid_motion.blend` and does not replace either still source scene.

## Modeled scene

`rainforest_cabin.blend` and `renders/realism_still.png` contain the substantial
geometry/material rebuild. Architecture, plants, water and weather are rendered
geometry, lit using the CC0 photographic `rainforest_trail` HDRI plus practical
and sky-fill lights. Changes from the rejected version include:

- Cabin rotated approximately 13 degrees for a less frontal view, with all
  attached architecture, lights and steps moved together.
- Visible near porch wall and extended shelter; bowed/chipped plank geometry,
  photographic grain aligned to the structural members and irregular fastenings.
- 4K weathered timber, soil, gravel and bark maps; varied wetness/roughness in place
  of a uniformly polished surface response.
- Actual interior walls, floor, ceiling, curtains and furniture silhouettes behind
  the windows. The area light is hidden from camera to avoid a white emitter panel.
- Nine timber supports tested against the actual terrain mesh; their bases are
  embedded approximately 18–52 mm instead of hovering.
- Scanned roots, bark litter and moss: 27 root clusters, 73 litter pieces, 184 moss
  colonies and 161 extra regrowth instances in the finished build.
- Shallow gravel-bed water with smaller ripples and three stone-supported riffles.
  Submerged pebbles and ledge rocks are grounded on the creek bed.
- Approximately 19,410 visible rain streaks, softened across width and length,
  with the main covered footprint excluded. Nonuniform, less blue depth mist.

The full-size modeled image still reads as a constructed scene, particularly in
the cabin and palm details. It is not represented as meeting the user's final
photorealism target. More render samples cannot solve that visual-design gap.

## Hybrid variant

`rainforest_hybrid.blend` and `renders/hybrid_still.png` use a generated
photographic-style matte painting as the detailed backdrop, with actual Cycles
rain and geometric depth holdouts composited over it. The plate was generated
with OpenAI image generation using our modeled composition and two CC0 botanical
photographs as references. It is not a camera photograph.

The source plate and its provenance are under `assets/hybrid/`. The generated
source is 1672×941; the Blender compositor scales/crops it to the 1920×1080 output.
The compositor uses Standard colour management so the plate is not tonemapped a
second time. A separate transparent rain pass is written to `renders/hybrid_pass/`.

The camera is locked. Architecture, detailed foliage, stream and whitewater in
this plate are currently static. The rain is a separate animated 3D field. Foreground
leaf separation and moving-water layers still need production work before this
variant becomes a finished ambience video. The hybrid is not presented as a fully
modeled, freely movable 3D scene or a completed animation.

Both variants are preserved for a concrete visual and workflow comparison.

## Sources and rebuild

The additional 13 source assets are CC0 Poly Haven scans/materials/HDRI. Provider
MD5 checks for all 58 downloaded files are in `asset_checks.json`; author/source
records are in `asset_sources.json`. The generated plate has its own explicitly
separate provenance. Earlier research-photo credits are unchanged.

```sh
python scripts/prepare_realism_assets.py
python scripts/build_realism_library.py
python scripts/render_supervised.py
python scripts/check_realism_scene.py
python scripts/render_hybrid.py
python scripts/check_realism_output.py
python scripts/check_portability.py
```

The prior four-second video and `rainforest_motion.blend` belong to the previous
modeled iteration. They are retained as historical motion diagnostics and do not
show either current visual variant. No new motion video or audio is claimed here.
