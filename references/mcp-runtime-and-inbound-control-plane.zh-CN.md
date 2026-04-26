# MCP Runtime And Inbound Control Plane（MCP 运行时与入站控制面）

当请求涉及 MCP 运行时行为而非仅仅 `/mcp` 或 `claude mcp add` 时使用本文件。

以下是 Claude Code 中真正重要的拆分：

1. 工具和资源的运行时使用
2. 服务器配置的管理
3. 入站控制面行为——MCP 服务器可以推送或注册对话可见的行为

## Claude Code 实际在做什么

Claude Code 不把 MCP 当作单一功能桶。

真实的运行时至少有三个面：

### Runtime Plane（运行时面）

这是大多数用户首先注意到的面：
- 连接服务器
- 发现工具
- 发现资源
- 在需要时添加资源辅助工具
- 会话过期时重连
- 暴露 needs-auth 状态

### Administration Plane（管理面）

这是 `/mcp` 和 `claude mcp *` 暴露的面：
- 服务器定义
- 审批和信任选择
- list/get/add/remove 流程
- 配置文件和托管策略状态

### Inbound Control Plane（入站控制面）

这是最难的部分，也最容易被忽视：
- channel 风格的入站通知
- 注册门控
- 组织策略 opt-in
- 会话级 `--channels` opt-in
- 插件/服务器允许列表
- 认证和 marketplace 来源验证

第三个面是为什么 Claude Code 中的 MCP 不仅仅是"工具调用加配置编辑"。

## Source Anchors

反向工程的 Claude Code 镜像：
- `src/services/mcp/client.ts:1175` - 连接建立时记录服务器能力，包括 tools、prompts、resources 和 resource-subscribe 支持。
- `src/services/mcp/client.ts:1190` - 初始化过程中注册了 elicitation handler，表明运行时协商包含非工具请求处理。
- `src/services/mcp/client.ts:2173` - tool、command、skill 和 resource 发现一起获取，然后规范化到会话运行时中。
- `src/services/mcp/client.ts:2183` - 当资源存在但通用资源工具尚未就位时，注入资源辅助工具。
- `src/services/mcp/client.ts:3217` - 会话过期时清除连接缓存，下次工具调用用新会话重连。
- `src/services/mcp/channelNotification.ts:176` - 入站 channel 注册按严格顺序门控：capability、运行时门控、认证、组织策略、会话 opt-in、允许列表。
- `src/services/mcp/channelNotification.ts:245` - 即使是受信任的服务器也必须被列在会话的 `--channels` 中才能推送入站消息。
- `src/services/mcp/channelNotification.ts:276` - 插件来源验证和已审批插件允许列表是入站注册的一部分，不是通用 MCP 使用的一部分。
- `src/utils/settings/types.ts:407` - 项目级已审批和已拒绝的 `.mcp.json` 服务器选择是持久化设置。
- `src/utils/settings/types.ts:895` - 托管组织设置暴露 `channelsEnabled`，使入站 MCP 成为一个策略面，不仅仅是本地配置细节。
- `src/bootstrap/state.ts:213` - 允许的 channels 作为会话状态被跟踪，与普通 MCP 使用分开。

`claw-code` 洁净室运行时：
- `rust/crates/runtime/src/mcp.rs:26` - 运行时 MCP 工具由服务器和工具标识命名，不被视为匿名通用调用。
- `rust/crates/runtime/src/mcp.rs:65` - 服务器签名区分 stdio 和 remote 传输，使运行时标识成为一等概念。
- `rust/crates/runtime/src/mcp.rs:84` - 作用域 MCP 配置哈希编码传输、headers、helpers 和 OAuth 相关字段，用于重连和漂移检测。
- `rust/crates/runtime/src/config.rs:531` - MCP 服务器定义作为类型化运行时配置加载，不是自由格式的 shell 备注。
- `rust/crates/runtime/src/config.rs:713` - remote 传输和托管代理形式是不同的 MCP 配置变体。

## 1. Runtime Plane（运行时面）

对于运行时使用，重要的问题不是"MCP 启用了吗？"而是"这个已连接的服务器实际上公告了什么？"

运行时行为包括：
- 能力检查
- 工具发现
- 资源发现
- 资源辅助工具注入
- 认证或 needs-auth 处理
- 重连和会话过期恢复

操作影响：
- "使用 MCP 工具"在 Codex 中通常是 `approximate`，因为 Codex 可能暴露工具和资源，但不具备相同的完整协商、重连或认证面

## 2. Administration Plane（管理面）

管理面是用户通过 `/mcp` 和 `claude mcp *` 接触的面。

这个面涵盖：
- 列出已配置的服务器
- 检查单个配置条目
- 添加、移除或导入服务器配置
- 项目范围的审批或拒绝
- 托管允许列表或策略叠加

操作影响：
- 管理操作根据当前 Codex 宿主是否存在真实可编辑的配置面，保持 `approximate` 或 `unavailable`

## 3. Inbound Control Plane（入站控制面）

这是大多数迁移中被低估建模的部分。

Claude Code 允许某些 MCP 服务器注册一条入站路径，可以推送对话可见的消息。该路径不等同于普通的工具使用。

门控顺序很重要：

1. 服务器声明 `claude/channel` 能力
2. 运行时功能门控已启用
3. 认证是 Claude.ai OAuth，不是通用 API key 访问
4. 组织策略通过 `channelsEnabled` opt-in
5. 会话通过 `--channels` 显式 opt-in
6. 允许列表和插件来源检查通过

操作影响：
- 入站/channel 行为在 Codex 中通常是 `unavailable`，除非宿主显式暴露了等效的传输和会话控制面
- 不要将其翻译为"只是另一个 MCP 工具"

## 4. 标识、传输与重连

运行时面还有一个标识模型：
- 工具名称是服务器限定的
- remote 代理 URL 可能包装了底层 MCP URL
- 服务器签名和作用域配置哈希驱动重连和漂移检测

这很重要，因为"相同的配置条目"和"相同的运行时会话"不是一回事。

操作影响：
- 当用户询问 MCP 运行时在认证、重连或配置编辑后为何发生变化时，应解释这是连接标识问题，不仅仅是配置文件问题

## 5. Mapping 指南

### Runtime MCP 使用

保持 `approximate`。

说明：
- Codex 可能能直接使用暴露的 MCP 工具和资源
- 这不意味着与 Claude Code 的认证、重连或入站运行时行为对等

### MCP 管理

根据是否存在真实可编辑的配置面，保持 `approximate` 或 `unavailable`。

说明：
- 运行时 MCP 可用性不保证管理面的对等
- 配置编辑、list/get/add/remove 和审批状态管理是独立的问题

### 入站通知、Channels 或服务器推送消息

通常保持 `unavailable`。

说明：
- Claude Code 有一个独立的入站控制面
- Codex 可能消费工具但不暴露服务器驱动的消息注册、会话 opt-in 或组织托管的允许列表

### `claude mcp add`、`list`、`get`

这些属于管理桶，即使用户的动机来自运行时问题。

不要将其作为普通工具调用问题来回答。

## Codex 应该学到什么

持久的教训是：

- MCP 使用不是 MCP 管理
- MCP 管理不是入站控制
- 运行时标识和重连很重要
- 服务器推送路径是控制面行为，不仅仅是更丰富的工具结果

这是值得提炼的 Claude Code 操作逻辑。
