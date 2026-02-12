---
name: product-reverse
description: Use when the user provides a URL to a web product and wants to reverse-engineer it, analyze its UI/UX, discover its tech stack and API surface, and produce a comprehensive report plus actionable design document for building a similar product. Triggers on requests like "analyze this product", "reverse engineer this site", "help me clone this", "what tech does this use", or when a user provides a URL and asks to understand how a product works.
---

# Product Reverse Engineering

Systematically explore a web product using Chrome browser automation to produce:
1. **Product Analysis Report** (`report.md`) - what the product is and how it works
2. **Design Document** (`design-doc.md`) - how to build something similar (with your own technical recommendations)
3. **API Surface** (`api-surface.md`) - documented API endpoints

## Trigger Conditions

Use this skill when the user provides a product URL and asks to:
- analyze how a site/app works,
- reverse-engineer UX or user flows,
- infer API/data model and technical stack,
- produce a build plan for a similar product.

## Inputs and Outputs

### Required Input

- Target URL

### Optional Inputs

- Focus areas (for example: auth flow, editor, billing, search)
- Depth/coverage constraints (for example: "only public pages")
- Preferred implementation stack for replica planning

### Standard Outputs

- `report.md`
- `design-doc.md`
- `api-surface.md`
- `ui-design-mockup.md` (when UI draft step is requested)

## Out of Scope

- Entering real credentials or bypassing authentication walls
- Security exploitation, penetration testing, or destructive actions
- Copying proprietary assets or source code verbatim
- Legal/compliance advice beyond high-level risk notes

## Workflow Overview

```
Phase 1: Reconnaissance     -> Initial page load, tech detection, structure overview
Phase 2: Systematic Exploration -> Page-by-page, flow-by-flow deep dive
Phase 3: API Analysis        -> Synthesize captured API calls, infer data model
Phase 4: External Research   -> WebSearch for product context, tech blog posts, competitors
Phase 5: UI/UX Design Draft  -> Generate replica interaction/UI design draft via ui-ux-pro-max
Phase 6: Synthesis           -> Analyze all data, formulate architecture recommendations
Phase 7: Output Generation   -> Generate report.md, design-doc.md, api-surface.md (+ ui-design-mockup.md)
Phase 8: Replica Acceptance  -> Validate implementation, compare against original, explain product-level gaps
```

Phases are iterative. The user can direct exploration at any point.

## Input & Setup

**Required**: A URL to the product.
**Optional**: Focus areas (e.g., "focus on the editor", "I care most about the API").

### Default Screenshot Policy (Project Directory)

By default, screenshots should be saved in the project output folder (not only in session memory):

```
{output_dir}/screenshots/
```

Use stable file names and keep `state.json` screenshot references aligned to project-relative paths:

```json
{
  "id": "screenshots/homepage-initial.png"
}
```

### Slug Generation

Derive the output directory slug from the URL:
- Extract the domain name (e.g., `www.example.com` -> `example`)
- Remove common prefixes: `www.`, `app.`, `dashboard.`
- Remove TLD: `.com`, `.io`, `.org`, etc.
- Lowercase, replace dots/spaces with hyphens
- Examples: `https://www.notion.so` -> `notion`, `https://app.linear.app` -> `linear`

### Initialize Output Directory

```
output_dir = {workspace_root}/output/{product-slug}/
```

Create the directory structure:
```
{output_dir}/
├── state.json
├── screenshots/
└── recordings/
```

Initialize `state.json`:
```json
{
  "product_name": "{name}",
  "url": "{url}",
  "current_phase": "reconnaissance",
  "current_branch": "main",
  "tab_id": null,
  "focus_areas": [],
  "tech_stack": {},
  "pages_discovered": [],
  "api_endpoints": [],
  "operations": [],
  "screenshots": [],
  "notes": []
}
```

## Phase 1: Reconnaissance

Goal: Get the lay of the land before deep exploration.

