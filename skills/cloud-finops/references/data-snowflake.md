# Snowflake Cost Optimization Reference

Snowflake-specific pricing, warehouse sizing, credit optimization, and cost management patterns.

## Snowflake Pricing Model

### Credit-Based Pricing

Snowflake charges in credits, consumed by virtual warehouses (compute):

| Warehouse Size | Credits/Hour | Approximate $/Hour |
|---|---|---|
| X-Small | 1 | ~$2-4 |
| Small | 2 | ~$4-8 |
| Medium | 4 | ~$8-16 |
| Large | 8 | ~$16-32 |
| X-Large | 16 | ~$32-64 |
| 2X-Large | 32 | ~$64-128 |

*Credit pricing varies by edition (Standard, Enterprise, Business Critical) and cloud/region.*

### Edition Pricing

| Edition | Credit Rate | Key Features |
|---|---|---|
| **Standard** | Lowest | Basic features |
| **Enterprise** | ~1.5x Standard | Multi-cluster warehouses, time travel (90 days) |
| **Business Critical** | ~2x Standard | Enhanced security, failover |
| **VPS** | Highest | Dedicated infrastructure |

### Total Cost Components

**Total Snowflake cost = Compute (credits) + Storage + Data transfer + Serverless features**

| Component | % of Typical Bill | Optimization Lever |
|---|---|---|
| Compute (warehouses) | 50-70% | Warehouse sizing, scheduling, query optimization |
| Storage | 15-25% | Data retention, compression, cloning |
| Cloud services | 5-15% | Usually free (included in 10% compute threshold) |
| Serverless features | 5-15% | Snowpipe, tasks, materialized views |
| Data transfer | 2-10% | Minimize cross-region, cross-cloud |

## Warehouse Optimization

### Sizing

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Right-size warehouses | 20-50% | M | Match size to query complexity, not data volume |
| Auto-suspend (1-5 min) | 30-60% | S | Default is 10 min — reduce for intermittent workloads |
| Auto-resume | N/A | S | Enable for all warehouses |
| Separate warehouses by workload | 10-30% | M | ETL vs. BI vs. ad-hoc — different sizing needs |
| Multi-cluster scaling (Enterprise) | 10-30% | M | Scale out for concurrent users, not up for complexity |

### Sizing Strategy

```
Query type determines warehouse size:
├── Simple lookups, dashboards → X-Small or Small
├── Moderate aggregations, BI → Small or Medium
├── Complex joins, large scans → Medium or Large
├── Heavy ETL, data transformations → Large or X-Large
└── Very large data processing → X-Large or larger
```

**Common mistake:** Using Large warehouses for simple dashboard queries. A dashboard query
that runs in 3 seconds on a Large warehouse might run in 5 seconds on a Small — same result,
75% cost reduction.

### Auto-Suspend Configuration

| Workload | Recommended Auto-Suspend |
|---|---|
| Interactive/BI | 1-2 minutes |
| ETL/Batch | 0 (immediate) or 1 minute |
| Ad-hoc analysis | 5 minutes |
| Always-on dashboards | 1 minute (with auto-resume) |

**Key insight:** Every minute a warehouse runs idle burns credits. The default 10-minute
auto-suspend wastes ~40% of credits for intermittent workloads.

### Multi-Cluster Warehouses

Enterprise edition feature. Scale out (more clusters) vs. scale up (bigger warehouse):

| Scenario | Scale Up (Bigger) | Scale Out (Multi-Cluster) |
|---|---|---|
| Complex queries | Yes — more resources per query | No benefit |
| Many concurrent users | No benefit per query | Yes — parallel execution |
| Mixed workloads | Possibly — depends on mix | Yes — isolate workloads |

**Rule:** Scale up for query complexity. Scale out for concurrency.

## Query Cost Optimization

### Expensive Query Patterns

| Anti-Pattern | Cost Impact | Fix |
|---|---|---|
| `SELECT *` | Scans all columns | Select specific columns |
| Missing clustering keys | Full table scans | Add cluster keys on filter columns |
| No partition pruning | Scans all micro-partitions | Filter on clustering key columns |
| Cartesian joins | Exponential data processing | Fix join conditions |
| Large result sets | Network + compute | Limit results, aggregate in Snowflake |
| Repeated queries | Redundant compute | Use materialized views or result caching |

### Query Optimization

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Clustering keys | 20-50% | M | Cluster on frequently filtered columns |
| Search optimization | 10-30% | S | Enable for point-lookup queries |
| Materialized views | 30-60% | M | Pre-compute frequent aggregations |
| Result caching | 20-40% | Free | Automatic for identical queries within 24h |
| Query tags | N/A (visibility) | S | Track costs per query type |

### Monitoring Expensive Queries

