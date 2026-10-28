# Revised rain-dominant sound review

[One-minute review](../../renders/audiovisual/preview.mp4)
· [Quick review](../../renders/audiovisual/quick_preview.mp4)
· [Two-minute production test](../../renders/production_test/preview.mp4)
· [Current changes and measured QA](../production_test/review.md)
· [Audio attribution](../../renders/production_test/AUDIO_CREDITS.txt)

Rain leads the stream by eleven LUFS in the mix, versus the previous five-LUFS
target gap. The stream is another 6 dB quieter relative to rain. Overall level
remains near −24 LUFS. Both reviews keep continuous rain audio across the visual
repeats. The one-minute/quick review uses jackthemurray's close stream; the longer
test uses Extemporalist's continuous CC0 flowing-water recording.

Rain is valvalion's CC BY 3.0 track. The close stream and long flowing-water source
are CC0. The supplied attribution file records creators, URLs, licences, excerpts
and processing. The Freesound original page was blocked, so the close-stream
licence evidence is its Commons record and source link. The long source uses
Wikimedia's Ogg derivative because its original FLAC download returned 403.

The level/peak, timing and audio-continuity checks are technical verification.
Source descriptions and spectrograms were inspected; no human listening pass is
claimed. Review unwanted sounds, brightness, rain dominance and stream placement.
No added thunder, music or wildlife track is used. These sources are acoustic
stand-ins, not geographically authentic rainforest location recordings.

The prepared FLACs, `assets/audio/sources.json` and screening manifest can rebuild
the mixes with `mix_rainforest_audio.py` (default 60 s; set
`AUDIO_DURATION_SECONDS=120` for the longer test). Native source downloads are
ignored. Release intro, final duration and the long master remain a later stage.
