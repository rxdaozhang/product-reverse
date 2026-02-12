# product-reverse

`product-reverse` is a skill for reverse-engineering web products from a URL.

It helps Claude/Codex systematically:
- analyze UI/UX and user flows,
- inspect API surface and inferred data model,
- identify likely tech stack,
- generate actionable outputs (`report.md`, `design-doc.md`, `api-surface.md`) for building a similar product.

## Install

### Recommended (skills.sh)

```bash
npx skills add rxdaozhang/ProductRevise
```

Install the specific skill explicitly:

```bash
npx skills add rxdaozhang/ProductRevise --skill product-reverse
```

## Usage

Invoke this skill when a user provides a product URL and asks to analyze or clone the product behavior, for example:
- "Analyze this product and tell me how it works"
- "Reverse engineer this site"
- "Help me clone this product"

## Repository Structure

```text
skills/
  product-reverse/
    SKILL.md
    references/
      chrome-patterns.md
      design-doc-template.md
      report-template.md
    scripts/
      summarize_state.py
```

## Changelog

### v0.1.0 - 2026-02-11

- Initial public release
- Added skills.sh install instructions
- Aligned repository layout to `skills/product-reverse`
- Published as searchable skill source for `npx skills add`

## License

MIT
