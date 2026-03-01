# File Analysis Protocol

When the user provides infrastructure files, read them and analyze for cost signals. This
reference covers the analysis patterns for each supported file type.

## General Approach

1. **Read the file** using the Read tool
2. **Identify the file type** from the content and extension
3. **Apply the relevant analysis patterns** below
4. **Quantify findings** where possible — estimate monthly cost impact
5. **Incorporate findings** into the appropriate sections of the report

## Terraform / Infrastructure as Code

### Instance Types & Sizes

Look for oversized compute resources:

```hcl
# Red flag: large instance type without justification
resource "aws_instance" "api" {
  instance_type = "m5.4xlarge"  # 16 vCPU, 64 GB — is this justified?
}
```

**Check for:**
- Instance family and generation — older generations (m4, m5) cost more per unit than current (m6i, m7i)
- Instance size relative to workload — a t3.medium often suffices where m5.xlarge is provisioned
- GPU instances without AI/ML workloads — p3/p4/g5 instances are expensive
- Burstable vs. fixed performance — t3/t4g are cheaper for variable workloads
- ARM instances (Graviton) — 20-40% cheaper for compatible workloads

### Storage Configurations

```hcl
# Red flag: high IOPS provisioned without usage data
resource "aws_ebs_volume" "data" {
  type = "io2"
  iops = 10000       # Provisioned IOPS at $0.065/IOPS/month = $650/month
  size = 500         # Could gp3 at baseline 3000 IOPS suffice?
}
```

**Check for:**
- Volume type selection — io2 vs. gp3 cost difference is dramatic
- Provisioned IOPS — each IOPS costs money whether used or not
- Snapshot retention — no lifecycle policies means unlimited accumulation
- EFS/FSx usage — check throughput mode and performance settings
- S3 lifecycle rules — are they present? Do they tier to Glacier/Deep Archive?

### Auto-Scaling Settings

```hcl
# Red flag: min equals desired equals max — no scaling
resource "aws_autoscaling_group" "web" {
  min_size     = 10
  max_size     = 10
  desired_capacity = 10
}
```

**Check for:**
- Min/max/desired values — static configs negate auto-scaling benefits
- Scaling policies — are they defined? Are they target tracking or step?
- Cool-down periods — too long means slow scale-down (paying for unused capacity)
- Mixed instance policies — is spot capacity configured for fault-tolerant workloads?

### Region & AZ Choices

**Check for:**
- Multi-region deployments — data transfer between regions costs $0.01-0.02/GB
- Cross-AZ data transfer — often overlooked at $0.01/GB
- Region selection — some regions are 10-20% cheaper than others
- Workload placement relative to users — latency-driven over-provisioning

### Commitment Resources

**Check for:**
- Reserved Instances or Savings Plans defined in IaC — are they matched to actual usage?
- Capacity Reservations — are they fully utilized?
- Spot instance usage — are fault-tolerant workloads using spot?

### Tagging

```hcl
# Red flag: no tags
resource "aws_instance" "worker" {
  instance_type = "m5.xlarge"
  # No tags block — cost allocation impossible
}
```

**Check for:**
- Presence of tags on all resources (especially team, environment, service, cost-center)
- Tag consistency — are the same keys used across all resources?
- Default tags via provider block — most efficient approach for consistent tagging
- Tag enforcement — are there tag policies or SCPs preventing untagged resources?

### Module Patterns

**Check for:**
- Hardcoded values vs. variables — hardcoded instance types can't be easily right-sized
- Missing cost-relevant variables — no variable for instance type, storage size, or region
- Module reuse with different parameters — same module at different scales

## Kubernetes Manifests

### Resource Requests vs. Limits

```yaml
# Red flag: requests equal limits with no scaling
resources:
  requests:
    cpu: "4"          # Requesting 4 full cores
    memory: "8Gi"     # Requesting 8 GB
  limits:
    cpu: "4"
    memory: "8Gi"
```

**Check for:**
- Requests significantly higher than actual usage — over-provisioned containers
- Requests equal to limits — no burst capacity, forces over-provisioning
- No requests defined — scheduler can't make efficient placement decisions
- Memory limits without requests — risk of OOM kills and rescheduling

### Replica Counts

```yaml
# Red flag: static high replica count
spec:
  replicas: 20    # Is this justified by traffic? Any HPA?
```