1. **Set up browser tab**: Follow tab setup pattern from `references/chrome-patterns.md`. Store `tabId` in state.json.
2. **Load the product URL**: Navigate, wait 3s, take screenshot, read interactive elements, get page text. Follow "Page Exploration (Initial Load)" pattern from `references/chrome-patterns.md`.
3. **Detect tech stack**: Execute the tech detection JS snippet from `references/chrome-patterns.md` via `javascript_tool`. **The snippet returns a JSON string** - parse it and record in `state.json` `tech_stack`.
4. **Capture homepage structure**: Identify navigation links, key CTAs, main content areas from the `read_page` output.
5. **Capture initial API calls**: If needed, use the reload-based network capture pattern. Filter out static assets and chrome extensions per the "Filtering Network Noise" section in chrome-patterns.md.
6. **Log screenshot**: Save screenshots to `{output_dir}/screenshots/` with stable names (e.g., `homepage-initial.png`). In state.json, log project-relative `path` and optional tool/session `id` when available.

**After Phase 1**, present a summary to the user:
- Product name and purpose (inferred)
- Tech stack detected
- Navigation structure / main pages found
- Any API calls seen
- Ask: "What areas should I explore next?" or proceed to systematic exploration

## Phase 2: Systematic Exploration

Goal: Methodically explore each page and user flow.

### CRITICAL: Test Core User Flows

**Do NOT just observe static page states.** You MUST actively test core user flows:
- If the product has search, **perform an actual search** and observe the results page
- If the product has forms, **fill and submit them** (with test data) to see validation and success states
- If the product has navigation, **click through each nav item** to discover all views
- If the product has interactive elements (dropdowns, modals, tabs), **trigger them**

This is essential because many products transform their UI on interaction (e.g., Baidu replaces the entire homepage with a results page when you search). Failing to test flows means missing entire views and interaction patterns.

### Exploration Loop

For each page or flow to explore:

1. **Navigate** to the page (use same-domain pattern if staying on same host)
2. **Screenshot** and log the screenshot ID
3. **Analyze structure**: `read_page` for interactive elements, `get_page_text` for content
4. **Discover behavior**: Selectively click/hover interactive elements to reveal dropdowns, modals, etc.
5. **Test core flows**: Actually perform the product's primary actions (search, submit, navigate) to discover all UI states
6. **Capture API calls**: Clear network, perform actions, capture resulting API calls. Filter noise.
7. **Scroll exploration**: For long pages, scroll and screenshot each section
8. **Batch update state.json**: After exploring a page (not after every action), read state.json, append new operations/pages/endpoints, write back

### State Update Strategy

**Do NOT read/write state.json after every single action.** Instead:
- Keep a mental log of operations during exploration
- Batch-write to state.json after completing a page or flow exploration
- Operation IDs: derive from `operations.length + 1`, formatted as `op_XXX` (zero-padded to 3 digits)

### Branch Management

Branches are lightweight labels on operations for organizing parallel exploration paths.

- Default branch: `main`
- Create a new branch: set `current_branch` in state.json to a new label (e.g., `auth-flow`, `settings-page`)
- Operations logged under the current branch
- Switch branches by updating `current_branch`
- Branches are append-only labels, not git-like - no merging needed

### Auth-Gated Content

When encountering login walls or auth-gated features:
- **Never enter credentials** - this is a hard rule
- Document what's behind the wall (page name, expected functionality)
- Note it in state.json `notes`
- Move on to other explorable areas
- Inform the user about auth-gated areas found

### When to Pause and Ask

- After exploring 3-5 pages, summarize findings and ask if the user wants to redirect
- When encountering unexpected complexity (e.g., very large app)
- When auth-gated content blocks further exploration
- When the user says "pause" or "show progress"

## Phase 3: API Analysis

Goal: Synthesize all captured API calls into a coherent API surface.

