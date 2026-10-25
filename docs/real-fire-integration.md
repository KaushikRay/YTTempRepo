# Downloaded real-fire asset and still integration

BlenderKit and JangaFX searches were attempted, but their hosts remained
blocked at the time of the search. Network access additions were saved in
the environment draft; that save does not establish runtime access/publication.
Wikimedia Commons responded successfully with an identified research client.

A CC0 640 × 640 hotel-fireplace clip was downloaded and rejected because it
has a mesh screen in front of the fire. It is not part of the delivered asset.

Selected: "Fantastic-fireplace-fire-chimney-hearth- background - texture -
motion graphics - free video library", attributed to **free video library**,
via Wikimedia Commons, listed under **CC BY 3.0**. Commercial reuse is allowed
with attribution and an indication of modifications. Exact source/download
URLs, author, licence, original checksum and still timestamp are recorded in
`assets/fire/source.json`. The unmodified Commons metadata is retained as
`assets/fire/source-commons-metadata.json`. Attribution is in
`assets/fire/CREDITS.txt` and embedded in the Blender file.

The downloaded original is `source.webm`: 1920 × 1080. It was converted to a
silent 30 fps / 900-frame MP4 for later animation work. The still uses the frame
at 2 seconds, keyed using temporal median background subtraction on the green channel,
a bright flame-core mask, and a small median filter to suppress the
stationary red-lit wall and compression speckles. Reproduce
with `scripts/prepare_fire_asset.py`. The original is retained unmodified.

The keyed PNG is placed on a transparent emitting card behind the hearth grate.
Its aspect ratio is preserved, and it is packed into `storm_lounge.blend`.
The old procedural hearth flames and glowing oval embers are not used.

This is real downloaded fire footage integrated into a Blender render, **not a 3D
fire simulation or imported native VDB**. It is intended for a fixed camera;
large viewpoint changes can expose the image-card nature. The video is retained
but only a still is integrated in this revision. No animation or seamless-loop
validation is claimed. No soundtrack is included.

Validation: final room image rendered at 1280 × 720 / 64 samples with
OpenImageDenoise; hearth detail rendered at 960 × 720 / 64 samples in 1 min
44 sec. Both inspected. Temporal matte removes the red stationary background
speckles from the rejected colour-key test. It still trims some dim orange
wisps and is not a finished cinematic composite. The source is video footage,
not a native 3D fire asset; no animated flame integration is claimed.
