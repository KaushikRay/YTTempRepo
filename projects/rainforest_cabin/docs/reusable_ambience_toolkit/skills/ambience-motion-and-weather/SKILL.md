---
name: ambience-motion-and-weather
description: Create continuous believable weather, foliage, water, fire and optional events with tested loop continuity.
---

# Ambience Motion and Weather

## Inputs

Approved still, camera, scene scale, required effects, excluded effects, loop
length/FPS, solver/render capabilities and motion review criteria.

## Workflow

1. Build coherent near/mid/far rain with wind, motion blur, continuous replenishment
   and shelter occlusion. Warm up particles and test early/middle/late frames.
2. Match roof runoff, pane trails, splashes and contact to geometry. Keep exterior
   weather outside. Animate plants by exposure and branch/leaf response; sheltered
   indoor plants should not sway violently without a cause.
3. Choose water representation explicitly. A requested fluid simulation needs
   actual geometry/contact dynamics or an agreed alternative, not disguised UV
   distortion. Verify velocity scale, bank contact, foam/spray and reflections.
4. If fire/candles are requested, use convincing licensed elements, volumes or
   simulations with fuel/wick contact, embers, smoke and illumination. Reject
   cloth-like sheets and oversized identical teardrops.
5. Implement only requested events. Sound-only thunder needs no added flashes.
   Linked lightning must affect scene lighting/reflections and have a plausible
   delayed thunder event. No invented wildlife/people.
6. Make motion periodic where required: no duplicate endpoint, no visible recycle,
   compatible phase and preferably velocity. Seeds are not proof of periodicity.
   Document approximate fluid blends and compositing limits.
7. Benchmark representative frames and caches. Deliver a short test, close-up
   details and multiple repeated loops. Watch normal-speed motion and compare
   local seams with ordinary adjacent-frame changes.

## Outputs and acceptance

Real motion clips, cache/solver provenance, timing/event manifest, loop QA and
known limitations. Do not start the long master while major motion defects remain.


See [the master playbook](../../AMBIENCE_VIDEO_MASTER_PLAYBOOK.md) for the complete workflow. Current user instructions and governing tool/system rules take precedence over these defaults.
