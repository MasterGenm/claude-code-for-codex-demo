# Plugin Runtime And Lifecycle

Use this file when the request touches `/plugin`, marketplace behavior, plugin install or update flows, hook aggregation, plugin-provided tools, or extension lifecycle.

## What `claw-code` Makes Explicit

`claw-code` treats plugins as a runtime extension plane, not just a marketplace object.

High-value source anchors:
- `rust/crates/plugins/src/lib.rs:685` - enabled plugins aggregate hooks after validation.
- `rust/crates/plugins/src/lib.rs:695` - enabled plugins aggregate tools with collision checks.
- `rust/crates/plugins/src/lib.rs:716` - plugin initialization is an explicit runtime phase.
- `rust/crates/plugins/src/lib.rs:978` - install is a real staged source materialization flow.
- `rust/crates/plugins/src/lib.rs:1021` - enable and disable are persisted state changes, not just UI toggles.
- `rust/crates/plugins/src/lib.rs:1059` - update is a real lifecycle flow, not just "refresh metadata."
- `rust/crates/plugins/src/lib.rs:1801` - lifecycle commands run as executable init and shutdown phases.
- `rust/crates/claw-cli/src/main.rs:352` - the runtime assembles plugin tools before building the global tool registry.
- `rust/crates/claw-cli/src/main.rs:2794` - plugin-derived feature config is injected into the conversation runtime.
- `rust/crates/runtime/src/conversation.rs:143` - hooks are part of the conversation loop through `HookRunner`.

## The Real Control Plane

A plugin system like this can change the runtime in at least five ways:

1. Add tools
2. Add hooks
3. Add lifecycle commands
4. Persist enabled or disabled state
5. Affect runtime feature composition before the conversation loop starts

This is deeper than a plain "install package" story.

## Why This Matters For Our Skill

Our current skill already says Claude plugins are only `approximate` in Codex, which is correct.

What was under-explained is *why*:
- Claude-style plugins can contribute runtime hooks and tools
- plugin enablement changes the assembled runtime surface
- lifecycle commands can run outside a one-off user request

So a good translation must distinguish:
- reusable behavior that is really just a skill
- runtime extension that needs a plugin package
- marketplace mechanics that are product-specific and may remain unavailable

## Mapping Guidance

### `claude plugin install`

Do not reduce this to "use a skill" without checking the user's real goal.

Ask which of these they want:
- reusable prompt/procedure -> skill
- runtime extension with tools/hooks/lifecycle -> plugin package if supported
- one-off capability -> normal Codex workflow, no plugin needed

### `claude plugin enable` / `disable` / `update` / `uninstall`

Map to the real underlying artifact:
- skill files
- plugin package
- local metadata

Do not pretend there is guaranteed marketplace parity.

### Hard Boundary

If the request assumes:
- hosted marketplace parity
- product-owned plugin verification surfaces
- exactly matching plugin hook semantics

keep the result `approximate` or `unavailable` as appropriate.

## What Codex Should Learn

The important Claude Code lesson is that extensions are not only distribution objects. They are runtime control-plane inputs.

That means Codex should learn to reason about extensions through:
- aggregation
- precedence
- lifecycle
- runtime assembly

not only through "installed or not installed."
