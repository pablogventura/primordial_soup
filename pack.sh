#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

VERSION="$(python3 -c "import json; print(json.load(open('manifest.json'))['version'])")"
DIST="$ROOT/dist"
XPI="$DIST/primordial-soup-${VERSION}.xpi"

mkdir -p "$DIST"
rm -f "$XPI"

zip -r "$XPI" \
  manifest.json \
  _locales \
  img \
  icons \
  LICENSE \
  COPYING \
  -x "*.git*" "__MACOSX/*" ".DS_Store"

echo "Built $XPI ($(du -h "$XPI" | cut -f1))"
