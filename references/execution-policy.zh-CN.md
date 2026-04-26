# 执行策略

在映射决策完成后使用本文件。

## 核心规则

本 skill 遵循 `map first, confirm, execute`（先映射，再确认，后执行）。

具体含义：

1. 识别 Claude Code 命令或工作流
2. 将其分类为 `direct`、`approximate` 或 `unavailable`
3. 声明 boundary
4. 在执行仍然可行时请求明确确认
5. 然后才执行任务

不要仅因为用户明显想要执行就跳过第 2 或第 3 步。
不要将用户最初的"立即执行"措辞视为映射后确认。

## 过渡规则

### 如果用户只要求翻译

- 在给出 execution path 后停止。
- 不要运行工具或 shell 命令。

### 如果用户要求立即执行任务

- 仍然先呈现 mapping 块。
- 然后停止并提出一个简洁的确认问题。

### 如果用户在看到映射后明确确认

- 仅在映射路径被下方 status 规则允许时才继续。

## Status 规则

### `direct`

- 必须进行映射。
- 仅在映射后明确确认后才可执行。
- 直接使用映射的 Codex 机制。

示例：

- `/help` -> 可用工具汇总
- `/doctor` -> 本地诊断
- `/skills` -> Codex skill 列表

### `approximate`

- 必须进行映射。
- 在提出操作方案之前先说明损失的能力。
- 仅在映射后明确确认且近似方案仍能满足实际目标时才可执行。
- 如果近似损失过大，停止并将其视为实际上不可用。

示例：

- `/diff` -> 带有每轮 diff 损失的 git diff 审查
- `/plan` -> 规划工作流加计划文档
- `/compact` -> 写入检查点摘要
- `/resume` -> 从计划、笔记和 git 状态重建上下文
- `/plugin install` -> 使用最接近的 Codex skill 或插件工作流

### `unavailable`

- 必须进行映射。
- 不得执行。
- 解释为什么该能力在当前 Codex 环境中不可用。

示例：

- `/remote-control-server`
- `/voice`
- `claude server`
- `claude auth login`

## Execution Path 语言

描述 execution path 时，说明将使用哪个 Codex 机制：

- skill
- shell 工作流
- 仓库检查
- 审查工作流
- 规划工作流
- 委托 agent 工作流
- unavailable

路径要足够具体，以便用户确认后 Codex 能在下一轮中据此执行。

## 反模式

不要：

- 将映射和执行视为同一步骤
- 将用户最初的执行请求视为确认
- 在未先说明只是近似方案的情况下自动运行回退
- 在 `unavailable` 结果之后继续执行
- 暗示宿主管理的 UI 或账户操作可以在本地模拟（实际上不能时）
