# 能力边界

本文件说明为什么 skill 不能将 Claude Code 和 Codex 视为可互换的。

## 差异矩阵

| 领域 | Claude Code | Codex | 操作层面的影响 |
| --- | --- | --- | --- |
| 命令界面 | 丰富的斜杠命令和 CLI 命令模型 | 工具驱动的助手加 skill | 翻译用户意图，而非命令拼写 |
| 会话模型 | 终端 REPL，具备对话记录持久化、恢复、回退、压缩功能 | 对话线程加工作区制品 | 许多会话控制命令为 approximate 或 unavailable |
| 权限 | 面向用户的权限模式和提示 | 宿主管理的审批和沙箱策略 | 不要声称存在斜杠命令权限模型 |
| Agent 模型 | 内置的产品 agent 和群流程 | 委托可能存在，但仅限有界形式且通常需要明确许可 | Agent 命令通常为 approximate |
| MCP 管理 | 面向用户的服务器管理命令 | 环境可能暴露 MCP 工具/资源但不提供相同的管理 UI | 将 MCP 使用与 MCP 管理分开 |
| 插件 | Claude 插件和市场模型 | Codex skill/插件是不同的抽象 | 不要天真地映射插件命令 |
| UI 控制 | 终端 UI 模式、状态行、主题、贴纸、移动端配对 | 宿主 UI 控制不在 skill 范围内 | UI 命令通常为 unavailable |
| 远程和守护进程功能 | 桥接、守护进程、remote-control、云端审查、移动端交接 | 通常不存在 | 除非环境明确提供，否则标记为 unavailable |
| 账户界面 | 用量、通行证、隐私设置、认证命令 | 提供商/账户模型不同 | 计费/账户命令通常为 unavailable |

## 高风险翻译错误

避免以下错误：

- 将宿主管理的设置视为 skill 可以更改的
- 将 Claude 特定的每轮 diff 视为普通 `git diff` 具有完全对等性
- 将 Claude 的计划模式视为 Codex 具有相同的会话原语
- 声称 `/resume`、`/rewind` 或 `/compact` 在 Codex 中是一等的会话原语
- 将 Claude 插件管理视为等同于 Codex skill
- 因为 Claude Code 会自动生成委托 agent 就自动生成
- 将仅限远程/云端的命令映射到本地 shell 工作流而不说明能力损失

## Boundary 语言

使用如下表述：

- `direct`："Codex 可以直接做到这一点，但界面不同。"
- `approximate`："Codex 可以达到相同的目标，但通过不同的工作流。"
- `unavailable`："Codex 在当前环境中不提供此能力。"

避免如下表述：

- "与 Claude Code 相同"
- "等价"
- "直接用这个命令替代"

除非实际能力确实存在。
