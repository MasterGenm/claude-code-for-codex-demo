# Command Mapping

Coverage note:

- This file covers the user-facing Claude Code slash commands and CLI subcommands surfaced by the reverse-engineered project documentation and command registry.
- Commands are grouped by operational area for maintainability.
- Canonical command rows live here; aliases and visibility notes live in `aliases-and-visibility.md`.
- Status meanings are strict:
  - `direct`
  - `approximate`
  - `unavailable`

## Slash Commands: Core Session And Context

| Claude Command | Intent | Status | Codex Mechanism | How To Operate In Codex | Boundary | Fallback / Reason |
| --- | --- | --- | --- | --- | --- | --- |
| `/help` | Show available actions | direct | Normal assistant response plus local skill and tool awareness | Summarize available tools, skills, and workflow options in the current environment | No dedicated slash help UI | Ask Codex what tools and skills are available |
| `/clear` | Clear conversation history and free up context | approximate | New thread or explicit scope reset | Start a new thread or instruct Codex to ignore prior context and restate the task | Codex does not expose a slash command that resets transcript state in place | Approximate with a fresh thread or a scoped reset |
| `/exit` | Exit the Claude terminal session | unavailable | None | None | Chat or session lifecycle is owned by the host UI, not a skill | Unavailable: session termination is not controlled by skill logic |
| `/status` | Show Claude Code status including version, model, account, API connectivity, and tool statuses | approximate | Environment and workspace status summary | Summarize cwd, branch, visible model information, relevant tool availability, and environment constraints | Codex does not expose the same integrated account or API status panel | Approximate with an environment summary |
| `/session` | Show remote session URL and QR code | unavailable | None | None | This command is remote-only upstream and depends on a remote pairing surface | Unavailable: Codex does not expose a generic remote session URL or QR flow |
| `/stats` | Show Claude Code usage statistics and activity | unavailable | None | None | Codex does not expose a public equivalent for this usage-activity surface | Unavailable: product metrics are not surfaced as a slash workflow |
| `/usage` | Show plan usage limits | unavailable | None | None | Plan usage is an account-managed Claude surface, not a generic Codex runtime primitive | Unavailable: usage limits are product-managed |
| `/extra-usage` | Configure extra usage to keep working when limits are hit | unavailable | None | None | This is an account and billing control surface, not a workspace operation | Unavailable: extra-usage controls are product-managed |
| `/cost` | Show the total cost and duration of the current session | unavailable | None | None | Codex does not expose a user-level session cost and duration surface in this skill context | Unavailable: pricing telemetry is not generally available |
| `/export` | Export the current conversation to a file or clipboard | approximate | Workspace export document | Produce a structured transcript or summary file in the workspace, or return a copy-ready export block | Not a first-class transcript exporter or clipboard writer | Approximate by writing an export document |
| `/copy` | Copy Claude's last response to clipboard | approximate | Re-emit the requested content | Repeat the relevant content in a copy-ready block, including a specific earlier response when the user asks for one | Clipboard control is host-owned | Approximate by returning the exact text |
| `/rename` | Rename the session | unavailable | None | None | Thread naming is host-owned | Unavailable: no skill-level session rename surface |
| `/files` | List all files currently in context | approximate | Context-file summary | Summarize files already touched, read, attached, or otherwise central to the current task | Codex does not expose Claude Code's exact in-context file set, and this command is `ant`-only upstream | Approximate with a touched-files summary |
| `/diff` | View uncommitted changes and per-turn diffs | approximate | Git diff review | Inspect `git diff`, summarize changes, and cite files | Codex can inspect working-tree diffs but does not expose Claude Code's per-turn diff surface | Approximate with git diff review |
| `/context` | Show current context usage | approximate | Context budget summary | Summarize the current task context, touched files, and any visible context-pressure signals | No colored grid or exact token-usage visualization | Approximate with a context-usage summary |
| `/memory` | Edit Claude memory files | approximate | Workspace guidance files | Read or update project guidance files such as `CLAUDE.md`, local notes, or other persistent instructions when explicitly asked | Codex does not expose Claude's dedicated memory-file manager | Approximate with workspace files |
| `/compact` | Reduce conversation size | approximate | Manual summarization | Summarize completed context, persist it to a file if needed, then continue from the summary | No transcript compaction primitive | Approximate with a checkpoint summary |
| `/rewind` | Restore the code and/or conversation to a previous point | approximate | Explicit rollback of approach | Restate the earlier checkpoint, discard the current approach, and continue from that restored plan or workspace state | No session-level code or transcript rewind primitive | Approximate with instruction-level reset and manual workspace rollback |
| `/resume` | Resume a previous conversation | approximate | Existing thread plus local artifacts | Reconstruct context from files, plans, notes, and git state | No Claude-style transcript resume flow | Approximate with manual restoration from workspace state |

