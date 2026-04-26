# Architecture Lenses（架构视角）

当用户请求依赖 Claude Code 内部运行时模型（而不仅仅是斜杠命令名称）时，使用本文件。

本文件不替代 `command-mapping.md` 或 `workflow-mapping.md`。它解释的是*为什么*某些映射只能是 `approximate` 或 `unavailable`。

## 1. Instruction Assembly（指令组装）

Claude Code 不是靠单个 `CLAUDE.md` 文件驱动的。它从共享指导、个人指导、规则、skill、hook 以及相关仓库产物中组装行为。

上游源码锚点：
- `src/commands/init.ts:28` — `/init` 是一个产物选择工作流，不只是文件生成器。
- `src/commands/init.ts:46` — 引导流程会扫描 `CLAUDE.md`、`AGENTS.md`、规则、Copilot/Cursor 指令和 `.mcp.json`。
- `src/commands/init.ts:70` — 当 worktree 是同级或外部而非嵌套时，个人指导的放置位置会变化。
- `src/bootstrap/state.ts:205` — session 状态跟踪用于加载 CLAUDE.md 的附加目录。

Mapping 影响：
- `/init` 应保持 `approximate`。
- 关于"Claude 在这个仓库中应如何行为"的请求可能映射到指导文件、设置、hook 或 skill，取决于用户的真实目标。

## 2. Settings And Policy（设置与策略）

Claude Code 暴露的是广泛的策略和设置面，不只是单个偏好设置文件。

上游源码锚点：
- `src/utils/settings/types.ts:407` — 项目级 MCP 审批是一等设置。
- `src/utils/settings/types.ts:435` — hook 是类型化设置面的一部分。
- `src/utils/settings/types.ts:438` — worktree 行为是可通过策略配置的。
- `src/utils/settings/types.ts:823` — plan 可以存放在可配置的目录中。
- `src/utils/settings/types.ts:937` — auto-memory 有显式的启用和存储设置。

Mapping 影响：
- `/config`、`/settings`、`/permissions` 以及部分 `/mcp` 通常是 `approximate`。
- 当可编辑文件存在时，说明具体文件。不要暗示 Codex 有统一的设置界面。

## 3. Permission Decision Ladder（权限决策阶梯）

Claude Code 的权限不只是模式切换。它是一个有序的决策阶梯，组合了 deny 和 ask 规则、安全检查、内部路径豁免、工作目录边界、shell 结构检查和基于模式的快速路径。

上游源码锚点：
- `src/utils/permissions/filesystem.ts:1205` — 文件写入进入有序的权限阶梯。
- `src/utils/permissions/filesystem.ts:1305` — 安全检查在普通的 ask 和 allow 逻辑之前运行。
- `src/utils/permissions/filesystem.ts:1367` — `acceptEdits` 快速路径仍限定在允许的工作目录内。
- `src/tools/BashTool/bashPermissions.ts:2229` — shell deny 和 ask 规则在路径约束之前运行。
- `src/tools/BashTool/bashPermissions.ts:2338` — 即使看似被允许的 shell 命令也必须通过注入敏感检查。
- `rust/crates/runtime/src/permissions.rs:89` — `claw-code` 将权限建模为每个工具的当前模式与所需模式的对比。

Mapping 影响：
- `/permissions` 保持 `approximate`，因为 Codex 可以解释当前审批模型，但不暴露 Claude Code 完整的决策阶梯。
- `/sandbox` 保持 `unavailable`，因为宿主沙箱控制与 Claude Code 内部的风险排序不是同一回事。

## 4. Agent Isolation And Background Execution（Agent 隔离与后台执行）

Claude Code 的 agent 行为包括隔离模式、后台执行、continuation 和团队/任务状态。不只是"启动另一个 agent"。

上游源码锚点：
- `src/tools/AgentTool/AgentTool.tsx:87` — subagent 可以在后台运行。
- `src/tools/AgentTool/AgentTool.tsx:99` — 隔离是显式的，包括 `worktree` 和受控的 `remote`。
- `src/skills/bundled/batch.ts:61` — 批量执行需要隔离的 worktree agent 和后台执行。
- `src/bootstrap/state.ts:143` — session 创建的团队会被跟踪和清理。
- `src/bootstrap/state.ts:175` — 已调用的 skill 按 agent 跟踪，用于 compaction 和保留。

Mapping 影响：
- `/fork`、`/agents` 和 `/tasks` 应从隔离和后台语义角度来推理。
- Codex 委托保持 `approximate`，因为它不暴露相同的持久化 agent/任务管理器。

