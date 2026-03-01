# AI Value Governance

**Skip this reference if the organization is not investing significantly in AI or struggling
with AI ROI accountability.**

As AI spending scales from experiments to enterprise programs, the gap between investment and
demonstrated value becomes a governance problem. Most companies cannot confidently evaluate
AI ROI — they are making investment decisions blind.

## The AI Investment Problem

### Why Standard Governance Fails for AI

Traditional IT governance evaluates projects against clear deliverables and timelines. AI
projects have different characteristics:

| Dimension | Traditional IT | AI Projects |
|---|---|---|
| Cost predictability | High — scope determines cost | Low — usage determines cost |
| Value timeline | Clear milestones | Emergent, often non-linear |
| Success criteria | Feature delivered | Quality threshold met |
| Cost driver | Infrastructure provisioned | Tokens consumed, data processed |
| Scaling cost | Roughly linear | Often exponential (agentic) |
| Failure mode | Late delivery | Poor quality, cost overrun |

### The Agentic Escalation

Many agentic AI projects get canceled due to cost and complexity. The failure pattern:
1. Prototype works great in demo ($50/month in API calls)
2. Production pilot looks promising ($500/month)
3. Scale to 10 teams → agent-to-agent communication multiplies ($50,000/month)
4. CFO asks for ROI justification → nobody can attribute value to specific agents
5. Project canceled

## AI Investment Council

### Structure

Organizations with multiple AI initiatives need centralized governance — not to gatekeep, but
to ensure portfolio-level visibility and resource allocation.

**Recommended composition:**
- CTO or VP Engineering (technical feasibility, architecture)
- CFO or VP Finance (investment accountability, budget)
- Head of Product (business value alignment)
- FinOps lead (cost visibility, optimization)
- AI/ML lead (technical strategy, model selection)
- Data lead (data readiness, pipeline costs)

**Cadence:** Monthly review of all AI initiatives. Weekly during rapid scaling.

### Investment Categories

Classify AI initiatives by investment stage:

| Stage | Investment Level | Governance | Kill Criteria |
|---|---|---|---|
| **Exploration** | <$5K/month | Team-level approval | No formal criteria — experiments expected to fail |
| **Pilot** | $5K-$25K/month | Manager approval + cost tracking | No measurable user/business impact after 3 months |
| **Production** | $25K-$100K/month | AI council approval | Cost per outcome exceeds business value |
| **Scale** | >$100K/month | Executive + AI council | Unit economics don't improve with scale |

### Stage Gate Framework

Each transition requires explicit evidence:

**Exploration → Pilot:**
- [ ] Business problem clearly defined
- [ ] Baseline metric established (what does "better" mean?)
- [ ] Cost tracking in place (not just API costs — full infrastructure)
- [ ] Data requirements identified and available
- [ ] Success criteria defined with timeline

**Pilot → Production:**
- [ ] Pilot results meet success criteria
- [ ] Full cost visibility (4-5x multiplier accounted for)
- [ ] Production architecture designed with cost constraints
- [ ] Model selection justified (not defaulting to most expensive)
- [ ] Monitoring and observability in place
- [ ] Rollback plan defined

**Production → Scale:**
- [ ] Unit economics positive and documented
- [ ] Cost-per-outcome trending down (not up) with volume
- [ ] Architecture supports scaling without exponential cost growth
- [ ] Model routing optimized for cost-quality trade-off
- [ ] Commitment strategy in place for stable workloads
- [ ] ROI measurable and attributable

## AI ROI Measurement

### The ROI Framework

AI ROI must account for total cost (4-5x the visible bill) and both direct and indirect value:

**Total AI Cost =**
Direct model costs
+ Data infrastructure costs
+ Monitoring and governance costs
+ Storage and data movement costs
+ Integration and orchestration costs
+ Team time (prompt engineering, monitoring, tuning)