## Slash Commands: Planning, Review, And Analysis

| Claude Command | Intent | Status | Codex Mechanism | How To Operate In Codex | Boundary | Fallback / Reason |
| --- | --- | --- | --- | --- | --- | --- |
| `/plan` | Enable plan mode or view the current session plan | approximate | Planning workflow and plan docs | Create or update a plan, track steps, and store plan docs under `docs/plans/` when useful | Codex can plan effectively but does not expose Claude's session-level plan-mode primitive | Approximate with planning workflow plus durable plan docs |
| `/review` | Review a pull request | approximate | PR review workflow | Review the pull request via `gh` when available, or review the checked-out diff and state the limitation | Codex does not expose the same PR-scoped slash workflow or guaranteed GitHub integration surface | Approximate with a PR review workflow |
| `/ultrareview` | Cloud-heavy deep review | approximate | Local deep review only | Do a thorough local review and state that remote Claude-on-the-web review is not available | Remote execution surface differs | Approximate with a stronger local review |
| `/security-review` | Security-focused review | direct | Security review workflow | Review changes with a security focus and call out exploit paths and trust boundaries | Different UI | Use the standard review workflow with security emphasis |
| `/doctor` | Diagnose and verify Claude Code installation and settings | approximate | Local health checks | Run targeted shell checks, inspect config, and report issues with remediation | Codex can diagnose the local environment, but not Claude-specific installation state with full parity | Approximate with repo and environment diagnostics |
| `/insights` | Analyze session history | unavailable | None | None | Codex does not expose the same session-history analytics surface | Unavailable: no equivalent local insights product surface |
| `/advisor` | Use advisory assistant mode | approximate | Second-pass reasoning | Provide a second-pass critique or recommendation set when asked | No explicit advisor feature toggle | Approximate with an explicit advisory pass |
| `/passes` | Show pass or tier info | unavailable | None | None | Account or subscription product concept differs | Unavailable: provider or account-specific |

## Slash Commands: Repository And Environment Operations

