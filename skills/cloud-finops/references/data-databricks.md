# Databricks Cost Optimization Reference

Databricks-specific pricing, DBU optimization, and cost management patterns.

## Databricks Pricing Model

### DBU (Databricks Unit) Pricing

Databricks charges in DBUs — a unit of processing capability:

| Workload Type | Approximate DBU/hr | Notes |
|---|---|---|
| Jobs Compute (Standard) | 0.07-2.0+ per VM | Depends on VM size |
| All-Purpose Compute (Standard) | 0.10-3.0+ per VM | Interactive workloads, more expensive |
| SQL Compute (Serverless) | Per-query DBU | Pay per query |
| Delta Live Tables | Pipeline DBU pricing | Additional surcharge |
| Model Serving | Per-DBU or per-token | AI inference |
| Serverless Compute | Per-DBU consumed | No cluster management |

**Key insight:** DBU pricing varies by:
- Workload type (Jobs < All-Purpose)
- Cloud provider (AWS, Azure, GCP have different DBU rates)
- Tier (Standard, Premium, Enterprise)
- Region

### Infrastructure Costs

Databricks charges DBUs, but the underlying cloud infrastructure (VMs, storage, networking)
is billed by the cloud provider separately.

**Total Databricks cost = DBU charges + cloud infrastructure + storage**

Many organizations focus on DBU costs and miss that cloud VM costs are often larger.

## Cost Optimization Patterns

### Compute Optimization

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Jobs Compute vs. All-Purpose | 30-50% | M | All-Purpose is for interactive dev; use Jobs for production |
| Auto-termination | 20-40% | S | Set auto-terminate after 10-30 min idle |
| Cluster right-sizing | 20-40% | M | Match worker count and type to workload |
| Spot/preemptible workers | 60-90% | M | Use for fault-tolerant jobs |
| Autoscaling | 20-40% | S | Set appropriate min/max workers |
| Serverless Compute | Variable | M | No cluster management, pay per use |

### Photon Optimization

Photon is Databricks' vectorized query engine:
- 2-8x faster for compatible queries
- Higher DBU rate per hour
- **Net cheaper** when it reduces job duration significantly

**When Photon helps:**
- SQL-heavy workloads (transformations, aggregations)
- Large scan operations
- Delta Lake read-heavy workloads

**When Photon hurts:**
- Python/Scala UDFs (Photon can't accelerate)
- Streaming workloads (limited benefit)
- Small data volumes (overhead exceeds benefit)

**Assessment:** Compare total cost (DBU rate × runtime) with and without Photon.

### SQL Warehouse Optimization

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Serverless SQL | Variable | S | No idle cluster cost, pay per query |
| Auto-stop after idle | 30-50% | S | Stop warehouse when no queries |
| Right-size warehouse (T-shirt) | 20-40% | S | Small → Medium → Large based on query patterns |
| Query optimization | 20-50% | M | Reduce data scanned per query |
| Warehouse scheduling | 40-60% | S | Stop outside business hours for BI |

### Storage Optimization

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| OPTIMIZE command (compaction) | 10-30% | S | Reduce small files, improve read performance |
| VACUUM command | 10-20% | S | Delete old file versions |
| Z-ORDER clustering | 10-30% | M | Co-locate related data for faster queries |
| Liquid Clustering | 10-30% | M | Auto-optimizing clustering (newer alternative) |
| Delta sharing | Variable | M | Share without copying data |
| Unity Catalog lineage | N/A | M | Track data usage for retention decisions |

### Notebook & Development Costs

| Pattern | Savings | Details |
|---|---|---|
| Single-node clusters for development | 50-70% | Don't use multi-node for notebook exploration |
| Auto-termination on dev clusters | 40-60% | 10-minute timeout for interactive clusters |
| Shared clusters for light users | 30-50% | Multiple users on one cluster via Shared mode |
| Serverless for SQL development | Variable | No cluster management overhead |

## Unity Catalog Cost Implications

Unity Catalog adds governance capabilities with cost implications:

| Feature | Cost Impact |
|---|---|
| Lineage tracking | Minimal additional compute |
| Access control | No additional cost |
| Audit logging | Storage for logs |
| Delta Sharing | Reduced data duplication (savings) |
| Lakehouse Monitoring | Additional compute for quality checks |

**Net effect:** Unity Catalog often reduces cost by eliminating data duplication and
enabling better governance.

## Databricks + Cloud Provider Optimization

### AWS-Specific

- Use Graviton instances for workers (20-30% cheaper)
- Spot instances for workers with Databricks spot fallback
- S3 lifecycle policies for Delta tables
- VPC Endpoints to reduce data transfer

### Azure-Specific

- Use Azure Spot VMs for workers
- Premium Storage only for hot data
- Azure Hybrid Benefit for SQL Server workloads
- ADLS lifecycle management for Delta tables

### GCP-Specific

- Preemptible VMs for workers
- Standard storage for cold Delta tables
- CUDs for stable compute baseline

## Cost Attribution

### Cluster Tags

Tag every cluster with:
- `team` — Cost ownership
- `project` — Project attribution
- `environment` — dev/staging/prod
- `workload-type` — ETL/ML/BI/ad-hoc

### Job-Level Attribution

Track costs per job:
- Use Databricks billing APIs for job-level cost data
- Map jobs to features/products
- Track cost per successful job run (not just compute time)

### Key Metrics

| Metric | Formula | Target |
|---|---|---|
| Cost per job run | DBU cost + infra cost / runs | Trending down |
| DBU efficiency | Business value / DBU consumed | Improving |
| Cluster utilization | Active compute / provisioned compute | >60% |
| Spot adoption | Spot hours / total hours | >50% for eligible workloads |
| All-Purpose waste | All-Purpose DBU / total DBU | <20% (should be Jobs) |

## Assessment Questions

1. What's the ratio of All-Purpose to Jobs Compute? (All-Purpose should be minimal in prod)
2. Are clusters auto-terminating after idle periods?
3. Is Photon enabled? Is it net cost-positive for the workload?
4. What's the spot/preemptible adoption rate for workers?
5. Are SQL Warehouses stopped outside business hours?
6. Is OPTIMIZE and VACUUM running regularly on Delta tables?
7. What's the total cost (DBU + cloud infrastructure + storage)?
8. Are costs attributed by team and project via cluster tags?