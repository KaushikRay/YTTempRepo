# Darker storm finish with a little distant thunder

[Two-minute preview](../../renders/production_test/preview.mp4)
· [Quick twelve-second preview](../../renders/audiovisual/quick_preview.mp4)
· [Brightness comparison](../../renders/production_test/brightness_comparison.jpg)
· [Darker still](../../renders/production_test/darker_still.png)
· [Soundtrack](../../renders/production_test/soundtrack.flac)
· [Audio credits](../../renders/production_test/AUDIO_CREDITS.txt)

## Requested changes

The scene is modestly darker, with no camera, geometry or motion edits. A static
33-cube LUT applies approximately −0.55 EV to shadows/midtones in linear light,
with smooth highlight protection to retain the warm cabin glow. It preserves
linear RGB proportions rather than adding a new colour cast. The comparison is
previous brightness on the left, darker finish on the right.

The measured median midtone linear-luminance ratio is 0.6725
(-0.572 EV). Warm lantern pixels retain
0.8297 of their former linear luminance.
No light flashes, lightning bolts or weather events have been added to the image.
The rain/palm timeline and the previously approved 80% river playback remain.

Thunder is Bidgee's CC BY 3.0 *Thunder* recording. It is high-passed at 35 Hz and
low-passed at 650 Hz to remove the sharp crack, with a gentle 1.5-second attack
and four-second fade at the tail. The first distant rumble starts at 00:06 and
lasts about 18.4 seconds. A second begins at 01:15 in the longer preview, slightly
slowed and 1.5 dB quieter. These are preview event timings, not a final multi-hour
schedule. **No visual lightning accompanies either sound.**

Rain stays dominant and the stream remains about eleven LUFS below it. The one-
minute/quick preview keeps the close-stream recording; the two-minute preview
uses the existing continuous CC0 flowing-water bed. No music or wildlife track
is added. Both longer soundtracks remain continuous across picture repeats.
The quick excerpt has a separate level adjustment to avoid making its early
thunder event disproportionately loud.

## Finishing pipeline and source

`assets/colour/storm_dusk.cube` is the reusable finishing LUT.
`grade_storm_scene.py` creates `renders/production_test/graded_loop.mp4` from the
native twelve-second PNG cache, or from the ungraded loop if the cache is absent.
The LUT is constant in time and changes colour values only. This is a final grade;
Blender geometry, materials, physical-light settings and simulation caches are
unchanged. The raw Blender render remains available at its original brightness.

The mixing/muxing script automatically uses the graded loop when it exists.
The two-minute picture contains ten repeats of that loop, not two minutes of
unique animation. Its sharing encode is 1080p/24 fps, CRF 18 with a 6.4 Mb/s cap.
The full-quality quick preview copies the graded loop's video packets unchanged.
The former river-speed comparison is a historical diagnostic at the pre-grade
brightness and is not a comparison of this new colour finish.

## Actual QA

All preview videos decode cleanly with correct durations and frame counts.
The two-minute result measures **-24.06 LUFS integrated /
-3.23 dBFS true peak**, with a rain/stream separation of
10.97 LUFS. SSIM against ten repetitions of the graded
high-quality loop is 0.994292.
The short preview measures -24.03 LUFS /
-8.64 dBFS true peak.

The grade's midtone reduction and warm-highlight protection passed pixel checks.
Thunder appears only inside its scheduled audio intervals. The mix remains the
sum of the existing rain/stream bed and thunder, apart from the common final
level adjustment; there was no peak limiter required. Sample peaks, audio joins,
finite samples, source licences/hashes and portable water playback checks remain
available in the QA files. Video is compared against the **graded** reference;
the earlier unchanged-surroundings pixel checks refer to the underlying render
before this intentionally global brightness change.

Numerical and spectral checks are not a human listening pass. User review should
judge whether the darkness and distant rumble feel cozy and suitably subtle.
Existing visual limits remain: generated static cabin/forest, approximate banks,
coarse/glossy water and a short artistic 3D loop transition. This is a review
preview, not a final multi-hour YouTube release.

## Attribution and rebuild

The credit file includes valvalion's CC BY rain, jackthemurray/Extemporalist's CC0
water recordings and Bidgee's CC BY thunder, with sources, licences and changes.
The thunder licence was rechecked on its Commons page. Recordings are acoustic
stand-ins, not claims of geographically authentic sound from the generated scene.

```sh
python scripts/grade_storm_scene.py
python scripts/mix_rainforest_audio.py
AUDIO_DURATION_SECONDS=120 python scripts/mix_rainforest_audio.py
python scripts/check_rainforest_audio.py
python scripts/check_production_test.py
python scripts/check_darker_thunder.py
```

Regenerate the grade after any future Blender render revision. No Blender render
is needed for this finishing step. The LUT, prepared audio sources, manifests and
scripts are committed; native frame caches and work files remain ignored.
