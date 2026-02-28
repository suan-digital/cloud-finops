# FinOps Foundation Framework Reference

The FinOps Framework (https://www.finops.org/framework/) is the industry standard for cloud
financial management. This reference covers the complete framework structure.

## Six FinOps Principles

1. **Teams need to collaborate** — Finance, technology, product, and leadership teams work
   together in near-real time. Silos create waste.

2. **Business value drives technology decisions** — Unit economics and business value metrics
   drive spending decisions, not just cost reduction. Cheapest isn't always best.

3. **Everyone takes ownership for their technology usage** — Engineers, not just finance, own
   their cloud usage and cost. Cost is a first-class efficiency metric from the start of the
   development lifecycle. Ownership at the point of decision is essential.

4. **FinOps data should be accessible, timely, and accurate** — Fast feedback enables better
   decisions. Data must be fresh, accurate, and available to all stakeholders.

5. **FinOps should be enabled centrally** — A central FinOps function enables and evangelizes
   best practices. It facilitates, not gatekeeps. The emphasis is on enabling the organization,
   not driving from the center.

6. **Take advantage of the variable cost model of the cloud** — Cloud's pay-as-you-go model
   is an opportunity, not just a billing mechanism. Design for variability and agile iteration.

## Three Phases

### Inform

**Goal:** Visibility, allocation, benchmarking. Where does the money go?

**Key activities:**
- Ingest cost and usage data from all providers
- Allocate costs to teams, products, and features
- Establish tagging standards and enforce coverage
- Create showback reports — teams must see their spend
- Set up anomaly detection for unexpected cost spikes
- Benchmark current spend against industry peers

**Signs of completion:**
- Anyone can answer "what are we spending and where?"
- Cost data is fresh (hours, not months)
- 80%+ of spend is attributed to owners
- Anomalies are detected within hours

**Common anti-pattern: Stuck in Inform**
Dashboards exist but nobody acts on them. Reports are generated but not reviewed. Teams know
what they spend but don't know why or what to do about it.

### Optimize

**Goal:** Right-sizing, rate optimization, waste elimination. How do we spend better?

**Key activities:**
- Right-size instances based on utilization data
- Purchase commitment instruments (RIs, Savings Plans, CUDs) for stable workloads
- Eliminate waste (zombie resources, orphaned volumes, idle endpoints)
- Optimize data transfer paths
- Implement scheduling for non-production environments
- Review and optimize storage tiers

**Signs of completion:**
- Commitment coverage matches stable workload baseline
- Right-sizing is a continuous process, not a one-time event
- Waste is measured and tracked (trending toward zero)
- Storage lifecycle policies are in place

**Common anti-pattern: Jumping to Optimize without Inform**
Buying Savings Plans without understanding usage patterns. Right-sizing without utilization
data. Commitment purchases based on guesswork rather than data.

### Operate

**Goal:** Governance, automation, continuous improvement. How do we stay efficient?

**Key activities:**
- Implement governance policies (tag enforcement, budget alerts, approval workflows)
- Automate recurring optimizations
- Establish review cadences (weekly cost reviews, monthly optimization sprints)
- Integrate cost awareness into engineering culture
- Continuous improvement — measure, adjust, repeat

**Signs of completion:**
- Cost governance is automated, not manual
- Optimization is a practice, not a project
- Cost awareness is embedded in engineering culture
- Waste reductions are sustained over quarters, not just achieved once

**Common anti-pattern: Optimize without Operate**
One-time cleanups that regress within months. No governance preventing waste from recurring.
Optimization is a project, not a practice. Savings disappear within a quarter.

## Four Domains & 22 Capabilities

### Domain 1: Understand Usage & Cost (4 capabilities)

| Capability | Description | Crawl | Walk | Run |
|---|---|---|---|---|
| **Data Ingestion** | Collect cost/usage data from all sources | Manual exports, single provider | Automated ingestion, multi-provider | Real-time, normalized (FOCUS), all sources |
| **Allocation** | Attribute costs to teams/products/features — includes tagging, labeling, and shared cost distribution | Basic account-level allocation, <50% tag coverage | Tag-based allocation, 70%+ coverage, proportional shared costs | Full allocation, 95%+ coverage, dynamic shared cost methodology, self-healing tags |
| **Reporting & Analytics** | Deliver cost insights to stakeholders | Basic monthly reports | Automated dashboards by audience | Self-service analytics, conversational cost queries |
| **Anomaly Management** | Detect and respond to unexpected cost changes | Manual discovery, monthly review | Automated alerts, weekly review | Real-time detection, automated response, <1hr to investigation |

### Domain 2: Quantify Business Value (5 capabilities)

| Capability | Description | Crawl | Walk | Run |
|---|---|---|---|---|
| **Planning & Estimating** | Forecast cost of new projects/features | No cost estimation | Cost included in project planning | Automated estimation in CI/CD |
| **Forecasting** | Predict future cloud spend | Historical extrapolation | Statistical models, 80% accuracy | ML-based, scenario planning, 90%+ accuracy |
| **Budgeting** | Set and manage cloud budgets | Annual, top-down | Quarterly, team-level | Dynamic, rolling, aligned to business metrics |
| **Benchmarking** | Compare performance against peers/targets | No benchmarking | Internal benchmarking across teams | Industry benchmarking, unit economics comparison |
| **Unit Economics** | Cost per business unit (user, request, etc.) | Not tracked | Primary metrics defined | Comprehensive, drives architecture decisions |

### Domain 3: Optimize Usage & Cost (5 capabilities)

| Capability | Description | Crawl | Walk | Run |
|---|---|---|---|---|
| **Architecting for Cloud** | Design for cost efficiency | Reactive — fix after deployment | Cost in architecture reviews | Cost is a first-class design constraint |
| **Workload Optimization** | Right-size and schedule workloads | Ad-hoc right-sizing | Regular right-sizing cycles | Continuous, automated right-sizing |
| **Rate Optimization** | Reduce unit costs via commitments/pricing | No commitments | Basic SP/RI coverage, 60-70% util | Managed portfolio, 85%+ utilization |
| **Licensing & SaaS** | Optimize software licensing and SaaS costs | No visibility | License inventory tracked | Optimized, right-sized, consolidated |
| **Sustainability** | Minimize environmental impact | Not tracked | Carbon footprint measured | Carbon-aware scheduling, region selection |

### Domain 4: Manage the FinOps Practice (8 capabilities)

| Capability | Description | Crawl | Walk | Run |
|---|---|---|---|---|
| **FinOps Practice Operations** | Run the FinOps function | Part-time role | Dedicated team | Embedded in engineering culture |
| **FinOps Education & Enablement** | Build FinOps skills across the organization | Ad-hoc knowledge sharing | Training programs, certification paths | Continuous learning culture, FinOps embedded in onboarding |
| **Onboarding Workloads** | Bring new workloads under FinOps governance | Manual, inconsistent | Standardized onboarding process | Automated, self-service |
| **Policy & Governance** | Enforce cost-related policies | Manual reviews | Policy-as-code, basic enforcement | Automated guardrails, self-healing |
| **FinOps Assessment** | Evaluate and improve FinOps maturity | No formal assessment | Annual assessment | Continuous improvement metrics |
| **Invoicing & Chargeback** | Bill internal teams for cloud usage | Shared cost center | Showback reports | Full chargeback with team accountability |
| **FinOps Tools & Services** | Select and manage FinOps tooling | Native cloud tools only | Third-party tools integrated | Unified platform, custom integrations |
| **Intersecting Disciplines** | Connect FinOps with DevOps, Security, etc. | Siloed | Some collaboration | Fully integrated practices |

## FinOps Scopes

FinOps now extends beyond public cloud. The "Cloud+" era covers:

| Scope | Examples |
|---|---|
| **Public Cloud** | AWS, Azure, GCP, OCI (traditional FinOps scope) |
| **SaaS** | Salesforce, Snowflake, Databricks, GitHub, Datadog |
| **Data Center** | On-premises, colocation, hybrid infrastructure |
| **AI** | LLM inference, GPU compute, model training, agentic workflows |
| **Licensing** | Software licenses, enterprise agreements, marketplace purchases |

## FinOps Personas

### Core Personas

These are the primary stakeholders in any FinOps practice:

| Persona | Role in FinOps | Key Concerns |
|---|---|---|
| **FinOps Practitioner** | Central FinOps function — facilitates, evangelizes, enables | Capability maturity, tooling, process adoption, cross-team alignment |
| **Engineering / DevOps** | Owns cloud usage at the point of decision | Architecture efficiency, right-sizing, IaC cost patterns, deployment cost |
| **Finance / Procurement** | Manages budgets, forecasts, and vendor contracts | Unit economics, forecasting accuracy, commitment ROI, chargeback |
| **Executive (CTO/CFO/CIO)** | Sponsors and funds FinOps, sets organizational direction | Business impact, cost trends, strategic investments, risk |
| **Product Owner** | Connects cloud cost to product economics | Cost per feature, cost per customer, budget impact on roadmap |
| **Platform Engineering** | Controls infrastructure abstractions that determine cost structure | Cost-efficient defaults, golden paths, namespace attribution, self-service |

### Allied Personas

These stakeholders intersect with FinOps in specific domains:

| Persona | FinOps Intersection |
|---|---|
| **ITAM (IT Asset Management)** | License optimization, SaaS rationalization, hybrid cost modeling |
| **Security** | Compliance cost, secure-by-default architectures, audit trail |
| **Sustainability / ESG** | Carbon-aware computing, GreenOps alignment, emissions reporting |
| **Data / ML Engineering** | Training cost optimization, inference economics, GPU utilization |
| **Procurement** | Contract negotiation, commitment instruments, vendor management |

## FinOps and Platform Engineering

Platform engineering teams are natural FinOps allies — they control the infrastructure abstractions
that determine cost structure. When platform teams build cost-efficient defaults, every team that
uses the platform inherits good economics without extra effort.

### Integration Points

| Platform Capability | FinOps Opportunity |
|---|---|
| Internal developer platform | Embed cost defaults (right-sized templates, auto-scheduling for non-prod) |
| Service catalog | Include cost estimates per template — engineers see cost before they deploy |
| Golden paths | Design cost-efficient by default — efficient is the easy path, not the exception |
| Kubernetes platform | Namespace cost attribution, resource quotas, Karpenter/spot defaults |
| CI/CD platform | PR-time cost estimation (Infracost integration), deployment cost tracking |
| Observability platform | Include cost metrics alongside latency and error rates in service dashboards |

### Why This Matters

The most effective FinOps organizations don't rely on cost reviews and dashboards alone. They
bake efficiency into the platform itself:

- A service template that provisions a right-sized instance by default prevents over-provisioning
  at creation time — no review needed.
- A CI pipeline that shows cost delta on every PR makes cost a visible design constraint —
  no separate tooling needed.
- A Kubernetes platform that sets resource quotas per namespace prevents unbounded growth —
  no manual policing needed.

Platform engineering makes the efficient path the default path. That's Ri-level behavior
encoded in infrastructure.

## FOCUS Specification

The **FinOps Open Cost & Usage Specification** (FOCUS) is the open-source standard for
normalizing cost and usage data across providers.

**Key concepts:**
- Standard column names across providers (BilledCost, EffectiveCost, UsageQuantity, etc.)
- Normalizes billing concepts (amortized costs, on-demand equivalents)
- Enables multi-cloud cost comparison without custom mapping
- Supported by AWS (CUR 2.0), Azure, GCP, and major FinOps vendors

**When to reference FOCUS:**
- Multi-cloud environments needing unified cost reporting
- Data standardization projects
- Evaluating FinOps tools (FOCUS compliance is a quality signal)
- Building custom cost analytics

**Specification:** https://focus.finops.org/

## FinOps for AI

The FinOps Foundation's working group on AI addresses the unique challenges of AI/ML cost
management:

**AI-specific KPIs:**
- Cost per inference
- Training cost efficiency (performance gained per dollar)
- Token consumption per workflow
- GPU/TPU resource utilization
- Cost per AI-generated output
- Model cost efficiency (performance per dollar per parameter)

**AI-specific challenges:**
- Inference costs dominate operational AI spend
- GPU pricing and capacity planning differ from traditional compute
- Model selection has exponential cost implications
- Agentic workflows multiply token consumption 5-25x
- Hidden infrastructure costs create 4-5x multiplier on visible AI spend

**Reference:** https://www.finops.org/wg/finops-for-ai/

## Assessment Using the Framework

### Quick Assessment Checklist

For each domain, determine the maturity of the highest-impact capability:

| Domain | Key Capability | Current Maturity | Target | Gap |
|---|---|---|---|---|
| Understand Usage & Cost | Allocation | ? | Walk | ? |
| Quantify Business Value | Unit Economics | ? | Walk | ? |
| Optimize Usage & Cost | Rate Optimization | ? | Walk | ? |
| Manage the Practice | Policy & Governance | ? | Walk | ? |

### Mapping to Shuhari

| Shuhari Stage | Typical Framework Profile |
|---|---|
| **Shu** | Most capabilities at Crawl. 1-2 at Walk. Focus on Domain 1. |
| **Early Ha** | Domain 1 at Walk. Domain 3 emerging. Beginning Domain 2. |
| **Mid Ha** | Domains 1-3 at Walk. Domain 4 developing. |
| **Late Ha** | Most at Walk, some at Run. Strong Domain 4. |
| **Ri** | Framework assessment no longer relevant — practices are internalized. |

### Key Benchmarks

| Metric | Poor | Average | Good | Excellent |
|---|---|---|---|---|
| Waste percentage | >35% | 25-35% | 15-25% | <15% |
| Tagging coverage | <50% | 50-70% | 70-90% | >90% |
| Commitment utilization | <60% | 60-75% | 75-85% | >85% |
| Cost attribution | <50% | 50-70% | 70-90% | >90% |
| Anomaly detection time | >1 month | 1 week | 1 day | <1 hour |
| Forecasting accuracy | >30% variance | 20-30% | 10-20% | <10% |