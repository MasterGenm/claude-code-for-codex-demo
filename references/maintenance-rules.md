# Maintenance Rules

Use this file when updating the skill.

## Source Discipline

- Treat the reverse-engineered Claude Code repository and current Codex environment as separate sources of truth.
- Re-check mappings whenever either side changes materially.
- Do not preserve a stale `direct` label out of convenience.

## Status Discipline

Only use:

- `direct`
- `approximate`
- `unavailable`

Do not introduce softer labels like `partial`, `kind of`, or `mostly`.

## Execution Discipline

- Keep mapping and execution as separate stages.
- Do not change the skill into an auto-executing command shim.
- Preserve the fixed response order: `Status`, `Codex mapping`, `Boundary`, `Execution path in Codex`.
- If a future edit adds richer execution behavior, it must still preserve the visible mapping stage.
- Do not allow first-response mapping and execution in the same turn.
- Do not treat an initial request to execute as post-mapping confirmation.

## Update Procedure

1. Run `python scripts/extract_upstream_commands.py --repo <path-to-claude-code-repo> --stdout summary`.
2. Run `python scripts/check_mapping_consistency.py --repo <path-to-claude-code-repo> --skill-root .`.
3. Identify the Claude Code command or workflow and confirm its user-visible intent.
4. Decide whether Codex has a stable practical equivalent.
5. If yes, mark `direct`.
6. If not, check whether Codex can still achieve the goal through a different workflow.
7. If yes, mark `approximate` and add or reuse a strategy in `approximate-strategies.md`.
8. If not, mark `unavailable` and record the reason in `unsupported-commands.md` if it reflects a durable gap.
9. Update `capability-boundaries.md` if the new command reveals a new class of product difference.
10. Update `execution-policy.md` if the command changes when or how execution may proceed after mapping.
11. Update `aliases-and-visibility.md` if the command has aliases, hidden behavior, or environment-specific gating.
12. Update `integration-playbooks.md` if the command depends on a hardest integration path such as MCP administration or plugin lifecycle.

## Automation

- `scripts/extract_upstream_commands.py` extracts upstream slash and CLI metadata into normalized JSON or a short summary.
- `scripts/check_mapping_consistency.py` compares the current skill docs against the extracted upstream registry and reports coverage gaps, alias drift, missing visibility notes, and likely-overstrong `direct` rows.
- Treat script output as a review surface, not as an auto-fix system. The scripts find drift; maintainers still decide the final mapping.

## Writing Rules

- Write for operational use, not historical commentary.
- Prefer concise entries over long narrative explanations.
- Keep repeated fallback logic in `approximate-strategies.md` and reference it consistently.
- When a command has aliases, group them in one entry.

## Do Not Do

- Do not claim parity for host-owned UI or account surfaces.
- Do not silently convert `unavailable` into a shell workaround that loses the original feature.
- Do not assume delegated agents are always allowed.
- Do not duplicate the same long explanation in every command row.
- Do not let a `direct` label erase the map-first stage.
- Do not hand-wave alias or visibility differences away when they affect user expectations.
