# Fitted 3D river in the approved cabin view

The user approved the standalone 3D liquid test and asked to proceed carefully
with integration. This revision preserves the approved cabin, composition,
foreground palms and rain while replacing the image-based river motion with
actual simulated liquid geometry. It is still a locked-camera photographic
hybrid; the cabin and most forest detail remain generated static imagery.

## What changed

The new river is simulated in a varying-width, gently curved 7.8 m channel fitted
to the approved image. A perspective camera and five proxy collision rocks were
estimated from visible stream/rock correspondences. This is an approximate
single-image camera/scale reconstruction, not measured real-world geometry.
The inlet extends two metres upstream behind the existing bank so the visible
water does not begin at a clipped mesh boundary.

An original Taichi CPU position-based liquid solver produces gravity-driven
surface meshes. The particle pool contains 82,154 particles; approximately 35,700
are active in the channel during the delivered interval, with the remainder
waiting at the inlet. Eight substeps per 24 fps frame and six pressure iterations
are used. The first four seconds settle the flow; the next four seconds are
rendered as 96 distinct native Blender frames at 1920×1080.

Inlet particles enter only available, above-bed slots. Steep bank collisions
project along the surface normal. These replace random reinsertion and vertical
bank corrections that caused excessive spray in rejected setup tests. The
delivered flow is continuous, with sampled mean downstream velocity about 2 m/s.
Surface foam and small 3D bubbles derive from particle motion. Foam remains an
empirical field, not a two-phase air/water simulation or validated CFD solution.

The small upstream glimpse is a spatial instance of the same liquid bake in an
estimated distant pose. It is not claimed to be a second independent simulation.
The main water material uses refraction, absorption, simulated normals/foam and
small procedural micro-roughness; it uses no water photograph, movie or UV flow.

## Image integration

The approved palm and rain objects are reprojected onto the calibrated camera
without changing their local geometry, shape keys or drivers. Original pixels
outside the rerendered lower border are reused losslessly from the approved
native frame cache. A rebuild without that cache renders complete full frames.
There is no generated video or frame interpolation.

Photographic bank proxies use the original rock texture and soft edges to handle
occlusion. A generated static, water-free creek-bed texture removes frozen foam
behind refractive liquid. That image is used only in the creek cleanup footprint
and as the underlying bed; it is not a replacement cabin/palm background or a
source of animated water. Its provenance is in `assets/integrated_fluid`.

The liquid reflects the CC0 rainforest HDRI and soft cool/warm area lights.
Camera-only image layers do not act as luminous panels in secondary rays. A
liquid-object mask applies an HDR highlight shoulder to the water while keeping
the already graded photographic backdrop unchanged.

## Review priorities and remaining limits

Inspect the full-frame clip and the native 1040×400 river crop. Check rock
contacts, the hidden inlet, highlight/foam detail and the smaller upstream
instance. Camera-projected banks remain an approximation and can expose matte
edges on close inspection. Some source rock/bank highlights are static. The 2 cm
surface reconstruction is not a final close-up fluid resolution. No claim of
finished photographic realism is made by passing the numerical checks.

This is a silent four-second moving review. It is not yet a seamless long video.
The next production stages are visual corrections from this review, loop design,
and a rain/stream/thunder soundtrack before the long YouTube build.

## Source and rebuild

`rainforest_integrated_fluid.blend` contains the integrated scene. Keep the four
`assets/integrated_fluid/fluid_cache_*.zip` files beside the project. The embedded
`ENABLE_INTEGRATED_FLUID_PLAYBACK.py` text enables cached mesh playback when run
once inside Blender; bpy, NumPy and SciPy are required by the helper/environment.

```sh
FLUID_VARIANT=integrated_fluid python scripts/simulate_fluid_river.py
SAMPLES=32 WIDTH=1920 python scripts/render_integrated_fluid.py
python scripts/package_integrated_fluid.py
python scripts/check_integrated_fluid.py
python scripts/check_integrated_scene.py
```

The committed channel/camera JSON and upstream pose are the calibrated inputs.
`fit_integrated_channel.py` retains the centreline fit and upstream extension
construction. Shader settings, particle snapshots for contact checks and cache
checksums are retained for review. Raw solver caches and native PNGs stay ignored.

## Completed checks

Both clips decode cleanly with 96 distinct frames at 24 fps / four seconds.
All 96 simulated geometry states are distinct. Sampled particles remain above
the fitted bed and outside the rock shells, with downstream velocity about
2 m/s. Five native-frame comparisons show zero changed pixels outside the river
render border. The palm geometry/driver fingerprint matches the approved
revision and its maximum screen projection error is below 0.001 pixel.
A relocated scene plays the changing liquid and foam geometry from the four
ZIP archives. The water material has zero image textures and the scene uses
zero movie images. These checks establish delivery and method integrity, not
perceptual photographic realism. Reports accompany the preview and scene.
