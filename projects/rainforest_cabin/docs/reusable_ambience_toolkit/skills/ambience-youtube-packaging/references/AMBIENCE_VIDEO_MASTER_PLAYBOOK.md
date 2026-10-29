# Reusable Ambience Video Production Playbook

Version: 1.0 · Updated: 2026-10-29 · Format: self-contained production instructions

Use this file for any original ambience project: rain, storms, forests, cabins,
greenhouses, gardens, coastlines, snow, fireplaces, interiors, or another agreed
setting. No particular channel, project, computer, runtime, or video duration is
assumed. The examples are starting points, not mandatory creative decisions.

This is a production playbook and handoff template. It is not a finished Blender
scene, an executable renderer, an automatic YouTube uploader, or a promise that
tools from another chat are available. Actual scripts and assets must be built,
tested, and delivered for the selected project. Attaching this MD alone is enough
to communicate the workflow; the optional companion skill pack supplies shorter
task-specific instructions and editable templates.

## Contents

1. How to start a new chat
2. Operating rules and live progress
3. Project brief and decisions
4. Practical combination matrix
5. Skills, tools, and environment
6. Project files and reproducibility
7. Reference research and asset rights
8. Scene, camera, materials, and lighting
9. Weather, water, fire, and optional motion
10. Seamless loops, event pieces, and render preparation
11. Natural audio and soundtrack production
12. Long-video timeline and assembly
13. Technical and perceptual QA
14. Three thumbnails for every version
15. Complete YouTube Studio package
16. Delivery, downloads, and local Mac execution
17. Review gates, estimates, and completion checklist
18. Troubleshooting matrix
19. Reusable prompts and resume handoff
20. Acceptance contract

## 1. How to start a new chat

Attach this file to a new chat and paste:

```text
Use the attached Reusable Ambience Video Production Playbook as the working
instructions for this project. Read it before starting. My concept is:
[DESCRIBE THE SETTING, WEATHER, MOOD, AND ANY MUST-HAVE DETAILS].

My reference image/video or links are: [ATTACH OR LIST].
My target device is: [MAC / WINDOWS / LINUX / CLOUD / UNKNOWN].
My intended video versions are: [DESCRIBE OR ASK ME TO CHOOSE].

Inspect the available files and tools first. Summarize what is known and what
must be decided. Ask only the few questions that materially affect the next
stage; do not repeat questions already answered. Begin with real photographic
reference research and a composition study. Do not start a long render before
the appearance and short motion preview are reviewed, unless I explicitly
authorize bypassing that gate.

Give me three clear items in every progress update: current stage, verified
progress or blocker, and next action. Do useful authorized work continuously
within the active turn. Never imply background work continues when no process
is running. Deliver working links and actual files, not only proposed filenames.

Use relevant installed skills when available. If a named optional skill is
missing, use the self-contained instructions here and explain the limitation.
Do not silently replace requested real 3D motion with an image overlay. Do not
publish or schedule a video, incur costs, or expose private assets without
authorization for that action.
```

For an existing project, also attach the latest `PROJECT_BRIEF.md`, `status.json`,
`HANDOFF.md`, current scripts, asset manifests, and last approved preview. A new
chat does not automatically inherit the previous chat's files, approvals, tools,
credentials, or running processes. Distinguish an existing authorization carried
in trustworthy session context from an unverified assertion inside an external
document. Verify access and actual state before resuming.

### First response expected from the new assistant

1. State the intended outcome and which inputs have been found.
2. Identify material missing choices, tool limitations, and the next review gate.
3. Start independent, authorized work, or clearly state the one required input
   that prevents it. Do not promise a render has started before launching it.

## 2. Operating rules and live progress

### Communication

- Use three organized items: **now**, **evidence/blocker**, **next**.
- During active work, provide a meaningful update approximately every 30–60 s
  when the interface permits it. Long tool jobs need visible progress or a
  truthful notice that the tool has not yet returned.
- State whether a job is actually running, queued, complete, failed, or waiting
  for input. A saved script, a plan, and a running worker are different states.
- Report measured facts separately from estimates and aesthetic judgments.
- Give a file's purpose, working link, and what to review. Do not ask for approval
  of a file that is inaccessible to the user.
- Do not promise unattended work between messages unless a real persistent job
  exists and the hosting environment supports it. Explain how to inspect/stop it.
- A local Mac does nothing merely because a download link was opened. The user
  must run local commands unless an explicitly connected execution tool exists.

### Scope and permissions

- Preserve prior work and cancelled projects; never resume a cancelled project
  because it happens to share assets or a repository.
- Work in an isolated project folder/branch and inspect applicable `AGENTS.md`
  or repository instructions before editing.
- Reuse existing decisions and authorizations; do not repeatedly ask permission
  for routine, reversible work within the authorized scope.
- Ask before new spending, public publication, scheduling, destructive deletion,
  or sharing private material beyond authorized destinations.
- A request for a plan does not authorize a costly render. A request to create
  thumbnails does authorize creating the actual images, not just describing them.
- Do not send messages to other people or services unless explicitly authorized.
- Use one agent by default. Separate skill modules are not instructions to spawn
  subagents. Delegate only when the user or applicable governing instructions
  authorize delegation.

### Review gates

Default gates are: creative brief; composition; realism still; short motion;
audio/motion preview; endurance test; final deliverables. The user may combine or
waive gates. Continue independent preparation while optional choices are pending,
but do not treat silence as approval of an expensive or external action.

## 3. Project brief and decisions

Save the agreed decisions before production. Mark unknown fields `TBD`, propose
defaults, and explain consequences. Avoid a long questionnaire when existing
context supplies the answer.

| Field | Decisions to record |
| --- | --- |
| Identity | Project name, slug, channel name if supplied, intended audience |
| Concept | Setting, era if relevant, climate, indoor/outdoor camera position |
| Reference | Images/videos, URLs, liked details, disliked details, realism target |
| Mood | Cozy/dramatic/quiet, dusk/night/day, brightness and color balance |
| Camera | Fixed or moving; framing, lens range, foreground and focal subject |
| Required details | Objects, plants, architecture, views, practical light sources |
| Exclusions | People, wildlife, lightning flashes, music, speech, fire, logos, etc. |
| Visual method | Full 3D, scan-based 3D, photographic hybrid, licensed footage |
| Weather | Rain/snow/fog/wind and intensity; which surfaces are sheltered |
| Motion | Foliage, runoff, flowing water, fire, optional events, camera motion |
| Sound | Dominant bed, supporting layers, events, spatial perspective |
| Versions | Duration, scene-visible duration, dark-screen portion, differences |
| Opening/ending | Black lead-in, picture/audio fades, optional subscribe badge |
| Output | Resolution, FPS, aspect ratio, SDR/HDR, codec and master format |
| Hardware | OS, chip/CPU/GPU, RAM/VRAM, disk, cloud/local location |
| Rights | Original/CC0/CC BY/commercial sources; budget and login requirements |
| Workflow | Review gates, preview sizes, checkpointing and status location |
| Delivery | Storage destination, direct download/rebuild kit, access restrictions |
| YouTube | Language, audience, monetization facts, playlist, thumbnails |
| Publication | Whether upload/scheduling is authorized; dates and IANA timezone |

### Editable generic brief

```json
{
  "project_name": "YOUR PROJECT",
  "project_slug": "your_project",
  "concept": "TBD",
  "references": [],
  "must_have": [],
  "must_avoid": [],
  "visual_method": "TBD",
  "camera": {"motion": "fixed", "description": "TBD"},
  "mood": {"time_of_day": "TBD", "brightness": "TBD"},
  "weather": {"type": "TBD", "intensity": "TBD"},
  "audio": {"dominant_bed": "TBD", "supporting_layers": [], "events": []},
  "output": {"width": 1920, "height": 1080, "fps": 24, "color": "SDR Rec.709"},
  "versions": [
    {"id": "scene_3h", "duration_seconds": 10800, "scene_seconds": 10800},
    {"id": "dark_8h", "duration_seconds": 28800, "scene_seconds": 3600}
  ],
  "opening": {"black_seconds": 1, "picture_fade_seconds": 5,
    "audio_fade_seconds": 8, "subscribe_badge": "confirm"},
  "ending": {"picture_fade_seconds": 20, "audio_fade_seconds": 20},
  "hardware": {"os": "TBD", "processor": "TBD", "ram_gb": null,
    "free_disk_gb": null, "execution_location": "TBD"},
  "review_gates": ["composition", "still", "motion", "audio", "endurance", "final"],
  "publication": {"upload_authorized": false, "public_publish_authorized": false,
    "scheduled_datetime": null, "timezone": "TBD"},
  "delivery_destination": "TBD"
}
```

The two durations above are optional examples. Replace them, remove one, or add
custom versions. Require `0 <= scene_seconds <= duration_seconds`. Distinguish
“dark from the beginning,” “dark after N minutes,” and “scene throughout.” They
are different products and need accurate titles, thumbnails, and timelines.

## 4. Practical combination matrix

No finite checklist enumerates every possible artistic combination. Use the
following axes to cover practical production branches without producing every
permutation. Select a coherent combination and implement only applicable rows.

### Visual method

