# Rebuild the approved videos on a Mac

This package assembles the approved pre-rendered animation and rebuilds the long
rain/stream/thunder soundtrack locally. It does not run Blender or simulate new
water. Picture units are copied without re-encoding, including the approved
darker grade, intro badge, slow river and fade to black. Audio is rebuilt from
the licensed full recordings. Different FFmpeg/CPU versions can change the
encoded audio and final MP4 checksum; these are equivalent timeline rebuilds,
not promised byte-identical downloads of the cloud masters.

## Start

1. Download `Rainforest_Mac_Rebuild.zip` and extract it. Move its
   `RainforestCabin` folder into your home `Movies` folder in Finder.
2. Install Homebrew from <https://brew.sh> if you do not already have it.
   This package installs FFmpeg, Python 3.12 and a private Python environment
   with NumPy, SciPy and Pillow. Blender is not needed. Keep at least 25 GiB free;
   30 GB or more is recommended. Both Apple silicon and Intel Macs are intended;
   Homebrew support for your macOS version is also required.
3. In Terminal, run:

   ```sh
   bash "$HOME/Movies/RainforestCabin/1_Setup.command"
   ```

   This verifies package checksums and downloads about 85 MB of original rain
   and stream recordings directly from Wikimedia, checking their SHA256 hashes.
   No GitHub API, cloud credentials, paid assets or extra video download is needed.

## Run each next step

Double-click the numbered commands, in order. If macOS does not allow a command
to launch, run it explicitly in Terminal with `bash`, as above; do not disable
Gatekeeper. All command contents are plain text and can be reviewed first.

- `2_Preview.command`: build a 15-minute local test: twelve minutes of scene
  then three minutes dark, with continuous audio. Review
  `renders/long_release/endurance.mp4` before the full build.
- `3_Build_Both.command`: produce both full videos. The terminal reports completed
  minutes and a running estimate while audio builds. Keep it open. The Mac is
  kept awake during the job. This can take tens of minutes to several hours;
  no Mac benchmark has been measured for this kit.
- `4_Check_Videos.command`: measure all eleven hours of audio and check video
  timing, selected frames, joins and endings. This can take a substantial amount
  of time; video is sampled, not exhaustively decoded or watched. Listen and
  review the outputs yourself before publication.

Outputs (hard links to the built masters, without a second disk copy):

- `youtube/3h/rainforest_3h.mp4`: 1080p, 24 fps, scene throughout three hours.
- `youtube/8h/rainforest_8h.mp4`: 1080p, 24 fps, one hour of scene then seven
  hours black, sound continuing.

Expected output sizes are around 9.5 GB and 4 GB, respectively. Nothing uploads
to YouTube or any other service. The visual repeats the approved twelve-second
hybrid loop; this is not eleven hours of unique animation.

## Progress and recovery

Read the live Terminal output, `status.json`, or `logs/mac_<stage>.log`.
No work runs after these local processes exit. Close the Terminal or press
Control-C to stop the foreground build. Completed audio/video stages are reused;
a partially interrupted audio stage restarts from its beginning. Do not run two
stages simultaneously. Do not edit or delete files inside the package while
building. If a running estimate is unavailable during muxing or QA, the current
stage is still printed; it is not a claim of a percentage-based progress bar.

License credits are in `renders/long_release/AUDIO_CREDITS.txt`. Include those
credits when publishing. A fresh Blender scene render is a separate workflow
and requires the scene, caches and Blender-compatible dependencies.
