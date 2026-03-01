# Shuhari (守破離) Maturity Model

The FinOps Foundation's Crawl-Walk-Run model is useful shorthand but creates a dangerous
misconception: that maturity is a race to the finish line. Organizations hear "Run" and rush
through fundamentals, implementing advanced automation before understanding what they're
automating.

Shuhari offers a deeper lens — one where each stage serves a purpose, mastery requires patience,
and "transcendence" means something different from "moving fast."

## The Three Stages

### Shu (守) — Protect / Follow the Rules

**Duration:** 6-12 months typical. Some need longer. That's not failure.

In martial arts, Shu is about repetition until basics become muscle memory. You don't question.
You don't innovate. You copy your teacher's movements exactly until they become yours.

In FinOps, Shu is building the foundation everything else depends on.

#### What Shu Looks Like

- Implement cost visibility across all cloud accounts
- Establish tagging standards and enforce consistently (target: 80%+ coverage)
- Create showback reports so teams see their spend
- Set up anomaly alerts for unexpected cost spikes
- Learn one provider's pricing model deeply before adding complexity
- Develop intuition through observing cost patterns daily/weekly

#### The Shu Mistake

Organizations treat visibility as a checkbox. "We have a dashboard, let's move on."

Shu isn't about having a dashboard. It's about developing intuition. When you've spent months
watching cost patterns, you start recognizing anomalies before alerts fire. You understand which
services drive spend. You know which teams respond to cost data and which ignore it.

This intuition can't be automated. It can't be purchased from a vendor. It comes from
repetition, observation, and patience.

#### Readiness to Leave Shu

All of these must be true:

- [ ] You can explain your cost structure without looking at a dashboard
- [ ] Teams know their spend and can predict it reasonably well
- [ ] Anomalies get investigated, not ignored
- [ ] Tagging coverage exceeds 80%
- [ ] You understand unit economics for primary workloads
- [ ] Cost conversations happen regularly, not just at billing surprises

#### Shu Anti-Patterns

- Buying advanced tooling before understanding what to measure
- Implementing chargeback before teams understand their spend
- Purchasing commitments (RIs/SPs) based on guesswork rather than data
- Benchmarking against organizations at different stages
- Declaring victory because a dashboard exists

### Ha (破) — Break / Question the Rules

**Duration:** 12-24 months typical. Organizations that rush through return to relearn.

In martial arts, Ha is when students start questioning why techniques work. They study other
styles. They experiment. They adapt movements to their own circumstances.

In FinOps, Ha means deliberately breaking rules that served you in Shu, because you now
understand why those rules existed.

#### What Ha Looks Like

- Automate repetitive optimizations
- Build chargeback models that create real accountability
- Experiment with commitment strategies (RIs, Savings Plans, CUDs)
- Integrate cost considerations into CI/CD pipelines
- Learn from other organizations' FinOps practices
- Understand the relationship between utilization, performance, and cost
- Develop judgment about when best practices don't apply

#### The Key Shift

In Shu, you tagged resources because the policy said to. In Ha, you understand that tagging
enables allocation → allocation enables accountability → accountability changes behavior. Now
you make intelligent decisions about when tagging matters and when it doesn't.

In Shu, you right-sized instances because a tool recommended it. In Ha, you understand the
relationship between utilization, performance, and cost, and can have nuanced conversations
with engineering about acceptable trade-offs.

#### The Ha Danger

Many organizations get stuck here. They've broken from rigid rules but replaced them with new
rigid rules from a different source.

They read that Company X achieved 40% savings with a particular approach, so they copy it
exactly. They attend a conference and implement whatever the speaker recommended. They hire a
consultant and follow the playbook without adaptation.

That's not Ha. That's Shu with a different master.

True Ha means developing judgment — understanding principles deeply enough to know when best
practices don't apply to your situation.

#### Readiness to Leave Ha

All of these must be true:

- [ ] You can articulate why practices work for your organization and not others
- [ ] You've tried multiple approaches and understand their trade-offs
- [ ] Your automation reflects your specific needs, not generic recommendations
- [ ] You can predict how changes will affect your cost structure
- [ ] Engineering and finance speak the same language about cloud economics
- [ ] Cost optimization suggestions come from engineering teams, not just FinOps

#### Ha Anti-Patterns

- Copying another organization's FinOps playbook exactly
- Automating without understanding what you're automating
- Treating all workloads the same (one-size-fits-all commitment strategy)
- Over-investing in tooling while under-investing in organizational change
- Confusing tool sophistication with organizational maturity

### Ri (離) — Transcend / Create Your Own Path

**Duration:** Rare. Not the goal for every capability.

In martial arts, Ri is mastery. The practitioner moves in ways their original teachers never
taught, yet every movement reflects deep understanding of fundamentals.

In FinOps, Ri means the framework is no longer needed because the principles are internalized.

#### What Ri Looks Like

- Cost optimization is embedded in how the organization builds, not applied after
- Teams self-govern without central enforcement
- Practices evolve organically based on results
- The distinction between "FinOps" and "how we build things" disappears
- The organization creates approaches others study

#### Ri in Practice

What does Ri actually look like day-to-day?

- **Cost efficiency is embedded in sprint planning, not separate reviews.** Engineers estimate
  cost impact alongside story points. "How much will this cost to run?" is as natural a question
  as "how long will this take to build?"
