#!/usr/bin/env python3
"""Summarize a product-reverse state.json file.

Usage: python3 summarize_state.py <path/to/state.json>

Outputs a concise summary of exploration progress to keep the context window clean.
"""

import json
import sys
from collections import defaultdict
from pathlib import Path


def summarize(state_path: str) -> None:
    path = Path(state_path)
    if not path.exists():
        print(f"Error: {state_path} not found")
        sys.exit(1)

    state = json.loads(path.read_text())

    # Header
    print(f"# State Summary: {state.get('product_name', 'Unknown')}")
    print(f"URL: {state.get('url', 'N/A')}")
    print(f"Phase: {state.get('current_phase', 'N/A')}")
    print(f"Current Branch: {state.get('current_branch', 'main')}")
    print()

    # Branch tree
    operations = state.get("operations", [])
    branches = defaultdict(list)
    for op in operations:
        branches[op.get("branch", "main")].append(op)

    print("## Branches")
    for branch, ops in branches.items():
        actions = defaultdict(int)
        for op in ops:
            actions[op.get("action", "unknown")] += 1
        action_str = ", ".join(f"{v} {k}" for k, v in actions.items())
        print(f"  - {branch}: {len(ops)} ops ({action_str})")
    print()

    # Pages discovered
    pages = state.get("pages_discovered", [])
    if pages:
        print("## Pages Discovered")
        for page in pages:
            if isinstance(page, dict):
                print(f"  - {page.get('path', 'N/A')}: {page.get('title', 'untitled')}")
            else:
                print(f"  - {page}")
        print()

    # API endpoints grouped by category
    endpoints = state.get("api_endpoints", [])
    if endpoints:
        print("## API Endpoints")
        by_cat = defaultdict(list)
        for ep in endpoints:
            if isinstance(ep, dict):
                cat = ep.get("category", "unknown")
                by_cat[cat].append(ep)
            else:
                by_cat["unknown"].append(ep)
        for cat, eps in by_cat.items():
            print(f"  [{cat}] ({len(eps)} endpoints)")
            for ep in eps[:5]:
                if isinstance(ep, dict):
                    print(f"    {ep.get('method', '?'):<8} {ep.get('url', '?')[:50]:<50} {ep.get('status', '?')}")
            if len(eps) > 5:
                print(f"    ... and {len(eps) - 5} more")
        print()

    # Tech stack
    tech = state.get("tech_stack", {})
    if tech:
        print("## Tech Stack")
        for key, val in tech.items():
            print(f"  - {key}: {val}")
        print()

    # Screenshots
    screenshots = state.get("screenshots", [])
    if screenshots:
        print(f"## Screenshots: {len(screenshots)} captured")
        for ss in screenshots[-5:]:  # show last 5
            if isinstance(ss, dict):
                ss_id = ss.get("id", ss.get("filename", "?"))
                print(f"  - {ss_id}: {ss.get('description', '')}")
            else:
                print(f"  - {ss}")
        if len(screenshots) > 5:
            print(f"  ... and {len(screenshots) - 5} more")
        print()

    # Summary stats
    print("## Stats")
    print(f"  Operations: {len(operations)}")
    print(f"  Pages: {len(pages)}")
    print(f"  API endpoints: {len(endpoints)}")
    print(f"  Screenshots: {len(screenshots)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path/to/state.json>")
        sys.exit(1)
    summarize(sys.argv[1])
