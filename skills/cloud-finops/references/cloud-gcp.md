# GCP Cost Optimization Reference

Google Cloud Platform-specific FinOps patterns covering billing, commitment instruments,
service-level optimization, and BigQuery cost management.

## GCP Billing Data

### Cloud Billing Export

Export billing data to BigQuery for custom analytics.

**Export types:**
| Export Type | Content | Best For |
|---|---|---|
| Standard usage cost | Billing-level data | Basic cost tracking |
| Detailed usage cost | Resource-level data | Deep analysis |
| Pricing export | SKU pricing data | Custom cost modeling |

**Best practice:** Enable detailed usage cost export to BigQuery. Query with SQL for custom
analysis. Build Looker Studio dashboards from BigQuery views.

### Cloud Billing Reports

Built-in reporting in the console:

- Cost breakdown by project, service, SKU
- Cost trends over time
- Forecasted spend
- Credit and discount tracking
- Label-based filtering

### Budgets & Alerts

| Feature | Configuration |
|---|---|
| Budget alerts | Email, Pub/Sub, Cloud Function triggers |
| Programmatic budgets | Budget API for automated management |
| Threshold actions | Trigger Cloud Functions for automated response |

**Best practice:** Set budgets at project level. Use Pub/Sub + Cloud Functions for automated
response to budget alerts (e.g., disable billing API for sandbox projects).

## Commitment Instruments

### Committed Use Discounts (CUDs)

| Type | Discount | Flexibility |
|---|---|---|
| **Spend-based CUD** | Up to 25% | Any eligible service, flexible |
| **Resource-based CUD** | Up to 57% | Specific machine type, region |

**CUD comparison to AWS:**
| Aspect | GCP CUD | AWS Savings Plan |
|---|---|---|
| Discount depth | 25-57% | 40-72% |
| Flexibility | Spend-based is very flexible | Compute SP is flexible |
| Term | 1 or 3 year | 1 or 3 year |
| Payment | Monthly or upfront | All upfront, partial, no upfront |

**Strategy:**
- **Resource-based CUDs** for known, stable Compute Engine workloads (deeper discount)
- **Spend-based CUDs** for variable or multi-service workloads (more flexibility)
- Layer both for optimal coverage

### Sustained Use Discounts (SUDs)

Automatic discounts for Compute Engine instances running more than 25% of the month.

| Usage (% of month) | Effective Discount |
|---|---|
| 25% | Starts applying |
| 50% | ~12% effective |
| 75% | ~20% effective |
| 100% | ~30% effective |

