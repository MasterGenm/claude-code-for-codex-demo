# Permission Decision Ladder（权限决策阶梯）

当请求涉及以下内容时使用本文件：`/permissions`、`/sandbox`、危险等级、审批提示、只读与写行为，或者为什么 Claude Code 在命令看起来无害时仍要求权限。

这不仅仅是一个设置问题，而是一个运行时风险排序问题。

## Claude Code 实际在做什么

Claude Code 的权限不是一个简单的"模式开关"。它们是一个有序阶梯，结合了：

- 基于规则的 deny 和 ask 决策
- 内部路径豁免
- 危险文件和危险命令的安全门
- 工作目录边界
- 工具级别的只读允许列表
- shell 解析错误和命令注入检查
- 基于模式的快速通道
- 显式 allow 规则
- 分类器或提示升级处理剩余情况

这就是为什么许多 Claude Code 权限请求在 Codex 中应当保持 `approximate`，即便用户看到的权限界面表面上相似。

## Source Anchors

反向工程的 Claude Code 镜像：
- `src/utils/permissions/filesystem.ts:1205` - 文件写入经过一个有序的权限阶梯，而非扁平的模式检查。
- `src/utils/permissions/filesystem.ts:1223` - deny 规则在所有后续写检查之前运行。
- `src/utils/permissions/filesystem.ts:1244` - 内部可写路径在危险路径检查之前被豁免。
- `src/utils/permissions/filesystem.ts:1262` - `.claude/**` 会话级 allow 规则在通用安全阻断之前检查。
- `src/utils/permissions/filesystem.ts:1305` - 安全检查在 ask 规则、模式快速通道和普通 allow 规则之前运行。
- `src/utils/permissions/filesystem.ts:1367` - `acceptEdits` 仅在允许的工作目录内自动放行写操作。
- `src/tools/BashTool/bashPermissions.ts:1073` - shell 模式验证是权限评估的一部分，不是事后补充。
- `src/tools/BashTool/bashPermissions.ts:2229` - bash deny 和 ask 规则必须在路径检查之前运行以防止绕过。
- `src/tools/BashTool/bashPermissions.ts:2248` - 一个被 deny 的子命令会导致整个复合命令被拒绝。
- `src/tools/BashTool/bashPermissions.ts:2338` - 即使子命令看起来被允许，命令注入检查仍可阻止自动放行。
- `src/tools/BashTool/bashSecurity.ts:2109` - 引号内换行检查被视为解析敏感的安全检查。
- `src/tools/BashTool/bashSecurity.ts:2392` - 非解析类 ask 被推迟，以确保解析器差异检查优先。
- `src/utils/shell/readOnlyCommandValidation.ts:104` - 只读 shell 行为由显式允许列表支撑，不是模糊的"安全命令"启发式。
- `src/utils/shell/readOnlyCommandValidation.ts:1562` - UNC 路径检测是权限和数据泄露防御的一部分。

`claw-code` 洁净室运行时：
- `rust/crates/runtime/src/permissions.rs:89` - 授权建模为当前模式与每个工具所需模式的比较。
- `rust/crates/runtime/src/permissions.rs:108` - 部分升级会提示用户而非静默拒绝或允许。
- `rust/crates/tools/src/lib.rs:165` - 工具注册表显式暴露所需权限。
- `rust/crates/tools/src/lib.rs:219` - 内置工具被类型化为 read-only、workspace-write 或 danger-full-access，而非临时推断。

## 1. 文件权限阶梯

对于文件读写，真实的执行顺序比模式名称更重要。

### 写路径

写阶梯实际上是：

1. deny 规则
2. 内部可编辑路径豁免
3. 窄范围的 `.claude/**` 会话 allow 规则
4. 危险文件、危险目录、可疑 Windows 路径技巧和 UNC 类路径的安全检查
5. ask 规则
6. 模式快速通道如 `acceptEdits`，但仅限允许的工作目录内
7. 显式 allow 规则
8. 工作目录提示及建议

