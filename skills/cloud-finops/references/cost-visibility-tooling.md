# Cost Visibility & Tooling

The gap between seeing costs and acting on them is where most organizations stall.

## The Visibility Gap

### What Broken Looks Like

- Cost data lives in spreadsheets, exported monthly
- Only finance or FinOps can access cost dashboards
- Attribution requires manual investigation for each anomaly
- Cost anomalies are discovered at monthly billing, not in real-time
- Engineers have no visibility into the cost of their services
- Multi-cloud cost data requires manual normalization

### What Good Looks Like

- Cost queries happen in natural language, not spreadsheet archaeology
- Attribution is automatic through consistent tagging and labeling
- Anomalies trigger alerts within hours, not billing cycles
- Optimization recommendations come with one-click or automated execution
- Multi-cloud data is normalized to a common schema (FOCUS)
- Engineers can see cost impact before code merges

## Tool Categories

### Native Cloud Cost Tools

Every cloud provider includes cost management tools. Start here before adding third-party tools.

| Provider | Cost Tool | Strengths | Limitations |
|---|---|---|---|
| **AWS** | Cost Explorer, CUR, Budgets | Deep AWS data, CUR for analytics | AWS-only, complex CUR schema |
| **Azure** | Cost Management + Billing | Good Azure data, built-in budgets | Azure-focused, limited cross-cloud |
| **GCP** | Cloud Billing, BigQuery export | SQL-queryable, good dashboards | GCP-focused |
| **OCI** | Cost Analysis, Budgets | Oracle workload visibility | OCI-only, limited ecosystem |

**When native tools suffice:**
- Single cloud provider
- Basic cost visibility needs
- Small to medium spend (<$100K/month)
- Engineering team comfortable with cloud consoles

### Third-Party FinOps Platforms

| Tool | Strengths | Best For |
|---|---|---|
| **CloudHealth (VMware)** | Multi-cloud, policy engine, governance | Enterprise multi-cloud |
| **Spot.io (NetApp)** | Spot instance management, container optimization | Kubernetes, auto-scaling |
| **Kubecost** | Kubernetes-specific cost allocation | K8s environments |
| **Vantage** | Developer-friendly, clean UI, multi-cloud | Engineering-led FinOps |
| **CloudZero** | AI cost tracking, unit economics | AI-heavy workloads |
| **Infracost** | PR-time cost estimation, shift-left | Engineering CI/CD integration |
| **Apptio Cloudability** | Enterprise governance, forecasting | Large enterprise |
| **nOps** | AWS optimization, automated savings | AWS-focused mid-market |
| **CAST AI** | Kubernetes auto-optimization | K8s cost automation |

**When to add third-party:**
- Multi-cloud environment
- Need for automated optimization (not just visibility)
- Kubernetes cost allocation required
- Spend exceeds $100K/month (ROI justifies tool cost)
- Engineering needs self-service cost access

### Open-Source FinOps Tools

Free and community-maintained tools for cost visibility — especially valuable for organizations
at Foundation (Shu) maturity or with limited tooling budgets.

| Tool | Focus | License | Strengths |
|---|---|---|---|
| **OpenCost** | Kubernetes cost monitoring | Apache 2.0 | CNCF Sandbox project, real-time K8s cost allocation, Prometheus integration |
| **Cloud Carbon Footprint** | Carbon emissions estimation | Apache 2.0 | Multi-cloud carbon tracking, visualization dashboard |
| **Komiser** | Multi-cloud cost visibility | Elastic License 2.0 | Cloud resource inventory, cost insights, 100+ cloud services |
| **Infracost (Community)** | IaC cost estimation | Apache 2.0 | PR-time cost diffs for Terraform, free for open-source projects |

**OpenCost vs. Kubecost — when to upgrade:**

| Capability | OpenCost (free) | Kubecost (commercial) |
|---|---|---|
| Real-time cost allocation | Yes | Yes |
| Namespace/label cost breakdown | Yes | Yes |
| Multi-cluster visibility | Limited | Yes (unified view) |
| Savings recommendations | No | Yes |
| Alerting and governance | Basic | Advanced |
| Cloud cost integration (non-K8s) | No | Yes |
| Support | Community | Commercial SLA |

**Start with OpenCost** if you run Kubernetes and need cost allocation without budget for
commercial tools. Upgrade to Kubecost when you need multi-cluster views, automated savings
recommendations, or commercial support.

### Shift-Left Cost Tools

Cost visibility at the point of decision — before code merges.

| Tool | Integration | Capability |
|---|---|---|
| **Infracost** | GitHub/GitLab PR comments | Cost diff on infrastructure changes |
| **env0** | Terraform collaboration | Cost estimation + policy enforcement |
| **Spacelift** | IaC management | Cost policies in deployment pipeline |
| **Terraform Cloud** | HashiCorp | Cost estimation (via Sentinel) |

Adoption of shift-left cost tools mirrors security scanning a decade ago.

### AI-Powered Cost Tools

Emerging category using AI agents for cost management.

