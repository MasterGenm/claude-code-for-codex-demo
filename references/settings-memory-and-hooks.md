# Settings, Memory, And Hooks

Use this file when the request involves `/init`, `/memory`, `/hooks`, `/config`, `CLAUDE.md`, `CLAUDE.local.md`, settings layering, plans, or auto-memory.

## What Claude Code Is Actually Doing

Claude Code treats repo guidance, local preferences, settings, hooks, and memory as different artifact types.

For runtime hook semantics inside the tool loop, also read `hook-and-tool-governance.md`. This file is mainly about artifact choice and settings layering.

Upstream source anchors:
- `src/commands/init.ts:28` - `/init` chooses among project guidance, personal guidance, skills, and hooks.
- `src/commands/init.ts:70` - worktree layout affects where personal guidance should live.
- `src/utils/settings/types.ts:435` - hooks are part of typed settings, not ad hoc shell snippets.
- `src/utils/settings/types.ts:823` - plans directory is configurable.
- `src/utils/settings/types.ts:943` - auto-memory directory is configurable and partially scope-restricted.
- `src/skills/bundled/updateConfig.ts:15` - settings locations have explicit layering.
- `src/skills/bundled/updateConfig.ts:135` - hook events, hook types, and matcher structure are treated as a real schema.
- `src/skills/bundled/updateConfig.ts:269` - hook setup includes verification steps and watcher caveats.
- `src/memdir/memdir.ts:255` - memory prompts explicitly distinguish memory from plans and tasks.

## Artifact Choice

When translating a Claude Code request, decide which artifact the user actually wants.

### Guidance File

Use for:
- repo instructions
- coding conventions
- durable workflow notes
- shared or personal operating guidance

Typical Codex translation:
- project instructions -> `CLAUDE.md`, `AGENTS.md`, or another repo guidance file
- personal instructions -> local-only file or home-level Codex guidance file

### Settings Edit

Use for:
- explicit config keys
- permission rules
- MCP approvals
- worktree behavior
- persistent output or runtime defaults

Typical Codex translation:
- edit a concrete settings file only when the environment actually exposes one
- otherwise stop at translation and explain the missing host surface

### Hook Or Automation Config

Use for:
- deterministic automation on tool events
- formatting after edits
- tests after changes
- pre/post-compact behavior

Typical Codex translation:
- explain the real config file and event structure if present
- do not pretend Codex has a universal `/hooks` UI

### Memory Or Plan Artifact

Use for:
- checkpoint summaries
- durable plan files
- persistent project context
- manual continuity across sessions

Typical Codex translation:
- write explicit Markdown artifacts in the workspace
- keep `/compact` and `/resume` as `approximate`, because Codex does not expose Claude's transcript memory manager

## Layering Rules

Claude Code distinguishes shared, personal, and local-private state.

Operational translation:
- shared team guidance -> repo-tracked docs
- personal preferences -> local or home-level untracked guidance
- runtime settings -> concrete config file if available
- enforced automation -> hooks or local automation config

Do not collapse these into "just edit CLAUDE.md" unless the user's goal is genuinely guidance-only.

Special case:
- nested worktrees can often inherit the main repo's personal guidance naturally
- sibling or external worktrees may need a home-level personal file plus thin local stubs instead of duplicating private instructions everywhere

## Mapping Guidance

### `/init`

Keep `approximate`.

Why:
- upstream `/init` is interactive and artifact-aware
- Codex can inspect the repo and create guidance artifacts, but not through the same integrated bootstrap surface

### `/memory`

Keep `approximate`.

Why:
- Claude Code has a dedicated memory-management idea
- Codex usually substitutes workspace guidance files, plan docs, or local notes

### `/hooks`

Keep `approximate`.

Why:
- Claude Code has typed hook events and a real verification flow
- Codex usually only has file-level inspection or manual config edits

### `/config` or `/settings`

Keep `approximate`.

Why:
- Codex can edit a real config file when one exists
- it should not claim a single unified settings command surface

## Failure Modes To Avoid

- Treating hooks as mere prose notes when the user asked for enforced automation
- Treating memory as only `CLAUDE.md`
- Treating personal and shared guidance as the same thing
- Treating plans as generic notes instead of explicit continuity artifacts
- Editing non-existent config files just to simulate parity
