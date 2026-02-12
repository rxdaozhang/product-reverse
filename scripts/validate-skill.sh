#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILL_MD="$ROOT_DIR/skills/product-reverse/SKILL.md"
INDEX_JSON="$ROOT_DIR/.well-known/skills/index.json"

echo "[validate] checking required files..."
test -f "$SKILL_MD"
test -f "$INDEX_JSON"

echo "[validate] checking SKILL.md frontmatter fields..."
rg -q '^name:\s*product-reverse\s*$' "$SKILL_MD"
rg -q '^description:\s*.+$' "$SKILL_MD"

echo "[validate] checking .well-known index schema..."
node - "$INDEX_JSON" <<'NODE'
const fs = require("fs");
const indexPath = process.argv[2];
const data = JSON.parse(fs.readFileSync(indexPath, "utf8"));

function assert(cond, msg) {
  if (!cond) {
    throw new Error(msg);
  }
}

assert(data.source === "rxdaozhang/product-reverse", "invalid source");
assert(data.homepage === "https://github.com/rxdaozhang/product-reverse", "invalid homepage");
assert(Array.isArray(data.skills), "skills must be an array");

const skill = data.skills.find((s) => s.name === "product-reverse");
assert(skill, "missing product-reverse skill entry");
assert(skill.path === "skills/product-reverse/SKILL.md", "invalid skill path");

assert(data.install && typeof data.install === "object", "missing install object");
assert(
  data.install.all === "npx skills add rxdaozhang/product-reverse",
  "invalid install.all"
);
assert(
  data.install.single === "npx skills add rxdaozhang/product-reverse --skill product-reverse",
  "invalid install.single"
);
NODE

echo "[validate] all checks passed."