| Claude Command | Intent | Status | Codex Mechanism | How To Operate In Codex | Boundary | Fallback / Reason |
| --- | --- | --- | --- | --- | --- | --- |
| `/init` | Initialize a new CLAUDE.md bootstrap for the repository | approximate | Repo inspection plus guidance-file bootstrap | Inspect the repo, then create or update `CLAUDE.md` and related guidance artifacts when requested | Codex does not expose Claude Code's interactive `/init` bootstrap flow with optional skills and hooks | Approximate with repo inspection and guidance-file setup |
| `/add-dir` | Add another directory into scope | direct | Explicit path scoping | Read and operate on the requested directory after confirming scope | No dedicated tracked-dir UI | Use the requested path directly |
| `/branch` | Create a branch of the current conversation at this point | approximate | New thread or checkpointed fork workflow | Write a checkpoint summary, then continue in a new thread or explicitly fork the work plan from that checkpoint | This is a conversation branch, not a git branch | Approximate with a checkpoint-and-fork workflow |
| `/mcp` | Manage MCP servers | approximate | MCP admin or usage workflow | Use the MCP administration playbook for real config changes, or use configured MCP tools and resources directly when the user only wants runtime usage | Codex may expose MCP usage but not the same server-management UI | Approximate with available MCP tooling plus the MCP admin playbook |
| `/plugin` | Manage Claude plugins | approximate | Codex skills or plugins where available | Translate plugin intent into Codex skill or plugin mechanisms case by case | Plugin systems are different | Approximate; do not claim direct parity |
| `/reload-plugins` | Activate pending plugin changes in the current session | approximate | Re-read skill or plugin state if supported | Re-scan local skills or plugins when the environment supports it | No universal reload command or identical session-plugin lifecycle | Approximate with a manual refresh or re-read |
| `/skills` | List available skills | direct | Codex skill system | List relevant skills, choose one, and use it explicitly when needed | Different product, same core concept | Use Codex skills directly |
| `/permissions` | Manage allow & deny tool permission rules | approximate | Permission explanation plus local config inspection | State the current approval model, explain what is host-managed, and only edit local permission-related config when the environment actually exposes one | Codex permission policy is primarily host-configured, not slash-command-configured | Approximate with explanation and careful local config handling |
| `/sandbox` | Change sandbox mode | unavailable | None | None | Sandbox mode is controlled by the host environment | Unavailable: no skill-level sandbox toggle |
| `/config` or `/settings` | Manage settings | approximate | File edits and environment explanation | Edit local config files only when the host environment exposes them and the user asks | No single unified Codex settings slash command | Approximate with explicit file-level changes |
| `/remote-env` | Inspect remote environment config | unavailable | None | None | No equivalent remote-environment surface in a generic Codex skill | Unavailable: remote environment is not a common exposed primitive |
| `/model` | Switch model | unavailable | None | None | The active model is generally not switched through a local skill | Unavailable: model selection is host-controlled |
| `/fast` | Toggle fast mode | unavailable | None | None | No direct Codex equivalent exposed here | Unavailable: product-specific runtime toggle |
| `/effort` | Adjust reasoning effort | approximate | Response-depth adjustment | Use shorter or deeper reasoning according to the user request when supported by the host | No guaranteed explicit runtime toggle | Approximate with response behavior |
| `/output-style` | Deprecated command for changing output style | approximate | Style instruction | Adopt the requested output format in the current conversation or route the user toward config-style settings when the environment exposes them | The upstream command is hidden and deprecated, and Codex has no persistent output-style command surface | Approximate with response formatting instructions |
| `/theme` | Change terminal theme | unavailable | None | None | UI theme is host-owned | Unavailable: presentation layer is not controlled by this skill |
| `/color` | Change color identity | unavailable | None | None | Terminal or UI color personalization is host-owned | Unavailable |
| `/statusline` | Set up Claude Code's status line UI | unavailable | None | None | This configures Claude-specific status line UI through Claude settings and a dedicated setup flow | Unavailable: Codex does not expose the same status line surface |
| `/keybindings` | Configure keyboard bindings | unavailable | None | None | Input bindings are host-owned | Unavailable |
| `/vim` | Toggle vim mode | unavailable | None | None | Input-mode behavior is host-owned | Unavailable |

## Slash Commands: Account, Setup, And Hidden Utilities

| Claude Command | Intent | Status | Codex Mechanism | How To Operate In Codex | Boundary | Fallback / Reason |
| --- | --- | --- | --- | --- | --- | --- |
| `/login` | Sign in to Anthropic-backed Claude surfaces | unavailable | None | None | Authentication is host-managed and product-specific | Unavailable: Codex skills do not control account sign-in |
| `/logout` | Sign out from Anthropic-backed Claude surfaces | unavailable | None | None | Authentication is host-managed and product-specific | Unavailable |
| `/privacy-settings` | View or update privacy settings | unavailable | None | None | Privacy settings are account or product-owned | Unavailable |
| `/rate-limit-options` | Show subscriber options when rate limited | unavailable | None | None | Rate-limit upsell or account recovery flows are product-owned | Unavailable |
| `/upgrade` | Upgrade to Max for higher rate limits and more Opus | unavailable | None | None | Subscription upgrade flow is provider-managed and account-gated upstream | Unavailable: account upgrade is product-managed |
| `/terminal-setup` | Install or tweak terminal keybindings for Claude Code | approximate | Manual terminal configuration guidance | Explain or edit terminal config files if the user wants the equivalent newline or keybinding behavior locally | Codex has no built-in terminal setup installer | Approximate with terminal-specific instructions |
| `/release-notes` | View product release notes | approximate | Read changelog or release documents | Open the relevant release notes file or source when available and summarize it | No built-in Codex release-notes command | Approximate with doc inspection |
| `/hooks` | Inspect tool-event hook configuration | approximate | Local config inspection | Read the relevant hook or automation config files and explain them | Codex does not expose a unified hook settings UI | Approximate with file-based inspection |
| `/think-back` | Show Claude Code year-in-review experience | unavailable | None | None | Product analytics and animation surface are product-specific | Unavailable |
| `/thinkback-play` | Play the hidden thinkback animation | unavailable | None | None | Hidden product animation command | Unavailable |
| `/heapdump` | Dump the Claude Code process heap | unavailable | None | None | This targets Claude Code's own runtime internals, not the workspace project | Unavailable: no Codex-host heap dump surface |

