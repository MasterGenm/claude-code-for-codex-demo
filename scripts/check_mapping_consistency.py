from __future__ import annotations

import argparse
from pathlib import Path

from command_registry_lib import (
    RegistryCommand,
    extract_upstream_commands,
    format_report,
    likely_overstrong_direct,
    parse_alias_reference,
    parse_mapping_rows,
)


def _registry_index(items: list[dict]) -> dict[str, RegistryCommand]:
    return {item["canonical"]: RegistryCommand(**item) for item in items}


def _is_container(command: RegistryCommand, all_canonicals: set[str]) -> bool:
    return "container" in command.visibility_hints and any(
        other.startswith(f"{command.canonical} ") for other in all_canonicals if other != command.canonical
    )


def _mentions_gating(text: str) -> bool:
    lower = text.lower()
    keywords = (
        "remote-only",
        "ant-only",
        "claude-ai",
        "console",
        "interactive",
        "hidden",
        "deprecated",
        "platform",
        "subscriber",
        "feature",
        "gated",
        "internal",
        "mac and wsl",
    )
    return any(keyword in lower for keyword in keywords)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check `claude-code-for-codex` mapping docs for upstream drift.",
    )
    parser.add_argument("--repo", required=True, help="Path to the upstream Claude Code repo")
    parser.add_argument(
        "--skill-root",
        required=True,
        help="Path to the `claude-code-for-codex` skill root",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with status 1 when findings are present",
    )
    args = parser.parse_args()

    skill_root = Path(args.skill_root)
    upstream = extract_upstream_commands(Path(args.repo))
    mapping_rows = parse_mapping_rows(skill_root / "references" / "command-mapping.md")
    alias_info = parse_alias_reference(skill_root / "references" / "aliases-and-visibility.md")

    slash_upstream = _registry_index(upstream["slash_commands"])
    cli_upstream = _registry_index(upstream["cli_commands"])
    upstream_index = {**slash_upstream, **cli_upstream}
    mapping_index = {row.canonical: row for row in mapping_rows}
    mapping_codes = {code for row in mapping_rows for code in row.codes}

    findings: dict[str, list[str]] = {
        "Missing mapping rows": [],
        "Doc-only mapping rows": [],
        "Missing alias coverage": [],
        "Unexpected documented aliases": [],
        "Missing visibility notes": [],
        "Likely-overstrong direct mappings": [],
    }

    ignored_doc_only = {"claude"}
    all_upstream_canonicals = set(upstream_index)
    for canonical, command in sorted(upstream_index.items()):
        if command.surface == "cli" and _is_container(command, all_upstream_canonicals):
            continue
        if canonical not in mapping_codes:
            findings["Missing mapping rows"].append(canonical)
    for canonical in sorted(mapping_index):
        if canonical not in upstream_index and canonical not in ignored_doc_only:
            findings["Doc-only mapping rows"].append(canonical)

    documented_aliases = {}
    documented_aliases.update(alias_info["slash_aliases"])
    documented_aliases.update(alias_info["cli_aliases"])

    for canonical, command in sorted(upstream_index.items()):
        expected_aliases = set(command.aliases)
        documented = set(documented_aliases.get(canonical, []))
        missing = sorted(expected_aliases - documented)
        extra = sorted(documented - expected_aliases)
        if missing:
            findings["Missing alias coverage"].append(f"{canonical}: {', '.join(missing)}")
        if extra:
            findings["Unexpected documented aliases"].append(f"{canonical}: {', '.join(extra)}")

        row = mapping_index.get(canonical)
        if row and (command.availability or command.visibility_hints):
            combined_text = " ".join([row.boundary, row.reason, row.intent, alias_info["raw_text"]])
            if canonical not in alias_info["raw_text"] and not _mentions_gating(combined_text):
                hints = ", ".join(command.availability + command.visibility_hints)
                findings["Missing visibility notes"].append(f"{canonical}: {hints}")
        if row and likely_overstrong_direct(row, command):
            findings["Likely-overstrong direct mappings"].append(
                f"{canonical}: upstream description '{command.description}'"
            )

    report = format_report(findings)
    print(report)
    total = sum(len(items) for items in findings.values())
    return 1 if args.strict and total else 0


if __name__ == "__main__":
    raise SystemExit(main())
