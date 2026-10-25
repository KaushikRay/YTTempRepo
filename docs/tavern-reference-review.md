# Rustic tavern / reference stonework review

## Observed in the supplied reference

The side wall and chimney contain grey-brown, roughly dressed stone in
horizontal courses. Block widths vary; faces have chipped edges, shallow
fractures and mineral mottling. Joints are irregular and mostly shallow,
with softened mortar rather than a clean black grid. Soot darkens the hearth
and some upper surfaces. Thick architectural surrounds are smoother than
ordinary wall blocks. The overall room is heavily dressed and worn, with
textiles, food, firewood, greenery and many small practical objects.

The reference is still more detailed and less regular than our generated
scene. It does not establish any exact historical date or animation behavior.

## This revision

- Replaced the regular side/back masonry with varied course heights, widths,
  chamfered corners and non-planar stone faces; mortar is narrower and lighter.
- Reoriented side stones so chipped front faces, rather than flat backs, face
  the interior. Added soot staining to the chimney.
- Removed modern leather lounge seating. Added heavy matte oak benches,
  a trestle base, ale casks, firewood, iron hooks/cookware, straw and debris.
- Added dense wind-driven rain near the glass, reflective rivulets and droplets,
  with more window illumination. Rain visibility must be judged in the still
  and later in a motion test; extra rendering alone cannot create missing rain.
- Removed the rejected procedural hearth flames entirely.

## Real-fire asset: blocked, not complete

User explicitly requested downloaded real fire. No other hand-built flame
is substituted. The current scene contains logs and embers only. A movie
integration path is prepared for assets/fire/fire.mp4 plus source.json with
source_url, license_url, commercial_use_verified and frame_count. No movie
was loaded, and that integration path is not functionally validated yet.

Wikimedia Commons, Pexels and Poly Haven requests returned network-proxy
403 responses. GitHub searches were accessible, but no suitable real-fire
footage with established reusable licensing was found; a fireplace app's
README explicitly omitted its movie for copyright reasons. It was not used.

A network configuration draft was saved adding the required Commons,
Wikimedia upload, Pexels and Poly Haven hostnames, preserving the selected
package-manager presets. The configuration tool returned requires_publish.
The user must review/save settings and publish the environment; the draft
save itself does not change runtime access. Retry downloads after access
changes, select a real flame clip suitable for keying, verify the asset licence,
retain its provenance, then integrate and render-check it. Do not call this
fire task complete before that work is done.

The earlier candle close-up belongs to the preceding lounge iteration.

Final checks: full-room render at 1280 × 720 / 48 samples completed;
960 × 720 / 64-sample masonry detail completed in 1 min 50 sec.
Both denoised images inspected. Corrected mortar depth is visible; rain
is readable in the still. The reference remains more detailed and natural.
No real-fire footage or animation validation is claimed.
