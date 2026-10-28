# Revised river loop: water at 80% speed

[Full-quality silent loop](../../renders/looped_fluid/preview.mp4)
· [River crop](../../renders/looped_fluid/river_detail.mp4)
· [Two-repeat test](../../renders/looped_fluid/repeat_test.mp4)
· [Current changes, checks and source instructions](../production_test/review.md)

The 12-second / 1080p / 24 fps loop now uses a fresh 30 fps water bake, displayed
at 24 fps, to reduce river motion by 20%. Rain and palms keep their approved speed.
The particles and meshes are new native simulation states; the earlier water
video was not slowed by duplicating frames or interpolating rendered images.

The river border is rerendered at the original pixel density and 32-sample cap.
Matching native pixels elsewhere preserve the approved view. The first second
still uses a remeshed 3D scalar-field transition; this is an artistic loop rather
than periodic physics. Source: `rainforest_looped_fluid.blend` and the twelve
relative cache ZIPs in `assets/looped_fluid`. Run the embedded playback script.

The cabin/forest remain a generated static photographic-style backdrop. Coarse,
glossy water, approximate photographed bank geometry and reused upstream water
are continuing limits. The current longer audiovisual test and QA are linked above.
