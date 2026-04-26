# 命令映射

覆盖范围说明：

- 本文件涵盖逆向工程项目文档和命令注册表中暴露的面向用户的 Claude Code 斜杠命令和 CLI 子命令。
- 命令按操作领域分组，便于维护。
- 规范命令行在此维护；别名和可见性说明见 `aliases-and-visibility.md`。
- Status 含义严格限定为：
  - `direct`
  - `approximate`
  - `unavailable`

## 斜杠命令：核心会话与上下文

| Claude 命令 | 意图 | Status | Codex 机制 | 在 Codex 中的操作方式 | Boundary | 回退方案/原因 |
| --- | --- | --- | --- | --- | --- | --- |
| `/help` | 显示可用操作 | direct | 常规助手响应，加上本地 skill 和工具感知 | 汇总当前环境中可用的工具、skill 和工作流选项 | 无专用斜杠帮助 UI | 询问 Codex 有哪些可用工具和 skill |
| `/clear` | 清除对话历史并释放上下文 | approximate | 新线程或显式作用域重置 | 开启新线程，或指示 Codex 忽略先前上下文并重新描述任务 | Codex 不提供在原位重置对话记录状态的斜杠命令 | 用新线程或作用域重置来近似实现 |
| `/exit` | 退出 Claude 终端会话 | unavailable | 无 | 无 | 聊天或会话生命周期由宿主 UI 管理，不属于 skill 范畴 | 不可用：会话终止不受 skill 逻辑控制 |
| `/status` | 显示 Claude Code 状态，包括版本、模型、账户、API 连通性和工具状态 | approximate | 环境和工作区状态汇总 | 汇总 cwd、分支、可见的模型信息、相关工具可用性和环境约束 | Codex 不提供相同的集成账户或 API 状态面板 | 用环境汇总来近似实现 |
| `/session` | 显示远程会话 URL 和二维码 | unavailable | 无 | 无 | 此命令仅限上游远程使用，依赖远程配对界面 | 不可用：Codex 不提供通用远程会话 URL 或二维码流程 |
| `/stats` | 显示 Claude Code 使用统计和活动 | unavailable | 无 | 无 | Codex 不提供此使用活动界面的公开等价物 | 不可用：产品指标未作为斜杠工作流暴露 |
| `/usage` | 显示计划用量限制 | unavailable | 无 | 无 | 计划用量是账户管理的 Claude 界面，不是通用 Codex 运行时原语 | 不可用：用量限制由产品管理 |
| `/extra-usage` | 配置额外用量以在达到限制时继续工作 | unavailable | 无 | 无 | 这是账户和计费控制界面，不是工作区操作 | 不可用：额外用量控制由产品管理 |
| `/cost` | 显示当前会话的总费用和持续时间 | unavailable | 无 | 无 | 在此 skill 上下文中，Codex 不提供用户级别的会话费用和持续时间界面 | 不可用：定价遥测不公开提供 |
| `/export` | 将当前对话导出到文件或剪贴板 | approximate | 工作区导出文档 | 在工作区中生成结构化的对话记录或摘要文件，或返回可复制的导出块 | 不是一等的对话记录导出器或剪贴板写入器 | 用写入导出文档来近似实现 |
| `/copy` | 将 Claude 的上一条回复复制到剪贴板 | approximate | 重新输出请求的内容 | 以可复制的块形式重复相关内容，当用户要求时包括特定的早期回复 | 剪贴板控制由宿主管理 | 用返回精确文本来近似实现 |
| `/rename` | 重命名会话 | unavailable | 无 | 无 | 线程命名由宿主管理 | 不可用：无 skill 级别的会话重命名界面 |
| `/files` | 列出当前上下文中的所有文件 | approximate | 上下文文件汇总 | 汇总已触及、已读取、已附加或与当前任务密切相关的文件 | Codex 不提供 Claude Code 的精确上下文内文件集，且此命令在上游仅限 `ant` 使用 | 用已触及文件汇总来近似实现 |
| `/diff` | 查看未提交的更改和每轮 diff | approximate | Git diff 审查 | 检查 `git diff`，汇总更改并引用文件 | Codex 可以检查工作树 diff，但不提供 Claude Code 的每轮 diff 界面 | 用 git diff 审查来近似实现 |
| `/context` | 显示当前上下文使用情况 | approximate | 上下文预算汇总 | 汇总当前任务上下文、已触及文件和任何可见的上下文压力信号 | 无彩色网格或精确的 token 使用可视化 | 用上下文使用汇总来近似实现 |
| `/memory` | 编辑 Claude 记忆文件 | approximate | 工作区指导文件 | 在明确要求时读取或更新项目指导文件，如 `CLAUDE.md`、本地笔记或其他持久化指令 | Codex 不提供 Claude 的专用记忆文件管理器 | 用工作区文件来近似实现 |
| `/compact` | 缩减对话大小 | approximate | 手动摘要 | 对已完成的上下文进行摘要，必要时持久化到文件，然后从摘要继续 | 无对话记录压缩原语 | 用检查点摘要来近似实现 |
| `/rewind` | 将代码和/或对话恢复到先前的某个点 | approximate | 显式回滚方案 | 重新声明先前的检查点，放弃当前方案，从恢复的计划或工作区状态继续 | 无会话级别的代码或对话记录回退原语 | 用指令级别的重置和手动工作区回滚来近似实现 |
| `/resume` | 恢复先前的对话 | approximate | 现有线程加本地制品 | 从文件、计划、笔记和 git 状态重建上下文 | 无 Claude 风格的对话记录恢复流程 | 用从工作区状态手动恢复来近似实现 |

