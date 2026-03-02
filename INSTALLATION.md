# Installation Guide

3 ways to install the Cloud FinOps Agent Skill.

## Method 1: skills.sh CLI (Recommended)

Works with Claude Code, Cursor, Codex, OpenCode, and 40+ other agents.

```bash
npx skills add suan-digital/cloud-finops
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
- `references/capabilities/` files relevant to your situation
- `references/personas.md` for persona context

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

## Verify

```bash
find .claude/skills/cloud-finops -name "*.md" | wc -l
# Should list all skill markdown files
```

Test with: **"Assess our FinOps maturity"** — should trigger intake questions before analysis.
