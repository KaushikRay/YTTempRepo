# River flow revision after palm approval

The user approved the palms and rejected the river because it did not flow.
The previous seven patches used small random UV perturbations: pixels changed,
but most photographic whitewater stayed fixed. The previous pixel-difference QA
did not establish directional motion, which was the actual visual requirement.

## Revised approach

- Retain the approved palm grid, shape keys and driver expressions exactly.
  Before/after SHA-256 fingerprints are in `palm_preservation.json`.
- Remove all seven old wobble patches and the 36 artificial impact rings.
- Ten traced creek footprints now transport the photographic water texture
  downstream: about 38 source pixels/s down the drops and 42 pixels/s across the
  lower pools, with small lateral/vertical components following the stream.
- Two overlapping transport phases crossfade at their wrap boundaries instead
  of visibly resetting the texture. The borders feather approximately seven
  source pixels into the static banks. A photographic luminance mask protects
  dark rock recesses; darker pools use a lower threshold than whitewater.
- Real CC0 rapids footage supplies changing water turbulence, modulating the
  transported photographic texture while retaining its lighting and colour.
  Source: **Cbaile19, Rapids and Falls of the Youghiogheny at Ohiopyle**, Wikimedia
  Commons, CC0 1.0. The selected steady-camera source interval is 70–78 seconds.
  The audio is not used. Complete metadata/credit links are in `assets/river_flow`.

An initial direct footage replacement looked pasted on; it was rejected before
delivery. The final technique retains the creek's photographic colour and uses
the real footage for temporal turbulence, with explicit directional transport.

## Review and limits

Inspect both the water crop and full scene. Whitewater should travel downward,
and the foreground current should travel toward the bottom right. Inspect the
rock contacts for sliding edges, repeated transported features, and doubled foam
during phase crossfades. Border pixels still contain some static source water.
This remains a locked-camera image-based hybrid; it is not a fluid simulation or
a fully modeled river. A silent six-second diagnostic does not establish a long
seamless ambience loop. The user must judge whether the flow now feels natural.

The approved native full frames are reused outside a 1040×400 lower-scene border;
Blender rerenders that region including its original rain, palms and river at
1920×1080 pixel density. This keeps the approved outside image pixels intact and
avoids rendering the entire scene again. A cache-free rebuild renders whole
native frames instead. No video frame interpolation is used.

## Rebuild and files

```sh
python scripts/update_river_flow.py
python scripts/render_river_flow.py
python scripts/check_river_flow.py
```

Use the supplied bpy environment for the update/render, and Pillow/NumPy for
output checks. The update modifies `rainforest_hybrid_motion.blend` in place.
Both background/palm images remain packed; the CC0 movie must stay beside it at
`assets/river_flow/real_rapids.mp4`. Its relative path is verified in a relocated
project. `renders/river_flow` contains the revised full preview, native water crop,
side-by-side previous/revised water video, first frame and QA reports. The previous
delivered MP4 remains under `renders/hybrid_motion` for comparison.

## Completed checks

All three six-second clips decode cleanly at 24 fps / 144 frames. Template
matching in rendered water regions measures median travel of 3 pixels downward
in the falls, and 6 right / 2 down in the foreground pool over three frames.
The previous foreground pool tracked close to stationary. These local measures
confirm travel, not subjective naturalness. Five sampled native full frames have
zero changed pixels outside the rerendered river border; palm data fingerprints
match the approved original. The relocated scene resolves its one relative movie
asset alongside the two packed images. Full results are in `renders/river_flow/qa.json`.
