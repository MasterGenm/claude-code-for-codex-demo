# Claude Code for Codex

[English](README.md) | [简体中文](README.zh-CN.md)

把 Claude Code 的命令和工作流翻译成 Codex 能理解、能执行的流程，同时明确告诉你两者哪里一样、哪里不一样。

这个仓库打包的是一个 Codex skill，它主要做这些事：
- 把 Claude Code 的 slash 命令、CLI 子命令和常见工作流翻成 Codex 语义
- 强制走 `先映射，再确认，再执行` 的流程
- 每条映射都标成 `direct`、`approximate` 或 `unavailable`
- 不拿模糊话术糊弄边界
- 带上脚本，能持续检查和上游 Claude Code 快照有没有漂移

当前发布范围是 `v0.1`。这是一个能发布、能维护、带源码锚点的兼容 skill，不是 Claude Code 的完整复刻版。

## 这东西是干嘛的

Claude Code 和 Codex 有重合，但不是一回事：
- 命令名字不一样
- 有些流程只能近似迁移
- 有些 Claude Code 能力本来就是产品面能力，Codex 没法原样拥有

如果没有一层兼容翻译，最容易犯的错就是把 Claude Code 风格的问题，当成 Codex 也原生支持。这个 skill 的价值，就是专门防这种误判。

## 实际使用里，差别主要在哪

| 场景 | 不装 skill 时 | 装了 skill 后 | 直接差别 |
| --- | --- | --- | --- |
| `/help` | 一般也能答出来 | 一般也能答出来，但结构更稳 | 差距不大 |
| `/resume` | 容易解释得比较松 | 更会明确说明会丢什么 | 边界更清楚 |
| `claude mcp add` | 容易把运行时和管理面混在一起 | 更容易拆清楚层次 | hardest 场景更稳 |
| `remote-control` | 更容易讲成“类似替代” | 更容易直接说明不可用 | 更少伪等价 |
| `/compact` | 容易说成“做个摘要” | 更会按 context hygiene 来解释 | 机制理解更深 |

如果你想看更直观的总结，见：[`examples/with-vs-without-skill.zh-CN.md`](examples/with-vs-without-skill.zh-CN.md)  
如果你想看完整实验记录，见：[`examples/experiments/skill-comparison-experiment.zh-CN.md`](examples/experiments/skill-comparison-experiment.zh-CN.md)

## 仓库里有什么

仓库根目录本身就是可安装的 Codex skill 目录。安装时要拷整个目录，不是只拿 `SKILL.md`。