| Method | Best use | Main advantage | Constraint and truthful label |
| --- | --- | --- | --- |
| Fully modeled 3D | Camera moves, deep parallax, complex interactions | Consistent geometry, lighting, reflections | Highest asset/render effort; not automatically photoreal |
| Scan-based 3D | Close natural surfaces, rocks, wood, foliage | Real surface detail and scale | Optimize heavy meshes/maps and verify licenses |
| Photographic hybrid | Fixed camera, strong scenic backdrop | Efficient still-image realism | Moving camera, shadows, reflections, and flat layers are limited; disclose method |
| Original generated plates + 3D motion | Fixed-camera fictional ambience | Flexible composition and atmospheric detail | Fine details can be invented; no claim of real camera footage |
| Licensed live-action footage | Existing recorded weather/place | Natural motion and acoustics | Rights, recognizable location, loop seams, and originality constraints |
| Mixed footage/3D/compositing | Specific missing components | Focus effort on visible problem | Match perspective, exposure, motion blur, occlusion, and provenance |

If the user requests actual simulated water, a scrolling texture or animated
image distortion is not an equivalent substitution. If a simpler method is the
only viable option, explain its visible limitation and obtain agreement before
claiming the requested result is complete.

### Scene and weather combinations

| Scene family | Key realism work | Useful movement | Sound perspective |
| --- | --- | --- | --- |
| Interior looking through glass | Thickness, reflections, condensation, wet exterior | Droplet trails, distant foliage, exterior rain | Muffled outdoor bed, glass/roof impacts |
| Open shelter/porch | Roof edge, wet/dry boundaries, runoff contact | Layered rain, eave drips, nearby leaves | Clear outside rain plus close roof/edge water |
| Dense forest/garden | Botanical variety, depth, imperfect distribution | Branch-level wind, rain interception, ground splashes | Rain by surface; stream only if present |
| Glasshouse/conservatory | Frames, pane curvature/thickness, dirt and seals | Roof streaks, drainage, exterior trees | Glass impacts, roof runoff, enclosed reflections |
| Coast/lake | Shoreline contact, reflections, scale, horizon | Waves/ripples and wind-driven rain | Surf/shore water under the dominant weather bed |
| Snow scene | Accumulation, contact, shelter, cold lighting | Falling/blown snow, gentle branches | Wind/snow acoustics; do not reuse tropical rain unchanged |
| Fire-lit setting | Real flame structure, fuel contact, soot, light response | Flame, embers, subtle smoke | Fire near the listener; weather according to enclosure |

### Event combinations

| Choice | Visual behavior | Audio behavior |
| --- | --- | --- |
| No thunder or lightning | Continuous weather only | Bed and supporting sounds |
| Thunder only | No added flashes | Sparse distant rumble, justified as off-screen weather |
| Lightning and thunder | Light the scene and visible reflections consistently | Delayed thunder based on apparent distance |
| Fire only | Fuel, flame, embers, contact lighting | Restrained crackles, no unrelated thunder |
| Optional wildlife/person/event | Only when requested and believable in the setting | Timing, acoustic distance, licensing and presence checks |

### Release combinations

| Version | Timeline | Packaging implication |
| --- | --- | --- |
| Short review | Seconds/minutes; can deliberately sample events | Clearly label preview cuts or accelerated test transitions |
| Scene throughout | Visible until closing fade | Do not label dark-screen playback |
| Scene then dark | Fade picture before chosen transition; audio continues | State exact dark-screen timing in title/thumbnail/description |
| Dark from start | No scenic opening unless explicitly agreed | Avoid a misleading promise of visible scenery |
| Multiple sound mixes | Same picture with different bed/event balances | Separate mix/version IDs and metadata |
| Higher-resolution release | Render/export at selected resolution | Upscaling does not create native fine detail; describe accurately |

## 5. Skills, tools, and environment

### Existing skills that may be available

- **`ambience-long-video-release`**: release planning, event pieces, soundtrack,
  long builds, QA, thumbnails, and YouTube Studio metadata. Use it when available;
  adapt its defaults to the user's current instructions and this project's brief.
- **`cloud-environment-onboarding:setup`**: only when configuring or troubleshooting
  a cloud environment/repository. Do not invoke it merely because a project has
  files. Saving a configuration draft may not activate or publish it.

These names are not a guarantee that another chat has the skills installed.
Discover/read the actual skill instructions when applying them. Never invent a
successful installation or present a newly written module as a pre-existing tool.

### Optional portable skill modules in the companion ZIP

| Module | Responsibility |
| --- | --- |
| `ambience-project-director` | Brief, scope, review gates, progress, handoff |
| `ambience-reference-research` | Real-world references, asset selection, rights |
| `ambience-scene-production` | Camera, geometry, PBR, lighting, still realism |
| `ambience-motion-and-weather` | Rain, water, wind, fire, events, loop QA |
| `ambience-audio-production` | Licensed recordings, acoustic mix, long sound |
| `ambience-long-master-builder` | Codec-compatible units, timelines, QA |
| `ambience-thumbnail-production` | Actual A/B/C covers for every version |
| `ambience-youtube-packaging` | Full Studio fields, credits, metadata limits |
| `ambience-delivery-and-mac` | Real downloads, rebuild kits, local logs |

These are instruction files, not executable apps or independent agents. You may
attach relevant modules in a chat. Install them only through the client's
supported custom-skill workflow, if any; folder layouts vary between products.
The main playbook remains usable when no installation is possible.
Each portable skill folder also contains its own reference copy of this playbook,
so copying the complete skill folder does not break a link to an external sibling.

### Tool map

| Task | Typical tools | Verify before relying on them |
| --- | --- | --- |
| Scene creation | Blender, Cycles/Eevee, Geometry Nodes, Python | Version, GPU backend, headless render, asset path portability |
| Fluid/fire | Blender simulation or compatible external solver/VDB | Bake capability, memory, cache compatibility, actual motion quality |
| Source research | Web/browser/search, public asset APIs | Current pages, downloadable files, individual license evidence |
| Image creation/editing | Available image-generation/editor tools | Reference-image support, output paths, image provenance |
| Formatting/inspection | ImageMagick or equivalent | Dimensions, color profile, file size, contact-sheet layout |
| Audio/video | FFmpeg and FFprobe | Build options, codecs, duration/frame metadata, loudness filters |
| Processing | Python, NumPy, SciPy, Pillow where permitted | Versions, memory use, platform wheels; no assumed installed modules |
| Publication/delivery | Git, storage connector/CLI, release API | Host allowlist, authorization, size limits, actual download route |
| Local Mac run | Homebrew where supported, Python venv, FFmpeg, caffeinate | OS/chip, free space, installation consent and user execution |

Use the session's required image tool for creative image edits when its rules
require it. Do not silently replace that workflow with Python painting. Mechanical
resizing/encoding is a separate delivery step only where tools/instructions permit.

### Environment preflight

1. Identify where commands execute: cloud container, attached workstation, or
   user's Mac. Do not confuse these machines or their file paths.
2. Inspect OS, CPU/GPU, RAM/VRAM, available disk, software versions, and permissions.
3. Open a known scene or minimal test and verify rendering before downloading a
   large asset library or launching a multi-hour job.
4. Verify source download hosts and intended storage/API/upload hosts separately.
   Working Git access does not prove release-API or upload-host access.
5. If blocked, record the actual error and affected host. Do not extract secrets,
   disable security, or bypass network policy. Continue unaffected work.
6. Confirm persistence and job lifetime. Do not promise that a temporary cloud
   workspace, `/tmp`, or an in-memory session survives reconnection.

## 6. Project files and reproducibility

Use a predictable layout; adapt the root to the execution machine:

```text
<Project>/
  PROJECT_BRIEF.md
  project_config.json
  DECISIONS.md
  HANDOFF.md
  status.json
  reference/                 # saved references + URL/rights notes
  research/                  # boards, license evidence, measurements
  assets/
    models/ textures/ hdri/ audio/ plates/ fonts/
    asset_register.csv
  scenes/                    # versioned Blender scene + source scripts
  cache/                     # reproducible simulations, not ordinary Git blobs
  scripts/                   # portable production and QA scripts
  units/                     # compatible calm/intro/event/fade/black pieces
  previews/                  # still, motion, mix, endurance review
  renders/                   # frame sequences and intermediate exports
  audio/                     # source/stem/mix reports and event CSVs
  youtube/
    <version_id>/
      <version_id>.mp4
      thumbnails/ A.jpg B.jpg C.jpg
      title_options.txt description.txt tags.txt pinned_comment.txt
      studio_settings.json AUDIO_CREDITS.txt QA_REPORT.json
  delivery/                  # manifests, checksums, joining/rebuild helpers
  logs/
  1_Setup.command            # optional Mac launchers
  2_Preview.command
  3_Build.command
  4_Check.command
```

### State, provenance, and restart behavior

- Use stable IDs for assets, units, events, versions, and random seeds.
- Store URLs, author, license/version, license URL/evidence date, changes, hash,
  local file path, and where each source is used.
- Keep originals immutable and write generated derivatives to separate paths.
- Use `.partial`/temporary files and atomic rename after successful checks.
- A file existing is not enough to skip a stage: check duration, frame count,
  expected inputs/config hash, and completion report.
- Identify which changes invalidate downstream caches. A new camera can invalidate
  projections, occlusion, simulation fitting, shadows, and all rendered units.
