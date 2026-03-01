# Architecture-Cost Alignment

**Core insight: 80% of cloud costs are locked in at design time, not deployment time.**

If cost isn't a first-class design constraint alongside security and reliability, optimization
is retrofitting. By the time finance reviews a quarterly cloud bill, the architectural decisions
that shaped it happened months ago, buried in pull requests no one thought to question.

FinOps isn't a finance discipline. It's an architecture discipline.

## The Misplaced Accountability Problem

The structural dysfunction: finance teams review costs quarterly, but engineers make
architectural decisions that determine those costs daily.

**The timeline of a cost decision:**
1. Engineer chooses synchronous API pattern over async queue (Tuesday afternoon)
2. Code merges (Wednesday)
3. Cost implications compound silently — higher compute, scaling characteristics, cold starts
4. Finance sees elevated bill (next quarter)
5. Engineer has moved to three other projects
6. Refactoring requires a sprint nobody budgeted

The gap between cost decision and feedback is measured in months, not minutes.

## Cost as a First-Class Design Constraint

Just as we treat security, reliability, and performance as architectural concerns with explicit
trade-offs, cost must be treated the same way.

### Architectural Cost Traps

**1. Synchronous vs. Asynchronous Patterns**

A REST API that blocks while processing costs differently than an event-driven architecture.
The async pattern can handle 10x the load at half the compute cost — but only if you design
for eventual consistency from the start.

| Pattern | Cost Characteristic | When to Use |
|---|---|---|
| Synchronous REST | Linear scaling with request volume | Real-time user-facing responses |
| Async queue + workers | Decouple ingestion from processing | Background processing, batch ops |
| Event-driven | Pay only when events fire | Intermittent workloads, webhooks |
| Streaming | Constant throughput cost | Real-time data pipelines |

**2. Data Retention Policies**

"Keep everything forever" isn't a business requirement. It's an unexamined default with
compounding storage costs.

| Data Type | Typical Hot Retention | Then Move To | Final Tier |
|---|---|---|---|
| Application logs | 7-30 days | Warm (90 days) | Archive or delete |
| Audit logs | 90 days | Cold (1 year) | Archive (compliance period) |
| User data | Active period | Warm after inactivity | Archive per policy |
| Analytics events | 30 days hot | Data warehouse | Cold after 1 year |
| ML training data | Active training | Cold | Archive after model retired |

**3. Caching Strategies**

Adding a cache changes your cost curve fundamentally — trading memory cost for reduced database
and API calls. The decision point is architecture review, not capacity planning.

| Cache Type | Cost Trade-off | Break-Even |
|---|---|---|
| CDN (CloudFront, etc.) | Edge cache vs. origin compute | >100 req/sec to same content |
| Application cache (Redis) | Memory cost vs. DB reads | When DB cost exceeds cache cost |
| API response cache | Memory vs. upstream API calls | Any repeated external API call |
| Prompt/response cache | Cache storage vs. inference cost | Any repeated AI query |

**4. Observability Granularity**

High-cardinality metrics and verbose logging provide insight at a cost.

| Decision | Cost Impact |
|---|---|
| Custom metrics (high cardinality) | $0.30/metric/month at scale — 10K metrics = $3K/month |
| Log verbosity (DEBUG in production) | 5-10x storage cost vs. INFO level |
| Trace sampling (100% vs. 10%) | 10x difference in APM costs |
| Log retention (90 days vs. 30 days) | 3x storage cost |

**5. Multi-Region Architecture Decisions**

Multi-region is one of the most expensive architectural choices — a 2-3x cost multiplier that
compounds across every layer of the stack. Yet it's often adopted without a rigorous cost-vs-benefit
analysis.

| Driver | Justifies Multi-Region? | Cheaper Alternative to Evaluate First |
|---|---|---|
| Regulatory/data residency compliance | Yes — often mandatory | Confirm actual legal requirements (often narrower than assumed) |
| Sub-50ms latency for global users | Usually yes | CDN + edge caching for read-heavy workloads |
| Disaster recovery (RPO <1 hour) | Sometimes | Cross-region backups + automated restore (cheaper than active-active) |
| High availability (99.99%+) | Rarely | Multi-AZ in a single region typically delivers 99.99% |
| "We might need it someday" | No | Design for portability, deploy when justified |

**Cost multiplier breakdown:**

| Component | Multi-Region Multiplier | Notes |
|---|---|---|
| Compute | 2x+ | Duplicate instances in each region |
| Database | 1.5-3x | Cross-region replication, conflict resolution |
| Data transfer | $0.01-0.02/GB (AWS/Azure), $0.01-0.08/GB (GCP) | Continuous replication cost |
| Load balancing | 1.5-3x | Global load balancer + regional balancers |
| Operational overhead | 2-3x | Deployment complexity, testing, incident response |

**Before committing to multi-region, quantify:**
1. What is the cost of downtime per hour? If it's less than the annual multi-region premium, single-region + fast recovery is cheaper.
2. What latency do users actually experience vs. require? Measure before assuming multi-region is needed.
3. Can CDN, edge compute, or read replicas solve the problem at 10-20% of the cost?

### Design-Time Cost Patterns

