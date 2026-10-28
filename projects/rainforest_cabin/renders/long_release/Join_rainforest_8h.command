#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
test -f "rainforest_8h.mp4.part001" || { echo "Missing rainforest_8h.mp4.part001"; exit 1; }
test -f "rainforest_8h.mp4.part002" || { echo "Missing rainforest_8h.mp4.part002"; exit 1; }
test -f "rainforest_8h.mp4.part003" || { echo "Missing rainforest_8h.mp4.part003"; exit 1; }
shasum -a 256 -c rainforest_8h_parts.sha256
cat "rainforest_8h.mp4.part001" "rainforest_8h.mp4.part002" "rainforest_8h.mp4.part003" > "rainforest_8h.mp4.assembling"
echo "80803b5c78ea8f102ddb19988d412ed26228f43e94432c4734b46a60499436e0  rainforest_8h.mp4.assembling" | shasum -a 256 -c -
mv "rainforest_8h.mp4.assembling" "rainforest_8h.mp4"
echo "Verified master ready: rainforest_8h.mp4"