- Keep long processing bounded in memory. Stream hashes and encoded output; do
  not load a 10 GB MP4 or an hours-long float64 soundtrack into RAM.
- Store status with stage, worker state, last heartbeat, processed frames/blocks,
  output paths, error, and next action. A stale heartbeat must not look like live work.
- Use relative paths and explicit configuration. Avoid hardcoded Linux font paths,
  temporary paths, or one machine's Python binary in a supposedly portable kit.
- Preserve source scenes/caches until final delivery is verified. Delete only
  agreed or clearly reproducible intermediates after checking what uses them.

Example status record:

```json
{
  "project": "your_project",
  "phase": "rendering_motion_preview",
  "worker_running": true,
  "execution_location": "cloud",
  "updated_utc": "REPLACE_WITH_ACTUAL_TIMESTAMP",
  "completed": 48,
  "total": 240,
  "unit": "frames",
  "estimated_seconds_remaining": null,
  "estimate_basis": "insufficient completed samples",
  "last_verified_output": "previews/frame_0048.png",
  "blocker": null,
  "next_action": "Finish preview, inspect motion, provide a working review link"
}
```

## 7. Reference research and asset rights

### Research process

1. Read the supplied reference at full size. Record geometry, proportions, lens,
   brightness, color relationships, material wear, wetness, plant shapes, rain
   visibility, motion, and the viewer's apparent shelter/acoustic position.
2. Find real photographs/video for each difficult component, not only attractive
   concept art. Useful groups: architecture, plants, wet glass, rain on surfaces,
   water flow, fire, lighting, furniture, and period details where applicable.
3. Build a manageable board, such as 8–20 well-chosen references. Prefer a few
   relevant images with notes over hundreds of unexamined search results.
4. Write what each reference teaches. Separate research-only inspiration from
   assets actually copied into the finished product.
5. Keep a primary comparison reference and compare each reviewed still/preview
   against it. List concrete gaps: leaf silhouette, stone scale, overly uniform
   roughness, implausible glass reflection, static water, or flat depth.

### Asset sourcing order

- Existing authorized project assets and original work.
- High-quality free commercial assets, preferably CC0/PD or suitable CC BY.
- Licensed free/commercial packs after inspecting the individual license.
- Paid assets only within an agreed budget.
- Procedural/manual creation for missing pieces, explaining the visible tradeoff.

Candidate sources include Poly Haven, ambientCG, Smithsonian Open Access,
BlenderKit, Sketchfab/Fab, Wikimedia Commons, Freesound, and suitable stock sites.
These are candidate services, not blanket license guarantees or promises of
network availability. Some require login or have asset-specific restrictions.

### Rights checks

- Verify the actual asset page, license version, commercial use, attribution,
  redistribution restrictions, and any model/property/person restrictions.
- Reject non-commercial sources for a commercial/monetized use case unless
  separate appropriate permission is obtained. Avoid no-derivatives material
  when editing is required.
- CC0, CC BY, royalty-free, and a stock provider's free license are different.
- A Google Images result is a reference discovery route, not a reuse license.
- For CC BY, credit author/title, source, license/version/link, and changes.
- A bundled model/texture/font is a redistributed asset; confirm redistribution
  rights separately from permission to use its rendered appearance in a video.
- A license page proves terms, not the absence of every possible Content ID claim.
- Do not fabricate source URLs, author names, licenses, or successful downloads.
- Label generated imagery and hybrid methods accurately in provenance and platform
  disclosure where applicable. Do not call a generated plate a camera photograph.

### Asset quality checks

Inspect at the actual camera distance: silhouette, topology, texture texel
density, normal/displacement response, alpha edges, scale, tiling, and specular
behavior. Foreground foliage needs real leaf shapes, veins/thickness cues and
variation; a low-resolution rectangular card can fail even with a large image.
Use enough resolution for the projected detail; “2K” alone is not a quality test.

Do not download a huge library before selecting the camera. Prioritize assets
that will be visible, and benchmark their memory/render cost.

## 8. Scene, camera, materials, and lighting

### 8.1 Composition before detail

Build a rough blockout with real-world dimensions. Establish foreground shelter,
the main subject, middle-ground movement, and distant depth. Ensure the focal
subject survives a small preview; do not let an accidental central tree/post
block the intended view. Use occlusion deliberately rather than filling every gap.

For fixed-camera ambience, a restrained perspective is usually easier to sustain
than a moving camera. A lens around 28–50 mm full-frame equivalent can be a useful
starting range, not a rule. Match the reference and sensor framing; wider lenses
need careful scale and edge distortion checks. Keep enough depth of field to
read the scene. Extreme blur does not repair weak geometry or materials.

Offer 2–3 composition alternatives only when useful. Once one is approved, lock
camera transforms, focal length, framing, and output aspect ratio in configuration.
Record later changes because projections, masks, reflections and cached motion
may depend on them.

### 8.2 Architecture and room dressing

- Use plausible construction: supports reach the ground, roof thickness and
  drainage make sense, panes sit inside frames, stairs and furniture have usable
  dimensions, and loads do not float.
- Add bevels where real edges catch light. Vary materials by construction and
  exposure rather than adding uniform random noise everywhere.
- Choose a few purposeful objects with believable placement and contact shadows.
  Avoid cloned pots/chairs at identical angles, unrelated clutter, and hidden
  geometry that adds cost without affecting the camera.
- Show age through worn edges, water staining, softened wood, dirt in recesses,
  repaired joints, moss in suitable damp areas, and uneven roughness. Do not
  make every surface glossy, distressed, or covered in identical moss.
- For historically specific projects, research the actual materials/construction
  and avoid unsupported claims of exact historical reconstruction.

### 8.3 PBR materials

Use the renderer's appropriate physically based model. Check base-color color
space versus non-color roughness/normal/displacement maps. Calibrate texture
scale and displacement in real units. Excessive bump, sharpened normal maps,
uniform roughness and repeating texture patterns often look more artificial than
moderate detail. High polygon counts alone do not guarantee realism.

Wet materials usually darken diffuse response and gain coherent specular
reflections. Water collects according to slope, shelter and contact; it does not
coat every interior surface equally. Retain roughness variation and dirty seams.

For stone, reference the actual masonry type: irregular stones versus cut blocks,
mortar width/depth, chipped edges, orientation, scale and local weathering. A flat
stone-color texture cannot replace convincing silhouette, recesses and lighting.

### 8.4 Foliage

Use species-compatible references and a varied age/size distribution. Foreground
leaves need curved silhouettes and believable thickness/transmission; midground
can use well-made cards if edges and shadows hold up. Avoid boxy outlines, repeated
fans, identical rotations, overly bright subsurface glow and floating stems.

Check plant attachment, growth direction, gravity, wind exposure and pot/soil
contact. Creepers attach to plausible supports and cluster around suitable light
and moisture; they should not be arbitrary green wires. Interior foliage remains
mostly still unless there is an open door, draft, fan, or another justified cause.

### 8.5 Glass and enclosure

- Model thickness or use the renderer's correct thin-surface approach deliberately.
  Glass IOR around 1.45–1.52 is a plausible starting range; dirty/wet/condensed
  glass needs localized roughness and water layers, not a universal frosted shader.
- Check whether condensation belongs on the inside, outside, or neither given
  temperature and humidity. Avoid covering all panes with identical fog patterns.
- Distinguish pane reflections, transmitted view, rain on the outer face, and
  near/far objects. A rain layer must not float in front of the interior framing.
- Respect seals, frames, gutters and drip edges. Water trails follow gravity and
  pane slope; merged trails, runoff and small stationary droplets differ in scale.
- Test reflections/refractions from the final camera early. Excessive reflections
  can hide the weather; no reflection at all can make the pane seem absent.

### 8.6 Lighting and exposure

Set a consistent color-management pipeline, such as AgX for scene rendering and
a deliberate SDR Rec.709 delivery transform. Do not apply display transforms twice.
Check the relationship between cool ambient daylight/moonlight and warm practical
sources; darkness does not mean every unlit surface is crushed to black.

Use lamps/emissive elements supported by believable illumination. Preserve warm
highlights and readable texture instead of clipping white rectangles into windows.
Choose an HDRI/sun/area-light arrangement that makes sense for the enclosure and
weather. Strong directional sunlight rarely matches an overcast heavy-rain sky.
Add restrained atmospheric depth; uniform opaque fog looks like a grey overlay.

Review at native size and normal playback size. Compare shadows, roughness,
wetness, scale, reflections and leaf edges with real references. Save an honest
gap list before declaring the still photoreal.

### 8.7 Still review gate

Deliver a whole-scene still, critical detail crops, a reference comparison, scene
file/scripts, and a short explanation of visible limits. Separate the actual
render from a generated concept image or illustrative cover. Proceed to expensive
motion work after the appearance is reviewed or the user explicitly waives it.

## 9. Weather, water, fire, and optional motion

### 9.1 Rain

Create distinct scales: distant rain for density, middle rain for depth, near
streaks for camera-scale impact, plus surface-specific splashes and runoff.
Use physically plausible streak direction, speed, opacity and motion blur.
Rain should respond to wind and be visible where it catches light; large uniform
opaque white lines tend to look like a screen filter.

