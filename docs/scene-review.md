# Reference and first-pass review

Reference: recovered original screenshot from commit 51e4ad4.

## Visual target

Low seated viewpoint into a tall Gothic lounge. Brown sofa at left foreground,
large oak table close to camera, paired tall leaded lancets and oculus at rear,
large hearth on right. Reference lighting is dark, with warm practical pools
and a cool blue window. Roughly dressed stone, irregular flags, distressed
leather, piled cloth, books, tableware, rugs and climbing foliage provide detail.
The screenshot alone does not establish the original animation or exterior layout.

## First-pass findings and corrections

The first camera showed the sofa back; moved inside the seating area to show
its cushions. Area lights produced bright visible bands through the glazing;
excluded their shapes from camera, glossy and transmission visibility while
retaining their illumination. Added a ceiling, closed the arch spandrels,
removed the nearest distracting sconces and reduced illumination.

## Remaining gaps

This is a blockout, not a photoreal match. Major work remains on irregular
masonry, deeper carved Gothic surrounds, full chimney stonework, furnishings
and fabric folds, realistic leaf assets, fireplace flame shading and smoke,
credible wax and prop detail, and more accurate foreground table scale.
The reference has richer shadow detail, more architectural ornament, and
much denser dressing. Exterior village is an added interpretation requested
by the user; its visibility must be checked again after glazing and storm work.

Animation is provisional and has not been rendered or seam-tested. Rain is
static in this version. No glass runoff or lightning animation yet. The current
144-frame timeline is a development test range, not a finished seamless loop.

## Next visual gates

1. Refine camera and architecture against the screenshot.
2. Replace prominent placeholders with licensed high-detail materials/assets;
   verify source licence and store attribution before use. External asset hosts
   were blocked by the current network policy in the initial research attempt.
3. Render a stronger still for user review before expensive animation.
4. Produce a short moving test: layered rain, rivulets, tree motion, coherent
   firelight/candle variation and one lightning event. Audio deferred.

## Second visual pass

Implemented staggered individual stone courses, nested arch mouldings,
chimney breast blocks and carved jamb courses, rear door recess, directional
wood texture, softer leather micro-bump, a continuous draped blanket,
individual interior leaf surfaces, flame ribbons and a fireplace grate.
Moved the foreground table/props closer and adjusted the camera.
Rendering at 1280 × 720 / 192 Cycles samples with indirect clamping.
Visual acceptance remains pending the render; these additions are procedural
studies and do not establish reference-level realism.

Second-pass render completed successfully: 1280 × 720, 192 samples,
4 min 24 sec rendering time. Direct visual inspection: improved stone courses,
readable thin flame shapes, finer foliage, and stronger foreground table.
Still substantially short of the target: masonry and furnishings too regular,
room underdressed, glass/exterior too dark, thin artificial flames, insufficient
aged surface detail and architectural ornament. Rain is not convincingly
readable. No animation readiness claim. Blender exited after the still render.

## Third pass — surface and storm visibility

Added world-space fine stone bump, small stone vertex irregularities,
continuous creased upholstery meshes, woven rug pattern, ceiling beams,
open pottery, a jug, page blocks, linen, wax drips and climbing ivy.
Changed glass to restrained reflection with mostly transparent transmission;
added a dim cloud backdrop, lit exterior, elevated village and distant ridges.
Rain now has provisional linear keyframes, with extra fine streaks.

A 640 × 360 / 48-sample diagnostic completed. It exposed an exterior ground
plane intersecting the interior; moved its near edge beyond the back wall.
Larger review still is 1280 × 720 / 160 samples. Still-image review is the
next gate; no long animation or audio work has begun.

Third-pass larger still completed successfully: 1280 × 720 / 160 samples,
5 min 8 sec. Visual inspection confirms the exterior ground intersection is
removed and distant village lights/roofs are now readable. Upholstery,
tableware and ivy added. Remaining gaps: stone still too orderly, furnishings
too sparse, flame rendering stylized, rain insufficiently visible, exterior
sky too uniform for a heavy thunderstorm. No animation approved or rendered.
Framing review is the next user-facing checkpoint; the full look is not ready.

## Fire/candle review iteration

