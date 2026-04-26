# Registry And Precedence（注册表与优先级）

当请求实际上是关于 Claude 式行为从哪里被发现、哪个定义胜出、或者为什么两个同名产物不会合并时，使用本文件。

本文件关注有序注册表、兼容性根、来源追踪和遮蔽。

## Claude Code 实际在做什么

Claude Code 不是通过单一的目录扫描来发现行为的。

它有多个有序的注册表：
- 指令文件
- 设置文件
- skill
- agent
- 兼容性根（如旧版 commands 目录）

关键源码锚点：
- `rust/crates/runtime/src/prompt.rs:192` — 指令文件沿祖先链被发现。
- `rust/crates/runtime/src/prompt.rs:204` — `CLAW.md`、`CLAW.local.md`、`.claw/CLAW.md` 和 `.claw/instructions.md` 都会被考虑。
- `rust/crates/runtime/src/prompt.rs:326` — 指令文件被去重而非盲目重复。
- `rust/crates/runtime/src/config.rs:197` — 设置发现是显式的、有序的、带来源标签的。
- `rust/crates/runtime/src/config.rs:204` — 用户设置在项目和本地层之前加载。
- `rust/crates/runtime/src/config.rs:220` — 本地设置是独立的最高优先级覆盖层。
- `rust/crates/commands/src/lib.rs:686` — agent 根跨项目和用户作用域被发现。
- `rust/crates/commands/src/lib.rs:727` — skill 根包括现代 skills 目录和旧版 commands 目录。
- `rust/crates/commands/src/lib.rs:829` — agent 按来源优先级被跟踪为 active 或 shadowed。
- `rust/crates/commands/src/lib.rs:872` — skill 同样被跟踪为 active 或 shadowed，保留来源信息。
- `src/skills/loadSkillsDir.ts:68` — 原始 TypeScript 系统区分 `skills`、旧版 `commands_DEPRECATED`、`plugin`、`managed`、`bundled` 和 `mcp` 来源。
- `src/skills/loadSkillsDir.ts:78` — 按来源的 skill 路径是显式的，不是临时推断的。
- `src/skills/loadSkillsDir.ts:726` — 原始系统按解析后的身份去重 skill 文件，采用先到先得行为。
- `src/skills/loadSkillsDir.ts:799` — 已加载的 skill 数量按来源类别跟踪，而非扁平化为一个集合。

## 真实的注册表模型

### 1. 指导发现是分层的

指令发现按祖先路径和文件类型排序。

这意味着：
- 仓库根目录可以贡献指导
- 嵌套目录可以贡献更具体的指导
- 本地和作用域化的指令文件可以共存
- 重复项应被去重，而非在 prompt 中重复回显

### 2. 设置是带来源标签的栈

设置不是一个 JSON 文件。

它至少有这些层：
- user
- project
- local

操作影响：
- 后面的层可以覆盖前面的层
- 来源很重要
- "我应该在哪里编辑这个？"是一个控制面问题，不是外观偏好

### 3. Skill 和 Agent 来自有序的根

`claw-code` 模型明确了顺序：
- 项目 `.codex`
- 项目 `.claw`
- 用户 `$CODEX_HOME`
- 用户 `~/.codex`
- 用户 `~/.claw`

对于 skill，兼容性根还包括：
- 现代 `skills/`
- 旧版 `commands/`

这意味着一个定义不只是"存在"或"不存在"。它存在于某个带优先级的来源处。

### 4. First-Wins 遮蔽

当两个 skill 或 agent 共享相同的有效名称时：
- 较早的来源胜出
- 较晚的来源仍然可见，作为被遮蔽的来源信息
- 它们不会静默合并

这是 Claude Code 最重要的教训之一。

用户侧的影响：
- "为什么我的 skill 没生效？"可能真正意味着"它存在，但被遮蔽了"
- "我应该把这个放在哪里？"取决于该行为应该覆盖项目、个人还是兼容性定义

### 5. 兼容性根是真实的输入

旧版命令目录不是历史冷知识。

它们仍然重要，因为：
- 保留了旧的工作流打包方式
- 提供迁移连续性
- 参与发现和命名冲突

Codex 应该认识到兼容性根是真实运行时面的一部分，而非仅仅是过时文件。

## Mapping 指导

### `/skills`

保持 `direct`，但在需要时解释注册表模型。

翻译影响：
- Codex 可以直接使用 skill
- 更深层的解释涉及发现根、优先级和遮蔽

### `/agents`

保持 `approximate`。

翻译影响：
- 解释可用的委托角色
- 同时解释 Claude 式 agent 定义存在于带来源优先级的有序注册表中

### `/init`

保持 `approximate`。

翻译影响：
- 决定新行为应放在哪里通常是一个注册表问题：
  - 共享仓库指导
  - 本地指导
  - skill
  - agent
  - 设置覆盖

### 插件与扩展问题

注册表逻辑也影响插件和 skill 打包问题。

翻译影响：
- 安装不等于激活
- 激活不等于赢得优先级
- 兼容性目录和本地覆盖可以影响可见的运行时面

## Codex 应学到什么

Claude Code 有用的教训是：
- 行为存在于注册表中
- 注册表有有序的根
- 根有来源追踪
- 优先级是显式的
- 重复项被遮蔽，不会神奇地合并

这个操作逻辑值得跨项目学习，因为它改善了：
- 产物放置决策
- 迁移说明
- "为什么这个指令或 skill 没生效？"的调试
- 对仓库级行为的可信解释