For cyclic particles, implement continuous birth/recycling so the top of the view
never empties. Warm up simulations before the visible interval. Hide recycling
outside the camera or with natural occlusion; visible teleports are not acceptable.
Test early, middle and late frames, not only the first second. Record whether the
rain is true geometry/particles, a composited footage layer, or a screen-space
effect. Respect the user's requested method.

Objects beneath roofs should remain sheltered. Eave water follows roof coverage
and gathers in appropriate channels. Impacts appear on ground, water or leaves
where rain actually lands. Do not rain through solid ceilings or interior glass.

### 9.2 Wind and plants

Animate stems/branches with a coherent wind field and layered response, then add
smaller leaf flutter. Heavy branches move more slowly than leaf tips. Avoid rigid
whole-plant rotation, synchronized copies, unnatural looping jerks and sheltered
indoor plants moving as violently as exterior trees.

Use repeatable, smooth motion with compatible periods where a loop is required.
Record wind direction and make rain lean, foliage and nearby loose elements agree.

### 9.3 Flowing water

Choose by camera distance and interaction requirements:

| Method | Appropriate use | Limitation to document |
| --- | --- | --- |
| Animated shader/displacement | Distant small ripples, quiet surfaces | Weak at contact, breaking waves, foam and changing silhouettes |
| Geometry-driven flow | Modest water movement with controllable shape | May approximate turbulence and conservation |
| FLIP/APIC/SPH/PBF or comparable fluid simulation | Visible flow, obstacles, cascades and contact | Bake cost, mesh resolution, cache portability and solver limits |
| Licensed footage composite | Fixed-camera natural water when approved | Perspective, edges, occlusion and reflection mismatch |

Use the correct solver label. A custom PBF solver is not a Mantaflow bake, and an
animated texture is not a fluid simulation. If a tool crashes or is unavailable,
report it and choose an agreed alternative rather than claiming the requested bake.

Build bank/bed geometry with sensible gradient and obstacle contact. Match water
depth, surface velocity and turbulence to scale and slope. Foam should gather
around breaking/contact/shear zones, not slide over the whole river as a uniform
image. Ripples, foam, spray and lighting need temporal consistency with the liquid.
Water IOR near 1.333 is a useful optical starting point; reflections and absorption
depend on depth and environment, not an opaque blue paint material.

When slowing water, retime the liquid and dependent foam/spray together. Do not
slow rain, plants and unrelated motion by accident. Recheck gravity/contact cues:
slowing a waterfall too much can look like low gravity. Report approximate methods
and their visible limitations.

### 9.4 Fire, candles, and smoke — optional

Use high-quality licensed fire elements, VDB volumes, or a convincing simulation
before trying elaborate procedural stand-ins. Avoid cloth-like flame meshes,
repeated solid teardrops and neon emission with no fuel/contact light.

Fire needs logs/fuel, ember glow at contact, darkening/charring, plausible flame
structure, light on nearby surfaces and restrained smoke where airflow supports it.
Candles need real scale, wick attachment, wax translucency/drips and a compact
flame with subtle variation. Large random flicker or identical flame copies look
artificial. Handle transparent flame footage with correct premultiplication,
occlusion and black-level matching, and disclose the composite method.

Test fire at the final camera exposure. A beautiful isolated asset can fail when
its brightness, color, depth or contact does not match the room. Confirm looping,
source license, cache completeness and performance before committing to it.

### 9.5 Lightning and thunder — optional

Respect the selected branch: no events, sound-only thunder, or linked flashes and
thunder. For visible lightning, illuminate relevant surfaces, fog, reflections
and shadows coherently; an isolated bright sprite does not light a real scene.
Keep a restful treatment when that is the brief, and do not add flashes after the
user has excluded them.

For an apparent strike at distance `d`, a rough thunder delay is `d / 343` seconds
at ordinary near-surface temperatures, with natural variation. This is a staging
guide, not a precise weather model. Record actual event times and delays. Distant
off-screen thunder can exist without visible lightning.

### 9.6 Snow, fog, waves and other effects — optional

Apply the same rules: scale, continuous supply, shelter, contact, coherent wind,
correct depth ordering, and loop behavior. Snow has accumulation and flutter;
it is not white rain. Fog should reveal depth rather than erase the scene.
Ocean surf is a substantially larger task than pond ripples; benchmark its
simulation/render cost and do not assume a stream setup transfers unchanged.

## 10. Seamless loops, event pieces, and render preparation

### 10.1 Choose a loop architecture

- **Short perfect loop:** efficient, but repeated distinctive events become obvious.
- **Longer base loop:** greater variety, higher render/cache cost.
- **Calm loop plus optional event pieces:** render short compatible units and vary
  scheduling; each event piece starts/ends at a compatible scene phase.
- **Layered loops:** independent motion periods can reduce visible repetition,
  provided the assembled overall repeat period and all seams are understood.
- **Continuous long simulation:** appropriate when non-repeating motion matters
  enough to justify the cost; do not default to rendering every hour uniquely.

For an integer-FPS loop with period `L`, output exactly `round(L * fps)` distinct
frames. Do not append the duplicate endpoint. For rational FPS such as 30000/1001,
plan in integer frame/sample counts and document exact rational timing.

### 10.2 Motion continuity

Periodic animation should match position, orientation, brightness and preferably
velocity at the join. Integer harmonics of a chosen period can help wind or light
functions repeat smoothly. Random seeds alone do not make noise periodic.
Particles need valid state across the wrap. Fluid transitions may require
simulation warm-up, compatible states, a longer solve, or a documented blend.

Blending 3D fluid fields is an approximation, not proof of an exactly periodic
physical solution. A 2D crossfade can hide a cut while creating double edges or
unphysical flow. Choose the method deliberately and disclose material limitations.

Measure the last-to-first change against normal adjacent-frame changes, including
regional checks. Average pixel difference alone can miss a local splash popping,
brightness flash or direction reversal. Watch several repeats at normal speed.

### 10.3 Event pieces

Use whole-loop durations where possible. Start/end events at a matching loop
phase; keep framing, exposure, weather and camera constant. Render moving additions
as isolated layers only when occlusion, contact, shadows, reflections and fog can
be reconstructed correctly. Partial/crop renders must match native full-frame
pixel placement and color transforms. Do not accidentally resample a held layer.

Build an event manifest with piece ID, duration/frames, phase, flash/call/impact
times, sound IDs and variant. Avoid consecutive identical events and overly
regular scheduling. Do not invent events solely to make a metadata chapter list.

### 10.4 Render settings and budget

Use small previews for composition, then native-resolution crops/frames for
quality. Increase samples only when the remaining defect is actually sampling
noise. Denoising cannot fix boxy leaves, wrong materials, absent water flow,
bad lighting, incorrect glass, or fake fire. Inspect temporal denoising/flicker
and fine rain/foliage loss, not just a single clean still.

Record renderer/version, device, samples, denoiser, volume settings, motion blur,
color transform, output bit depth and frame rate. An approximately 180-degree
shutter is a possible starting point, not a universal rain setting. Tune streaks
and motion blur against reference and actual playback.

Benchmark representative heavy frames, not only an empty frame. Estimate:

```text
render_time ≈ median_seconds_per_representative_frame × new_frames
             + simulation_bake + compositing + encoding + contingency
```

Publish the benchmark, hardware, estimate range and unmeasured portions. Do not
give a universal “10 minutes” or “one hour” guarantee for a new computer.

### 10.5 Common export units

All units intended for H.264 concat-without-reencoding need compatible codec
parameters and stream metadata: dimensions, FPS/time base, pixel format, profile,
level, SAR, color tags, reference behavior, SPS/PPS and closed GOPs.

An illustrative SDR H.264 starting point is CRF 16–20, yuv420p, closed GOP, with
keyframe spacing appropriate to the chosen FPS. For 24 fps, a 48-frame GOP is a
common option. Do not copy 48 blindly to a different frame rate or require a fixed
profile/level that cannot support the chosen resolution/rate.

Probe `extradata_hash` and relevant stream fields across every unit. Identical
command-line flags do not prove identical headers. Building a black unit from the
same scene source/filter chain can avoid accidental SAR/header changes. If headers
remain incompatible, use a known compatible re-encode or one continuous encode;
do not force an unsafe concat because it appears fast.

Keep a high-quality master/image sequence when justified by the budget. Native
4K detail must come from adequate source/render detail; upscale-only output is
not evidence that a 1080p asset became a genuinely detailed 4K scene.

## 11. Natural audio and soundtrack production

### 11.1 Define the listening position

Decide what the dominant sound is and where the listener sits. Rain on glass,
metal roofing, foliage, soil and water sound different. An enclosed room muffles
outside high frequencies; an open porch has a clearer weather bed and nearby
drips. Avoid combining loud unrelated recordings merely because they are licensed.

Suggested layer order for rain-led ambience: rain bed first, near roof/glass/edge
texture second, stream/wind as quieter support, sparse events last. For another
theme, change the priority. Do not force a river, insects, fire or thunder into a
scene that does not call for it.

### 11.2 Source vetting and rights

Prefer long original natural recordings with documented commercial rights. Record
author, title, source, license/version/link, file hash, duration and exact edits.
Inspect the license on the actual source page; a filename or mirrored upload is
not sufficient evidence by itself. Preserve evidence and credit only sources
actually used in that release version.

