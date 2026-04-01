# Aliases And Visibility

Use this file when the user names a Claude Code alias, shorthand, or a command whose visibility depends on product mode, account type, or platform.

## Mapping Rule

- Normalize the user's phrasing to the canonical command first.
- Then apply the canonical mapping from `command-mapping.md`.
- If the command is hidden, remote-only, account-gated, or environment-gated in Claude Code, mention that in the boundary.

## Common Slash Command Aliases

| Canonical Command | Aliases | Visibility Notes |
| --- | --- | --- |
| `/clear` | `/reset`, `/new` | Always normalize to `/clear` |
| `/rewind` | `/checkpoint` | Same rollback family, still approximate in Codex |
| `/resume` | `/continue` | Same resume semantics, still approximate in Codex |
| `/session` | `/remote` | Remote-mode only in Claude Code |
| `/permissions` | `/allowed-tools` | Same command family |
| `/config` | `/settings` | Same command family |
| `/plugin` | `/plugins`, `/marketplace` | Same plugin-management surface |
| `/desktop` | `/app` | `claude-ai` subscriber plus platform-gated |
| `/mobile` | `/ios`, `/android` | Same mobile pairing surface |
| `/feedback` | `/bug` | Product feedback surface |
| `/exit` | `/quit` | Same exit behavior |
| `/tasks` | `/bashes` | Background-task oriented, not plan-tracking oriented |
| `/branch` | `/fork` only when `/fork` is not separately enabled | Conversation branch, not git branch |
| `/remote-control` | `/rc` | Feature-gated remote-control surface |

## Common CLI Aliases

| Canonical CLI Form | Aliases | Visibility Notes |
| --- | --- | --- |
| `claude plugin` | `claude plugins` | Same management surface |
| `claude plugin install` | `claude plugin i` | Same command |
| `claude plugin uninstall` | `claude plugin remove`, `claude plugin rm` | Same command |
| `claude plugin marketplace remove` | `claude plugin marketplace rm` | Same command |
| `claude update` | `claude upgrade` | Same updater command |
| `claude remote-control` | `claude rc`, `claude remote`, `claude sync`, `claude bridge` | Same bridge surface |

## Visibility And Gating Cases

Mention these in the boundary when relevant:

- `/session` is remote-only upstream.
- `/files` is effectively `ant`-only upstream.
- `/desktop` depends on `claude-ai` account type and platform support.
- `/chrome` depends on `claude-ai` account type and an interactive environment.
- `/output-style` is hidden and deprecated upstream in favor of `/config`.
- `/voice` depends on `claude-ai` account type and a feature gate.
- Some aliases only exist when a feature-gated command is absent, such as `/branch` using `/fork`.

## Do Not Do

- Do not treat an alias as a separate feature.
- Do not ignore upstream visibility when explaining the boundary.
- Do not map an alias to a different Codex workflow than its canonical command.
