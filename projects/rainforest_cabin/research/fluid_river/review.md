# Actual 3D fluid study after the workspace reconnect

The user asked for real turbulence instead of image overlays. This is a separate
fully 3D water-method test, not an update claimed to be integrated into the cabin
render. The approved cabin/palm scene and its previous videos are preserved.

## What runs

The preinstalled bpy 4.5.3 Mantaflow bindings fail while initializing Manta grids;
the native Blender 4.3.2 executable aborts during fluid/Python initialization.
Official binary download hosts and three public mirrors are unreachable from this
environment. Those failures are recorded in `environment_checks.json`.

The working alternative is an original **3D position-based fluid solver** running
on Taichi 1.7.4 CPU, following the density-constraint approach of Macklin & Mueller,
*Position Based Fluids* (SIGGRAPH 2013). It models gravity, particle pressure
constraints, solid collisions, a small viscosity term, empirical vorticity
confinement and a continuous inlet/outlet. It is not Mantaflow or a validated
high-resolution CFD solver. No water photograph, movie or animated UV is used.

The refined run contains 51,286 particles at 3 cm spacing, eight substeps per
24 fps frame and four pressure iterations per substep. Six ellipsoidal collision
rocks and a three-drop bed make the flow separate and splash. Four seconds settle
the initial water; four further seconds are cached. The delivered preview uses
the first two settled seconds, 48 native Cycles frames at 960×540 / 24 fps.

Surface meshes are reconstructed on a 2 cm grid. Foam is an empirical field based
on exposed particles' velocity/curl and decays with time; small surface bubbles
are geometry derived from those particles. Foam is not a simulated air phase.
The water uses transmission/refraction, surface normals and geometry, lit by the
existing CC0 photographic rainforest HDRI. Rock materials/scans are existing CC0
Poly Haven assets documented elsewhere in this project.

## Honest visual review

The first 16,696-particle render had coarse sheets and excessive white foam, and
was rejected. The refined test is more transparent, with lower foam coverage.
It still visibly reads as a simulation: smooth collision rocks, coarse surface
features, bubbly edges and abrupt splash shapes need further work. It is not
presented as meeting the final photographic realism target.

Judge this clip for genuine volume motion, obstacle interaction, falling sheets
and spray. It is a standalone view with a different camera from the cabin. There
is no rain soundtrack, long video, seamless loop or completed cabin integration.
The next step is to improve the surface/whitewater detail and calibrate a river
bed and camera to the approved cabin view, retaining the approved palm movement.

## Files and playback

- `rainforest_fluid_study.blend`: physical study scene, saved at frame 1.
- `renders/fluid_river/preview.mp4`: two-second native motion proof.
- `assets/fluid_river/fluid_cache_01.zip` and `_02.zip`: 48 mesh/foam frames,
  stored as compressed NumPy arrays. Keep both archives in their relative folder.
- `scripts/simulate_fluid_river.py`: solver and surface reconstruction.
- `scripts/render_fluid_river.py`: PBR scene and direct native-frame renderer.

To scrub the cached geometry inside Blender, open the scene, select its embedded
`ENABLE_FLUID_PLAYBACK.py` text in the Scripting workspace and run it once. Then
change frames normally. The helper reads the two cache archives directly; NumPy
is required. The geometry updates may not run at real-time speed in the viewport.
The supplied MP4 is encoded at a native 24 fps, without optical interpolation.

For a complete rebuild in the supplied environment:

```sh
python scripts/simulate_fluid_river.py
SAMPLES=16 WIDTH=960 RENDER_FRAMES=48 python scripts/render_fluid_river.py
python scripts/package_fluid_cache.py
python scripts/check_fluid_river.py
```

Raw simulation arrays and intermediate PNGs stay local/ignored. The two archives
contain the geometry needed for the delivered two-second proof. The remaining two
seconds of local cache are not represented as published footage. All final reports
record solver settings and limitations explicitly.

## Completed verification

All 48 geometry frames and all 48 decoded video frames are distinct. Sampled
particles remain above the bed and outside the rock collision shells; their mean
downstream velocity is about 0.61 m/s. The packaged caches pass CRC and SHA-256
checks. A relocated scene enables its embedded playback and changes water/foam
geometry at frames 1, 24 and 48 without raw solver arrays. Its water material has
zero image textures. These checks establish the 3D method and delivery integrity,
not perceptual realism or CFD validation. See the QA and playback reports.