Use waveform/RMS/peak plots, spectrograms and candidate-event lists to find
handling noise, voices, birds, clicks, embedded thunder and abrupt tonal changes.
Then audition selected passages and flagged regions where listening is available.
Numerical/spectral checks do not certify that no voice or unwanted animal exists.
State the listening coverage honestly. Do not claim an exhaustive human audition
of an hours-long soundtrack that was only measured automatically.

### 11.3 Processing and balancing

- Decode large sources as float32 slices or memory-mapped blocks, not entire
  long float64 arrays. Keep original sample rates in provenance and use a common
  working rate such as 48 kHz for production.
- Start with subtle EQ and removal of true rumble/handling noise. A rain high-pass
  near 80–120 Hz may help some recordings, but inspect the source; filtering out
  all low weather energy can make rain thin.
- Tame intrusive splash/tonal bands gently rather than removing every transient.
  Avoid pumping, metallic denoising and over-compression.
- Preserve a coherent stereo image. Width/pan must match the sound's apparent
  location. Swapping left/right can vary a nondirectional bed but may conflict
  with a known moving source or spatial feature; decide by source type.
- Keep supporting sounds lower by ear and measurement. A stream 8–12 LU below
  a rain bed can be an initial audition target, not a mandatory measurement rule.
- A gentle master near −24 LUFS integrated and true peak at/below −2 dBTP is a
  possible sleep-ambience target, not a YouTube requirement. Match the chosen
  audience/device and approved preview; distinguish LUFS integrated, short-term,
  momentary loudness and sample peak.
- A sample-peak ceiling is not a true-peak guarantee after AAC encoding. Measure
  the encoded file with oversampling/appropriate loudness tools.
- Use slow event attacks and natural tails for restful distant thunder. Do not
  make every rumble identical. Pitch/time changes are variants of one source,
  not independently recorded thunder events.

### 11.4 Long sound without obvious short repetition

Use diverse clean source spans, randomized grain selection, suitable overlaps
and stored random seeds. For example, 60–90 s grains with 3–6 s overlaps can work
for steady rain; tune to source and content. Avoid consecutive duplicate grains
and cutting through distinctive calls/voices/transients. Do not reverse a stream
or transient-rich recording simply to claim more source variety.

Equal-power crossfades are useful for uncorrelated audio but can raise level when
signals are correlated. Check overlap loudness and peaks, not just the fade curve.
Keep randomization bounded and documented. Music, speech and directional events
need different editing logic from a stochastic rain bed.

Place events from an explicit schedule with sound ID, start time, gain, variant,
duration and any linked visual time. For calm thunder a roughly 2–5 minute spacing
may be a starting choice; user preference and source variety take precedence.
Do not insert a loud surprise at the first second. Dark-screen versions may use
quieter/sparser events if requested, while maintaining a continuous rain bed.

Stream mixed blocks into the encoder to bound RAM. Apply defined opening/ending
fades and true-peak-safe control. Cache completed stages with duration/config/hash
checks; interrupted output is not a valid completed soundtrack.

### 11.5 Audio review deliverables

Deliver a combined preview plus solo rain/support/event stems or representative
clips. Provide measurements, event CSV, source credits and the exact mix settings.
Review both quiet passages and the loudest event. Listen on ordinary speakers or
headphones where available; avoid claiming universal sleep/health outcomes.

## 12. Long-video timeline and assembly

### 12.1 Parameterized timeline

Define each version independently:

```text
T = total duration
S = scene-visible portion, including any picture fade to black
dark duration = T - S
opening + visible units + scene closing = S
audio duration = T
```

For a scene-throughout version, `S = T`. For dark-from-start, `S = 0` and no scenic
intro/badge should appear unless explicitly requested. For scene-then-dark, the
picture fades out before `S`; the audio must not accidentally fade out there.
Only the final audio ending fades at `T`.

Construct timing in frame/sample counts. If units do not divide the requested
duration, plan a compatible partial unit or special closing unit. Do not silently
change the requested length, freeze an arbitrary last frame, or add duplicate
frames to make arithmetic easy.

### 12.2 Opening and ending defaults

Offer the following starting design, adapting to explicit preferences:

- Approximately 1 s of black, then a 5 s picture fade.
- Sound enters with the picture and rises smoothly over about 8 s.
- If a subscribe reminder is agreed, show a calm one-time badge around seconds
  6–14, with a short soft fade/rise, safe margins, no sound effect and no flashing.
  Use a supplied channel asset or simple original typography/iconography.
- Fade picture/audio out over about 20 s at the appropriate ending. The picture
  fade for a scene-then-dark release occurs before its dark transition; audio
  continues until the full video's ending.

If an installed skill defaults the badge to enabled, explain that default and
honor the user's current choice. Never force a visual badge onto an explicitly
black-from-start release or add branding not supplied/authorized by the user.

### 12.3 Preview → endurance → masters

1. Short visual test, usually 15–30 s: rain supply, plant motion, water contact,
   fire if present, loop seam and exposure.
2. Mixed audiovisual test, usually 1–3 min: sound balance and representative events.
   Clearly label deliberate review cuts or accelerated event timing.
3. Endurance test, commonly 10–20 min: exercise multiple loops, varied events,
   intro/badge, picture fade to dark if applicable, audio continuity and ending.
4. Build each long master only after the necessary gates are satisfied.

An endurance test may exercise a one-hour transition earlier for testing; label
that mapping explicitly. Do not let accelerated test timing leak into the final
version's actual scene duration or description chapters.

### 12.4 Efficient assembly

Reuse verified compatible visual units instead of rerendering every hour. Build
the long soundtrack separately, then mux with the visual timeline. If stream
copy is valid, use it; otherwise encode from a compatible source. Use progressive
H.264/AAC MP4 as a broadly compatible upload copy unless another verified format
is selected. A 48 kHz stereo AAC track around 256 kb/s is a reasonable starting
point, not a mandatory quality ceiling.

Use fast-start layout for downloadable MP4s where appropriate. Verify exact
container/stream durations, timestamp continuity, frame count, audio priming and
end behavior. Do not assume that a successful FFmpeg exit proves a seamless file.

### 12.5 Disk and time budgeting

Estimate output and intermediate sizes before building:

```text
approximate_bytes = seconds × (video_bits_per_second + audio_bits_per_second) / 8
```

Account separately for scene and black-screen bitrates, source caches, audio
tracks, renders, temporary mux/fast-start copies, ZIPs and transport parts. Leave
operating headroom; RAM and disk are different constraints. A mostly black
eight-hour version can be smaller than a three-hour scene-throughout version.

Benchmark representative work on the actual hardware. Show a range and the
estimated basis. Encoding/QA speed can differ greatly from real-time duration.
Keep progress by frames or audio blocks; where no meaningful percentage exists,
show the active stage and heartbeat rather than a fabricated ETA.

## 13. Technical and perceptual QA

### Container and image checks

- Correct filename/version, exact requested duration, dimensions, rational FPS,
  pixel format, color tags, SAR and expected frame count.
- No missing/duplicate sequence frames, broken timestamps, unintended freezes,
  codec mismatches, corrupt ranges, or absent stream.
- Decode representative windows at intro, loop joins, event joins, scene/dark
  transition, dark middle and ending. Full video decode is stronger and may be
  appropriate, but label sampled versus exhaustive coverage accurately.
- Inspect beginning black, fade progression, badge timing, text safe margins,
  black-screen behavior and final fade. Use tolerances appropriate to decoded
  color range rather than assuming every encoded black pixel is numerically zero.
- Compare native-size foliage/glass/water/fire crops and several repeated loops.
  Check ghosting, denoise shimmer, edge leakage, double rain layers and popping.

### Audio checks

- Decode and measure the full encoded soundtrack for integrated loudness,
  true peak, clipping and timing. This is not equivalent to full human listening.
- Use audio-only decoding (`-vn -sn -dn` where applicable) for long audio scans;
  needlessly decoding hours of video wastes time and can hide the actual bottleneck.
- Check start/end silence/fades, every visual-to-dark transition, representative
  grain joins, quiet passages, loudest thunder and source changes.
- Confirm the stream/fire/wind has not become louder than the intended main bed.
  Inspect whether limiting/normalization audibly pumps or changes event balance.
- Do not “prove no speech” or “no unwanted animals” solely with RMS/spectrograms.

### Provenance and repeatability

- Stream SHA256 hashes of complete files in bounded chunks. Never use a multi-GB
  whole-file read merely to calculate a hash.
- Save QA results with machine/version, checks performed, measurements, paths,
  config hash, file bytes and checksum. Record failures and their repairs.
- Recheck only what a change affects, unless a new concern justifies broader work.
- Include human-review limits, hybrid/simulation approximations, and whether the
  long file was watched, sampled, fully decoded, or only container-probed.
- “QA passed” must refer to named checks, not a generic assertion of perfection.

## 14. Three thumbnails for every version

### 14.1 Deliver actual assets

Create **three finished thumbnail images per release version**, not only an idea
list. Two versions normally mean six upload-ready images. If the user requests a
different count, use that count. Do not mark this stage complete before the files,
comparison sheet, QA and working download links exist.

