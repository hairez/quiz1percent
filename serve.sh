#!/usr/bin/env bash
# Start the practice quiz on http://localhost:3003.
# Stop with Ctrl-C.
set -euo pipefail
cd "$(dirname "$0")"
PORT="${PORT:-3003}"
echo "Serving at http://localhost:${PORT}/"
exec python3 -m http.server "${PORT}" --directory public
