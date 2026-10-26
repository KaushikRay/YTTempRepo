# Dressing and motion diagnostic

This is an initial two-second motion diagnostic, not completion of the richer
room-dressing request or a final quality video. It adds a narrow woven table
runner and uses the existing licensed fire movie with the scene's gentle key.
Fire credit remains assets/fire/CREDITS.txt (CC BY 3.0).

The diagnostic samples the 24 fps timeline every other frame and encodes at
12 fps, 640x360, 12 Cycles samples with denoising. It tests footage playback,
small leaf rotation and falling water. It has no audio and is not seamless.
The rain population translates rather than replenishing, so density can fall
at the upper window edge; this needs replacement before a finished animation.
Cloth placement and the primitive secondary props still need refinement.

The test is saved separately as dressing_motion.blend. Keep the assets folder
and linked vegetation library alongside it. Original still and storm files
are preserved. Reproduce with the bpy interpreter:

    OMP_NUM_THREADS=5 /workspace/tools/fire-venv/bin/python scripts/dressing_motion_pass.py

Future work: richer real tableware/food/textile assets, improved fuel/contact
integration, rain replenishment and a longer motion test at the approved quality.