Rebuilt candles with melted profiles, subsurface wax, dark wicks, thin drips,
small warm volumetric flames and tiny blue bases. Added a 960 × 720 close-up.
Removed the flat hearth ribbons. Fluid baking failed across the installed and
isolated runtimes; see fire-assets-and-validation.md. Final fallback uses
irregular tapered three-dimensional emitting volumes, not fluid simulation.
Added stone relief and mineral variation. Denoised room render completed at
1280 × 720 / 80 samples in 3 min 4 sec; candle view completed at 960 × 720 /
96 samples in 2 min 36 sec. Both were inspected. Rejected earlier overexposed
and box-shaped volume tests. Current hearth silhouette remains stylized and
less complex than photographed fire. Candle/prop geometry also needs further
art direction. Animation has not been rendered or loop-validated.

## Rustic tavern revision

Compared masonry and dressing again against reference. Rebuilt wall courses
with uneven block sizes, chamfered corners, nonplanar faces and shallower
mortar; corrected inward-facing sidewall geometry. Replaced leather lounge
seating with oak benches, casks, firewood, trestle furniture and cookware.
Near-window rain and rivulets are now visible in the full-room still.
All rejected procedural hearth gas envelopes removed. Real-fire download and
integration remain blocked by environment network access; draft additions
saved, user review/save/publish required. Current fire is logs/embers only.
The room remains less richly dressed and less photoreal than the reference.

## Downloaded fire asset still

Retrieved 1920 × 1080 CC BY 3.0 fireplace footage from Wikimedia Commons;
BlenderKit/JangaFX hosts remained unavailable during lookup. Retained original
clip, raw source metadata, licence, attribution and checksum under assets/fire.
Selected frame at 2 sec; temporal median matte removes stationary source wall.
Packed the keyed still and credits into the Blender file. Rejected earlier
colour-key render with red background speckles. Final room and hearth close-up
completed and inspected. Low-brightness wisps are partly trimmed; the integration
remains a review composite. Original movie retained, but animation is not yet
integrated or loop-tested. No native VDB/3D simulation is used for these flames.

## Three-second motion study

Prepared 72 keyed fire images at 1280 × 720 / 24 fps from licensed source
seconds 2–5. Linked as a relative-path image sequence, with source brightness
driving the hearth light. Added independent rain wrapping, sliding droplets,
candle tilt/flicker and root-based exterior tree sway. Runtime checks passed
for changing driver evaluations and distinct fire source images.

Rendered 36 frames at 640 × 360 / 12 Cycles samples, sampled from the 24 fps
scene at every other frame. Render loop completed in 313 seconds. Full-room
MP4 plus magnified fire/window crops are each 3 seconds / 36 frames / 12 fps,
with no audio. Decode/frame-count checks passed and fire/window regions change.
Sampled frames inspected; full user playback review is pending. Not a seamless
loop or final photoreal animation. Blender's Python worker stalled after
render completion during cleanup; it was terminated after output validation.

## Smoother quality preview

Preserved approved camera and motion. Rendered all 72 timeline frames at true
24 fps, 960 × 540, adaptive sampling up to 24 with OIDN and persistent data.
Render loop finished in 28 min 5 sec. Worker cleanup stalled afterward and was
terminated by the supervisor, with -15 recorded. Full-room, fire crop and
window crop MP4s passed complete decoding and 3 sec / 72-frame / 24 fps checks.
Sampled first/mid/end frames inspected. No frame interpolation, no audio,
no long video and no seamless-loop claim. Source art and fire matte limitations
remain; this is a rendering quality pass. Playback review is the next gate.

## Lightning and audio preview

Six-second 24 fps / 960 × 540 review: two exterior lightning pulses illuminate
the room through its windows; main flash at 1.75 s, thunder mixed from 3.0 s.
Extended real fire footage continuously to source seconds 2–8. Preserved all
first-72 fire files and verified the prior quality input fingerprint before
reusing 64 physically unchanged frames; rendered 80 new frames at the same
quality in 32 min 55 sec. Supervisor recorded/stopped the known cleanup stall.

Window rain (public domain), thunder (CC BY 3.0) and fire-source audio (CC BY
3.0) are excerpted, filtered, level-adjusted and mixed with credits retained.
Final encoded audio measures -24.03 LUFS and -10.94 dBTP. Video/audio decode,
duration, frame count, and visible flash increase checks pass. Source audio
spectrum/signals inspected; human listening review is pending. No music is
added. This is not a seamless loop, final master or published long video.
