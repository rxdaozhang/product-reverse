# product-reverse

`product-reverse` is an agent skill for reverse-engineering web products from a URL.

`product-reverse` 是一个面向 AI agent 的技能，用于从 URL 逆向分析 Web 产品。

## Project Positioning | 项目定位

This repository publishes a single production-ready skill: `product-reverse`.
It is designed for Claude/Codex-style agents to analyze product UX, infer API/data patterns, and output actionable build docs.

本仓库发布一个可直接使用的单技能：`product-reverse`。
它用于帮助 Claude/Codex 类 agent 分析产品体验、推断 API/数据模型，并生成可落地的实现文档。

## Quick Install | 快速安装

Install from the current repository:

```bash
npx skills add rxdaozhang/product-reverse
```

Install only this skill explicitly:

```bash
npx skills add rxdaozhang/product-reverse --skill product-reverse
```

## Usage Examples | 使用示例

- "Analyze this product and tell me how it works."
- "Reverse engineer this site."
- "Help me clone this product."

可用中文示例：

- “分析这个产品的交互和技术栈”
- “帮我逆向这个网站并输出设计文档”

## Repository Structure | 仓库结构

```text
.
├── AGENTS.md
├── .well-known/skills/index.json
├── skills/
│   └── product-reverse/
│       ├── SKILL.md
│       ├── references/
│       │   ├── chrome-patterns.md
│       │   ├── design-doc-template.md
│       │   └── report-template.md
│       └── scripts/
│           └── summarize_state.py
└── scripts/
    ├── validate-skill.sh
    └── smoke-install.sh
```

## Directory Compatibility | 收录兼容说明

This repo is aligned with common ecosystem expectations:

- `skills.sh` / `npx skills` discovery (`SKILL.md` with `name` + `description`)
- repository-level agent guidance (`AGENTS.md`)
- machine-readable discovery endpoint (`.well-known/skills/index.json`)

该仓库已对齐主流收录需求：

- 兼容 `skills.sh` / `npx skills` 的技能发现机制
- 提供仓库级 agent 说明入口（`AGENTS.md`）
- 提供可机器读取的索引（`.well-known/skills/index.json`）

## Quality Checks | 质量校验

```bash
bash scripts/validate-skill.sh
bash scripts/smoke-install.sh
```

## Contribution & Release | 贡献与发布

- Keep skill name and path stable unless there is a breaking-change plan.
- If changing discovery metadata, update `README.md`, `AGENTS.md`, and `.well-known/skills/index.json` together.
- Run quality checks before commit and push.

## License

MIT
