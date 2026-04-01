# Claude Code for Codex

[English](README.md) | [简体中文](README.zh-CN.md)

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
+-- README.md
+-- .gitignore
+-- SKILL.md
+-- agents/
+-- evals/
+-- references/
+-- scripts/
`-- examples/
    +-- with-vs-without-skill.md
    +-- with-vs-without-skill.zh-CN.md
    `-- experiments/
        +-- skill-comparison-experiment.md
        `-- skill-comparison-experiment.zh-CN.md
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

## Release Scope

This public release includes:
- one installable Codex skill rooted at [`SKILL.md`](SKILL.md)
- command and workflow mappings for Claude Code slash commands and CLI flows
- mechanism-level references for the hardest Claude Code runtime concepts
- maintenance scripts for upstream drift detection
- a small regression framework with fixture packs under [`evals/`](evals)

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
