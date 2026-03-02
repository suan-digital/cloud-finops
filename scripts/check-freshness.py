#!/usr/bin/env python3
"""Git-based content freshness checker for FinOps skill.

Monitors upstream FinOps Foundation GitHub repos for changes that may
require updates to our reference content. Compares current repo state
against stored baselines in .content-baselines.json.

Monitored repos:
  - finopsfoundation/framework — capabilities, domains, personas
  - FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec — releases + working draft
  - finopsfoundation/kpis — waste sensors, KPI definitions

Usage:
  python scripts/check-freshness.py                   # check mode (CI)
  python scripts/check-freshness.py --update-baselines # update baselines

Exit codes:
  0 — no drift detected (or baselines updated)
  1 — drift detected
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
BASELINES_PATH = REPO_ROOT / ".content-baselines.json"

GITHUB_API = "https://api.github.com"
FRAMEWORK_REPO = "finopsfoundation/framework"
FOCUS_REPO = "FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec"
KPIS_REPO = "finopsfoundation/kpis"


def github_headers():
    """Build GitHub API headers with optional auth token."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    return headers


def api_get(url):
    """Make a GET request to the GitHub API."""
    resp = requests.get(url, headers=github_headers(), timeout=30)
    resp.raise_for_status()
    return resp.json()


def fetch_framework_tree():
    """Fetch the full file tree from finopsfoundation/framework."""
    url = f"{GITHUB_API}/repos/{FRAMEWORK_REPO}/git/trees/main?recursive=1"
    data = api_get(url)
    tree_sha = data.get("sha", "")

    capabilities = []
    domains = []
    for item in data.get("tree", []):
        path = item.get("path", "")
        if path.startswith("_capabilities/") and path.endswith(".md"):
            capabilities.append(path.replace("_capabilities/", "").replace(".md", ""))
        elif path.startswith("_domains/") and path.endswith(".md"):
            domains.append(path.replace("_domains/", "").replace(".md", ""))

    return {
        "tree_sha": tree_sha,
        "capabilities_files": sorted(capabilities),
        "domains_files": sorted(domains),
    }


def fetch_personas_hash():
    """Fetch and hash the personas YAML from the framework repo."""
    url = f"{GITHUB_API}/repos/{FRAMEWORK_REPO}/contents/_data/personas.yml"
    data = api_get(url)
    # Content is base64-encoded; hash the raw download URL content instead
    download_url = data.get("download_url", "")
    if download_url:
        resp = requests.get(download_url, timeout=15)
        resp.raise_for_status()
        content_hash = hashlib.sha256(resp.content).hexdigest()
        return f"sha256:{content_hash}"
    # Fallback: hash the sha from the API
    return f"git:{data.get('sha', 'unknown')}"


def fetch_focus_releases():
    """Fetch latest FOCUS release and working draft status."""
    # Latest release
    release_url = f"{GITHUB_API}/repos/{FOCUS_REPO}/releases/latest"
    try:
        release = api_get(release_url)
        latest_tag = release.get("tag_name", "").lstrip("v")
    except requests.exceptions.HTTPError:
        latest_tag = "unknown"

    # Working draft — latest commits
    commits_url = f"{GITHUB_API}/repos/{FOCUS_REPO}/commits?sha=working_draft&per_page=5"
    try:
        commits = api_get(commits_url)
        if commits:
            latest = commits[0]
            wd_commit = latest["sha"][:12]
            wd_date = latest["commit"]["committer"]["date"][:10]
        else:
            wd_commit = "unknown"
            wd_date = "unknown"
    except requests.exceptions.HTTPError:
        wd_commit = "unknown"
        wd_date = "unknown"

    return {
        "latest_release": latest_tag,
        "working_draft_commit": wd_commit,
        "working_draft_date": wd_date,
    }


def fetch_kpis_latest():
    """Fetch latest commit from the KPIs repo."""
    url = f"{GITHUB_API}/repos/{KPIS_REPO}/commits?per_page=1"
    commits = api_get(url)
    if commits:
        latest = commits[0]
        return {
            "latest_commit": latest["sha"][:12],
            "latest_commit_date": latest["commit"]["committer"]["date"][:10],
        }
    return {"latest_commit": "unknown", "latest_commit_date": "unknown"}


