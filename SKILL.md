---
name: claude-code-for-codex
description: Translate Claude Code slash commands, CLI subcommands, and operating workflows into Codex-native procedures using a map-first, confirm-before-execute policy. Use when a user asks how to do something in Codex that they know from Claude Code, wants a command-by-command migration, needs Claude Code docs rewritten for Codex, or wants Codex to perform a Claude-like task after first stating whether the mapping is direct, approximate, or unavailable.
---

# Claude Code For Codex

## Overview

Translate Claude Code behavior into Codex-native operations without assuming the two systems are equivalent. Map the user goal first, then decide whether Codex supports it directly, approximately, or not at all.

This skill is for migration and operational translation, not for pretending Codex exposes the same slash-command surface. Always make capability differences explicit, and do not execute anything before the mapping result is stated.

## Core Principles

- Treat Claude Code and Codex as different products with overlapping but non-identical capabilities.
- Prefer the user outcome over the Claude command spelling.
- Use exactly three status labels: `direct`, `approximate`, `unavailable`.
- If the mapping is not `direct`, explain the boundary before giving the fallback.
- If the mapping is `unavailable`, say so plainly and give the reason.
- Follow a map-first, confirm-before-execute policy. Mapping is mandatory; execution is conditional.
- Treat the user's initial request to "do it now" as intent, not as post-mapping confirmation.
- Do not claim parity for session controls, daemon behavior, remote control, mobile surfaces, or Anthropic-internal features unless the current Codex environment truly exposes them.
- Keep the answer operational. Tell Codex what to do, not just what the two products conceptually share.

## Execution Flow

1. Identify the request shape.
   Use `references/command-mapping.md` when the user names a Claude Code slash command or CLI subcommand.
   Use `references/workflow-mapping.md` when the user describes a behavior such as plan mode, resume, permissions, review flow, subagents, MCP usage, or worktree handling.
   Use `references/aliases-and-visibility.md` when the user uses an alias, shorthand, or a command that is hidden, gated, or environment-specific upstream.
2. Check `references/capability-boundaries.md` if the request assumes product parity or spans multiple command areas.
3. Read `references/architecture-lenses.md` when the request is a hardest case and needs mechanism-level explanation rather than only a command lookup.
4. Read `references/settings-memory-and-hooks.md` when the request touches `/init`, `/memory`, `/hooks`, settings layering, plans, or repo guidance artifacts.
5. Read `references/agent-isolation-and-background.md` when the request touches `/fork`, `/agents`, `/tasks`, worktree isolation, background execution, or remote-control assumptions.
6. Read `references/repo-operating-system.md` when the request is really about instruction discovery, settings layering, skills, agents, or where repo behavior should live.
7. Read `references/hook-and-tool-governance.md` when the request is really about tool-event hooks, permission mediation, MCP-output mutation, or runtime continuation control.
8. Read `references/registry-and-precedence.md` when the request is really about discovery roots, source precedence, shadowing, or where a behavior definition should live.
9. Read `references/context-hygiene.md` when the request is really about compaction, resume correctness, rewind boundaries, context pressure, overflow recovery, or post-compact restoration.
10. Read `references/mcp-runtime-and-inbound-control-plane.md` when the request is really about MCP runtime identity, auth, reconnect, resource discovery, channel notifications, or admin-versus-runtime boundaries.
11. Read `references/permission-decision-ladder.md` when the request is really about risk ordering, permission prompts, dangerous paths or commands, blast radius, or why a permission action is only approximate.
12. Read `references/plugin-runtime-and-lifecycle.md` when the request is really about extension behavior rather than only marketplace-style plugin commands.
13. Choose a status:
   - `direct`: Codex has a stable practical equivalent.
   - `approximate`: Codex can reach the same goal through a different workflow.
   - `unavailable`: Codex cannot currently implement the feature reliably.