**AWS MCP Server:**
- Enables AI agents to query 15,000+ AWS APIs including cost management
- Natural language cost queries: "What drove the 15% increase in EC2 costs last week?"
- Automated optimization execution with approval workflow
- CloudTrail audit logging for compliance

**Capabilities of AI-powered cost tools:**
- Conversational cost queries (replace dashboard navigation)
- Automated anomaly investigation (not just detection)
- Optimization recommendation + execution
- Cross-service correlation (connect cost to performance data)

### FOCUS-Compatible Tools

The FinOps Open Cost & Usage Specification (FOCUS) normalizes cost data across providers.

**FOCUS-native data sources:**
- AWS CUR 2.0 (FOCUS-compatible)
- Azure Cost Management export (FOCUS-compatible)
- GCP BigQuery export (mapping available)

**Benefits of FOCUS adoption:**
- Single schema for multi-cloud cost data
- Standardized column names (BilledCost, EffectiveCost, UsageQuantity)
- Enables apples-to-apples comparison across providers
- Reduces custom ETL for multi-cloud analytics

## Building a Cost Visibility Stack

### Maturity-Appropriate Tooling

**Shu (Foundation):**
- Native cloud cost tools (free, already available)
- OpenCost for Kubernetes cost allocation (free, low setup effort)
- Basic alerting (budget thresholds, anomaly detection)
- Manual cost review cadence (weekly)
- Tag coverage reporting

**Ha (Automation):**
- Add Infracost for PR-time visibility
- Add Kubecost if running Kubernetes
- Implement automated anomaly alerting
- Build cost dashboards per team (Grafana, native tools, or third-party)
- Consider FOCUS adoption for multi-cloud

**Ri (Embedded):**
- AI-powered cost querying (MCP servers)
- Automated optimization execution
- Self-service cost analytics for all engineers
- Unit economics dashboards tied to business metrics
- Carbon metrics alongside cost

### Implementation Priority

| Priority | Action | Effort | Impact |
|---|---|---|---|
| 1 | Enable native cloud cost tools | Low | Foundation |
| 2 | Set up budget alerts and anomaly detection | Low | Prevent surprises |
| 3 | Implement tagging standards | Medium | Enable attribution |
| 4 | Add shift-left tooling (Infracost) | Low-Medium | Engineer awareness |
| 5 | Add OpenCost (if K8s, budget-constrained) | Low | Free K8s cost visibility |
| 6 | Build team-level cost dashboards | Medium | Accountability |
| 7 | Upgrade to Kubecost (if outgrowing OpenCost) | Medium | Advanced K8s visibility |
| 8 | Implement FOCUS (if multi-cloud) | Medium | Normalization |
| 9 | Deploy AI-powered cost tools | Medium-High | Conversational access |

## Anomaly Detection

### Alert Configuration

| Alert Type | Threshold | Action |
|---|---|---|
| Budget threshold | 80% of monthly budget | Notification to team lead |
| Budget exceeded | 100% of budget | Notification to FinOps + manager |
| Daily anomaly | >20% increase vs. trailing average | Automated investigation trigger |
| Service spike | >50% increase in single service | Immediate notification |
| New high-cost resource | Any resource >$100/day | Review request |

### Anomaly Response Protocol

1. **Detect** — Automated alert fires (target: <1 hour from anomaly)
2. **Triage** — Is this expected? (Deployment, traffic spike, data migration)
3. **Investigate** — What changed? (CloudTrail, deployment logs, PR history)
4. **Act** — Remediate if unexpected (revert, scale down, fix configuration)
5. **Learn** — Update alerts, add prevention (policy, budget, governance)

**Target response time:** Investigation started within 4 hours of alert. For enterprise spend,
cost anomalies should be treated like production incidents.

## Assessment Questions

1. Can anyone query costs conversationally, or is it locked behind specialized tools?
2. Is attribution granular enough? (By team, service, feature, customer tier)
3. How fast from cost anomaly to investigation? Hours? Days? Next month?
4. Are cost insights actionable or just informational?
5. Is cost data normalized across providers? (FOCUS spec adoption)
6. Is cost visible at PR time? (Shift-left tooling)
7. Can engineers see their service costs without asking FinOps?
8. What's the cost of the cost tools? (Tool ROI)
9. Are AI/ML costs visible separately from infrastructure costs?
10. Is there an anomaly response protocol?
11. Have open-source options (OpenCost, Infracost Community) been evaluated before committing to commercial tools?

## Tool Selection Decision Tree

```
Single cloud or multi-cloud?
├── Single cloud:
│   ├── Spend <$100K/month → Native tools + Infracost + OpenCost (if K8s)
│   └── Spend >$100K/month → Native tools + Infracost + consider third-party
└── Multi-cloud:
    ├── Kubernetes-heavy → OpenCost or Kubecost + Vantage or CloudHealth
    ├── AI-heavy → CloudZero or custom + Infracost
    └── Enterprise governance → CloudHealth or Apptio + Infracost

All paths: Add FOCUS normalization when ready.
```