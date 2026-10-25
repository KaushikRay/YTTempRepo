# Three-second motion study

The current Blender scene has a 24 fps / 72-frame timeline. The rendered
preview samples frames 1,3,...,71 and encodes 36 images at 12 fps, giving three
seconds of motion at normal speed. It is 640 × 360, 12 Cycles samples with
OpenImageDenoise: a coarse motion check, not the final quality target.

## Motion changes

- Downloaded CC BY fire source seconds 2–5 are resampled to a 72-frame,
  1280 × 720 RGBA sequence. Temporal background subtraction and bright-core
  masking are applied per frame. This is video-derived fire, not a simulation.
- Measured fire brightness drives smoothed hearth-light energy.
- Rain falls and drifts with individual wrap phases, avoiding one simultaneous
  reset of the whole field. Droplets slide; rivulet length changes subtly.
- Candle flames tilt and change height gently; their lights flicker at
  independent phases.
- Exterior tree parent transforms are corrected, and the trunks sway around
  their roots. Tree geometry remains a placeholder rather than final vegetation.

## Reproduce

Use the existing Python 3.11 environment with NumPy and official bpy 4.5.3,
plus Blender 4.3.2 and FFmpeg:

```sh
/workspace/tools/fire-venv/bin/python scripts/prepare_fire_motion.py
blender -b -t 5 --python scripts/setup_motion.py
OMP_NUM_THREADS=5 /workspace/tools/fire-venv/bin/python scripts/render_motion.py
/workspace/tools/fire-venv/bin/python scripts/encode_motion.py
```

`setup_motion.py` modifies the current scene and saves it. Do not run
`build_scene.py` afterward unless you intend to rebuild the still scene and
then repeat motion setup. Keep assets/fire/sequence next to the Blender file;
the animated images are external relative-path assets, not a packed movie.
Download the whole repository branch if you want to open the animated scene.

The renderer saves progress in renders/motion/run.json. It can resume an
unchanged setup, skipping completed frames. If scene/settings/source images
change, archive old motion frames and start a new run; do not reuse stale PNGs.
Raw render PNGs are ignored by Git. The keyed fire sequence is retained.

## Validation and limits

Runtime checks evaluate rain, candle and tree animation at several frames,
and verify 72 distinct fire images. The encoder verifies 36 distinct rendered
frames, decodes the MP4s, checks duration/frame count and measures changes in
both the fire and window regions. See runtime_checks.json and qa.json.

Fire/window clips are magnified crops of the full-room video, not independent
high-resolution renders. Sampled frames and motion-region changes are checked;
user playback review is still needed. There is no audio, lightning pass, final
smooth 24 fps render, seamless-loop validation or long video in this iteration.
The mask can trim dim fire wisps, and image-card compositing may still flicker.

## Runtime cleanup observation

All 36 frames were written and the render loop reported completion in 313 s.
The official bpy runtime then stalled in interpreter/native cleanup, emitting
"Freeing memory after the leak detector has run" messages. The finished worker
was terminated after the MP4s had been encoded, decoded and validated. This is
not recorded as a clean renderer process exit. The delivered outputs passed
the checks in qa.json; the shutdown issue remains a runtime limitation.
