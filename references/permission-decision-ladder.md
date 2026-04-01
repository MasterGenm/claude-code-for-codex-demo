# Permission Decision Ladder

Use this file when the request is really about `/permissions`, `/sandbox`, danger level, approval prompts, read-only versus write behavior, or why Claude Code asks for permission when a command looks superficially harmless.

This is not just a settings question. It is a runtime risk-ordering question.

## What Claude Code Is Actually Doing

Claude Code permissions are not a single "mode toggle". They are an ordered ladder that combines:

- rule-based deny and ask decisions
- internal-path carve-outs
- dangerous-file and dangerous-command safety gates
- working-directory boundaries
- tool-specific read-only allowlists
- shell misparse and command-injection checks
- mode-based fast paths
- explicit allow rules
- classifier or prompt escalation for the remaining cases

That is why many Claude Code permission requests should stay `approximate` in Codex even when the user sees a seemingly similar permission surface.

## Source Anchors

Reverse-engineered Claude Code mirror:
- `src/utils/permissions/filesystem.ts:1205` - file writes go through an ordered permission ladder, not a flat mode check.
- `src/utils/permissions/filesystem.ts:1223` - deny rules run before all later write checks.
- `src/utils/permissions/filesystem.ts:1244` - internal writable paths are carved out before dangerous-path checks.
- `src/utils/permissions/filesystem.ts:1262` - `.claude/**` session-scoped allow rules are checked before general safety blocks.
- `src/utils/permissions/filesystem.ts:1305` - safety checks run before ask rules, mode fast paths, and ordinary allow rules.
- `src/utils/permissions/filesystem.ts:1367` - `acceptEdits` only auto-allows writes inside allowed working directories.
- `src/tools/BashTool/bashPermissions.ts:1073` - shell-mode validation is part of permission evaluation, not a separate afterthought.
- `src/tools/BashTool/bashPermissions.ts:2229` - bash deny and ask rules must run before path checks to avoid bypasses.
- `src/tools/BashTool/bashPermissions.ts:2248` - one denied subcommand denies the whole compound command.
- `src/tools/BashTool/bashPermissions.ts:2338` - even when subcommands look allowed, command-injection checks can still block auto-allow.
- `src/tools/BashTool/bashSecurity.ts:2109` - quoted-newline checks are treated as misparsing-sensitive safety checks.
- `src/tools/BashTool/bashSecurity.ts:2392` - non-misparsing asks are deferred so parser-differential checks still win.
- `src/utils/shell/readOnlyCommandValidation.ts:104` - read-only shell behavior is backed by explicit allowlists, not a vague "safe command" heuristic.
- `src/utils/shell/readOnlyCommandValidation.ts:1562` - UNC-path detection is part of permission and exfiltration defense.

`claw-code` clean-room runtime:
- `rust/crates/runtime/src/permissions.rs:89` - authorization is modeled as current mode versus required mode per tool.
- `rust/crates/runtime/src/permissions.rs:108` - some escalations prompt instead of silently denying or allowing.
- `rust/crates/tools/src/lib.rs:165` - tool registries expose required permissions explicitly.
- `rust/crates/tools/src/lib.rs:219` - built-in tools are typed as read-only, workspace-write, or danger-full-access rather than inferred ad hoc.

## 1. File Permission Ladder

For file reads and writes, the real order matters more than the mode name.

### Write Path

The write ladder is effectively:

1. deny rules
2. internal editable-path carve-outs
3. narrow `.claude/**` session allow rules
4. safety checks for dangerous files, dangerous directories, suspicious Windows path tricks, and UNC-like cases
5. ask rules
6. mode fast path such as `acceptEdits`, but only inside allowed working directories
7. explicit allow rules
8. working-directory prompt with suggestions

Why this matters:
- a broad allow is not the first thing Claude Code looks at
- dangerous config paths are intentionally protected before normal allow logic
- internal plan, scratchpad, memory, and agent paths are treated as first-class runtime carve-outs

### Read Path

The read ladder is similar but narrower:

1. deny rules
2. readable internal paths
3. allow rules
4. working-directory fast path
5. outside-working-directory prompt with `Read(...)` suggestions

Why this matters:
- "read-only" does not mean "everything readable everywhere"
- Claude Code still scopes reads by working directory and special internal stores

## 2. Shell Permission Ladder

Shell execution adds a second ladder on top of the general permission model.

The shell path is effectively:

1. exact or prefix rule checks
2. deny and ask rules before path constraints
3. compound-command guards such as multi-`cd` clarity checks and `cd && git` attack prevention
4. path and redirection validation on the original command
5. mode validation
6. subcommand merge and exact-match allow checks
7. command-injection and parser-differential safety checks
8. classifier handoff or explicit prompt for the remaining unresolved case

Why this matters:
- a command can be "allowed by rule" and still blocked by structural safety checks
- broad shell permission is a blast-radius decision, not just a convenience toggle
- read-only shell behavior depends on explicit safe-command tables and flag validation, not on command names alone

## 3. Safety And Misparse Ladder

Not every `ask` means the same thing.

Claude Code distinguishes at least two families:

- ordinary asks
  Example: working-directory prompts, explicit ask rules, config-boundary prompts
- misparse-sensitive or injection-sensitive asks
  Example: quoted-newline tricks, comment-quote desync, dangerous substitutions, malformed token injection

This distinction matters because misparse-sensitive asks are designed to survive later shortcut logic. They are not normal "maybe allow" prompts.

Operational consequence:
- when translating Claude Code permission behavior into Codex, do not describe every approval as a generic mode prompt
- some permission prompts are really safety-circuit behavior

## 4. Blast Radius And Mode Semantics

Modes are coarse envelopes, not the whole policy.

`claw-code` makes this explicit with:
- `read-only`
- `workspace-write`
- `danger-full-access`
- plus prompt-oriented escalation

The fuller Claude Code mirror shows why this still is not enough on its own:
- rule source matters
- path category matters
- shell structure matters
- safety validators matter
- working-directory scope matters

So the right mental model is:

- mode says how much power *might* be available
- the ladder decides whether a specific action actually gets that power

## 5. Mapping Guidance

### `/permissions`

Keep `approximate`.

Use this lens to explain:
- what the current Codex host approval model is
- which parts are host-owned
- that Claude Code internally has a finer ladder than a single slash command suggests

### `/sandbox`

Keep `unavailable`.

Reason:
- sandbox toggling is host-owned in Codex
- Claude Code's internal ladder still does not imply a portable skill-level sandbox switch

### `/config` And `/settings`

Keep `approximate`.

Reason:
- config edits may touch permission defaults or trust choices
- but Codex should only edit real config artifacts that actually exist

### "Why Did Claude Ask?"

Use this reference before replying.

The right answer often depends on:
- a dangerous path
- a working-directory boundary
- a shell-structure guard
- a misparse-sensitive validator
- or a mode escalation from workspace-write to danger-full-access

## What Codex Should Learn

The durable Claude Code lesson is not "more permission commands". It is a better risk-ordering habit:

- deny before convenience
- special internal paths before broad folder grants
- safety before allow
- structure-aware shell checks before fast paths
- blast radius before UI wording

That is the part worth distilling into Codex as an operating skill.
