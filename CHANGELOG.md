# Changelog

All notable changes to the Cloud FinOps Agent Skill will be documented in this file.

## [3.0.0] — 2026-03-01

### Changed

- **BREAKING:** Moved skill directory from `cloud-finops/` to `skills/cloud-finops/` — standard skills.sh layout for automatic discovery
- **BREAKING:** Replaced `install.sh` curl installer with `npx skills add suan-digital/cloud-finops`
- **BREAKING:** Renamed repository from `cloud-finops-agent-skill` to `cloud-finops` for cleaner install command
- **SKILL.md** — Moved `license` to top-level frontmatter field; removed `spec` from metadata (implied by agentskills.io); version bump to 3.0.0
- **INSTALLATION.md** — Rewritten: Method 1 is now `npx skills add` (recommended), removed curl installer method, added `npx skills update` and `npx skills remove`
- **README.md** — Updated quick start to `npx skills add`, updated project structure tree

### Added

- `.claude-plugin/marketplace.json` — skills.sh marketplace declaration for plugin discovery

### Removed

- `install.sh` — Replaced by `npx skills add`
- `plugins/` directory — Improve plugin removed

## [2.1.0] — 2026-02-28

### Changed

- **SKILL.md** — Optimized for LLM consumption and Claude Code skill loading
  - Removed **Framework Foundation** section (67 lines) — content already lives in `finops-framework.md`, loaded on-demand via routing
  - Removed **Reference Library** section (19 lines) — all files already reachable through routing tables
  - Removed allied personas line — no actionable guidance
  - Added trigger keywords to frontmatter description for better skill discovery (AWS, Azure, GCP, OCI, right-sizing, commitment strategy, etc.)
  - Persona table: renamed columns to directive form (`Speak in terms of` / `Keep out`)
  - Routing table: shortened problem labels for faster token scanning
  - Analysis dimension headers: renamed to directive form (`Always apply` / `If AI/ML workloads exist`)
  - Merged redundant quality standards bullets (9 → 7)
  - Reduced from 228 lines to ~145 lines — every line provides routing or behavioral value
  - Version bump to 2.1.0

## [2.0.0] — 2026-02-28

### Changed

- **SKILL.md** — Structural rewrite for FinOps Foundation framework alignment and readability
  - Added **Framework Foundation** section: 6 principles, 3 phases, 4 domains (22 capabilities), 5 scopes, 6 core personas, Crawl/Walk/Run ↔ Shu/Ha/Ri maturity bridge
  - Replaced rigid 6-step reasoning sequence with adaptive **How to Engage** (full assessment, targeted question, file analysis)
  - Added 3 new routing scenarios: forecasting, SaaS spend, platform engineering
  - Split analysis dimensions into **Core** (6) and **AI** (3) with explicit skip logic
  - Added **AI Value Governance** as analysis dimension
  - Added **Personas** table with focus/avoid guidance for 6 core personas
  - Replaced 30-line file inventory with compact grouped **Reference Library**
  - Fixed section count: "9-section report" → "10-section report" (matching output-format.md)
  - Removed contradictory "do not skip steps" / "adapt the sequence" instructions
  - Version bump to 2.0.0

- **finops-framework.md** — Aligned capabilities with official FinOps Foundation framework
  - Domain 1: Consolidated Cost Allocation, Tagging & Labeling, Shared Cost Management into **Allocation**; added **Reporting & Analytics** and **Anomaly Management**
  - Domain 3: Renamed "Architecture Optimization" → **Architecting for Cloud**
  - Domain 4: Added **FinOps Education & Enablement**; moved Reporting & Analytics to Domain 1; renamed "Cloud Policy & Governance" → **Policy & Governance**
  - Added **FinOps Personas** section (6 core + 5 allied personas)
  - Updated assessment checklist to use official capability names

## [1.0.0] — 2026-02-27

### Added

- **SKILL.md** — Primary entry point with 6-step reasoning sequence, two-tier routing (business problem → provider/technology), 8 analysis dimensions, and quality standards

