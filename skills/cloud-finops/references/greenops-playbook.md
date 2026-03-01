# GreenOps Remediation Playbook

Every cloud optimization that cuts costs also cuts carbon. GreenOps isn't a separate discipline
from FinOps — it's the same remediation playbook with an additional metric: carbon.

## The 8-Fix Remediation Playbook

### Fix 1: Oversized Compute Instances

**The waste:** Teams provision for peak capacity, then run at 10-20% utilization 24/7.
An m5.4xlarge running at 15% utilization costs the same as one at 85% but consumes electricity
for capacity it never uses.

**The fix:** Right-size instances based on actual utilization data.

| Action | Tool | Expected Savings |
|---|---|---|
| Review CPU/memory utilization metrics | CloudWatch, Azure Monitor, Cloud Monitoring | Identify candidates |
| Right-size to smaller instance type | AWS Compute Optimizer, Azure Advisor, GCP Recommender | 20-40% compute cost reduction |
| Switch to ARM-based instances (Graviton, Ampere) | Instance type change | Additional 20-40% cost reduction |
| Upgrade to current generation | Instance family migration | 15-40% better performance/watt |

**Quick win potential:** High — often the single largest optimization opportunity.

### Fix 2: Orphaned Instances Left Running

**The waste:** Zombie resources from forgotten tests, experiments, departed team members.
A significant portion of cloud budgets goes to unused resources.

**The fix:** Automated discovery and lifecycle management.

| Action | Implementation | Expected Savings |
|---|---|---|
| Discover instances with 0 traffic/CPU for 14+ days | Custom script or cloud-native tools | Identify zombies |
| Discover unattached EBS volumes, elastic IPs, load balancers | AWS Trusted Advisor, Azure Advisor | Quick delete |
| Tag resources with owner and expiration date | Tagging policy + automation | Prevention |
| Implement automated termination after grace period | Lambda/Azure Function triggered by tag | Ongoing savings |

**Quick win potential:** Very high — often takes hours, saves thousands/month.

### Fix 3: Aged, Inefficient Instance Types

**The waste:** Older instance generations consume more energy per compute unit. Each new
generation delivers 15-40% better performance per watt.

**The fix:** Migrate to current-generation instances.

| Old Generation | Current Generation | Improvement |
|---|---|---|
| m4.xlarge | m7i.xlarge or m7g.xlarge | ~40% better performance/$ |
| c5.2xlarge | c7g.2xlarge (Graviton) | ~40% better performance/$ |
| r5.xlarge | r7g.xlarge (Graviton) | ~35% better performance/$ |
| t3.medium | t4g.medium (Graviton) | ~20% better performance/$ |

**Quick win potential:** Medium — requires testing but delivers sustained savings.

### Fix 4: Over-Provisioned Containers

**The waste:** Over-provisioned resource requests/limits across microservices. 1,000
microservices each 20% over-provisioned = 200 extra nodes running idle.

**The fix:** Right-size container resource specs based on actual consumption.

| Action | Tool | Expected Savings |
|---|---|---|
| Audit resource requests vs. actual usage | Kubecost, Prometheus, VPA recommender | Identify over-provisioning |
| Implement Vertical Pod Autoscaler (VPA) | Kubernetes VPA | Auto-right-sizing |
| Set resource requests based on P95 usage + buffer | Manual or VPA | 20-40% node reduction |
| Review HPA settings (min replicas, target utilization) | kubectl/Helm | Scale-down efficiency |

**Quick win potential:** High in Kubernetes environments — can be dramatic at scale.

### Fix 5: Dev Environments Running 24/7

**The waste:** Dev/test environments mirror production but developers work 8 hours/day,
5 days/week = 76% idle time.

**The fix:** Automated scheduling.

| Action | Implementation | Expected Savings |
|---|---|---|
| Schedule stop outside business hours (7PM-7AM) | EventBridge + Lambda, Azure Automation | 50% cost reduction |
| Schedule stop on weekends | Same as above | Additional 20% reduction |
| On-demand spin-up with self-service | Slack bot or web interface | Near-zero idle cost |
| Use ephemeral environments (spin up per PR) | Terraform + CI/CD | Pay only for active dev time |

