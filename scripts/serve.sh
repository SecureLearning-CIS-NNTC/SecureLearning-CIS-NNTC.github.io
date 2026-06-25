#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-8000}"
HOST="127.0.0.1"

cd "$(dirname "$0")/.."
python3 scripts/build.py
echo "Serving Secure Learning site at http://${HOST}:${PORT}/"
python3 -m http.server "$PORT" --bind "$HOST"