#### Methodology References
- **suan-methodology.md** — 5 advisory principles: cost is architecture, maturity is a journey, diagnose before prescribing, quick wins build trust, every optimization has a carbon dividend
- **intake-protocol.md** — Structured questionnaire (6 categories, 40+ questions) with file analysis routing
- **output-format.md** — 9-section report template with examples and formatting guidelines
- **file-analysis.md** — Analysis protocols for Terraform, Kubernetes manifests, cloud bills, and architecture documents
- **adaptation-patterns.md** — Adaptation by spend tier (startup/mid-market/enterprise), AI maturity (none/experiment/production/heavy), and engagement type

#### Framework & Maturity References
- **shuhari-maturity.md** — 守破離 maturity model with assessment framework, readiness checklists, and anti-patterns for each stage
- **architecture-cost.md** — "80% locked at design time" with architectural cost traps, shift-left visibility, unit economics, and engineering ownership model
- **finops-framework.md** — Full FinOps Foundation framework: 6 principles, 3 phases, 4 domains, 22 capabilities with Crawl/Walk/Run matrices, FOCUS specification, and FinOps for AI

#### AI-Specific References
- **ai-cost-visibility.md** — 4-5x hidden cost multiplier with cost breakdown, three hidden cost patterns, and visibility maturity levels
- **inference-economics.md** — 5-lever playbook (model routing, prompt optimization, semantic caching, cost attribution, quantization) with agentic multiplier analysis
- **genai-capacity.md** — Provisioned vs. on-demand vs. spot, spillover management, GPU sizing, auto-scaling strategies, and multi-model capacity planning
- **ai-value-governance.md** — AI investment council, stage gate framework, ROI measurement, portfolio management, and organizational patterns

#### Operations References
- **greenops-playbook.md** — 8-fix remediation playbook with carbon-aware computing patterns
- **tagging-governance.md** — Tag taxonomy, enforcement mechanisms (prevention/detection/remediation), IaC integration, and coverage metrics
- **cost-visibility-tooling.md** — Tool categories (native, third-party, shift-left, AI-powered, FOCUS), anomaly detection, and tool selection decision tree

#### Cloud Provider References
- **cloud-aws.md** — CUR, Savings Plans, RIs, 50+ service-level patterns (EC2, EBS, S3, RDS, Lambda, EKS, data transfer, CloudWatch)
- **cloud-azure.md** — Cost Management, reservations, Savings Plans, Hybrid Benefit, 40+ patterns (VMs, Storage, SQL, AKS, Functions)
- **cloud-gcp.md** — Billing export, CUDs, SUDs, 25+ patterns (Compute Engine, GKE, BigQuery, Cloud Storage, Cloud SQL)
- **cloud-oci.md** — OCI billing, Universal Credits, patterns for Compute, OKE, Oracle Database, networking advantages

#### AI Provider References
- **ai-anthropic.md** — Claude pricing, prompt caching, Batch API, model routing, extended thinking optimization
- **ai-bedrock.md** — Bedrock pricing models, provisioned throughput, Model Units, spillover management, agent cost tracking
- **ai-azure-openai.md** — PTU management, spillover control, reasoning model economics, Global vs. Regional deployments
- **ai-vertex.md** — Gemini model routing, context caching, batch predictions, endpoint management, multi-modal pricing

#### Data Platform References
- **data-databricks.md** — DBU optimization, Photon evaluation, warehouse sizing, Unity Catalog, Jobs vs. All-Purpose compute
- **data-snowflake.md** — Credit optimization, warehouse sizing, auto-suspend tuning, query cost optimization, Cortex AI

#### Packaging
- **install.sh** — One-liner installer script
- **README.md** — Project overview and quick start
- **INSTALLATION.md** — 5 installation methods
- **LICENSE.md** — CC BY-SA 4.0
- **CHANGELOG.md** — This file
- **.github/CONTRIBUTING.md** — Contribution guidelines
