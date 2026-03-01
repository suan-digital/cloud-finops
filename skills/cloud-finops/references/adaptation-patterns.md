# Adaptation Patterns

Adapt the depth, focus, and language of your analysis based on the organization's spend tier
and AI maturity. These patterns ensure recommendations are realistic and actionable for each
context.

## By Spend Tier

### Startup ($5K-$50K/month)

**Shuhari stage:** Likely early Shu. Building foundations.

**Focus on:**
- Cost visibility across all accounts (often just 1-2)
- Tagging foundations — start with 4-5 mandatory tags
- Right-sizing obvious over-provisioning
- Dev environment scheduling (biggest quick win per effort)
- Single commitment strategy (1-year Savings Plans for predictable base)

**Skip or minimize:**
- Complex chargeback models (1-2 teams don't need formal chargeback)
- Multi-cloud governance (usually single provider)
- Elaborate reporting — a weekly Slack summary beats a dashboard nobody checks
- Advanced commitment strategies — simple Savings Plans beat complex RI portfolios

**Communication style:**
- Direct, actionable, low-ceremony
- Emphasize quick wins — every dollar counts at this scale
- Frame FinOps as engineering hygiene, not a discipline
- Avoid enterprise jargon (chargeback, showback, unit economics)
- Focus: "Here's what to turn off, resize, and schedule"

**Realistic savings:** 15-30% of total spend ($750-$15K/month)

### Mid-Market ($50K-$500K/month)

**Shuhari stage:** Likely Shu transitioning to Ha. Foundations exist, automation emerging.

**Focus on:**
- Commitment strategy optimization (RIs, Savings Plans, CUDs)
- Architecture-cost alignment — PR-time cost visibility
- Team accountability through showback reports
- Unit economics for primary products/features
- CI/CD cost integration (Infracost or equivalent)
- Container optimization (if Kubernetes is in use)

**Expand:**
- Chargeback models that create real accountability
- Multi-account structure for cost isolation
- Data transfer cost analysis (often a surprise at this scale)
- Commitment portfolio management

**Communication style:**
- Structured, with executive summary + detail
- Connect costs to business metrics (cost per customer, per feature)
- Involve both engineering leads and finance
- Frame FinOps as competitive advantage, not just cost reduction

**Realistic savings:** 20-35% of total spend ($10K-$175K/month)

### Enterprise ($500K+/month)

**Shuhari stage:** Varies by domain — some capabilities may be Ha while others remain Shu.

**Focus on:**
- Governance at scale (policies, guardrails, automation)
- Multi-cloud optimization and normalization (FOCUS spec)
- AI cost management (usually significant at this scale)
- Sustainability reporting and carbon metrics
- FinOps team maturity and operating model
- Platform engineering cost integration
- Enterprise Discount Programs (EDPs) and custom pricing

**Emphasize:**
- Organizational change — tooling alone doesn't reduce enterprise waste
- FinOps team structure and reporting lines
- Executive sponsorship and board-level reporting
- Cross-functional collaboration between finance, engineering, and product
- Maturity assessment by capability domain (not one-size-fits-all)

**Communication style:**
- Executive-ready with layered detail (summary → findings → deep dive)
- Business value language (TCO, ROI, unit economics)
- Risk-aware framing (compliance, security, sustainability)
- Include organizational change recommendations alongside technical ones

**Realistic savings:** 15-30% of total spend ($75K-$500K+/month)

## By AI Maturity

### No AI Workloads

- **Skip entirely:** Dimensions 5 (AI Cost Visibility) and 6 (Inference Economics)
- **Skip references:** All `ai-*.md` files, `genai-capacity.md`, `ai-value-governance.md`
- **Focus:** Cloud infrastructure optimization, traditional FinOps disciplines
- **Note:** If the organization is planning AI adoption, provide a brief forward-looking note
  about AI cost structures to set expectations

### AI in Experimentation

Organizations with AI proof-of-concepts, pilots, or early experiments.

- **Light touch:** Dimension 5 (hidden costs awareness) — surface the 4-5x multiplier early
- **Skip:** Dimension 6 (inference economics is premature before production scale)
- **Key message:** "Measure before you scale. Six months of pilot data reveals true cost drivers."
- **Warn:** About cost surprises before scaling — the jump from pilot to production is where
  budgets break
- **Reference:** `ai-cost-visibility.md` only — enough to set expectations without overwhelming

### AI in Production

Organizations running LLMs or ML models in production with measurable inference spend.

- **Full analysis:** Dimensions 5 and 6
- **Focus areas:**
  - Hidden cost assessment (is total AI cost tracked or just API charges?)
  - Model routing opportunities (are all queries hitting the same model?)
  - Prompt optimization potential
  - Cost attribution by AI feature/workflow
  - Caching strategy for repetitive queries
- **References:** `ai-cost-visibility.md`, `inference-economics.md`, relevant AI provider file
- **Key metrics to introduce:** Cost per inference, token consumption per workflow, cost per
  AI-generated output

### Heavy AI / Agentic Workflows

Organizations with multiple AI-powered features, agentic architectures, or AI as a core
product capability.

- **Deep dive:** Dimensions 5 and 6, plus capacity planning and governance
- **Focus areas:**
  - Agentic multiplier analysis (5-25x cost vs. standard LLM calls)
  - Agent-to-agent communication cost modeling
  - Token-level optimization strategy
  - Multi-model routing architecture
  - Provisioned throughput vs. on-demand decisions
  - AI value governance (stage gates, kill criteria for AI features)
  - GPU/TPU capacity planning
- **References:** `ai-cost-visibility.md`, `inference-economics.md`, `genai-capacity.md`,
  `ai-value-governance.md`, relevant AI provider files
- **Key risk:** Many agentic AI projects get canceled due to cost and complexity — help the
  organization avoid this

## By Engagement Type

### Quick Assessment (30-minute conversation)

- Abbreviated intake (skip organizational context, focus on environment + pain points)
- Focus on Dimensions 1, 3, 4 only
- Output: Executive summary + quick wins (Sections 1 and 5 only)
- Skip: Full roadmap, detailed findings tables

### Standard Assessment (full analysis)

- Complete intake protocol
- All 8 dimensions (skip AI if not applicable)
- Full 9-section report
- Include 90-day roadmap

### Deep Dive (specific topic)

- Targeted intake for the specific area
- Apply relevant dimensions only
- Output: Focused analysis with detailed recommendations
- Include implementation-level guidance (code examples, CLI commands, terraform changes)

## Combining Patterns

The spend tier and AI maturity patterns combine. For example:

- **Enterprise + Heavy AI:** Full depth on all dimensions, emphasis on governance and
  organizational change, AI-specific KPIs and capacity planning
- **Startup + AI in Experimentation:** Light intake, focus on visibility and quick wins,
  brief AI cost warning, skip governance complexity
- **Mid-Market + AI in Production:** Standard depth, emphasis on model routing and cost
  attribution, commitment strategy that accounts for AI spend variability