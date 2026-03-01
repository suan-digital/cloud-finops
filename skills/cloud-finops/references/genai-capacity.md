# GenAI Capacity Planning

**Skip this reference if the organization doesn't use GPU/TPU compute or provisioned AI
inference throughput.**

GenAI capacity planning differs fundamentally from traditional compute capacity planning.
GPU/TPU resources are expensive, scarce, and have unique pricing models. Getting capacity
strategy wrong means either overpaying for idle GPUs or failing to serve production traffic.

## Provisioned vs. On-Demand vs. Spot

### Capacity Models

| Model | Characteristics | Best For | Risk |
|---|---|---|---|
| **On-demand** | Pay per second/minute/token, no commitment | Variable workloads, experimentation | Highest unit cost, possible capacity unavailability |
| **Provisioned throughput** | Reserved capacity, guaranteed availability | Steady production inference | Pay for unused capacity if traffic drops |
| **Spot/preemptible** | Deeply discounted, can be interrupted | Training, batch inference, non-critical | Interruption risk, not for latency-sensitive |
| **Reserved instances** | 1-3 year commitment, significant discount | Known steady-state GPU needs | Long commitment, inflexible |
| **Savings Plans** | Flexible commitment, moderate discount | Mixed GPU workloads | Less discount than reserved |

### Decision Framework

```
Is the workload latency-sensitive?
├── Yes: Is traffic predictable?
│   ├── Yes (steady): Provisioned throughput or reserved
│   └── No (bursty): On-demand with auto-scaling + provisioned base
└── No: Can it tolerate interruption?
    ├── Yes: Spot/preemptible instances
    └── No: On-demand for flexibility
```

## The Spillover Problem

Provisioned throughput has a capacity ceiling. When traffic exceeds provisioned capacity, excess
requests "spill over" to on-demand pricing.

### Spillover Economics

| Scenario | Provisioned Cost | Spillover Cost | Total | Effective Unit Cost |
|---|---|---|---|---|
| 80% provisioned utilization | $10,000 | $0 | $10,000 | Low |
| 100% provisioned + 20% spillover | $10,000 | $4,000 | $14,000 | Medium |
| 100% provisioned + 50% spillover | $10,000 | $10,000 | $20,000 | High (wasted commitment) |

**The trap:** Organizations provision for average demand, then pay premium on-demand rates for
peaks. If peaks are frequent, the blended cost can exceed pure on-demand pricing.

### Managing Spillover

**Monitor:**
- Provisioned throughput utilization rate (target: 70-85%)
- Spillover frequency and volume
- Spillover cost as percentage of total AI compute cost
- Peak-to-average traffic ratio

**Strategies:**
1. **Right-size provisioned capacity** — Set to the 70th-80th percentile of demand, not average
2. **Implement request queuing** — Buffer requests during peaks instead of immediate spillover
3. **Traffic shaping** — Spread batch requests across time to smooth demand
4. **Model routing under pressure** — Route to smaller models during capacity pressure
5. **Regional distribution** — Spread load across regions with separate capacity pools

## GPU/TPU Capacity Sizing

### GPU Instance Economics

| Instance Type (AWS examples) | GPU | GPU Memory | On-Demand $/hr | Use Case |
|---|---|---|---|---|
| g5.xlarge | A10G | 24 GB | ~$1.00 | Small model inference, fine-tuning |
| g5.12xlarge | 4x A10G | 96 GB | ~$5.70 | Medium model inference |
| p4d.24xlarge | 8x A100 | 320 GB | ~$32.80 | Large model training/inference |
| p5.48xlarge | 8x H100 | 640 GB | ~$98.00 | Frontier model training |

*Prices are approximate and vary by region. Check current provider pricing.*

### Sizing Considerations

**For inference:**
- Model size determines minimum GPU memory requirement
- Quantized models (INT4/INT8) reduce memory requirement by 2-4x
- Batch size affects throughput — larger batches improve GPU utilization
- Latency requirements constrain batch size

