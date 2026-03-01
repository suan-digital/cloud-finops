# AWS Cost Optimization Reference

Comprehensive AWS-specific FinOps patterns covering billing data, commitment instruments,
service-level optimization, and architectural cost patterns.

## AWS Billing Data

### Cost and Usage Report (CUR)

The CUR is the foundational data source for AWS cost management.

**CUR 2.0 (FOCUS-compatible):**
- Standardized column names aligned with FOCUS specification
- Simplified schema vs. legacy CUR
- Enables multi-cloud cost normalization
- Export to S3, query via Athena or Redshift

**Key CUR columns for analysis:**
| Column | Purpose |
|---|---|
| `line_item_usage_amount` | Quantity of usage |
| `line_item_unblended_cost` | Actual cost charged |
| `line_item_usage_type` | Service-specific usage type |
| `reservation_reservation_a_r_n` | RI attribution |
| `savings_plan_savings_plan_a_r_n` | SP attribution |
| `resource_tags_*` | Custom tag columns |
| `pricing_public_on_demand_cost` | What you'd pay without commitments |

**Best practice:** Export CUR to S3, create Athena table, build queries for:
- Top spend by service, account, region
- Untagged resource spend
- Commitment utilization and coverage
- Data transfer cost breakdown
- Month-over-month trends

### AWS Cost Explorer

Good for quick analysis. Limited for deep investigation.

**Useful views:**
- Daily/monthly cost by service
- Cost by linked account
- Cost by tag
- RI/SP utilization and coverage
- Forecasting (machine learning-based)

**Limitations:**
- 14-month history only
- Limited custom groupings
- Can't drill into resource-level cost without CUR

### AWS Budgets

Set cost and usage thresholds with automated alerts.

**Budget types:**
- Cost budget — alert on total spend
- Usage budget — alert on specific service usage
- RI utilization — alert if RI utilization drops
- SP utilization — alert if SP utilization drops

**Best practice:** Set budgets at account level AND service level. Alert at 80%, 100%, and
forecasted to exceed.

## Commitment Instruments

### Savings Plans

**Types:**

| Type | Discount | Flexibility | Best For |
|---|---|---|---|
| **Compute SP** | 40-60% vs. on-demand | Any instance family, size, OS, region, tenancy | Unknown future instance mix |
| **EC2 Instance SP** | 50-72% vs. on-demand | Specific instance family + region | Known, stable workloads |
| **SageMaker SP** | Up to 64% | SageMaker ML instances | Steady ML workloads |

**Strategy by maturity:**

| Maturity | Approach |
|---|---|
| **Shu** | Start with Compute SP for 60-70% of stable baseline |
| **Ha** | Layer: EC2 Instance SP for known workloads + Compute SP for flexible coverage |
| **Ri** | Dynamic portfolio: Instance SP (deep discount) + Compute SP (flex) + on-demand (peaks) |

### Reserved Instances

Legacy but still useful for specific services (RDS, ElastiCache, OpenSearch, Redshift).

| Service | RI Type | Discount |
|---|---|---|
| RDS | Standard/Convertible | 30-60% |
| ElastiCache | Standard | 30-55% |
| OpenSearch | Standard | 30-50% |
| Redshift | Standard | 30-75% |

**Key rule:** Use Savings Plans for EC2/Fargate/Lambda. Use RIs for services not covered by SPs.

### Commitment Decision Framework

#### Which Instrument?

| Workload Pattern | Recommended | Why |
|---|---|---|
| Steady-state compute (>70% baseline) | Compute Savings Plans | Flexible across instance types, regions, OS |
| Specific instance family, predictable | EC2 Instance Savings Plans | Deepest discount for known workloads |
| Variable but grows quarter over quarter | 1-year Compute SP at 60% of current | Cover baseline only, let growth absorb headroom |
| Unpredictable / bursty | No commitment — use on-demand + spot | Don't commit to what you can't predict |
| RDS, ElastiCache, Redshift (stable) | Service-specific RIs | Not covered by Savings Plans |

#### Coverage Strategy

1. **Calculate stable baseline** — P10 of last 90 days' hourly spend (the floor, not the average)
2. **Commit to 70-80% of baseline** — leave headroom for optimization and workload changes
3. **Review monthly** — adjust as baseline shifts from new services, migrations, or optimizations
4. **Never commit to 100%** — waste from over-commitment is more expensive than the on-demand
   premium you're trying to avoid
5. **Stagger expirations** — don't let all commitments expire in the same month. Spread across
   quarters for flexibility

