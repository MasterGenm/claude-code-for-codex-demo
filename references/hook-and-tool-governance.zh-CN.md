# Hook And Tool Governance（Hook 与工具治理）

当请求涉及 `/hooks`、tool-event 自动化、权限中介、continuation 控制、MCP 输出变异或插件提供的运行时治理时，使用本文件。

## Claude Code 实际在做什么

Claude Code 的 hook 不只是配置条目或 shell 脚本片段。它们是工具运行时内部的治理层。

它们可以：
- 检查或重写工具输入
- 影响权限流程
- 向 transcript 注入额外上下文
- 在工具调用后停止 continuation
- 通过独立路径变异 MCP 工具输出
- 浮现警告或失败而不总是导致 turn 崩溃

关键源码锚点：
- `src/services/tools/toolHooks.ts:39` — `PostToolUse` hook 是一等执行阶段。
- `src/services/tools/toolHooks.ts:193` — `PostToolUseFailure` hook 有独立的失败路径。
- `src/services/tools/toolHooks.ts:322` — hook 的 `allow` 不会绕过基础设置和权限规则。
- `src/services/tools/toolHooks.ts:435` — `PreToolUse` hook 可以发出权限结果、更新后的输入和额外上下文。
- `src/services/tools/toolExecution.ts:800` — pre-tool hook 在最终权限解析之前运行。
- `src/services/tools/toolExecution.ts:979` — hook 驱动的权限决策会成为显式的 transcript 事件。
- `src/services/tools/toolExecution.ts:1073` — `PermissionDenied` hook 可以在拒绝后建议重试。
- `src/services/tools/toolExecution.ts:1397` — post-tool hook 在成功执行后运行，可以停止 continuation。
- `rust/crates/runtime/src/conversation.rs:143` — hook runner 是核心对话运行时的一部分。
- `rust/crates/runtime/src/conversation.rs:211` — pre hook 可以在执行前拒绝。
- `rust/crates/runtime/src/conversation.rs:230` — post hook 可以修改最终的 tool-result 路径。
- `rust/crates/plugins/src/hooks.rs:66` — 插件 hook 暴露显式的 pre-tool 执行。
- `rust/crates/plugins/src/hooks.rs:78` — 插件 hook 暴露显式的 post-tool 执行。
- `rust/crates/plugins/src/hooks.rs:95` — hook 命令通过结构化 payload 运行，而非原始自由文本。
- `rust/crates/plugins/src/hooks.rs:183` — hook 退出状态映射到 allow、deny 或 warn 行为。
- `rust/crates/plugins/src/lib.rs:685` — 已启用的插件将 hook 聚合到运行时控制面。

## 治理阶段

### 1. Pre-Tool 治理

此阶段可以：
- 检查请求的工具调用
- 重写输入
- 返回 allow、ask 或 deny 信号
- 在执行前添加额外上下文

关键不变量：
- hook 的 `allow` 不是绝对允许
- 基础权限策略仍然决定工具是否真正可执行

这意味着 Claude Code 将 hook 视为策略贡献者，而非策略独裁者。

### 2. Permission Mediation（权限中介）

Claude Code 合并：
- hook 结果
- 基于规则的权限
- 交互式提示或分类器路径
- 宿主或模式约束

这就是为什么关于 hook 的请求经常与 `/permissions` 或 `/config` 重叠。真正的问题往往不是"hook 文件在哪里？"而是"这个 hook 在决策阶梯的哪个位置起作用？"

### 3. Post-Tool 治理

工具调用成功后，hook 可以：
- 附加上下文
- 发出阻塞或警告消息
- 停止 continuation
- 通过 MCP 专用路径重写输出

重要边界：
- 输出变异不是通用的自由操作
- MCP 专用的输出重写应与普通的 tool-result 格式化分开

### 4. Failure 治理

失败 hook 是独立阶段，不只是带错误标志的 post hook。

它们可以：
- 标注失败
- 浮现重试指导
- 在不擦除底层失败的情况下添加上下文

这很重要，因为 Claude Code 不会将每个 hook 事件都视为致命的。

### 5. Error And Cancellation Policy（错误与取消策略）

Hook 取消和 hook 执行错误通常是可观测的运行时事件，不是静默丢弃，也不总是完全的硬失败。

这是对 Codex 最有价值的教训之一：
- 治理失败应当可观测
- 但治理层不应成为脆弱的单点故障，除非策略明确要求 fail closed

## Mapping 指导

### `/hooks`

保持 `approximate`。

翻译影响：
- 当实际配置面存在时，解释它
- 同时解释 Claude Code 的 hook 是运行时治理，不只是文件条目

### `/permissions`

保持 `approximate`。

翻译影响：
- 当涉及 hook 时，解释决策阶梯而不只是说"宿主管理的审批"

### `/config`

保持 `approximate`。

翻译影响：
- 区分 schema 层面的 hook 配置和运行时 hook 行为

### 插件与 MCP 请求

当用户询问插件或 MCP 时，不要把 hook 抹掉。

翻译影响：
- 插件生命周期可以改变活跃的运行时 hook
- MCP 工具输出可能经过 hook 中介
- 一些"插件安装"问题实际上是治理问题，不是包管理问题

## Codex 应学到什么

Claude Code 有价值的模式是：
- 工具不仅被执行
- 它们被治理

该治理有显式的阶段：
- pre-tool
- permission mediation
- post-tool
- failure handling
- 可观测的非致命错误

这是一个可复用的操作模型，应当塑造 Codex 解释最复杂 Claude Code 行为的方式。
