# Intake Protocol

Before analysis, gather context. Ask these questions conversationally — skip any the user has
already answered or that clearly don't apply to their situation.

**Important:** Do not generate a report without sufficient context. If the user jumps straight
to "optimize my costs," guide them through intake first. The intake determines which analysis
dimensions matter and which reference files to route to.

## Question Categories

### 1. Environment & Scale

These questions determine the provider-specific references and adaptation patterns to apply.

- **Which cloud providers?** (AWS, Azure, GCP, OCI, multi-cloud)
- **Approximate monthly cloud spend?** (Helps determine spend tier: startup <$50K, mid-market $50K-$500K, enterprise $500K+)
- **How many engineering teams consume cloud resources?**
- **What's the primary workload type?** (SaaS, data platform, ML/AI, internal tools, e-commerce, media/streaming)
- **Multi-account or single-account structure?**
- **How many cloud accounts/subscriptions/projects total?**
- **Multi-cloud strategy?** (Intentional multi-cloud with governance, or organic sprawl across providers?)
- **Kubernetes in use?** (Managed K8s like EKS/AKS/GKE, self-hosted, namespace-per-team, cluster-per-team?)

### 2. Architecture & Infrastructure

These questions reveal architectural cost drivers and determine which analysis dimensions will
yield the highest-impact findings.

- **Deployment model?** (Kubernetes, serverless, VMs, hybrid, PaaS)
- **Infrastructure as Code in use?** (Terraform, Pulumi, CloudFormation, CDK, Bicep, none)
- **Microservices or monolith?** How many services approximately?
- **Multi-region or single-region?** If multi-region, is it for DR, latency, or compliance?
- **Data architecture?** (Data warehouse, data lake, lakehouse, streaming)
- **Key databases?** (RDS/Aurora, DynamoDB, CosmosDB, BigQuery, Snowflake, Databricks)
- **CDN or edge compute in use?** (CloudFront, Akamai, Cloudflare)
- **CI/CD pipeline?** (GitHub Actions, GitLab CI, Jenkins, CircleCI)

### 3. AI/ML Workloads

Skip this section if the organization has no AI/ML workloads. These questions route to the
AI-specific analysis dimensions and reference files.

- **Running LLMs, ML models, or AI agents in production?**
- **Which models or providers?** (OpenAI, Anthropic/Claude, self-hosted, fine-tuned, Bedrock, Azure OpenAI, Vertex)
- **How many agentic workflows or AI-powered features?**
- **Current monthly AI/inference spend (if known)?**
- **AI deployment pattern?** (API calls to hosted models, self-hosted inference, hybrid)
- **GPU infrastructure?** (On-demand, reserved, spot/preemptible, provisioned throughput)
- **Using RAG, fine-tuning, or both?**
- **How is AI usage metered and attributed?** (Per team, per feature, per customer, not tracked)

### 4. Current FinOps Practices

These questions determine the organization's FinOps maturity stage and identify gaps in
existing practices.

- **Dedicated FinOps team or role?** (Dedicated team, part-time role, nobody, shared with DevOps/platform)
- **Cost visibility tools in use?** (Native cloud tools only, Kubecost, CloudHealth, Spot.io, Infracost, Vantage, CloudZero, FOCUS-compliant tools)
- **Tagging coverage estimate?** (<50%, 50-80%, 80%+)
- **Commitment instruments in place?** (Reserved Instances, Savings Plans, CUDs, none, don't know)
- **Commitment utilization rate?** (If commitments exist, what % is utilized?)
- **Chargeback or showback in place?** (Full chargeback, showback reports, nothing)
- **Cost anomaly detection?** (Automated alerts, manual review, billing surprises)
- **Budget forecasting approach?** (Data-driven, historical trend, guesswork, none)
- **Unit economics tracked?** (Cost per request, per user, per transaction, none)
- **Previous optimization attempts?** What worked, what regressed, what was abandoned?
- **Existing tool contracts?** (Locked into CloudHealth for 2 years, committed to Datadog, etc.)
- **Who can actually make infrastructure changes?** (Change management process, approval gates, CAB reviews?)

### 5. Organizational Context

These questions shape the communication approach and determine realistic recommendations.

- **Company size and growth stage?** (Startup, scale-up, mid-market, enterprise)
- **Approximate headcount?** (Engineering team size matters for implementation capacity)
- **Growth trajectory?** (Stable, moderate growth, hypergrowth, contraction)
- **Regulatory requirements?** (SOC 2, HIPAA, FedRAMP, PCI DSS, GDPR, ISO 27001)
- **Sustainability goals or carbon reporting requirements?** (ESG commitments, CSRD, voluntary reporting, none)
- **Recent or planned migrations?** (On-prem to cloud, cloud-to-cloud, replatforming)
- **Budget cycle?** (When are cloud commitments typically negotiated?)

### 6. Pain Points & Goals

These open-ended questions surface the business problem that drives routing in the analysis.

- **What triggered this conversation?** (Bill shock, board pressure, new CFO, compliance requirement, optimization initiative)
- **Top 3 pain points with current cloud spending?**
- **What does success look like?** (% reduction target, visibility goal, governance goal, sustainability target)
- **Any past optimization efforts?** What worked, what didn't?
- **Timeline expectations?** (Quick wins needed now, 90-day roadmap, annual strategy)
- **Internal politics or blockers?** (Engineering pushback on optimization, vendor relationships that constrain choices, org changes in progress?)
- **Budget owner?** (Who approves cloud spend changes? This determines whether recommendations are actionable or aspirational.)

## File Analysis

If the user provides files, analyze them using the protocols in `file-analysis.md`. Supported
file types:

| File Type | What to Look For |
|---|---|
| Terraform / IaC | Instance sizes, storage config, auto-scaling, region choices, missing tags |
| Kubernetes manifests | Resource requests vs. limits, replica counts, node pools, spot usage |
| Cloud bills / Cost reports | Top spend categories, untagged spend, data transfer, idle patterns |
| Architecture documents | Sync vs. async patterns, data retention, caching, observability cost |
| Cost Explorer exports | Trends, anomalies, commitment utilization, service breakdown |

## After Intake

Once you have sufficient context:

1. **Determine spend tier** — routes to appropriate depth in `adaptation-patterns.md`
2. **Determine AI maturity** — determines whether to apply AI analysis dimensions
3. **Identify business problem** — routes to primary and supporting reference files
4. **Assess FinOps maturity** — informs the Shuhari stage assessment
5. **Begin analysis** — apply the 8 dimensions using routed reference files