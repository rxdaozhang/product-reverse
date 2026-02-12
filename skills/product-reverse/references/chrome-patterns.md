# Chrome Automation Patterns

Reference patterns for systematic browser exploration using Chrome MCP tools.

## Tab Setup

```
1. tabs_context_mcp(createIfEmpty: true)  -> get group info
2. tabs_create_mcp()                       -> create dedicated tab, store tabId
```

Always store `tabId` for all subsequent operations.

## Page Exploration (Initial Load)

**Important**: Network tracking starts on first `read_network_requests` call, and requests are **automatically cleared on cross-domain navigation**. To capture initial page load requests:

```
1. navigate(tabId, url)                             # load page
2. computer(action: "wait", tabId, duration: 3)     # wait for render
3. computer(action: "screenshot", tabId)            # capture visual state -> log screenshot ID
4. read_page(tabId, filter: "interactive")          # get interactive elements
5. get_page_text(tabId)                             # extract text content
6. read_network_requests(tabId, clear: true)        # INIT tracking + clear
7. navigate(tabId, url)                             # reload to capture network
8. computer(action: "wait", tabId, duration: 3)     # wait for reload
9. read_network_requests(tabId)                     # now captures page load requests
```

Steps 6-9 are only needed if you want to see initial page load network activity. For most pages, skip to "API Capture" below.

## Page Exploration (Same-Domain Navigation)

When navigating within the same domain, network tracking persists:

```
1. read_network_requests(tabId, clear: true)       # clear previous
2. [click link or navigate to subpage]
3. computer(action: "wait", tabId, duration: 3)
4. computer(action: "screenshot", tabId)
5. read_page(tabId, filter: "interactive")
6. read_network_requests(tabId)                    # captures navigation requests
```

## Interactive Element Discovery

```
1. read_page(tabId, filter: "interactive")   # all clickable/input elements
2. find(tabId, query: "navigation menu")     # find specific elements by description
3. computer(action: "hover", tabId, ref)     # reveal tooltips/dropdowns
4. computer(action: "screenshot", tabId)     # capture hover state
5. computer(action: "left_click", tabId, ref) # interact
6. computer(action: "wait", tabId, duration: 2)
7. computer(action: "screenshot", tabId)     # capture result
```

## API Capture

For capturing API calls triggered by user actions:

```
1. read_network_requests(tabId, clear: true)          # clear baseline
2. [perform action: click button, submit form, etc.]
3. computer(action: "wait", tabId, duration: 2)
4. read_network_requests(tabId)                       # capture new calls
```

Record each endpoint with: method, URL, status, request/response shape.

### Filtering Network Noise

Raw `read_network_requests` returns ALL requests (images, CSS, JS, extensions). To filter:

- **Use `urlPattern`**: Try `/api/`, `/v1/`, `/graphql`, or product-specific patterns
- **Ignore noise**: Discard URLs matching these patterns:
  - `chrome-extension://` (browser extensions)
  - `data:image/` (inline images)
  - `.js`, `.css`, `.png`, `.jpg`, `.woff`, `.svg` (static assets)
  - Common CDN domains: `cdnjs.cloudflare.com`, `googleapis.com`, etc.
- **Categorize what remains**:
  - **Data API**: REST/GraphQL endpoints returning JSON (the main target)
  - **Analytics/Tracking**: Pixel endpoints (`/v.gif`, `/collect`, `/track`, `/ztbox`)
  - **Suggestions/Autocomplete**: Search suggestion endpoints
  - **Auth**: Login, token refresh, session check endpoints

For traditional server-rendered sites (not SPAs), there may be few or no clean REST APIs. Focus on:
- Search/suggestion endpoints
- Tracking/analytics calls (reveal product instrumentation)
- Any XHR/Fetch calls (check `method: POST` requests especially)

## Tech Stack Detection

JavaScript snippet to detect common frameworks and tools. Uses `getAttribute('class')` to avoid SVG className bug.

