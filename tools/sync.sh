#!/usr/bin/env bash
# Regenera paleta, iconos y colores del manifest desde img/background.png
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
python3 tools/extract_palette.py
python3 tools/build_icons.py
python3 tools/apply_palette.py
echo "Theme assets synced."
