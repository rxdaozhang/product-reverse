# Product Analysis Report Template

Use this as a flexible template. Adapt sections based on what was discovered during exploration.

---

```markdown
# {Product Name} - Product Analysis Report

**URL**: {url}
**Analysis Date**: {date}
**Exploration Branches**: {branch list}

## Executive Summary

{2-3 paragraph overview: what the product is, who it serves, key technical findings, and notable design decisions.}

## Product Overview

- **Category**: {e.g., SaaS, marketplace, developer tool}
- **Target Users**: {primary and secondary personas}
- **Core Value Proposition**: {one sentence}
- **Business Model**: {freemium, subscription, usage-based, etc.}
- **Maturity**: {early stage, growth, mature}

## Tech Stack

| Layer | Technology | Confidence | Evidence |
|-------|-----------|------------|----------|
| Framework | {e.g., Next.js} | {High/Medium/Low} | {e.g., __NEXT_DATA__ present} |
| Styling | {e.g., Tailwind CSS} | | |
| State Mgmt | {e.g., Redux} | | |
| Auth | {e.g., JWT cookie} | | |
| Analytics | {e.g., Mixpanel} | | |
| CDN/Hosting | {e.g., Vercel} | | |
| API Style | {e.g., REST, GraphQL} | | |

## Page-by-Page Analysis

### {Page Name} ({url path})

**Screenshot**: `screenshots/{op_id}_{page_slug}.png`

**Purpose**: {what this page does}

**Key Elements**:
- {element description}

**Notable Patterns**:
- {design pattern, interaction, etc.}

**API Calls**: {list endpoints triggered on this page}

{Repeat for each explored page}

## User Flows

### {Flow Name} (e.g., "Sign Up Flow")

| Step | Action | Page | Screenshot | API Call |
|------|--------|------|------------|----------|
| 1 | {action} | {page} | `screenshots/{ref}` | {endpoint} |
| 2 | ... | | | |

**Notes**: {observations about the flow}

{Repeat for each explored flow}

## API Surface

Summary of discovered endpoints. Full details in `api-surface.md`.

| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|---------------|
| GET | /api/... | {purpose} | {yes/no} |

**Total endpoints discovered**: {count}
**API style**: {REST/GraphQL/RPC/mixed}
**Auth mechanism**: {description}

## Inferred Data Model

Based on API responses and UI structure:

{Entity relationship descriptions or simple ERD in text}

### {Entity Name}
- `id`: {type}
- `field`: {type, notes}
- Relations: {belongs_to X, has_many Y}

## Authentication & Authorization

- **Auth type**: {cookie/JWT/OAuth/session}
- **Login methods**: {email+password, SSO, social}
- **Auth-gated areas**: {list pages/features behind auth}
- **Token storage**: {cookie/localStorage/sessionStorage}
- **Token refresh**: {mechanism if detected}

## External Research

### Product Context
- {findings from WebSearch about the product}

### Technical Insights
- {blog posts, tech talks, job listings revealing stack}

### Competitor Landscape
- {similar products and differentiation}

## Exploration Log

| Op ID | Branch | Action | Target | Timestamp |
|-------|--------|--------|--------|-----------|
| op_001 | main | navigate | homepage | ... |
| op_002 | main | screenshot | homepage | ... |

{Or reference state.json for full log}
```
