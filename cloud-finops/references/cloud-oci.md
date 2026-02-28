# OCI (Oracle Cloud Infrastructure) Cost Optimization Reference

OCI-specific FinOps patterns covering billing, optimization, and Oracle workload cost management.

## OCI Billing

### Cost Analysis

OCI's built-in cost analysis tool:
- Filter by compartment, service, tag, region
- Daily and monthly granularity
- Forecast based on historical trends
- Export to Object Storage for custom analytics

### Budgets

- Set at compartment level
- Alert thresholds (50%, 80%, 100%)
- Email notifications and event-based triggers

### Usage Reports

Detailed CSV exports for custom analytics:
- Hourly granularity
- Resource-level detail
- Available via Object Storage automatic export

## OCI Pricing Model

### Key Differentiators

OCI has pricing advantages in specific areas:

| Feature | OCI Advantage |
|---|---|
| **Outbound data transfer** | 10 TB/month free (vs. ~1 GB free on other clouds) |
| **Block storage** | Lower per-GB pricing than competitors |
| **OCPU pricing** | 1 OCPU = 2 vCPUs (compare carefully) |
| **Oracle database licensing** | Bring-your-own-license + OCI discount |
| **Autonomous Database** | Pay per ECPU, scale to zero |

### Commitment Instruments

| Type | Term | Discount | Details |
|---|---|---|---|
| **Annual Universal Credits** | 1-4 years | 8-33% (scales with term and amount) | Prepaid credits consumed against usage |
| **Monthly Universal Credits** | Monthly | 0-8% | Minimum monthly spend, no long-term lock-in |
| **Pay-As-You-Go** | None | None | Flexible, no commitment |
| **Support Rewards** | Ongoing | Credits earned | Reinvest support spending as service credits |

#### Annual Universal Credits Detail

Credits are consumed against OCI usage at discounted rates. Key mechanics:
- Credits are prepaid — unused credits do not roll over past contract end
- Overage beyond commitment is billed at list price (no discount)
- Discount increases with commitment size and term length
- Credits apply to most OCI services including compute, storage, database, and networking

**Representative discount ranges:**

| Annual Commitment | 1-Year Term | 3-Year Term | 4-Year Term |
|---|---|---|---|
| $10K-$50K | 8-12% | 15-20% | 20-25% |
| $50K-$500K | 12-18% | 20-28% | 25-30% |
| $500K+ | 18-25% | 25-30% | 28-33% |

*Exact discounts are negotiated. Larger commitments and longer terms yield higher discounts.*

#### Commitment Strategy

| Workload Pattern | Recommended Instrument | Rationale |
|---|---|---|
| Steady-state production | Annual Universal Credits (3-4 year) | Maximum discount for predictable spend |
| Growing but predictable | Annual Universal Credits (1 year) | Lock in discount, re-evaluate at renewal |
| Variable/seasonal | Monthly Universal Credits | Flexibility with modest discount |
| Experimental/dev | Pay-As-You-Go | No commitment risk for uncertain workloads |
| Oracle DB-heavy with licenses | Annual Universal Credits + BYOL | Stack BYOL savings on top of credit discount |

**Coverage strategy:**
1. Calculate baseline monthly spend from 3-6 months of usage data
2. Commit to 70-80% of baseline — leave headroom for workload changes
3. Factor BYOL savings separately (they reduce the usage credits consume)
4. Negotiate term length based on confidence in workload stability
5. Review credit burn rate quarterly — adjust at renewal

**Common mistakes:**
- Committing to 100% of current spend (no room for optimization or workload reduction)
- Ignoring BYOL impact on credit consumption (overcommitting)
- Choosing 4-year term without workload stability confidence
- Not tracking credit burn rate (discovering overcommitment at contract end)
- Treating overage at list price as acceptable (it erodes the commitment discount)

#### Utilization Targets

| Metric | Poor | Acceptable | Good | Excellent |
|---|---|---|---|---|
| Credit utilization | <60% | 60-75% | 75-90% | 90-98% |
| Overage rate | >20% | 10-20% | 5-10% | <5% |
| BYOL coverage | Not tracked | Partial inventory | 80%+ applied | Full optimization |

## Service-Level Optimization