```javascript
(function() {
  const tech = {};
  // Modern Frameworks
  if (window.__NEXT_DATA__) tech.nextjs = window.__NEXT_DATA__.buildId || true;
  if (window.__NUXT__) tech.nuxt = true;
  if (document.querySelector('[data-reactroot], [id="__next"], [id="root"][data-reactroot]')) tech.react = true;
  if (document.querySelector('[ng-version]')) { tech.angular = document.querySelector('[ng-version]').getAttribute('ng-version'); }
  if (window.__VUE__ || document.querySelector('[data-v-]') || document.querySelector('div[id="app"].__vue__')) tech.vue = true;
  if (window.__SVELTE__) tech.svelte = true;
  // Legacy Libraries
  if (window.jQuery) tech.jquery = jQuery.fn.jquery;
  if (window.Backbone) tech.backbone = true;
  if (window.angular) tech.angularjs = window.angular.version ? window.angular.version.full : true;
  // CSS Frameworks - Tailwind: check for responsive prefixes or specific utility patterns
  var allCls = new Set();
  document.querySelectorAll('[class]').forEach(function(el) {
    var c = el.getAttribute('class');
    if (c) c.split(/\s+/).forEach(function(x) { allCls.add(x); });
  });
  var clsArr = Array.from(allCls);
  var hasTwResponsive = clsArr.some(function(c) { return /^(sm|md|lg|xl|2xl):/.test(c); });
  var hasTwUtilities = clsArr.filter(function(c) { return /^(bg|text|px|py|mx|my|mt|mb|ml|mr|pt|pb|pl|pr|flex|grid|gap|rounded|shadow|border|w|h|min|max)-/.test(c); }).length > 10;
  if (hasTwResponsive || hasTwUtilities) tech.tailwind = true;
  // Bootstrap
  if (clsArr.some(function(c) { return /^(col-|btn-|navbar|container-fluid|row)$/.test(c); })) tech.bootstrap = true;
  // State Management
  if (window.__REDUX_DEVTOOLS_EXTENSION__ || window.__REDUX_STATE__) tech.redux = true;
  if (window.__MOBX_DEVTOOLS_GLOBAL_HOOK__) tech.mobx = true;
  // Analytics
  if (window.ga || window.gtag) tech.googleAnalytics = true;
  if (window.mixpanel) tech.mixpanel = true;
  if (window.amplitude) tech.amplitude = true;
  if (window._hmt) tech.baiduAnalytics = true;
  // Auth indicators
  if (document.cookie.match(/token|jwt|session_id|auth/i)) tech.cookieAuth = true;
  try { if (localStorage.getItem('token') || localStorage.getItem('access_token') || localStorage.getItem('auth')) tech.tokenAuth = true; } catch(e) {}
  // Meta
  var generator = document.querySelector('meta[name="generator"]');
  if (generator) tech.generator = generator.content;
  // Script sources (for CDN/hosting inference)
  var scriptHosts = Array.from(new Set(
    Array.from(document.querySelectorAll('script[src]'))
      .map(function(s) { try { return new URL(s.src).hostname; } catch(e) { return null; } })
      .filter(Boolean)
  ));
  tech._scriptHosts = scriptHosts;
  return JSON.stringify(tech);
})()
```

Execute via `javascript_tool(tabId, action: "javascript_exec", text: <snippet>)`.

**Parse the JSON string result** before recording in state.json.

## Scroll Exploration

For long pages, capture content in viewport-sized chunks:

```
1. computer(action: "screenshot", tabId)                    # top of page
2. computer(action: "scroll", tabId, coordinate: [512, 400], scroll_direction: "down", scroll_amount: 5)
3. computer(action: "wait", tabId, duration: 1)
4. computer(action: "screenshot", tabId)                    # next section
5. [repeat until page bottom or no new content]
```

## Form Analysis

Discover form structure without submitting:

```
1. find(tabId, query: "form")
2. read_page(tabId, filter: "interactive")   # list all form fields
3. [document field names, types, validation rules]
```

Never enter real credentials or sensitive data. Note auth-gated areas for documentation.

## GIF Recording (opt-in)

Only record GIFs when user requests them:

```
1. gif_creator(action: "start_recording", tabId)
2. computer(action: "screenshot", tabId)       # initial frame
3. [perform actions with screenshots between each]
4. computer(action: "screenshot", tabId)       # final frame
5. gif_creator(action: "stop_recording", tabId)
6. gif_creator(action: "export", tabId, download: true, filename: "flow_name.gif")
```
