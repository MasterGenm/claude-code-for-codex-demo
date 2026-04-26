# Integration Playbooks（集成操作手册）

本文件用于处理最困难的 `approximate` 集成场景，尤其是 MCP 管理和插件生命周期流程。

## MCP 管理

### `claude mcp list`

推荐顺序：

1. 如果 Codex 环境暴露了 MCP 资源或模板列表工具，使用它们展示可用的 MCP 接口。
2. 如果工作区或用户配置中有已知的可编辑 MCP 配置文件，检查该文件以展示已配置的 server。
3. 如果两者都不存在，说明运行时 MCP 使用可能可用，但 server 管理功能无法对等。

### `claude mcp get`

推荐顺序：

1. 如果相关的 MCP 配置条目可访问，直接读取该条目。
2. 否则，在 mapping 块之后停止，并说明 Codex 缺少通用的 MCP server 检查界面。

### `claude mcp add`、`add-json`、`remove`

推荐顺序：

1. 确认是否存在 Codex 可以编辑的具体 MCP 配置文件或宿主管理的配置接口。
2. 如果有，修改该具体配置。
3. 如果没有，在 mapping 块之后停止，并说明 Codex 可以消费 MCP 工具但不暴露 MCP server 管理功能。

### `claude mcp add-from-claude-desktop`

推荐顺序：

1. 如果 Claude Desktop 配置文件可访问，读取它。
2. 将相关条目转换为本地 Codex MCP 配置格式。
3. 如果目标配置不可编辑或未知，停在转换步骤并说明差距。

### 入站或 Channel 式 MCP 请求

推荐顺序：

1. 判断用户是在问运行时使用、管理配置，还是入站通知。
2. 如果是运行时使用，基于宿主已暴露的 MCP 工具和资源来处理。
3. 如果是管理配置，沿正常的 MCP 管理决策树进行。
4. 如果依赖 channel 通知、session `--channels`、组织级 opt-in、allowlist 或 server 推送的对话消息，在 mapping 块之后停止，除非当前宿主明确暴露了等效的控制面。

## 插件与 Marketplace 生命周期

### `claude plugin install`

推荐顺序：

1. 确认用户目标：
   - 可复用的 Codex 行为
   - 可安装的 Codex 插件包
   - 一次性任务能力
2. 如果目标是可复用行为，优先使用现有 Codex skill 或 `skill-installer` 工作流。
3. 如果目标是 Codex 插件包，使用 `plugin-creator` 工作流或直接编辑本地插件包。
4. 如果目标只是获得某种能力，不要强制走 marketplace 式安装流程；使用最近的现有 Codex skill 或工作流。

### `claude plugin validate`

推荐顺序：

1. 判断目标是 Codex 插件包还是 Codex skill。
2. 验证目标对应的 manifest 和必要文件结构。
3. 明确说明 Claude marketplace schema 和 Codex 插件 schema 不同。

### `claude plugin update`、`uninstall`、`enable`、`disable`

推荐顺序：

1. 确认被管理的实际 Codex 产物：skill、插件包还是本地元数据。
2. 使用该产物真实的更新或删除机制。
3. 如果没有具体产物，在 mapping 块之后停止，并说明 marketplace 对等功能不可用。

## 何时停止

在以下情况下，应在 mapping 块之后停止：

- 环境只暴露运行时使用功能而不暴露管理功能
- 相关配置文件或包路径未知
- 翻译结果会变成含糊的"视情况可用"式回答

在这些情况下，先要求提供具体的配置路径、插件路径或目标产物，再执行操作。
