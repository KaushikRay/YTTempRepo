# Production and release QA checklist

## Inputs and scene

- [ ] Brief, versions, exclusions and visual method are recorded.
- [ ] Reference board includes real-world evidence and a concrete gap list.
- [ ] Used assets have source/license/change records and redistribution checks.
- [ ] Camera scale, support/contact, plants, PBR, glass and lighting were reviewed.
- [ ] Still/crops and short motion are actually accessible and reviewed as required.

## Motion

- [ ] Rain replenishes at early/middle/late times and respects shelter.
- [ ] Wind and foliage agree with scale/exposure.
- [ ] Water/fire/contact match the requested method and are named accurately.
- [ ] Loop frame count has no duplicate endpoint; local joins watched repeatedly.
- [ ] Optional events are in scope and their times are recorded.

## Sound

- [ ] Dominant/support balance matches the approved preview.
- [ ] Actual source spans, edits, licenses and credits are recorded per version.
- [ ] No unsupported claim of exhaustive listening or semantic absence.
- [ ] Grain transitions, events, start/end and dark-transition continuity checked.
- [ ] Full encoded audio loudness and true peak measured, with video disabled.

## Long masters

- [ ] Exact version duration, scene duration, frame count, resolution and FPS.
- [ ] Unit headers/SAR/color/GOP compatibility verified before stream concat.
- [ ] Intro/badge/fades/black transitions and ending checked.
- [ ] Video decode coverage is accurately labeled sampled/full.
- [ ] Whole-file hash uses bounded streaming I/O.
- [ ] QA report, source/config hash, logs and safe-resume notes exist.

## Thumbnails and metadata

- [ ] Three actual images per requested version, not only directions.
- [ ] Every duration/dark-screen label is correct; text read at 320px width.
- [ ] No absent subjects/flashes, false location/footage or ad-free claims.
- [ ] Image dimensions, bytes, hashes, comparison, ZIP and links checked.
- [ ] Three title options and full description/credits per version are complete.
- [ ] Metadata lengths, actual chapters, cross-links and disclosure checked.
- [ ] Studio fields and publication facts are explicit, not assumed.

## Delivery / publication

- [ ] User has a working route to full outputs or an explicit remaining blocker.
- [ ] Exact transfer, parts, timeline rebuild and source render are distinguished.
- [ ] Local kit extraction/smoke test and platform coverage stated honestly.
- [ ] Private upload/processing/checks reviewed before authorized release.
- [ ] Public publication/schedule happens only when authorized.
- [ ] Handoff lists actual output links, state, limitations and next action.
