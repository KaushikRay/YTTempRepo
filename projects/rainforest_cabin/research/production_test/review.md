# Rain-first ambience, slower river and two-minute production test

[Two-minute 1080p test](../../renders/production_test/preview.mp4)
· [Quick full-quality review](../../renders/audiovisual/quick_preview.mp4)
· [Previous/new river speed comparison](../../renders/production_test/speed_comparison.mp4)
· [Soundtrack](../../renders/production_test/soundtrack.flac)
· [Credits](../../renders/production_test/AUDIO_CREDITS.txt)

## Requested changes

Rain now leads the stream by **10.97 LUFS**, versus the previous
five-LUFS target separation. The stream is reduced another 6 dB relative to rain.
Overall loudness stays near −24 LUFS rather than simply turning everything up.
The one-minute/quick preview retains the previous close-stream source at the new
quieter balance. The longer test uses a continuous CC0 flowing-water recording
so neither sound needs to repeat at the twelve-second visual joins.

Only the river motion is slowed. Its fresh particle-fluid bake is sampled at
30 fps and displayed at 24 fps, giving **80% water playback speed**. Rain, roof
runoff and palms keep their original 24 fps timeline. All 288 water states are
native, distinct 3D meshes; there are no repeated/interpolated video frames or
stock-footage water effects. This is river-only slow motion, not a claim that the
channel's physical discharge was reduced by 20%.

## Motion and source

The solver retains gravity 9.81 m/s² and the existing bed/rock geometry. It uses
120 warmup frames at 30 fps (four physical seconds), followed by 312 output
states. The delivered loop uses 288 states. Its first second retains the existing
artistic density/froth-field transition, remeshed before rendering, to join the
continued tail into the head. It remains an approximate loop, not periodic fluid
physics.

Mean physical particle speed is 2.2356 m/s versus
2.2366 m/s previously; after the .8 delivery
clock ratio, the apparent mean-speed ratio is **0.7996**.
The renderer resampled no earlier water images. It rendered the river border at
native 1080p pixel density and the same 32-sample Cycles cap, then combined those
pixels with the matching approved full-resolution frame. Six sampled frames
have exactly zero changed pixels outside x=720–1760, y=680–1080. Rain and palm
repeat/playback checks also passed from relocated cache archives.

Open `rainforest_looped_fluid.blend` with its twelve updated relative cache ZIPs;
run its embedded playback script once. The source is updated in place. Earlier
approved results remain available at their immutable Git commits.

## Longer audiovisual test

The two-minute test contains ten repetitions of the revised twelve-second
visual loop, **not two minutes of unique simulation**. Audio uses uninterrupted
120-second excerpts: rain original seconds 173–293 and flowing water original
seconds 103–223. The latter is Extemporalist's CC0 *Snowmelt flowing into lake at
Okanagan Mountain Provincial Park*, obtained through Wikimedia's standard Ogg
version after the original FLAC URL returned 403. These are acoustic stand-ins,
not recordings from the generated scene's location. Creator, licence, changes,
download evidence and hashes are retained in the project.

There is no added music, thunder or wildlife track. The preview fades audio in
and out; it is not itself a seamless two-minute audio loop. No release intro or
subscribe badge is added to this review test.

The longer sharing encode is 1080p/24 fps, CRF 18 with a 6.4 Mb/s maximum video
rate, to keep the file downloadable through this repository. SSIM against ten
repeats of the high-quality source loop is **0.993315**.
The quick preview retains the high-quality loop's video packets unchanged.

## Completed QA

- Exactly 2,880 video frames / 120 seconds, stereo 48 kHz audio; clean decode.
- Encoded audio: **-24.06 LUFS**, **-2.84 dBFS true peak**.
- Rain solo: -24.34 LUFS; stream solo: -35.31 LUFS.
- Audio continuity checks passed at all nine visual repeat joins.
- All 288 liquid/foam cache states passed integrity checks and portable playback.
- River repeat-point pixel change is 0.9984× the largest sampled ordinary step.
- The revised one-minute and quick previews also decode cleanly and keep the new loop's encoded picture unchanged.

## Remaining limits and next gate

The original hybrid limits remain: generated static cabin/forest, approximate
bank proxies, coarse/glossy water and a short artistic 3D surface transition.
Slowing the river does not reconstruct those elements or establish photographic
realism. Source descriptions, spectrograms and numerical audio checks were
reviewed; subjective naturalness and unwanted incidental sounds still require
user audition. Review whether this slower pace and rain dominance feel right.
After that, choose the final YouTube duration/version and prepare the long master.
This two-minute file is a production test, not a multi-hour release.

## Rebuild

```sh
FLUID_VARIANT=looped_fluid SIMULATION_FPS=30 WARMUP=120 FLUID_FRAMES=432 python scripts/simulate_fluid_river.py
python scripts/prepare_fluid_loop.py
python scripts/prepare_loop_foam.py
SAMPLES=32 python scripts/render_looped_fluid.py
python scripts/package_fluid_loop.py
python scripts/check_fluid_loop.py
python scripts/check_looped_scene.py
python scripts/mix_rainforest_audio.py
AUDIO_DURATION_SECONDS=120 python scripts/mix_rainforest_audio.py
python scripts/check_rainforest_audio.py
python scripts/check_production_test.py
```

With the preserved local approved PNG cache, `RIVER_ONLY=1` renders only the river
border. A fresh clone can rebuild full frames without that option. Prepared audio
FLACs and the screening/source manifests are sufficient for mixing. Native frame
caches, original audio downloads and work files are ignored by Git.
