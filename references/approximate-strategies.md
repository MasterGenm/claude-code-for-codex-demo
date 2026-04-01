# Approximate Strategies

Use this file when the correct status is `approximate`.

## Strategy Catalog

### 1. Replace Slash Commands With A Workflow

Use when Claude Code has a dedicated command but Codex only has the underlying general capability.

Examples:

- `/clear` -> start a new thread or explicitly reset scope
- `/compact` -> write a checkpoint summary
- `/export` -> write a Markdown export file

### 2. Replace Product Surfaces With Shell And File Operations

Use when the user goal is local and reproducible.

Examples:

- `/branch` -> git commands
- `/doctor` -> shell diagnostics
- `/env` -> environment inspection

### 3. Replace Managed Review Features With A Stronger Local Review

Use when Claude Code has a managed or remote review path that Codex lacks.

Examples:

- `/ultrareview` -> deeper local review
- `/bughunter` -> local bug hunt

### 4. Replace Mode Switches With Explicit Behavioral Instructions

Use when Claude Code exposes a runtime mode toggle that Codex does not.

Examples:

- `/effort` -> vary reasoning depth in the response
- `/output-style` -> honor the requested formatting style in-line
- `/brief` -> provide a concise manual brief

### 5. Replace Agent-Specific Commands With Optional Delegation

Use only when the environment supports delegated agents and the user explicitly requests them.

Examples:

- `/fork` -> delegated subagent on explicit request
- `/agents` -> explain available delegation choices rather than pretending there is a persistent agent manager

### 6. Replace Resume-Oriented Features With Workspace Reconstruction

Use when Claude Code would restore from transcript state but Codex cannot.

Preferred sequence:

1. Read the latest plan or note file.
2. Inspect git state.
3. Summarize recovered context.
4. Continue from that checkpoint.

## Approximation Rules

- State the lost capability first.
- Keep the fallback concrete and executable.
- Do not label a manual workaround as `direct`.
- If the fallback is too lossy, downgrade to `unavailable`.
