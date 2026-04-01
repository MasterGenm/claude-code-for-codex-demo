# Integration Playbooks

Use this file for the hardest approximate integrations, especially MCP administration and plugin lifecycle flows.

## MCP Administration

### `claude mcp list`

Preferred sequence:

1. If the Codex environment exposes MCP resource or template listing tools, use them to show usable MCP surfaces.
2. If an editable MCP config file is known in the workspace or user config, inspect that file to show configured servers.
3. If neither exists, state that runtime MCP usage may be available but server-administration parity is not.

### `claude mcp get`

Preferred sequence:

1. If the relevant MCP config entry is accessible, read that entry directly.
2. Otherwise, stop after the mapping block and explain that Codex lacks a general MCP server-inspection UI.

### `claude mcp add`, `add-json`, `remove`

Preferred sequence:

1. Identify whether there is a concrete MCP config file or host-managed config surface that Codex can edit.
2. If yes, patch that concrete config.
3. If no, stop after the mapping block and explain that Codex may consume MCP tools without exposing MCP server administration.

### `claude mcp add-from-claude-desktop`

Preferred sequence:

1. If the Claude Desktop config file is accessible, read it.
2. Translate the relevant entries into the local Codex MCP config format.
3. If the destination config is not editable or not known, stop at translation and explain the gap.

### Inbound Or Channel-Style MCP Requests

Preferred sequence:

1. Identify whether the user is asking about runtime use, admin config, or inbound notifications.
2. If it is runtime use, work from the MCP tools and resources already exposed by the host.
3. If it is admin config, stay on the normal MCP admin decision tree.
4. If it depends on channel notifications, session `--channels`, org opt-in, allowlists, or server-pushed conversation messages, stop after the mapping block unless the current host explicitly exposes an equivalent control plane.

## Plugin And Marketplace Lifecycle

### `claude plugin install`

Preferred sequence:

1. Identify the user goal:
   - reusable Codex behavior
   - installable Codex plugin package
   - one-off task capability
2. If the goal is reusable behavior, prefer an existing Codex skill or use the `skill-installer` workflow.
3. If the goal is a Codex plugin package, use the `plugin-creator` workflow or edit the local plugin package directly.
4. If the goal is only the capability, do not force a marketplace-style install flow; use the nearest existing Codex skill or workflow.

### `claude plugin validate`

Preferred sequence:

1. Identify whether the target is a Codex plugin package or a Codex skill.
2. Validate the relevant manifest and required file structure for that target.
3. State clearly that Claude marketplace schemas and Codex plugin schemas are not identical.

### `claude plugin update`, `uninstall`, `enable`, `disable`

Preferred sequence:

1. Identify the actual Codex artifact being managed: skill, plugin package, or local metadata.
2. Use that artifact's real update or removal mechanism.
3. If there is no concrete artifact, stop after the mapping block and explain that marketplace parity is unavailable.

## When To Stop

Stop after the mapping block if:

- the environment exposes only runtime usage and not administration
- the relevant config file or package path is unknown
- the translation would otherwise become a hand-wavy "where available" answer

In those cases, ask for the concrete config path, plugin path, or target artifact before executing.
