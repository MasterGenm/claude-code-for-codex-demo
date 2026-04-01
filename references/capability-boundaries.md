# Capability Boundaries

This file explains why the skill must not treat Claude Code and Codex as interchangeable.

## Difference Matrix

| Area | Claude Code | Codex | Operational Consequence |
| --- | --- | --- | --- |
| Command surface | Rich slash-command and CLI command model | Tool-driven assistant plus skills | Translate user intent, not command spelling |
| Session model | Terminal REPL with transcript persistence, resume, rewind, compact features | Conversation thread plus workspace artifacts | Many session-control commands are approximate or unavailable |
| Permissions | User-facing permission modes and prompts | Host-managed approval and sandbox policy | Do not claim a slash-command permission model exists |
| Agent model | Built-in product agent and swarm flows | Delegation may exist, but only in bounded forms and often with explicit permission | Agent commands are often approximate |
| MCP management | User-facing server management commands | Environment may expose MCP tools/resources but not the same management UI | Separate MCP usage from MCP administration |
| Plugins | Claude plugin and marketplace model | Codex skills/plugins are a different abstraction | Do not map plugin commands naively |
| UI controls | Terminal UI modes, statusline, theme, stickers, mobile pairing | Host UI controls outside the skill | UI commands are usually unavailable |
| Remote and daemon features | Bridge, daemon, remote-control, cloud review, mobile handoff | Often absent | Mark these unavailable unless the environment explicitly provides them |
| Account surfaces | Usage, passes, privacy settings, auth commands | Provider/account model differs | Billing/account commands are usually unavailable |

## High-Risk Translation Mistakes

Avoid these mistakes:

- Treating a host-managed setting as if a skill can change it
- Treating Claude-specific per-turn diffs as if plain `git diff` were full parity
- Treating Claude's plan mode as if Codex had the same session primitive
- Claiming `/resume`, `/rewind`, or `/compact` are first-class session primitives in Codex
- Treating Claude plugin management as equivalent to Codex skills
- Spawning delegated agents automatically because Claude Code would
- Mapping remote/cloud-only commands to local shell workflows without stating the loss of capability

## Boundary Language

Use language like:

- `direct`: "Codex can do this directly, though the surface differs."
- `approximate`: "Codex can reach the same goal, but through a different workflow."
- `unavailable`: "Codex does not expose this capability in the current environment."

Avoid language like:

- "Same as Claude Code"
- "Equivalent"
- "Just use this command instead"

unless the practical capability is genuinely present.
