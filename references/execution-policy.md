# Execution Policy

Use this file after the mapping decision is made.

## Core Rule

This skill is `map first, confirm, execute`.

That means:

1. identify the Claude Code command or workflow
2. classify it as `direct`, `approximate`, or `unavailable`
3. state the boundary
4. ask for explicit confirmation if execution is still possible
5. only then perform the task

Do not skip step 2 or 3 just because the user clearly wants action.
Do not treat the user's initial "do it now" phrasing as post-mapping confirmation.

## Transition Rules

### If the user asked only for translation

- Stop after giving the execution path.
- Do not run tools or shell commands.

### If the user asked to perform the task now

- Still present the mapping block first.
- Then stop and ask one concise confirmation question.

### If the user explicitly confirms after seeing the mapping

- Continue only if the mapped path is allowed by the status rules below.

## Status Rules

### `direct`

- Mapping is required.
- Execution may proceed only after explicit post-mapping confirmation.
- Use the mapped Codex mechanism directly.

Examples:

- `/help` -> available-tools summary
- `/doctor` -> local diagnostics
- `/skills` -> Codex skill listing

### `approximate`

- Mapping is required.
- State the lost capability before proposing action.
- Execution may proceed only after explicit post-mapping confirmation and only if the approximation still satisfies the practical goal.
- If the approximation is too lossy, stop and treat it as effectively unavailable.

Examples:

- `/diff` -> git diff review with loss of per-turn diffs
- `/plan` -> planning workflow plus plan docs
- `/compact` -> write a checkpoint summary
- `/resume` -> reconstruct context from plans, notes, and git state
- `/plugin install` -> use the closest Codex skill or plugin workflow

### `unavailable`

- Mapping is required.
- Execution must not proceed.
- Explain why the capability is unavailable in the current Codex environment.

Examples:

- `/remote-control-server`
- `/voice`
- `claude server`
- `claude auth login`

## Execution Path Language

When describing the execution path, say which Codex mechanism would be used:

- skill
- shell workflow
- repo inspection
- review workflow
- planning workflow
- delegated agent workflow
- unavailable

Keep the path concrete enough that Codex can act on it in the next turn once the user confirms.

## Anti-Patterns

Do not:

- treat mapping and execution as the same step
- treat the user's initial request to execute as confirmation
- auto-run a fallback without first stating it is only approximate
- continue after an `unavailable` result
- imply that a host-owned UI or account operation can be simulated locally when it cannot
