# AWS Bedrock Cost Optimization Reference

Amazon Bedrock-specific pricing, provisioned throughput management, and optimization patterns.

## Bedrock Pricing Models

### On-Demand

Pay per input/output token with no commitment.

**Pricing varies by model:**
| Model Family | Input (per 1M tokens) | Output (per 1M tokens) |
|---|---|---|
| Claude Sonnet 4 | $3.00 | $15.00 |
| Claude Haiku 3.5 | $0.80 | $4.00 |
| Amazon Nova Pro | ~$0.80 | ~$3.20 |
| Amazon Nova Lite | ~$0.06 | ~$0.24 |
| Amazon Nova Micro | ~$0.035 | ~$0.14 |
| Llama 3.x (various) | Varies by size | Varies by size |
| Mistral models | Varies by size | Varies by size |

*Check AWS Bedrock pricing page for current rates.*

### Provisioned Throughput

Reserve model capacity for guaranteed performance and potentially lower unit cost.

**How it works:**
- Purchase Model Units (MUs) for specific models
- 1 MU = a guaranteed inference capacity block
- 1-month or 6-month terms
- No per-token charges for provisioned capacity — unlimited tokens within MU throughput

**When to use provisioned throughput:**
- Predictable, steady inference volume
- Latency-sensitive applications requiring guaranteed performance
- High-volume workloads where per-token costs exceed MU cost
- Compliance requirements for dedicated capacity

**When NOT to use:**
- Variable or unpredictable traffic
- Experimentation or pilot phase
- Low-volume usage (on-demand is cheaper)

### Batch Inference

50% discount for non-real-time workloads:
- Submit batch jobs, results within 24 hours
- Same models and quality as on-demand
- Maximum batch size varies by model

**Best for:** Content generation, data classification, bulk processing, testing.

## Provisioned Throughput Optimization

### Utilization Monitoring

| Metric | Source | What to Watch |
|---|---|---|
| `InvocationCount` | CloudWatch | Requests hitting provisioned capacity |
| `InvocationLatency` | CloudWatch | Response time per request |
| `ThrottledCount` | CloudWatch | Requests exceeding capacity (spillover indicator) |
| Model unit utilization | Bedrock console | % of provisioned capacity used |

### Right-Sizing

| Utilization | Action |
|---|---|
| <40% | Over-provisioned — reduce MUs or switch to on-demand |
| 40-70% | Potentially over-provisioned — analyze traffic patterns |
| 70-85% | Good utilization — monitor for spikes |
| 85-95% | Optimal — watch for throttling |
| >95% | Under-provisioned — increase MUs or accept spillover |

### Spillover Management

When traffic exceeds provisioned capacity, Bedrock can fall back to on-demand:
- Spillover requests billed at on-demand rates
- Track spillover percentage to optimize MU count
- High spillover (>20%) suggests under-provisioned capacity

**Strategy:** Provision for 70th-80th percentile of demand. Accept 10-20% spillover as cheaper
than provisioning for peak.

## Model Selection for Cost

### Bedrock Model Routing

Route by task complexity to optimize cost:

| Task | Recommended Model | Cost/1M Input |
|---|---|---|
| Simple classification | Nova Micro or Nova Lite | $0.035-$0.06 |
| Entity extraction | Nova Lite or Haiku 3.5 | $0.06-$0.80 |
| Summarization | Nova Pro or Sonnet 4 | $0.80-$3.00 |
| Complex reasoning | Claude Sonnet 4 or Opus 4 | $3.00-$15.00 |

**Amazon Nova advantage:** For many enterprise tasks (summarization, classification, Q&A),
Amazon Nova models offer significant cost savings over frontier models with acceptable quality.
Evaluate quality for your specific use case before committing.

### Custom Models

| Approach | Cost Consideration |
|---|---|
| Fine-tuning | Training cost (one-time) + lower inference cost per request |
| Continued pre-training | Higher training cost, potentially better domain performance |
| RAG (no fine-tuning) | No training cost, higher per-request token cost |

**Fine-tuning ROI:** If a fine-tuned smaller model matches a larger model's quality for your
task, the inference savings over thousands of requests far exceed the training cost.

## Bedrock-Specific Features

### Knowledge Bases (RAG)

| Cost Component | Pricing |
|---|---|
| Storage | OpenSearch Serverless collection charges |
| Embedding | Per-token charges for embedding model |
| Retrieval | Per-query charges |
| Inference | Standard model charges for generation |

**Optimization:**
- Right-size chunk size (smaller chunks = more embeddings but better retrieval)
- Use efficient embedding models (Titan Embeddings is cost-effective)
- Cache frequent RAG results to avoid repeated retrievals
- Monitor retrieval quality — poor retrieval causes retries

### Agents

Bedrock Agents incur costs at each step:

| Step | Cost |
|---|---|
| Orchestration | Model inference for reasoning |
| Action execution | Lambda invocation + any downstream costs |
| Knowledge base retrieval | RAG costs per query |
| Response generation | Model inference for final response |

**The agentic multiplier applies here:** A single agent task can invoke 5-25 model calls.
Monitor total token consumption per agent task, not just per API call.

### Guardrails

| Feature | Cost |
|---|---|
| Content filters | Per-text-unit charge |
| Denied topics | Per-text-unit charge |
| PII detection | Per-text-unit charge |

**Note:** Guardrails add cost to every request. Ensure they're providing value. For
low-risk internal applications, lighter guardrails may be appropriate.

## Cost Attribution in Bedrock

### CloudWatch Metrics

Group Bedrock costs by:
- Model ID (which models cost most)
- Provisioned model ID (MU utilization)
- Application tags (via custom metrics)

### CUR Attribution

Bedrock charges appear in CUR under:
- Service: `Amazon Bedrock`
- Usage types include model identifier
- Tag resources using Bedrock model tags

### Custom Tracking

For feature-level attribution:
- Pass custom headers or metadata with each API call
- Log request metadata (model, feature, user_tier, tokens) to CloudWatch or S3
- Build dashboards showing cost per feature per day

## Integration with AWS FinOps

Bedrock costs integrate with the broader AWS cost management stack:

| Tool | Bedrock Capability |
|---|---|
| Cost Explorer | Bedrock service-level costs |
| CUR | Detailed model-level billing |
| Budgets | Bedrock-specific budget alerts |
| Trusted Advisor | Provisioned throughput utilization |
| AWS MCP Server | Conversational cost queries including Bedrock |

## Assessment Questions

1. Which Bedrock models are in use? Is selection optimized by task?
2. Is provisioned throughput in place? What's the utilization rate?
3. Is spillover monitored and managed?
4. Are batch-eligible workloads using Batch Inference?
5. What's the monthly Bedrock spend breakdown by model?
6. Are Bedrock Agents in use? What's the per-task token consumption?
7. Are Knowledge Base costs tracked separately?
8. Is there a model routing strategy or does everything go to one model?