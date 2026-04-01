# With vs Without the Skill

[English](with-vs-without-skill.md) | [简体中文](with-vs-without-skill.zh-CN.md)

This note compares two answer styles for the same Claude Code-style requests:
- ordinary Codex behavior
- Codex using `claude-code-for-codex`

For the raw experiment record, see [`experiments/skill-comparison-experiment.md`](experiments/skill-comparison-experiment.md).

## Experiment Setup

We ran paired subagent answers against the same five prompts:
- `/help`
- `/resume`
- `claude mcp add`
- `remote-control`
- `/compact`

Important caveat:
- this experiment was run inside the current skill-oriented workspace
- the control arm was therefore stronger than a true blank baseline
- the result is still useful because it reflects the real environment where this repo will usually be used

## What Changed

### 1. Simple requests changed only a little

For a straightforward request such as `/help`, both versions were reasonably good. The skill does not magically create a huge difference on every prompt.

### 2. Approximate replacements became more stable

For `/resume` and `/compact`, the skill-backed answer was more consistent about separating:
- what Claude Code really does
- what Codex can only approximate
- what continuity is lost in the translation

That matters because these requests are easy to answer too casually.

### 3. Hardest integration cases were decomposed better

`claude mcp add` was the clearest example. The skill-backed answer more reliably separated:
- MCP runtime use
- MCP administration
- host-specific writable config surfaces

Without that split, it is easy to over-promise.

### 4. Unavailable features were handled more cleanly

For `remote-control`, the skill-backed answer stayed strict: no bridge surface, no fake parity. A normal answer is more likely to drift into “you could maybe do something similar with ssh or shared state,” which can blur the boundary.

### 5. The output format became reusable

With the skill, the response consistently followed:
1. `Status`
2. `Codex mapping`
3. `Boundary`
4. `Execution path in Codex`

That makes the behavior easier to trust and easier to reuse in repeated migration-style tasks.

## Bottom Line

This skill does not make Codex a stronger base model.

It does make Codex better at Claude Code-shaped requests:
- less likely to confuse approximation with parity
- more explicit about capability boundaries
- better at decomposing hardest cases
- more stable from one answer to the next

For ordinary coding, the difference is smaller. For Claude Code migration, translation, and boundary-heavy workflows, the difference is substantial.