## 斜杠命令：规划、审查与分析

| Claude 命令 | 意图 | Status | Codex 机制 | 在 Codex 中的操作方式 | Boundary | 回退方案/原因 |
| --- | --- | --- | --- | --- | --- | --- |
| `/plan` | 启用计划模式或查看当前会话计划 | approximate | 规划工作流加计划文档 | 创建或更新计划，跟踪步骤，在有用时将计划文档存储在 `docs/plans/` 下 | Codex 可以有效规划，但不提供 Claude 的会话级别计划模式原语 | 用规划工作流加持久化计划文档来近似实现 |
| `/review` | 审查拉取请求 | approximate | PR 审查工作流 | 在 `gh` 可用时通过它审查拉取请求，或审查已检出的 diff 并说明限制 | Codex 不提供相同的 PR 范围斜杠工作流或保证的 GitHub 集成界面 | 用 PR 审查工作流来近似实现 |
| `/ultrareview` | 云端重度深度审查 | approximate | 仅限本地深度审查 | 进行彻底的本地审查，并说明远程 Claude-on-the-web 审查不可用 | 远程执行界面不同 | 用更强的本地审查来近似实现 |
| `/security-review` | 安全导向的审查 | direct | 安全审查工作流 | 以安全为重点审查更改，指出漏洞利用路径和信任边界 | UI 不同 | 使用带安全重点的标准审查工作流 |
| `/doctor` | 诊断和验证 Claude Code 安装及设置 | approximate | 本地健康检查 | 运行有针对性的 shell 检查，检查配置，并报告问题及修复方案 | Codex 可以诊断本地环境，但无法完全等同于 Claude 特定的安装状态检查 | 用仓库和环境诊断来近似实现 |
| `/insights` | 分析会话历史 | unavailable | 无 | 无 | Codex 不提供相同的会话历史分析界面 | 不可用：无等价的本地洞察产品界面 |
| `/advisor` | 使用顾问助手模式 | approximate | 二次推理 | 在被要求时提供二次评估或建议集 | 无显式的顾问功能开关 | 用显式的顾问通道来近似实现 |
| `/passes` | 显示通行证或层级信息 | unavailable | 无 | 无 | 账户或订阅产品概念不同 | 不可用：特定于提供商或账户 |

## 斜杠命令：仓库与环境操作

