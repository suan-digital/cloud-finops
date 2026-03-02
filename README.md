# Cloud FinOps Agent Skill

The FinOps Foundation framework transcribed and structured for AI agents. All reference content is sourced directly from Foundation repositories — no custom content. Installable in one command via [skills.sh](https://skills.sh).

## Quick Start

```bash
npx skills add suan-digital/cloud-finops
```

Works with Claude Code, Cursor, Codex, OpenCode, and [40+ other agents](https://skills.sh/docs/agents). See [INSTALLATION.md](INSTALLATION.md) for all methods.

## What It Does

This skill turns any AI agent into a FinOps advisor grounded in Foundation material:

- **Routes by business problem** — Condition-keyed routing loads only the capabilities needed. A targeted question loads 1-2 files, not the entire knowledge base.
- **Covers the full framework** — All domains and capabilities with Crawl/Walk/Run maturity criteria, plus all personas
- **Includes FOCUS billing spec** — Column definitions and data model for multi-cloud cost normalization
- **Waste sensor definitions** — Standardized waste sensors from the KPIs repo for identifying savings opportunities
- **Tracks upstream changes** — Git-based monitoring detects drift in Foundation repos, FOCUS spec releases, and KPI definitions

## Source Repositories

| Repo | Content | License |
|---|---|---|
| [finopsfoundation/framework](https://github.com/finopsfoundation/framework) | Capabilities, domains, personas | CC BY 4.0 |
| [FOCUS_Spec](https://github.com/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec) | Billing data specification | Community Specification License 1.0 |
| [finopsfoundation/kpis](https://github.com/finopsfoundation/kpis) | KPI definitions, waste sensors | CC BY-SA 4.0 |

## Sample Prompts

- **"Assess our FinOps maturity"** — Walks through all 18 capabilities using Crawl/Walk/Run criteria
- **"Our cloud bill is too high"** — Routes to utilization-efficiency + cost-allocation capabilities
- **"How should I structure Savings Plans?"** — Routes to manage-commitment-based-discounts capability
- **"We can't attribute costs to teams"** — Routes to cost-allocation + manage-shared-cloud-costs
- **"We had a cost spike last week"** — Routes to manage-anomalies capability
- **"Need to forecast next quarter"** — Routes to forecasting + budget-management capabilities
- **"Multi-cloud cost comparison"** — Routes to FOCUS spec + data-normalization capability
- **"Identify waste in our environment"** — Routes to waste sensors + utilization-efficiency

## Project Structure

```
cloud-finops/
├── skills/cloud-finops/
│   ├── SKILL.md                              ← Prompt + routing (only custom file)
│   └── references/
│       ├── capabilities/                     ← From framework repo
│       ├── domains/                          ← From framework repo
│       ├── personas.md                       ← From framework repo
│       ├── focus/
│       │   └── overview.md                   ← From FOCUS_Spec repo
│       └── kpis/
│           ├── kpi-definitions.md            ← From kpis repo
│           └── waste-sensors.md              ← From kpis repo
├── scripts/
│   ├── check-coverage.py                     ← Framework coverage validation
│   └── check-freshness.py                    ← Git-based content drift detection
├── .github/workflows/
│   └── content-monitoring.yml                ← Weekly CI (coverage + freshness)
├── coverage-matrix.yaml                      ← Framework element → file mapping
├── .content-baselines.json                   ← Git repo baselines for drift detection
├── .claude-plugin/marketplace.json           ← skills.sh marketplace config
├── INSTALLATION.md
├── CHANGELOG.md
└── LICENSE.md                                ← CC BY-SA 4.0
```

## Content Monitoring

Two scripts keep the skill aligned with upstream sources:

- **`check-coverage.py`** — Validates that every Foundation framework capability maps to a reference file. Checks for new capability files in the `finopsfoundation/framework` GitHub repo and verifies FOCUS spec version.
- **`check-freshness.py`** — Monitors three GitHub repos for content drift: framework capabilities/domains/personas, FOCUS releases and working draft, and KPI definitions. Compares against stored baselines.

Both run weekly via GitHub Actions. Drift triggers an auto-created issue.

## Contributing

See [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md). Contributions welcome — especially:
- Updated transcriptions when upstream repos change
- Bug fixes in monitoring scripts

## License

CC BY-SA 4.0 — See [LICENSE.md](LICENSE.md)