**Quick win potential:** Very high — minimal risk, immediate savings, 60-70% reduction.

### Fix 6: Excessive Storage Snapshots

**The waste:** Daily snapshots accumulating for years. Snapshots of deleted instances. Point-in-
time copies nobody will ever restore.

**The fix:** Lifecycle policies by environment and data classification.

| Action | Implementation | Expected Savings |
|---|---|---|
| Audit snapshot age and associated instances | AWS CLI/SDK, Azure CLI | Find orphaned snapshots |
| Define retention by environment (prod: 30d, dev: 7d) | Lifecycle policies | Prevent accumulation |
| Delete snapshots of terminated instances | Automated cleanup script | Immediate savings |
| Implement DLM (Data Lifecycle Manager) policies | AWS DLM, Azure Backup policies | Ongoing governance |

**Typical reduction:** 40-60% of snapshot storage costs.

### Fix 7: Data on the Wrong Tier

**The waste:** Hot storage costs 10-20x more than archive. Log files from 2021 on premium SSD.
Compliance archives at real-time retrieval prices.

**The fix:** Intelligent tiering and lifecycle policies.

| Storage Tier | Use Case | Relative Cost |
|---|---|---|
| Hot (SSD/gp3) | Active data, <30 days old | 1x (baseline) |
| Warm (S3-IA, Cool Blob) | Infrequent access, 30-90 days | 0.3-0.5x |
| Cold (Glacier Flexible, Cool) | Rare access, 90 days-1 year | 0.1-0.2x |
| Archive (Glacier Deep, Archive) | Compliance, >1 year | 0.02-0.05x |

| Action | Implementation | Expected Savings |
|---|---|---|
| Audit storage by access pattern | S3 Storage Lens, Azure Storage Analytics | Identify cold data on hot tiers |
| Enable intelligent tiering (S3, Blob) | Storage class configuration | Automatic optimization |
| Set lifecycle policies for logs, backups, artifacts | S3 lifecycle rules, Blob lifecycle management | Move data automatically |
| Archive compliance data explicitly | Glacier Deep Archive, Azure Archive | Dramatic cost reduction |

### Fix 8: Services in the Wrong Region

**The waste:** Region affects both latency and carbon intensity. Workloads in coal-powered
regions emit more than renewable-powered regions at identical compute cost. Services far from
users incur data transfer costs and latency penalties leading to over-provisioning.

**The fix:** Audit workload placement for cost, latency, and carbon.

| Action | Consideration | Tool |
|---|---|---|
| Place latency-sensitive apps near users | Performance requirement | Latency testing |
| Place batch jobs in clean-energy regions | Environmental impact | Cloud carbon dashboards |
| Minimize cross-region data transfer | Cost optimization | VPC flow logs, billing data |
| Consider single-region for non-global workloads | Simplicity + cost | Architecture review |

## Beyond Remediation: Carbon-Aware Computing

For organizations with sustainability commitments, go beyond waste elimination:

### Time-Shifting

Schedule non-urgent workloads for periods when the grid runs on renewable energy:
- Batch processing during solar peak hours
- Training jobs during wind-heavy overnight periods
- Report generation during low-carbon grid periods

**Implementation tools for time-shifting and region-shifting:**

| Tool | What It Does | Integration |
|---|---|---|
| Carbon Aware SDK (Green Software Foundation) | Returns optimal time/region for lowest carbon | REST API + CLI; integrates with schedulers |
| Electricity Maps API | Real-time grid carbon intensity, 190+ countries | REST API; powers GCP carbon reporting |
| WattTime API | Marginal emissions data by grid region | REST API; used by Azure carbon tooling |
| KEDA Carbon Aware Scaler | Scales Kubernetes workloads based on carbon intensity | Kubernetes-native, uses Carbon Aware SDK |

### Region-Shifting

