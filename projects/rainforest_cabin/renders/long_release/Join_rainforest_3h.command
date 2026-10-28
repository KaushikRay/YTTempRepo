#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
test -f "rainforest_3h.mp4.part001" || { echo "Missing rainforest_3h.mp4.part001"; exit 1; }
test -f "rainforest_3h.mp4.part002" || { echo "Missing rainforest_3h.mp4.part002"; exit 1; }
test -f "rainforest_3h.mp4.part003" || { echo "Missing rainforest_3h.mp4.part003"; exit 1; }
test -f "rainforest_3h.mp4.part004" || { echo "Missing rainforest_3h.mp4.part004"; exit 1; }
test -f "rainforest_3h.mp4.part005" || { echo "Missing rainforest_3h.mp4.part005"; exit 1; }
test -f "rainforest_3h.mp4.part006" || { echo "Missing rainforest_3h.mp4.part006"; exit 1; }
shasum -a 256 -c rainforest_3h_parts.sha256
cat "rainforest_3h.mp4.part001" "rainforest_3h.mp4.part002" "rainforest_3h.mp4.part003" "rainforest_3h.mp4.part004" "rainforest_3h.mp4.part005" "rainforest_3h.mp4.part006" > "rainforest_3h.mp4.assembling"
echo "5a16a78e8df27495c55a076d3b74fa9418005dfc6bd1fd0c70c89a8f0d323b06  rainforest_3h.mp4.assembling" | shasum -a 256 -c -
mv "rainforest_3h.mp4.assembling" "rainforest_3h.mp4"
echo "Verified master ready: rainforest_3h.mp4"
