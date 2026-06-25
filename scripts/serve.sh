#!/usr/bin/env bash
set -euo pipefail

PORT="${1:-8000}"
HOST="127.0.0.1"

cd "$(dirname "$0")/.."
echo "Serving Secure Learning site with Jekyll at http://${HOST}:${PORT}/"
bundle exec jekyll serve --host "$HOST" --port "$PORT"
