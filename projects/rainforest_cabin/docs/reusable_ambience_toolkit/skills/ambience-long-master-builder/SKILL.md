---
name: ambience-long-master-builder
description: Assemble exact-duration long ambience versions from verified visual units and sound with resumable stages and technical QA.
---

# Ambience Long Master Builder

## Inputs

Approved short/mixed previews, version matrix, visual units, source sound,
event manifest, opening/ending choices, output settings and free disk budget.

## Workflow

1. Define total T, visible scene S, and dark duration T−S for each version.
   Plan in integer frames/samples; handle partial units deliberately. Dark-from-
   start must not unexpectedly show a scenic intro or subscribe badge.
2. Verify all concat units' codec headers/extradata, dimensions, FPS/time base,
   SAR, pixel format, GOP, profile/level and color tags. Identical flags alone
   are not proof. Re-encode coherently when stream copy is unsafe.
3. Build the agreed opening, optional calm badge, events, closing and black units.
   Fade picture before S while audio continues to T where applicable.
4. Build an endurance test exercising repeats, events, fades, dark transition
   and ending. Label accelerated test timing and review cuts explicitly.
5. Assemble masters efficiently from approved units and bounded-memory audio.
   Reuse only stages with matching input/config checks and completion reports.
   Preserve unfinished `.partial` state safely; do not call it complete.
6. Probe exact timing/frame counts, decode relevant joins, inspect critical frames,
   scan all encoded audio with video disabled, and stream whole-file hashes.
7. Record sampled versus exhaustive video/audio/listening coverage. Estimate time
   and disk from actual benchmarks, bitrates, caches and temporary copies.

## Outputs and acceptance

Actual version masters, event CSVs, unit/config manifests, QA reports, hashes,
progress logs and resume notes. No upload/publication is implied by a completed
build. Do not claim hours of unique animation for repeated visual units.


See [the master playbook](references/AMBIENCE_VIDEO_MASTER_PLAYBOOK.md) for the complete workflow. Current user instructions and governing tool/system rules take precedence over these defaults.