| Claude 命令 | 意图 | Status | Codex 机制 | 在 Codex 中的操作方式 | Boundary | 回退方案/原因 |
| --- | --- | --- | --- | --- | --- | --- |
| `/init` | 为仓库初始化一个新的 CLAUDE.md 引导 | approximate | 仓库检查加指导文件引导 | 检查仓库，然后在请求时创建或更新 `CLAUDE.md` 及相关指导制品 | Codex 不提供 Claude Code 的交互式 `/init` 引导流程（含可选 skill 和 hook） | 用仓库检查和指导文件设置来近似实现 |
| `/add-dir` | 将另一个目录加入作用域 | direct | 显式路径范围指定 | 确认范围后读取并操作请求的目录 | 无专用的已跟踪目录 UI | 直接使用请求的路径 |
| `/branch` | 在当前对话的此时创建一个分支 | approximate | 新线程或检查点分叉工作流 | 写入检查点摘要，然后在新线程中继续或从该检查点显式分叉工作计划 | 这是对话分支，不是 git 分支 | 用检查点加分叉工作流来近似实现 |
| `/mcp` | 管理 MCP 服务器 | approximate | MCP 管理或使用工作流 | 对实际配置更改使用 MCP 管理剧本，或在用户仅需运行时使用时直接使用已配置的 MCP 工具和资源 | Codex 可能暴露 MCP 使用但不提供相同的服务器管理 UI | 用可用的 MCP 工具加 MCP 管理剧本来近似实现 |
| `/plugin` | 管理 Claude 插件 | approximate | Codex skill 或插件（如可用） | 逐案将插件意图转化为 Codex skill 或插件机制 | 插件系统不同 | 近似实现；不要声称直接对等 |
| `/reload-plugins` | 在当前会话中激活待定的插件更改 | approximate | 如支持则重新读取 skill 或插件状态 | 在环境支持时重新扫描本地 skill 或插件 | 无通用重新加载命令或相同的会话插件生命周期 | 用手动刷新或重新读取来近似实现 |
| `/skills` | 列出可用 skill | direct | Codex skill 系统 | 列出相关 skill，选择一个，并在需要时显式使用 | 不同产品，相同核心概念 | 直接使用 Codex skill |
| `/permissions` | 管理允许和拒绝工具权限规则 | approximate | 权限说明加本地配置检查 | 说明当前审批模型，解释哪些由宿主管理，仅在环境实际暴露本地权限相关配置时才编辑 | Codex 权限策略主要由宿主配置，不是通过斜杠命令配置 | 用说明和谨慎的本地配置处理来近似实现 |
| `/sandbox` | 更改沙箱模式 | unavailable | 无 | 无 | 沙箱模式由宿主环境控制 | 不可用：无 skill 级别的沙箱切换 |
| `/config` 或 `/settings` | 管理设置 | approximate | 文件编辑和环境说明 | 仅在宿主环境暴露本地配置文件且用户要求时才编辑 | 无单一统一的 Codex 设置斜杠命令 | 用显式的文件级别更改来近似实现 |
| `/remote-env` | 检查远程环境配置 | unavailable | 无 | 无 | 通用 Codex skill 中无等价的远程环境界面 | 不可用：远程环境不是常见的暴露原语 |
| `/model` | 切换模型 | unavailable | 无 | 无 | 活跃模型通常不通过本地 skill 切换 | 不可用：模型选择由宿主控制 |
| `/fast` | 切换快速模式 | unavailable | 无 | 无 | 此处无直接的 Codex 等价物暴露 | 不可用：产品特定的运行时开关 |
| `/effort` | 调整推理投入 | approximate | 响应深度调整 | 在宿主支持时根据用户请求使用更简短或更深入的推理 | 无保证的显式运行时开关 | 用响应行为来近似实现 |
| `/output-style` | 已弃用的更改输出样式命令 | approximate | 样式指令 | 在当前对话中采用请求的输出格式，或在环境暴露配置样式设置时引导用户前往 | 上游命令已隐藏且弃用，Codex 无持久化输出样式命令界面 | 用响应格式化指令来近似实现 |
| `/theme` | 更改终端主题 | unavailable | 无 | 无 | UI 主题由宿主管理 | 不可用：展示层不受此 skill 控制 |
| `/color` | 更改颜色标识 | unavailable | 无 | 无 | 终端或 UI 颜色个性化由宿主管理 | 不可用 |
| `/statusline` | 设置 Claude Code 的状态行 UI | unavailable | 无 | 无 | 这通过 Claude 设置和专用设置流程配置 Claude 特定的状态行 UI | 不可用：Codex 不提供相同的状态行界面 |
| `/keybindings` | 配置键盘绑定 | unavailable | 无 | 无 | 输入绑定由宿主管理 | 不可用 |
| `/vim` | 切换 vim 模式 | unavailable | 无 | 无 | 输入模式行为由宿主管理 | 不可用 |

## 斜杠命令：账户、设置与隐藏工具

| Claude 命令 | 意图 | Status | Codex 机制 | 在 Codex 中的操作方式 | Boundary | 回退方案/原因 |
| --- | --- | --- | --- | --- | --- | --- |
| `/login` | 登录 Anthropic 支持的 Claude 界面 | unavailable | 无 | 无 | 认证由宿主管理且特定于产品 | 不可用：Codex skill 不控制账户登录 |
| `/logout` | 从 Anthropic 支持的 Claude 界面登出 | unavailable | 无 | 无 | 认证由宿主管理且特定于产品 | 不可用 |
| `/privacy-settings` | 查看或更新隐私设置 | unavailable | 无 | 无 | 隐私设置由账户或产品管理 | 不可用 |
| `/rate-limit-options` | 在被限速时显示订阅者选项 | unavailable | 无 | 无 | 限速追加销售或账户恢复流程由产品管理 | 不可用 |
| `/upgrade` | 升级到 Max 以获得更高速率限制和更多 Opus | unavailable | 无 | 无 | 订阅升级流程由提供商管理且在上游有账户门控 | 不可用：账户升级由产品管理 |
| `/terminal-setup` | 安装或调整 Claude Code 的终端键绑定 | approximate | 手动终端配置指导 | 在用户需要等价的换行或键绑定行为时解释或编辑终端配置文件 | Codex 无内置终端设置安装器 | 用终端特定的指令来近似实现 |
| `/release-notes` | 查看产品发布说明 | approximate | 读取变更日志或发布文档 | 打开可用的相关发布说明文件或源码并进行汇总 | 无内置的 Codex 发布说明命令 | 用文档检查来近似实现 |
| `/hooks` | 检查工具事件 hook 配置 | approximate | 本地配置检查 | 读取相关的 hook 或自动化配置文件并解释 | Codex 不提供统一的 hook 设置 UI | 用基于文件的检查来近似实现 |
| `/think-back` | 显示 Claude Code 年度回顾体验 | unavailable | 无 | 无 | 产品分析和动画界面特定于产品 | 不可用 |
| `/thinkback-play` | 播放隐藏的 thinkback 动画 | unavailable | 无 | 无 | 隐藏的产品动画命令 | 不可用 |
| `/heapdump` | 转储 Claude Code 进程堆 | unavailable | 无 | 无 | 这针对 Claude Code 自身的运行时内部，而非工作区项目 | 不可用：无 Codex 宿主堆转储界面 |

