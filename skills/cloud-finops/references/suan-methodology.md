# Suan Digital Advisory Methodology

The Suan Digital FinOps methodology is built on five principles drawn from real-world advisory
engagements. These principles shape how you frame findings, prioritize recommendations, and
communicate with stakeholders.

## The Five Principles

### 1. Cost Is Architecture

**80% of cloud costs are locked in at design time, not deployment time.**

If cost isn't a first-class design constraint alongside security and reliability, optimization is
retrofitting. The engineer who chooses a synchronous API pattern over an async queue on Tuesday
afternoon determines the cost structure for months. Finance discovers the impact at the quarterly
review. By then, refactoring requires a sprint nobody budgeted.

This means:
- Architecture reviews must include cost impact analysis
- Cost visibility must exist at PR time, not just in monthly reports
- Unit economics (cost per request, per user, per transaction) are architectural metrics
- Engineers own cost optimization — they have the context and the levers
- Cost anomalies should be investigated like production incidents

**Don't optimize outputs. Shape inputs.** The most impactful FinOps work happens in design
documents and pull requests, long before any infrastructure exists to optimize.

### 2. Maturity Is a Journey

**Each stage of FinOps maturity must be fully experienced before advancing.**

The industry's Crawl-Walk-Run model creates a dangerous misconception: that maturity is a race.
Organizations hear "Run" and rush through fundamentals. They implement advanced automation before
understanding what they're automating.

The Shuhari (守破離) framework corrects this:
- **Shu (守)**: Follow the rules. Build visibility. Develop intuition through repetition.
- **Ha (破)**: Question the rules. Adapt practices to your context. Develop judgment.
- **Ri (離)**: Transcend the framework. Cost efficiency is how you build, not what you optimize.

Most organizations are in Shu whether they realize it or not. Not every capability needs to
reach Ri — some should appropriately stay at Ha.

**Do not rush organizations through stages. Do not shame them for their current state. Meet them
where they are.**

### 3. Diagnose Before Prescribing

**Context determines which optimization levers matter most.**

A $30K/month startup and a $3M/month enterprise have different problems even when symptoms look
similar. "Our cloud bill is too high" could mean:
- No visibility (need tagging and attribution)
- No governance (need policies and automation)
- No architecture-cost alignment (need design-time cost awareness)
- No commitment strategy (need Reserved Instance / Savings Plan optimization)
- AI costs exploding (need inference economics and model routing)

The intake protocol exists because premature recommendations waste credibility and time. Ask
first. Understand the environment, architecture, organizational context, and current practices.
Then — and only then — apply the analysis dimensions.

**Never generate a report without sufficient context. Ask follow-up questions rather than
guessing.**

### 4. Quick Wins Build Trust

**Deliver visible savings in 30 days to earn permission for structural changes.**

Organizations don't adopt FinOps practices because a consultant recommends them. They adopt
them because early wins demonstrate the value of the approach.

The trust sequence:
1. **Week 1-2**: Identify and quantify quick wins (zombie resources, dev scheduling, right-sizing)
2. **Week 2-4**: Execute quick wins, report actual savings
3. **Month 2-3**: Propose structural improvements backed by demonstrated credibility
4. **Month 3+**: Implement governance and automation with organizational buy-in

Quick wins are not just about money. They're about building organizational muscle memory — the
experience of identifying waste, acting on it, and seeing results. This experience is what
transforms FinOps from a mandate into a practice.

**Prioritize by savings-to-effort ratio.** A $500/month fix that takes 10 minutes earns more
credibility than a $5,000/month fix that takes two weeks.

### 5. Every Optimization Has a Carbon Dividend

**Cloud waste and carbon emissions share a common source.**

Every idle server burns carbon alongside budget. Every oversized instance draws power for capacity
it never uses. Every forgotten dev environment runs 24/7 for an 8-hour workday.

This means every cost optimization also reduces environmental impact:
- Right-sizing compute reduces both cost and energy consumption by 20-40%
- Scheduling dev environments saves 60-70% of costs and eliminates idle power draw
- Migrating to current-generation instances delivers 15-40% better performance per watt
- Moving cold data to archive storage reduces both cost and storage energy requirements

Cloud waste and carbon emissions share a common source — every idle server burns both budget
and energy.

**GreenOps is not a separate discipline. It's the environmental return on the same optimizations
you're already recommending for financial reasons.**

## Applying the Methodology

When conducting a FinOps engagement:

1. **Open with intake** — never assume you know the problem
2. **Assess maturity honestly** — position determines appropriate recommendations
3. **Frame findings architecturally** — connect costs to design decisions, not just resource usage
4. **Lead with quick wins** — build the credibility needed for structural change
5. **Include carbon context** — even when not requested, note the environmental co-benefit

The methodology adapts by spend tier and AI maturity. See `adaptation-patterns.md` for specific
guidance on adjusting depth, focus, and language for different organizational profiles.

## Organizational Change Patterns

FinOps recommendations fail not because they're technically wrong, but because they require
behavioral change that wasn't planned for. The best optimization playbook is worthless if the
organization can't or won't execute it.

### Common Resistance Patterns

| Resistance | Root Cause | Response |
|---|---|---|
| "We don't have time for cost optimization" | Optimization seen as extra work | Frame as engineering quality, not overhead — waste reduction simplifies systems |
| "That's finance's responsibility" | No engineering ownership | Start with showback, not chargeback. Make costs visible without blame |
| "Our architecture can't change" | Fear of refactoring risk | Lead with quick wins that don't require architecture changes. Build trust first |
| "We already tried that" | Previous effort failed or regressed | Understand what failed — usually governance, not the optimization itself |
| "The savings aren't worth the effort" | No clear ROI framing | Quantify savings vs. engineering cost. Use the 3x payback rule from `architecture-cost.md` |

### Building Buy-In

1. **Start with engineers who care.** Every organization has 1-2 cost-curious engineers. Find
   them, empower them, and make them visible. Grassroots adoption outperforms mandates.
2. **Make cost visible, not punitive.** Showback before chargeback. Always. Teams that see their
   costs develop intuition. Teams that get billed for their costs develop resentment.
3. **Celebrate wins publicly.** "Team X saved $12K/month by right-sizing their dev clusters"
   builds momentum. Recognition drives repetition.
4. **Connect to engineering values.** Waste reduction = cleaner systems = less operational burden
   = fewer pages. Frame optimization as engineering excellence, not cost cutting.
5. **Respect the change curve.** Awareness → understanding → acceptance → commitment. You can't
   skip steps. An organization that hasn't internalized why FinOps matters won't sustain
   practices that require daily effort.