## Slash Commands: Integrations And Surfaces

| Claude Command | Intent | Status | Codex Mechanism | How To Operate In Codex | Boundary | Fallback / Reason |
| --- | --- | --- | --- | --- | --- | --- |
| `/chrome` | Open Claude in Chrome settings | unavailable | None | None | This is a Claude-owned Chrome settings surface gated by account type and interactive mode, not generic browser automation | Unavailable: Codex cannot open or manage the same Chrome integration settings |
| `/desktop` | Claude desktop integration | unavailable | None | None | Desktop product integration is different | Unavailable |
| `/mobile` | Mobile pairing and QR flow | unavailable | None | None | Mobile product surface is absent | Unavailable |
| `/ide` | Manage IDE integrations and show status | approximate | Existing IDE-related tools or local repo workflow | Explain the available IDE bridge or editor workflow in the current environment, then use local file editing or exposed IDE tools when present | No unified IDE connection command | Approximate |
| `/install-github-app` | Set up Claude GitHub Actions for a repository | unavailable | None | None | This is a Claude-owned integration setup flow gated by product account surfaces | Unavailable |
| `/install-slack-app` | Install the Claude Slack app | unavailable | None | None | This is a Claude-owned integration setup flow gated by product account surfaces | Unavailable |
| `/pr-comments` | Get comments from a GitHub pull request | approximate | GitHub CLI or repo tools | Use `gh` or local review workflows if available to fetch PR-level and review comments | No single dedicated PR comments command | Approximate |

## Slash Commands: Collaboration, Tasks, And Miscellaneous

| Claude Command | Intent | Status | Codex Mechanism | How To Operate In Codex | Boundary | Fallback / Reason |
| --- | --- | --- | --- | --- | --- | --- |
| `/agents` | Manage agent configurations | approximate | Codex delegated agents when explicitly allowed | Explain the available delegation roles and use subagents only when the user explicitly requests them | Codex delegation is permissioned and differs from Claude agent UX and agent-configuration UI | Approximate |
| `/tasks` | List and manage background tasks | approximate | Active task or process summary | Summarize active delegated agents, pending long-running shell tasks, or visible queued work when such state exists | No persistent Claude-style background task manager | Approximate with visible task or process state |
| `/btw` | Ask a quick side question without interrupting the main conversation | approximate | Scoped side-question workflow | Answer the side question briefly, then explicitly return to the main task context | No dedicated side-question UI that preserves a separate conversational branch | Approximate with a brief scoped detour |
| `/feedback` | Send product feedback | unavailable | None | None | Product feedback channel is host-owned | Unavailable |
| `/stickers` | Visual sticker feature | unavailable | None | None | UI-only feature | Unavailable |

## CLI Subcommands: Public And Semi-Public Surfaces