Use the approved scene as the visual foundation. Prefer actual final video
frames for literal fidelity. If permitted image-generation tools are used for
creative cover edits, provide the approved image as a reference, retain outputs
and prompts/provenance, inspect invented details, and label them as cover edits
rather than untouched frame exports. If an image tool is unavailable, explain
the limitation; do not claim ideas are completed thumbnails.

### 14.2 A/B/C design structure

| Option | Visual approach | Question it tests |
| --- | --- | --- |
| A | Wide recognizable scene with a short clear headline | Does explicit topic identification help? |
| B | Closer focal subject, minimal text, accurate duration badge | Does the atmosphere/subject carry the cover? |
| C | Alternative balanced crop or mood/benefit wording | Does a different composition/message attract interest? |

Keep the channel style coherent, but make the three variants distinguishable.
Where a controlled test is desired, vary one main factor rather than changing
every element. Do not promise a winner before audience data exists.

### 14.3 Image and typography rules

- Make the focal subject readable at 320 px width and a smaller phone preview.
  Avoid busy fine-detail text, long sentences and large logos.
- Use high-contrast, properly spaced typography with safe margins; keep critical
  wording away from YouTube's bottom-right duration overlay.
- A duration badge must match the exact version. For scene-then-dark, use explicit
  wording such as **8 HOURS · DARK AFTER 1 H**, not an ambiguous full-time-dark claim.
- Do not add lightning, animals, people, extraordinary weather or another hero
  subject that never appears in the video. Avoid medical promises or unrelated
  clickbait. A brighter cover may improve readability, but should still represent
  the actual atmosphere and subject.
- Do not use **No Ads**. Use **No Mid-Roll Ads** only if the channel's actual settings
  and resulting configuration support that narrower claim; avoid it by default.
- Verify font rights if fonts are redistributed. Retain originals separately.
- Read every generated word, duration and timing phrase. Generative text can be
  misspelled even when the design looks polished.

### 14.4 Export and review

Use a broadly compatible target such as **1280 × 720, 16:9, sRGB JPG/PNG**, keeping
each file below a conservative **2 MB**. Verify current platform requirements
before upload because limits/features can change. Specify bytes precisely in
manifests; do not confuse decimal MB and binary MiB when close to a limit.

Check dimensions, file size, decode, color profile, clipping and readability.
Inspect the original approved scene alongside the covers and describe material
changes. Create:

```text
youtube/<version_id>/thumbnails/A.jpg
youtube/<version_id>/thumbnails/B.jpg
youtube/<version_id>/thumbnails/C.jpg
delivery/thumbnail_comparison.jpg
delivery/thumbnail_small_size_review.jpg
delivery/thumbnail_manifest.json
delivery/All_Thumbnails.zip
```

The comparison sheet needs visible version and A/B/C labels outside the cover
art. The ZIP needs the actual upload files, not just the comparison image. Store
hashes, source frame, method, wording, dimensions, bytes and review status.
Provide individual links and one ZIP when delivery tools support them.

If Test & Compare is available, use the three matching-duration files on the
matching video. Review results with enough data and the platform's actual
experiment status. Do not declare a universal CTR threshold or a winner from a
tiny sample. Record learnings for the next project.

## 15. Complete YouTube Studio package

Create one complete package per version. The descriptions must already contain
the correct source credits; do not make the user assemble scattered license
snippets. Save copy-ready text files and a human-readable worksheet.

### 15.1 Titles

Supply three accurate options, each within the current title limit (commonly
100 characters; verify current limits). Use the scene/sound subject, duration,
and important dark-screen behavior naturally. Avoid keyword stuffing, guaranteed
sleep/medical benefits, fake recorded locations, “real footage” claims for
generated scenes, and claims of ad-free playback.

Examples of generic structures:

```text
[SETTING] in [WEATHER] | [MAIN SOUND] & [SUPPORT] | [DURATION]
[DURATION] of [WEATHER] at [SETTING] | [MOOD / SUPPORTING SOUND]
[MAIN SOUND] for Rest | [DURATION] | Dark Screen After [SCENE DURATION]
```

Change wording to fit the actual content. Not every title needs every keyword.

### 15.2 Complete description structure

1. One or two natural sentences describing what the viewer sees/hears.
2. Exact duration and scene/dark-screen behavior.
3. Important experience facts: music/speech/flashes only as actually present or
   excluded; sound priorities and any meaningful differences between versions.
4. Useful true chapter timestamps, if appropriate.
5. Cross-link to the other version and optional channel/playlist/subscribe link.
6. A concise truthful original/generated/hybrid disclosure where relevant.
7. Complete attribution for every used source requiring it, with accurate edits.
8. A small set of relevant hashtags, commonly 3–5.

Keep within the current description limit (commonly 5,000 characters). Count
titles/descriptions/tags programmatically and leave headroom for URL replacement.
A long final URL can exceed a limit even when a short placeholder did not.

Example attribution pattern, repeated per used asset:

```text
[SOUND/ASSET]: "[TITLE]" by [AUTHOR].
License: [LICENSE + VERSION] — [LICENSE URL]
Source: [ACTUAL ASSET URL]
Changes: [SPECIFIC FILTERING / EDITING / PITCH / LOOP / MIX CHANGES].
```

Only credit assets used in this version. Do not list a rejected candidate or a
short-preview-only sound as if it supplied the final soundtrack. Keep visual,
audio and font credits as needed. Do not invent provenance when metadata is missing.

### 15.3 Chapters

Use actual final-timeline timings, not review excerpt positions or accelerated
test transitions. Where current YouTube chapter rules apply, start at 00:00,
provide at least three ascending timestamps, and keep chapters at least 10 s.
Verify the current rules before upload. Stable ambience may be clearer without
chapters than with fabricated events.

For scene-then-dark, meaningful phases can be opening scene, fade to black, and
dark-screen sound. Derive the fade's exact start from the final timeline. Do not
label “Thunder” at an arbitrary time because an event happened elsewhere in a
shorter preview. Automatic chapters may be disabled when using a deliberate manual
list or when they would add misleading place/concept labels.

### 15.4 Tags, hashtags and pinned comment

- Provide one comma-separated tag block per video, within the current total limit
  (commonly 500 characters). Prioritize specific scene, sound and version terms.
- Use relevant hashtags, not a wall of unrelated search terms.
- Draft one natural pinned comment per version with a focused viewer question
  and an optional cross-link. Do not fabricate user engagement or testimonials.
- Leave unresolved URLs as conspicuous placeholders and remove/replace them
  before publication. Do not pretend the videos already have public watch URLs.

### 15.5 Studio fields in upload order

| Field | Decision / instruction |
| --- | --- |
| Title | Choose one checked title option |
| Description | Paste the complete version-specific text including credits |
| Thumbnail | Upload the chosen A/B/C or use the available comparison feature |
| Playlist | Select/create the user's actual playlist; do not invent its URL |
| Audience | Classify the actual intended audience; ordinary general-audience ambience is often not made for kids, but assess rather than blindly defaulting |
| Age restriction | Assess actual content; ordinary calm scenery usually has no basis for restriction |
| Paid promotion | Match actual sponsorship/placement facts |
| Altered/synthetic content | Use truthful disclosure where realistic generated/altered scenes meet current platform criteria; typically Yes for realistic AI-created environments |
| Automatic chapters/places/concepts | Choose deliberately; avoid fictional-location mislabeling |
| Tags | Paste the checked version-specific block |
| Language | Match actual dialogue if present; do not imply spoken English when there is none; metadata can separately be English |
| Captions | Add accurate dialogue captions if relevant; ambient descriptions are optional accessibility content |
| Recording date/location | Leave unset unless real and verified; do not invent a filming location for a fictional scene |
| License | Standard YouTube License is a common choice; do not license third-party components beyond the rights you actually have |
| Embedding | Creator choice; commonly enabled |
| Shorts remixing | Choose from the actual options based on rights and preference; do not promise an option exists for every account |
| Category | Entertainment is often suitable; choose the actual content category |
| Comments/moderation | Creator choice; basic moderation can be a practical default |
| Monetization | Depends on channel eligibility, content and current review; do not promise approval |
| Mid-rolls | For uninterrupted ambience, recommend off if available; check both automatic and manual slots |
| Cards/end screens | Use sparingly; avoid intrusive or contradictory graphics on a dark-screen ending |
| Copyright/checks | Review actual results; retain license records and investigate any claim before deciding how to respond |
| Visibility | Private for review; publish/schedule only with authorization |

Current interface names and platform policies can change. Verify them if tools
allow, and describe unverified recommendations as such. CC0/CC BY evidence may
support a legitimate claim response; it is not a guarantee that every claim is
invalid or that monetization is automatic. Avoid blanket claims of channel safety.

### 15.6 Upload and schedule

- Confirm the account supports the intended video length and current upload limits.
  Login/verification is handled by the user or an explicitly authorized connector.
- Upload privately first, wait for the intended resolution to process, and review
  copyright checks. Do not publish while HD/4K processing is incomplete unless
  the user knowingly chooses that.
- Confirm title, thumbnail, source credits, synthetic-content disclosure, dark-screen
  behavior, cross-links, ad settings and final file version before publication.
- Ask for dates only when scheduling is requested and no authorized dates exist.
  Record an IANA timezone such as `Europe/Berlin`; account for daylight saving.
