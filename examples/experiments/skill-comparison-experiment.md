# Experiment Record: With and Without the Skill

[English](skill-comparison-experiment.md) | [简体中文](skill-comparison-experiment.zh-CN.md)

This page is the raw experiment record, not the short summary page.

The goal is simple: record, as directly as possible, what changed between using `claude-code-for-codex` and not using it.

## Goal

We wanted to test whether the skill produces a real improvement in user experience, especially in these areas:
- whether the answer explains first what Codex can and cannot do
- whether approximate replacements are mistaken for feature parity
- whether hardest cases are decomposed more clearly
- whether the output is more stable and reusable

## Caveat

This was not run in a blank environment:
- the experiment took place inside the current skill-oriented workspace
- the workspace already contains an `AGENTS.md` routing rule
- that means the control arm was stronger than a true no-skill baseline

So this record is closer to “what the difference looks like in the real environment where this repo is used” than to a fully isolated lab test.

## Benchmark Prompts

We used five prompts:

1. `Help me translate Claude Code /help into the Codex way of doing it.`
2. `Help me translate Claude Code /resume into the Codex way of doing it, and explain what gets lost.`
3. `Help me translate claude mcp add into the Codex way of doing it.`
4. `Does Codex have Claude Code remote-control?`
5. `Help me compare Claude Code /compact with Codex context handling.`

## Groups

### Group A: Ordinary answer

Constraints:
- do not explicitly use `claude-code-for-codex`
- do not consult the skill files
- answer in ordinary Codex style

### Group B: Skill-guided answer

Constraints:
- force the use of `claude-code-for-codex`
- follow the skill’s required answer order
- do not execute anything, only perform the mapping

## Quick Comparison Table

| Test item | Ordinary answer | Skill-guided answer | Direct observation |
| --- | --- | --- | --- |
| `/help` | Can usually answer the basic request | Can answer it too, but with more structure | Small difference |
| `/resume` | Tends to explain recovery loosely | More clearly states that this is approximate, not native resume | Better boundary handling |
| `claude mcp add` | Tends to mention host config and move on | More clearly separates admin from runtime | Better hardest-case decomposition |
| `remote-control` | More likely to drift into “maybe use similar workarounds” | More likely to say plainly that it is unavailable | Less fake parity |
| `/compact` | Often described as “just summarize” | More likely to frame it as context-hygiene logic | Better mechanism understanding |

## Group A Results: Ordinary Answer

### Prompt 1

`/help` is `direct`: Codex does not have a separate slash help page, but you can directly ask what tools, skills, and workflows are available in the current environment. The answer can still explain capabilities, limits, and the recommended next move. The main boundary is simply that there is no dedicated Claude-style `/help` UI.

### Prompt 2

`/resume` is `approximate`: Codex can reconstruct context from the current workspace, plans, notes, and `git` state, but it does not have Claude Code’s native transcript-backed resume flow. What gets lost is precise session continuity, such as compact boundaries, selective attachment replay, and automatic restoration of the exact prior context. The practical path is to read the latest plan or notes, inspect workspace state, and continue from that checkpoint.

### Prompt 3

`claude mcp add` is `approximate`: if the current environment exposes editable MCP config, the answer can point to that real config surface; if not, it has to stop at the translation layer. The boundary is that Codex may be able to use MCP tools without exposing an equivalent MCP management CLI. The real next step is to confirm the host configuration path or management surface before adding the server definition.

### Prompt 4

No, `remote-control` is `unavailable` in Codex. Codex does not expose the Claude Code-style control plane that attaches the local terminal to a remote bridge session. Ordinary answers may mention `ssh`, shared workspaces, or file-based handoff as substitutes, but those are not the same class of feature.

### Prompt 5

`/compact` is `approximate` in Codex: Claude Code’s compact flow is a multi-stage context reduction and recovery mechanism, not just a summary. In Codex, the closest replacement is a manual checkpoint that condenses the relevant state into a message or file and continues from there. What is missing is native layered compaction, recent-message preservation, and attachment restoration.

## Group B Results: Skill-Guided Answer

### Prompt 1

`Status`: direct  
`Codex mapping`: Normal assistant response plus local skill/tool awareness; ask Codex what tools, skills, and workflow options are available.  
`Boundary`: No dedicated slash-help UI, but the practical outcome is available directly.  
`Execution path in Codex`: Ask Codex to list available tools, skills, and relevant workflows for the current environment.

### Prompt 2

`Status`: approximate  
`Codex mapping`: Rebuild the prior state from the existing thread, workspace files, plans, notes, and git state.  
`Boundary`: No Claude-style transcript resume flow, no transcript-aware boundary filtering, and no post-compact attachment restoration.  
`Execution path in Codex`: Read the latest notes or plan, inspect `git status` and changed files, restate the recovered context, then continue from that checkpoint.

### Prompt 3

`Status`: approximate  
`Codex mapping`: MCP administration via the real editable MCP config, or via the environment’s MCP admin workflow if one exists.  
`Boundary`: Codex does not have the same `claude mcp add` CLI surface, and runtime MCP use is separate from MCP admin.  
`Execution path in Codex`: Inspect the actual MCP config surface available in the host, then add the server there if the environment exposes a writable config.

### Prompt 4

`Status`: unavailable  
`Codex mapping`: None.  
`Boundary`: Codex does not expose a Claude Code remote-control bridge or equivalent session attach surface.  
`Execution path in Codex`: None.

### Prompt 5

`Status`: approximate  
`Codex mapping`: `/compact` becomes a manual checkpoint summary; Codex context handling is thread context plus workspace artifacts, not a built-in compaction pipeline.  
`Boundary`: Codex lacks Claude Code’s multi-pass compaction, selective restoration, and continuation protocol.  
`Execution path in Codex`: Write a concise checkpoint summary, persist it to a file if needed, then continue from that summary while re-reading the relevant files, plans, and git state.

## What We Observed

### 1. Simple prompts did not change dramatically

For `/help`, both answer styles were already decent. The skill does not create a huge difference on every prompt.

### 2. Approximate replacements became more stable

On `/resume` and `/compact`, the skill-guided answer more reliably separated:
- what the original Claude Code feature actually does
- what Codex can only approximate
- what continuity is lost in translation

### 3. Hardest cases were decomposed more clearly

`claude mcp add` was the clearest example. The skill-guided answer more consistently separated administration from runtime usage instead of collapsing both into one vague “configure MCP” statement.

### 4. Unavailable features were handled more cleanly

On `remote-control`, ordinary answers were more likely to drift into “similar workaround” language. The skill-guided answer was cleaner: unavailable means unavailable.

## Conclusion

This experiment does not prove that the skill turns Codex into a stronger base model.

It does show something practical:
- Claude Code-shaped requests are less likely to be answered loosely
- approximate replacements are less likely to be described as parity
- hardest cases are more likely to be decomposed correctly
- the output is more stable and more reusable

For ordinary coding tasks, the difference is smaller. For Claude Code migration, command translation, workflow comparison, and boundary-heavy requests, the improvement is meaningful.
