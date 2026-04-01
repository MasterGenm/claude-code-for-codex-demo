# Skill Evals

This directory contains the minimal regression framework for the `claude-code-for-codex` skill.

## Scope

This MVP does static regression checks for:
- `prompt -> expected_status`
- optional mapping-text snippets that should appear in the matched command or workflow row

It does **not** run model behavior or judge full natural-language answers.

## Files

- `fixtures/basic-regression.json`: starter regression fixtures
- `fixtures/settings-memory.json`: mechanism-level checks for guidance files, hooks, plans, and memory-related boundaries
- `fixtures/agent-mcp-remote.json`: mechanism-level checks for delegation, MCP admin/runtime, and remote-control boundaries
- `fixtures/repo-plugin-control-plane.json`: control-plane checks for repo behavior placement, skills and agents discovery, and plugin lifecycle boundaries
- `fixtures/hook-tool-governance.json`: mechanism-level checks for hook mediation, plugin-provided hooks, and MCP/admin boundaries that still route through existing command rows
- `fixtures/registry-and-precedence.json`: mechanism-level checks for ordered roots, shadowing, legacy compatibility directories, and artifact placement
- `fixtures/context-hygiene.json`: mechanism-level checks for compaction, resume correctness, checkpoint export, and visible context pressure
- `fixtures/permission-decision-ladder.json`: mechanism-level checks for permission ordering, sandbox boundaries, dangerous-command reasoning, and approval-surface explanations
- `fixtures/mcp-runtime-inbound-control-plane.json`: mechanism-level checks for MCP runtime use, admin inspection, add/remove boundaries, and inbound/channel expectations
- `../scripts/run_skill_evals.py`: eval runner

## Run

From the repo root:

```powershell
python .\scripts\run_skill_evals.py --skill-root . --fixtures .\evals\fixtures\basic-regression.json
```

Additional packs:

```powershell
python .\scripts\run_skill_evals.py --skill-root . --fixtures .\evals\fixtures\settings-memory.json
python .\scripts\run_skill_evals.py --skill-root . --fixtures .\evals\fixtures\agent-mcp-remote.json
python .\scripts\run_skill_evals.py --skill-root . --fixtures .\evals\fixtures\repo-plugin-control-plane.json
python .\scripts\run_skill_evals.py --skill-root . --fixtures .\evals\fixtures\hook-tool-governance.json
python .\scripts\run_skill_evals.py --skill-root . --fixtures .\evals\fixtures\registry-and-precedence.json
python .\scripts\run_skill_evals.py --skill-root . --fixtures .\evals\fixtures\context-hygiene.json
python .\scripts\run_skill_evals.py --skill-root . --fixtures .\evals\fixtures\permission-decision-ladder.json
python .\scripts\run_skill_evals.py --skill-root . --fixtures .\evals\fixtures\mcp-runtime-inbound-control-plane.json
```

## How It Works

The runner:
1. Parses `references/command-mapping.md`
2. Parses `references/workflow-mapping.md`
3. Normalizes aliases from `references/aliases-and-visibility.md`
4. Matches each prompt against the known command and workflow phrases
5. Compares the matched status and mapping text against fixture expectations

The mechanism packs are still static. They improve regression coverage by forcing hardest boundary prompts back through known command and workflow rows.

The hook-governance pack does not yet parse mechanism references directly. It keeps coverage small by making hook-heavy prompts resolve through the existing `/hooks`, `/permissions`, `/config`, `/plugin`, and MCP/plugin CLI rows.

The registry-and-precedence pack works the same way. It keeps coverage compatible with the current runner by routing precedence-heavy prompts through the existing `/skills`, `/agents`, `/init`, and plugin rows.

The context-hygiene pack also stays compatible with the current runner. It routes compaction and continuity prompts through the existing `/compact`, `/resume`, `/rewind`, `/context`, and export/checkpoint rows.

The permission-decision-ladder pack works the same way. It keeps coverage small by routing risk-heavy prompts through the existing `/permissions`, `/config`, `/hooks`, `/sandbox`, `/env`, `claude doctor`, and permissions workflow rows.

The MCP runtime and inbound-control pack also stays compatible with the current runner. It routes hardest MCP prompts through the existing `/mcp`, `claude mcp *`, and MCP workflow rows instead of requiring a new command taxonomy.

## Current Limitations

- Matching is phrase-based, not semantic
- Command matches take priority over workflow matches
- Mapping-text checks validate the matched row text, not the final assistant answer
- This is a regression skeleton, not a behavior-eval system