| Claude CLI Subcommand | Intent | Status | Codex Mechanism | How To Operate In Codex | Boundary | Fallback / Reason |
| --- | --- | --- | --- | --- | --- | --- |
| `claude` | Default interactive session | approximate | Normal Codex conversation | Work in the current Codex session | Different shell or UI entrypoint | Approximate |
| `claude mcp serve` | Start the Claude Code MCP server | unavailable | None | None | Codex does not expose a universal skill-level MCP server runtime | Unavailable |
| `claude mcp add` | Add an MCP server configuration | approximate | MCP admin decision tree | Use the MCP administration playbook: edit a concrete MCP config if it exists, otherwise stop at translation | Codex does not expose the same MCP admin CLI | See `integration-playbooks.md` |
| `claude mcp remove` | Remove an MCP server configuration | approximate | MCP admin decision tree | Remove the server from a real editable MCP config when one exists; otherwise stop after mapping | No identical MCP admin CLI | See `integration-playbooks.md` |
| `claude mcp list` | List configured MCP servers | approximate | MCP admin decision tree | First distinguish runtime MCP surfaces from admin config, then inspect whichever concrete surface actually exists | Codex may expose resources but not the same server registry | See `integration-playbooks.md` |
| `claude mcp get` | Inspect one MCP server configuration | approximate | MCP admin decision tree | Inspect a concrete MCP config entry when accessible; otherwise stop after mapping and explain the gap | No identical admin surface | See `integration-playbooks.md` |
| `claude mcp add-json` | Add a JSON-defined MCP server | approximate | MCP admin decision tree | Write the equivalent MCP config only when a real editable config surface is known | No direct MCP config writer command | See `integration-playbooks.md` |
| `claude mcp add-from-claude-desktop` | Import servers from Claude Desktop | approximate | MCP migration playbook | Read the Claude Desktop config if accessible, then translate entries into the local Codex MCP config | Cross-product import is not automatic | See `integration-playbooks.md` |
| `claude mcp reset-project-choices` | Reset project-scoped MCP approval choices | unavailable | None | None | Codex does not expose the same project trust-choice store | Unavailable |
| `claude server` | Start a Claude Code direct-connect session server | unavailable | None | None | No equivalent Codex direct-connect server surface | Unavailable |
| `claude ssh <host> [dir]` | Run Claude Code on a remote host via SSH | approximate | Shell SSH workflow | Use `ssh` directly when allowed and then operate in the remote shell explicitly | Not a Codex-managed remote session mode | Approximate |
| `claude open <cc-url>` | Connect to a Claude Code direct-connect URL | unavailable | None | None | No equivalent `cc://` direct-connect surface | Unavailable |
| `claude auth login` | Sign in to Anthropic auth | unavailable | None | None | Auth flow is host-managed | Unavailable |
| `claude auth status` | Show Anthropic auth status | unavailable | None | None | Account status surface differs | Unavailable |
| `claude auth logout` | Sign out of Anthropic auth | unavailable | None | None | Auth flow is host-managed | Unavailable |
| `claude plugin validate` | Validate a Claude plugin manifest | approximate | Plugin or skill validation workflow | First identify whether the target artifact is a Codex plugin or a Codex skill, then validate that artifact's real structure | Plugin schemas and package layouts differ | See `integration-playbooks.md` |
| `claude plugin list` | List installed Claude plugins | approximate | Inspect local Codex skills or plugins | List locally available skills and plugins in the current environment | Plugin inventory surface differs | Approximate |
| `claude plugin marketplace add` | Add a Claude marketplace source | approximate | Edit local plugin-marketplace metadata if the environment supports it | Update local marketplace metadata files when that workflow exists | Marketplace architecture differs | Approximate |
| `claude plugin marketplace list` | List configured Claude marketplaces | approximate | Inspect local plugin-marketplace metadata if present | Read the configured marketplace declarations from local files | No identical CLI or hosted marketplace surface | Approximate |
| `claude plugin marketplace remove` | Remove a Claude marketplace source | approximate | Edit local plugin-marketplace metadata if present | Remove the marketplace declaration from local files | Marketplace architecture differs | Approximate |
| `claude plugin marketplace update` | Refresh marketplace definitions | approximate | Re-read or update marketplace files manually | Pull or edit the backing metadata files when they exist | No one-shot Codex marketplace updater | Approximate |
| `claude plugin install` | Install a Claude plugin | approximate | Skill or plugin installation workflow | Prefer an existing Codex skill or the `skill-installer` workflow for reusable behavior; use plugin packaging only when the user truly wants a Codex plugin | Installation mechanics differ | See `integration-playbooks.md` |
| `claude plugin uninstall` | Remove a Claude plugin | approximate | Remove the local Codex plugin or skill files | Uninstall by deleting or disabling the relevant local package only when requested | Plugin lifecycle differs | Approximate |
| `claude plugin enable` | Enable a disabled Claude plugin | approximate | Enable the relevant Codex plugin or skill via local config | Re-enable the local package if the host exposes that control | No identical enablement surface | Approximate |
| `claude plugin disable` | Disable a Claude plugin | approximate | Disable the relevant Codex plugin or skill via local config | Disable the package through local config or file-level changes when that mechanism exists | No identical disablement surface | Approximate |
| `claude plugin update` | Update a Claude plugin | approximate | Artifact-specific update workflow | Re-run the real update path for the target Codex skill, plugin package, or local metadata instead of mimicking marketplace parity | No one-shot managed updater | See `integration-playbooks.md` |
| `claude setup-token` | Configure long-lived token | unavailable | None | None | Auth or token flow is product-managed | Unavailable |
| `claude agents` | List configured agents | approximate | Explain available Codex delegation roles | Summarize the available agent roles and delegation constraints in the current environment | Codex does not expose the same persistent agent registry | Approximate |
| `claude auto-mode defaults` | Print default classifier rules | unavailable | None | None | Codex does not expose Claude's transcript classifier system | Unavailable |
| `claude auto-mode config` | Print effective classifier config | unavailable | None | None | No equivalent Codex auto-mode config surface | Unavailable |
| `claude auto-mode critique` | Critique custom classifier rules | approximate | Manual rules review | Review the provided rules or heuristics directly in chat | No native Codex auto-mode subsystem | Approximate |
| `claude remote-control` and aliases `rc`, `remote`, `sync`, `bridge` | Attach local environment to Claude remote-control | unavailable | None | None | No equivalent bridge product surface | Unavailable |
| `claude assistant [sessionId]` | Attach to a running bridge session | unavailable | None | None | No equivalent assistant-client bridge surface | Unavailable |
| `claude doctor` | Check the health of the Claude Code auto-updater and trusted local environment | approximate | Local diagnostics | Run shell and file checks and report remediation | Codex can inspect the local environment, but not Claude's updater or trust workflow with full parity | Approximate with local diagnostics |
| `claude update` and alias `upgrade` | Update the Claude CLI | unavailable | None | None | Codex host or runtime update is outside skill control | Unavailable |
| `claude install [target]` | Install the Claude native build | unavailable | None | None | Codex installation is outside skill control | Unavailable |

