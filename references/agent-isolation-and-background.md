# Agent Isolation And Background Execution

Use this file when the request touches `/fork`, `/agents`, `/tasks`, worktree mode, background execution, or bridge-style remote delegation.

## What Claude Code Is Actually Doing

Claude Code agent behavior includes:
- explicit isolation modes
- background execution
- persistent task or team state
- cleanup semantics
- continuation versus spawn decisions

Upstream source anchors:
- `src/tools/AgentTool/AgentTool.tsx:87` - background execution is an explicit parameter.
- `src/tools/AgentTool/AgentTool.tsx:99` - isolation is explicit and includes `worktree`, with gated `remote`.
- `src/skills/bundled/batch.ts:61` - large parallel work is expected to use isolated background worktrees.
- `src/bootstrap/state.ts:136` - session-only cron tasks and other background task state are tracked.
- `src/bootstrap/state.ts:143` - session-created teams are tracked for cleanup.
- `src/commands.ts:619` - remote-safe and bridge-safe command subsets exist as a separate safety model.

## Mapping Guidance

### `/fork`

Keep `approximate`.

Codex consequence:
- only delegate when the user explicitly asks
- keep the subtask narrow and bounded
- do not imply a persistent fork UI or background-task manager

### `/agents`

Keep `approximate`.

Codex consequence:
- explain available delegation roles and boundaries
- do not claim there is a full persistent agent registry or configuration UI

### `/tasks`

Keep `approximate`.

Codex consequence:
- summarize visible delegated agents or long-running operations when possible
- do not imply parity with Claude Code's task/session registry

### Remote Or Bridge Surfaces

Keep `unavailable` unless the current host truly exposes them.

Codex consequence:
- `claude remote-control`, `/remote-control`, `/session`, mobile pairing, daemon attach flows, and bridge attach remain unavailable by default
- explain that the missing piece is a transport/control plane, not just a command spelling

## Decision Rules

- If the user wants parallel work now, use normal Codex delegation rules plus explicit permission.
- If the user wants a persistent background manager, stay conservative and explain the gap.
- If the user wants true worktree isolation, use real git worktree operations only when they are necessary and explicit.
- If the request assumes remote attachment or bridge-safe command routing, mark it unavailable unless the environment proves otherwise.