14. If the status is `approximate`, read `references/approximate-strategies.md` and choose the narrowest fallback that still satisfies the user goal.
15. If the status is `unavailable`, confirm the reason against `references/unsupported-commands.md`.
16. Read `references/execution-policy.md` before deciding whether to stop after the mapping block and ask for confirmation.
17. Read `references/integration-playbooks.md` when the request is about MCP administration, plugin lifecycle, marketplace behavior, or another hardest integration path.
18. If the task is to maintain or extend this skill, read `references/maintenance-rules.md` before editing and run the maintenance scripts there before changing mapping rows by hand.

## Output Rules

Always present the mapping result in this order:

1. `Status`
2. `Codex mapping`
3. `Boundary`
4. `Execution path in Codex`

Additional rules:

- Start with the mapped status when the user is explicitly asking for translation or execution.
- Name the Codex mechanism clearly: skill, tool, shell workflow, local review flow, planning flow, or unavailable.
- When giving a fallback, keep it executable and short.
- If several Claude Code commands are involved, summarize the overall boundary first, then map each command.
- If the user wants a rewritten runbook, preserve the original intent but rewrite the procedure in Codex terms.
- If the user asks to perform the task now, complete the mapping block first, then ask one concise confirmation question before executing.
- If the user asks only for translation, stop after the execution path.

## Reference Navigation

- Read `references/command-mapping.md` for explicit slash commands and CLI subcommands.
- Read `references/workflow-mapping.md` for plan mode, permissions, session handling, review flow, agent delegation, MCP usage, plugins, and worktree behavior.
- Read `references/aliases-and-visibility.md` for aliases, hidden commands, and environment-specific visibility.
- Read `references/capability-boundaries.md` for structural product differences.
- Read `references/architecture-lenses.md` for mechanism-level explanations behind hardest cases.
- Read `references/settings-memory-and-hooks.md` for guidance files, settings layering, hooks, plans, and auto-memory.
- Read `references/hook-and-tool-governance.md` for hook lifecycle stages, permission mediation, continuation control, and MCP-output mutation boundaries.
- Read `references/agent-isolation-and-background.md` for agent isolation, background execution, and remote-control boundaries.
- Read `references/repo-operating-system.md` for guidance discovery, skills and agents roots, source precedence, and repo-level behavior placement.
- Read `references/registry-and-precedence.md` for ordered roots, shadowing, compatibility directories, and active-versus-shadowed definitions.
- Read `references/context-hygiene.md` for compaction layers, resume correctness, attachment restoration, and recovery before surfacing context failures.
- Read `references/mcp-runtime-and-inbound-control-plane.md` for MCP runtime identity, reconnect, auth state, admin-versus-runtime split, and inbound/channel control-plane boundaries.
- Read `references/permission-decision-ladder.md` for deny/ask ordering, dangerous-path and shell-risk gates, mode escalation, and blast-radius explanations.
- Read `references/plugin-runtime-and-lifecycle.md` for runtime extension behavior beyond marketplace commands.
- Read `references/approximate-strategies.md` for reusable fallback patterns.
- Read `references/execution-policy.md` for the map-first execution rule and transition conditions.
- Read `references/integration-playbooks.md` for MCP and plugin decision trees.
- Read `references/unsupported-commands.md` for commands and feature areas that are currently not implementable in Codex.
- Read `references/maintenance-rules.md` only when updating the skill.

## Selection Rules

### Choose `direct`

Use `direct` only when Codex can perform the same practical job without hand-waving. Different syntax is allowed; missing capability is not.

Even for `direct`, do not skip the mapping stage.

### Choose `approximate`

Use `approximate` when the Claude Code feature can be replaced by:

- an existing Codex skill
- a standard shell workflow
- a code review or planning workflow
- a delegated-agent workflow that Codex actually supports in the current environment

State the missing piece explicitly.

If the user asked to execute the task now, say what is lost before asking for confirmation.

### Choose `unavailable`

Use `unavailable` when the request depends on:

- product-owned UI or account settings
- session primitives Codex does not expose
- daemon, bridge, mobile, voice, or remote-control surfaces
- Anthropic-internal or feature-flagged behavior with no Codex equivalent

Do not soften `unavailable` into a fake workaround.

If the status is `unavailable`, do not execute. Stop after explaining the boundary and the reason.
