# Azure Cost Optimization Reference

Comprehensive Azure-specific FinOps patterns covering Cost Management, commitment instruments,
service-level optimization, and architectural patterns.

## Azure Billing Data

### Cost Management + Billing

Azure's built-in cost management platform.

**Key features:**
- Cost analysis with custom views, filters, and groupings
- Budget alerts with action groups
- Advisor recommendations for right-sizing and commitments
- Export to storage account for custom analytics
- FOCUS-compatible export format

**Cost analysis views:**
| View | Purpose |
|---|---|
| Accumulated cost | Month-to-date spend trending |
| Daily cost | Day-by-day breakdown for anomaly detection |
| Cost by resource | Identify top-spending resources |
| Cost by resource group | Team/project attribution |
| Cost by service | Service-level spending patterns |

### Cost Exports

Export billing data for custom analytics:

- **Amortized cost** — Spreads commitment costs across usage period
- **Actual cost** — Shows actual charges as billed
- **FOCUS export** — Standardized format for multi-cloud

**Best practice:** Export daily to Storage Account, build Power BI dashboards or query with
Azure Data Explorer.

### Azure Advisor

Free recommendations across five categories:

| Category | Cost-Relevant Recommendations |
|---|---|
| Cost | Right-size VMs, unused resources, reservation opportunities |
| Reliability | May conflict with cost (redundancy costs money) |
| Performance | Sometimes aligns with cost (efficient = cheaper) |
| Security | Rarely cost-relevant |
| Operational Excellence | Tagging, governance |

## Commitment Instruments

### Azure Reservations

| Resource Type | Discount | Term |
|---|---|---|
| Virtual Machines | 30-72% | 1 or 3 year |
| SQL Database | 30-65% | 1 or 3 year |
| Cosmos DB | 25-65% | 1 or 3 year |
| Azure Synapse | 25-65% | 1 or 3 year |
| App Service | 30-55% | 1 or 3 year |
| Azure Cache for Redis | 30-55% | 1 or 3 year |
| Managed Disks | 20-40% | 1 or 3 year |

**Reservation scope:**
- **Shared** — Applies across all subscriptions in billing account
- **Single subscription** — Only applies to one subscription
- **Resource group** — Most restrictive scope

**Best practice:** Use Shared scope for maximum flexibility.

### Azure Savings Plans

| Type | Discount | Flexibility |
|---|---|---|
| **Compute SP** | Up to 65% | Any VM family, size, region, OS |
| **Azure Savings Plan for Compute** | Up to 65% | VMs, App Service, Container Instances, Functions |

**Strategy:** Layer reservations (deep discount, specific) with Savings Plans (moderate discount,
flexible).

### Azure Hybrid Benefit

Bring existing Windows Server and SQL Server licenses to Azure:

| License | Savings |
|---|---|
| Windows Server | Up to 40% on VMs |
| SQL Server | Up to 55% on SQL Database/MI |
| Combined (Windows + SQL) | Up to 80% |

**Don't forget:** Track license availability and Azure Hybrid Benefit utilization.

### Enterprise Agreements & MACC

- **Enterprise Agreement (EA):** Volume pricing, commitment discounts
- **Microsoft Azure Consumption Commitment (MACC):** Spend commitment for additional discounts
- **CSP:** Cloud Solution Provider pricing (partner-managed)

## Service-Level Optimization Patterns

### Virtual Machines

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Right-size based on Advisor | 20-40% | M | Azure Advisor provides specific recommendations |
| B-series for variable workloads | 30-50% | S | Burstable VMs for dev, low-traffic services |
| Spot VMs for fault-tolerant | 60-90% | M | Batch processing, CI/CD, stateless workers |
| Dev/Test pricing | 40-60% | S | Use Dev/Test subscriptions for non-prod |
| Auto-shutdown for dev/test | 50-70% | S | Azure DevTest Labs or Automation |
| Constrained vCPU sizes | 25-50% | S | Same memory, fewer CPUs (e.g., Standard_E8-2s_v5) |

### Azure Storage

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Cool/Archive tiers | 50-90% | S | Based on access patterns |
| Lifecycle management | 30-60% | S | Auto-tier based on last access time |
| Reserved capacity | 25-38% | S | 1-year commitment for predictable storage |
| Delete soft-deleted blobs | Variable | S | Soft-delete retains data at cost |
| Premium → Standard for cold data | 60-80% | M | Premium SSD unnecessary for cold data |