When reviewing architecture, assess these patterns:

**Cost-efficient patterns:**
- Event-driven architectures for variable workloads
- Serverless for unpredictable traffic (pay per invocation, not per hour)
- Multi-tier storage with lifecycle policies
- Read replicas for read-heavy workloads (cheaper than scaling primary)
- Spot/preemptible instances for fault-tolerant batch processing
- ARM-based instances (Graviton, Ampere) for compatible workloads (20-40% cheaper)

**Cost-dangerous patterns:**
- Monolithic databases that must scale vertically (expensive ceiling)
- Synchronous microservice chains (each hop adds latency and cost)
- Homogeneous instance fleets (same size regardless of workload)
- Cross-region replication without clear latency or compliance requirement
- Real-time processing where batch would suffice
- Premium storage tiers used as defaults

## Shift-Left Cost Visibility

Cost impact must be visible before code merges, not after deployment.

### PR-Time Cost Estimation

Tools like Infracost integrate into pull requests:
```
Monthly cost will increase by $776/month
$427/month → $1,203/month

+ aws_instance.api
  +$776/month (m5.xlarge → m5.4xlarge)
```

Shift-left cost tools are gaining adoption rapidly — the curve mirrors security scanning
a decade ago.

### Unit Economics as Architectural Metrics

Move beyond "what did we spend" to business-connected metrics:

| Metric | Formula | What It Reveals |
|---|---|---|
| Cost per request | Total infra cost / request count | API efficiency |
| Cost per active user | Total cost / MAU | User-level economics |
| Cost per transaction | Processing cost / transaction count | Business unit economics |
| Cost per GB processed | Compute cost / data volume | Data pipeline efficiency |
| Cost per AI inference | Total AI cost / inference count | AI unit economics |

These metrics connect architectural decisions to business outcomes in a way raw spend numbers
never can.

## Engineering Ownership Model

If cost is an architectural concern, engineering owns optimization — not finance.

**Finance owns:** Budgeting, forecasting, procurement, strategic financial planning
**Engineering owns:** Optimization, architecture decisions, resource efficiency

### Healthy Cost Ownership Indicators

- [ ] Teams predict their spend directionally
- [ ] Cost anomalies trigger investigation like production incidents
- [ ] Cost conversations happen in architecture reviews, not just finance reviews
- [ ] Engineers instrument for cost visibility alongside latency and error rates
- [ ] Cost appears in service SLIs alongside availability and latency

### Building the Engineering Cost Competency

Understanding how architectural decisions translate to monthly spend is a core engineering skill,
not optional expertise.

**Steps to build the competency:**
1. Add cost dashboards to service ownership pages
2. Include cost impact in architecture decision records (ADRs)
3. Run "cost retrospectives" alongside incident retrospectives
4. Include cost questions in interview loops for senior engineers
5. Celebrate cost optimizations like you celebrate performance improvements

Organizations with mature FinOps practices significantly reduce waste. The difference isn't
better tools — it's placed accountability.

## Assessment Questions

When evaluating architecture-cost alignment, ask:

1. Do architecture reviews include cost impact analysis?
2. Is there PR-time cost visibility? (Infracost, custom tooling, manual estimates)
3. Are unit economics tracked as architectural metrics?
4. Do engineers own cost optimization? Or is it "finance's job"?
5. Are cost anomalies investigated like incidents?
6. What's the feedback loop time between cost decision and cost visibility?
7. Are there documented architectural cost trade-offs in design docs?
8. Does the team know which architectural decisions drive 80% of their spend?
9. Was the multi-region decision justified with a cost-vs-downtime analysis?

## When NOT to Optimize

Not every cost is worth reducing. Optimization has costs of its own.

### Don't Optimize When:

- **Velocity matters more than efficiency.** A startup burning $5K/month extra to ship 2 weeks
  faster is making the right trade-off. Time-to-market has a cost too — it's just harder to
  measure than a cloud bill.
- **The optimization requires architectural changes during a freeze.** Stability has value.
  If the team is in a critical launch window or incident recovery, the disruption risk outweighs
  the savings.
- **Savings are under the effort threshold.** $200/month savings requiring 2 weeks of engineering
  is a bad trade unless it's also reducing operational complexity. Engineering time has a cost —
  often $80-150/hour loaded.
- **It introduces operational risk.** Aggressive spot usage on stateful workloads saves money
  until it doesn't. Savings Plans at 100% coverage leaves zero headroom for workload reduction.

### The Trade-Off Framework

For every optimization recommendation, assess:

| Factor | Question |
|---|---|
| **Savings** | What's the monthly $ impact? |
| **Effort** | How many engineering days? |
| **Risk** | What breaks if this goes wrong? |
| **Reversibility** | Can we undo this quickly? |
| **Velocity impact** | Does this slow down feature delivery? |

**Rule of thumb:** Monthly savings should exceed 3x the one-time engineering cost within 6 months.
High-risk optimizations need 5x or more.

**Example:** A $1,500/month savings that requires 5 engineering days ($6,000 loaded cost) pays
back in 4 months at 1x, 12 months at 3x. That's marginal. But if the same change also simplifies
operations and reduces on-call burden, the total value exceeds the cost number.