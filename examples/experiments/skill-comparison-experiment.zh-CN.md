# 装技能和不装技能的对照实验记录

[English](skill-comparison-experiment.md) | [简体中文](skill-comparison-experiment.zh-CN.md)

这页不是总结页，而是实验记录页。

目的很简单：把“装了 `claude-code-for-codex` 和没装时，到底差在哪”这件事，尽量按原始过程记下来。

## 实验目的

验证这套 skill 到底有没有带来真实体验提升，重点看：
- 会不会更先讲清楚能不能做
- 会不会把近似替代说成等价实现
- hardest 场景会不会拆得更清楚
- 输出是不是更稳定、更适合长期复用

## 实验边界

这次实验不是白纸环境下做的，必须先说明：
- 实验发生在当前这个已经偏 skill 化的工作区里
- 当前工作区本身就有 `AGENTS.md` 路由规则
- 所以“普通组”其实也比完全没装任何 skill 的白板环境更强

换句话说，这份记录更接近“你现在真实使用环境里的对比”，不是纯学术隔离实验。

## 测试提示词

一共用了 5 个问题：

1. `帮我把 Claude Code 的 /help 翻成 Codex 里的做法。`
2. `帮我把 Claude Code 的 /resume 翻成 Codex 里的做法，并说明会丢什么。`
3. `帮我把 claude mcp add 翻成 Codex 里的做法。`
4. `Codex 里有没有 Claude Code 的 remote-control？`
5. `帮我比较一下 Claude Code 的 /compact 和 Codex 的上下文处理。`

## 实验分组

### A 组：普通回答

要求：
- 不显式使用 `claude-code-for-codex`
- 不查 skill 文件
- 用正常 Codex 风格回答

### B 组：技能回答

要求：
- 强制使用 `claude-code-for-codex`
- 按 skill 要求的固定顺序回答
- 不执行动作，只做映射说明

## 一眼看懂版对照表

| 测试项 | 普通回答组 | 技能回答组 | 直接观察 |
| --- | --- | --- | --- |
| `/help` | 能答出大概做法 | 能答出做法，而且结构更固定 | 简单场景差距不大 |
| `/resume` | 会说能恢复上下文，但更像经验型解释 | 会明确讲“这是近似恢复，不是原生恢复” | 技能组边界更稳 |
| `claude mcp add` | 会说看宿主配置，但容易一句话带过 | 会更明确拆成管理面和运行时面 | 技能组更会拆 hardest 场景 |
| `remote-control` | 可能会给一些替代协作方式 | 会更干脆地说明不可用 | 技能组更不容易伪等价 |
| `/compact` | 会说成“做个摘要”或 checkpoint | 会更明确说明这是 context hygiene 的近似替代 | 技能组机制理解更深 |

## A 组结果：普通回答

### Prompt 1

`/help` 是 `direct`：Codex 没有单独的 slash 帮助页，但你可以直接问我当前能用的工具、技能和工作流。我会按当前环境把可用能力、限制和推荐做法说清楚。边界就是没有 Claude Code 那种专门的 `/help` UI；执行上就是让我概述当前会话能做什么。

### Prompt 2

`/resume` 是 `approximate`：Codex 可以从当前工作区、计划、笔记和 `git` 状态里重建上下文继续做，但没有 Claude Code 那种原生 transcript 恢复流。会丢的是会话级的精确连续性，比如 compact 边界、选择性附件重放、以及自动恢复后的原样上下文。实际做法是我先读最近的计划或说明，再看变更和工作区状态，然后从那个检查点继续。

### Prompt 3

`claude mcp add` 是 `approximate`：如果当前环境里有可编辑的 MCP 配置，我就去改那个真实配置；如果没有，就只能停在翻译层面，不能像 Claude Code 那样一条命令直接加。边界在于 Codex 可能能用 MCP 工具，但不等于有同等的 MCP 管理 CLI。执行上就是先确认具体的配置文件或宿主入口，再把 server 定义写进去。

### Prompt 4

没有，`remote-control` 在 Codex 里是 `unavailable`。Codex 不暴露 Claude Code 那种把本地终端挂到远程桥接会话上的控制平面。你可以用普通 `ssh`、共享工作区或把状态写回文件来替代，但那不是同类功能。

