# Context Hygiene（上下文卫生）

当请求涉及以下内容时使用本文件：保持长会话健康运行、compaction、resume 正确性、rewind 边界、附件恢复、上下文压力，或 prompt 长度失败后的恢复。

本文件描述的是维持上下文长期可用的运行时管线。

## Claude Code 实际在做什么

Claude Code 的上下文管理不是单一的"做个摘要"动作。

它是一个分层卫生系统，能够：
- 裁剪冗余历史
- 缩减工具返回结果的负担
- 保留近期的高粒度上下文
- 重建 continuation 消息
- 在 compaction 后恢复重要附件
- 在 compact 和 snip 边界处过滤 resume 状态
- 在暴露 prompt 长度或最大输出失败之前尝试恢复

关键源码锚点：
- `rust/crates/runtime/src/compact.rs:37` - compaction 是基于阈值的，不是无条件触发。
- `rust/crates/runtime/src/compact.rs:65` - continuation 消息是显式协议，不只是原始摘要文本。
- `rust/crates/runtime/src/compact.rs:107` - 近期消息逐字保留，较旧的上下文被摘要化。
- `rust/crates/runtime/src/compact.rs:230` - 重复 compaction 会合并先前的摘要，而不是丢弃连续性。
- `src/query.ts:396` - snip 在 microcompact 之前运行。
- `src/query.ts:412` - microcompact 在 autocompact 之前运行。
- `src/query.ts:429` - context collapse 在 autocompact 之前运行，以便更廉价的恢复可以避免全局 compaction。
- `src/query.ts:790` - 可恢复错误会被暂扣，直到运行时确认恢复是否成功。
- `src/query.ts:1068` - prompt-too-long 恢复是一条结构化路径，不是直接报致命错误。
- `src/query.ts:1188` - max-output 恢复也走专用路径。
- `src/services/compact/autoCompact.ts:57` - autocompact 有熔断器。
- `src/services/compact/autoCompact.ts:345` - 重复失败后会停止该会话后续的 autocompact 尝试。
- `src/services/compact/compact.ts:330` - compact 后的状态按特定顺序重建。
- `src/services/compact/compact.ts:533` - 附件生成作为 compact 后重建的一部分异步处理。
- `src/services/compact/compact.ts:1402` - 最近访问的文件可以在 compaction 后按 token 预算恢复。
- `src/services/compact/compact.ts:1470` - plan 文件在 compaction 中被显式保留。
- `src/services/compact/compact.ts:1492` - 已调用的 skill 在 compaction 中被显式保留。
- `src/services/compact/compact.ts:1566` - 异步 agent 在 compaction 后重新公告。
- `src/utils/sessionStorage.ts:1396` - compact 边界对 resume 链的正确性至关重要。
- `src/utils/sessionStorage.ts:1979` - snip 边界也影响 resume 正确性。
- `src/utils/sessionStorage.ts:2212` - resume 一致性作为真实的正确性问题被监控。
- `src/utils/sessionStorage.ts:4354` - 附件在 resume 时被刻意过滤，而非整体回放。

## 真实的卫生管线

### 1. 先做预算，再做折叠

Claude Code 在执行最重的操作之前，先尝试更廉价的卫生处理。

大致顺序：
- snip
- microcompact
- context collapse
- autocompact

这个顺序很重要，因为系统希望尽可能保留近期的详细上下文。

### 2. Compaction 保留一个活跃的 Continuation

Compaction 不是"把所有内容替换成摘要"。

它通常保留：
- 一个 continuation/系统摘要
- 近期的高粒度消息
- 选定的附件或恢复的产物

这就是为什么 `/compact` 在 Codex 中只能是 `approximate`。缺失的不仅仅是一个内置摘要命令，而是完整的 continuation 协议。

### 3. 附件和产物被选择性重建

Compaction 之后，Claude Code 可以恢复：
- 近期的文件上下文
- plan 文件
- 已调用的 skill 内容
- plan 模式或 agent 状态线索

这是与简单的"写笔记然后继续"工作流的最大区别之一。

Compact 后的上下文是精心策划的，不是随意倾倒的。

### 4. Resume 正确性依赖边界过滤

Resume 不只是"从磁盘加载之前的消息"。

正确的 resume 依赖于：
- compact 边界过滤
- snip 边界过滤
- 保留片段重建
- 选择性附件回放
- context-collapse 快照恢复

这就是为什么 `/resume` 和 `/rewind` 应当保持 `approximate`。Codex 可以重建工作区状态，但它没有暴露这个基于会话记录的卫生栈。

### 5. 恢复先于错误暴露

Claude Code 并不总是立即暴露上下文错误。

它可能先尝试：
- context collapse
- 被动 compaction
- max-output 恢复
- 其他结构化缩减

这是一个运行时状态机，不只是一个错误消息策略。

### 6. 卫生失败需要防护

Autocompact 有熔断器，因为重复失败的 compaction 会让系统抖动。

这对 Codex 是一个重要教训：
- 卫生和恢复系统需要停止条件
- 否则运行时会在同一故障模式上无限循环

## Mapping 指南

### `/compact`

保持 `approximate`。

翻译影响：
- 说明 Codex 可以写检查点摘要或文档
- 不要暗示与 Claude Code 的多轮 compaction 和恢复管线对等

### `/resume`

保持 `approximate`。

翻译影响：
- 从文件、plan、git 状态和笔记进行重建
- 说明 Codex 缺少基于会话记录的边界过滤和 compact 后恢复

### `/rewind`

保持 `approximate`。

翻译影响：
- 将其视为恢复到之前的检查点或方案
- 不要暗示具备会话级回退以及会话记录和链正确性

### `/context`

保持 `approximate`。

翻译影响：
- 总结可见的上下文压力、已触及的文件和可能的风险
- 不要暗示 Claude Code 精确的 token 网格或卫生状态可视化

### 导出和检查点请求

将其视为连续性产物请求，不仅仅是"把文本存到某处"。

翻译影响：
- 写持久化的摘要或检查点产物
- 说明 Claude Code 的 compact 后上下文是重建的，不仅仅是导出的

## Codex 应该学到什么

Claude Code 的核心教训是：
- 长上下文健康是一项主动的运行时职责

这项职责包括：
- 预算管理
- 分级缩减
- 选择性恢复
- 边界感知的 resume
- 结构化恢复

这是一个可复用的操作模型，应当塑造 Codex 解释最困难的会话连续性请求的方式。
