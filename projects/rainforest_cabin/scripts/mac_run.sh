#!/bin/bash
set -euo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STAGE="${1:?Missing stage}"
mkdir -p "$ROOT/logs"
exec > >(tee -a "$ROOT/logs/mac_${STAGE}.log") 2>&1
echo "Started $STAGE: $(date)"
trap 'result=$?; if [ "$result" -ne 0 ]; then echo "Stopped. See logs/mac_'"$STAGE"'.log for the error."; fi' EXIT
if ! command -v brew >/dev/null; then
  echo "Install Homebrew from https://brew.sh, then run this step again."
  exit 1
fi
if [ "$STAGE" = setup ]; then
  brew install ffmpeg python@3.12
fi
PYTHON="$(brew --prefix python@3.12)/bin/python3.12"
test -x "$PYTHON" || { echo "Run 1_Setup.command first."; exit 1; }
command -v ffmpeg >/dev/null
command -v ffprobe >/dev/null
if [ "$STAGE" = setup ]; then
  "$PYTHON" -m venv "$ROOT/.venv"
  "$ROOT/.venv/bin/python" -m pip install -r "$ROOT/requirements-mac.txt"
fi
test -x "$ROOT/.venv/bin/python" || { echo "Run 1_Setup.command first."; exit 1; }
cd "$ROOT"
# caffeinate prevents idle sleep only for this foreground job.
if command -v caffeinate >/dev/null; then
  caffeinate -i "$ROOT/.venv/bin/python" -u scripts/mac_build.py "$STAGE"
else
  "$ROOT/.venv/bin/python" -u scripts/mac_build.py "$STAGE"
fi
echo "Finished $STAGE: $(date)"
