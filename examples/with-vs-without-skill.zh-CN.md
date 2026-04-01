# 装这个 Skill 和不装，到底差在哪

[English](with-vs-without-skill.md) | [简体中文](with-vs-without-skill.zh-CN.md)

这页文档对比的是同一批 Claude Code 风格请求下，两种回答方式的区别：
- 普通 Codex 回答
- 装上 `claude-code-for-codex` 之后的回答

如果你想看原始实验记录，见：[`experiments/skill-comparison-experiment.zh-CN.md`](experiments/skill-comparison-experiment.zh-CN.md)

## 实验怎么做的

我们拿同样 5 个问题做了成对对照：
- `/help`
- `/resume`
- `claude mcp add`
- `remote-control`
- `/compact`

先说清楚实验边界：
- 这次实验是在当前这个已经偏 skill 化的工作区里做的
- 所以“普通组”其实比真正的白板环境更强
- 但这个结果反而更贴近你以后真实的使用环境

## 真正的区别是什么

### 1. 简单请求，差距不算特别大

像 `/help` 这种相对直接的问题，两边其实都能答到点上。  
所以这个 skill 不是每个问题都会拉开巨大差距。

### 2. 一到“近似替代”场景，差距就出来了

像 `/resume`、`/compact` 这种问题，装了 skill 之后的回答会更稳定地说明：
- Claude Code 原动作到底是什么
- Codex 里现在只能怎么近似做
- 过程中会丢什么

这类问题最怕的不是不会答，而是答得太轻飘，听起来像完全等价。

### 3. hardest 场景会拆得更清楚

`claude mcp add` 是最明显的例子。  
装了 skill 之后，更容易把事情拆成：
- MCP 运行时使用
- MCP 管理配置
- 当前宿主到底有没有可写的配置面

不这样拆，就很容易一句“我帮你配 MCP”带过去，但其实边界没讲清。

### 4. 不可用能力会处理得更干净

`remote-control` 就属于这种。  
装了 skill 之后，会更明确地告诉你：
- 没有就是没有
- 缺的是整套控制面，不是只缺一个命令名
- 不会用一些相似但不等价的办法来硬装成“差不多能用”

这点其实很值钱，因为它能减少误判。

### 5. 回答结构更稳定，可复用性更强

装了 skill 后，回答会更稳定地按这 4 步来：
1. `Status`
2. `Codex mapping`
3. `Boundary`
4. `Execution path in Codex`

这意味着它不是“这次碰巧答得好”，而是以后同类问题都更容易保持同一标准。

## 结论

这个 skill 不会让 Codex 换一个更强的大脑。

但它会让 Codex 在 Claude Code 相关任务上明显更专业：
- 更不容易把近似方案说成等价方案
- 更会讲边界
- 更会拆 hardest 场景
- 回答更稳，更适合长期反复使用

普通编码任务里，差距不会特别大。  
但在 Claude Code 迁移、命令翻译、工作流对照、边界判断这些场景里，提升是很明显的。
