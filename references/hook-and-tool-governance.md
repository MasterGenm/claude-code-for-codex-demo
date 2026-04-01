# Hook And Tool Governance

Use this file when the request touches `/hooks`, tool-event automation, permission mediation, continuation control, MCP-output mutation, or plugin-provided runtime governance.

## What Claude Code Is Actually Doing

Claude Code hooks are not just config entries or shell snippets. They are a governance layer inside the tool runtime.

They can:
- inspect or rewrite tool input
- influence permission flow
- inject additional context into the transcript
- stop continuation after a tool call
- mutate MCP tool output through a separate path
- surface warnings or failures without always crashing the turn

High-value source anchors:
- `src/services/tools/toolHooks.ts:39` - `PostToolUse` hooks are a first-class execution stage.
- `src/services/tools/toolHooks.ts:193` - `PostToolUseFailure` hooks have a separate failure path.
- `src/services/tools/toolHooks.ts:322` - hook `allow` does not bypass the base settings and permission rules.
- `src/services/tools/toolHooks.ts:435` - `PreToolUse` hooks can emit permission results, updated input, and additional context.
- `src/services/tools/toolExecution.ts:800` - pre-tool hooks run before final permission resolution.
- `src/services/tools/toolExecution.ts:979` - hook-driven permission decisions become explicit transcript events.
- `src/services/tools/toolExecution.ts:1073` - `PermissionDenied` hooks can advise retry after denial.
- `src/services/tools/toolExecution.ts:1397` - post-tool hooks run after successful execution and can stop continuation.
- `rust/crates/runtime/src/conversation.rs:143` - the hook runner is part of the core conversation runtime.
- `rust/crates/runtime/src/conversation.rs:211` - pre hooks can deny before execution.
- `rust/crates/runtime/src/conversation.rs:230` - post hooks can modify the final tool-result path.
- `rust/crates/plugins/src/hooks.rs:66` - plugin hooks expose explicit pre-tool execution.
- `rust/crates/plugins/src/hooks.rs:78` - plugin hooks expose explicit post-tool execution.
- `rust/crates/plugins/src/hooks.rs:95` - hook commands run through a structured payload instead of raw free text.
- `rust/crates/plugins/src/hooks.rs:183` - hook exit status maps to allow, deny, or warn behavior.
- `rust/crates/plugins/src/lib.rs:685` - enabled plugins aggregate hooks into the runtime control plane.

## Governance Stages

### 1. Pre-Tool Governance

This stage can:
- inspect the requested tool call
- rewrite input
- return allow, ask, or deny signals
- add extra context before execution

The critical invariant is:
- hook `allow` is not absolute allow
- base permission policy still decides whether the tool is truly runnable

That means Claude Code treats hooks as policy contributors, not policy dictators.

### 2. Permission Mediation

Claude Code merges:
- hook results
- rule-based permissions
- interactive prompting or classifier paths
- host or mode constraints

This is why requests about hooks often overlap with `/permissions` or `/config`. The real question is often not "what is the hook file?" but "where in the decision ladder does this hook act?"

### 3. Post-Tool Governance

After a successful tool call, hooks can:
- attach context
- emit blocking or warning messages
- stop continuation
- rewrite MCP output through an MCP-only path

Important boundary:
- output mutation is not a generic free-for-all
- MCP-specific output rewriting should stay separate from normal tool-result formatting

### 4. Failure Governance

Failure hooks are a separate stage, not just post hooks with an error flag.

They can:
- annotate the failure
- surface retry guidance
- add context without erasing the underlying failure

This matters because Claude Code does not treat every hook event as fatal.

### 5. Error And Cancellation Policy

Hook cancellation and hook execution errors are usually visible runtime events, not silent drops and not always full hard failures.

This is one of the strongest lessons for Codex:
- governance failures should be observable
- but the governance layer should not become a fragile single point of failure unless the policy explicitly says fail closed

## Mapping Guidance

### `/hooks`

Keep `approximate`.

Translation consequence:
- explain the real config surface when it exists
- but also explain that Claude Code hooks are runtime governance, not only file entries

### `/permissions`

Keep `approximate`.

Translation consequence:
- when hooks are involved, explain the decision ladder rather than only saying "host-managed approvals"

### `/config`

Keep `approximate`.

Translation consequence:
- distinguish schema-level hook configuration from runtime hook behavior

### Plugin And MCP Requests

When the user asks about plugins or MCP, do not flatten hooks away.

Translation consequence:
- plugin lifecycle can change active runtime hooks
- MCP tool output may be hook-mediated
- some "plugin install" questions are really governance questions, not package-management questions

## What Codex Should Learn

The valuable Claude Code pattern is:
- tools are not only executed
- they are governed

That governance has explicit stages:
- pre-tool
- permission mediation
- post-tool
- failure handling
- observable non-fatal errors

This is a reusable operating model that should shape how Codex explains hardest Claude Code behaviors.
