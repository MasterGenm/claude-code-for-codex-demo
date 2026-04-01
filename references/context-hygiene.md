# Context Hygiene

Use this file when the request is really about keeping long Claude-style sessions healthy: compaction, resume correctness, rewind boundaries, attachment restoration, context pressure, or recovery after prompt-length failures.

This file is about the runtime pipeline that keeps context usable over time.

## What Claude Code Is Actually Doing

Claude Code context management is not a single "make a summary" action.

It is a layered hygiene system that can:
- trim redundant history
- shrink tool-result burden
- preserve recent high-granularity context
- rebuild a continuation message
- restore important attachments after compaction
- filter resume state at compact and snip boundaries
- attempt recovery before surfacing prompt-length or max-output failures

High-value source anchors:
- `rust/crates/runtime/src/compact.rs:37` - compaction is threshold-based, not unconditional.
- `rust/crates/runtime/src/compact.rs:65` - the continuation message is an explicit protocol, not just raw summary text.
- `rust/crates/runtime/src/compact.rs:107` - recent messages are preserved verbatim while older context is summarized.
- `rust/crates/runtime/src/compact.rs:230` - repeated compactions merge prior summaries instead of discarding continuity.
- `src/query.ts:396` - snip runs before microcompact.
- `src/query.ts:412` - microcompact runs before autocompact.
- `src/query.ts:429` - context collapse runs before autocompact so cheaper recovery can avoid global compaction.
- `src/query.ts:790` - recoverable errors are withheld until the runtime knows whether recovery succeeded.
- `src/query.ts:1068` - prompt-too-long recovery is a structured path, not an immediate fatal response.
- `src/query.ts:1188` - max-output recovery also goes through a dedicated path.
- `src/services/compact/autoCompact.ts:57` - autocompact has a circuit breaker.
- `src/services/compact/autoCompact.ts:345` - repeated failures stop future attempts for the session.
- `src/services/compact/compact.ts:330` - post-compact state is rebuilt in a deliberate order.
- `src/services/compact/compact.ts:533` - attachment generation is handled asynchronously as part of post-compact reconstruction.
- `src/services/compact/compact.ts:1402` - recently accessed files can be restored after compaction under a token budget.
- `src/services/compact/compact.ts:1470` - plan files are explicitly preserved across compaction.
- `src/services/compact/compact.ts:1492` - invoked skills are explicitly preserved across compaction.
- `src/services/compact/compact.ts:1566` - async agents are re-announced after compaction.
- `src/utils/sessionStorage.ts:1396` - compact boundaries matter for correct resume chaining.
- `src/utils/sessionStorage.ts:1979` - snip boundaries also affect resume correctness.
- `src/utils/sessionStorage.ts:2212` - resume consistency is monitored as a real correctness concern.
- `src/utils/sessionStorage.ts:4354` - attachments are filtered deliberately on resume rather than replayed wholesale.

## The Real Hygiene Pipeline

### 1. Budget Before Collapse

Claude Code tries cheaper hygiene passes before the heaviest one.

The rough order is:
- snip
- microcompact
- context collapse
- autocompact

That order matters because the system wants to preserve detailed recent context whenever possible.

### 2. Compaction Preserves A Live Continuation

Compaction is not "replace everything with a summary."

It usually keeps:
- a continuation/system summary
- recent high-granularity messages
- selected attachments or restored artifacts

This is why `/compact` is only `approximate` in Codex. The missing piece is not just a built-in summary command. The missing piece is the full continuation protocol.

### 3. Attachments And Artifacts Are Rebuilt Selectively

After compaction, Claude Code can restore:
- recent file context
- plan files
- invoked skill content
- plan-mode or agent state cues

This is one of the biggest differences from a naive "write notes and continue" workflow.

The post-compact context is curated, not dumped.

### 4. Resume Correctness Depends On Boundary Filtering

Resume is not just "load prior messages from disk."

Correct resume depends on:
- compact-boundary filtering
- snip-boundary filtering
- preserved segment reconstruction
- selective attachment replay
- context-collapse snapshot restoration

That is why `/resume` and `/rewind` should stay `approximate`. Codex can reconstruct workspace state, but it does not expose this transcript-aware hygiene stack.

### 5. Recovery Comes Before Failure Surfacing

Claude Code does not always surface context errors immediately.

It may first try:
- context collapse
- reactive compaction
- max-output recovery
- other structured reductions

This is a runtime state machine, not only an error message strategy.

### 6. Hygiene Failures Need Guardrails

Autocompact has a circuit breaker because repeated failed compactions can make the system thrash.

That is an important lesson for Codex:
- hygiene and recovery systems need stop conditions
- otherwise the runtime can loop forever on the same failure mode

## Mapping Guidance

### `/compact`

Keep `approximate`.

Translation consequence:
- explain that Codex can write checkpoint summaries or docs
- do not imply parity with Claude Code's multi-pass compaction and restoration pipeline

### `/resume`

Keep `approximate`.

Translation consequence:
- reconstruct from files, plans, git state, and notes
- explain that Codex lacks transcript-aware boundary filtering and post-compact restoration

### `/rewind`

Keep `approximate`.

Translation consequence:
- treat it as restoring a prior checkpoint or approach
- do not imply session-level rewind with transcript and chain correctness

### `/context`

Keep `approximate`.

Translation consequence:
- summarize visible context pressure, touched files, and likely risks
- do not imply Claude Code's exact token-grid or hygiene-state visualization

### Export And Checkpoint Requests

Treat them as continuity-artifact requests, not only "save text somewhere."

Translation consequence:
- write durable summary or checkpoint artifacts
- explain that Claude Code's post-compact context is reconstructed, not only exported

## What Codex Should Learn

The useful Claude Code lesson is:
- long-context health is an active runtime responsibility

That responsibility includes:
- budgeting
- staged reduction
- selective restoration
- boundary-aware resume
- structured recovery

This is a reusable operating model that should shape how Codex explains hardest session-continuity requests.
