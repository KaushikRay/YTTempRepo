# Rainforest cabin — new scene

Independent Blender project based on the tropical rain cabin reference supplied
in chat. The canceled tavern project is not modified.

## New 3D liquid-method study

[Watch the fully 3D water test](renders/fluid_river/preview.mp4)
· [Rendered still](renders/fluid_river/still.png)
· [Method, playback instructions and visual limitations](research/fluid_river/review.md)

The workspace has reconnected and a working CPU particle-fluid solver now
produces actual 3D water meshes. This standalone 960×540 / 24 fps, two-second
study uses 51,286 simulated particles, gravity, pressure constraints, solid rocks
and simulation-derived foam. It uses no image or footage for water motion.

This is a physical-method proof, not an integrated revision of the approved cabin
view or a final photoreal river. Coarse surfaces and test-channel details still
need refinement. The approved palm/cabin scene is preserved. The next stage is to
improve the water/foam detail and fit a simulated channel to that camera.

`rainforest_fluid_study.blend` is the study scene; keep the two cache ZIP files
under `assets/fluid_river` beside the project. In Blender, run its embedded
`ENABLE_FLUID_PLAYBACK.py` once to enable cached geometry playback.

## Previous image-based river revision

The palms are retained as approved. The revised river replaces the weak wobble
with directional photographic texture transport, modulated by real CC0 rapids
footage. Water travels down the cascades and toward the bottom right through the
foreground pool. Fixed banks and rocks frame ten feathered water footprints.

[Revised full scene](renders/river_flow/preview.mp4)
· [Revised river close-up](renders/river_flow/water_detail.mp4)
· [Previous/revised motion comparison](renders/river_flow/water_comparison.mp4)
· [Method, sources and remaining limits](research/river_flow/review.md)

The current `rainforest_hybrid_motion.blend` uses two packed images plus the
relative `assets/river_flow/real_rapids.mp4` movie. Download that asset alongside
the scene. The clip is a silent six-second, 1080p/24 fps motion test, not yet a
seamless long video or a fluid simulation. See the river QA report for actual
rendered-pixel motion tracking and checks preserving the approved outside image.

## Previous layered motion preview

![First native frame of the layered motion scene](renders/hybrid_motion/still.png)

The photographic hybrid is now prepared as a layered Blender animation. The
foreground palms flex separately from a clean background, seven stream patches
move locally, rain recycles continuously, and eave beads/stream impacts animate.
The six-second 1080p / 24 fps clip is complete: 144 native Cycles frames, with no
frame interpolation. Detailed architecture and distant forest remain a generated
static matte. This is a locked-camera 2.5D scene, not fully modeled. It is silent
and not yet a seamless loop; the water is localized image-based animation.

[Watch the new full-frame motion preview](renders/hybrid_motion/preview.mp4)
· [Palm detail crop](renders/hybrid_motion/palms_detail.mp4)
· [Water detail crop](renders/hybrid_motion/water_detail.mp4)

[Method, rebuild and limits](research/hybrid_motion/review.md)
· The source scene has since been updated for the river revision above.

## Previous still refinement — two clearly labelled variants

![Hybrid Blender still: generated static matte and 3D rain](renders/hybrid_still.png)

[Hybrid Blender still](renders/hybrid_still.png): a generated photographic-style
static matte with separately rendered 3D rain and depth holdouts. The cabin,
detailed foliage and stream in the matte are currently static; they require
separate animation layers for a video. The camera is locked. This is not a camera
photograph or a fully modeled version of the detailed backdrop.

[Rebuilt modeled 3D still](renders/realism_still.png): photographic forest lighting,
weathered 4K materials, angled cabin, interior depth, scanned ground detail and
shallow stone riffles. This version still reads as a constructed scene and has
not met the final realism target.

[Detailed changes, sources and limits](research/realism/review.md)
· [Comparison of the two current approaches](renders/realism_variants.jpg)

Source files: `rainforest_cabin.blend` (modeled) and `rainforest_hybrid.blend`
(generated static matte + native 3D rain). All earlier stills are retained.

## Previous motion diagnostic

[Watch the four-second motion test](renders/motion/preview.mp4)
· [Placement, motion details and checks](research/tree-and-motion.md)