**Check for:**
- Static replica counts with no HorizontalPodAutoscaler (HPA)
- HPA min replicas set too high — floor that can't scale down
- HPA metrics — are they based on actual demand or just CPU?
- PodDisruptionBudgets — overly restrictive budgets prevent efficient scaling

### Node Pool Configurations

**Check for:**
- Instance types in node pools — are they right-sized for the workloads they run?
- Spot/preemptible nodes — are fault-tolerant workloads using cheaper node types?
- Node pool count — too many small pools prevent efficient bin-packing
- Cluster autoscaler configuration — is it enabled? What are the min/max node counts?

### Namespace Structure

**Check for:**
- Namespaces mapped to teams or services — enables cost attribution via labels
- ResourceQuotas per namespace — prevent runaway resource consumption
- LimitRanges — ensure sensible defaults for pods without explicit resource specs

### Storage

```yaml
# Red flag: large PVC with no clear retention policy
apiVersion: v1
kind: PersistentVolumeClaim
spec:
  storageClassName: gp2     # Legacy, gp3 is cheaper and faster
  resources:
    requests:
      storage: 500Gi
```

**Check for:**
- StorageClass selection — gp2 vs. gp3, premium vs. standard
- PVC sizes relative to actual usage
- Reclaim policy — Delete vs. Retain affects orphaned volume cost
- StatefulSet storage — often over-provisioned and hard to resize

## Cloud Bills / Cost Reports

### Top Spend Categories

**Analyze:**
- Top 10 services by spend — where is the money concentrated?
- Month-over-month growth by service — which services are growing fastest?
- Cost per service relative to business metrics — is growth justified?

### Untagged or Unallocated Spend

**Check for:**
- Percentage of spend that can't be attributed to a team/service/product
- Which services have the most untagged resources
- Support and marketplace costs — often unattributable

### Data Transfer Costs

**Check for:**
- Cross-region transfer — often a hidden multiplier
- Cross-AZ transfer — frequently overlooked
- NAT Gateway data processing — can be the most expensive "network" cost
- CloudFront origin fetches — excessive cache misses drive origin costs

### Idle or Low-Utilization Patterns

**Check for:**
- Resources with zero or near-zero usage in the billing period
- Consistent low utilization across a fleet (suggests over-provisioning)
- Weekend/night patterns — resources that could be scheduled

### Commitment Utilization

**Check for:**
- Reserved Instance utilization rate — below 80% suggests poor matching
- Savings Plan utilization — unused commitment is wasted money
- Commitment vs. on-demand ratio — what percentage of eligible spend is committed?
- Upcoming expirations — opportunities to adjust strategy

## Architecture Documents

### Synchronous vs. Asynchronous Patterns

**Check for:**
- Synchronous API calls that could be async — REST endpoints doing heavy processing
- Missing message queues for decoupling — SQS, SNS, EventBridge, Kafka
- Request-reply patterns where fire-and-forget would suffice
- Cost implication: async patterns handle 10x load at ~half the compute cost

### Data Retention Policies

**Check for:**
- "Keep everything forever" defaults — compounding storage costs
- No defined retention by data classification (hot/warm/cold/archive)
- Log retention settings — CloudWatch Logs default to never expire
- Compliance-driven retention vs. convenience retention

### Caching Strategies

**Check for:**
- Missing caching layers — every uncached read hits the database or API
- Cache invalidation strategy — stale caches cause retries; no cache causes load
- CDN usage for static assets — serving from origin is more expensive
- Application-level caching — Redis/ElastiCache usage and sizing

### Observability Granularity

**Check for:**
- High-cardinality metrics — custom metrics can be expensive at scale
- Log verbosity levels — DEBUG logging in production drives storage costs
- Trace sampling rates — 100% sampling is rarely necessary
- Retention periods for observability data — do you need 90 days of DEBUG logs?

## Analysis Output

For each finding from file analysis, structure as:

| File | Finding | Estimated Impact | Recommendation | Confidence |
|---|---|---|---|---|
| main.tf:47 | m5.4xlarge at 15% utilization | $3,200/month | Right-size to m6i.xlarge | Medium — needs CloudWatch confirmation |

**Confidence levels:**
- **High:** Finding is conclusive from the file alone (e.g., unattached EBS volume, no tags)
- **Medium:** Finding is likely but needs runtime data to confirm (e.g., instance oversizing)
- **Low:** Finding is possible but speculative (e.g., architecture pattern assessment)

Always note when findings need runtime data (CloudWatch metrics, billing data) to confirm.