## 斜杠命令：集成与界面

| Claude 命令 | 意图 | Status | Codex 机制 | 在 Codex 中的操作方式 | Boundary | 回退方案/原因 |
| --- | --- | --- | --- | --- | --- | --- |
| `/chrome` | 在 Chrome 设置中打开 Claude | unavailable | 无 | 无 | 这是 Claude 拥有的 Chrome 设置界面，受账户类型和交互模式门控，不是通用浏览器自动化 | 不可用：Codex 无法打开或管理相同的 Chrome 集成设置 |
| `/desktop` | Claude 桌面集成 | unavailable | 无 | 无 | 桌面产品集成不同 | 不可用 |
| `/mobile` | 移动端配对和二维码流程 | unavailable | 无 | 无 | 移动端产品界面不存在 | 不可用 |
| `/ide` | 管理 IDE 集成并显示状态 | approximate | 现有的 IDE 相关工具或本地仓库工作流 | 解释当前环境中可用的 IDE 桥接或编辑器工作流，然后在存在时使用本地文件编辑或暴露的 IDE 工具 | 无统一的 IDE 连接命令 | 近似实现 |
| `/install-github-app` | 为仓库设置 Claude GitHub Actions | unavailable | 无 | 无 | 这是 Claude 拥有的集成设置流程，受产品账户界面门控 | 不可用 |
| `/install-slack-app` | 安装 Claude Slack 应用 | unavailable | 无 | 无 | 这是 Claude 拥有的集成设置流程，受产品账户界面门控 | 不可用 |
| `/pr-comments` | 从 GitHub 拉取请求获取评论 | approximate | GitHub CLI 或仓库工具 | 在可用时使用 `gh` 或本地审查工作流获取 PR 级别和审查评论 | 无单一专用的 PR 评论命令 | 近似实现 |

## 斜杠命令：协作、任务与其他

| Claude 命令 | 意图 | Status | Codex 机制 | 在 Codex 中的操作方式 | Boundary | 回退方案/原因 |
| --- | --- | --- | --- | --- | --- | --- |
| `/agents` | 管理 agent 配置 | approximate | 在明确允许时使用 Codex 委托 agent | 解释可用的委托角色，仅在用户明确请求时使用子 agent | Codex 委托有权限限制且与 Claude agent UX 和 agent 配置 UI 不同 | 近似实现 |
| `/tasks` | 列出和管理后台任务 | approximate | 活跃任务或进程汇总 | 在存在时汇总活跃的委托 agent、待处理的长时间运行 shell 任务或可见的排队工作 | 无持久化的 Claude 风格后台任务管理器 | 用可见的任务或进程状态来近似实现 |
| `/btw` | 在不中断主对话的情况下问一个快速附带问题 | approximate | 限定范围的附带问题工作流 | 简短回答附带问题，然后明确返回主任务上下文 | 无专用的附带问题 UI 来保持独立的对话分支 | 用简短的限定范围偏题来近似实现 |
| `/feedback` | 发送产品反馈 | unavailable | 无 | 无 | 产品反馈渠道由宿主管理 | 不可用 |
| `/stickers` | 视觉贴纸功能 | unavailable | 无 | 无 | 仅限 UI 的功能 | 不可用 |

## CLI 子命令：公开和半公开界面