This historical motion test is silent, 640×360, native 24 fps / 96 frames. It checks falling
rain, gentle leaf sway/flex, creek movement, expanding ripples and eave runoff.
It belongs to the previous scene revision and does not show the current rebuilt
or hybrid variants. It is not final YouTube quality or a seamless loop.

[Real-photograph reference board](research/forest_photographs/reference_board.jpg)
· [Photograph credits and licences](research/forest_photographs/CREDITS.md)
· [Neutral-light leaf comparison](renders/leaf_comparison.jpg)
· [Reference observations and implementation](research/foliage-study.md)

The previous JPEG glTF leaf textures had fully opaque alpha channels. The corrected
libraries use the provider's separate silhouette masks, including canopy masks.
Four understory assets now use 4K photographic maps. Wide paired palm strips have
been replaced with curved, staggered pinnae and varied droop. No reference
photographs are used as render textures.

## First milestone

Build and inspect a still from a sheltered timber porch looking across a rocky
stream at a raised wooden cabin. Foreground palms frame the view; tropical
undergrowth and mist separate the cabin from the forest. Cool storm illumination
is balanced against a small warm lantern. Match the reference composition before
attempting a long animation.

Reference details: dark porch at left, near post around the left third, overhanging
roof, pitched tiled cabin roof, front veranda, warm wall lantern, uneven stone
steps, sinuous shallow stream, wet rocks, ferns and large glossy palm fronds.
The reference is visible in chat; the attachment is not exposed as a local file.
Do not substitute the old tavern reference or claim a pixel-aligned comparison.

## Asset approach

Use publicly downloadable CC0 Poly Haven ferns, broadleaf plants, rocks, tree
geometry, 2K architectural/canopy maps and 4K understory leaf maps. The catalog contains no suitable complete palm or
matching cabin: build these as original detailed geometry. Source manifests,
checksums and credit links are retained alongside the project.

## Intended checks

Inspect composition, geometry contact, texture orientation, rain visibility,
water reflections, shadow detail and close foliage before the final still.
This milestone is a still, not an approved animation or finished YouTube video.

## Render and rebuild

Use Python 3.11 with `pip install -r requirements.txt`. No paid assets or logins
are required. `scripts/prepare_assets.py` fetches the original glTF sources and
2K/4K maps and separate alpha masks, verifies provider MD5 checksums and keeps the manifests. The supplied
Blender libraries already contain the scanned model geometry and packed maps.

From this project directory:

```sh
python scripts/prepare_assets.py
python scripts/build_asset_library.py
python scripts/prepare_realism_assets.py
python scripts/build_realism_library.py
python scripts/render_supervised.py
python scripts/check_realism_scene.py
python scripts/render_hybrid.py
python scripts/check_realism_output.py
python scripts/check_portability.py
```

The supervisor defaults to `renders/realism_still.png`, a 1920×1080, up-to-128-sample Cycles CPU still. For a quick
composition diagnostic, use `WIDTH=640 SAMPLES=24 OUTPUT=composition.png` before
the supervisor command. It writes `status.json` and `logs/render.log`. All output
is under this project. The final scene is `rainforest_cabin.blend`; download this
entire project folder to retain linked model libraries and architectural maps.

The render worker explicitly exits after the completed image write, bypassing
a known native bpy shutdown stall in this environment. It does not interrupt an
unfinished render. The supervisor marks success only after the completion marker
and a zero worker exit code.

## First still: realism limits and next milestone

This is an initial camera/material/lighting study. The cabin and palms use original
geometry; scanned assets provide detailed ferns, broadleaf plants, rocks and canopy.
The reference's very dark foreground, dense organic layering and irregular cabin
silhouette remain the comparison targets. Look for overly even timber/shingles,
repetitive palm leaflets, an unnaturally uniform forest and insufficient stream
turbulence. More samples cannot solve those geometry/material issues.

Rain streak geometry has independent recycling drivers. It is an optical exposure
approximation, not a fluid or droplet-collision simulation. Eave strands and ripple
rings in this still are static. Stream flow, splash timing, wind, rain wrap visibility
and temporal denoising require review in the short moving test. The first silent
motion diagnostic is supplied; no soundtrack or long video has been produced.
Do not describe this study as finished ultra realism.

Next review priorities: camera/framing and night mood first, then irregularity of
the timber/roof, foreground palm realism, stream detail and visible rainfall.
After those are satisfactory, animate rain, stream/runoff and restrained plant
movement and render a short test before producing a long YouTube sequence.
