#!/usr/bin/env python3
"""FinOps Framework Coverage Checker.

Parses coverage-matrix.yaml and validates:
1. Coverage statistics across all framework elements
2. All referenced files exist in references/
3. Compares capabilities against framework GitHub repo
4. Checks FOCUS spec version against GitHub releases

Exit codes:
  0 — all checks pass
  1 — coverage gaps or validation errors detected
"""

import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml")
    sys.exit(1)

try:
    import requests
except ImportError:
    requests = None

REPO_ROOT = Path(__file__).resolve().parent.parent
MATRIX_PATH = REPO_ROOT / "coverage-matrix.yaml"
REFERENCES_DIR = REPO_ROOT / "skills" / "cloud-finops" / "references"
FRAMEWORK_REPO = "finopsfoundation/framework"
FRAMEWORK_TREE_URL = f"https://api.github.com/repos/{FRAMEWORK_REPO}/git/trees/main?recursive=1"
FOCUS_RELEASES_URL = "https://api.github.com/repos/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec/releases/latest"

# Minimum coverage threshold (percentage of capabilities with full coverage)
MIN_COVERAGE_THRESHOLD = 80


def load_matrix():
    """Load and parse the coverage matrix YAML."""
    if not MATRIX_PATH.exists():
        print(f"ERROR: Coverage matrix not found at {MATRIX_PATH}")
        sys.exit(1)

    with open(MATRIX_PATH) as f:
        return yaml.safe_load(f)


def validate_reference_files(matrix):
    """Check that every file referenced in covered_by exists."""
    errors = []
    all_files = set()

    def collect_files(obj):
        if isinstance(obj, dict):
            for f in obj.get("covered_by", []):
                all_files.add(f)
            for v in obj.values():
                collect_files(v)
        elif isinstance(obj, list):
            for item in obj:
                collect_files(item)

    collect_files(matrix)

    for filename in sorted(all_files):
        # Support subdirectory paths (e.g., "capabilities/forecasting.md")
        filepath = REFERENCES_DIR / filename
        if not filepath.exists():
            errors.append(f"Referenced file missing: {filename}")

    return errors, all_files


def calculate_coverage(matrix):
    """Calculate coverage statistics across unique capabilities."""
    # Deduplicate capabilities (same cap can appear in multiple domains)
    seen_caps = {}  # id -> {cap_data, domains: []}
    for domain in matrix.get("domains", []):
        for cap in domain.get("capabilities", []):
            cap_id = cap["id"]
            if cap_id not in seen_caps:
                seen_caps[cap_id] = {**cap, "domains": [domain["name"]]}
            else:
                seen_caps[cap_id]["domains"].append(domain["name"])

    stats = {"full": 0, "partial": 0, "none": 0, "total": 0}
    gaps = []
    for cap_id, cap in seen_caps.items():
        stats["total"] += 1
        coverage = cap.get("coverage", "none")
        stats[coverage] = stats.get(coverage, 0) + 1
        if coverage != "full":
            gaps.append({
                "name": cap["name"],
                "domain": ", ".join(cap["domains"]),
                "coverage": coverage,
                "id": cap_id,
            })

    # Scopes/scope_gaps kept for backward compat (empty if not in matrix)
    scope_stats = {"full": 0, "partial": 0, "none": 0, "total": 0}
    scope_gaps = []
    for scope in matrix.get("scopes", []):
        scope_stats["total"] += 1
        coverage = scope.get("coverage", "none")
        scope_stats[coverage] = scope_stats.get(coverage, 0) + 1
        if coverage != "full":
            scope_gaps.append({
                "name": scope["name"],
                "coverage": coverage,
                "note": scope.get("note", ""),
            })

    return stats, gaps, scope_stats, scope_gaps


def check_framework_repo(matrix):
    """Check finopsfoundation/framework repo for new/changed capability files."""
    if requests is None:
        return [], "skipped (requests not installed)"

    try:
        headers = {"Accept": "application/vnd.github.v3+json"}
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"token {token}"
        resp = requests.get(FRAMEWORK_TREE_URL, timeout=15, headers=headers)
        resp.raise_for_status()
    except Exception as e:
        return [], f"skipped ({e})"

    # Extract capability slugs from _capabilities/*.md files in the repo tree
    repo_slugs = set()
    for item in resp.json().get("tree", []):
        path = item.get("path", "")
        if path.startswith("_capabilities/") and path.endswith(".md"):
            slug = path.replace("_capabilities/", "").replace(".md", "")
            if slug:
                repo_slugs.add(slug)

    # Get matrix capability IDs
    matrix_ids = set()
    for domain in matrix.get("domains", []):
        for cap in domain.get("capabilities", []):
            matrix_ids.add(cap["id"])

    # Find capabilities in repo but not in matrix
    new_capabilities = repo_slugs - matrix_ids
    return sorted(new_capabilities), "success"