def fetch_all():
    """Fetch current state from all monitored repos."""
    print("Fetching framework repo tree...")
    framework = fetch_framework_tree()

    print("Fetching personas hash...")
    framework["personas_hash"] = fetch_personas_hash()

    print("Fetching FOCUS releases and working draft...")
    focus = fetch_focus_releases()

    print("Fetching KPIs repo latest commit...")
    kpis = fetch_kpis_latest()

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "framework_repo": framework,
        "focus_repo": focus,
        "kpis_repo": kpis,
    }


def load_baselines():
    """Load stored baselines from disk."""
    if not BASELINES_PATH.exists():
        return None
    with open(BASELINES_PATH) as f:
        return json.load(f)


def save_baselines(data):
    """Save baselines to disk."""
    with open(BASELINES_PATH, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    print(f"Baselines saved to {BASELINES_PATH}")


def compare(current, baselines):
    """Compare current state against baselines. Returns list of drift items."""
    drifts = []

    # Framework capabilities
    cur_caps = set(current["framework_repo"]["capabilities_files"])
    base_caps = set(baselines["framework_repo"]["capabilities_files"])
    added = cur_caps - base_caps
    removed = base_caps - cur_caps
    if added:
        drifts.append(f"Framework: {len(added)} new capability file(s): {', '.join(sorted(added))}")
    if removed:
        drifts.append(f"Framework: {len(removed)} removed capability file(s): {', '.join(sorted(removed))}")

    # Framework domains
    cur_doms = set(current["framework_repo"]["domains_files"])
    base_doms = set(baselines["framework_repo"]["domains_files"])
    added_d = cur_doms - base_doms
    removed_d = base_doms - cur_doms
    if added_d:
        drifts.append(f"Framework: {len(added_d)} new domain file(s): {', '.join(sorted(added_d))}")
    if removed_d:
        drifts.append(f"Framework: {len(removed_d)} removed domain file(s): {', '.join(sorted(removed_d))}")

    # Framework personas
    if current["framework_repo"]["personas_hash"] != baselines["framework_repo"]["personas_hash"]:
        drifts.append("Framework: personas.yml content has changed")

    # Framework tree SHA (general change indicator)
    if current["framework_repo"]["tree_sha"] != baselines["framework_repo"]["tree_sha"]:
        if not drifts:  # Only report if no specific changes found
            drifts.append("Framework: repo tree SHA changed (general content update)")

    # FOCUS release
    if current["focus_repo"]["latest_release"] != baselines["focus_repo"]["latest_release"]:
        drifts.append(
            f"FOCUS: new release {baselines['focus_repo']['latest_release']} → "
            f"{current['focus_repo']['latest_release']}"
        )

    # FOCUS working draft
    if current["focus_repo"]["working_draft_commit"] != baselines["focus_repo"]["working_draft_commit"]:
        drifts.append(
            f"FOCUS: working draft updated (latest commit: "
            f"{current['focus_repo']['working_draft_commit']} on "
            f"{current['focus_repo']['working_draft_date']})"
        )

    # KPIs repo
    if current["kpis_repo"]["latest_commit"] != baselines["kpis_repo"]["latest_commit"]:
        drifts.append(
            f"KPIs: repo updated (latest commit: "
            f"{current['kpis_repo']['latest_commit']} on "
            f"{current['kpis_repo']['latest_commit_date']})"
        )

    return drifts


def main():
    update_mode = "--update-baselines" in sys.argv

    current = fetch_all()

    if update_mode:
        save_baselines(current)
        print("\nBaseline summary:")
        fw = current["framework_repo"]
        print(f"  Framework: {len(fw['capabilities_files'])} capabilities, "
              f"{len(fw['domains_files'])} domains")
        print(f"  FOCUS: release v{current['focus_repo']['latest_release']}, "
              f"working draft @ {current['focus_repo']['working_draft_commit']}")
        print(f"  KPIs: latest commit {current['kpis_repo']['latest_commit']} "
              f"({current['kpis_repo']['latest_commit_date']})")
        return

    baselines = load_baselines()
    if baselines is None:
        print("ERROR: No baselines found. Run with --update-baselines first.")
        sys.exit(1)

    print("\nComparing against baselines from", baselines.get("generated_at", "unknown"), "...")
    drifts = compare(current, baselines)

    if drifts:
        print(f"\n## Content Drift Detected ({len(drifts)} change(s))\n")
        for d in drifts:
            print(f"- {d}")
        print("\nRun `python scripts/check-freshness.py --update-baselines` after reviewing.")
        sys.exit(1)
    else:
        print("\nNo content drift detected — all repos match baselines.")
        sys.exit(0)


if __name__ == "__main__":
    main()
