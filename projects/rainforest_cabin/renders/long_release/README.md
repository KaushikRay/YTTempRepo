# Long rainforest masters

[Two-minute endurance review excerpt](review_excerpt.mp4)

The excerpt shows: 0:00–0:20 the actual opening; 0:20–1:00 source endurance
01:05–01:45 with a distant rumble; 1:00–2:00 source endurance 11:15–12:15,
including the fade to black and continuing sound. The excerpt contains deliberate
review cuts; those cuts do not occur in the masters.

Both masters retain the approved darker forest/cabin view, 80% river playback,
rain-led audio and a quiet stream. No visual lightning is added. A calm one-time
subscribe reminder appears from 0:06 to 0:14 after the picture fades in.

- `rainforest_3h.mp4`: exactly three hours, scene throughout, final 20 s fade.
- `rainforest_8h.mp4`: exactly eight hours, one hour of scene then seven hours
  of black picture with sound continuing; final 20 s audio fade.

Full master MP4s are too large for ordinary Git files and are not committed.
SHA256s, durations, file sizes and technical QA are recorded here. A delivery
manifest and joining helpers describe release-asset parts without changing the
MP4 data. The actual delivery status will be updated after upload access is tested.

The sound uses randomized natural-source grains with 3 s equal-power overlaps,
referenced to the approved rain/stream levels, plus distant thunder every roughly
2.5–4 minutes. Thunder is quieter during the long black-screen portion. It uses
one licensed thunder recording with four processing variations, not four unique
recordings. Sources were screened technically; this is not a claim of exhaustive
human audition of eleven hours.

The image is a repeated twelve-second hybrid loop, not hours of unique animation.
Existing generated-backdrop, approximate-bank and glossy-water limits remain.

Rebuild:

```sh
python scripts/fetch_long_sources.py
python scripts/prepare_long_release.py
python scripts/build_long_release.py
python scripts/check_long_release.py
python scripts/prepare_master_delivery.py
```

Use the provided source credits for public distribution. No YouTube upload or
public release has been performed by these build scripts.

## Current download blocker

Both masters are built and passed their audio scans and sampled-video checks.
Full-file upload is pending: the current cloud allowlist blocks `api.github.com`
and `uploads.github.com`. A draft was saved adding just those domains. General
network permission alone did not remove the proxy block. Review/save the network
change in environment settings and publish the environment; then retry the API.

After access works, `python scripts/upload_long_masters.py` uploads checksum-
verified 1.8 GB transport parts and joining helpers to a **draft** release. It does
not publish the release or upload to YouTube. Every remote part must have the
expected GitHub SHA256 digest before its temporary local copy is removed. The
full master MP4s are retained. API authorization remains to be tested after the
network change; successful ordinary Git access alone does not prove API access.