1. Collect all API endpoints from state.json `api_endpoints`
2. Group by resource/domain (e.g., /api/users/*, /api/projects/*)
3. For each endpoint group:
   - Document method, URL pattern, purpose
   - Note request/response shape if captured
   - Identify auth requirements
4. Infer data model from API shapes
5. Identify auth mechanism (cookie, bearer token, API key)
6. Write `api-surface.md` with full documentation

**For non-SPA / server-rendered sites**: There may be no clean REST APIs. Document what IS available: search endpoints, suggestion APIs, tracking calls, form submission endpoints. Note this in the report.

## Phase 4: External Research

Goal: Supplement browser exploration with external knowledge.

Use `WebSearch` and `WebFetch` to research:

1. **Product information**: What the product does, who makes it, pricing, target market
2. **Technical blog posts**: Engineering blog, tech talks, conference presentations
3. **Job listings**: Technologies mentioned in job postings reveal stack
4. **Competitor landscape**: Similar products, alternatives
5. **Open source components**: Any OSS libraries or frameworks they've built on

Record findings in state.json `notes`.

## Phase 5: UI/UX Design Draft (via ui-ux-pro-max)

Goal: Generate a practical replica UI interaction design draft from reverse-engineered findings.

### Skill Dependency

Use `ui-ux-pro-max` skill for design-system generation.

If the skill is not present, install from:
- `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill`

### Workflow

1. Use reverse results (`state.json`, discovered pages, screenshots) as input.
2. Run `ui-ux-pro-max` design-system generation first (required by that skill).
3. Generate `ui-design-mockup.md` including:
   - Design tokens (color/type/spacing/shadow)
   - Page wireframes / interaction flow
   - Component states (hover/active/loading/error)
   - Responsive behavior and accessibility checklist
4. Cross-reference saved screenshot files in `{output_dir}/screenshots/`.

## Phase 6: Synthesis

Goal: Turn raw data into insights and recommendations.

1. **Architecture inference**: Based on tech stack, API patterns, and page structure, infer the likely architecture
2. **Key design decisions**: Identify important technical and UX decisions the product made
3. **Tradeoff analysis**: For each major decision, consider alternatives and why they might have chosen this approach
4. **Recommendations**: Formulate your own technical recommendations for building a similar product - don't just clone, improve where possible

## Phase 7: Output Generation

Generate final deliverables using templates from `references/`.

### CRITICAL: Design Doc First, Then Code

When the user's goal is to **build/replicate** (not just analyze), you MUST:
1. **Write `design-doc.md` FIRST** - before writing any implementation code
2. **Present the design doc to the user for review** - get explicit approval
3. **Ask about tech stack preferences** - e.g., "Do you prefer React/Vue/plain HTML? Any specific libraries?"
4. **Only start coding after design approval** - the user may redirect your approach

This prevents wasted effort from building the wrong thing. The design doc should include:
- Architecture overview with diagrams
- All views/pages and their layout (ASCII art wireframes)
- API endpoints and data flow
- Implementation plan with phases

### report.md
Read `references/report-template.md` and generate a comprehensive product analysis report. Reference screenshot IDs where relevant (the user can cross-reference with their browser session).

### design-doc.md
Read `references/design-doc-template.md` and generate an actionable design document with:
- Your own tech stack recommendations (not just copying the original)
- Tradeoff analysis for major decisions
- Prioritized feature list (P0/P1/P2)
- Implementation phases

### api-surface.md
Full API documentation with all discovered endpoints, grouped by resource.

### ui-design-mockup.md
UI/interaction replica draft generated using findings + `ui-ux-pro-max` recommendations.

### compare-diff.md (Required when a replica has been implemented)
When the user says the clone/replica is already built (or asks for verification), generate `compare-diff.md` with:
- Deployment verification (`build/start`, URL reachability, key logs)
- Functional smoke test matrix (create/read/update-like flows, auth, search, API status)
- Side-by-side differences vs original (UI, behavior, API contract)
- Product reason analysis for each major gap (stage, risk policy, infra strategy, growth loop)
- Prioritized parity plan (P0/P1/P2)

All output files go in the `output_dir`.

## State Management

### state.json Format

```json
{
  "product_name": "string",
  "url": "string",
  "current_phase": "reconnaissance|exploration|api_analysis|research|synthesis|output|replica_acceptance",
  "current_branch": "string",
  "tab_id": "number - browser tab ID for this session",
  "focus_areas": ["string"],
  "tech_stack": {"framework": "Next.js", "jquery": "1.10.2", ...},
  "pages_discovered": [
    {"path": "/dashboard", "title": "Dashboard", "branch": "main", "op_id": "op_005"}
  ],
  "api_endpoints": [
    {"method": "GET", "url": "/api/users/me", "status": 200, "auth": true, "category": "data_api", "branch": "main", "op_id": "op_010"}
  ],
  "operations": [
    {"id": "op_001", "branch": "main", "action": "navigate", "target": "https://...", "timestamp": "ISO8601", "screenshot_ref": "screenshots/homepage-initial.png"}
  ],
  "screenshots": [
    {"path": "screenshots/homepage-initial.png", "description": "Homepage initial load", "op_id": "op_001", "id": "optional_tool_id"}
  ],
  "notes": ["string"]
}
```

### Screenshot Handling

Screenshots are project artifacts by default:
- **Save to disk** under `{output_dir}/screenshots/` (or subfolders like `compare/local` and `compare/original`)
- **Log project-relative `path`** in `state.json` for durable references
- **Optionally log tool/session screenshot `id`** if the tool returns one

In the `screenshots` array, prefer `path` + `description`, and include `id` only as optional metadata.

### Operation Logging

Every significant action gets logged as an operation:
- `id`: Sequential `op_XXX` format (derive from `operations.length + 1`)
- `branch`: Current branch label
- `action`: navigate, screenshot, click, scroll, api_capture, tech_detect, etc.
- `target`: URL, element description, etc.
- `timestamp`: ISO 8601
- `screenshot_ref`: Project-relative screenshot path (optional)

### API Endpoint Categories

When logging endpoints, categorize them:
- `data_api`: REST/GraphQL endpoints returning JSON data
- `analytics`: Tracking pixels, event logging endpoints
- `suggestion`: Autocomplete, search suggestion endpoints
- `auth`: Login, token refresh, session check
- `static`: CDN, static asset requests (usually not logged)

### When State Gets Large

If state.json grows beyond what fits comfortably in context, run:

```bash
python3 scripts/summarize_state.py output/{product-slug}/state.json
```

This prints a concise summary instead of reading the full state file.

## User Commands

During exploration, the user can direct the process:

| Command | Action |
|---------|--------|
| `explore {area}` | Focus exploration on a specific area (page, flow, feature) |
| `go back to {branch}` | Switch to a different exploration branch |
| `show progress` | Display current state summary (use summarize_state.py) |
| `generate report` | Skip to Phase 6 and produce output files |
| `pause` | Save state and stop; can resume later |
| `record {flow}` | Enable GIF recording for a specific flow |
| `research {topic}` | Run external research on a specific topic |

## Key Rules

1. **Screenshots default to project files** - save to `{output_dir}/screenshots/` and keep state index aligned
2. **Never enter credentials** or sensitive data into the product
3. **All output in English**
4. **Design doc is prescriptive** - include your own recommendations, not just describing the original
5. **Ask before deep-diving** - after initial recon, check what the user wants to focus on
6. **Batch state updates** - update state.json per-page, not per-action
7. **Filter network noise** - ignore static assets, chrome extensions, data URIs
8. **Tech detection returns JSON string** - parse it before storing in state.json
9. **Test core user flows** - don't just observe static pages; perform searches, submit forms, click through navigation to discover all UI states and transitions
10. **Design doc before code** - when the user wants to build/replicate, write design-doc.md first, get user review, ask about tech stack preferences, then code
11. **Prefer real data chains for core features (scenario-based)** - "real data" means a real business data path (request -> backend/proxy -> response), not necessarily scraping the original site.  
   - For search/aggregation products (e.g., baidu-like search), use real result sources from day one.  
   - For forum/UGC replicas, mock seed data is acceptable for MVP, but create/write flows must be fully functional and persistent.
12. **Generate UI design draft with ui-ux-pro-max** - produce `ui-design-mockup.md` after research and before final output synthesis
13. **MVP confirmation loop before coding** - when moving from reverse-analysis to implementation, confirm 2-4 scope decisions first (data source strategy, backend shape, storage, deployment/container policy), then code
14. **Prefer lightweight stack for MVP** - default to zero-container, single-process, local persistence; only introduce Redis/queues/object storage/containers when explicitly requested or justified by scale constraints
15. **Replica acceptance is mandatory for completed clones** - run deploy + smoke test + side-by-side original comparison, then produce `compare-diff.md` with product-level gap reasons and prioritized parity plan
