# Historic reference study and construction revision

## Sources actually inspected

Google search and the attempted Haddon Hall, Weald & Downland and National
Trust pages returned proxy 403 errors. They were not read. The attempts are
recorded in `research/historic_interiors/sources.json`. Wikimedia Commons API
search and original photograph downloads worked. The following photographs
were opened and visually inspected:

| Photograph | Visible construction cues | Application in this scene |
| --- | --- | --- |
| [Gainsborough Old Hall kitchen fireplace, Richard Croft](https://commons.wikimedia.org/wiki/File:Medieval_fireplace_-_geograph.org.uk_-_531926.jpg) | Very broad, deeply recessed brick hearth; darkened brickwork, substantial lintel, irregular brick floor; heavy tables and benches | A deeper masonry fireback, individual brick joints, dark side returns and ash at the fuel bed; restrained hearth lighting |
| [Penshurst Place Baron's Hall, Marathon](https://commons.wikimedia.org/wiki/File:In_the_Baron%27s_Hall_at_Penshurst_Place_-_geograph.org.uk_-_5460448.jpg) | Deep stone window reveals with block joints; plastered wall fields, timber screen/panelling, trestle tables/benches, large clear floor area | Deep, squared jambs and separate arch voussoirs instead of tubular trim; wide stone sills; believable physical furniture scale |
| [Penshurst chestnut roof, Michael Garlick](https://commons.wikimedia.org/wiki/File:Penshurst_Place%2C_Baron%27s_Hall%2C_The_magnificent_chestnut_roof_1_-_geograph.org.uk_-_5767117.jpg) | Hierarchy of major posts, curved braces, longitudinal members and many smaller rafters; weathering follows real members | Construction reference for future roof refinement; a complete roof reconstruction is not claimed in this still |

These are present-day photographs of historic buildings, including later
alterations, restoration, displays and furnishings. They are visual evidence
of visible construction, not proof that every photographed detail dates to
1400. A great hall or kitchen is not a direct documentary reference for an
inn parlour. The original supplied image remains the composition/mood target.

The three original photographs are retained for study with full attribution
and CC BY-SA 2.0 licence links in `research/historic_interiors/photo-credits.json`.
They were not used as render textures or composited into the image.

## Changes implemented

- Replace the regular block texture with CC0 Old Stone Wall 02 and Rustic
  Stone Wall 02, at a smaller physical scale. Add modest surface relief.
- Replace round pipe-like lancet surrounds with deep dressed-stone jamb
  courses and individually jointed arch blocks. Add broad, projecting sills.
- Attach sconces to visible iron mounting plates and projecting arms.
- Add a sooted, individually jointed brick fireback, side returns, throat and
  ash bed. Reduce the broad orange lighting wash. Integrate the original RGB
  fire frame with spatial feathering and a gentle linear-light key, preserving
  its logs and dim orange wisps. A wide unkeyed photo blend was tested and
  rejected because it left a visible reddish rectangle.
  This remains a photographic integration for a fixed camera, not a fire simulation.
- Use the CC0 Sofa 03 with 4K PBR maps for worn leather and carved seating;
  retain a secondary scanned chair. Replace the floral jug with a wooden bowl.
  Add scanned wooden stool and wicker basket, all CC0 from Poly Haven.
- Add restrained, fine rain geometry beyond the glass. This is a still
  visibility study, not a validated new animated storm sequence.

The original procedural settle was rejected after diagnostic rendering because
it did not meet the inviting, realistic furniture target. The accessible
catalogue supplied no convincing period settle. The replacement sofa is
explicitly Victorian according to the provider. Together with the existing
upholstered chair and coffee table, it is a deliberate comfort/mood concession.
This is a historically inspired Gothic retreat, not an archaeological replica
of a medieval tavern. Architectural reference and furniture dating are kept
separate rather than presenting a later sofa as medieval.

## Assets and licensing

Poly Haven assets are CC0. Original file API manifests and provider MD5 values
are retained in `assets/realism/`; downloaded bytes were verified before use.
See `historic-assets-provenance.json`, `sofa_03-info.json`, the existing
`provenance.json` and retained licence page. The filmed fire remains CC BY 3.0
with required attribution in `assets/fire/CREDITS.txt`.

## Reproduction

`scripts/realism_rebuild.py` loads the preserved original storm scene, applies
the existing asset pass and then `scripts/historic_detail_pass.py`. This
rebuilds deterministically rather than repeatedly transforming the saved
result. It updates the existing `realism_study.blend` and
`renders/realism_study.png`. The original `storm_lounge.blend` is preserved.

```sh
OMP_NUM_THREADS=5 REALISM_PERCENT=100 REALISM_SAMPLES=96 \
  /workspace/tools/fire-venv/bin/python scripts/render_realism_supervised.py
```

Keep the complete `assets/` directory beside the Blender file. Most textures
are packed; the unmodified old/rustic stone and worn wood maps remain relative
external files to stay within GitHub's individual file size limit. The render
supervisor records live local progress in `renders/realism_status.json` and
distinguishes a completed render from the known native bpy cleanup stall.

## Quality limits

The full-size 1280 × 720 / 96-sample render was inspected against the original
reference side by side (`renders/realism_comparison.png`: reference left,
new render right). The revised sofa and stone joints are stronger, but the
reference has much richer foreground dressing, more naturally varied light,
denser exterior layers and less obviously constructed surfaces. Fine rain
geometry is present but still too subtle to sell a heavy storm in this image.
No claim is made that the photorealism target has been reached.

The exterior village still needs detailed assets and atmospheric depth. The
fire is filmed footage on a card, so it is suitable only for the fixed review
camera, and its matte/light integration still needs refinement. The room is
still less richly dressed than the original reference. Deep joints, PBR maps
and more samples alone cannot establish photorealism. Inspect the actual
render before any expensive animation; this revision is a still, not a new
video or final quality approval.

Delivery check: 41 used file images are packed, nine large PBR maps resolve as
relative external files, and no used file image is missing. The saved Blender
file is below GitHub's 100 MiB limit. The original motion scene's Git content
hash matches the previous delivery. Runtime outcome, including the known
post-render native cleanup stall and its termination after completion, is
recorded separately in `renders/realism_runtime.json`.
