# Registry And Precedence

Use this file when the request is really about where Claude-style behavior is discovered from, which definition wins, or why two similarly named artifacts do not merge.

This file is about ordered registries, compatibility roots, provenance, and shadowing.

## What Claude Code Is Actually Doing

Claude Code does not discover behavior through one naive directory scan.

It has several ordered registries:
- instruction files
- settings files
- skills
- agents
- compatibility roots such as legacy commands directories

High-value source anchors:
- `rust/crates/runtime/src/prompt.rs:192` - instruction files are discovered across the ancestor chain.
- `rust/crates/runtime/src/prompt.rs:204` - `CLAW.md`, `CLAW.local.md`, `.claw/CLAW.md`, and `.claw/instructions.md` are all considered.
- `rust/crates/runtime/src/prompt.rs:326` - instruction files are deduplicated rather than blindly repeated.
- `rust/crates/runtime/src/config.rs:197` - settings discovery is explicit, ordered, and source-labelled.
- `rust/crates/runtime/src/config.rs:204` - user settings are loaded before project and local layers.
- `rust/crates/runtime/src/config.rs:220` - local settings are a distinct top-most override layer.
- `rust/crates/commands/src/lib.rs:686` - agent roots are discovered across project and user scopes.
- `rust/crates/commands/src/lib.rs:727` - skill roots include both modern skills directories and legacy commands directories.
- `rust/crates/commands/src/lib.rs:829` - agents are tracked as active or shadowed by source precedence.
- `rust/crates/commands/src/lib.rs:872` - skills are also tracked as active or shadowed, with origin preserved.
- `src/skills/loadSkillsDir.ts:68` - the original TypeScript system distinguishes `skills`, legacy `commands_DEPRECATED`, `plugin`, `managed`, `bundled`, and `mcp` sources.
- `src/skills/loadSkillsDir.ts:78` - source-specific skill paths are explicit rather than inferred ad hoc.
- `src/skills/loadSkillsDir.ts:726` - the original system deduplicates skill files by resolved identity with first-wins behavior.
- `src/skills/loadSkillsDir.ts:799` - loaded skill counts are tracked by source class rather than flattened into one bag.

## The Real Registry Model

### 1. Guidance Discovery Is Layered

Instruction discovery is ordered by ancestor path and file kind.

That means:
- the repo root can contribute guidance
- nested directories can contribute more specific guidance
- local and scoped instruction files can coexist
- duplicates should be deduplicated, not echoed into the prompt repeatedly

### 2. Settings Are A Source-Labelled Stack

Settings are not one JSON blob.

They have at least these layers:
- user
- project
- local

Operational consequence:
- later layers can override earlier ones
- provenance matters
- "where should I edit this?" is a control-plane question, not a cosmetic preference

### 3. Skills And Agents Come From Ordered Roots

The `claw-code` model makes the order explicit:
- project `.codex`
- project `.claw`
- user `$CODEX_HOME`
- user `~/.codex`
- user `~/.claw`

For skills, compatibility roots also include:
- modern `skills/`
- legacy `commands/`

This means a definition is not just "present" or "missing." It is present at a source with priority.

### 4. First-Wins Shadowing

When two skills or agents share the same effective name:
- the earlier source wins
- the later source is still visible as shadowed provenance
- they do not silently merge

This is one of the most important Claude Code lessons.

The user-facing consequence is:
- "why isn't my skill showing up?" may really mean "it exists, but is shadowed"
- "where should I put this?" depends on whether the behavior should override project, personal, or compatibility definitions

### 5. Compatibility Roots Are Real Inputs

Legacy command directories are not historical trivia.

They still matter because they:
- preserve older workflow packaging
- provide migration continuity
- participate in discovery and naming conflicts

Codex should learn that compatibility roots are part of the real runtime surface, not just stale files.

## Mapping Guidance

### `/skills`

Keep `direct`, but explain the registry model when needed.

Translation consequence:
- Codex can use skills directly
- the deeper explanation is about discovery roots, precedence, and shadowing

### `/agents`

Keep `approximate`.

Translation consequence:
- explain available delegation roles
- also explain that Claude-style agent definitions live in ordered registries with source precedence

### `/init`

Keep `approximate`.

Translation consequence:
- deciding where a new behavior should live is often a registry question:
  - shared repo guidance
  - local guidance
  - skill
  - agent
  - settings override

### Plugin And Extension Questions

Registry logic also affects plugin and skill packaging questions.

Translation consequence:
- installation is not the same as activation
- activation is not the same as winning precedence
- compatibility directories and local overrides can affect the visible runtime surface

## What Codex Should Learn

The useful Claude Code lesson is:
- behavior lives in registries
- registries have ordered roots
- roots have provenance
- precedence is explicit
- duplicates are shadowed, not magically merged

That operating logic is worth learning across projects because it improves:
- artifact placement decisions
- migration explanations
- debugging of "why did this instruction or skill not apply?"
- trustworthy explanations of repo-level behavior
