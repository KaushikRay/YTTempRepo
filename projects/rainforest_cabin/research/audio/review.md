# Rainforest cabin — first audiovisual review

[One-minute full-quality preview](../../renders/audiovisual/preview.mp4)
· [Twelve-second quick preview](../../renders/audiovisual/quick_preview.mp4)
· [Lossless stereo soundtrack](../../renders/audiovisual/soundtrack.flac)
· [Rain solo](../../renders/audiovisual/rain_solo.flac)
· [Stream solo](../../renders/audiovisual/stream_solo.flac)
· [Copyable audio attribution](../../renders/audiovisual/AUDIO_CREDITS.txt)

## What changed

This is the sound-review stage after approval of the twelve-second visual loop.
The approved 1080p / 24 fps video is copied five times for the one-minute preview;
its encoded video packets are identical to the approved source. There is no new
Blender render, video re-encoding or claim of sixty unique seconds of visual motion.
The lighter preview contains one unchanged twelve-second visual loop.

Audio is a continuous sixty-second excerpt from each source, not a twelve-second
sound loop. There are no audio cuts at the picture repeats (12, 24, 36 and 48 s).
Rain is dominant. The quieter stream is narrowed and placed slightly right of
centre, matching its location in front of the porch. Gentle high-pass filtering
reduces rumble, low-pass filtering restrains brightness, and light dynamic control
reduces short broadband/midrange spikes while retaining water detail. There is
no music, synthetic rain noise, added wildlife or added thunder track. No separate
roof-drip foley has been manufactured; the rainfall track carries the close texture.

The preview fades audio in over 0.75 s and out over 1.5 s. This minute is not a
seamless audio loop. Release titles, subscribe badges and a full release intro
are intentionally deferred until the audiovisual direction is reviewed.

## Sources and selection

- Rain: valvalion, "Falling Rain SFX 1 2016-11-19", CC BY 3.0. A 180-second
  preparation excerpt starts at original second 120; the mix uses its seconds
  53–113, corresponding to original seconds 173–233. The source is a licensed
  rain SFX track. Its metadata does not establish microphone or capture-location
  provenance, so it is not presented as a verified recording from this rainforest.
- Stream: jackthemurray, Freesound 433589, CC0, described as soft flowing stream
  water. The mix uses original seconds 6–66. Original length is about 69 seconds.
- Rejected: James River Rapids 1, CC0. Its decoded candidate has hot peaks above
  full scale; its broad-rapids description is also less suited to a small brook.
  No rapids candidate audio appears in the final mix. Vorbis overshoot alone does
  not establish that audible distortion exists in the source.

Full Commons metadata, licence fields, page wikitext, source URLs and SHA256
checksums are retained. The original Freesound page was requested but blocked
by the network proxy; the Wikimedia file page links that original and explicitly
carries CC0. The CC BY rain attribution must accompany public distribution.
The ready-to-copy credit file includes creator, title, source, licence and changes.
These recordings are selected for acoustic fit, not as geographically authentic
location sound for the generated rainforest backdrop.

## Actual checks and their limits

All files are stereo 48 kHz. The full video decodes cleanly with 1,440 frames
(60 seconds), and the quick preview has 288 frames (12 seconds). Video packet
hashes prove both retain the approved picture without dropped/re-encoded frames.

The encoded one-minute audio measures **−24.07 LUFS integrated** and
**−2.98 dBFS true peak**. The lossless master measures −24.0 LUFS / −2.96 dBFS
true peak with 1.3 LU loudness range. It needed no peak limiter. The quick preview
measures −24.1 LUFS / −8.02 dBFS true peak. Source excerpt hashes, finite samples,
sample count, technical dropouts, mono fold-down and continuity at visual-repeat
boundaries passed. See [machine-readable QA](../../renders/audiovisual/qa.json).

Source descriptions, waveform-derived levels and spectrograms were inspected.
These checks do not certify the absence of voices, distant birds, vehicles or
baked-in thunder. No human listening pass was performed here. **User audition is
the next quality gate**: listen for intrusive content, harsh hiss, excessive stream
presence, unnatural stereo placement and whether the rain feels sheltered/cozy.

The image retains its existing limits: generated static cabin/forest, approximate
bank proxies, coarse/glossy simulated water and a short artistic 3D surface loop
transition. Sound has not corrected those visual limits. This is a review preview,
not the final long-form YouTube release.

## Rebuild

The committed prepared source FLACs are sufficient to rebuild the delivered mix:

```sh
python scripts/mix_rainforest_audio.py
python scripts/check_rainforest_audio.py
```

Dependencies: ffmpeg/ffprobe, NumPy and SciPy. Prepared FLACs preserve the decoded
source excerpts losslessly; they do not restore information lost in the original
Vorbis encoding. Download URLs and original hashes are in `assets/audio/sources.json`.
Original downloads and intermediate measurement files are ignored by Git.
`prepare_ambience_audio.py` can rebuild the preparation excerpts from the originals.

## Next step

Review the rain/stream balance and any unwanted source sounds. After that, settle
the final duration/version, source more long-form variation where needed, and build
an audiovisual endurance test before multi-hour encoding. The short stream source
is suitable for this audition; it should not be stretched into hours unchanged.
