# Architecture Lenses

Use this file when the user's request depends on Claude Code's internal runtime model rather than only a slash command name.

This file does not replace `command-mapping.md` or `workflow-mapping.md`. It explains *why* some mappings are only `approximate` or `unavailable`.

## 1. Instruction Assembly

Claude Code is not driven by a single `CLAUDE.md` file. It assembles behavior from shared guidance, personal guidance, rules, skills, hooks, and related repo artifacts.

Upstream source anchors:
- `src/commands/init.ts:28` - `/init` is an artifact-selection workflow, not just a file generator.
- `src/commands/init.ts:46` - the bootstrap flow surveys `CLAUDE.md`, `AGENTS.md`, rules, Copilot/Cursor instructions, and `.mcp.json`.
- `src/commands/init.ts:70` - personal guidance placement changes when worktrees are sibling or external rather than nested.
- `src/bootstrap/state.ts:205` - session state tracks additional directories for CLAUDE.md loading.

Mapping consequence:
- `/init` should stay `approximate`.
- Requests about "how Claude should behave in this repo" may map to guidance files, settings, hooks, or skills depending on the user's real goal.

## 2. Settings And Policy

Claude Code exposes a broad policy and settings plane, not just a single preferences file.

Upstream source anchors:
- `src/utils/settings/types.ts:407` - project MCP approvals are first-class settings.
- `src/utils/settings/types.ts:435` - hooks are part of the typed settings surface.
- `src/utils/settings/types.ts:438` - worktree behavior is policy-configurable.
- `src/utils/settings/types.ts:823` - plans can live in a configurable directory.
- `src/utils/settings/types.ts:937` - auto-memory has explicit enablement and storage settings.

Mapping consequence:
- `/config`, `/settings`, `/permissions`, and parts of `/mcp` are usually `approximate`.
- Explain concrete editable files when they exist. Do not imply Codex has a single unified settings UI.

## 3. Permission Decision Ladder

Claude Code permissions are not just a mode switch. They are an ordered ladder that combines deny and ask rules, safety checks, internal-path carve-outs, working-directory boundaries, shell structure checks, and mode-based fast paths.

Upstream source anchors:
- `src/utils/permissions/filesystem.ts:1205` - file writes enter an ordered permission ladder.
- `src/utils/permissions/filesystem.ts:1305` - safety checks run before ordinary ask and allow logic.
- `src/utils/permissions/filesystem.ts:1367` - `acceptEdits` fast paths are still scoped to allowed working directories.
- `src/tools/BashTool/bashPermissions.ts:2229` - shell deny and ask rules run before path constraints.
- `src/tools/BashTool/bashPermissions.ts:2338` - even apparently allowed shell commands must still clear injection-sensitive checks.
- `rust/crates/runtime/src/permissions.rs:89` - `claw-code` models permission as current-mode versus required-mode per tool.

Mapping consequence:
- `/permissions` remains `approximate`, because Codex can explain the current approval model but does not expose Claude Code's full ladder.
- `/sandbox` remains `unavailable`, because host sandbox control is not the same as Claude Code's internal risk ordering.

## 4. Agent Isolation And Background Execution

Claude Code agent behavior includes isolation mode, background execution, continuation, and team/task state. It is not just "spawn another agent."

Upstream source anchors:
- `src/tools/AgentTool/AgentTool.tsx:87` - subagents can run in background.
- `src/tools/AgentTool/AgentTool.tsx:99` - isolation is explicit and includes `worktree` plus gated `remote`.
- `src/skills/bundled/batch.ts:61` - batch execution requires isolated worktree agents and background execution.
- `src/bootstrap/state.ts:143` - session-created teams are tracked and cleaned up.
- `src/bootstrap/state.ts:175` - invoked skills are tracked per agent for compaction and preservation.

Mapping consequence:
- `/fork`, `/agents`, and `/tasks` should be reasoned about through isolation and background semantics.
- Codex delegation remains `approximate` because it does not expose the same persistent agent/task manager.