### Prompt 5

`/compact` 在 Codex 里是 `approximate`：Claude Code 的 compact 是一套多阶段的上下文收缩和恢复机制，不只是把内容压成摘要。Codex 更像手动 checkpoint，把已完成的上下文总结到消息或文件里，再从那里继续。少掉的是原生的分层压缩、最近消息保留和附件重建能力，所以连续性和自动恢复没法做到同级。

## B 组结果：装上 skill 的回答

### Prompt 1

`Status`：直接对应  
`Codex mapping`：普通助手回答加上对本地 skill / tool 的感知；直接问 Codex 当前有哪些工具、技能和工作流可用。  
`Boundary`：没有专门的 slash help 界面，但实际想达到的效果可以直接做到。  
`Execution path in Codex`：让 Codex 列出当前环境下可用的工具、技能和相关工作流。

### Prompt 2

`Status`：近似对应  
`Codex mapping`：从当前线程、工作区文件、计划、笔记和 git 状态里重建之前的状态。  
`Boundary`：没有 Claude 那种基于 transcript 的 resume 流程，也没有基于 transcript 边界的过滤，以及 compact 之后的附件恢复。  
`Execution path in Codex`：先读最新的笔记或计划，再看 `git status` 和变更文件，重新表述恢复出来的上下文，然后从这个检查点继续。

### Prompt 3

`Status`：近似对应  
`Codex mapping`：通过真实可编辑的 MCP 配置来做 MCP 管理；如果当前环境有 MCP 管理流程，也可以走宿主环境自己的管理方式。  
`Boundary`：Codex 没有和 `claude mcp add` 一样的 CLI 界面，而且运行时使用 MCP 和管理 MCP 是两回事。  
`Execution path in Codex`：先检查当前宿主里实际可用的 MCP 配置入口，如果环境提供可写配置，再把 server 加进去。

### Prompt 4

`Status`：不可用  
`Codex mapping`：无。  
`Boundary`：Codex 没有提供 Claude Code 那种 remote-control bridge，也没有等价的会话附着能力。  
`Execution path in Codex`：无。

### Prompt 5

`Status`：近似对应  
`Codex mapping`：`/compact` 在 Codex 里对应的是手动做一个 checkpoint 摘要；Codex 的上下文处理更像线程上下文加工作区材料，而不是内建的 compact 流水线。  
`Boundary`：Codex 缺少 Claude Code 那种多轮 compact、选择性恢复和 continuation protocol。  
`Execution path in Codex`：先写一个简洁的 checkpoint 摘要；如果有需要就落到文件里，然后基于这个摘要继续，同时重新读取相关文件、计划和 git 状态。

## 直接观察到的差异

### 1. 简单问题差距不大

`/help` 这种问题，两边都能答得不错。  
这说明 skill 不是所有场景都会带来巨大差距。

### 2. 近似替代场景，技能组更稳

在 `/resume` 和 `/compact` 上，技能组更稳定地把“原能力”和“替代路径”分开说清楚。  
普通组也能答到点上，但更像临场发挥。

### 3. hardest 场景，技能组更会拆层

`claude mcp add` 是最明显的。  
技能组更稳定地把它拆成“管理面”和“运行时面”，不容易一句话带过。

### 4. 不可用能力，技能组更干净

`remote-control` 这个例子里，普通组给了 `ssh`、共享工作区这类替代思路。  
这些替代思路不是没用，但容易让人误以为“差不多能替代”。  
技能组在这里更干脆：没有就是没有。

## 结论

这次实验不能证明“装 skill 后 Codex 会换一个更强模型”。  
它证明的是另一件更实际的事：

- 装了 skill 后，Claude Code 风格请求更不容易答偏
- 更不容易把近似替代说成等价实现
- hardest 场景更容易拆清楚
- 输出结构更稳定，更适合长期反复使用

普通编码任务里，这种差距不会特别大。  
但在 Claude Code 迁移、命令翻译、工作流对照、边界解释这些任务里，提升是明显的。