- **Engineers propose cost-aware architectures without being asked.** The design doc includes
  a cost section not because a template requires it, but because the engineer considers cost
  a design constraint like latency or availability.
- **New services launch with cost dashboards on day one.** Observability includes cost from
  the start — not bolted on after the first billing surprise.
- **The FinOps team role evolves into platform engineering.** The central FinOps function
  dissolves because cost awareness is now a platform capability — built into templates,
  defaults, and guardrails that make the efficient path the easy path.
- **Cost anomalies are investigated like production incidents.** Not because policy demands it,
  but because the team instinctively treats unexpected cost as a signal that something is wrong.

#### The Paradox of Ri

You can't aim for Ri directly. You can't skip Shu and Ha to get there faster. Ri emerges from
fully experiencing the previous stages.

Organizations that claim "Run" maturity often reveal, under scrutiny, that they're performing
Ha activities with Ri vocabulary. Sophisticated tooling but shallow understanding. Automated
processes they don't fully grasp.

True Ri is rare. And that's fine.

#### Ri Indicators

- Cost efficiency is simply part of how the organization operates, like security or reliability
- No one talks about "FinOps maturity" anymore — it's assumed
- Cost-aware decisions happen instinctively at all levels
- The organization generates novel approaches that others adopt
- FinOps practitioners move to other roles because the practice sustains itself

#### Ri Anti-Patterns

Not everything that looks like Ri is Ri. Watch for:

- **Declaring Ri because leadership stopped asking about costs.** They may have given up, not
  transcended. If cost conversations disappeared because nobody cares — that's regression, not
  mastery.
- **Sophisticated automation that nobody understands.** If the team can't explain what their
  cost automation does or why, they've built fragile complexity, not internalized practice.
  Ri means understanding is deep, not that tooling is complex.
- **"We don't need FinOps" as avoidance, not mastery.** True Ri organizations don't need the
  framework because they've internalized its principles. Organizations in denial don't need
  the framework because they've never engaged with it. The outputs look identical on the
  surface but the underlying reality is opposite.
- **Optimizing everything to the floor.** Ri includes the wisdom to know when cost isn't the
  right constraint. Over-optimization that sacrifices velocity or reliability is Ha behavior —
  applying rules rigidly — not Ri.

## Assessment Framework

### Conducting the Assessment

Map the organization against three dimensions:

**1. Overall Stage:**
- Where does the organization primarily operate? (Shu / early Ha / mid Ha / late Ha / Ri)
- What's the evidence? (List 3-5 supporting observations)

**2. Capability Variation:**
Not all capabilities are at the same stage. Map key capabilities:

| Capability | Stage | Evidence |
|---|---|---|
| Cost visibility | Ha | Dashboards automated, teams review weekly |
| Tagging governance | Shu | Standards exist but only 60% coverage |
| Commitment strategy | Ha | SP portfolio managed, 85% utilization |
| CI/CD cost integration | Shu | No cost gates in pipeline |
| Unit economics | Not started | No cost-per-user tracking |

**3. Advancement Readiness:**
- Which stage-exit criteria are met?
- Which are gaps?
- What's the recommended next milestone?

### Quick Scoring

Rate each area 1-5 and sum for overall positioning:

| Area | 1 (Shu) | 3 (Ha) | 5 (Ri) |
|---|---|---|---|
| Cost visibility | Manual exports | Automated dashboards | Self-service, real-time |
| Accountability | Central team only | Showback to teams | Teams self-govern |
| Optimization | Reactive | Scheduled reviews | Continuous, automated |
| Architecture | Cost as afterthought | Cost in reviews | Cost as design constraint |
| Culture | "Finance's problem" | Shared responsibility | Engineering-owned |

**Total: 5-10 = Shu, 11-18 = Ha, 19-25 = Ri**

Use this as a conversation starter, not a definitive assessment. The qualitative evidence from
the stage descriptions above matters more than the number. An organization scoring 14 might be
solidly in Ha — or might be a Shu organization that overrates itself. Validate scores against
the stage-exit criteria.

Most organizations are in Shu whether they realize it or not. Only a small percentage have
genuinely reached Ha. Ri organizations are exceptional.

## Mapping to FinOps Foundation Crawl-Walk-Run

| Shuhari | Foundation | Key Difference |
|---|---|---|
| Shu | Crawl | Shu emphasizes patience and intuition, not just "getting started" |
| Ha | Walk | Ha emphasizes judgment and adaptation, not just "doing more" |
| Ri | Run | Ri emphasizes transcendence — framework becomes invisible, not "optimized" |

The Foundation explicitly states "Run" isn't the goal for every capability. Shuhari adds: even
within "Run," there are depths. A lifetime of martial arts practice still leaves room for
growth.

## Communication Guidelines

**For organizations in Shu:**
- Validate their starting point — Shu is where everyone begins
- Emphasize patience — rushing creates gaps that haunt later stages
- Focus on observable, quick-win improvements that build confidence
- Don't overwhelm with advanced concepts they're not ready for

**For organizations in Ha:**
- Challenge their assumptions — are they truly in Ha or Shu with different masters?
- Encourage experimentation and adaptation over copying
- Push for judgment over rules
- Surface where capabilities are still in Shu despite overall Ha positioning

**For organizations approaching Ri:**
- Stop benchmarking against frameworks
- Focus on what's unique about their approach
- Explore where depth remains even in "mastered" areas
- Celebrate what they've built while identifying remaining growth