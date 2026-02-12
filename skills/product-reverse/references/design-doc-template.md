# Design Document Template

This template is **prescriptive** - it should contain the author's own technical recommendations, not just describe what the original product does.

---

```markdown
# {Product Name} Clone - Design Document

**Based on analysis of**: {original URL}
**Date**: {date}

## 1. Objective

Build a {category} product that {core value proposition}, inspired by {original product}.

**Key differentiators from original**:
- {what to do differently or better}

## 2. Scope

### In Scope (MVP)
- {feature 1}
- {feature 2}

### In Scope (Post-MVP)
- {feature 3}

### Out of Scope
- {feature explicitly excluded, with reason}

### Deliberate Differences from Original
- {design choice where we diverge, with rationale}

## 3. Recommended Architecture

### Tech Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Frontend | {e.g., Next.js 14 App Router} | {why this over alternatives} |
| Styling | {e.g., Tailwind CSS + shadcn/ui} | {why} |
| Backend | {e.g., Next.js API Routes / FastAPI} | {why} |
| Database | {e.g., PostgreSQL via Supabase} | {why} |
| Auth | {e.g., Supabase Auth / NextAuth} | {why} |
| Hosting | {e.g., Vercel} | {why} |
| Storage | {e.g., S3 / Supabase Storage} | {why} |

### Architecture Diagram (text)

```
[Browser] -> [CDN/Edge] -> [App Server] -> [Database]
                                        -> [Cache]
                                        -> [Object Storage]
```

### Key Technical Decisions

**Decision 1: {topic}**
- Options considered: {A, B, C}
- Chosen: {B}
- Rationale: {why B wins for this context}
- Tradeoffs: {what we give up}

## 4. Data Model

### {Entity}
```sql
CREATE TABLE {entity} (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  {field} {TYPE} {constraints},
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
```

### Relationships
- {Entity A} 1:N {Entity B} via `{foreign_key}`

## 5. API Design

### Endpoints

| Method | Path | Purpose | Auth | Request | Response |
|--------|------|---------|------|---------|----------|
| POST | /api/auth/login | User login | No | `{email, password}` | `{token, user}` |

### API Conventions
- {REST/GraphQL, naming conventions, pagination style, error format}

## 6. Frontend Structure

### Route Map
```
/                  -> Landing page
/app               -> Main dashboard (auth required)
/app/{feature}     -> Feature page
/auth/login        -> Login
/auth/register     -> Register
```

### Component Architecture
```
src/
├── app/           # Next.js app router pages
├── components/
│   ├── ui/        # Base components (shadcn)
│   ├── features/  # Feature-specific components
│   └── layouts/   # Layout wrappers
├── lib/           # Utilities, API client, hooks
└── types/         # TypeScript types
```

### Key UI Patterns
- {pattern from original worth replicating, e.g., "optimistic updates on form submit"}
- {pattern to improve upon}

## 7. Feature Implementation Plan

### P0 - Must Have (MVP)
| Feature | Complexity | Dependencies | Notes |
|---------|-----------|-------------|-------|
| {feature} | {S/M/L} | {deps} | {notes} |

### P1 - Should Have
| Feature | Complexity | Dependencies | Notes |
|---------|-----------|-------------|-------|

### P2 - Nice to Have
| Feature | Complexity | Dependencies | Notes |
|---------|-----------|-------------|-------|

## 8. Implementation Phases

### Phase 1: Foundation (Week 1-2)
- [ ] Project setup (framework, DB, auth)
- [ ] Core data model + migrations
- [ ] Auth flow (register, login, logout)
- [ ] Base layout and navigation

### Phase 2: Core Features (Week 3-4)
- [ ] {primary feature 1}
- [ ] {primary feature 2}
- [ ] Basic API endpoints

### Phase 3: Polish & Launch (Week 5-6)
- [ ] {secondary features}
- [ ] Error handling and edge cases
- [ ] Performance optimization
- [ ] Deployment pipeline

## 9. Open Questions

- [ ] {question that needs user input or further research}
- [ ] {technical decision deferred}
```
