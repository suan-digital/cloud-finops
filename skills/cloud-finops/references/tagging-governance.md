# Tagging & Labeling Governance

Tagging is the foundation of cost attribution. Without consistent, enforced tagging, cost data
is just numbers without actionable insight. 40% of organizations can't accurately attribute
cloud spend — tagging gaps are the primary cause.

## Why Tagging Matters

**Cost attribution chain:** Tags → Allocation → Accountability → Behavior change

Without tags:
- Finance can't attribute costs to teams or products
- Engineering can't identify which services drive spend
- FinOps can't measure optimization impact
- Nobody can calculate unit economics
- Chargeback/showback is impossible

With 90%+ tagging coverage:
- Every dollar is attributed to an owner
- Cost anomalies are immediately traceable
- Unit economics (cost per user, per request) are calculable
- Optimization impact is measurable by team
- Sustainability metrics can be attributed

## Tag Taxonomy

### Mandatory Tags (Minimum Viable Set)

Every resource must have these tags. Enforce via policy — no exceptions.

| Tag Key | Purpose | Example Values |
|---|---|---|
| `team` | Cost ownership | `platform`, `payments`, `data-eng`, `ml` |
| `environment` | Lifecycle stage | `production`, `staging`, `development`, `sandbox` |
| `service` | Application/service name | `api-gateway`, `user-service`, `ml-pipeline` |
| `cost-center` | Financial attribution | `eng-001`, `marketing-002`, `data-003` |

### Recommended Tags (High Value)

Add these as the organization matures:

| Tag Key | Purpose | Example Values |
|---|---|---|
| `product` | Product/feature attribution | `checkout`, `search`, `recommendations` |
| `owner` | Individual accountability | `jsmith@company.com`, `team-platform` |
| `managed-by` | IaC tool tracking | `terraform`, `cloudformation`, `manual` |
| `created-date` | Age tracking for cleanup | `2026-01-15` |
| `expiration` | Lifecycle management | `2026-04-15`, `never` |
| `data-classification` | Compliance and storage tiering | `public`, `internal`, `confidential`, `regulated` |
| `compliance` | Regulatory mapping | `hipaa`, `pci`, `sox`, `gdpr` |

### AI-Specific Tags

For organizations with AI workloads:

| Tag Key | Purpose | Example Values |
|---|---|---|
| `ai-workload` | AI cost attribution | `inference`, `training`, `fine-tuning`, `rag` |
| `model` | Model cost tracking | `claude-sonnet`, `gpt-4o`, `llama-70b` |
| `ai-feature` | Feature-level AI cost | `chat-support`, `code-review`, `summarization` |
| `gpu-purpose` | GPU utilization tracking | `inference`, `training`, `development` |

## Tag Naming Conventions

### Rules

1. **Lowercase with hyphens:** `cost-center` not `CostCenter` or `cost_center`
2. **Consistent across providers:** Same tag keys in AWS, Azure, GCP
3. **No spaces:** Use hyphens as separators
4. **Finite value sets:** Define allowed values for each tag (enumerated, not free-text)
5. **Provider mapping:** Document the mapping between providers

| Concept | AWS Tag | Azure Tag/Label | GCP Label |
|---|---|---|---|
| Team | `team` | `team` | `team` |
| Environment | `environment` | `environment` | `environment` |
| Service | `service` | `service` | `service` |
| Cost center | `cost-center` | `cost-center` | `cost-center` |

*Note: Azure tags allow 512 characters for key and value; GCP labels allow 63 characters for
key and value; AWS tags allow 128/256 characters for key/value.*

## Enforcement Mechanisms

### Prevention (Best)

Stop untagged resources from being created.