## 5. Memory, Plans, And Compaction Lifecycle

Claude Code session continuity is a runtime subsystem with memory compaction, plan files, checkpoint-like summaries, and cache hygiene.

Upstream source anchors:
- `src/services/compact/autoCompact.ts:287` - auto-compaction tries session-memory compaction before legacy compaction.
- `src/services/compact/autoCompact.ts:257` - auto-compaction has a circuit breaker for repeated failures.
- `src/memdir/memdir.ts:255` - memory prompts distinguish memory, plans, and task-like state rather than flattening them.
- `src/bootstrap/state.ts:167` - plan slugs are cached in session state.
- `src/bootstrap/state.ts:175` - invoked skills are tracked across compaction boundaries.
- `src/utils/settings/types.ts:823` - plan storage location is configurable.
- `src/utils/settings/types.ts:943` - auto-memory storage is configurable and security-sensitive.

Mapping consequence:
- `/compact`, `/resume`, and `/rewind` are more than "write a summary."
- Keep them `approximate`, and explain what Codex lacks: transcript primitives, session memory layers, and automatic compaction behavior.

## 6. MCP Runtime, Administration, And Inbound Control

Claude Code splits MCP into at least three layers:
- runtime use of tools/resources
- administration of server config
- inbound runtime surfaces such as channel notifications

Upstream source anchors:
- `src/services/mcp/client.ts:2173` - runtime discovery fetches tools, commands, skills, and resources together.
- `src/services/mcp/channelNotification.ts:176` - inbound channel registration is gated in a strict order.
- `src/utils/settings/types.ts:407` - `.mcp.json` approvals are persisted settings.
- `src/utils/settings/types.ts:895` - org policy can opt in to channel notifications separately.

Mapping consequence:
- Keep "use MCP tools" separate from "manage MCP servers."
- Keep both separate from inbound/channel control-plane behavior.
- Hardest MCP cases should also read `mcp-runtime-and-inbound-control-plane.md`.

## 7. Remote And Bridge Control Planes

Claude Code has distinct remote, bridge, and session-attachment surfaces. These are not just shell commands with different names.

Upstream source anchors:
- `src/commands.ts:619` - command safety is separated for remote and bridge surfaces.
- `src/bootstrap/state.ts:197` - remote mode is tracked in session state.
- `src/bootstrap/state.ts:207` - allowed channel servers are tracked separately from normal MCP usage.

Mapping consequence:
- `/session`, `claude remote-control`, `/remote-control`, mobile pairing, daemon flows, and bridge attachment should remain `unavailable` unless the current Codex host explicitly exposes them.
- Explain that these are missing transport/control planes, not merely missing command aliases.

## How To Use These Lenses

- If the user asks "why is this only approximate?", start here before extending the command table.
- If the request touches repo setup, hooks, memory, or settings, also read `settings-memory-and-hooks.md`.
- If the request touches tool-event hooks, permission mediation through hooks, continuation control, or MCP-output mutation, also read `hook-and-tool-governance.md`.
- If the request touches approval prompts, deny and ask ordering, shell safety gates, working-directory boundaries, or blast-radius questions, also read `permission-decision-ladder.md`.
- If the request touches subagents, background tasks, worktrees, or remote-control, also read `agent-isolation-and-background.md`.
- If the request is really about where repo behavior lives, how guidance is discovered, or how skills and agents shadow each other, also read `repo-operating-system.md`.
- If the request is specifically about source order, active versus shadowed definitions, legacy compatibility directories, or where a skill or agent should be placed, also read `registry-and-precedence.md`.
- If the request is specifically about `/compact`, `/resume`, `/rewind`, context pressure, attachment restoration, or recovery after prompt-length errors, also read `context-hygiene.md`.
- If the request is specifically about MCP runtime identity, resource discovery, auth, reconnect, or server-pushed channel behavior, also read `mcp-runtime-and-inbound-control-plane.md`.
- If the request is really about plugin or extension behavior beyond marketplace commands, also read `plugin-runtime-and-lifecycle.md`.
