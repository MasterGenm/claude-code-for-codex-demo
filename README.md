# Claude Code for Codex

[English](README.md) | [简体中文](README.zh-CN.md)

> 系统化处理 Claude Code 到 Codex 的命令和工作流迁移。不是一张对照表，而是一个带三态分类（direct / approximate / unavailable）、执行策略、回归测试和上游漂移检测的兼容层 Agent Skill。

Translate Claude Code commands and workflows into Codex-native procedures without pretending the two products are the same.

This repository packages a Codex skill that:
- maps Claude Code slash commands, CLI subcommands, and operating workflows into Codex terms
- forces a `map-first, confirm-before-execute` policy
- labels every mapping as `direct`, `approximate`, or `unavailable`
- keeps product differences explicit instead of hiding them behind vague workarounds
- includes maintenance scripts to detect mapping drift against upstream Claude Code source snapshots

Current release scope: `v0.1` of a publishable, source-anchored compatibility skill. This repo ships a stable translator plus mechanism references and regression checks, not a full Claude Code reimplementation.

## Why This Exists

Claude Code and Codex overlap, but they are not interchangeable:
- command names are different
- some workflows are only approximately portable
- some Claude Code features are product-owned and cannot be reproduced in Codex

Without a compatibility layer, it is easy to answer a Claude Code-style request as if Codex had the same surface. This skill exists to prevent that category error.

## What Changes In Practice

| Scenario | Without the skill | With the skill | Practical difference |
| --- | --- | --- | --- |
| `/help` | Usually fine | Usually fine, but more structured | Small difference |
| `/resume` | Easier to describe loosely | More explicit about what is lost | Better boundary handling |
| `claude mcp add` | Easier to blur runtime and admin | More likely to split the layers correctly | Better hardest-case decomposition |
| `remote-control` | More likely to drift into “similar workaround” talk | More likely to say plainly that it is unavailable | Less fake parity |
| `/compact` | Often described as “just summarize” | More likely to treat it as context-hygiene logic | Better mechanism understanding |

For a fuller summary, see [`examples/with-vs-without-skill.md`](examples/with-vs-without-skill.md).  
For the full experiment record, see [`examples/experiments/skill-comparison-experiment.md`](examples/experiments/skill-comparison-experiment.md).

## What This Repo Contains

The repository root is also the installable Codex skill directory. Install the whole folder, not just `SKILL.md`.