Place workloads in regions with cleaner energy grids. Carbon intensity varies **200x** between
the cleanest and dirtiest regions — this is not a rounding error.

**Cleanest regions by provider** (lowest grid carbon intensity):

| Provider | Region | Location | Grid Carbon Intensity | Notes |
|---|---|---|---|---|
| GCP | europe-north2 | Stockholm | 3 gCO2eq/kWh, 100% CFE | Hydro/wind grid |
| GCP | northamerica-northeast1 | Montréal | 5 gCO2eq/kWh, 99% CFE | Hydro-dominated grid |
| GCP | europe-west6 | Zürich | 15 gCO2eq/kWh, 98% CFE | Nuclear + hydro |
| GCP | europe-west9 | Paris | 16 gCO2eq/kWh, 96% CFE | Nuclear-dominated grid |
| GCP | europe-north1 | Finland | 39 gCO2eq/kWh, 98% CFE | Wind + nuclear |
| GCP | us-west1 | Oregon | 79 gCO2eq/kWh, 87% CFE | Hydro + wind |
| AWS | eu-north-1 | Stockholm | Low — >95% renewable grid | Hydro/wind grid |
| AWS | us-west-2 | Oregon | Low — high renewable mix | Hydro-dominated grid |
| Azure | Sweden Central | Gävle | ~15 gCO2eq/kWh | 100% hourly renewable matching |

**High-carbon regions to avoid for flexible workloads:**

| Provider | Region | Location | Grid Carbon Intensity |
|---|---|---|---|
| GCP | asia-south1 | Mumbai | 679 gCO2eq/kWh |
| GCP | africa-south1 | Johannesburg | 657 gCO2eq/kWh |
| GCP | europe-central2 | Warsaw | 643 gCO2eq/kWh |
| GCP | us-east1 | South Carolina | 576 gCO2eq/kWh |

GCP publishes per-region carbon-free energy (CFE) percentages and grid carbon intensity at
[cloud.google.com/sustainability/region-carbon](https://cloud.google.com/sustainability/region-carbon).
AWS and Azure publish aggregate renewable energy data but not per-region grid intensity — use
Electricity Maps or WattTime for comparable cross-provider data.

### Demand-Shaping

Reduce compute intensity during grid stress periods:
- Lower batch processing priority during peak grid demand
- Defer non-critical ML training during heat waves (grid stress)
- Shape auto-scaling to prefer efficiency during high-carbon periods

## Carbon Measurement Tools

| Provider | Tool | Coverage |
|---|---|---|
| AWS | Customer Carbon Footprint Tool | Account-level, monthly, regional breakdown |
| Azure | Emissions Impact Dashboard | Scope 1, 2, 3 emissions |
| GCP | Carbon Footprint Dashboard | Project-level, near real-time, per-region CFE% |
| Third-party | Cloud Carbon Footprint (open source) | Multi-cloud estimation |
| Third-party | Electricity Maps | Real-time grid intensity, 190+ countries |
| Third-party | Carbon Aware SDK | Optimal time/region selection for lowest carbon |
| Standard | SCI (ISO/IEC 21031:2024) | Software Carbon Intensity — standard formula for application-level carbon rate |

**The SCI formula:** `SCI = (E × I) + M per R` — where E = energy consumed, I = grid carbon
intensity, M = embodied carbon of hardware, R = functional unit (per request, per user, per
minute). Use SCI to compare the carbon efficiency of architectural alternatives, not just
absolute emissions.

## GreenOps Assessment Questions

1. Is carbon tracked alongside cost? (Most organizations: no)
2. What's the estimated waste percentage?
3. Which of the 8 fixes have the highest potential in this environment?
4. Are dev environments scheduled? (Quickest GreenOps win)
5. Are storage lifecycle policies in place?
6. What instance generations are in use? (Older = less efficient)
7. Is sustainability a board-level or compliance requirement?
8. Are batch workloads eligible for time-shifting or region-shifting?
9. Are workloads in high-carbon regions that could run in cleaner ones?
10. Is real-time carbon intensity data (Electricity Maps, WattTime) integrated into scheduling?