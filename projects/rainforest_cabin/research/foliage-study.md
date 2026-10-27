# Photograph-led foliage correction

## Real references inspected

`forest_photographs/reference_board.jpg` collects 14 real photographs: Daintree
understory/canopy, Koh Chang tropical forest, Dominica ferns, Peruvian layered
vegetation, coconut leaf anatomy, wet leaf droplets, Mossman/Guyana stream banks
and whole palm fronds/crowns. Source URLs, photographers, licences and downloaded
file hashes are in `forest_photographs/sources.json` and `CREDITS.md`.

These photographs guide anatomy, placement and materials. The original chat image
continues to guide the night composition. No reference photograph is a texture
in the Blender scene. Several photographs are CC BY/CC BY-SA; they are distinct
from the CC0 Poly Haven assets used in the render.

| Photographic evidence | Change |
| --- | --- |
| Ferns have fine gaps between individual leaflets. | Restore the separately supplied scan masks: the previous JPEG colour maps had alpha=1 everywhere. |
| Broadleaf outlines curve and taper independently of the carrier mesh. | Use 4K masks, colour, normal and roughness maps for fern, calathea, anthurium and shrub materials. |
| Canopies have gaps between leaves. | Add the dedicated masks to pachira and island-tree leaf materials too. |
| Palm pinnae have offset insertions and vary in length, orientation and wear. | Rebuild 51 fronds with staggered insertion, lanceolate blades, individual twist/droop, small gaps and occasional edge damage. |
| Palm blades have a soft folded section and thin tips. | Use 25 longitudinal / 7 transverse samples per pinna, smooth shading and a shallow folded section. |
| Wet leaves have localized highlights and variable sheen. | Raise base roughness, reduce uniform clearcoat and retain photographic normal/roughness variation. |
| Trunks have bark texture, taper and lean. | Replace earlier poorly mapped cylinders/square trunks with round, smoothly shaded, UV-mapped geometry. |
| Greens remain visible under cool light. | Make the key/fill less saturated blue, retaining the distant cool rain light and warm lantern. |

## Controlled inspection

`renders/leaf_comparison.jpg` shows the same three plant specimens at the same
camera, scale and neutral lighting. The top uses original published libraries from
commit `deb72532749b85bd77425fa9cb18279e664a94aa`; the bottom uses the corrected
libraries. The before fern's broad solid strips resolve into separate pinnae after
the correction. Broadleaf masks improve the outline more subtly. Higher-resolution
maps and material changes are included; this is not an alpha-only measurement.

The full-size night render was inspected separately. The lower ferns now have
visible gaps, and the right palms have finer curved blades instead of the original
wide strips. Raising sample counts alone would not have fixed the opaque cards.

## Remaining limits

Palms remain original geometry informed by photographs, not complete scanned palm
assets. Individual water-bead geometry and wind have not been added. The cabin,
steps and stream still need surface/shape detail. This pass addresses foliage;
the full ultra-realism target is not declared achieved. No moving test is included.