## 5. Memory, Plans, And Compaction Lifecycle（记忆、计划与压缩生命周期）

Claude Code 的会话连续性是一个运行时子系统，包含记忆压缩、plan 文件、类检查点摘要和缓存清理。

上游源码锚点：
- `src/services/compact/autoCompact.ts:287` — 自动压缩先尝试 session-memory compaction，再回退到旧版 compaction。
- `src/services/compact/autoCompact.ts:257` — 自动压缩有针对重复失败的断路器。
- `src/memdir/memdir.ts:255` — memory prompt 区分 memory、plan 和类任务状态，而非将它们扁平化。
- `src/bootstrap/state.ts:167` — plan slug 缓存在 session 状态中。
- `src/bootstrap/state.ts:175` — 已调用的 skill 跨 compaction 边界被跟踪。
- `src/utils/settings/types.ts:823` — plan 存储位置可配置。
- `src/utils/settings/types.ts:943` — auto-memory 存储可配置且涉及安全敏感性。

Mapping 影响：
- `/compact`、`/resume` 和 `/rewind` 不只是"写一个摘要"。
- 保持 `approximate`，并说明 Codex 缺少的部分：transcript 原语、session memory 层和自动压缩行为。

## 6. MCP Runtime, Administration, And Inbound Control（MCP 运行时、管理与入站控制）

Claude Code 将 MCP 至少分为三层：
- 工具/资源的运行时使用
- server 配置的管理
- 入站运行时接口（如 channel 通知）

上游源码锚点：
- `src/services/mcp/client.ts:2173` — 运行时发现同时获取工具、命令、skill 和资源。
- `src/services/mcp/channelNotification.ts:176` — 入站 channel 注册按严格顺序控制。
- `src/utils/settings/types.ts:407` — `.mcp.json` 审批是持久化设置。
- `src/utils/settings/types.ts:895` — 组织策略可以单独控制 channel 通知的 opt-in。

Mapping 影响：
- "使用 MCP 工具"和"管理 MCP server"要分开。
- 两者都与入站/channel 控制面行为分开。
- 最困难的 MCP 场景还应参阅 `mcp-runtime-and-inbound-control-plane.md`。

## 7. Remote And Bridge Control Planes（远程与桥接控制面）

Claude Code 有独立的远程、桥接和 session 附接接口。这些不只是名称不同的 shell 命令。

上游源码锚点：
- `src/commands.ts:619` — 远程和桥接接口的命令安全性是分开的。
- `src/bootstrap/state.ts:197` — 远程模式在 session 状态中被跟踪。
- `src/bootstrap/state.ts:207` — 允许的 channel server 与普通 MCP 使用分开跟踪。

Mapping 影响：
- `/session`、`claude remote-control`、`/remote-control`、移动端配对、daemon 流程和桥接附接应保持 `unavailable`，除非当前 Codex 宿主明确暴露了这些功能。
- 说明这些是缺失的传输/控制面，而不仅仅是缺失的命令别名。

## 如何使用这些视角

- 如果用户问"为什么这个只是 approximate？"，先从本文件开始，再扩展命令表。
- 如果请求涉及仓库设置、hook、memory 或 settings，还应阅读 `settings-memory-and-hooks.md`。
- 如果请求涉及 tool-event hook、通过 hook 进行的权限中介、continuation 控制或 MCP 输出变异，还应阅读 `hook-and-tool-governance.md`。
- 如果请求涉及审批提示、deny 和 ask 排序、shell 安全门、工作目录边界或爆炸半径问题，还应阅读 `permission-decision-ladder.md`。
- 如果请求涉及 subagent、后台任务、worktree 或远程控制，还应阅读 `agent-isolation-and-background.md`。
- 如果请求实际上是关于仓库行为存放位置、指导如何被发现、或 skill 和 agent 如何互相遮蔽，还应阅读 `repo-operating-system.md`。
- 如果请求专门关于源顺序、active 与 shadowed 定义、旧版兼容目录、或 skill/agent 应放在哪里，还应阅读 `registry-and-precedence.md`。
- 如果请求专门关于 `/compact`、`/resume`、`/rewind`、上下文压力、附件恢复或 prompt 长度错误后的恢复，还应阅读 `context-hygiene.md`。
- 如果请求专门关于 MCP 运行时身份、资源发现、认证、重连或 server 推送的 channel 行为，还应阅读 `mcp-runtime-and-inbound-control-plane.md`。
- 如果请求实际上是关于超出 marketplace 命令范围的插件或扩展行为，还应阅读 `plugin-runtime-and-lifecycle.md`。