#### Common Mistakes

- Buying commitments before understanding usage patterns (Shu anti-pattern)
- Committing to 100% of current spend, then optimizing — commitments become waste
- Ignoring convertible options when architecture is evolving
- Treating RI/SP purchases as "set and forget" — utilization degrades without monitoring

### Commitment Utilization Targets

| Metric | Poor | Acceptable | Good | Excellent |
|---|---|---|---|---|
| SP utilization | <60% | 60-75% | 75-85% | >85% |
| RI utilization | <70% | 70-80% | 80-90% | >90% |
| Commitment coverage | <30% | 30-50% | 50-70% | >70% |

## Service-Level Optimization Patterns

### EC2

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Right-size instances | 20-40% | M | Use Compute Optimizer, CloudWatch metrics |
| Graviton migration | 20-40% | M | ARM-compatible workloads, significant savings |
| Spot for fault-tolerant | 60-90% | M | Batch processing, CI/CD, stateless workers |
| Current generation migration | 15-30% | M | m5→m7i, c5→c7g, etc. |
| Scheduled scaling | 30-50% | S | Non-production, predictable traffic patterns |
| Auto-scaling optimization | 10-30% | M | Target tracking, mixed instances, warm pools |

**Graviton savings detail:** Graviton3 (m7g, c7g, r7g) delivers ~40% better price-performance
than comparable x86 instances. Compatible with most Linux workloads. Check application
compatibility first.

### EBS

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| gp2→gp3 migration | 20% | S | gp3 is cheaper AND faster baseline. No reason to stay on gp2. |
| Delete unattached volumes | 100% of waste | S | `aws ec2 describe-volumes --filters "Name=status,Values=available"` |
| Right-size volumes | 10-30% | S | Reduce oversized volumes (CloudWatch VolumeReadBytes/WriteBytes) |
| io2→gp3 where possible | 50-80% | M | gp3 baseline 3000 IOPS covers many io2 use cases |
| Snapshot lifecycle | 40-60% | S | AWS DLM policies, delete orphaned snapshots |

### S3

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Intelligent Tiering | 20-40% | S | Zero retrieval fees, auto-tiers by access pattern |
| Lifecycle policies | 30-70% | S | Move to IA/Glacier based on age |
| Delete incomplete multipart uploads | Variable | S | Can accumulate significant hidden cost |
| Requester Pays for shared data | Variable | S | Shift cost to consumers for shared datasets |
| S3 Express One Zone | Variable | M | Low-latency access for frequently accessed data |

### RDS / Aurora

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Right-size instances | 20-40% | M | CloudWatch CPUUtilization, FreeableMemory |
| Aurora Serverless v2 | 30-60% | L | Variable workloads, scales to zero-ish |
| Read replicas for reads | 20-40% | M | Offload read traffic from primary |
| Reserved Instances | 30-60% | S | Stable production databases |
| Stop non-production | 50-70% | S | `aws rds stop-db-instance` (7-day max) |
| Multi-AZ only for prod | 50% of standby cost | S | Dev/staging doesn't need Multi-AZ |

### Lambda

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Memory right-sizing | 10-30% | S | Use AWS Lambda Power Tuning |
| ARM (Graviton) | 20% | S | Simply change architecture setting |
| Provisioned Concurrency review | Variable | S | Only for cold-start-sensitive functions |
| Optimize execution time | 10-50% | M | Reduce duration = reduce cost |
| Batch processing | 30-60% | M | Process in batches instead of per-record |

### EKS / Kubernetes

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Karpenter for node management | 20-40% | M | Better bin-packing than Cluster Autoscaler |
| Spot nodes for non-critical | 60-90% | M | Use Karpenter spot integration |
| Fargate for burst workloads | Variable | M | No node management overhead |
| Right-size pods | 20-40% | M | VPA or manual based on Prometheus data |
| Namespace cost allocation | N/A | M | Kubecost or built-in cost allocation tags |

### Data Transfer

**The hidden multiplier.** Data transfer often surprises organizations.

| Transfer Type | Cost | Optimization |
|---|---|---|
| Cross-region | $0.01-$0.02/GB | Minimize unnecessary replication |
| Cross-AZ | $0.01/GB each way | Co-locate services in same AZ where possible |
| NAT Gateway processing | $0.045/GB | VPC endpoints for AWS services eliminate NAT cost |
| Internet egress | $0.09/GB (first 10TB) | CloudFront often cheaper than direct egress |
| S3 to EC2 (same region) | Free | Always co-locate |
| CloudFront to origin | $0.00/GB (reduced) | CDN reduces origin load + data transfer |

