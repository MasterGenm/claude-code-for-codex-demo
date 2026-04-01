from __future__ import annotations

import argparse
from pathlib import Path

from command_registry_lib import dump_json, extract_upstream_commands


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract upstream Claude Code slash and CLI command metadata.",
    )
    parser.add_argument("--repo", required=True, help="Path to the upstream Claude Code repo")
    parser.add_argument(
        "--json-out",
        help="Optional path to write normalized JSON output",
    )
    parser.add_argument(
        "--stdout",
        choices=("summary", "json"),
        default="summary",
        help="What to print to stdout",
    )
    args = parser.parse_args()

    data = extract_upstream_commands(Path(args.repo))
    if args.json_out:
        dump_json(data, Path(args.json_out))

    if args.stdout == "json":
        print(dump_json(data))
        return 0

    slash_count = len(data["slash_commands"])
    cli_count = len(data["cli_commands"])
    print(f"Repo: {data['repo_root']}")
    print(f"Slash commands: {slash_count}")
    print(f"CLI commands: {cli_count}")
    if args.json_out:
        print(f"JSON: {args.json_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
