# Workflow Mapping

Use this file when the user is asking about Claude Code behavior rather than a single command name.

## Map-First Execution Rule

| Claude Code Workflow | Codex Status | Codex Mechanism | How To Operate In Codex | Boundary |
| --- | --- | --- | --- | --- |
| Ask Codex to do a Claude-like task immediately | direct or approximate | Mapping block first, then the relevant Codex workflow | State `Status`, `Codex mapping`, `Boundary`, and `Execution path in Codex` before acting | Translation does not imply parity, and execution must follow the mapped status rules |

Rules:

- Do not execute before the mapping decision is visible.
- If the user asked only for translation, stop after the execution path.
- If the user asked to perform the task now, stop after the mapping block and ask for confirmation.
- Continue only after explicit post-mapping confirmation and only if `execution-policy.md` allows it.

## Plan Mode

| Claude Code Workflow | Codex Status | Codex Mechanism | How To Operate In Codex | Boundary |
| --- | --- | --- | --- | --- |
| Enter plan mode, maintain a live plan, then execute | approximate | Planning workflow plus plan docs | Build a plan, keep steps current, and store plan docs under `docs/plans/` when useful | Codex can follow the workflow but does not expose Claude's session-level plan-mode primitive |

Preferred pattern:

1. Clarify the task.
2. Produce a plan with explicit steps.
3. Save a durable plan file when the task is large.
4. Execute the plan and update the user as work progresses.

## Permissions And Sandboxing

| Claude Code Workflow | Codex Status | Codex Mechanism | How To Operate In Codex | Boundary |
| --- | --- | --- | --- | --- |
| Switch permission modes or inspect permission prompts | approximate | Explain current host approval model | State what the environment allows, what needs approval, and how execution will proceed | Permission policy is host-configured, not usually changed by a skill |

Rules:

- Do not promise that Codex can switch permission mode on command.
- Explain when a requested operation is blocked by the current environment.
- If approval is required by the host, present the action clearly and minimally.

For the deeper runtime model behind deny and ask ordering, dangerous-path checks, shell safety gates, and mode escalation, also read `permission-decision-ladder.md`.

## Session Resume And Continuation

| Claude Code Workflow | Codex Status | Codex Mechanism | How To Operate In Codex | Boundary |
| --- | --- | --- | --- | --- |
| Resume a previous transcript-backed session | approximate | Rebuild context from files, plans, notes, and git state | Reconstruct the working state manually and continue | No Claude-style transcript resume primitive is guaranteed |

Preferred pattern:

1. Read the latest plan or notes file.
2. Inspect git status and changed files.
3. Re-state the recovered context.
4. Continue from the recovered checkpoint.

For the deeper runtime model behind compaction, preserved context, and resume correctness, also read `context-hygiene.md`.

## Review Flow

| Claude Code Workflow | Codex Status | Codex Mechanism | How To Operate In Codex | Boundary |
| --- | --- | --- | --- | --- |
| Local review or PR review | direct | Codex review mode | Inspect diffs and produce findings-first review output | Same practical outcome, different UI |
| Deep cloud review (`ultrareview`) | approximate | Stronger local review | Do a deeper local review and say remote review is not available | Remote Claude-on-the-web path is absent |

## Agent And Delegation Flow

| Claude Code Workflow | Codex Status | Codex Mechanism | How To Operate In Codex | Boundary |
| --- | --- | --- | --- | --- |
| Spawn subagents for parallel work | approximate | Delegated agents only when explicitly requested | Use delegated agents only with explicit user permission and a scoped subtask | Codex delegation is not a generic always-on agent swarm |
| Team, peers, buddy, mailbox workflows | unavailable | None | None | No equivalent peer messaging or swarm mailbox surface |

Rules:

- Do not spawn agents just because Claude Code would.
- Require explicit user permission for delegation.
- Keep the main task on the main thread unless a subtask is clearly parallelizable.
- Even when delegation is allowed, state the mapping first.

## MCP Workflow

| Claude Code Workflow | Codex Status | Codex Mechanism | How To Operate In Codex | Boundary |
| --- | --- | --- | --- | --- |
| Use MCP tools and resources | approximate | Use whatever MCP tools/resources the environment already exposes | Consume resources and tools directly, but separate runtime use from server administration and inbound notification expectations | Server lifecycle, auth/reconnect behavior, and inbound notification control may not match Claude Code |
| Add or remove MCP servers through slash or CLI flows | unavailable or approximate | Environment-specific | Only edit config files or use host tooling if explicitly available | No universal Codex-side MCP management command |

For the deeper runtime difference between runtime use, server administration, and channel-style inbound control, also read `mcp-runtime-and-inbound-control-plane.md`.

## Plugin Versus Skill Workflow

| Claude Code Workflow | Codex Status | Codex Mechanism | How To Operate In Codex | Boundary |
| --- | --- | --- | --- | --- |
| Install or manage Claude plugins | approximate | Codex skills and plugins where available | Translate the user goal into a skill or plugin operation | Plugin architecture is not equivalent |

Rules:

- If the user wants reusable Codex behavior, prefer a skill.
- If the user wants packaging or marketplace mechanics, explain the mismatch.

## Worktree And Branch Workflow

| Claude Code Workflow | Codex Status | Codex Mechanism | How To Operate In Codex | Boundary |
| --- | --- | --- | --- | --- |
| Enter worktree mode | approximate | Manual git worktree commands | Use git worktree directly when needed | No dedicated worktree mode command |
| Branch inspection and switching | direct | Git shell workflow | Use git commands and summarize the result | Same practical effect |

## Export And Checkpoint Workflow

| Claude Code Workflow | Codex Status | Codex Mechanism | How To Operate In Codex | Boundary |
| --- | --- | --- | --- | --- |
| Export a conversation, checkpoint a state, compact a long session | approximate | Write summary docs or checkpoint files | Persist the relevant state to Markdown files in the workspace | No direct transcript-export or compact primitives |

For the runtime difference between a simple checkpoint file and Claude Code's hygiene pipeline, also read `context-hygiene.md`.
