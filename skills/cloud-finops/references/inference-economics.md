# Inference Economics — The 5-Lever Playbook

**Skip this reference if the organization doesn't use LLMs or generative AI in production.**

The majority of AI spend goes to inference — running models in production — not training.

## Token Economics Fundamentals

Understanding token pricing is now a financial skill, not just a technical one.

### Token Basics

- 1 token ≈ 0.75 words in English
- You pay for both input and output tokens
- Input tokens (prompt/context) and output tokens (response) often have different prices
- System prompts count as input tokens on every request

### Non-Linear Cost Scaling

**Context window costs:**
Sending 100,000 tokens of context doesn't cost 100x what 1,000 tokens costs — it costs
significantly more due to memory and compute requirements. Long-context applications (document
analysis, code review) burn through budgets faster than simple Q&A.

**Model size costs:**
A 70B parameter model doesn't cost 10x what a 7B model costs — the relationship is steeper.
And larger models don't always perform better for specific tasks.

### Pricing Tiers

Model tiers span orders of magnitude in cost. Representative API pricing as of early 2026:

| Tier | Example Models | Input $/1M tokens | Output $/1M tokens | Best For |
|---|---|---|---|---|
| Budget | GPT-4o Mini, Gemini 2.0 Flash | $0.10–0.15 | $0.40–0.60 | Classification, formatting, extraction |
| Mid-range | Claude Haiku 4.5, Gemini 2.5 Pro, GPT-4o | $1.00–2.50 | $5.00–10.00 | Summarization, Q&A, analysis |
| Frontier | Claude Sonnet 4.5, Claude Opus 4.6 | $3.00–15.00 | $15.00–75.00 | Complex reasoning, novel generation |
| Reasoning | OpenAI o3 | $10.00 | $40.00 | Multi-step math, code, research |

*Prices shift frequently — verify against provider pricing pages before financial modeling.
The structural pattern is durable: budget-to-frontier spans 100–150x on output tokens.*
Routing intelligently captures most of that spread.

**Reasoning token trap:** Reasoning models (OpenAI o-series, Claude extended thinking) consume
internal "thinking" tokens billed as output tokens but invisible in API responses. A request
producing 500 visible output tokens may consume 2,000–5,000+ total tokens. Factor 3–10x token
overhead when budgeting reasoning model workloads.

## The Agentic Multiplier

If you think inference costs are high now, agentic AI scales them dramatically.

**Standard LLM call:** One prompt → one response. Predictable cost.

**Agentic AI:** The agent reasons in loops. Calls tools. Evaluates results. Revises. Calls
more tools. Each step consumes tokens.

| Interaction Type | Typical Token Consumption | Cost Multiplier |
|---|---|---|
| Simple prompt-response | 500-2,000 tokens | 1x (baseline) |
| Multi-turn conversation | 2,000-10,000 tokens | 2-5x |
| Agentic task (single agent) | 5,000-50,000 tokens | 5-25x |
| Multi-agent collaboration | 20,000-200,000 tokens | 25-100x |

**The compounding factor:** Agent-to-agent communication. Agents delegate to other agents, pass
context, receive results, synthesize. Every handoff flows tokens between models.

The unit economics that worked for chatbots collapse when agents talk to each other.

**What to audit:** If deploying agentic AI, audit what agents say to each other. Internal
agent communication is often where budgets explode.

## The 5-Lever Playbook

Token optimization alone delivers 20-40% cost reduction. Combined with these levers, savings
compound.

### Lever 1: Model Routing

**Principle:** Not every query needs your most powerful model. Route by task complexity.

| Task Complexity | Route To | Examples |
|---|---|---|
| Simple | Small/fast model | Classification, entity extraction, formatting, validation |
| Standard | Mid-tier model | Summarization, standard Q&A, translation, content generation |
| Complex | Frontier model | Multi-step reasoning, creative generation, nuanced analysis |
| Reasoning-heavy | Reasoning model | Mathematical proofs, complex code generation, research |

**Implementation approaches:**
- **Keyword/regex routing:** Simple rules based on query characteristics
- **Classifier routing:** Small model classifies query complexity, routes to appropriate model
- **Cascade routing:** Start with small model, escalate if confidence is low
- **User-tier routing:** Premium users get frontier models, free tier gets small models

**Impact:** Route intelligently and capture 10-50x cost spread between model tiers.

### Lever 2: Prompt Optimization

**Principle:** Efficient prompts cost less. Better prompts reduce retries.

**Optimization techniques:**
- **Shorter system prompts:** Strip unnecessary instructions. Every token counts at scale.
- **Structured output formats:** JSON mode or structured outputs reduce parsing failures
  and retries.
- **Few-shot reduction:** Find the minimum examples needed. 2 examples often work as well as 5.
- **Context pruning:** Send only relevant context, not everything available.
- **Prompt caching:** Cache system prompts and common prefixes (provider-specific feature).

**Impact:** Better-structured prompts reduce both token consumption and retry rates,
compounding the savings.

### Lever 3: Semantic Caching

**Principle:** Many AI queries are repetitive. Identify similar queries and serve cached
responses.

**How it works:**
1. New query arrives
2. Compute embedding of the query
3. Search cache for similar embeddings (cosine similarity threshold)
4. If match found → serve cached response (free)
5. If no match → call model, cache result

**Effectiveness by use case:**

| Use Case | Cache Hit Rate | Cost Reduction |
|---|---|---|
| Customer support FAQ | 40-60% | 40-60% |
| Document summarization (same docs) | 50-70% | 50-70% |
| Code explanation (common patterns) | 20-40% | 20-40% |
| Creative generation | 5-10% | 5-10% |
| Novel reasoning tasks | <5% | Minimal |