def check_focus_version(matrix):
    """Check if FOCUS spec has a newer version than what's in the matrix."""
    if requests is None:
        return None, "skipped (requests not installed)"

    try:
        headers = {"Accept": "application/vnd.github.v3+json"}
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"token {token}"
        resp = requests.get(FOCUS_RELEASES_URL, timeout=15, headers=headers)
        resp.raise_for_status()
        latest = resp.json().get("tag_name", "").lstrip("v")
        # Check both old and new matrix structure for FOCUS version
        current = matrix.get("focus_spec", {}).get("version", "unknown")
        if current == "unknown":
            current = matrix.get("focus_version", "unknown")
        if current == "unknown":
            for ref in matrix.get("additional_references", []):
                if ref.get("id") == "focus-spec":
                    current = ref.get("version", "unknown")
                    break
        return {"current": current, "latest": latest}, "success"
    except Exception as e:
        return None, f"skipped ({e})"


def generate_report(matrix, stats, gaps, scope_stats, scope_gaps,
                    file_errors, new_caps, sitemap_status,
                    focus_info, focus_status, all_files):
    """Generate a markdown coverage report."""
    total = stats["total"]
    full = stats["full"]
    pct = (full / total * 100) if total > 0 else 0

    lines = [
        "## FinOps Framework Coverage Report",
        "",
        f"**Framework version:** {matrix.get('framework_version', 'unknown')}",
        f"**FOCUS version:** {matrix.get('focus_version', matrix.get('focus_spec', {}).get('version', 'unknown'))}",
        f"**Last audit:** {matrix.get('last_audit', 'unknown')}",
        f"**Overall capability coverage:** {full}/{total} ({pct:.0f}%)",
        f"**Reference files tracked:** {len(all_files)}",
        "",
    ]

    # Capability gaps
    if gaps:
        lines.append("### Capability Gaps")
        lines.append("")
        lines.append("| Capability | Domain | Coverage | Notes |")
        lines.append("|---|---|---|---|")
        for g in gaps:
            lines.append(f"| {g['name']} | {g['domain']} | {g['coverage']} | |")
        lines.append("")

    # Scope gaps
    if scope_gaps:
        lines.append("### Scope Gaps")
        lines.append("")
        lines.append("| Scope | Coverage | Notes |")
        lines.append("|---|---|---|")
        for g in scope_gaps:
            lines.append(f"| {g['name']} | {g['coverage']} | {g.get('note', '')} |")
        lines.append("")

    # Framework repo check
    lines.append("### Framework Drift Check")
    lines.append("")
    if sitemap_status != "success":
        lines.append(f"Framework repo check: {sitemap_status}")
    elif new_caps:
        lines.append("**New capabilities detected on finops.org (not in coverage matrix):**")
        for cap in new_caps:
            lines.append(f"- `{cap}`")
    else:
        lines.append("No new capabilities detected — framework unchanged since last audit.")
    lines.append("")

    # FOCUS version check
    lines.append("### FOCUS Version Check")
    lines.append("")
    if focus_status != "success":
        lines.append(f"FOCUS check: {focus_status}")
    elif focus_info:
        if focus_info["current"] == focus_info["latest"]:
            lines.append(f"FOCUS v{focus_info['current']} — up to date.")
        else:
            lines.append(f"**FOCUS update available:** v{focus_info['current']} → v{focus_info['latest']}")
    lines.append("")

    # File validation
    lines.append("### Reference File Validation")
    lines.append("")
    if file_errors:
        for err in file_errors:
            lines.append(f"- {err}")
    else:
        lines.append(f"All {len(all_files)} referenced files exist.")
    lines.append("")

    return "\n".join(lines)


def main():
    matrix = load_matrix()
    has_errors = False

    # Validate reference files
    file_errors, all_files = validate_reference_files(matrix)
    if file_errors:
        has_errors = True

    # Calculate coverage
    stats, gaps, scope_stats, scope_gaps = calculate_coverage(matrix)

    # Check coverage threshold
    total = stats["total"]
    full = stats["full"]
    pct = (full / total * 100) if total > 0 else 0
    if pct < MIN_COVERAGE_THRESHOLD:
        has_errors = True

    # Check framework repo for new capabilities
    new_caps, sitemap_status = check_framework_repo(matrix)
    if new_caps:
        has_errors = True

    # Check FOCUS version
    focus_info, focus_status = check_focus_version(matrix)
    if focus_info and focus_info.get("current") != focus_info.get("latest"):
        has_errors = True

    # Generate report
    report = generate_report(
        matrix, stats, gaps, scope_stats, scope_gaps,
        file_errors, new_caps, sitemap_status,
        focus_info, focus_status, all_files,
    )

    print(report)

    if has_errors:
        print("---")
        print("RESULT: ISSUES DETECTED — see report above.")
        sys.exit(1)
    else:
        print("---")
        print("RESULT: ALL CHECKS PASSED.")
        sys.exit(0)


if __name__ == "__main__":
    main()
