# CLAUDE.md — Project Instructions for Claude Code

## Repository

Cloud FinOps Agent Skill — 25 reference files providing structured FinOps domain knowledge to LLMs.
Maintained by Suan Digital (https://suan.digital). Licensed CC BY-SA 4.0.

## Git Conventions

- **Commit email:** Always use `git -c user.email=github@suan.digital -c user.name="suan"` for commits
- **Branch naming:** `improve/<short-slug>` for auto-improvement PRs
- **Commit messages:** Conventional commits — `feat:`, `fix:`, `docs:`, `chore:`
- **PR titles:** Short, imperative, under 70 characters

## Content Style

- **Direct and confident** — Expert advisor tone, not cautious consultant
- **Specific and actionable** — "right-size instances" is vague; "migrate m5.4xlarge to m6i.xlarge" is actionable
- **Quantify impact** — Use ranges when exact numbers aren't available
- **Plain language** — Avoid jargon without explanation
- **Accurate statistics** — Cite sources. Do not fabricate numbers. Use "typically X–Y" if uncertain.

## File Structure

All skill content lives in `skills/cloud-finops/`:
- `SKILL.md` — Entry point (agentskills.io spec)
- `references/` — 25 domain reference files

Each reference file should have:
1. Title and scope description
2. Core content with tables, patterns, actionable guidance
3. Assessment questions for analysis

## When Making Changes

- Read the target file(s) before editing
- Preserve existing structure and formatting conventions
- Keep tables aligned and consistent
- Do not add provider vendor recommendations unless backed by data
- Statistics must come from reference files or well-known industry sources
