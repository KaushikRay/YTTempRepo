# Twelve-second rainforest river loop — review stage

This stage extends the approved integrated cabin preview into a twelve-second,
1920×1080, native 24 fps visual loop. It retains the approved framing, wet palms,
cozy cabin lighting and hybrid photographic-style background.

## Motion and loop construction

The existing Taichi CPU position-based particle-fluid solver runs 408 simulation
frames: 96 warmup frames followed by 312 new water states. The 288-frame delivery
uses a one-second overlap. During output frames 1–24, the continued tail states
289–312 blend into head states 1–24 in **3D density/froth field space**, with a
smoothstep weight. Each blended field is remeshed and then rendered normally.
Frames 25–288 retain their direct simulated surface geometry.

Both source states advance forwards. There is no reverse playback, rendered-image
dissolve, video interpolation, animated water photograph or water footage.
The loop transition is an artistic approximation; it is **not** a periodic solution
of the fluid equations. Its interior can soften or merge small surface features,
so the first second needs visual review in the river close-up.

Rain and roof-runoff frequencies are rounded to integer cycles per twelve seconds.
The optical streak count, widths, directions and positions remain as approved.
Palm geometry, root anchoring and the six-second sway drivers remain unchanged;
two full palm cycles fit the twelve-second loop. All frames are rendered natively,
including the new periodic rain; the old six-second image cache is not replayed.

## Reference comparison and limitations

The supplied reference emphasizes wet tropical leaves, dark timber shelter,
a narrow rocky stream, dense rain, forest depth and a warm cabin light. The
approved photographic hybrid carries those features. Compared with the original
blue nighttime reference, the accepted scene has brighter, greener storm light;
this stage preserves that accepted direction.

The cabin, most forest and rock appearance remain generated static imagery.
Camera-projected bank proxies approximate their geometry; the bed is a generated
water-free texture beneath actual refractive liquid. This is not a fully modeled
rainforest. The small upstream stream glimpse reuses a posed instance of the same
water bake, rather than a second hydrodynamic calculation. Coarse water meshing,
empirical foam and approximate rock contact geometry remain visible limitations.
A longer clip does not by itself establish photographic realism.

## Review files

- `renders/looped_fluid/preview.mp4`: the twelve-second full scene.
- `renders/looped_fluid/river_detail.mp4`: native river crop.
- `renders/looped_fluid/repeat_test.mp4`: two repetitions, with the join at 00:12.
- `renders/looped_fluid/still.png`: full-resolution frame 144.
- `renders/looped_fluid/qa.json`: decoded media, cache and contact checks.
- `research/looped_fluid/scene_checks.json`: relocated playback and rain/palm repeat checks.

The clips are silent visual tests. They have no subscribe badge or release intro;
those belong to a later approved YouTube build, not to this loop inspection.

## Source and reproducibility

Open `rainforest_looped_fluid.blend`, retain the twelve cache ZIP files under
`assets/looped_fluid`, and run its embedded `ENABLE_INTEGRATED_FLUID_PLAYBACK.py`
once. It enables looping mesh updates, including frame 289 wrapping to frame 1.
The HDRI must retain its relative path. Other visible image assets are packed.
Python dependencies are listed in the project requirements (bpy, NumPy, SciPy).

From the project folder, using the configured Python/Blender environment:

```sh
FLUID_VARIANT=looped_fluid FLUID_FRAMES=408 WARMUP=96 python scripts/simulate_fluid_river.py
python scripts/prepare_fluid_loop.py
python scripts/prepare_loop_foam.py
SAMPLES=32 python scripts/render_looped_fluid.py
python scripts/package_fluid_loop.py
python scripts/check_fluid_loop.py
python scripts/check_looped_scene.py
```

The renderer resumes intact frames only when its source/bake signature matches.
Raw particles, meshes, native PNG frames and logs stay local and are ignored by
Git. The delivered ZIP archives carry all playback mesh/foam states; selected
unmodified solver particles support independent collision/flow checks.

## Next gate

Review naturalness of the first-second water transition and the repeat at 00:12,
including rock edges and upstream contact. After that visual review, source and
vet licensed rain/stream audio and create a longer audiovisual review before any
multi-hour YouTube release build.

## Completed checks and actual result

All three H.264 videos decode cleanly. The full scene and river crop each contain
288 distinct decoded frames over exactly twelve seconds. The repeat test contains
576 frames over twenty-four seconds, with both decoded repetitions identical.
All twelve cache archives passed CRC and per-member SHA256 checks, covering
288 distinct liquid meshes and 288 foam states.

The river-region pixel change across frame 288 → frame 1 is 0.9634 times the
largest sampled neighboring-frame change. This passes the motion-outlier check;
it does not prove a perceptually invisible transition. Sampled solver particles
have zero bed penetration and remain outside the expanded rock collision shells.
Their average downstream speed is approximately 2.0–2.15 m/s.

Relocated Blender playback passed without raw mesh files. The script updates the
first-second transition, later frames and frame 289 wrapping to frame 1. Rain
repeat-position error is below 0.000006 m in local geometry; palm repeat error is
zero. The water shader has no image textures, and no movie images are used.

Native frames 1, 12, 24, 72, 144 and the seam contact sheet were inspected. The
approved framing and cozy cabin light remain. The water has visibly coarse/glossy
surfaces at close range, especially on the upper step, and the photographic bank
proxies remain approximate. The transition can soften small surface details.
These are still review limitations; this result is not presented as final
photographic realism. Motion was checked numerically and through sampled frames;
the two-repeat video is provided for direct visual assessment.

[First-second details](../../renders/looped_fluid/transition_details.jpg)
· [End/start seam details](../../renders/looped_fluid/seam_details.jpg)

The complete native render took 3,458 seconds (about 58 minutes) on four CPU cores,
at a 32-sample cap with denoising and adaptive sampling. No frames were resumed
from an earlier clip, and no rendered image dissolve or video interpolation was
used. The longer simulation took 254 seconds, plus loop preparation and checks.