为什么这很重要：
- 宽泛的 allow 不是 Claude Code 首先检查的内容
- 危险配置路径在普通 allow 逻辑之前被刻意保护
- 内部 plan、scratchpad、memory 和 agent 路径被视为一等运行时豁免

### 读路径

读阶梯类似但更窄：

1. deny 规则
2. 可读的内部路径
3. allow 规则
4. 工作目录快速通道
5. 工作目录外提示及 `Read(...)` 建议

为什么这很重要：
- "只读"不意味着"任何地方都可读"
- Claude Code 仍然按工作目录和特殊内部存储限定读取范围

## 2. Shell 权限阶梯

Shell 执行在通用权限模型之上叠加了第二层阶梯。

Shell 路径实际上是：

1. 精确或前缀规则检查
2. deny 和 ask 规则在路径约束之前
3. 复合命令防护，如多 `cd` 明确性检查和 `cd && git` 攻击防御
4. 对原始命令的路径和重定向验证
5. 模式验证
6. 子命令合并和精确匹配 allow 检查
7. 命令注入和解析器差异安全检查
8. 分类器交接或对剩余未决情况的显式提示

为什么这很重要：
- 一个命令可以"被规则允许"但仍被结构性安全检查阻断
- 宽泛的 shell 权限是一个爆炸半径决策，不只是一个便利开关
- 只读 shell 行为依赖显式的安全命令表和标志验证，不只是命令名称

## 3. 安全和解析错误阶梯

并非每个 `ask` 都意味着同样的事情。

Claude Code 至少区分两类：

- 普通 ask
  示例：工作目录提示、显式 ask 规则、配置边界提示
- 解析敏感或注入敏感 ask
  示例：引号内换行技巧、注释-引号失同步、危险替换、畸形 token 注入

这个区分很重要，因为解析敏感 ask 被设计为在后续快捷逻辑中存活。它们不是普通的"也许允许"提示。

操作影响：
- 将 Claude Code 权限行为翻译到 Codex 时，不要将每个审批都描述为通用模式提示
- 某些权限提示实际上是安全回路行为

## 4. 爆炸半径和模式语义

模式是粗粒度的信封，不是完整的策略。

`claw-code` 用以下方式明确了这一点：
- `read-only`
- `workspace-write`
- `danger-full-access`
- 加上面向提示的升级

更完整的 Claude Code 镜像展示了为什么单靠这些仍然不够：
- 规则来源很重要
- 路径类别很重要
- shell 结构很重要
- 安全验证器很重要
- 工作目录范围很重要

所以正确的心智模型是：

- 模式决定了*可能*有多大权力
- 阶梯决定了某个具体操作是否真正获得该权力

## 5. Mapping 指南

### `/permissions`

保持 `approximate`。

用这个视角来说明：
- 当前 Codex 宿主的审批模型是什么
- 哪些部分由宿主控制
- Claude Code 内部有比单个斜杠命令所暗示的更精细的阶梯

### `/sandbox`

保持 `unavailable`。

原因：
- sandbox 切换在 Codex 中由宿主控制
- Claude Code 的内部阶梯并不意味着存在可移植的 skill 级 sandbox 开关

### `/config` 和 `/settings`

保持 `approximate`。

原因：
- 配置编辑可能涉及权限默认值或信任选择
- 但 Codex 应只编辑实际存在的真实配置产物

### "Claude 为什么要问权限？"

回复前先查阅本参考文档。

正确答案通常取决于：
- 危险路径
- 工作目录边界
- shell 结构防护
- 解析敏感验证器
- 或从 workspace-write 到 danger-full-access 的模式升级

## Codex 应该学到什么

Claude Code 持久的教训不是"更多权限命令"，而是更好的风险排序习惯：

- deny 先于便利
- 特殊内部路径先于宽泛的目录授权
- 安全先于 allow
- 结构感知的 shell 检查先于快速通道
- 爆炸半径先于界面措辞

这是值得提炼到 Codex 中作为操作技能的部分。