**For training/fine-tuning:**
- Model size + optimizer states + gradients determine memory
- Multi-GPU training adds communication overhead (10-30%)
- Spot instances can reduce training cost by 60-90% with checkpointing
- Training is typically bursty — avoid reserved instances for training only

### Utilization Targets

| Workload Type | Target GPU Utilization | Below Target = | Above Target = |
|---|---|---|---|
| Steady inference | 70-85% | Over-provisioned, right-size down | Risk spillover or latency |
| Bursty inference | 50-70% average | Acceptable if peaks are served | Consider auto-scaling |
| Training | 85-95% | Under-utilizing expensive hardware | Good |
| Fine-tuning | 70-90% | Consider smaller instances | Good |

## Auto-Scaling for AI Workloads

### Challenges

Traditional auto-scaling metrics (CPU, memory) don't work well for GPU workloads:
- GPU utilization can spike from 0 to 100% in seconds
- GPU instances take minutes to start (vs. seconds for CPU)
- Model loading adds 30-120 seconds to instance readiness
- Cold start costs are significant for large models

### Strategies

**Warm pool scaling:**
Keep a pool of instances with models pre-loaded but idle. Scale from warm pool instead of
launching new instances. Trade idle cost for fast scaling.

**Predictive scaling:**
Use historical traffic patterns to pre-scale before demand arrives. Works well for workloads
with predictable daily/weekly patterns.

**Queue-based scaling:**
Scale based on request queue depth rather than GPU utilization. Provides better signal for
bursty workloads.

**Model cascade under pressure:**
When capacity is constrained, automatically route to smaller/faster models rather than queuing
or failing. Graceful degradation > hard failures.

## Multi-Model Capacity Planning

Organizations running multiple models face allocation challenges:

### Shared vs. Dedicated Infrastructure

| Approach | Pros | Cons |
|---|---|---|
| **Dedicated instances per model** | Simple, predictable, isolated | Poor utilization if demand varies |
| **Shared GPU cluster** | Better utilization, flexible | Complex orchestration, noisy neighbor |
| **Serverless inference** | No capacity management | Higher unit cost, cold starts |

### Consolidation Opportunities

- Multiple small models can share a single GPU (multi-model serving)
- Batch inference for different models can time-share the same hardware
- Similar model families can share infrastructure with model swapping

## Cost Optimization Patterns

### Pattern 1: Time-Shift Batch Inference

Move non-real-time inference to off-peak hours when spot/preemptible pricing is lowest.
Applicable to: content generation, document processing, data enrichment, model evaluation.

### Pattern 2: Region-Shift for Training

GPU pricing varies by region. Training workloads that don't need to be co-located with data
can run in the cheapest region. Note: data transfer costs may offset region savings.

### Pattern 3: Scheduled Capacity

If inference demand follows a predictable pattern (business hours, weekday peaks), schedule
provisioned capacity to match. Scale down during off-hours.

### Pattern 4: Commitment Layering

| Layer | Coverage | Instrument |
|---|---|---|
| Base load (always-on) | 40-60% of peak | Reserved instances or 1-year commitment |
| Steady demand | 60-80% of peak | Savings Plans or shorter commitment |
| Peak demand | 80-100% of peak | On-demand |
| Burst (>100%) | Overflow | Spot instances or spillover |

### Pattern 5: Model Efficiency First

Before adding capacity, optimize what you have:
- Quantize models (4-bit can reduce GPU memory 4x)
- Optimize batch sizes for throughput
- Implement prompt caching to reduce inference calls
- Route simple queries to smaller models
- Evaluate if a smaller fine-tuned model outperforms a larger general model

## Assessment Questions

1. What GPU/TPU instances are provisioned? What's the monthly cost?
2. What's the average GPU utilization across the fleet?
3. Is there provisioned throughput? What's the utilization rate?
4. How much spillover to on-demand occurs? What does it cost?
5. Are training workloads using spot instances?
6. What's the peak-to-average demand ratio?
7. Is auto-scaling configured for AI workloads? Based on what metrics?
8. Are models quantized where applicable?
9. Is there a warm pool for fast scaling?
10. Can batch inference be time-shifted to cheaper hours?