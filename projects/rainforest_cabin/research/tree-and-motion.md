# Clear central view and first motion test

The isolated palm previously at (-2, 22) is moved six metres into the left forest,
including its trunk and all eight fronds. Five bare pole-like background trunks
whose bases projected into screen x=0.43–0.55 are relocated to the side forest.
All moved trunks are grounded again using the same terrain surface. The camera,
cabin and porch framing remain fixed. Placement records are retained in
`palm_relocation.json` and `tree_relocation.json`.

The full-size static review is `renders/clear_view_still.png`, 1920×1080 and up to
128 Cycles samples. Earlier foliage stills are retained for comparison.

## Motion test

`renders/motion/preview.mp4` is a four-second, silent, native 24 fps test, comprising
96 distinct rendered frames at 640×360 / 12 Cycles samples. It checks movement;
the full-size still remains the material/detail reference. It is not the final
YouTube quality export and is not a seamless loop.

- Existing 9,107 recycling rain streaks continue falling through the full clip.
- All 51 palm fronds sway around their stem attachments; 11 foreground fronds
  also flex along their length, with matching midrib deformation.
- 389 near/middle understory instances have restrained, differently phased sway.
- Two travelling geometric wave fields and advected surface shading animate the
  creek. This is a procedural surface approximation, not a fluid simulation.
- 70 small ripple rings expand and disappear; 25 eave-runoff strands vary length.
- The camera, lantern brightness and architecture stay fixed.

Checks evaluate frond root positions and geometric wave changes at five timeline
positions. A separate render check validates 96 native frames, four seconds,
24 fps, no audio, a clean decode and unique source-frame hashes. The final visual
check looks for detachment, rain clearing, distracting jumps and denoiser flicker.

## Completed checks and remaining limits

The completed MP4 decodes cleanly: 96 distinct source PNGs and 96 distinct decoded
pixel frames, 24 fps, exactly four seconds, no audio. Frond attachment-point drift
was zero at the five checked timeline positions. Both Blender files reopened from
a different directory with their assets present. The maximum adjacent change in
whole-frame mean luminance was 0.057 of 255 code values; no large brightness jump
was detected. This does not rule out fine detail flicker at the preview sampling.

Six sampled images from the full sequence are in `renders/motion/contact.jpg`.
The foliage/water motion and clear sightline are visible in those samples. Fine
rain detail is faint at 640×360; a higher-resolution weather pass remains necessary
before judging final rain quality. There is no seamless-loop or final-photorealism
approval claim. Runtime and exact checks are retained in the motion output folder.

## Rebuild

```sh
python scripts/render_supervised.py
python scripts/setup_motion.py
python scripts/check_motion_rig.py
python scripts/render_motion.py
python scripts/check_motion_visual.py
python scripts/check_delivery.py
python scripts/check_portability.py
```

`rainforest_cabin.blend` is the still scene; `rainforest_motion.blend` contains the
animated test. Both use the supplied relative model libraries. The frame renderer
skips intact completed PNGs only when its saved blend/script signature matches.
It writes progress to `status.json` and `renders/motion/status.json`. Raw frames
remain local and are ignored by Git; the MP4, setup and check records are published.

## Next work after review

Assess motion speed and amplitude, then improve timber/roof irregularity, aged
surface detail, creek turbulence and localized splash contact. A higher-resolution
motion render and a longer loop come after that review. No audio, long-video build
or seamless-loop claim is included in this diagnostic.
