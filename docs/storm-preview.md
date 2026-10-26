# Lightning and audio review preview

Target: six seconds, true 24 fps / 144 frames, 960 × 540, matching the approved
quality preview's Cycles settings (adaptive maximum 24, minimum 8, threshold
0.05, OIDN, five CPU threads). This is a review clip, not a seamless loop.

## Lightning

A cold area light outside the windows, an animated cloud-bank emission level,
and a branched distant channel create two short pulses. The main pulse is at
frame 43 (1.75 seconds); thunder begins mixing at 3.0 seconds, a nominal 1.25 s
delay. The bolt can be partly obscured by trees and window leadwork. Exposure
must retain detail in the illuminated room, rather than turning the whole
frame white. A small test render was checked before the full-quality pass.

## Motion and reuse

The fire sequence is extended to source seconds 2–8, without changing approved
frames 1–72. The fire light is extended while retaining original integer-frame
values. Rain, candles, tree drivers, camera and art remain unchanged.

The previous quality preview's input fingerprint is verified against the
preserved baseline scene, renderer and original 72 fire images. Only baseline
frames with the added light at zero, the channel hidden and the sky exactly at
its baseline value are reused. This permits 64 reused frames and 80 newly
rendered frames, instead of rerendering all 144. Reuse and render indices are
recorded in renders/storm_setup.json. New inputs are hashed for resume safety.

## Audio draft

Sources are retained with raw Commons licence metadata and checksums:

- Public-domain `Rain against the window.ogg`, by cori, source seconds 10–16.
- CC BY 3.0 `Thunder.ogg`, by Bidgee; a strong event is selected and delayed.
- Audio from the existing CC BY 3.0 fire footage, source seconds 2–8, matching
  the fire imagery's source interval. No music is added.

The rain is filtered to suggest listening from inside; crackle is placed toward
the hearth side, with a small room response. Thunder is low-pass filtered and
faded into/out of the short clip. The mix has short opening/closing fades.
Source descriptions, waveform/spectrum and levels are checked; these do not
replace human listening. The draft mix is near -24 LUFS and comfortably below
a -2 dBTP ceiling. Actual final AAC values are measured in av_qa.json.

The initial rain trim was nine milliseconds short because of compressed-audio
seeking/timestamps. Full decoding followed by exact sample-index selection
fixes the trim; no invented data is used to fill a missing recording segment.

Attribution and modification statements are in assets/audio/CREDITS.txt and
assets/fire/CREDITS.txt. They must accompany a published video as required by
the CC BY assets. The source metadata, not only a filename, establishes the
licence choice. No NC assets are used.

## Reproduce this revision

The setup starts from the approved 72-frame scene, and is not run twice on
an already-extended scene. A baseline backup is under /workspace/scratch/storm-baseline.

```sh
/workspace/tools/fire-venv/bin/python scripts/extend_fire_storm.py
blender -b -t 5 --python scripts/setup_storm.py
OMP_NUM_THREADS=5 /workspace/tools/fire-venv/bin/python scripts/run_storm_preview.py
/workspace/tools/fire-venv/bin/python scripts/mix_storm_audio.py
LOUNGE_REVIEW_DIR=storm_preview /workspace/tools/fire-venv/bin/python scripts/encode_motion.py
/workspace/tools/fire-venv/bin/python scripts/finish_storm.py
```

A known bpy cleanup stall is supervised and recorded after frame completion;
this is not represented as a clean worker exit. Video/audio streams are decoded
and checked independently. The final review files have `_with_audio.mp4` names;
the intermediate silent clips are retained for comparison. Fire/window crops
are magnified from the room view, not separate high-resolution camera renders.

The original scene's art and fire matte limitations remain. No full-length
video, final soundtrack master, loop-seam validation or publication is claimed.

## Completed validation

Eighty new frames completed in 1974.6 seconds (32 min 55 sec); 64 verified
unchanged quality frames were reused. The known bpy cleanup stall recurred
after frame completion, and the supervisor recorded worker return code -15.
No clean renderer process exit is claimed.

All final MP4s contain 144 video frames at 24 fps, six seconds duration, and
48 kHz stereo AAC. Complete decoding passed. The full-room view is 960 × 540.
Measured encoded audio: -24.03 LUFS integrated, -10.94 dBTP. Main-flash sampled
region luma rises from 22.19 to 50.05 and returns to 22.67 afterward. Nominal
thunder delay is 1.25 seconds. Source/spectrum and automated signal checks are
complete; human playback and listening review remain pending.