| Claude CLI 子命令 | 意图 | Status | Codex 机制 | 在 Codex 中的操作方式 | Boundary | 回退方案/原因 |
| --- | --- | --- | --- | --- | --- | --- |
| `claude` | 默认交互会话 | approximate | 正常 Codex 对话 | 在当前 Codex 会话中工作 | 不同的 shell 或 UI 入口点 | 近似实现 |
| `claude mcp serve` | 启动 Claude Code MCP 服务器 | unavailable | 无 | 无 | Codex 不提供通用的 skill 级别 MCP 服务器运行时 | 不可用 |
| `claude mcp add` | 添加 MCP 服务器配置 | approximate | MCP 管理决策树 | 使用 MCP 管理剧本：如果存在具体的 MCP 配置则编辑，否则在翻译处停止 | Codex 不提供相同的 MCP 管理 CLI | 参见 `integration-playbooks.md` |
| `claude mcp remove` | 移除 MCP 服务器配置 | approximate | MCP 管理决策树 | 在存在真实可编辑的 MCP 配置时从中移除服务器；否则在映射后停止 | 无相同的 MCP 管理 CLI | 参见 `integration-playbooks.md` |
| `claude mcp list` | 列出已配置的 MCP 服务器 | approximate | MCP 管理决策树 | 首先区分运行时 MCP 界面和管理配置，然后检查实际存在的具体界面 | Codex 可能暴露资源但不提供相同的服务器注册表 | 参见 `integration-playbooks.md` |
| `claude mcp get` | 检查一个 MCP 服务器配置 | approximate | MCP 管理决策树 | 在可访问时检查具体的 MCP 配置条目；否则在映射后停止并解释差距 | 无相同的管理界面 | 参见 `integration-playbooks.md` |
| `claude mcp add-json` | 添加 JSON 定义的 MCP 服务器 | approximate | MCP 管理决策树 | 仅在已知真实可编辑的配置界面时写入等价的 MCP 配置 | 无直接的 MCP 配置写入命令 | 参见 `integration-playbooks.md` |
| `claude mcp add-from-claude-desktop` | 从 Claude Desktop 导入服务器 | approximate | MCP 迁移剧本 | 如果可访问则读取 Claude Desktop 配置，然后将条目转换到本地 Codex MCP 配置 | 跨产品导入不是自动的 | 参见 `integration-playbooks.md` |
| `claude mcp reset-project-choices` | 重置项目范围的 MCP 审批选择 | unavailable | 无 | 无 | Codex 不提供相同的项目信任选择存储 | 不可用 |
| `claude server` | 启动 Claude Code 直连会话服务器 | unavailable | 无 | 无 | 无等价的 Codex 直连服务器界面 | 不可用 |
| `claude ssh <host> [dir]` | 通过 SSH 在远程主机上运行 Claude Code | approximate | Shell SSH 工作流 | 在允许时直接使用 `ssh`，然后在远程 shell 中显式操作 | 不是 Codex 管理的远程会话模式 | 近似实现 |
| `claude open <cc-url>` | 连接到 Claude Code 直连 URL | unavailable | 无 | 无 | 无等价的 `cc://` 直连界面 | 不可用 |
| `claude auth login` | 登录 Anthropic 认证 | unavailable | 无 | 无 | 认证流程由宿主管理 | 不可用 |
| `claude auth status` | 显示 Anthropic 认证状态 | unavailable | 无 | 无 | 账户状态界面不同 | 不可用 |
| `claude auth logout` | 从 Anthropic 认证登出 | unavailable | 无 | 无 | 认证流程由宿主管理 | 不可用 |
| `claude plugin validate` | 验证 Claude 插件清单 | approximate | 插件或 skill 验证工作流 | 首先识别目标制品是 Codex 插件还是 Codex skill，然后验证该制品的真实结构 | 插件 schema 和包布局不同 | 参见 `integration-playbooks.md` |
| `claude plugin list` | 列出已安装的 Claude 插件 | approximate | 检查本地 Codex skill 或插件 | 列出当前环境中本地可用的 skill 和插件 | 插件清单界面不同 | 近似实现 |
| `claude plugin marketplace add` | 添加 Claude 市场源 | approximate | 如环境支持则编辑本地插件市场元数据 | 在该工作流存在时更新本地市场元数据文件 | 市场架构不同 | 近似实现 |
| `claude plugin marketplace list` | 列出已配置的 Claude 市场 | approximate | 如存在则检查本地插件市场元数据 | 从本地文件读取已配置的市场声明 | 无相同的 CLI 或托管市场界面 | 近似实现 |
| `claude plugin marketplace remove` | 移除 Claude 市场源 | approximate | 如存在则编辑本地插件市场元数据 | 从本地文件中移除市场声明 | 市场架构不同 | 近似实现 |
| `claude plugin marketplace update` | 刷新市场定义 | approximate | 手动重新读取或更新市场文件 | 在元数据文件存在时拉取或编辑 | 无一键 Codex 市场更新器 | 近似实现 |
| `claude plugin install` | 安装 Claude 插件 | approximate | Skill 或插件安装工作流 | 优先使用现有 Codex skill 或 `skill-installer` 工作流实现可复用行为；仅在用户确实需要 Codex 插件时使用插件打包 | 安装机制不同 | 参见 `integration-playbooks.md` |
| `claude plugin uninstall` | 卸载 Claude 插件 | approximate | 移除本地 Codex 插件或 skill 文件 | 仅在请求时通过删除或禁用相关本地包来卸载 | 插件生命周期不同 | 近似实现 |
| `claude plugin enable` | 启用已禁用的 Claude 插件 | approximate | 通过本地配置启用相关 Codex 插件或 skill | 如果宿主暴露该控制则重新启用本地包 | 无相同的启用界面 | 近似实现 |
| `claude plugin disable` | 禁用 Claude 插件 | approximate | 通过本地配置禁用相关 Codex 插件或 skill | 在该机制存在时通过本地配置或文件级别更改禁用包 | 无相同的禁用界面 | 近似实现 |
| `claude plugin update` | 更新 Claude 插件 | approximate | 制品特定的更新工作流 | 运行目标 Codex skill、插件包或本地元数据的真实更新路径，而非模仿市场对等 | 无一键托管更新器 | 参见 `integration-playbooks.md` |
| `claude setup-token` | 配置长期令牌 | unavailable | 无 | 无 | 认证或令牌流程由产品管理 | 不可用 |
| `claude agents` | 列出已配置的 agent | approximate | 解释可用的 Codex 委托角色 | 汇总当前环境中可用的 agent 角色和委托约束 | Codex 不提供相同的持久化 agent 注册表 | 近似实现 |
| `claude auto-mode defaults` | 打印默认分类器规则 | unavailable | 无 | 无 | Codex 不提供 Claude 的对话记录分类器系统 | 不可用 |
| `claude auto-mode config` | 打印有效分类器配置 | unavailable | 无 | 无 | 无等价的 Codex auto-mode 配置界面 | 不可用 |
| `claude auto-mode critique` | 评估自定义分类器规则 | approximate | 手动规则审查 | 在聊天中直接审查提供的规则或启发式 | 无原生 Codex auto-mode 子系统 | 近似实现 |
| `claude remote-control` 及别名 `rc`、`remote`、`sync`、`bridge` | 将本地环境附加到 Claude remote-control | unavailable | 无 | 无 | 无等价的桥接产品界面 | 不可用 |
| `claude assistant [sessionId]` | 附加到正在运行的桥接会话 | unavailable | 无 | 无 | 无等价的 assistant-client 桥接界面 | 不可用 |
| `claude doctor` | 检查 Claude Code 自动更新器和受信任本地环境的健康状态 | approximate | 本地诊断 | 运行 shell 和文件检查并报告修复方案 | Codex 可以检查本地环境，但无法完全等同于 Claude 的更新器或信任工作流 | 用本地诊断来近似实现 |
| `claude update` 及别名 `upgrade` | 更新 Claude CLI | unavailable | 无 | 无 | Codex 宿主或运行时更新不受 skill 控制 | 不可用 |
| `claude install [target]` | 安装 Claude 原生构建 | unavailable | 无 | 无 | Codex 安装不受 skill 控制 | 不可用 |