**AWS:**
- Service Control Policies (SCPs) — deny resource creation without required tags
- AWS Config rules — detect non-compliant resources
- CloudFormation Guard — validate templates before deployment

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "DenyUntaggedEC2",
    "Effect": "Deny",
    "Action": "ec2:RunInstances",
    "Resource": "arn:aws:ec2:*:*:instance/*",
    "Condition": {
      "Null": {
        "aws:RequestTag/team": "true",
        "aws:RequestTag/environment": "true",
        "aws:RequestTag/service": "true"
      }
    }
  }]
}
```

**Azure:**
- Azure Policy — deny or audit resources missing required tags
- Initiative definitions — group tag policies together

**GCP:**
- Organization policies — require labels at project or folder level
- Config Connector policies — enforce in GKE

### Detection (Good)

Find and remediate untagged resources after creation.

| Tool | Provider | Capability |
|---|---|---|
| AWS Config | AWS | Continuous compliance monitoring |
| AWS Tag Editor | AWS | Bulk tag management and discovery |
| Azure Policy (audit mode) | Azure | Non-compliance reporting |
| GCP Asset Inventory | GCP | Resource and label inventory |
| Cloud Custodian | Multi-cloud | Policy-as-code, remediation actions |
| Infracost | Multi-cloud | Tag validation in CI/CD |

### Remediation

Handle existing untagged resources:

1. **Export untagged resource inventory** — by service, by account
2. **Prioritize by cost** — tag the expensive resources first
3. **Auto-tag where possible** — inherit tags from parent (VPC, subnet, resource group)
4. **Set a deadline** — "all resources tagged by [date] or terminated"
5. **Measure progress weekly** — track coverage percentage trending toward 90%+

## Infrastructure as Code Integration

### Terraform

**Default tags via provider block (AWS):**
```hcl
provider "aws" {
  default_tags {
    tags = {
      team        = var.team
      environment = var.environment
      managed-by  = "terraform"
      service     = var.service_name
    }
  }
}
```

**Module-level enforcement:**
```hcl
variable "required_tags" {
  type = object({
    team        = string
    environment = string
    service     = string
    cost-center = string
  })
}
```

### CI/CD Validation

Add tag validation to the deployment pipeline:

1. **Pre-plan check:** Validate that all resources in Terraform have required tags
2. **Plan-time check:** Use `terraform plan` output to verify tags are set
3. **Infracost integration:** Flag untagged resources alongside cost estimates
4. **Post-deploy check:** AWS Config or equivalent validates deployed resources

### Tag Drift Prevention

Tags set by IaC can be manually changed or removed. Prevent drift:

- **AWS Config rules** — detect when tags change from IaC-defined values
- **Terraform refresh** — detect drift on `terraform plan`
- **Automated remediation** — Lambda function to restore tags from IaC state
- **Cloud Custodian policies** — auto-remediate tag changes

## Coverage Metrics

### Measuring Tag Coverage

| Metric | Formula | Target |
|---|---|---|
| Resource coverage | Tagged resources / total resources | >90% |
| Spend coverage | Tagged spend / total spend | >90% |
| Compliance rate | Correctly tagged / total tagged | >95% |
| Tag completeness | Resources with ALL required tags / total | >85% |

### Reporting

Track and report tag coverage:

| Report | Frequency | Audience |
|---|---|---|
| Tag coverage dashboard | Real-time | FinOps team |
| Coverage by team | Weekly | Engineering leads |
| Untagged spend report | Weekly | Finance + FinOps |
| Compliance trend | Monthly | Leadership |

## Cost Allocation Models

Tags enable cost allocation, but allocation requires a model. Choose based on organizational maturity and culture.

### Showback vs Chargeback

| Model | Definition | When to Use | Maturity |
|---|---|---|---|
| **Showback** | Display cost data to teams — no financial impact | Starting out, building awareness | Crawl/Walk |
| **Chargeback** | Transfer costs to team budgets — real financial impact | Mature practice, clear ownership | Walk/Run |
| **Hybrid** | Chargeback for direct resources, showback for shared | Most organizations land here | Walk/Run |

**Start with showback.** Chargeback without accurate data creates political fights, not accountability. Graduate to chargeback only when tagging coverage exceeds 90% and teams trust the data.

### Showback Implementation

1. **Build dashboards** — cost by team, environment, service (weekly)
2. **Send automated reports** — email/Slack cost summaries to team leads
3. **Add context** — show cost trends, anomalies, and peer comparisons
4. **No budget consequences** — purely informational in this phase
5. **Track behavior change** — measure whether visibility alone drives optimization

Showback alone reduces waste by 15–25% in organizations where teams had no prior cost visibility.

### Chargeback Implementation

1. **Define the billing unit** — team, business unit, cost center, or product
2. **Map tags to billing units** — each billing unit maps to tag values
3. **Set allocation frequency** — monthly aligned with financial close
4. **Establish dispute process** — teams must be able to challenge incorrect charges
5. **Integrate with finance systems** — export allocations to ERP or GL

### Shared Cost Distribution

Not all costs map cleanly to one team. Shared services (networking, security, platform infrastructure, support contracts) require a distribution strategy.

| Strategy | How It Works | Best For |
|---|---|---|
| **Proportional** | Distribute by each team's % of total direct spend | General shared infrastructure |
| **Even split** | Divide equally among consuming teams | Services with equal consumption |
| **Usage-based** | Distribute by measured consumption (requests, data transfer) | APIs, shared databases, platform services |
| **Fixed allocation** | Pre-agreed percentages per team | Enterprise licenses, support contracts |

**Recommended approach:** Allocate direct costs (70–80% of spend) via tags. Distribute shared costs (20–30%) proportionally. Don't over-engineer shared cost splits — a reasonable approximation that everyone accepts beats a precise formula nobody trusts.

### Unattributable Costs

Some costs resist attribution: cross-AZ data transfer, DNS, IAM, CloudTrail, organization-level services. Handle these explicitly:

1. **Categorize** — list all unattributable cost categories and their monthly totals
2. **Minimize** — improve tagging to shrink the unattributable pool over time
3. **Distribute** — apply a flat overhead rate or proportional distribution
4. **Report separately** — show unattributable costs as a line item, not hidden in team totals
5. **Target** — keep unattributable costs below 10% of total spend

## Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Free-text tag values | Inconsistent, hard to aggregate | Enumerated allowed values |
| Tags only on compute | Storage, networking, databases untagged | Tag all resource types |
| Manual tagging | Inconsistent, forgotten | IaC + enforcement policies |
| Tag-and-forget | Values become stale (team renamed, service retired) | Periodic tag audits |
| Too many required tags | Teams resist, compliance drops | Start with 4 mandatory, add gradually |
| Case sensitivity issues | `Production` vs `production` vs `PRODUCTION` | Lowercase-only policy |

## Maturity Model

| Maturity | Coverage | Enforcement | Automation |
|---|---|---|---|
| **Crawl** | <50%, inconsistent | None — honor system | Manual tagging |
| **Walk** | 70-85%, mostly consistent | Detection + reporting | IaC defaults, some prevention |
| **Run** | 90%+, consistent | Prevention (SCPs/policies) | Full IaC, auto-remediation, CI/CD |

## Assessment Questions

1. What's the current tagging coverage? (% of resources, % of spend)
2. Are there defined tagging standards? Are they documented?
3. How are tags enforced? (Prevention, detection, or honor system?)
4. Is tagging integrated into IaC? (Default tags in Terraform/CDK?)
5. Are tag values enumerated or free-text?
6. How consistent are tags across providers? (Multi-cloud)
7. Are AI workloads tagged distinctly from infrastructure?
8. Is there a process for handling untagged resources?
9. Who owns the tagging standard? (FinOps, platform team, nobody)
10. What's the plan to get from current coverage to 90%+?