## CLI Subcommands: Feature-Flagged Or Internal

| Claude CLI Subcommand | Intent | Status | Codex Mechanism | How To Operate In Codex | Boundary | Fallback / Reason |
| --- | --- | --- | --- | --- | --- | --- |
| `claude mcp xaa setup` | Configure XAA IdP auth for MCP | unavailable | None | None | This is Claude-specific auth infrastructure for MCP | Unavailable |
| `claude mcp xaa login` | Acquire or cache XAA IdP token | unavailable | None | None | Claude-specific auth infrastructure | Unavailable |
| `claude mcp xaa show` | Show XAA IdP config | unavailable | None | None | Claude-specific auth infrastructure | Unavailable |
| `claude mcp xaa clear` | Clear XAA IdP config | unavailable | None | None | Claude-specific auth infrastructure | Unavailable |
| `claude daemon [subcommand]` | Start or manage the daemon supervisor | unavailable | None | None | Codex does not expose the Claude daemon lifecycle | Unavailable |
| `claude ps` | List Claude background sessions | unavailable | None | None | No equivalent background-session registry | Unavailable |
| `claude logs` | Inspect Claude background session logs | unavailable | None | None | No equivalent background-session registry | Unavailable |
| `claude attach` | Attach to a background Claude session | unavailable | None | None | No equivalent background-session registry | Unavailable |
| `claude kill` | Kill a background Claude session | unavailable | None | None | No equivalent background-session registry | Unavailable |
| `claude new` | Create a template job | unavailable | None | None | Template-job subsystem is feature-gated and product-specific | Unavailable |
| `claude list` | List template jobs | unavailable | None | None | Template-job subsystem is product-specific | Unavailable |
| `claude reply` | Reply to a template job | unavailable | None | None | Template-job subsystem is product-specific | Unavailable |
| `claude environment-runner` | Run BYOC environment runner | unavailable | None | None | No equivalent environment-runner surface | Unavailable |
| `claude self-hosted-runner` | Run self-hosted worker service | unavailable | None | None | No equivalent self-hosted runner surface | Unavailable |
| `claude up` | Bootstrap Anthropic dev environment from `CLAUDE.md` | unavailable | None | None | Anthropic-internal dev bootstrap flow | Unavailable |
| `claude rollback [target]` | Roll back Claude releases | unavailable | None | None | Product-runtime lifecycle control is not exposed | Unavailable |
| `claude log` | Inspect Anthropic conversation logs | unavailable | None | None | Anthropic-internal operational surface | Unavailable |
| `claude error` | Inspect Anthropic error logs | unavailable | None | None | Anthropic-internal operational surface | Unavailable |
| `claude export` | Export Anthropic log sessions to text | unavailable | None | None | This targets Anthropic log storage, not a generic Codex transcript model | Unavailable |
| `claude task create` | Create an internal task item | approximate | Workspace task file or plan | Create the task in a local checklist, plan, or issue file | No internal task service exists in Codex | Approximate |
| `claude task list` | List internal task items | approximate | Workspace task file or plan | List tasks from the maintained local checklist or plan | No internal task service exists in Codex | Approximate |
| `claude task get` | Inspect one internal task | approximate | Workspace task file or plan | Read the requested task entry from local task artifacts | No internal task service exists in Codex | Approximate |
| `claude task update` | Update an internal task | approximate | Workspace task file or plan | Edit the task entry in the local plan or task file | No internal task service exists in Codex | Approximate |
| `claude task dir` | Show Anthropic task store path | unavailable | None | None | No equivalent hidden task-store path in Codex | Unavailable |
| `claude completion <shell>` | Generate shell completion scripts | unavailable | None | None | Codex CLI completion is not managed from this skill surface | Unavailable |

