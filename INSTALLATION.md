# Installation Guide

3 ways to install the Cloud FinOps Agent Skill.

## Method 1: skills.sh CLI (Recommended)

Works with Claude Code, Cursor, Codex, OpenCode, and 40+ other agents.

```bash
npx skills add suan-digital/cloud-finops-agent-skill
```

The CLI auto-detects your agent and installs the skill to the correct location.

### Updating

```bash
npx skills update cloud-finops
```

### Uninstalling

```bash
npx skills remove cloud-finops
```

## Method 2: Claude.ai Projects

For use in Claude.ai project knowledge:

1. Download the repository as a ZIP
2. In your Claude.ai project, go to **Project Knowledge**
3. Upload `skills/cloud-finops/SKILL.md` as the entry point
4. Upload all files from `skills/cloud-finops/references/` as additional knowledge files

**Note:** Claude.ai has file size limits. If you hit limits, prioritize uploading:
- `SKILL.md` (required — entry point)
- `intake-protocol.md`, `output-format.md`, `suan-methodology.md` (core methodology)
- Provider-specific files relevant to your environment

## Method 3: API / System Prompt

For direct API integration, include `SKILL.md` content in your system prompt and reference
files as needed:

```python
import anthropic

# Load the skill
with open("skills/cloud-finops/SKILL.md") as f:
    skill_content = f.read()

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=8192,
    system=skill_content,
    messages=[
        {"role": "user", "content": "Assess our FinOps maturity. We're on AWS, spending $120K/month."}
    ]
)
```

For reference files, load them dynamically based on the routing table in SKILL.md,
or include the most relevant ones in your system prompt.

## Verifying Installation

After installation, verify all files are present:

```bash
# Count files (should be 26: 1 entry point + 25 references)
find .claude/skills/cloud-finops -name "*.md" | wc -l

# List all reference files
ls .claude/skills/cloud-finops/references/
```

Expected reference files:
```
adaptation-patterns.md    cloud-gcp.md            greenops-playbook.md
ai-anthropic.md           cloud-oci.md            inference-economics.md
ai-azure-openai.md        cost-visibility-tooling.md  intake-protocol.md
ai-bedrock.md             data-databricks.md      output-format.md
ai-cost-visibility.md     data-snowflake.md       shuhari-maturity.md
ai-value-governance.md    file-analysis.md        suan-methodology.md
ai-vertex.md              finops-framework.md     tagging-governance.md
architecture-cost.md      genai-capacity.md
cloud-aws.md              cloud-azure.md
```

## Testing the Installation

Try these prompts to verify the skill is loaded:

1. **"Assess our FinOps maturity"**
   - Should trigger the intake protocol (asking questions before analysis)
   - Should reference the Shuhari framework

2. **"Our AWS bill is $80K/month, too high"**
   - Should ask intake questions about environment and architecture
   - Should eventually reference AWS-specific optimization patterns

3. **"AI inference costs are out of control"**
   - Should trigger AI-specific intake questions
   - Should reference inference economics and AI cost visibility
