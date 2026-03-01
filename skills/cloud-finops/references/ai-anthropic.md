# Anthropic / Claude Cost Optimization Reference

Anthropic Claude-specific pricing, optimization patterns, and cost management strategies.

## Claude Model Pricing

### Current Model Lineup (as of early 2026)

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Best For |
|---|---|---|---|
| **Claude Opus 4** | $15.00 | $75.00 | Complex reasoning, research, multi-step analysis |
| **Claude Sonnet 4** | $3.00 | $15.00 | Balanced performance/cost, enterprise workhorse |
| **Claude Haiku 3.5** | $0.80 | $4.00 | Fast, high-volume, simple tasks |

*Prices change. Check https://www.anthropic.com/pricing for current rates.*

### Extended Thinking

Claude models support "extended thinking" — internal reasoning before responding:
- Thinking tokens are billed at output token rates
- Can significantly increase per-request cost
- Controllable via `budget_tokens` parameter
- Worth it for complex tasks, wasteful for simple ones

**Cost impact:** A request that generates 500 output tokens with 2,000 thinking tokens costs
~5x what the same request would cost without extended thinking.

**Optimization:** Set `budget_tokens` appropriately for each use case. Don't enable extended
thinking for classification, formatting, or simple extraction tasks.

### Context Window

| Model | Context Window | Notes |
|---|---|---|
| Claude Opus 4 | 200K tokens | Long-context adds to input cost |
| Claude Sonnet 4 | 200K tokens | Same window, lower cost |
| Claude Haiku 3.5 | 200K tokens | Most cost-effective for long context |

**Cost consideration:** Sending 200K tokens of context at Opus pricing = $3.00 per request
just for input. Same context at Haiku = $0.16. Choose model based on task, not habit.

## Cost Optimization Strategies

### Prompt Caching

Anthropic supports prompt caching for repeated system prompts and context:

**How it works:**
- Cache frequently used prompt prefixes (system prompts, reference documents)
- **Cache write:** 1.25x base input price (25% premium to write to cache)
- **Cache read (hit):** 0.1x base input price (90% discount on cached tokens)
- **TTL:** 5 minutes by default, refreshed on each cache hit
- Minimum cacheable prefix: 1024 tokens (all models)

**Cost mechanics:** Every cache miss pays the 1.25x write cost. Every hit within the 5-minute TTL pays 0.1x. If requests are infrequent (>5 min apart), caching costs more — you pay the write premium every time with no read benefit.

**Break-even:** You need at least 2 cache reads per TTL window to save money. At 3+ reads per window, savings are substantial. For high-frequency use cases (chatbots, agentic loops), caching is almost always worth it.

**Best use cases:**
- System prompts repeated across requests (high hit rate)
- Reference documents used in RAG (stable prefix)
- Few-shot examples included in every call
- Agentic workflows with repeated tool definitions
- Long context windows with stable prefixes

**Savings example (Sonnet, 10K token system prompt, 1000 req/day):**

| Scenario | Daily Cost | Savings vs. No Cache |
|---|---|---|
| No cache | $30.00/day | — |
| Cache, 1 req every 10 min (frequent misses) | $27.50/day | 8% |
| Cache, 5 req/min (high hit rate) | $4.50/day | 85% |
| Cache, 20 req/min (very high hit rate) | $3.20/day | 89% |

*Actual savings depend on request frequency relative to the 5-minute TTL.*

### Batch API

For non-real-time workloads, the Batch API offers 50% discount:

**Characteristics:**
- 50% off standard pricing (both input and output)
- Results returned within 24 hours (not real-time)
- Same model quality and capabilities
- Submit up to 100,000 requests per batch

**Best for:**
- Content generation (blog posts, product descriptions)
- Data processing and classification
- Bulk summarization
- Evaluation and testing
- Nightly report generation

**Not suitable for:**
- Real-time user interactions
- Latency-sensitive applications
- Interactive conversations

### Model Routing

Route requests to the appropriate model tier:

| Task | Recommended Model | Rationale |
|---|---|---|
| Classification/labeling | Haiku 3.5 | Simple task, high volume, fast |
| Entity extraction | Haiku 3.5 | Structured extraction, doesn't need reasoning |
| Summarization | Sonnet 4 | Balance of quality and cost |
| Code generation | Sonnet 4 | Good code quality at moderate cost |
| Complex analysis | Opus 4 | Worth the premium for depth |
| Creative writing | Sonnet 4 or Opus 4 | Depends on quality requirements |
| Multi-step reasoning | Opus 4 with thinking | Extended thinking justified for complexity |

**Routing implementation:**
1. Define task categories in your application
2. Map each category to a model
3. Route at the application layer
4. Monitor quality per tier — adjust if quality drops

### Token Optimization

| Technique | Savings | Implementation |
|---|---|---|
| Shorter system prompts | 10-30% input | Audit and trim verbose instructions |
| Structured output (JSON) | 10-20% output | Reduces verbose natural language |
| Context pruning | 20-50% input | Only send relevant context per request |
| Response length limits | 10-40% output | `max_tokens` parameter |
| Few-shot reduction | 10-30% input | Minimum examples needed for quality |

### Rate Limits and Throughput

| Tier | Rate Limits | Consideration |
|---|---|---|
| Free | Very limited | Testing only |
| Build | Moderate | Development, small production |
| Scale | High | Production workloads |
| Custom | Negotiated | Enterprise agreements |

**Cost planning:** Higher tiers don't cost more per token — they allow more throughput.
But higher throughput = higher potential spend. Set budget alerts.

## Cost Attribution

### Tracking Dimensions

Tag every API call with:
- `feature` — Which product feature triggered this call
- `user_tier` — Free, premium, enterprise
- `task_type` — Classification, generation, analysis, etc.
- `model` — Which Claude model was used
- `status` — Success, retry, failure

### Key Metrics

| Metric | Formula | Target |
|---|---|---|
| Cost per successful response | Total cost / successful responses | Trending down |
| Token efficiency | Output tokens / input tokens | Depends on use case |
| Cache hit rate | Cached requests / total requests | >50% where applicable |
| Retry rate | Retried requests / total requests | <5% |
| Model tier distribution | % requests per model | Aligned to task complexity |

## Integration Patterns

### Direct API vs. AWS Bedrock vs. Other

| Access Method | Pros | Cons |
|---|---|---|
| **Anthropic API direct** | Latest models, full features, Batch API | Separate billing, no cloud integration |
| **AWS Bedrock** | AWS billing consolidation, IAM, VPC | May lag on new features, see `ai-bedrock.md` |
| **Google Vertex AI** | GCP billing consolidation | Limited model selection, see `ai-vertex.md` |

**Cost consideration:** Direct API may offer better pricing for high-volume usage via
enterprise agreements. Cloud provider access consolidates billing but may add markup.

## Assessment Questions

1. Which Claude models are in use? Is model selection intentional or default?
2. Is prompt caching enabled for repeated context?
3. Are batch-eligible workloads using the Batch API?
4. Is extended thinking used? Is it justified for each use case?
5. What's the average input/output token ratio per request?
6. Are costs tracked by feature and user tier?
7. What's the retry rate? (Retries = wasted tokens)
8. Is there a model routing strategy or does everything go to one model?