## Slash Commands: Feature-Flagged Or Optional Claude Code Features

| Claude Command | Intent | Status | Codex Mechanism | How To Operate In Codex | Boundary | Fallback / Reason |
| --- | --- | --- | --- | --- | --- | --- |
| `/voice` | Voice mode | unavailable | None | None | Voice I/O is not exposed through this skill | Unavailable |
| `/proactive` | Autonomous proactive mode | unavailable | None | None | Persistent autonomous loop is product-specific | Unavailable |
| `/brief` | Brief autonomous update | approximate | Manual concise summary | Write a brief summary on demand | No autonomous brief channel | Approximate |
| `/assistant` | Kairos assistant mode | unavailable | None | None | Product-specific long-running assistant mode | Unavailable |
| `/remote-control` | Connect this terminal for remote-control sessions | unavailable | None | None | Remote-control bridge behavior is product-owned and not exposed as a generic Codex slash surface | Unavailable |
| `/remote-control-server` | Serve remote control endpoint | unavailable | None | None | No daemon bridge server exposed here | Unavailable |
| `/force-snip` | Force history snip | unavailable | None | None | No transcript surgery primitive | Unavailable |
| `/workflows` | Run workflow scripts | approximate | Skill-guided or shell workflow | Run the requested workflow directly if Codex can execute it | Different workflow system | Approximate |
| `/web-setup` | Remote web setup flow | unavailable | None | None | Product-specific setup surface | Unavailable |
| `/subscribe-pr` | Subscribe to PR events | unavailable | None | None | No webhook subscription product surface | Unavailable |
| `/ultraplan` | Large remote planning workflow | approximate | Deep planning plus optional delegation | Use planning workflow and subagents only when available and explicitly requested | No identical remote planner | Approximate |
| `/torch` | Internal feature-flag command | unavailable | None | None | Feature meaning is product-specific and not exposed | Unavailable |
| `/peers` | Peer inbox or socket messaging | unavailable | None | None | No equivalent peer mailbox surface | Unavailable |
| `/fork` | Fork subagent | approximate | Delegated agent workflow | Spawn a subagent only if the user explicitly asks for delegation | Codex has stricter delegation rules | Approximate |
| `/buddy` | Paired buddy mode | unavailable | None | None | Product-specific collaboration mode | Unavailable |

