#!/usr/bin/env sh
set -eu
PORT="${1:-8000}"
printf 'MethaNor: http://localhost:%s\n' "$PORT"
python3 -m http.server "$PORT"
