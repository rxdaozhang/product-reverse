# AGENTS.md

Guidance for AI coding agents working in this repository.

## Repository Purpose

This repository publishes a reusable agent skill: `product-reverse`.
The skill helps reverse-engineer web products from a URL and produce structured outputs.

## Canonical Skill Source

- Skill name: `product-reverse`
- Skill file: `skills/product-reverse/SKILL.md`
- Repository source id: `rxdaozhang/product-reverse`

## Repository Layout

```text
.
├── skills/
│   └── product-reverse/
│       ├── SKILL.md
│       ├── references/
│       └── scripts/
├── .well-known/
│   └── skills/
│       └── index.json
└── scripts/
    ├── validate-skill.sh
    └── smoke-install.sh
```

## Quality Gates

Run both checks before committing:

```bash
bash scripts/validate-skill.sh
bash scripts/smoke-install.sh
```

## Publishing Contract

Public install commands must stay valid:

```bash
npx skills add rxdaozhang/product-reverse
npx skills add rxdaozhang/product-reverse --skill product-reverse
```

When changing skill name/path, update all of:

- `skills/product-reverse/SKILL.md`
- `.well-known/skills/index.json`
- `README.md`
- validation scripts
