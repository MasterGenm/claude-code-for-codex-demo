# Unsupported Commands And Areas

Use this file to verify that a command should be labeled `unavailable`.

## Common Reasons

| Reason | Meaning |
| --- | --- |
| host-owned UI | The host application controls the feature, not the skill |
| product/account surface | Billing, auth, privacy, or subscription mechanics differ |
| no session primitive | Codex does not expose the same transcript/session control |
| no daemon or bridge surface | Remote-control, daemon, or background server features are absent |
| internal-only | The command is Anthropic-only or tied to hidden product infrastructure |

## Usually Unavailable In Codex

### UI And Session Control

- `/exit`
- `/theme`
- `/color`
- `/statusline`
- `/keybindings`
- `/vim`
- `/stickers`
- `/mobile`
- `/desktop`
- `/chrome`

### Account, Billing, And Auth

- `/usage`
- `/extra-usage`
- `/cost`
- `/passes`
- `/login`
- `/logout`
- `/privacy-settings`
- `/rate-limit-options`
- `/upgrade`
- `claude auth login/status/logout`
- `claude setup-token`
- `claude update`
- `claude upgrade`
- `claude install [target]`

### Remote, Daemon, And Bridge Features

- `/bridge`
- `/remote-control-server`
- `claude remote-control`
- `claude server`
- `claude open <cc-url>`
- `/teleport`

### Voice, Mobile, And Product-Specific Surfaces

- `/voice`
- `/assistant`
- `/proactive`
- `/think-back`
- `/thinkback-play`
- `/heapdump`
- `claude assistant`
- `claude daemon [subcommand]`
- `claude ps`
- `claude logs`
- `claude attach`
- `claude kill`

### Internal Or Anthropic-Only Commands

- `/tag`
- `/backfill-sessions`
- `/break-cache`
- `/ctx_viz`
- `/good-claude`
- `/init-verifiers`
- `/mock-limits`
- `/bridge-kick`
- `/reset-limits`
- `/onboarding`
- `/share`
- `/ant-trace`
- `/oauth-refresh`
- `/agents-platform`
- `claude mcp xaa setup/login/show/clear`
- `claude up`
- `claude rollback`
- `claude log`
- `claude error`
- `claude export`

## How To Use This File

- If a command lands here, default to `unavailable`.
- Only upgrade it to `approximate` if there is a real Codex-native fallback that reaches the user goal.
- When in doubt, prefer `unavailable` over overstating parity.
