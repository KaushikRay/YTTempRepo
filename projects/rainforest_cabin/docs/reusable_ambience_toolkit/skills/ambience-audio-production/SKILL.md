---
name: ambience-audio-production
description: Vet licensed recordings and build natural scene-matched ambience soundtracks with bounded-memory long mixing and truthful QA.
---

# Ambience Audio Production

## Inputs

Listener position, dominant/supporting sounds, event preferences, source files
and license evidence, approved motion, versions and intended loudness character.

## Workflow

1. Verify actual source rights, authors, titles, URLs and edits. Prefer long clean
   natural recordings where appropriate. Record used sources per final version;
   do not carry rejected/preview-only assets into final attribution.
2. Screen waveform, peaks, RMS and spectrograms. Flag handling noise, speech,
   wrong-time wildlife and embedded events; audition available passages. Numerical
   screening is not proof of absence of voices or a complete listening pass.
3. Match acoustic perspective: enclosed glass versus open porch, surface-specific
   rain, nearby runoff versus distant stream, appropriate stereo width/pan.
4. Filter and control gently. Keep the chosen dominant bed first. Suggested sleep
   targets such as −24 LUFS integrated/−2 dBTP are audition starting points, not
   platform requirements. Distinguish sample peak from encoded true peak.
5. Build long beds from diverse source spans and appropriate overlapping grains.
   Check correlated-crossfade gain. Store seeds and grain/event schedules. Timing/
   pitch variants of one recording are not independent new source recordings.
6. Stream float32 blocks or use memory maps. Avoid multi-hour in-memory arrays.
   Keep picture-to-dark and final audio fades independent. Measure the encoded
   soundtrack, including loudest events and grain transitions.
7. Deliver a mixed preview plus solo stems/clips, complete credits, measurements
   and listening coverage. Get the agreed balance review before long assembly.

## Outputs and acceptance

Source register, actual stems/mix, source-change credits, event CSV, loudness and
peak reports, reusable parameters and honest listening limitations.


See [the master playbook](../../AMBIENCE_VIDEO_MASTER_PLAYBOOK.md) for the complete workflow. Current user instructions and governing tool/system rules take precedence over these defaults.
