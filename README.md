# Cloud FinOps Agent Skill

**Give any LLM structured FinOps domain knowledge.** Cloud cost optimization, AI economics, and the FinOps Foundation framework — installable in one command.

## Quick Start

```bash
npx skills add suan-digital/cloud-finops-agent-skill
```

Works with Claude Code, Cursor, Codex, OpenCode, and 40+ other agents. See [INSTALLATION.md](INSTALLATION.md) for all installation methods.

## What This Does

Drop this skill into any LLM-powered development environment and it becomes a FinOps advisor that:

- **Asks before prescribing** — Structured intake protocol gathers context before analysis
- **Assesses maturity** — Shuhari (守破離) framework goes deeper than Crawl-Walk-Run
- **Routes by business problem** — "Our AI costs are out of control" triggers different references than "We need a commitment strategy"
- **Applies 8 analysis dimensions** — From FinOps practice assessment to GreenOps waste remediation
- **Outputs structured reports** — 9-section template that executives can forward to their CFO
- **Knows provider specifics** — AWS, Azure, GCP, OCI, plus AI providers and data platforms

## Coverage

### Reference Files

| Category | Files | Topics |
|---|---|---|
| **Methodology** | 6 | Advisory principles, intake protocol, output format, file analysis, adaptation patterns, Suan methodology |
| **Framework** | 3 | Shuhari maturity, architecture-cost alignment, FinOps Foundation (22 capabilities) |
| **AI Economics** | 4 | Hidden 4-5x cost multiplier, inference economics (5-lever playbook), GenAI capacity planning, AI value governance |
| **Operations** | 3 | GreenOps 8-fix playbook, tagging governance, cost visibility tooling |
| **Cloud Providers** | 4 | AWS (100+ patterns), Azure (40+ patterns), GCP (25+ patterns), OCI |
| **AI Providers** | 4 | Anthropic/Claude, AWS Bedrock, Azure OpenAI, Google Vertex AI |
| **Data Platforms** | 2 | Databricks (DBU optimization), Snowflake (credit optimization) |

### 8 Analysis Dimensions

| Dimension | Key Question |
|---|---|
| FinOps Practice Assessment | Which of 22 capabilities are gaps? |
| Phase Positioning | Inform → Optimize → Operate — where stuck? |
| Maturity Assessment | Shu / Ha / Ri — which stage? |
| Architecture-Cost Alignment | Is cost a first-class design constraint? |
| AI Cost Visibility | Is the 4-5x hidden cost known? |
| Inference Economics | Model routing, caching, attribution? |
| Waste Remediation | Which GreenOps fixes apply? |
| Cost Visibility & Tooling | Can anyone query costs conversationally? |

## What Makes This Different

| Dimension | Other FinOps Skills | This Skill |
|---|---|---|
| **Entry point** | Jump to domain reference | Intake protocol — ask first |
| **Routing** | By provider/technology | By business problem first, then provider |
| **Maturity model** | Crawl/Walk/Run | Shuhari 守破離 (philosophical depth) |
| **Cost philosophy** | "Optimize existing spend" | "80% locked at design time — design for cost" |
| **AI costs** | Token pricing only | 4-5x total cost multiplier (hidden costs) |
| **Output** | Unstructured | 9-section report template |
| **File analysis** | None | Terraform, K8s, bills, architecture docs |
| **Adaptation** | One-size-fits-all | By spend tier + AI maturity |

## Sample Prompts

Try these after installation:

- **"Assess our FinOps maturity"** → Triggers intake protocol + Shuhari assessment
- **"Our AWS bill is $80K/month, too high"** → Triggers intake + AWS-specific + architecture-cost analysis
- **"AI inference costs are out of control"** → Triggers intake + inference economics + AI cost visibility
- **"Review this Terraform file for cost issues"** → File analysis protocol
- **"We need a commitment strategy for Azure"** → Azure-specific + finops framework

## Project Structure

```
cloud-finops-agent-skill/
├── README.md               ← You are here
├── INSTALLATION.md         ← Install methods
├── LICENSE.md              ← CC BY-SA 4.0
├── CHANGELOG.md            ← Version history
├── .github/
│   └── CONTRIBUTING.md     ← How to contribute
└── skills/
    └── cloud-finops/
        ├── SKILL.md        ← Entry point
        └── references/     ← Domain reference files
```

## Contributing

See [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md). Contributions welcome — especially:
- Updated pricing data
- New optimization patterns from real engagements
- Additional provider coverage
- Translations

## License

CC BY-SA 4.0 — See [LICENSE.md](LICENSE.md)

**Attribution:** When using or adapting this skill, credit [Suan Digital](https://suan.digital).

## About Suan Digital

Cloud & AI Advisory. Less burn. More return.

We help enterprises make smarter technology investments. Cloud and AI solutions that scale. Spend that actually delivers.

- Website: [suan.digital](https://suan.digital)
- Contact: [suan.digital/contact](https://suan.digital/contact)
- Blog: [suan.digital/posts](https://suan.digital/posts)