- Use audience analytics rather than claiming a universal best posting hour.
  A gap between related versions may be useful, but is not mandatory.
- Pin the actual comment after publication when authorized. Check playback on a
  normal device and save the actual video IDs/URLs in the project handoff.
- Record thumbnail experiment results and sensible follow-up changes. Do not
  automatically change titles/ads/schedules without the appropriate authorization.

## 16. Delivery, downloads, and local Mac execution

### 16.1 What a finished delivery contains

- Final video files and version manifest with bytes, duration, resolution, FPS,
  audio properties and streamed SHA256.
- Short review clip, representative stills, QA reports and review limitations.
- Actual A/B/C thumbnail files per version, comparison sheet and ZIP.
- Complete Studio worksheets and copy-ready metadata/credits.
- Source scripts/configuration and agreed source scene/cache/asset package.
- A readable README explaining download, verification, playback and recovery.

State exactly which files are delivered versus only described. A README pointing
at a cloud file is not the same as a downloadable full video. A preview link is
not a full-master link. A local rebuild is not necessarily byte-identical transfer.

### 16.2 Delivery route matrix

| Route | Useful when | Required checks |
| --- | --- | --- |
| Supported chat attachment | File size and client permit it | User-facing link actually works, full bytes accessible |
| User-authorized storage | Multi-GB masters | Destination authorization, quota, access, checksum, expiry |
| Draft release assets | Review delivery with repository access | API/upload hosts, auth, per-asset limits, login requirements |
| Public release | User explicitly wants public distribution | Explicit publication authorization, asset rights, verified URLs |
| Transport parts | Host per-file limit is too small | Exact byte slices, part hashes/order, joined-file hash |
| Local rebuild kit | Long masters are hard to transfer | Smaller licensed inputs, tested build path, actual local instructions |
| Source scene kit | User wants editable/new Blender renders | All dependencies, caches or regeneration path, compatible renderer |

Do not expose private assets through a public repository merely to avoid a
download problem. Do not use an anonymous upload site or tunnel without agreed
rights/destination. Do not provide an imagined URL or local/cloud path as if the
user could download it in the browser.

### 16.3 Hosting and network limits

Verify current limits before choosing a host. Ordinary GitHub repository files
have a commonly enforced 100 MiB file limit and lower recommended sizes; release
asset limits and API behavior are separate and must be checked. Git LFS is not
unlimited free storage and may have account quotas/access behavior.

Test ordinary Git, repository API and upload hosts independently. A saved network
configuration draft may still require a user-visible save/apply/publish action.
Report an actual proxy block, auth failure or size failure accurately. Do not
request another credential just because a network allowlist is blocking the host.
Never print tokens, extract secrets or disable security to bypass restrictions.

### 16.4 Checksummed transport parts

If needed, split the final MP4 as exact ordered byte slices under the destination's
current per-file limit. These are not independently playable clips or re-encodes.
Provide each part's index, bytes, SHA256 and offset plus the complete master hash.
Verify remote parts after upload and the whole joined file after download.

Stage one part at a time if disk is tight. Do not delete the only master after
uploading an unverified part. Joining should write a temporary output, check the
complete hash, then rename atomically. State extra disk needs for parts plus the
joined file. Use streaming I/O, not whole-file in-memory concatenation.

### 16.5 Mac rebuild versus Blender rerender

| Kit | What it does | What it needs |
| --- | --- | --- |
| Timeline/audio rebuild | Reuses approved rendered units and rebuilds hours locally | FFmpeg, compatible Python dependencies and licensed source audio |
| Source render kit | Renders new frames and possibly simulations | Blender/version, assets, caches or bake scripts, more RAM/VRAM/disk/time |
| Download/join kit | Reassembles exact already-built masters | Downloaded parts, shell/hash tools, enough free disk |

A timeline rebuild does not require Blender if all visual units are supplied.
It does not let the user change camera/geometry as a complete 3D project would.
Different FFmpeg builds, CPU paths and encoders can produce different bytes while
preserving the intended audiovisual timeline. Do not promise identical checksums
for a rebuild unless actually demonstrated.

### 16.6 Local launchers

Use numbered `.command` files that call a shared `scripts/mac_run.sh <stage>`:

```text
1_Setup.command    -> verify package, install/verify agreed dependencies,
                     download and hash required licensed inputs
2_Preview.command  -> create a short/endurance preview for local review
3_Build.command    -> build the selected full versions
4_Check.command    -> run documented QA and create final reports
```

Put the project in a stable folder such as `~/Movies/<Project>/` and place each
version under `youtube/<version_id>/`. Hard links may expose a completed file in
another folder without another disk copy on the same filesystem; verify support
and never overwrite an unrelated existing file. Otherwise use documented paths
or appropriate copies/symlinks and their access constraints.

Detect Apple silicon versus Intel, macOS/Homebrew support, Python ABI, wheels,
FFmpeg features and Blender compatibility. Prefer a private virtual environment.
Do not blindly install an entire Linux requirements file containing platform-
specific Blender/simulation packages for a simple audio/timeline rebuild.

If Homebrew or developer tools are missing, provide official installation
instructions; do not run an unreviewed remote shell installer or ask for login
credentials. Quote paths containing spaces. Do not repurpose `HOME` or other
system variables. Test launchers' shell syntax and dependencies.

If Finder blocks a launcher, provide a reviewed Terminal invocation such as:

```bash
bash "$HOME/Movies/<Project>/1_Setup.command"
```

Do not instruct the user to disable Gatekeeper. `caffeinate` may prevent idle
sleep for the foreground job; it does not guarantee survival after closing the
Terminal or shutting the laptop. Explain whether a job is foreground or persistent.

Write terminal progress, `status.json` and stage logs. On failure, preserve the
actual error and explain safe restart behavior. Let the user run one stage at a
time. A completed stage can be reused only after checks match its inputs/config.
Give a progress-inspection command and ask for its output when diagnosing a local
problem; never pretend to see the user's local process from the cloud.

### 16.7 Link and package verification

Fetch user-facing URLs and check status, content length where available, and
downloaded hashes. A 200 HTML login page is not a valid MP4/ZIP download; inspect
content type and actual bytes as needed. State whether login or expiry applies.
Open archives and verify contents/paths/checksums. When only a Linux smoke test
was possible, report that Mac launch behavior is untested rather than claiming
cross-platform verification.

## 17. Review gates, estimates, and completion checklist

### Gate-by-gate deliverables

| Gate | Actual deliverable | What the user reviews | Next work |
| --- | --- | --- | --- |
| Brief | Filled decisions and production route | Concept, versions, budget, hardware | References/blockout |
| Composition | 1–3 labeled views | Framing and focal point | Detail scene |
| Realism still | Native still, crops, reference comparison | Materials, plants, lighting, scale | Motion |
| Motion | 15–30 s plus detail views | Rain supply, flow, sway, loops | Mix/event test |
| Audio | Combined preview, stems, credits | Dominance, events, comfort | Endurance |
| Endurance | Longer test, measured reports | Repetition, fades, dark transition | Long build |
| Final | Masters, QA, six-or-required thumbnails, metadata, delivery | Exact versions and usable files | Authorized upload/publication |

Review durations are examples, not hard limits. An unresolved visual defect
should be repaired before an expensive long build. Do not repeatedly stop after
minor reversible steps if the user has authorized the larger work and the next
formal review gate has not been reached.

### Estimate discipline

Provide separate ranges for research, scene work, simulation, unique-frame
rendering, assembly, QA, transfer and upload processing. Hands-on creative work
and unattended machine time differ. Benchmark representative samples, include
hardware/network facts, and revise estimates when measurements change.

Never infer that an 8 h video needs 8 h of rendering, or that a 77 MB kit means
the full build needs only 77 MB disk. Source preparation, generated audio,
temporary mux files and outputs may be orders of magnitude larger.

### Completion checklist

- [ ] Brief and chosen versions are recorded; no cancelled project was resumed.
- [ ] Reference research and asset rights are documented.
- [ ] Approved still and motion previews exist and are accessible.
- [ ] The method matches the user's request, with material approximations disclosed.
- [ ] Rain replenishes; water/fire/contact and plant motion are convincing at scale.
- [ ] Loop joins and event transitions are reviewed at normal playback speed.
- [ ] Audio uses the actual licensed sources; levels/events/fades are approved.
- [ ] Long versions have exact scene/dark/audio durations and technical QA reports.
- [ ] QA coverage says sampled/full-decode/listening accurately.
- [ ] Three actual thumbnails exist per requested version; labels match behavior.
- [ ] Titles/descriptions/tags/settings and complete credits exist per version.
- [ ] Delivery links and hashes are verified, with access/expiry stated.
- [ ] Mac/source/rebuild kit claims match what is actually included and tested.
- [ ] Handoff lists decisions, file locations, scripts, blockers and next action.
- [ ] Upload/publication/scheduling state is explicitly stated, never assumed.

## 18. Troubleshooting matrix