### Azure SQL / Cosmos DB

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Elastic pools | 20-40% | M | Share resources across databases |
| Serverless tier | 30-60% | S | Auto-pause for intermittent workloads |
| Reserved capacity | 30-65% | S | Stable production databases |
| DTU → vCore (or reverse) | 10-30% | M | Choose model matching workload pattern |
| Cosmos DB autoscale | 20-40% | S | vs. manual throughput provisioning |
| Cosmos DB serverless | 50-70% | S | Low-traffic workloads |

### AKS (Azure Kubernetes Service)

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Spot node pools | 60-90% | M | Non-critical workloads |
| Cluster auto-scaler | 20-40% | M | Right-size node count dynamically |
| Virtual nodes (ACI) | Variable | M | Burst to serverless containers |
| Right-size pods | 20-40% | M | VPA or manual optimization |
| Karpenter (preview) | 20-40% | M | Better bin-packing |

### Azure Functions

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Consumption vs. Premium plan | 30-60% | S | Consumption for intermittent, Premium for steady |
| Optimize execution time | 10-30% | M | Reduce duration = reduce cost |
| Durable Functions optimization | Variable | M | Minimize orchestrator replays |
| Connection reuse | 10-20% | S | Static HTTP clients, connection pooling |

### Data Services

| Service | Optimization Patterns |
|---|---|
| **Synapse Analytics** | Pause dedicated SQL pools when idle, use serverless for ad-hoc |
| **Databricks** | See `data-databricks.md` |
| **Data Factory** | Self-hosted IR for high-volume, optimize pipeline triggers |
| **Event Hubs** | Right-size throughput units, use auto-inflate |
| **Service Bus** | Basic vs. Standard vs. Premium tier selection |

### Networking

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Private Endpoints | 10-30% less than NAT/public | M | Also improves security |
| VNet peering vs. VPN | Variable | M | Peering is simpler and cheaper |
| Bandwidth reservation | 5-20% | S | For predictable egress |
| Azure CDN/Front Door | Variable | M | Reduce origin load and egress |
| Minimize cross-region traffic | $0.02/GB savings | M | Co-locate related services |

## Azure-Specific Cost Patterns

### Resource Group Organization

Use resource groups for cost attribution:
- One resource group per service/application per environment
- Tag resource groups (tags don't inherit to resources automatically — use Azure Policy)
- Resource group = cost allocation boundary

### Management Group Hierarchy

Use management groups for governance at scale:
```
Root Management Group
├── Production
│   ├── Business Unit A
│   └── Business Unit B
├── Non-Production
│   ├── Development
│   └── Staging
└── Sandbox
```

Apply policies at management group level for consistent governance.

### Azure Policy for Cost

| Policy | Purpose |
|---|---|
| Require tags on resources | Cost attribution |
| Restrict VM sizes | Prevent expensive instances |
| Restrict regions | Minimize data transfer, compliance |
| Audit unused resources | Waste detection |
| Enforce auto-shutdown | Non-production cost control |

## PTU (Provisioned Throughput Units) — Azure OpenAI

See `ai-azure-openai.md` for Azure OpenAI-specific PTU optimization.

## Azure-Specific Tools

| Tool | Purpose | Cost |
|---|---|---|
| **Cost Management + Billing** | Built-in cost analysis | Free |
| **Azure Advisor** | Optimization recommendations | Free |
| **Azure Migrate** | Assessment for migration pricing | Free |
| **Azure Pricing Calculator** | Pre-deployment cost estimation | Free |
| **Azure Hybrid Benefit calculator** | License savings estimation | Free |

## Assessment Checklist

- [ ] Cost Management exports configured (daily, amortized)
- [ ] Budgets set with action group alerts
- [ ] Azure Advisor recommendations reviewed (Cost category)
- [ ] Reservations in place for stable workloads
- [ ] Azure Hybrid Benefit applied where licenses exist
- [ ] Dev/Test pricing used for non-production
- [ ] Auto-shutdown configured for dev/test VMs
- [ ] Storage lifecycle policies in place
- [ ] Resource group structure supports cost attribution
- [ ] Azure Policy enforcing tagging and sizing limits