**AI Value =**
Direct revenue impact (new features, improved conversion)
+ Cost avoidance (automation replacing manual processes)
+ Time savings (employee productivity gains)
+ Quality improvement (fewer errors, better decisions)
+ Customer experience improvement (measurable satisfaction/retention)

### Measurement Approaches

| Approach | Best For | Limitation |
|---|---|---|
| **A/B testing** | Features with measurable conversion | Requires traffic volume |
| **Before/after comparison** | Process automation | Confounding variables |
| **Cost per outcome** | Transaction-oriented AI | Requires good attribution |
| **Time savings audit** | Productivity tools | Self-reported, often inflated |
| **Customer satisfaction** | Support/experience AI | Lagging indicator |

### AI-Specific KPIs by Use Case

| Use Case | Primary KPI | Cost Metric |
|---|---|---|
| Customer support | Resolution rate, CSAT | Cost per resolution |
| Content generation | Output volume, quality score | Cost per asset |
| Code assistance | Developer velocity, bug rate | Cost per PR |
| Data analysis | Insight generation rate | Cost per report |
| Search/retrieval | Relevance score, query success | Cost per query |
| Agentic workflows | Task completion rate | Cost per completed task |

## Portfolio Management

### Rationalization

Quarterly review all AI initiatives:

1. **Continue and invest:** Positive ROI, scaling opportunity, strategic value
2. **Continue and optimize:** Positive ROI but cost optimization needed
3. **Reassess:** Unclear ROI — set 90-day deadline for measurable results
4. **Sunset:** Negative ROI with no path to positive, or duplicate capability

### Consolidation Opportunities

Common redundancies to eliminate:

| Pattern | Waste | Fix |
|---|---|---|
| Multiple teams using different LLM providers for similar tasks | Duplicate costs, no volume leverage | Standardize on 1-2 providers, negotiate volume pricing |
| Each team building custom AI infrastructure | Duplicate pipelines, monitoring, storage | Platform team provides shared AI infrastructure |
| Shadow AI spending | Untracked, ungoverned | Centralized procurement + audit |
| Multiple RAG implementations | Duplicate vector stores, embedding compute | Shared knowledge base service |

### Budget Allocation

Allocate AI budget across the portfolio:

| Category | % of AI Budget | Purpose |
|---|---|---|
| Production workloads | 50-60% | Running proven AI features |
| Optimization | 15-20% | Improving cost efficiency of production AI |
| Experimentation | 10-20% | New use cases, model evaluation |
| Infrastructure | 10-15% | Shared platform, tooling, monitoring |

## Organizational Patterns

### Who Owns AI Costs?

| Model | Pros | Cons |
|---|---|---|
| **Centralized AI team** | Consistent governance, volume leverage | Bottleneck, disconnected from business |
| **Federated (each team)** | Close to business needs, fast | Duplicated infrastructure, no coordination |
| **Hub-and-spoke** | Central platform + team autonomy | Requires strong platform team |

**Recommendation:** Hub-and-spoke. Central team provides infrastructure, model access, and
cost visibility. Business teams own their use cases, costs, and ROI.

### AI FinOps Integration

AI cost management should integrate with existing FinOps practice:

1. **Extend tagging standards** to include AI-specific dimensions (model, feature, use_case)
2. **Add AI KPIs** to existing FinOps dashboards
3. **Include AI in commitment strategy** (provisioned throughput decisions)
4. **Apply the same Shuhari maturity model** — AI FinOps starts at Shu even if cloud FinOps
   is at Ha

## Assessment Questions

1. Is there a centralized view of all AI initiatives and their costs?
2. Can the organization calculate ROI for each AI feature?
3. Are there stage gates for AI investments (exploration → pilot → production → scale)?
4. Who approves new AI spending? What's the threshold?
5. How many separate AI tools/platforms are in use? Any overlap?
6. Is there a kill criteria for AI projects that aren't delivering value?
7. Is AI spending included in the FinOps practice or managed separately?
8. What's the total AI headcount cost (not just infrastructure)?