## CLI 子命令：功能门控或内部

| Claude CLI 子命令 | 意图 | Status | Codex 机制 | 在 Codex 中的操作方式 | Boundary | 回退方案/原因 |
| --- | --- | --- | --- | --- | --- | --- |
| `claude mcp xaa setup` | 为 MCP 配置 XAA IdP 认证 | unavailable | 无 | 无 | 这是 Claude 特定的 MCP 认证基础设施 | 不可用 |
| `claude mcp xaa login` | 获取或缓存 XAA IdP 令牌 | unavailable | 无 | 无 | Claude 特定的认证基础设施 | 不可用 |
| `claude mcp xaa show` | 显示 XAA IdP 配置 | unavailable | 无 | 无 | Claude 特定的认证基础设施 | 不可用 |
| `claude mcp xaa clear` | 清除 XAA IdP 配置 | unavailable | 无 | 无 | Claude 特定的认证基础设施 | 不可用 |
| `claude daemon [subcommand]` | 启动或管理守护进程监控器 | unavailable | 无 | 无 | Codex 不提供 Claude 守护进程生命周期 | 不可用 |
| `claude ps` | 列出 Claude 后台会话 | unavailable | 无 | 无 | 无等价的后台会话注册表 | 不可用 |
| `claude logs` | 检查 Claude 后台会话日志 | unavailable | 无 | 无 | 无等价的后台会话注册表 | 不可用 |
| `claude attach` | 附加到后台 Claude 会话 | unavailable | 无 | 无 | 无等价的后台会话注册表 | 不可用 |
| `claude kill` | 终止后台 Claude 会话 | unavailable | 无 | 无 | 无等价的后台会话注册表 | 不可用 |
| `claude new` | 创建模板任务 | unavailable | 无 | 无 | 模板任务子系统受功能门控且特定于产品 | 不可用 |
| `claude list` | 列出模板任务 | unavailable | 无 | 无 | 模板任务子系统特定于产品 | 不可用 |
| `claude reply` | 回复模板任务 | unavailable | 无 | 无 | 模板任务子系统特定于产品 | 不可用 |
| `claude environment-runner` | 运行 BYOC 环境运行器 | unavailable | 无 | 无 | 无等价的环境运行器界面 | 不可用 |
| `claude self-hosted-runner` | 运行自托管工作服务 | unavailable | 无 | 无 | 无等价的自托管运行器界面 | 不可用 |
| `claude up` | 从 `CLAUDE.md` 引导 Anthropic 开发环境 | unavailable | 无 | 无 | Anthropic 内部开发引导流程 | 不可用 |
| `claude rollback [target]` | 回滚 Claude 发布版本 | unavailable | 无 | 无 | 产品运行时生命周期控制未暴露 | 不可用 |
| `claude log` | 检查 Anthropic 对话日志 | unavailable | 无 | 无 | Anthropic 内部运营界面 | 不可用 |
| `claude error` | 检查 Anthropic 错误日志 | unavailable | 无 | 无 | Anthropic 内部运营界面 | 不可用 |
| `claude export` | 将 Anthropic 日志会话导出为文本 | unavailable | 无 | 无 | 这针对 Anthropic 日志存储，不是通用 Codex 对话记录模型 | 不可用 |
| `claude task create` | 创建内部任务项 | approximate | 工作区任务文件或计划 | 在本地清单、计划或 issue 文件中创建任务 | Codex 中不存在内部任务服务 | 近似实现 |
| `claude task list` | 列出内部任务项 | approximate | 工作区任务文件或计划 | 从维护的本地清单或计划中列出任务 | Codex 中不存在内部任务服务 | 近似实现 |
| `claude task get` | 检查一个内部任务 | approximate | 工作区任务文件或计划 | 从本地任务制品中读取请求的任务条目 | Codex 中不存在内部任务服务 | 近似实现 |
| `claude task update` | 更新内部任务 | approximate | 工作区任务文件或计划 | 在本地计划或任务文件中编辑任务条目 | Codex 中不存在内部任务服务 | 近似实现 |
| `claude task dir` | 显示 Anthropic 任务存储路径 | unavailable | 无 | 无 | Codex 中无等价的隐藏任务存储路径 | 不可用 |
| `claude completion <shell>` | 生成 shell 补全脚本 | unavailable | 无 | 无 | Codex CLI 补全不从此 skill 界面管理 | 不可用 |

