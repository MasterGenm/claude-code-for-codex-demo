# MCP Runtime And Inbound Control Plane

Use this file when the request is really about MCP runtime behavior rather than only `/mcp` or `claude mcp add`.

This is the Claude Code split that matters:

1. runtime use of tools and resources
2. administration of server configuration
3. inbound control plane behavior, where an MCP server can push or register conversation-visible behavior

## What Claude Code Is Actually Doing

Claude Code does not treat MCP as a single feature bucket.

The real runtime has at least three planes:

### Runtime Plane

This is the plane most users notice first:
- connect to servers
- discover tools
- discover resources
- add resource helper tools when needed
- reconnect on session expiry
- surface needs-auth state

### Administration Plane

This is the plane exposed by `/mcp` and `claude mcp *`:
- server definitions
- approvals and trust choices
- list/get/add/remove flows
- config-file and managed-policy state

### Inbound Control Plane

This is the hardest part and the easiest to miss:
- channel-style inbound notifications
- registration gates
- org policy opt-in
- session `--channels` opt-in
- plugin/server allowlists
- auth and marketplace-source verification

That third plane is why MCP in Claude Code is more than "tool calling plus config editing".

## Source Anchors

Reverse-engineered Claude Code mirror:
- `src/services/mcp/client.ts:1175` - connection setup records server capabilities including tools, prompts, resources, and resource-subscribe support.
- `src/services/mcp/client.ts:1190` - an elicitation handler is registered during initialization, showing that runtime negotiation includes non-tool request handling.
- `src/services/mcp/client.ts:2173` - tool, command, skill, and resource discovery are fetched together, then normalized into the session runtime.
- `src/services/mcp/client.ts:2183` - resource helper tools are injected when resources exist but generic resource tools are not already present.
- `src/services/mcp/client.ts:3217` - session expiry clears connection cache so the next tool call reconnects with a fresh session.
- `src/services/mcp/channelNotification.ts:176` - inbound channel registration is gated in a strict order: capability, runtime gate, auth, org policy, session opt-in, allowlist.
- `src/services/mcp/channelNotification.ts:245` - even a trusted server must still be listed in session `--channels` to push inbound messages.
- `src/services/mcp/channelNotification.ts:276` - plugin-origin verification and approved-plugin allowlists are part of inbound registration, not generic MCP use.
- `src/utils/settings/types.ts:407` - project-level approved and rejected `.mcp.json` server choices are persisted settings.
- `src/utils/settings/types.ts:895` - managed org settings expose `channelsEnabled`, making inbound MCP a policy surface, not just a local config detail.
- `src/bootstrap/state.ts:213` - allowed channels are tracked as session state separate from ordinary MCP usage.

`claw-code` clean-room runtime:
- `rust/crates/runtime/src/mcp.rs:26` - runtime MCP tools are named from server and tool identity, not treated as anonymous generic calls.
- `rust/crates/runtime/src/mcp.rs:65` - server signatures distinguish stdio and remote transports, making runtime identity first-class.
- `rust/crates/runtime/src/mcp.rs:84` - scoped MCP config hashes encode transport, headers, helpers, and OAuth-related fields for reconnection and drift detection.
- `rust/crates/runtime/src/config.rs:531` - MCP server definitions are loaded as typed runtime config, not as free-form shell notes.
- `rust/crates/runtime/src/config.rs:713` - remote transports and managed proxy forms are distinct MCP config variants.

## 1. Runtime Plane

For runtime use, the important question is not "is MCP enabled?" but "what did this connected server actually advertise?"

Runtime behavior includes:
- capability inspection
- tool discovery
- resource discovery
- helper-tool injection for resources
- auth or needs-auth handling
- reconnect and session-expiry recovery

Operational consequence:
- "use MCP tools" is usually `approximate` in Codex because Codex may expose tools and resources, but not the same full negotiation, reconnect, or auth surface

## 2. Administration Plane

Administration is the plane users touch with `/mcp` and `claude mcp *`.

This plane covers:
- listing configured servers
- inspecting one config entry
- adding, removing, or importing server configs
- project-scoped approvals or rejections
- managed allowlists or policy overlays

Operational consequence:
- admin actions remain `approximate` or `unavailable` depending on whether a real editable config surface exists in the current Codex host

## 3. Inbound Control Plane

This is the part most migrations under-model.

Claude Code allows some MCP servers to register an inbound path that can push conversation-visible messages. That path is not equivalent to ordinary tool use.

The gate order matters:

1. server declares the `claude/channel` capability
2. runtime feature gate is enabled
3. auth is Claude.ai OAuth, not generic API-key access
4. org policy opts in with `channelsEnabled`
5. the session explicitly opted in with `--channels`
6. allowlist and plugin-source checks pass

Operational consequence:
- inbound/channel behavior is usually `unavailable` in Codex unless the host explicitly exposes an equivalent transport and session control plane
- do not translate it as "just another MCP tool"

## 4. Identity, Transport, And Reconnect

The runtime plane also has an identity model:
- tool names are server-qualified
- remote proxy URLs may wrap underlying MCP URLs
- server signatures and scoped config hashes drive reconnect and drift detection

This matters because "same config entry" and "same runtime session" are not the same thing.

Operational consequence:
- when a user asks why MCP runtime changed after auth, reconnect, or config edits, explain that this is a connection-identity issue, not just a config-file issue

## 5. Mapping Guidance

### Runtime MCP Use

Keep `approximate`.

Explain:
- Codex may be able to use exposed MCP tools and resources directly
- this does not imply parity with Claude Code's auth, reconnect, or inbound runtime behavior

### MCP Administration

Keep `approximate` or `unavailable` based on whether there is a real editable config surface.

Explain:
- runtime MCP availability does not guarantee admin parity
- config editing, list/get/add/remove, and approval-state management are separate questions

### Inbound Notifications, Channels, Or Server-Pushed Messages

Usually keep `unavailable`.

Explain:
- Claude Code has a distinct inbound control plane
- Codex may consume tools without exposing server-driven message registration, session opt-in, or org-managed allowlists

### `claude mcp add`, `list`, `get`

These stay in the admin bucket even when the user is motivated by runtime issues.

Do not answer them as if they were ordinary tool-invocation questions.

## What Codex Should Learn

The durable lesson is:

- MCP use is not MCP administration
- MCP administration is not inbound control
- runtime identity and reconnection matter
- server push paths are control-plane behavior, not just richer tool results

That is the Claude Code operating logic worth distilling.
