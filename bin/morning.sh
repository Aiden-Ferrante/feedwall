#!/usr/bin/env bash
# feedwall morning run: score the overnight firehose, then post the briefing.
# Invoked by the feedwall-briefing systemd --user timer (~06:45).
set -euo pipefail
cd "$(dirname "$0")/.."

python3 -m brain run --limit 250 --hours 36
python3 -m briefing.render --hours 24