### Compute

| Pattern | Savings | Details |
|---|---|---|
| Right-size instances | 20-40% | OCI Compute Optimizer recommendations |
| Preemptible instances | 50% | For fault-tolerant batch workloads |
| Burstable instances (E4/E5 Flex) | 30-50% | Variable workloads |
| Ampere A1 (ARM) | 20-40% | Price-performance advantage |
| Autoscaling | 20-40% | Metric-based instance pool scaling |
| Dedicated VM hosts | Variable | For licensing compliance |

**A1 Flex (ARM):** OCI's Ampere A1 instances are extremely cost-effective. Free tier includes
4 OCPUs + 24 GB memory. Production pricing is highly competitive.

### OCI Kubernetes (OKE)

| Pattern | Savings | Details |
|---|---|---|
| Virtual node pools | Variable | Serverless pods, pay per pod |
| Managed node pools with autoscaling | 20-40% | Right-size cluster |
| Preemptible nodes | 50% | For non-critical workloads |
| ARM node pools (A1) | 20-40% | Cost-effective for compatible workloads |

### Oracle Database on OCI

| Pattern | Savings | Details |
|---|---|---|
| Autonomous Database | 30-60% | Automated optimization, scale to zero |
| BYOL vs. License Included | 30-50% | If existing Oracle licenses available |
| Exadata Cloud Service | Variable | For large Oracle workloads |
| Database Cloud Service | 20-40% | Right-size OCPU and storage |
| Standard Edition for smaller workloads | 50-70% | Don't use Enterprise when Standard suffices |

### Storage

| Pattern | Savings | Details |
|---|---|---|
| Object Storage tiers (Standard/Infrequent/Archive) | 50-90% | Lifecycle policies |
| Block Volume performance tiers | 20-50% | Lower performance for cold data |
| File Storage right-sizing | Variable | Reduce provisioned capacity |
| Boot volume backup policies | 30-50% | Automated lifecycle management |

### Networking

OCI's data transfer pricing is a major advantage:

| Transfer Type | Cost |
|---|---|
| First 10 TB/month egress | Free |
| Beyond 10 TB | $0.0085/GB |
| Cross-region | Low (varies by region pair) |
| FastConnect | Fixed monthly + reduced data transfer |

For data-intensive workloads, OCI's egress pricing can make it significantly cheaper than
AWS/Azure/GCP.

## OCI-Specific Patterns

### Compartment Organization

```
Root Compartment
├── Production
│   ├── App-Services
│   └── Data-Services
├── Non-Production
│   ├── Development
│   └── Staging
└── Shared-Services
    ├── Networking
    └── Security
```

Use compartments for cost isolation and governance. Apply budgets per compartment.

### Tagging

OCI supports two types:
- **Defined tags:** Namespace.Key = Value (enforced, structured)
- **Free-form tags:** Key = Value (flexible, less governed)

**Best practice:** Use defined tags with tag namespaces for cost allocation. Enforce via
tag defaults and IAM policies.

### Cost Tracking Tags

| Tag Namespace | Tag Key | Purpose |
|---|---|---|
| `FinOps` | `CostCenter` | Financial attribution |
| `FinOps` | `Environment` | Lifecycle stage |
| `FinOps` | `Team` | Team ownership |
| `FinOps` | `Service` | Application/service name |

## OCI Tools

| Tool | Purpose |
|---|---|
| **Cost Analysis** | Built-in cost reporting and analysis |
| **Budgets** | Threshold alerts per compartment |
| **Usage Reports** | Detailed CSV exports |
| **Cloud Advisor** | Optimization recommendations |
| **Compute Optimizer** | Right-sizing for compute |

## Assessment Checklist

- [ ] Cost Analysis reviewed regularly
- [ ] Budgets set per compartment
- [ ] Annual Universal Credits sized to 70-80% of baseline spend
- [ ] Credit burn rate tracked quarterly
- [ ] Data transfer advantage leveraged (10 TB free egress)
- [ ] Autonomous Database used where applicable
- [ ] ARM (A1) instances used for compatible workloads
- [ ] Defined tags in place for cost allocation
- [ ] Storage lifecycle policies configured
- [ ] BYOL applied where Oracle licenses exist