```text
claude-code-for-codex/
+-- README.md / README.zh-CN.md
+-- SKILL.md                          # Skill entry: 18-step decision flow
+-- agents/openai.yaml                # Codex agent interface
+-- references/                       # 19 mechanism-level docs (3000+ lines)
|   +-- command-mapping.md            # 100+ command mappings (direct/approximate/unavailable)
|   +-- workflow-mapping.md           # workflow-level migration rules
|   +-- capability-boundaries.md      # product difference matrix
|   +-- execution-policy.md           # map-first, confirm-before-execute rules
|   `-- ... (14 more mechanism references with upstream source anchors)
+-- evals/                            # 9 regression fixture suites (500+ test cases)
+-- scripts/                          # 4 maintenance tools incl. upstream drift detection
|   +-- run_skill_evals.py            # regression runner
|   +-- check_mapping_consistency.py  # upstream drift detector
|   `-- ...
`-- examples/                         # with-vs-without comparison + experiment records
```

## What The Skill Does

The skill turns Claude Code requests into a stable response contract:

1. `Status`
2. `Codex mapping`
3. `Boundary`
4. `Execution path in Codex`

It then asks for confirmation before execution.

Core references:
- command mappings: [`references/command-mapping.md`](references/command-mapping.md)
- workflow mappings: [`references/workflow-mapping.md`](references/workflow-mapping.md)
- capability boundaries: [`references/capability-boundaries.md`](references/capability-boundaries.md)
- execution policy: [`references/execution-policy.md`](references/execution-policy.md)
- hardest integration paths: [`references/integration-playbooks.md`](references/integration-playbooks.md)

Mechanism references:
- architecture overview: [`references/architecture-lenses.md`](references/architecture-lenses.md)
- hook-aware tool governance: [`references/hook-and-tool-governance.md`](references/hook-and-tool-governance.md)
- registry and precedence: [`references/registry-and-precedence.md`](references/registry-and-precedence.md)
- context hygiene: [`references/context-hygiene.md`](references/context-hygiene.md)
- permission decision ladder: [`references/permission-decision-ladder.md`](references/permission-decision-ladder.md)
- MCP runtime and inbound control plane: [`references/mcp-runtime-and-inbound-control-plane.md`](references/mcp-runtime-and-inbound-control-plane.md)

## What The Skill Does Not Do

This skill does not:
- make Codex a stronger base model
- add Claude Code product surfaces such as daemon, mobile, voice, account settings, or remote-control server behavior
- replace ordinary coding, debugging, testing, or code review skills
- claim feature parity where only an approximation exists

If a capability is not truly available in Codex, the skill should say `unavailable`.

## Skill Design

This project is not a cheatsheet or a blog post. It is a structured translation-layer Agent Skill with explicit design decisions:

| Design aspect | Implementation |
| --- | --- |
| **Decision framework** | Three-status classification (`direct` / `approximate` / `unavailable`) with per-status execution rules |
| **Execution governance** | Map-first, confirm-before-execute policy enforced through SKILL.md output rules |
| **Standardized output** | Every response follows Status → Mapping → Boundary → Execution path |
| **Regression testing** | 9 fixture suites (500+ cases) covering basic mappings through mechanism-level boundaries |
| **Maintainability** | Upstream drift detection scripts + command registry extraction from Claude Code source |
| **Knowledge depth** | 19 reference documents with source-code anchors, not surface-level summaries |

This is a **translation-layer Skill** — its core value is systematically managing product differences, not adding runtime capabilities. It complements domain-expertise Skills (such as [rag-system-planner](https://github.com/MasterGenm/rag-system-planner-demo)) by demonstrating a different Agent Skill paradigm: cross-product semantic compatibility rather than domain knowledge structuring.

## Internship Relevance

| Capability | Demonstrated in this project |
| --- | --- |
| Systematic product analysis | 100+ commands mapped with three-status taxonomy; every `approximate` explains what is lost |
| Agent Skill design methodology | Structured execution flow, output contracts, triggering conditions — not a prompt but a workflow asset |
| Engineering rigor for knowledge assets | Regression framework, upstream drift detection, automated consistency checks |
| Cross-product migration thinking | Explicit boundary management instead of vague "similar workaround" answers |
| Source-level technical depth | 19 reference documents anchored to upstream source code, not surface-level documentation |

### Not yet done

- No behavior-level evaluation (current evals are static regression, not model-output judges)
- No CI automation (scripts exist but are run manually)
- Narrow scope: only Claude Code → Codex, not a general cross-product migration framework

## Release Scope

This public release includes:
- one installable Codex skill with an 18-step decision flow ([`SKILL.md`](SKILL.md))
- **100+ command and workflow mappings**, each classified as `direct`, `approximate`, or `unavailable`
- **19 mechanism-level reference documents** (3000+ lines), with upstream source anchors
- 4 maintenance scripts including automated upstream drift detection
- **9 regression fixture suites** (500+ test cases) under [`evals/`](evals)

This release does **not** claim:
- full Claude Code parity
- daemon, mobile, voice, bridge, account, or remote-control product surfaces
- transcript-native resume/rewind/compact primitives in Codex
- behavior-eval parity beyond the included static regression framework

## Install

### Option 1: Local checkout into Codex skills

Clone this repository, then copy the entire repo folder into your Codex skills folder.

PowerShell:

```powershell
git clone https://github.com/MasterGenm/claude-code-for-codex-demo.git
New-Item -ItemType Directory -Force -Path $env:USERPROFILE\.codex\skills | Out-Null
Copy-Item -Recurse -Force .\claude-code-for-codex-demo `
  $env:USERPROFILE\.codex\skills\
```

### Option 2: Project-local install

If you want the skill scoped to one repo, copy this folder into:

```text
.agents/skills/claude-code-for-codex
```

### Option 3: Route Claude Code requests through AGENTS

If you want Claude Code-style requests to default to this skill inside one workspace, add an `AGENTS.md` rule such as:

```md
Use $claude-code-for-codex when a request mentions Claude Code commands, migration from Claude Code to Codex, or a Claude Code workflow concept where semantic mismatch is likely.
```

## Usage

Typical prompts:
- `Use $claude-code-for-codex to map /review into a Codex workflow`
- `How do I do claude mcp add in Codex?`
- `Rewrite this Claude Code runbook for Codex`
- `Map /resume into Codex and explain what is lost`

## Triggering Guidance

This skill should trigger when a request:
- names a Claude Code slash command or CLI subcommand
- asks for Claude Code to Codex migration or comparison
- uses Claude Code workflow concepts such as `resume`, `compact`, conversation `branch`, `mcp`, or `plugin install`
- would be unsafe to execute without first classifying the mapping

It should not trigger by default for:
- ordinary coding tasks
- normal debugging or testing
- standard git operations with no Claude Code semantic ambiguity

## Limitations

| Current limitation | Possible direction |
| --- | --- |
| Static regression only, no behavior-level eval | Add judge-based eval for model output quality |
| Manual script execution, no CI | Add GitHub Action for drift check on schedule |
| Only covers Claude Code → Codex direction | Generalize to a cross-product Skill migration framework |
| Single upstream snapshot, no continuous tracking | Automate periodic upstream extraction |
