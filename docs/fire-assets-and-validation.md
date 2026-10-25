# Fire and candle iteration

## Investigation

The previous hearth used transparent emitting ribbons, which produced the
cloth-like appearance reported by the user. Candle flames were 17 cm tall
before animation scale changes: much too large for the candle bodies.

Checked sources:

- Blender Quick Smoke / Fire implementation (official source, accessible):
  https://raw.githubusercontent.com/blender/blender/main/scripts/startup/bl_operators/object_quick_effects.py
- Blender gas rendering manual (network proxy denied access):
  https://docs.blender.org/manual/en/latest/physics/fluid/type/domain/gas/rendering.html
- Poly Haven asset catalogue (network proxy denied access):
  https://api.polyhaven.com/assets?t=models
- Official Blender Python distributions, available through PyPI:
  https://pypi.org/project/bpy/

No third-party fire asset was downloaded or incorporated. We did not establish
an accessible, licensed stock-fire asset suitable for this scene.

## Simulation outcome

The system Blender 4.3.2 crashes when its gas domain initializes, with a
PyImport_AppendInittab / Python initialization error. An isolated official
bpy 4.3.0 runtime and bpy 4.5.3 LTS runtime also failed during gas solver
initialization (LevelsetGrid.setConst / Mantaflow cache errors). NumPy was
pinned to 1.26.4 after diagnosing binary compatibility warnings.

Failed simulation experiments are outside the project, under
/workspace/scratch/fire-experiment. No broken fluid modifiers or unbaked
cache are included in the delivered scene.

## Delivered approach

The hearth now uses a procedural three-dimensional emitting volume, with
asymmetric tapered envelopes, animated 4D noise, and blackbody colour. This is a shader approximation, **not a baked simulation**.
The flame should be evaluated in the renders; it is not claimed to match
photographed or simulated fire yet.

Candles have rebuilt rounded wax bodies, recessed molten tops, small dark
wicks, thin rivulets, and approximately 32–43 mm tall volumetric flames.
Flames have a small blue base and temperature-based warm colour. Candle
illumination is provided by small practical lights rather than giant glowing
surfaces. Wax has subsurface scattering.

Stone has additional mineral mottling and geometric surface relief.

## Rendering

The standard system Blender lacks OpenImageDenoise. The official bpy 4.5.3 LTS
wheel has it, so review renders use that separate runtime. The saved scene
remains generated with Blender 4.3.2. Review rendering does not resave/upgrade it.

```sh
LOUNGE_SKIP_RENDER=1 LOUNGE_PREVIEW_PERCENT=100 LOUNGE_SAMPLES=128 \
  blender -b -t 5 --python scripts/build_scene.py
OMP_NUM_THREADS=5 LOUNGE_PREVIEW_PERCENT=100 LOUNGE_SAMPLES=80 LOUNGE_DETAIL=1 \
  /workspace/tools/fire-venv/bin/python scripts/render_review.py
```

The isolated renderer needs Python 3.11, bpy==4.5.3 and numpy==1.26.4.
The second command renders the room and a separate candle close-up.
The animation and its loop seam remain unvalidated. No audio is included.

## Visual checks during this pass

Rejected initial volume tests that produced overexposed blobs or a rectangular
bright patch. A low-resolution test of narrow, irregular tapered envelopes
resolved that container outline; increased their temperature and size for the
room review render. The final hearth remains a procedural approximation, not
a photographic fire asset or physically simulated combustion.

A separate 960 × 720 candle view completed at 96 samples with denoising.
Inspection confirmed reduced flame scale, visible wicks, melted rims and
drips. The surrounding props and upholstery remain simplified.
