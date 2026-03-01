# Azure OpenAI Cost Optimization Reference

Azure OpenAI Service-specific pricing, PTU management, spillover control, and optimization
patterns.

## Azure OpenAI Pricing Models

### Pay-As-You-Go (Token-Based)

Standard per-token pricing through Azure:

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|---|---|---|
| GPT-4o | $2.50 | $10.00 |
| GPT-4o-mini | $0.15 | $0.60 |
| GPT-4 Turbo | $10.00 | $30.00 |
| GPT-3.5 Turbo | $0.50 | $1.50 |
| o1 | $15.00 | $60.00 |
| o1-mini | $3.00 | $12.00 |

*Prices change. Check Azure OpenAI pricing page for current rates.*

### Provisioned Throughput Units (PTUs)

PTUs provide reserved capacity with guaranteed throughput and latency.

**How PTUs work:**
- Purchase a number of PTUs per model per region
- 1 PTU = a specific throughput capacity (varies by model)
- Monthly commitment (minimum)
- No per-token charges — pay for capacity, not consumption

**PTU sizing reference (approximate):**
| Model | Tokens per minute per PTU |
|---|---|
| GPT-4o | ~2,500 |
| GPT-4o-mini | ~37,000 |
| GPT-4 Turbo | ~2,500 |

*Values are approximate. Use Azure's PTU sizing calculator for accurate estimates.*

### Global vs. Regional Deployments

| Deployment Type | Characteristics |
|---|---|
| **Standard (Regional)** | Specific region, pay-as-you-go or PTU |
| **Global Standard** | Auto-routes across regions, pay-as-you-go |
| **Global Provisioned** | PTUs across global pool, better utilization |
| **Data Zone** | Restricted to geographic zone (EU, US) |

**Cost implication:** Global deployments can improve PTU utilization by spreading demand across
regions. Regional deployments provide data residency control.

## PTU Optimization

### The PTU Decision

**Use PTUs when:**
- Steady, predictable inference volume
- Latency SLAs require guaranteed performance
- Monthly token volume exceeds PTU break-even point
- Data residency requires specific regional capacity

**Use pay-as-you-go when:**
- Variable or unpredictable traffic
- Experimenting with different models
- Low volume (below PTU break-even)
- Flexibility more valuable than discount

### PTU Utilization Monitoring

| Metric | Where to Find | Target |
|---|---|---|
| PTU utilization % | Azure Portal, Diagnostic Logs | 70-85% |
| Requests per PTU | Azure Monitor | Stable or growing |
| Throttled requests | Azure Monitor | <5% |
| Spillover to pay-as-you-go | Cost Management | <15% |

### PTU Right-Sizing

| Utilization | Assessment | Action |
|---|---|---|
| <40% | Significantly over-provisioned | Reduce PTUs or move to PAYG |
| 40-60% | Moderately over-provisioned | Analyze if traffic will grow |
| 60-80% | Good utilization | Maintain, monitor trends |
| 80-90% | Optimal | Watch for throttling |
| >90% | Under-provisioned | Add PTUs or accept spillover |

### Spillover Management

When PTU capacity is exceeded, requests can spill over to pay-as-you-go pricing:

**Monitoring spillover:**
- Track throttled request counts in Azure Monitor
- Compare PTU cost vs. spillover cost monthly
- Calculate blended cost per token

**Spillover strategy:**
- Provision PTUs for 70th percentile of demand
- Accept 10-20% spillover as cost-optimal
- If spillover consistently >20%, increase PTUs
- Use model routing to redirect low-priority traffic away from PTU models during peaks

## Model Selection for Cost

### Azure OpenAI Model Routing

| Task | Recommended Model | Cost Tier |
|---|---|---|
| Simple classification | GPT-4o-mini | Lowest |
| Entity extraction | GPT-4o-mini | Lowest |
| Summarization | GPT-4o-mini or GPT-4o | Low-Medium |
| Content generation | GPT-4o | Medium |
| Complex reasoning | GPT-4o or o1-mini | Medium-High |
| Multi-step reasoning | o1 | Highest |

**GPT-4o-mini is often the right choice.** At $0.15/M input and $0.60/M output, it handles
most enterprise tasks at a fraction of the cost of larger models.

### Reasoning Model Economics

o1 and o1-mini use "reasoning tokens" (internal thinking):
- Reasoning tokens are billed at output token rates
- A query may consume 3-10x more tokens than visible in the response
- Cost per request can be 5-20x higher than equivalent GPT-4o request

**When to use reasoning models:**
- Complex multi-step problems where accuracy justifies cost
- Mathematical/logical reasoning tasks
- Reduce when: simple tasks routed to reasoning models by default

## Azure-Specific Optimization

### Content Filtering Cost

Azure OpenAI includes mandatory content filtering:
- Adds latency to every request
- No direct cost per filter, but latency affects throughput capacity
- Custom content filters may affect PTU utilization

### Managed Identity & VNET Integration

| Feature | Cost Impact |
|---|---|
| Private Endpoints | Additional networking cost, improved security |
| Managed Identity | No additional cost, recommended for auth |
| VNET Integration | May increase data transfer costs |

### Azure OpenAI + Azure AI Services

Bundling with other Azure AI services (Cognitive Services, AI Search):
- AI Search for RAG adds cost (index size, query volume, semantic ranker)
- Content Safety API adds per-call cost
- Consider total AI stack cost, not just OpenAI charges

## Cost Attribution

### Azure Tags

Tag Azure OpenAI deployments:
- Deployment name → feature mapping
- Resource group → team/project mapping
- Custom tags for cost center, environment

### Diagnostic Logs

Enable diagnostic logging for detailed usage tracking:
- Per-request token counts
- Model and deployment identification
- Latency metrics for performance/cost correlation
- Error rates for retry cost analysis

### Azure Cost Management

Azure OpenAI appears under:
- Service: `Azure AI services` or `Cognitive Services`
- Meter category: `Azure OpenAI`
- Meter subcategory: Model-specific

**Limitation:** Azure Cost Management doesn't break down by deployment or feature — you need
diagnostic logs for that level of detail.

## Integration Patterns

### Azure OpenAI vs. OpenAI Direct

| Dimension | Azure OpenAI | OpenAI Direct |
|---|---|---|
| Billing | Azure billing consolidation | Separate billing |
| Data residency | Regional/zone control | OpenAI data centers |
| Compliance | Azure compliance certifications | OpenAI compliance |
| PTU availability | Yes | No (OpenAI has tiers) |
| Latest models | May lag by weeks | Immediate access |
| Content filtering | Mandatory | Optional |

### Hybrid Approach

Some organizations use both:
- Azure OpenAI for production (compliance, PTUs, billing consolidation)
- OpenAI direct for experimentation (latest models, flexibility)

**Cost tracking challenge:** Track both billing streams to get total OpenAI spend.

## Assessment Questions

1. Which Azure OpenAI models are deployed? Are they right-sized for their tasks?
2. Are PTUs in place? What's the utilization rate?
3. How much spillover to pay-as-you-go occurs?
4. Is reasoning model usage justified? What's the reasoning token overhead?
5. Is GPT-4o-mini used where appropriate? (Or is everything hitting GPT-4o?)
6. Are diagnostic logs enabled for per-request cost tracking?
7. What's the Azure AI Search cost alongside Azure OpenAI? (RAG total cost)
8. Is there a model routing strategy?