```sql
-- Find top-cost queries (by warehouse credits consumed)
SELECT
  query_id,
  warehouse_name,
  total_elapsed_time / 1000 as seconds,
  bytes_scanned / (1024*1024*1024) as gb_scanned,
  credits_used_cloud_services,
  query_text
FROM snowflake.account_usage.query_history
WHERE start_time > DATEADD('day', -7, CURRENT_TIMESTAMP())
ORDER BY total_elapsed_time DESC
LIMIT 20;
```

## Storage Optimization

| Pattern | Savings | Effort | Details |
|---|---|---|---|
| Time Travel reduction | 10-30% | S | Default 1 day for dev, 90 days for prod (Enterprise) |
| Transient tables for staging | 30-50% | S | No fail-safe period = less storage |
| Drop unused tables | Variable | S | Regular cleanup of unused objects |
| Zero-copy cloning | Variable | S | Use clones instead of copies for dev |
| Compression review | 5-10% | M | Snowflake auto-compresses, but data types matter |

### Time Travel + Fail-Safe Costs

| Object Type | Time Travel | Fail-Safe | Total Retention |
|---|---|---|---|
| Permanent table | 0-90 days (configurable) | 7 days | Up to 97 days of copies |
| Transient table | 0-1 day | 0 days | Up to 1 day of copies |
| Temporary table | 0-1 day | 0 days | Session-scoped |

**Storage cost impact:** A 1 TB table with 90-day time travel and 7-day fail-safe could
store up to 97 days of historical versions. If the table changes daily, storage could be
significantly higher than the current data size.

## Serverless Feature Costs

| Feature | Cost Basis | Optimization |
|---|---|---|
| **Snowpipe** | Credits per file loaded | Batch files to reduce per-file overhead |
| **Tasks** | Credits per execution | Minimize task frequency, batch operations |
| **Materialized Views** | Credits for maintenance | Only materialize frequently queried views |
| **Automatic Clustering** | Credits for re-clustering | Accept some staleness for less-critical tables |
| **Replication** | Credits + storage + transfer | Only replicate what's necessary |
| **Cortex AI** | Credits per request | Right-size model selection |

## Cost Attribution

### Resource Monitors

Set up resource monitors for governance:

```sql
-- Create resource monitor with credit quota
CREATE RESOURCE MONITOR daily_monitor
  WITH CREDIT_QUOTA = 100
  FREQUENCY = DAILY
  START_TIMESTAMP = IMMEDIATELY
  TRIGGERS
    ON 75 PERCENT DO NOTIFY
    ON 90 PERCENT DO NOTIFY
    ON 100 PERCENT DO SUSPEND;

-- Assign to warehouse
ALTER WAREHOUSE analytics_wh SET RESOURCE_MONITOR = daily_monitor;
```

### Query Tagging

Tag queries for cost attribution:

```sql
ALTER SESSION SET QUERY_TAG = 'team=data-eng;project=etl-pipeline';
```

### Account Usage Views

| View | Purpose |
|---|---|
| `WAREHOUSE_METERING_HISTORY` | Credit consumption per warehouse |
| `QUERY_HISTORY` | Per-query cost analysis |
| `STORAGE_USAGE` | Storage costs over time |
| `AUTOMATIC_CLUSTERING_HISTORY` | Clustering credit consumption |
| `PIPE_USAGE_HISTORY` | Snowpipe credit consumption |

### Key Metrics

| Metric | Formula | Target |
|---|---|---|
| Cost per query | Credits consumed / query count | Trending down |
| Warehouse utilization | Active time / total running time | >60% |
| Credit efficiency | Business queries / total credits | Improving |
| Storage per active TB | Storage cost / active data volume | Stable |
| Idle warehouse time | Idle minutes / total running minutes | <20% |

## Snowflake Cortex (AI)

Snowflake's AI features add to cost:

| Feature | Cost Basis |
|---|---|
| Cortex LLM functions | Credits per request |
| Cortex Search | Credits per query |
| Cortex Analyst | Credits per interaction |
| Cortex Fine-tuning | Training credits |

**Optimization:** Same model routing principles apply — use smaller models for simple tasks.

## Assessment Questions

1. What's the warehouse sizing strategy? Are sizes matched to workload types?
2. What's the auto-suspend setting? (Default 10 min is usually too long)
3. Are separate warehouses used for ETL vs. BI vs. ad-hoc?
4. What are the top 20 most expensive queries? Can they be optimized?
5. Is Time Travel set appropriately? (90 days for dev is wasteful)
6. Are transient tables used for staging/temp data?
7. Are resource monitors in place per warehouse?
8. What's the total cost breakdown (compute vs. storage vs. serverless)?
9. Are clustering keys in place for large, frequently queried tables?
10. Is Snowflake Cortex in use? Are model selections cost-optimized?