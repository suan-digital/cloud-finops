# Vertex AI Cost Optimization Reference

Google Vertex AI-specific pricing, optimization patterns, and cost management strategies.

## Vertex AI Pricing Components

### Model Garden — API Pricing

Vertex AI provides access to multiple model families:

| Model | Input (per 1M tokens) | Output (per 1M tokens) | Notes |
|---|---|---|---|
| Gemini 2.0 Flash | ~$0.10 | ~$0.40 | Fast, cost-effective |
| Gemini 2.0 Pro | ~$1.25 | ~$5.00 | Balanced performance |
| Gemini 1.5 Pro | ~$1.25 | ~$5.00 | Long context (2M tokens) |
| Claude Sonnet (via Model Garden) | $3.00 | $15.00 | Via Anthropic partnership |
| Llama 3.x (via Model Garden) | Varies | Varies | Open models, Vertex pricing |

*Check Vertex AI pricing page for current rates.*

### Provisioned Throughput

Vertex AI offers provisioned throughput for Gemini models:
- Fixed monthly cost for guaranteed capacity
- No per-token charges within provisioned capacity
- Available for production workloads requiring guaranteed latency

### Compute Pricing (Custom Models)

For self-hosted/fine-tuned models on Vertex AI:

| Resource | Approximate $/hr |
|---|---|
| NVIDIA T4 | ~$0.35 |
| NVIDIA L4 | ~$0.70 |
| NVIDIA A100 (40GB) | ~$3.67 |
| NVIDIA A100 (80GB) | ~$5.00 |
| NVIDIA H100 (80GB) | ~$11.00 |
| TPU v5e | ~$1.20/chip |

*Prices vary by region. Check current Vertex AI pricing.*

## Cost Optimization Strategies

### Gemini Model Routing

| Task | Recommended Model | Cost Tier |
|---|---|---|
| Simple classification | Gemini Flash | Lowest (~$0.10/M input) |
| Entity extraction | Gemini Flash | Lowest |
| Summarization | Gemini Flash or Pro | Low-Medium |
| Complex generation | Gemini Pro | Medium |
| Long context analysis | Gemini 1.5 Pro | Medium (but context cost adds up) |
| Multi-modal (image/video) | Gemini Flash or Pro | Varies by modality |

**Gemini Flash advantage:** At ~$0.10/M input, Gemini Flash is one of the most cost-effective
models available. Route as much traffic as possible to Flash before escalating.

### Context Caching

Vertex AI supports context caching for Gemini models:
- Cache frequently used context (documents, system prompts)
- Cached context costs a fraction of regular input tokens
- Minimum cacheable size: 32,768 tokens
- Cache TTL: configurable, charged for storage time

**Best for:**
- RAG applications with large reference documents
- Agents with extensive system prompts
- Multi-turn conversations with stable context

### Batch Predictions

For non-real-time workloads:
- 50% discount on standard pricing
- Results returned asynchronously
- Available for Gemini models

### Tuning Cost Optimization

| Tuning Method | Cost | Best For |
|---|---|---|
| Prompt tuning | Low — no model training | Simple task adaptation |
| Supervised fine-tuning | Medium — training compute + storage | Domain specialization |
| RLHF | High — training + reward model | Quality-critical applications |
| Distillation | Medium — teacher + student models | Deploying smaller, cheaper models |

**ROI of fine-tuning:** If a fine-tuned Flash model matches Pro quality for your task, you
save ~12x on inference costs for every future request.

## Vertex AI Platform Costs

### Beyond Model Inference

| Component | Cost Driver | Optimization |
|---|---|---|
| **Vertex AI Pipelines** | Per-run compute + orchestration | Minimize pipeline complexity |
| **Feature Store** | Storage + online serving | Right-size feature sets |
| **Vector Search** | Index size + queries | Optimize index dimensions |
| **Endpoints** | Compute time (even when idle) | Auto-scaling, min replicas = 0 |
| **Model Registry** | Storage | Clean up unused model versions |
| **Experiments** | Compute per trial | Limit hyperparameter search space |

### Endpoint Cost Management

Custom model endpoints run on compute you provision:

| Pattern | Savings | Details |
|---|---|---|
| Min replicas = 0 | 100% when idle | Cold start trade-off |
| Auto-scaling | 20-40% | Scale based on traffic |
| Spot/preemptible VMs | 60-91% | For batch/non-critical |
| GPU right-sizing | 20-40% | Match GPU to model requirements |
| Model optimization (quantization) | 30-50% | Smaller GPU requirement |

### Training Cost Management

| Pattern | Savings | Details |
|---|---|---|
| Spot/preemptible VMs | 60-91% | With checkpointing |
| Right-size accelerator | 20-40% | Don't use H100 when A100 suffices |
| Hyperparameter tuning budget | Variable | Set max trials and early stopping |
| Distributed training efficiency | 10-20% | Optimize communication overhead |
| TPU for large training | Variable | Often cheaper than GPU for large models |

## GCP Integration

### Billing Attribution

Vertex AI costs appear in GCP billing under:
- Service: `Vertex AI`
- SKU: Model-specific or compute-specific
- Labels: Apply GCP labels for attribution

### BigQuery Integration

Export Vertex AI metrics to BigQuery for custom analytics:
- Per-request token counts
- Model and endpoint identification
- Latency and throughput metrics
- Cost per request calculation

### Monitoring

| Metric | Where | What to Watch |
|---|---|---|
| Prediction count | Cloud Monitoring | Volume trends |
| Prediction latency | Cloud Monitoring | Performance/cost trade-off |
| GPU utilization | Cloud Monitoring | Endpoint efficiency |
| Token usage | Vertex AI logs | Cost per request |

## Multi-Modal Pricing

Vertex AI supports multi-modal inputs (text, image, video, audio):

| Modality | Pricing Basis | Optimization |
|---|---|---|
| Text | Per token | Standard token optimization |
| Image | Per image (equivalent token count) | Compress, reduce resolution |
| Video | Per second + per frame | Sample frames, reduce duration |
| Audio | Per second | Compress, reduce duration |

**Watch for:** Multi-modal requests can be significantly more expensive than text-only.
Ensure multi-modal input is necessary for each use case.

## Assessment Questions

1. Which Vertex AI models are in use? Is selection optimized for cost?
2. Is Gemini Flash used for simple tasks? (Or everything going to Pro?)
3. Is context caching enabled for repeated context?
4. Are batch predictions used for non-real-time workloads?
5. What's the total Vertex AI platform cost (beyond model inference)?
6. Are custom model endpoints right-sized? Min replicas optimized?
7. Is training using spot/preemptible VMs?
8. Are labels applied for cost attribution?