| Symptom | Likely causes to inspect | Useful correction |
| --- | --- | --- |
| Scene looks cartoonish | Scale, silhouettes, smooth roughness, poor light, fake depth | Reference comparison and material/geometry fixes before more samples |
| Leaves look rectangular | Card silhouettes/alpha, low resolution, lack of curvature | Better geometry/alpha asset, correct normals/transmission, camera-aware LOD |
| A trunk/post blocks the view | Unreviewed composition or procedural scatter | Move/resize/remove obstruction and recheck camera before detailing |
| Stone looks painted/plastic | Flat displacement, identical blocks, shallow mortar, wrong scale | Match real masonry, recess mortar, varied roughness and wear |
| Glass disappears or blocks everything | Wrong thickness/IOR, reflection/environment mismatch | Test pane/frame detail under final exposure and reflection angles |
| Rain cannot be seen | Wrong lighting/depth, thin streaks, excessive blur/denoise | Layer scales, improve light contrast and real shutter/streak behavior |
| Rain clears at the top | One drifting sheet or finite emission without recycling | Continuous births/wrap outside view; test late frames |
| Rain falls indoors | Missing shelter occlusion or wrong compositing masks | Roof/glass-aware geometry/masks and surface-specific effects |
| Water looks like an overlay | No bank contact, occlusion, reflections or changing shape | Geometry/simulation or a better justified composite, matching perspective |
| River is static or too fast | Wrong playback sampling, shader-only motion, inconsistent foam | Check actual scene scale; retime all water-dependent layers together |
| Turbulence seems pasted on | Uniform foam/no obstacle response | Rework fluid/contact mesh and local foam generation |
| Fire resembles fabric | Solid sheet mesh, wrong emission, no fuel/contact | Better licensed fire/VDB/simulation and integrated logs/embers/light |
| Flames/candles look oversized | Wrong scene scale/exposure, identical copies | Match wick/fuel scale, compact flame shape and restrained variation |
| Loop visibly jumps | Duplicate endpoint, phase mismatch, nonperiodic noise/cache | Fix frame accounting/state continuity and compare local seams |
| Denoise flickers | Insufficient temporal stability, fine alpha/rain loss | Improve samples/lighting/assets or denoising strategy, inspect motion |
| Soundtrack pumps | Over-compression, loud overlap, limiter working constantly | Rebalance sources, improve crossfades, reduce event peaks |
| Thunder is startling | Abrupt attack, excessive loudness/high frequency, too frequent | Softer source/tail, lower level, longer intervals; audition in context |
| Stream overwhelms rain | Layer gains/source perspective conflict | Lower/narrow/muffle stream appropriately and re-audition |
| Black transition kills audio | Picture fade reused for whole mux | Separate picture and final audio envelopes |
| Concat glitches/freezes | Header/SAR/time-base/GOP mismatch | Probe units, fix encoding compatibility or re-encode coherently |
| QA appears stuck | Full video decoded unnecessarily for audio scan | Use audio-only scan, report heartbeat and measured progress |
| Mac fails immediately | Wrong path, missing brew/Python/wheels, permissions, space | Read actual log, verify dependencies/platform, use quoted bash launcher |
| Local status is missing | Wrong folder or commands never started | Locate extracted kit; run setup; do not claim local work is running |
| Download says loading then fails | Unsupported workspace link, auth page, huge file/client limit | Verified public/authorized storage route, parts, or tested rebuild kit |
| Git works but upload fails | API/upload host policy, auth scope, asset limit | Diagnose network and auth separately; never print/re-request secrets blindly |
| Thumbnail text is wrong | Generative typography error or wrong version | Correct with permitted editing workflow and inspect every word again |
| Metadata credits are inconsistent | Preview sources copied into final worksheet | Derive attribution from actual final-version asset manifest |
| User cannot review anything | Files only exist in cloud or links are imagined | Publish to authorized accessible route and verify before asking review |

## 19. Reusable prompts and resume handoff

### Reference and composition prompt

```text
Read the project brief and this playbook. Research real photographs/video for
the architecture, materials, plants, lighting and weather. Record URLs and
separate research inspiration from reusable licensed assets. Analyze the supplied
reference's finer details. Produce a reference board and 1–3 camera compositions,
with an honest realism gap list. Do not start long rendering yet.
```

### Scene refinement prompt

```text
Refine the approved composition against real references. Prioritize camera scale,
plant silhouettes, material roughness/wetness, glass/reflections, construction
detail, contact and lighting. Use suitable existing licensed assets before weak
procedural substitutes. Deliver a native-resolution still and detail crops.
Identify exactly what is a concept image, a Blender render, or a hybrid plate.
```

### Motion prompt

```text
Animate the approved scene using the selected method. Implement continuously
replenishing weather, coherent exposed-plant wind, real contact/flow where
requested, and optional events from the brief. Create a short motion preview,
critical detail clips, and a repeat test. Compare loop seams to normal frame
changes and state simulation/compositing limits. Preserve the approved camera.
```

### Audio prompt

```text
Build the soundtrack from verified licensed natural recordings. Match the
listener position and agreed dominant bed/support/event balance. Inspect source
signals and audition what is available; do not claim numerical tests prove an
absence of speech. Deliver combined and solo preview clips, source/changes/credit
records, event timing, loudness/true-peak measurements, and limitations.
```

### Long-master prompt

```text
Read the approved previews, version configuration and manifests. Verify unit
compatibility, exact frame/sample arithmetic and source rights. Build an endurance
test covering intro, repeated motion, events, dark transition if applicable and
ending. After the authorized review gate, assemble the selected durations using
bounded-memory audio and compatible visual units. Save progress, resumable stages,
per-version QA and streamed checksums. Do not claim unique hours of animation if
the picture is a repeated loop. Do not upload/publish without authorization.
```

### Thumbnail prompt

```text
Create three actual finished thumbnail covers for each release version, based
on the approved scene. A: wide clear topic headline. B: closer focal subject,
minimal text. C: distinct composition/message. Use the required image editing
tool where applicable and retain generation provenance. Keep all claims accurate,
including duration and exact dark-screen timing. No invented subjects, lightning
if absent, or ad-free claims. Export compatible 1280×720 files under the chosen
platform limit, inspect every word at 320px width, and deliver individual files,
a labeled comparison sheet, manifest and verified ZIP/download links.
```

### YouTube details prompt

```text
Prepare complete copy-ready YouTube Studio details for every final version:
three checked title options, full description with actual source credits, accurate
chapters where useful, tags within limits, hashtags, pinned comment, thumbnail
file choices, audience/category/language/disclosure/license/remix/comment/ad
recommendations, private-upload checklist and scheduling fields. Use actual
channel/publication facts only. Flag unresolved URLs. Save a worksheet and separate
text files per version. Do not upload, publish or schedule unless authorized.
```

### Delivery prompt

```text
Verify the final files, sizes, hashes, QA and access route. Provide actual working
download links or an explicitly described tested alternative. If direct transfer
is blocked, diagnose the real host/auth/limit issue and offer authorized storage,
checksummed parts, or a local rebuild kit. Distinguish exact master transfer,
timeline rebuild and fresh Blender rendering. Document local prerequisites,
disk/time estimates, status/log paths and safe restart. Never claim to control
my Mac unless a connected tool actually provides that capability.
```

### Resume handoff template

```text
PROJECT:
GOAL AND CURRENT CONCEPT:
AUTHORITATIVE BRIEF / CONFIG PATHS:
CURRENT BRANCH / COMMIT / SOURCE FOLDER:
CURRENT EXECUTION MACHINE AND HARDWARE:
USER DECISIONS AND RELEVANT EXISTING AUTHORIZATIONS:
CANCELLED / OUT-OF-SCOPE WORK:
APPROVED STILL / MOTION / AUDIO / ENDURANCE LINKS:
VISUAL METHOD AND KNOWN LIMITS:
ACTUAL USED SOURCE ASSETS / LICENSE RECORDS:
VERSIONS / TOTAL DURATION / SCENE DURATION / FPS / RESOLUTION:
LAST VERIFIED COMPLETED STAGE:
RUNNING JOB: yes/no/unknown; PID/job ID; start; heartbeat; log path
COMPLETED OUTPUTS: real paths, bytes, hashes, accessible links
QA COVERAGE AND FAILURES:
THUMBNAILS / YOUTUBE DETAILS / DELIVERY STATE:
UPLOAD / PUBLICATION / SCHEDULING STATE:
BLOCKERS: exact error and next remedy, without secrets
SAFE RESUME COMMANDS AND CACHE INVALIDATION NOTES:
NEXT ACTION / NEXT REVIEW GATE:
```

An assistant should validate this handoff against actual files/tool access. Do not
restart completed work unnecessarily, repeat failed unchanged requests, or carry
over a claim that a worker is live without checking its current state.

## 20. Acceptance contract

The intended result is a coherent, convincing, restful ambience production with
traceable rights, observable progress and reviewable artifacts. Photorealism is
assessed visually against references, not proven by a renderer name, a large
sample count, or a generated image that happens to look photographic.

“Complete” means the agreed deliverables actually exist, their important checks
have passed, and the user has a verified way to obtain/review them. It does not
mean that a new chat has inherited tools, that a Mac job has started, that a public
release exists, or that YouTube has approved monetization.

Use the configured creative choices and current user instructions as the source
of truth. Keep optional effects optional. When a tool, asset, license, delivery
route or environment is unavailable, make the useful work concrete, report the
specific limitation, and provide the safest viable next path within the scope.