## Slash Commands: Internal Or Anthropic-Only Commands

| Claude Command | Intent | Status | Codex Mechanism | How To Operate In Codex | Boundary | Fallback / Reason |
| --- | --- | --- | --- | --- | --- | --- |
| `/tag` | Tag session or issue state | unavailable | None | None | Internal-only surface | Unavailable |
| `/backfill-sessions` | Internal session maintenance | unavailable | None | None | Internal-only surface | Unavailable |
| `/break-cache` | Internal cache invalidation | unavailable | None | None | Internal-only surface | Unavailable |
| `/bughunter` | Internal bug finding flow | approximate | Local deep review | Perform a local deep bug hunt instead | Cloud or internal service not available | Approximate with a local deep bug hunt |
| `/commit` | Guided commit flow | approximate | Git workflow | Create commit messages and run git commands if the user asks | No built-in guarded commit command | Approximate |
| `/commit-push-pr` | Guided commit plus push plus PR | approximate | Git and `gh` workflow | Perform the git and GitHub steps explicitly if tools are available and the user approves | No one-shot managed workflow | Approximate |
| `/ctx-viz` | Internal context visualization | unavailable | None | None | No matching visualization surface | Unavailable |
| `/good-claude` | Internal command | unavailable | None | None | Internal-only surface | Unavailable |
| `/issue` | Internal issue workflow | approximate | GitHub or tracker workflow | Use issue tooling directly if available | No identical product wrapper | Approximate |
| `/init-verifiers` | Internal verifier setup | unavailable | None | None | Internal-only surface | Unavailable |
| `/mock-limits` | Internal limit mocking | unavailable | None | None | Internal-only surface | Unavailable |
| `/bridge-kick` | Internal bridge control | unavailable | None | None | Internal-only surface | Unavailable |
| `/version` | Show version | approximate | Explain environment or version if known | Report Codex environment details when available | No universal skill-level version command | Approximate |
| `/reset-limits` | Internal quota reset | unavailable | None | None | Internal or account control not available | Unavailable |
| `/onboarding` | Internal onboarding flow | unavailable | None | None | Product-managed flow | Unavailable |
| `/share` | Share session | unavailable | None | None | Product sharing surface differs | Unavailable |
| `/summary` | Internal summary flow | approximate | Manual summary | Write the summary directly | No dedicated internal feature parity | Approximate with a direct summary response |
| `/teleport` | Remote session teleport | unavailable | None | None | No equivalent remote session transport primitive | Unavailable |
| `/ant-trace` | Internal tracing | unavailable | None | None | Internal-only tracing surface | Unavailable |
| `/perf-issue` | Internal perf report | approximate | Local perf diagnosis | Diagnose performance locally and write findings | No identical product reporter | Approximate with a local performance diagnosis |
| `/env` | Inspect environment | direct | Shell environment inspection | Run environment checks and summarize them | No slash wrapper | Use shell inspection |
| `/oauth-refresh` | Refresh OAuth tokens | unavailable | None | None | Account auth flows are product-managed | Unavailable |
| `/debug-tool-call` | Internal debugging | approximate | Manual tool-call tracing | Trace the relevant tool behavior manually | No dedicated debug UI | Approximate with manual tracing |
| `/agents-platform` | Internal agents platform flow | unavailable | None | None | Internal-only surface | Unavailable |
| `/autofix-pr` | Internal automated PR fixing | approximate | Local fix workflow | Review the PR and implement fixes directly | No internal autofix service | Approximate with a local fix workflow |
