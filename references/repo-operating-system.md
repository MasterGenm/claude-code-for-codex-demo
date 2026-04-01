# Repo Operating System

Use this file when the request is really about how Claude-style guidance, settings, skills, agents, and local definitions are discovered and composed inside a repo.

This is not just a command question. It is a control-plane question about where behavior comes from.

For the exact ordering model, shadowing rules, and compatibility roots, also read `registry-and-precedence.md`. This file stays at the operating-system level.

## What `claw-code` Makes Explicit

`claw-code` turns Claude-style behavior into a portable repo operating layer rather than a single product shell.

High-value source anchors:
- `rust/crates/runtime/src/prompt.rs:192` - instruction files are discovered across the ancestor chain, not just in one fixed file.
- `rust/crates/runtime/src/prompt.rs:404` - system prompt assembly loads project context plus runtime config before each session.
- `rust/crates/runtime/src/config.rs:173` - settings discovery is explicitly layered across user, project, and local files.
- `rust/crates/commands/src/lib.rs:686` - agent definition roots are discovered across project and user scopes.
- `rust/crates/commands/src/lib.rs:727` - skills roots include both modern skills directories and legacy commands directories.
- `rust/crates/commands/src/lib.rs:829` - agent discovery tracks shadowing precedence instead of blindly merging.
- `rust/crates/commands/src/lib.rs:872` - skill discovery also tracks shadowing and source origin.

## The Real Control Plane

The repo operating system has at least five layers:

1. Guidance files
   Examples: `CLAW.md`, `CLAW.local.md`, `.claw/CLAW.md`, `.claw/instructions.md`

2. Settings files
   Examples: user config, project config, local overrides

3. Skill definitions
   Examples: `.codex/skills`, `.claw/skills`, legacy commands directories

4. Agent definitions
   Examples: `.codex/agents`, `.claw/agents`

5. Runtime composition
   The final prompt and available affordances are assembled from the layers above.

## Why This Matters For Our Skill

Without this lens, it is easy to flatten requests into:
- "just edit CLAUDE.md"
- "just use /skills"
- "just map plugins to skills"

That misses the actual operating logic:
- repo and user scopes coexist
- later sources can override earlier ones
- skills and agents are discoverable definitions, not only hardcoded product features
- legacy command directories can still act like a compatibility layer

## Mapping Guidance

### Requests About Repo Guidance

If the user is really asking "where should this behavior live?", answer in terms of artifact choice:
- shared repo behavior -> tracked repo guidance or project settings
- personal behavior -> local or home-level guidance
- reusable capability -> skill or agent definition
- deterministic automation -> hook or runtime config

### Requests About `/skills` And `/agents`

Do not treat them as only UI listings.

Use this lens to explain:
- discovery roots
- project versus user precedence
- shadowing behavior
- why a Codex host can support similar ideas even if the UI differs

### Requests About Migration To Codex

This is one of the strongest reasons **not** to split the main translator too early.

The main skill should still answer:
- `direct`
- `approximate`
- `unavailable`

But the repo operating system lens explains *why* a request lands in one of those buckets.

## What Codex Should Learn

The most valuable Claude Code lesson here is not a slash command. It is the habit of treating repo behavior as a layered operating system:
- guidance
- settings
- skills
- agents
- runtime assembly

That is a reusable operating model worth teaching Codex across projects.
