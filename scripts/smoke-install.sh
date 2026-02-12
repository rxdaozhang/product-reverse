#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[smoke] listing skills from local repository..."
OUTPUT="$(npx --yes skills add . --list 2>&1)"
echo "$OUTPUT"

echo "[smoke] asserting product-reverse is discoverable..."
echo "$OUTPUT" | rg -q 'product-reverse'

echo "[smoke] discoverability check passed."