**Key:** SUDs are automatic — no action required. They stack with CUDs. Factor them into
commitment calculations (don't double-count savings).

**Note:** SUDs do NOT apply to E2, N2D, or A2/A3 machine types. Check current eligibility.

## Service-Level Optimization Patterns

### Compute Engine

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Right-size VMs | 20-40% | M | Use Recommender Hub, Cloud Monitoring |
| Preemptible/Spot VMs | 60-91% | M | Batch processing, CI/CD, fault-tolerant |
| Custom machine types | 5-30% | S | Exact vCPU/memory ratio for workload |
| Sole-tenant nodes | Variable | M | When licensing requires dedicated hardware |
| T2A (Arm) instances | 20-40% | M | Arm-based, compatible workloads |

**GCP-specific advantage:** Custom machine types let you specify exact vCPU and memory, avoiding
the over-provisioning inherent in predefined sizes.

### GKE (Google Kubernetes Engine)

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Autopilot mode | 20-40% | M | Google manages nodes, pay per pod |
| Spot pods | 60-90% | M | For fault-tolerant workloads |
| Cluster autoscaler | 20-40% | M | Right-size node count |
| Right-size pods | 20-40% | M | VPA or manual optimization |
| Multi-zonal vs. regional | Variable | S | Regional for HA, multi-zonal for cost |

**GKE Autopilot:** Google manages the nodes, you only define pods. Can be more cost-efficient
than self-managed nodes because bin-packing is optimized.

### BigQuery

BigQuery cost management is critical for GCP-heavy organizations. It's often the top 3 cost
item.

**Pricing models:**
| Model | Best For | Cost |
|---|---|---|
| On-demand | Unpredictable queries | $6.25/TB scanned |
| Editions (Standard/Enterprise/Enterprise Plus) | Predictable, high-volume | Slot-based pricing |

**Optimization patterns:**

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Partition tables | 30-60% | M | Partition by date, reduce data scanned |
| Cluster tables | 10-30% | M | Co-locate related rows, reduce scan |
| Use columnar projections | 20-50% | S | `SELECT specific_columns` not `SELECT *` |
| Set query cost limits | Prevention | S | `maximum_bytes_billed` parameter |
| Use materialized views | 30-60% | M | Pre-compute frequent aggregations |
| Move to Editions (if high-volume) | 20-40% | M | Flat-rate better when scans exceed threshold |
| BI Engine | 30-50% | M | In-memory acceleration for dashboards |
| Storage pricing (long-term) | 50% | Automatic | Data not modified for 90 days |

**Key query cost optimization:**
```sql
-- Bad: Scans entire table
SELECT * FROM `project.dataset.large_table`

-- Good: Partitioned + specific columns
SELECT user_id, event_type, revenue
FROM `project.dataset.large_table`
WHERE DATE(timestamp) BETWEEN '2026-01-01' AND '2026-01-31'
  AND country = 'US'
```

### Cloud Storage

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Nearline (30-day minimum) | 50% vs. Standard | S | Infrequent access data |
| Coldline (90-day minimum) | 75% vs. Standard | S | Rare access data |
| Archive (365-day minimum) | 90% vs. Standard | S | Compliance, long-term retention |
| Autoclass | Variable | S | Automatic tier management |
| Lifecycle policies | 30-70% | S | Auto-transition based on age |
| Object Versioning review | Variable | S | Old versions accumulate cost |

### Cloud SQL / Spanner / AlloyDB

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Right-size instances | 20-40% | M | Recommender Hub provides guidance |
| HA only for production | 50% of standby cost | S | Non-prod doesn't need HA |
| CUDs for stable databases | 25-57% | S | For production databases |
| Cloud SQL Serverless | Variable | M | Auto-scaling for variable workloads |
| Stop non-production instances | 50-70% | S | Schedule stop for dev databases |

### Cloud Functions / Cloud Run

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Min instances review | Variable | S | Zero min-instances for low-traffic |
| Memory/CPU right-sizing | 10-30% | S | Match to actual usage |
| Concurrency optimization | 10-30% | M | Higher concurrency = fewer instances |
| Cold start vs. min instances trade-off | Variable | M | Balance latency and cost |

### Networking

| Transfer Type | Cost | Optimization |
|---|---|---|
| Same-zone | Free | Co-locate services |
| Cross-zone (same region) | $0.01/GB | Minimize where possible |
| Cross-region | $0.01-$0.08/GB | Reduce unnecessary replication |
| Internet egress | $0.08-$0.12/GB | CDN, caching, compression |
| Private Google Access | Free | Access Google APIs without NAT |
| Cloud Interconnect | Reduced egress | For high-volume connections |

### Data Services

| Service | Key Optimization |
|---|---|
| **Dataflow** | Right-size workers, use Streaming Engine, autoscaling |
| **Dataproc** | Preemptible workers, autoscaling, ephemeral clusters |
| **Pub/Sub** | Right-size throughput, use Lite for high-volume |
| **Vertex AI** | See `ai-vertex.md` |

## GCP-Specific Patterns

### Project Organization

```
Organization
├── Folder: Production
│   ├── Project: prod-api
│   └── Project: prod-data
├── Folder: Non-Production
│   ├── Project: dev-api
│   └── Project: staging-api
└── Folder: Sandbox
    └── Project: sandbox-experiments
```

**Best practice:** One project per service per environment. Apply billing budgets per project.
Use folders for hierarchical governance.

### Labels (GCP's Tags)

GCP uses "labels" (equivalent to AWS tags). Apply to all resources.

**Limitation:** Labels have a 63-character limit for both key and value. Plan taxonomy
accordingly. See `tagging-governance.md` for standards.

### Organization Policies

| Policy | Purpose |
|---|---|
| Restrict VM sizes | Prevent expensive instance types |
| Restrict regions | Minimize data transfer, compliance |
| Disable serial port | Security + prevent unauthorized access |
| Require labels | Cost attribution enforcement |

## GCP-Specific Tools

| Tool | Purpose | Cost |
|---|---|---|
| **Cloud Billing Reports** | Built-in cost analysis | Free |
| **Recommender Hub** | Right-sizing, commitment recommendations | Free |
| **Active Assist** | AI-driven optimization recommendations | Free |
| **Carbon Footprint** | Project-level carbon metrics | Free |
| **Billing BigQuery Export** | Custom analytics | BigQuery query costs |

## Assessment Checklist

- [ ] Billing export to BigQuery enabled (detailed usage)
- [ ] Budgets set per project with Pub/Sub alerts
- [ ] CUDs in place for stable workloads
- [ ] SUDs understood and factored into analysis
- [ ] Recommender Hub reviewed regularly
- [ ] BigQuery partitioning and clustering in place
- [ ] Labels applied consistently across projects
- [ ] Preemptible/Spot VMs used for eligible workloads
- [ ] Storage lifecycle policies configured
- [ ] Custom machine types used where predefined sizes waste resources