**VPC Endpoints** save significantly on NAT Gateway costs for AWS service traffic (S3, DynamoDB,
CloudWatch, etc.). Often the highest-impact data transfer optimization.

#### Common Data Transfer Traps

Data transfer is the most commonly overlooked AWS cost driver at scale. It rarely shows up in
architecture reviews but compounds silently.

- **Cross-AZ microservice traffic:** $0.01/GB each way. A service making 1M requests/day with
  5KB payloads across AZs costs ~$300/month for that single service pair. Multiply across a
  microservice mesh and this becomes material.
- **NAT Gateway data processing:** $0.045/GB on top of hourly charges. For S3 and DynamoDB
  traffic, Gateway VPC endpoints eliminate this entirely at no hourly cost.
- **CloudFront to ALB origin:** Charged at standard data transfer rates. CloudFront to S3 origin
  is free — architecture matters for distribution patterns.
- **Cross-region replication:** Necessary for DR, expensive if unmanaged. Audit what's being
  replicated — often includes dev/staging data that doesn't need DR.
- **ECR image pulls across regions:** Each pull across regions pays data transfer. Use regional
  ECR replicas for multi-region deployments.

#### Data Transfer Audit Checklist

- [ ] NAT Gateway data processing reviewed — VPC endpoints for top AWS service traffic?
- [ ] Cross-AZ traffic measured — can co-locate high-traffic service pairs?
- [ ] S3 transfer acceleration enabled only where latency justifies the 2x premium?
- [ ] CloudFront configured to minimize origin fetches (caching headers, origin shield)?
- [ ] Cross-region replication scoped to production data only?

### CloudWatch

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Log retention policies | 30-70% | S | Default is "never expire" — set 30/60/90 day retention |
| Reduce log verbosity | 50-80% | M | INFO not DEBUG in production |
| Metric filter vs. custom metrics | 80% | M | Filter from logs instead of PutMetricData |
| Contributor Insights evaluation | Variable | S | Disable if not actively used |
| Composite alarms | Variable | S | Reduce alarm count with composites |

## Cost Patterns by Architecture

### Serverless Architecture
- **Cost model:** Pay per invocation + duration + memory
- **Watch for:** Over-provisioned memory, cold start mitigation costs, Step Functions state transitions
- **Optimize:** Memory tuning, batch processing, direct service integrations (skip Lambda)

### Container Architecture (EKS/ECS)
- **Cost model:** Node instances + overhead (EKS control plane, load balancers)
- **Watch for:** Over-provisioned pods, too many small node pools, underused nodes
- **Optimize:** Karpenter/Spot, right-size pods, consolidate node pools

### VM-Based Architecture
- **Cost model:** Instance hours + storage + data transfer
- **Watch for:** Low utilization, old generations, no auto-scaling
- **Optimize:** Right-size, Graviton, Savings Plans, scheduling

### Data Architecture
- **Cost model:** Storage + queries + data transfer + compute
- **Watch for:** Unoptimized queries (Athena, Redshift), data duplication, archive neglect
- **Optimize:** Partitioning, columnar formats, lifecycle policies, query optimization

## AWS-Specific Tools

| Tool | Purpose | Cost |
|---|---|---|
| **Cost Explorer** | Visual cost analysis | Free (basic), $0.01/API request |
| **CUR** | Detailed billing data | Free (S3 storage costs apply) |
| **Compute Optimizer** | Right-sizing recommendations | Free |
| **Trusted Advisor** | Best practice checks | Business/Enterprise Support plan |
| **AWS Budgets** | Budget alerts | First 2 free, $0.01/day after |
| **S3 Storage Lens** | Storage analytics | Free (basic), paid (advanced) |
| **AWS MCP Server** | AI-powered cost management | Free (standard API costs) |

## Assessment Checklist

- [ ] CUR enabled and queryable (Athena or equivalent)
- [ ] Cost Explorer accessed regularly (not just at month-end)
- [ ] Budget alerts set at account and service level
- [ ] Compute Optimizer recommendations reviewed
- [ ] Savings Plans or RIs in place for stable workloads
- [ ] SP/RI utilization above 80%
- [ ] Graviton instances used where compatible
- [ ] Data transfer paths analyzed for VPC endpoint opportunities
- [ ] S3 lifecycle policies in place
- [ ] CloudWatch log retention set (not "never expire")
- [ ] EBS: no unattached volumes, no gp2 remaining