```text
claude-code-for-codex/
+-- README.md / README.zh-CN.md
+-- SKILL.md                          # Skill 入口：18 步决策流程
+-- agents/openai.yaml                # Codex agent 接口定义
+-- references/                       # 19 篇机制级文档（3000+ 行）
|   +-- command-mapping.md            # 100+ 条命令映射（direct/approximate/unavailable）
|   +-- workflow-mapping.md           # 工作流级迁移规则
|   +-- capability-boundaries.md      # 产品差异矩阵
|   +-- execution-policy.md           # 先映射、再确认、再执行的规则
|   `-- ...（另有 14 篇带上游源码锚点的机制参考）
+-- evals/                            # 9 套回归测试（500+ 测试用例）
+-- scripts/                          # 4 个维护工具，含上游漂移检测
|   +-- run_skill_evals.py            # 回归测试执行器
|   +-- check_mapping_consistency.py  # 上游漂移检测器
|   `-- ...
`-- examples/                         # 装/不装 skill 的对比 + 实验记录
```


## 这个 skill 会做什么

它会把 Claude Code 相关请求收敛成一套固定输出：

1. `Status`
2. `Codex mapping`
3. `Boundary`
4. `Execution path in Codex`

然后再询问你要不要继续执行。

核心参考：
- 命令映射：[`references/command-mapping.zh-CN.md`](references/command-mapping.zh-CN.md)
- 工作流映射：[`references/workflow-mapping.zh-CN.md`](references/workflow-mapping.zh-CN.md)
- 能力边界：[`references/capability-boundaries.zh-CN.md`](references/capability-boundaries.zh-CN.md)
- 执行策略：[`references/execution-policy.zh-CN.md`](references/execution-policy.zh-CN.md)
- 最难场景：[`references/integration-playbooks.zh-CN.md`](references/integration-playbooks.zh-CN.md)

机制层参考：
- 架构总览：[`references/architecture-lenses.zh-CN.md`](references/architecture-lenses.zh-CN.md)
- hooks 和工具治理：[`references/hook-and-tool-governance.zh-CN.md`](references/hook-and-tool-governance.zh-CN.md)
- registry 和优先级：[`references/registry-and-precedence.zh-CN.md`](references/registry-and-precedence.zh-CN.md)
- context hygiene：[`references/context-hygiene.zh-CN.md`](references/context-hygiene.zh-CN.md)
- 权限决策梯子：[`references/permission-decision-ladder.zh-CN.md`](references/permission-decision-ladder.zh-CN.md)
- MCP 运行时和入站控制面：[`references/mcp-runtime-and-inbound-control-plane.zh-CN.md`](references/mcp-runtime-and-inbound-control-plane.zh-CN.md)

## 这个 skill 不会做什么

它不会：
- 让 Codex 变成更强的基础模型
- 给 Codex 平白加上 Claude Code 的 daemon、mobile、voice、账号设置、remote-control server 这类产品面能力
- 替代普通编码、调试、测试、代码审查类 skill
- 在只能近似替代时，硬说成完全等价

如果某个能力在 Codex 里本来就不可靠或不存在，它就应该老老实实写 `unavailable`。

## Skill 设计理念

这个项目不是一张 cheatsheet，也不是一篇博客。它是一个结构化的翻译层 Agent Skill，有明确的设计决策：

| 设计维度 | 实现方式 |
| --- | --- |
| **决策框架** | 三态分类（`direct` / `approximate` / `unavailable`），每种状态有对应的执行规则 |
| **执行治理** | 先映射、再确认、再执行的策略，通过 SKILL.md 的输出规则强制执行 |
| **标准化输出** | 每次响应都按 Status → Mapping → Boundary → Execution path 的顺序 |
| **回归测试** | 9 套 fixture（500+ 用例），覆盖基础映射到机制级边界 |
| **可维护性** | 上游漂移检测脚本 + 从 Claude Code 源码提取命令注册表 |
| **知识深度** | 19 篇带源码锚点的参考文档，不是表面级别的摘要 |

这是一个**翻译层 Skill**——核心价值是系统化管理产品差异，而不是增加运行时能力。它和领域知识型 Skill（如 [rag-system-planner](https://github.com/MasterGenm/rag-system-planner-demo)）形成互补，展示了 Agent Skill 的另一种设计范式：跨产品语义兼容，而非领域知识结构化。

## 体现设计能力相关

| 能力维度 | 在项目中的体现 |
| --- | --- |
| 系统化产品分析 | 100+ 条命令用三态分类映射；每个 `approximate` 都说明丢了什么 |
| Agent Skill 设计方法论 | 结构化执行流程、输出合同、触发条件——不是一段 prompt，而是可复用的工作流资产 |
| 知识资产的工程严谨性 | 回归测试框架、上游漂移检测、自动化一致性检查 |
| 跨产品迁移思维 | 显式的边界管理，而不是模糊的"类似替代" |
| 源码级技术深度 | 19 篇参考文档锚定上游源码，不是表面级文档 |

### 还没做到的

- 没有行为级评测（当前评测是静态回归，不是模型输出的 judge）
- 没有 CI 自动化（脚本存在但需手动运行）
- 范围窄：只覆盖 Claude Code → Codex 方向，不是通用的跨产品迁移框架

## 当前发布边界

这次公开版包含：
- 一个可安装的 Codex skill，含 18 步决策流程（[`SKILL.md`](SKILL.md)）
- **100+ 条命令和工作流映射**，每条标为 `direct`、`approximate` 或 `unavailable`
- **19 篇机制级参考文档**（3000+ 行），带上游源码锚点
- 4 个维护脚本，含自动化上游漂移检测
- **9 套回归测试**（500+ 测试用例），放在 [`evals/`](evals)

这次公开版**不承诺**：
- 完整 Claude Code 等价
- daemon、mobile、voice、bridge、账号、remote-control 这类产品面能力
- Codex 里原生存在 transcript 风格的 resume / rewind / compact 原语
- 超出当前静态回归框架之外的完整行为评测

## 安装

### 方式 1：装到本机 Codex skills 目录

先 clone 仓库，再把整个目录拷到 Codex skills 目录里。

PowerShell：

```powershell
git clone https://github.com/MasterGenm/claude-code-for-codex-demo.git
New-Item -ItemType Directory -Force -Path $env:USERPROFILE\.codex\skills | Out-Null
Copy-Item -Recurse -Force .\claude-code-for-codex-demo `
  $env:USERPROFILE\.codex\skills\
```

### 方式 2：只给某个项目用

如果只想在某个仓库里用，把这个目录放到：

```text
.agents/skills/claude-code-for-codex
```

### 方式 3：配合 AGENTS.md 做默认路由

如果你希望某个工作区里，Claude Code 风格的请求默认走这个 skill，可以在 `AGENTS.md` 里加类似规则：

```md
Use $claude-code-for-codex when a request mentions Claude Code commands, migration from Claude Code to Codex, or a Claude Code workflow concept where semantic mismatch is likely.
```

## 怎么用

常见提示词：
- `Use $claude-code-for-codex to map /review into a Codex workflow`
- `How do I do claude mcp add in Codex?`
- `Rewrite this Claude Code runbook for Codex`
- `Map /resume into Codex and explain what is lost`

## 什么情况下该触发这个 skill

这些情况应该触发：
- 明确提到了 Claude Code 的 slash 命令或 CLI 子命令
- 在问 Claude Code 到 Codex 的迁移、对照、替代
- 用了 Claude Code 里的工作流概念，比如 `resume`、`compact`、对话 `branch`、`mcp`、`plugin install`
- 如果不先做映射判断，直接执行很容易误判

这些情况默认不该触发：
- 普通编码任务
- 普通调试和测试
- 没有 Claude Code 语义歧义的常规 git 操作

## 局限性与后续方向

| 当前局限 | 后续可能方向 |
| --- | --- |
| 只有静态回归，没有行为级评测 | 加 judge 机制评估模型输出质量 |
| 脚本手动执行，没有 CI | 加 GitHub Action 定期检查漂移 |
| 只覆盖 Claude Code → Codex 方向 | 泛化为通用跨产品 Skill 迁移框架 |
| 单次上游快照，没有持续追踪 | 自动化定期上游命令提取 |