**Implementation considerations:**
- Similarity threshold tuning — too aggressive caching serves wrong answers
- Cache invalidation — underlying data changes must invalidate related cache entries
- Cache storage costs vs. inference savings — break-even analysis needed
- Latency benefit — cached responses are near-instant

### Lever 4: Cost Attribution

**Principle:** You can't manage what you can't measure. Track AI costs granularly.

**Attribution dimensions:**

| Dimension | What It Reveals | Action |
|---|---|---|
| By feature/workflow | Which features consume most AI budget | Optimize or rethink high-cost features |
| By customer segment | Cost to serve different customer tiers | Inform pricing, tier model selection |
| By model/provider | Spending distribution across models | Negotiate volume, identify consolidation |
| By success/retry/failure | Waste from failed attempts | Fix failure patterns, reduce retries |
| By token type (input/output) | Whether prompts or responses drive cost | Optimize the dominant cost driver |

**The key insight:** When you discover one feature consumes 60% of AI budget while generating
10% of AI value, you have an optimization target.

**Implementation:**
- Tag every inference call with feature, user_tier, model, and outcome
- Build dashboards showing cost per feature per day
- Alert on anomalous token consumption
- Track cost-per-successful-outcome (not just cost-per-call)

### Lever 5: Quantization & Model Efficiency

**Principle:** Run models at reduced precision for massive savings with minimal quality loss.

**Quantization levels:**

| Precision | Memory Reduction | Speed Improvement | Quality Impact |
|---|---|---|---|
| FP16 (baseline) | 1x | 1x | None (reference) |
| INT8 | ~2x | 1.5-2x | Minimal for most tasks |
| INT4 | ~4x | 2-3x | Acceptable for many tasks |
| GPTQ/AWQ 4-bit | ~4x | 2-3x | Optimized, near-baseline quality |

**NVIDIA research** shows 4-bit quantized models match FP16 performance on standard benchmarks
while running on a fraction of the hardware.

**When to use:**
- Self-hosted models (not applicable to API-based models)
- Latency-sensitive applications (faster inference)
- Cost-sensitive batch processing
- Edge deployment with limited hardware

**When NOT to use:**
- Tasks requiring maximum precision (medical, legal, financial advice)
- When quality degradation is measurable in your specific use case
- API-based models (quantization happens provider-side)

## Implementation Patterns

### Model Router Architecture

A practical model routing system has four components:

1. **Request classifier** — lightweight model or rules engine classifies incoming query complexity
2. **Route table** — maps complexity + feature to model tier
3. **Fallback chain** — if small model confidence < threshold, escalate to larger model
4. **Cost tracker** — log model used, tokens consumed, latency, outcome per request

**Route table example:**

| Feature | Simple Route | Complex Route | Escalation Trigger |
|---|---|---|---|
| FAQ/Support | Haiku-class | Sonnet-class | Confidence < 0.8 |
| Code review | Sonnet-class | Opus-class | File count > 10 |
| Summarization | Haiku-class | Sonnet-class | Document > 50K tokens |
| Classification | Haiku-class | Haiku-class | N/A (always simple) |

**Start simple.** Keyword/regex routing captures 60-70% of the value of ML-based routing at
a fraction of the implementation cost. Graduate to classifier routing when you have enough
traffic data to train on.

### Caching Architecture

Three layers, each catching different patterns:

**Layer 1: Exact match cache** (Redis/Memcached)
- Hash the prompt → check cache → return if hit
- TTL: 1-24 hours depending on data freshness needs
- Best for: repeated identical queries (support, FAQ, status checks)
- Implementation: straightforward key-value lookup, lowest engineering effort

**Layer 2: Semantic cache** (vector DB)
- Embed the prompt → similarity search → return if cosine similarity > threshold
- Threshold: 0.95+ for factual queries, 0.90 for creative tasks
- Best for: paraphrased versions of the same question
- Implementation: requires embedding model + vector store (Pinecone, Weaviate, pgvector)

**Layer 3: Prompt prefix cache** (provider-native)
- Cache system prompts and common context prefixes at the provider level
- Anthropic: automatic prompt caching for repeated prefixes
- Best for: reducing cost of large system prompts across requests
- Implementation: zero engineering effort — happens automatically with supported providers

**Layer priority:** Implement Layer 1 first (hours of work, immediate savings). Layer 3 is often
free. Layer 2 only makes sense at scale with significant paraphrased query volume.

## FinOps Foundation AI KPIs

Implement these AI-specific metrics:

| KPI | Formula | Target |
|---|---|---|
| Cost per inference | Total AI cost / inference count | Trending down |
| Training cost efficiency | Model performance delta / training cost | Improving |
| Token consumption per workflow | Tokens used / workflow completion | Stable or decreasing |
| GPU/TPU utilization | Active compute time / total provisioned time | >70% |
| Cost per AI-generated output | Total AI cost / successful outputs | Trending down |
| Retry rate | Failed inferences / total inferences | <5% |
| Cache hit rate | Cached responses / total requests | >30% where applicable |

## Assessment Questions

1. What's the monthly inference spend? (By model, by feature)
2. Are all queries going to the same model, or is there routing?
3. What's the average token consumption per request? (Input vs. output)
4. Is there any caching layer for repetitive queries?
5. Are costs attributed by feature/workflow or just aggregated?
6. What's the retry/failure rate for AI calls?
7. Are agentic workflows in use? What's their token consumption profile?
8. Are system prompts cached or sent fresh on every call?
9. Is there a model selection framework, or does the team default to "use the best model"?
10. What's the cost-per-successful-outcome (not just cost-per-call)?