## 斜杠命令：功能门控或可选的 Claude Code 功能

| Claude 命令 | 意图 | Status | Codex 机制 | 在 Codex 中的操作方式 | Boundary | 回退方案/原因 |
| --- | --- | --- | --- | --- | --- | --- |
| `/voice` | 语音模式 | unavailable | 无 | 无 | 语音 I/O 不通过此 skill 暴露 | 不可用 |
| `/proactive` | 自主主动模式 | unavailable | 无 | 无 | 持久化自主循环特定于产品 | 不可用 |
| `/brief` | 简短自主更新 | approximate | 手动简洁摘要 | 按需写一份简短摘要 | 无自主简报通道 | 近似实现 |
| `/assistant` | Kairos 助手模式 | unavailable | 无 | 无 | 产品特定的长时间运行助手模式 | 不可用 |
| `/remote-control` | 将此终端连接到 remote-control 会话 | unavailable | 无 | 无 | Remote-control 桥接行为由产品管理，不作为通用 Codex 斜杠界面暴露 | 不可用 |
| `/remote-control-server` | 提供 remote control 端点 | unavailable | 无 | 无 | 此处无暴露的守护进程桥接服务器 | 不可用 |
| `/force-snip` | 强制历史裁剪 | unavailable | 无 | 无 | 无对话记录手术原语 | 不可用 |
| `/workflows` | 运行工作流脚本 | approximate | Skill 引导或 shell 工作流 | 如果 Codex 能执行则直接运行请求的工作流 | 工作流系统不同 | 近似实现 |
| `/web-setup` | 远程 web 设置流程 | unavailable | 无 | 无 | 产品特定的设置界面 | 不可用 |
| `/subscribe-pr` | 订阅 PR 事件 | unavailable | 无 | 无 | 无 webhook 订阅产品界面 | 不可用 |
| `/ultraplan` | 大型远程规划工作流 | approximate | 深度规划加可选委托 | 使用规划工作流和子 agent（仅在可用且明确请求时） | 无相同的远程规划器 | 近似实现 |
| `/torch` | 内部功能标志命令 | unavailable | 无 | 无 | 功能含义特定于产品且未暴露 | 不可用 |
| `/peers` | 对等收件箱或 socket 消息 | unavailable | 无 | 无 | 无等价的对等邮箱界面 | 不可用 |
| `/fork` | 分叉子 agent | approximate | 委托 agent 工作流 | 仅在用户明确要求委托时生成子 agent | Codex 有更严格的委托规则 | 近似实现 |
| `/buddy` | 配对伙伴模式 | unavailable | 无 | 无 | 产品特定的协作模式 | 不可用 |

