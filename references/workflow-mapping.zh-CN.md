# 工作流映射

当用户询问的是 Claude Code 行为而非单个命令名称时，使用本文件。

## 映射优先执行规则

| Claude Code 工作流 | Codex Status | Codex 机制 | 在 Codex 中的操作方式 | Boundary |
| --- | --- | --- | --- | --- |
| 要求 Codex 立即执行类似 Claude 的任务 | direct 或 approximate | 先进行 Mapping 块，然后执行相关 Codex 工作流 | 在行动之前先声明 `Status`、`Codex mapping`、`Boundary` 和 `Execution path in Codex` | 翻译不等于对等，执行必须遵循已映射的 status 规则 |

规则：

- 在映射决策可见之前不要执行。
- 如果用户只要求翻译，在 execution path 之后停止。
- 如果用户要求立即执行任务，在 mapping 块之后停止并请求确认。
- 仅在明确的映射后确认之后才继续，且仅当 `execution-policy.md` 允许时。

## 计划模式

| Claude Code 工作流 | Codex Status | Codex 机制 | 在 Codex 中的操作方式 | Boundary |
| --- | --- | --- | --- | --- |
| 进入计划模式，维护实时计划，然后执行 | approximate | 规划工作流加计划文档 | 构建计划，保持步骤更新，在有用时将计划文档存储在 `docs/plans/` 下 | Codex 可以遵循该工作流，但不提供 Claude 的会话级别计划模式原语 |

推荐模式：

1. 澄清任务。
2. 制定包含明确步骤的计划。
3. 在任务较大时保存持久化计划文件。
4. 执行计划并在工作推进时更新用户。

## 权限与沙箱

| Claude Code 工作流 | Codex Status | Codex 机制 | 在 Codex 中的操作方式 | Boundary |
| --- | --- | --- | --- | --- |
| 切换权限模式或检查权限提示 | approximate | 解释当前宿主审批模型 | 说明环境允许什么、什么需要审批以及执行将如何进行 | 权限策略由宿主配置，通常不由 skill 更改 |

规则：

- 不要承诺 Codex 可以按命令切换权限模式。
- 在请求的操作被当前环境阻止时进行说明。
- 如果宿主要求审批，清晰简洁地呈现操作。

关于 deny 和 ask 排序、危险路径检查、shell 安全门和模式升级背后更深层的运行时模型，另请阅读 `permission-decision-ladder.md`。

## 会话恢复与继续

| Claude Code 工作流 | Codex Status | Codex 机制 | 在 Codex 中的操作方式 | Boundary |
| --- | --- | --- | --- | --- |
| 恢复先前基于对话记录的会话 | approximate | 从文件、计划、笔记和 git 状态重建上下文 | 手动重建工作状态并继续 | 不保证提供 Claude 风格的对话记录恢复原语 |

推荐模式：

1. 读取最新的计划或笔记文件。
2. 检查 git status 和已更改文件。
3. 重新声明已恢复的上下文。
4. 从恢复的检查点继续。

关于压缩、保留上下文和恢复正确性背后更深层的运行时模型，另请阅读 `context-hygiene.md`。

## 审查流程

| Claude Code 工作流 | Codex Status | Codex 机制 | 在 Codex 中的操作方式 | Boundary |
| --- | --- | --- | --- | --- |
| 本地审查或 PR 审查 | direct | Codex 审查模式 | 检查 diff 并产出以发现为先的审查输出 | 实际效果相同，UI 不同 |
| 深度云端审查 (`ultrareview`) | approximate | 更强的本地审查 | 进行更深入的本地审查并说明远程审查不可用 | 远程 Claude-on-the-web 路径不存在 |

## Agent 和委托流程

| Claude Code 工作流 | Codex Status | Codex 机制 | 在 Codex 中的操作方式 | Boundary |
| --- | --- | --- | --- | --- |
| 生成子 agent 进行并行工作 | approximate | 仅在明确请求时使用委托 agent | 仅在用户明确允许且有限定范围的子任务时使用委托 agent | Codex 委托不是通用的始终开启 agent 群 |
| 团队、对等、伙伴、邮箱工作流 | unavailable | 无 | 无 | 无等价的对等消息或群邮箱界面 |

规则：

- 不要仅因为 Claude Code 会这样做就生成 agent。
- 委托需要用户明确许可。
- 将主任务保持在主线程上，除非子任务明显可并行化。
- 即使允许委托，也要先声明映射。

## MCP 工作流

| Claude Code 工作流 | Codex Status | Codex 机制 | 在 Codex 中的操作方式 | Boundary |
| --- | --- | --- | --- | --- |
| 使用 MCP 工具和资源 | approximate | 使用环境已暴露的任何 MCP 工具/资源 | 直接使用资源和工具，但将运行时使用与服务器管理和入站通知预期分开 | 服务器生命周期、认证/重连行为和入站通知控制可能与 Claude Code 不一致 |
| 通过斜杠或 CLI 流程添加或移除 MCP 服务器 | unavailable 或 approximate | 取决于环境 | 仅在明确可用时编辑配置文件或使用宿主工具 | 无通用的 Codex 端 MCP 管理命令 |

关于运行时使用、服务器管理和通道式入站控制之间更深层的运行时差异，另请阅读 `mcp-runtime-and-inbound-control-plane.md`。

## 插件与 Skill 工作流

| Claude Code 工作流 | Codex Status | Codex 机制 | 在 Codex 中的操作方式 | Boundary |
| --- | --- | --- | --- | --- |
| 安装或管理 Claude 插件 | approximate | Codex skill 和插件（如可用） | 将用户目标转化为 skill 或插件操作 | 插件架构不等价 |

规则：

- 如果用户想要可复用的 Codex 行为，优先选择 skill。
- 如果用户想要打包或市场机制，说明不匹配之处。

## Worktree 和分支工作流

| Claude Code 工作流 | Codex Status | Codex 机制 | 在 Codex 中的操作方式 | Boundary |
| --- | --- | --- | --- | --- |
| 进入 worktree 模式 | approximate | 手动 git worktree 命令 | 在需要时直接使用 git worktree | 无专用 worktree 模式命令 |
| 分支检查和切换 | direct | Git shell 工作流 | 使用 git 命令并汇总结果 | 实际效果相同 |

## 导出和检查点工作流

| Claude Code 工作流 | Codex Status | Codex 机制 | 在 Codex 中的操作方式 | Boundary |
| --- | --- | --- | --- | --- |
| 导出对话、检查点状态、压缩长会话 | approximate | 写入摘要文档或检查点文件 | 将相关状态持久化为工作区中的 Markdown 文件 | 无直接的对话记录导出或压缩原语 |

关于简单检查点文件与 Claude Code 清洁流水线之间的运行时差异，另请阅读 `context-hygiene.md`。