## 斜杠命令：内部或仅限 Anthropic 的命令

| Claude 命令 | 意图 | Status | Codex 机制 | 在 Codex 中的操作方式 | Boundary | 回退方案/原因 |
| --- | --- | --- | --- | --- | --- | --- |
| `/tag` | 标记会话或 issue 状态 | unavailable | 无 | 无 | 仅限内部界面 | 不可用 |
| `/backfill-sessions` | 内部会话维护 | unavailable | 无 | 无 | 仅限内部界面 | 不可用 |
| `/break-cache` | 内部缓存失效 | unavailable | 无 | 无 | 仅限内部界面 | 不可用 |
| `/bughunter` | 内部 bug 查找流程 | approximate | 本地深度审查 | 改为执行本地深度 bug 搜寻 | 云端或内部服务不可用 | 用本地深度 bug 搜寻来近似实现 |
| `/commit` | 引导式提交流程 | approximate | Git 工作流 | 在用户要求时创建提交信息并运行 git 命令 | 无内置的受保护提交命令 | 近似实现 |
| `/commit-push-pr` | 引导式提交加推送加 PR | approximate | Git 和 `gh` 工作流 | 在工具可用且用户批准时显式执行 git 和 GitHub 步骤 | 无一键托管工作流 | 近似实现 |
| `/ctx-viz` | 内部上下文可视化 | unavailable | 无 | 无 | 无匹配的可视化界面 | 不可用 |
| `/good-claude` | 内部命令 | unavailable | 无 | 无 | 仅限内部界面 | 不可用 |
| `/issue` | 内部 issue 工作流 | approximate | GitHub 或跟踪器工作流 | 在可用时直接使用 issue 工具 | 无相同的产品包装器 | 近似实现 |
| `/init-verifiers` | 内部验证器设置 | unavailable | 无 | 无 | 仅限内部界面 | 不可用 |
| `/mock-limits` | 内部限制模拟 | unavailable | 无 | 无 | 仅限内部界面 | 不可用 |
| `/bridge-kick` | 内部桥接控制 | unavailable | 无 | 无 | 仅限内部界面 | 不可用 |
| `/version` | 显示版本 | approximate | 解释环境或版本（如已知） | 在可用时报告 Codex 环境详情 | 无通用的 skill 级别版本命令 | 近似实现 |
| `/reset-limits` | 内部配额重置 | unavailable | 无 | 无 | 内部或账户控制不可用 | 不可用 |
| `/onboarding` | 内部引导流程 | unavailable | 无 | 无 | 产品管理的流程 | 不可用 |
| `/share` | 分享会话 | unavailable | 无 | 无 | 产品分享界面不同 | 不可用 |
| `/summary` | 内部摘要流程 | approximate | 手动摘要 | 直接写出摘要 | 无专用的内部功能对等 | 用直接摘要响应来近似实现 |
| `/teleport` | 远程会话传送 | unavailable | 无 | 无 | 无等价的远程会话传输原语 | 不可用 |
| `/ant-trace` | 内部跟踪 | unavailable | 无 | 无 | 仅限内部的跟踪界面 | 不可用 |
| `/perf-issue` | 内部性能报告 | approximate | 本地性能诊断 | 在本地诊断性能并写出发现 | 无相同的产品报告器 | 用本地性能诊断来近似实现 |
| `/env` | 检查环境 | direct | Shell 环境检查 | 运行环境检查并汇总 | 无斜杠包装器 | 使用 shell 检查 |
| `/oauth-refresh` | 刷新 OAuth 令牌 | unavailable | 无 | 无 | 账户认证流程由产品管理 | 不可用 |
| `/debug-tool-call` | 内部调试 | approximate | 手动工具调用跟踪 | 手动跟踪相关工具行为 | 无专用调试 UI | 用手动跟踪来近似实现 |
| `/agents-platform` | 内部 agents platform 流程 | unavailable | 无 | 无 | 仅限内部界面 | 不可用 |
| `/autofix-pr` | 内部自动化 PR 修复 | approximate | 本地修复工作流 | 审查 PR 并直接实施修复 | 无内部 autofix 服务 | 用本地修复工作流来近似实现 |
