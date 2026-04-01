from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable


STRING_RE = re.compile(r"'([^'\\]*(?:\\.[^'\\]*)*)'|\"([^\"\\]*(?:\\.[^\"\\]*)*)\"|`([^`\\]*(?:\\.[^`\\]*)*)`", re.S)
IMPORT_STMT_RE = re.compile(
    r"^\s*import\s+(?P<bindings>.*?)\s+from\s+'(?P<source>\./commands/[^']+)';?\s*$",
    re.S,
)
LAZY_REQUIRE_IN_STATEMENT_RE = re.compile(
    r"const\s+(?P<name>\w+)\s*=.*?require\('(?P<source>\./commands/[^']+)'\)",
    re.S,
)
COMMAND_CALL_RE = re.compile(
    r"(?P<parent>\w+)\s*\.\s*command\('(?P<signature>[^']+)'\s*(?:,\s*\{[^}]*\})?\)",
    re.S,
)

INLINE_COMMAND_METADATA = {
    "usageReport": {
        "name": "insights",
        "description": "Generate a report analyzing your Claude Code sessions",
    }
}

DIRECT_RISK_TERMS = (
    "plan mode",
    "per-turn",
    "current conversation",
    "clipboard",
    "qr code",
    "status line",
    "integration",
    "settings",
    "remote",
    "session",
    "usage",
    "cost",
    "plugin",
    "mcp",
    "memory files",
)


@dataclass
class RegistryCommand:
    canonical: str
    surface: str
    description: str = ""
    aliases: list[str] = field(default_factory=list)
    source_path: str = ""
    registry: str = ""
    availability: list[str] = field(default_factory=list)
    visibility_hints: list[str] = field(default_factory=list)
    feature_hints: list[str] = field(default_factory=list)
    internal: bool = False


@dataclass
class MappingRow:
    canonical: str
    codes: list[str]
    status: str
    intent: str
    boundary: str
    reason: str
    surface: str


def _collapse(text: str) -> str:
    return " ".join(text.split())


def _extract_strings(text: str) -> list[str]:
    values: list[str] = []
    for match in STRING_RE.finditer(text):
        value = next(group for group in match.groups() if group is not None)
        cleaned = _collapse(value.replace("\\n", " ").replace("\\t", " "))
        if cleaned:
            values.append(cleaned)
    return values


def _parse_bindings(bindings: str) -> list[str]:
    names: list[str] = []
    cleaned = " ".join(bindings.split())
    if "{" in cleaned:
        default_part, named_part = cleaned.split("{", 1)
        default_name = default_part.strip().rstrip(",")
        if default_name:
            names.append(default_name)
        named_part = named_part.split("}", 1)[0]
        for item in named_part.split(","):
            token = item.strip()
            if not token:
                continue
            if " as " in token:
                token = token.split(" as ", 1)[1].strip()
            names.append(token)
        return names
    if cleaned:
        names.append(cleaned.strip().rstrip(","))
    return names


def _resolve_source(repo_root: Path, source: str) -> Path | None:
    relative = source.removeprefix("./")
    base = repo_root / "src" / relative
    candidates = []
    if base.suffix == ".js":
        candidates.extend([base.with_suffix(".ts"), base.with_suffix(".tsx")])
    candidates.extend([base, base.with_suffix(".ts"), base.with_suffix(".tsx")])
    if base.name == "index.js":
        candidates.extend(
            [
                base.with_name("index.ts"),
                base.with_name("index.tsx"),
                base.with_name(f"{base.parent.name}.ts"),
                base.with_name(f"{base.parent.name}.tsx"),
            ]
        )
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _infer_name_from_source(source: str, symbol: str = "") -> str:
    relative = source.removeprefix("./")
    path = Path(relative)
    if path.name.startswith("index.") and path.parent.name:
        raw = path.parent.name
    elif path.stem:
        raw = path.stem
    else:
        raw = symbol
    inferred = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", raw).replace("_", "-")
    return inferred.lower()


def _extract_bracket_block_after_regex(text: str, pattern: str) -> str:
    match = re.search(pattern, text, re.S)
    if not match:
        return ""
    start = match.end() - 1
    depth = 0
    for index in range(start, len(text)):
        char = text[index]
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    return ""


def _extract_array_identifiers(block: str) -> list[str]:
    identifiers: list[str] = []
    for raw_line in block.splitlines():
        line = raw_line.split("//", 1)[0].strip()
        if not line or line in {"[", "]"}:
            continue
        if line.startswith("...") and "[" in line and "]" in line:
            inside = line.split("[", 1)[1].split("]", 1)[0]
            for item in inside.split(","):
                token = item.strip().removesuffix("()")
                if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", token):
                    identifiers.append(token)
            continue
        match = re.match(r"(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*(?:\(\))?,?$", line)
        if match:
            identifiers.append(match.group("name"))
    return identifiers


def _extract_property_window(text: str, pattern: str, width: int = 500) -> str:
    match = re.search(pattern, text)
    if not match:
        return ""
    start = match.end()
    return text[start : start + width]


def _extract_description(text: str) -> str:
    for pattern in (r"\bdescription\s*:\s*", r"\bget\s+description\s*\(\)\s*\{"):
        window = _extract_property_window(text, pattern)
        if not window:
            continue
        strings = _extract_strings(window)
        if strings:
            return _collapse(" ".join(strings[:4]))
    return ""


def _extract_scalar_property(text: str, prop: str) -> str:
    match = re.search(rf"\b{re.escape(prop)}\s*:\s*(?P<body>[^\n,]+)", text)
    if not match:
        return ""
    strings = _extract_strings(match.group("body"))
    return strings[0] if strings else ""


def _extract_list_property(text: str, prop: str) -> list[str]:
    match = re.search(
        rf"\b{re.escape(prop)}\s*:\s*(?P<body>.*?)(?:,\s*\n\s*[A-Za-z_][A-Za-z0-9_]*\s*:|\n\s*[A-Za-z_][A-Za-z0-9_]*\s*:|\n\s*\}})",
        text,
        re.S,
    )
    if not match:
        return []
    body = match.group("body")
    values: list[str] = []
    for array_match in re.finditer(r"\[(.*?)\]", body, re.S):
        values.extend(_extract_strings(array_match.group(1)))
    return values


def _parse_command_metadata(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    metadata: dict[str, object] = {
        "name": _extract_scalar_property(text, "name"),
        "description": _extract_description(text),
        "aliases": _extract_list_property(text, "aliases"),
        "availability": _extract_list_property(text, "availability"),
        "visibility_hints": [],
    }
    visibility_hints: list[str] = metadata["visibility_hints"]  # type: ignore[assignment]
    if "isEnabled" in text:
        visibility_hints.append("isEnabled")
    if re.search(r"\bisHidden\b", text):
        visibility_hints.append("hidden")
    if re.search(r"supportsNonInteractive\s*:\s*false", text):
        visibility_hints.append("noninteractive=false")
    return metadata


def _extract_object_body(text: str, symbol: str) -> str:
    patterns = [
        rf"\bconst\s+{re.escape(symbol)}\b[^=]*=\s*\{{",
        rf"\bexport default\s+{re.escape(symbol)}\b",
        r"\bexport default\s*\{",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if not match:
            continue
        start = text.find("{", match.start())
        if start == -1:
            continue
        depth = 0
        for index in range(start, len(text)):
            char = text[index]
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    return text[start : index + 1]
    export_match = re.search(r"\bexport default\s+(\w+)\b", text)
    if export_match:
        return _extract_object_body(text, export_match.group(1))
    return text


def _infer_name(path: Path, symbol: str) -> str:
    if path.name.startswith("index."):
        return path.parent.name.replace("_", "-")
    if path.stem and path.stem not in {"index", "_default"}:
        return path.stem.replace("_", "-")
    if symbol and symbol not in {"command", "default"}:
        inferred = re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", symbol).replace("_", "-")
        return inferred.lower()
    return path.stem.replace("_", "-")


def _parse_command_metadata_for_symbol(path: Path, symbol: str) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    body = _extract_object_body(text, symbol)
    name = _extract_scalar_property(body, "name")
    if not name or name == "stub":
        name = _infer_name(path, symbol)
    metadata: dict[str, object] = {
        "name": name,
        "description": _extract_description(body),
        "aliases": _extract_list_property(body, "aliases"),
        "availability": _extract_list_property(body, "availability"),
        "visibility_hints": [],
    }
    visibility_hints: list[str] = metadata["visibility_hints"]  # type: ignore[assignment]
    if "isEnabled" in body:
        visibility_hints.append("isEnabled")
    if re.search(r"\bisHidden\b", body):
        visibility_hints.append("hidden")
    if re.search(r"supportsNonInteractive\s*:\s*false", body):
        visibility_hints.append("noninteractive=false")
    return metadata


def _merge_commands(commands: Iterable[RegistryCommand]) -> list[RegistryCommand]:
    merged: dict[str, RegistryCommand] = {}
    for command in commands:
        existing = merged.get(command.canonical)
        if existing is None:
            merged[command.canonical] = command
            continue
        if command.description and not existing.description:
            existing.description = command.description
        if command.source_path and not existing.source_path:
            existing.source_path = command.source_path
        if command.registry and command.registry not in existing.registry:
            existing.registry = ",".join(filter(None, [existing.registry, command.registry])).strip(",")
        existing.internal = existing.internal or command.internal
        existing.aliases = sorted(set(existing.aliases) | set(command.aliases))
        existing.availability = sorted(set(existing.availability) | set(command.availability))
        existing.visibility_hints = sorted(
            set(existing.visibility_hints) | set(command.visibility_hints)
        )
        existing.feature_hints = sorted(set(existing.feature_hints) | set(command.feature_hints))
    return sorted(merged.values(), key=lambda item: item.canonical)


def extract_upstream_commands(repo_root: Path) -> dict[str, object]:
    commands_ts = (repo_root / "src" / "commands.ts").read_text(encoding="utf-8")
    import_sources: dict[str, str] = {}
    for statement in _iter_import_statements(commands_ts):
        match = IMPORT_STMT_RE.match(statement)
        if not match:
            continue
        source = match.group("source")
        for binding in _parse_bindings(match.group("bindings")):
            import_sources[binding] = source
    for statement in _iter_const_statements(commands_ts):
        match = LAZY_REQUIRE_IN_STATEMENT_RE.search(statement)
        if match:
            import_sources[match.group("name")] = match.group("source")

    builtins = _extract_array_identifiers(
        _extract_bracket_block_after_regex(commands_ts, r"const COMMANDS\b.*?=>\s*\[")
    )
    internal_only = _extract_array_identifiers(
        _extract_bracket_block_after_regex(
            commands_ts, r"export const INTERNAL_ONLY_COMMANDS\s*=\s*\["
        )
    )

    slash_commands: list[RegistryCommand] = []
    all_identifiers = [(identifier, False) for identifier in builtins]
    all_identifiers.extend((identifier, True) for identifier in internal_only)
    for identifier, is_internal in all_identifiers:
        inline = INLINE_COMMAND_METADATA.get(identifier)
        if inline:
            slash_commands.append(
                RegistryCommand(
                    canonical=f"/{inline['name']}",
                    surface="slash",
                    description=str(inline["description"]),
                    source_path="src/commands.ts",
                    registry="internal" if is_internal else "builtin",
                    internal=is_internal,
                )
            )
            continue
        source = import_sources.get(identifier)
        if not source:
            continue
        resolved = _resolve_source(repo_root, source)
        if resolved is None:
            name = _infer_name_from_source(source, identifier)
            slash_commands.append(
                RegistryCommand(
                    canonical=f"/{name}",
                    surface="slash",
                    description="",
                    aliases=[],
                    source_path=source,
                    registry="internal" if is_internal else "builtin",
                    visibility_hints=["unresolved-source"],
                    internal=is_internal,
                )
            )
            continue
        metadata = _parse_command_metadata_for_symbol(resolved, identifier)
        name = str(metadata["name"] or "").strip()
        if not name:
            continue
        aliases = [f"/{alias}" for alias in metadata["aliases"]]  # type: ignore[index]
        slash_commands.append(
            RegistryCommand(
                canonical=f"/{name}",
                surface="slash",
                description=str(metadata["description"]),
                aliases=aliases,
                source_path=str(resolved.relative_to(repo_root)),
                registry="internal" if is_internal else "builtin",
                availability=list(metadata["availability"]),  # type: ignore[arg-type]
                visibility_hints=list(metadata["visibility_hints"]),  # type: ignore[arg-type]
                internal=is_internal,
            )
        )

    cli_commands = _extract_cli_commands(repo_root)
    return {
        "repo_root": str(repo_root),
        "slash_commands": [asdict(command) for command in _merge_commands(slash_commands)],
        "cli_commands": [asdict(command) for command in _merge_commands(cli_commands)],
    }


def _extract_cli_commands(repo_root: Path) -> list[RegistryCommand]:
    commands: list[RegistryCommand] = []
    main_path = repo_root / "src" / "main.tsx"
    main_text = main_path.read_text(encoding="utf-8")
    commands.extend(_parse_commander_commands(main_text, main_path, {"program": ""}))

    add_path = repo_root / "src" / "commands" / "mcp" / "addCommand.ts"
    if add_path.exists():
        commands.extend(_parse_commander_commands(add_path.read_text(encoding="utf-8"), add_path, {"mcp": "mcp"}))

    xaa_path = repo_root / "src" / "commands" / "mcp" / "xaaIdpCommand.ts"
    if xaa_path.exists():
        commands.extend(_parse_commander_commands(xaa_path.read_text(encoding="utf-8"), xaa_path, {"mcp": "mcp"}))

    cli_entrypoint = repo_root / "src" / "entrypoints" / "cli.tsx"
    if cli_entrypoint.exists():
        entry_text = cli_entrypoint.read_text(encoding="utf-8")
        legacy_block = re.search(
            r'feature\("BRIDGE_MODE"\)\s*&&\s*\((?P<body>.*?)\)\s*\)\s*\{',
            entry_text,
            re.S,
        )
        legacy_aliases = (
            re.findall(r'args\[0\]\s*===\s*"([^"]+)"', legacy_block.group("body"))
            if legacy_block
            else []
        )
        if legacy_aliases:
            commands.append(
                RegistryCommand(
                    canonical="claude remote-control",
                    surface="cli",
                    aliases=[f"claude {alias}" for alias in legacy_aliases if alias != "remote-control"],
                    description="Connect your local environment for remote-control sessions",
                    source_path=str(cli_entrypoint.relative_to(repo_root)),
                    registry="builtin",
                    visibility_hints=["legacy-alias"],
                )
            )
        commands.extend(_extract_cli_fast_paths(entry_text, cli_entrypoint))

    return commands


def _extract_cli_fast_paths(text: str, source_path: Path) -> list[RegistryCommand]:
    commands: list[RegistryCommand] = []
    fast_paths = [
        ("claude daemon", "Start or manage the daemon supervisor"),
        ("claude ps", "List Claude background sessions"),
        ("claude logs", "Inspect Claude background session logs"),
        ("claude attach", "Attach to a background Claude session"),
        ("claude kill", "Kill a background Claude session"),
        ("claude new", "Create a template job"),
        ("claude list", "List template jobs"),
        ("claude reply", "Reply to a template job"),
        ("claude environment-runner", "Run BYOC environment runner"),
        ("claude self-hosted-runner", "Run self-hosted worker service"),
    ]
    for canonical, description in fast_paths:
        command_name = canonical.split()[-1]
        if re.search(rf'args\[0\]\s*===\s*"{re.escape(command_name)}"', text):
            commands.append(
                RegistryCommand(
                    canonical=canonical,
                    surface="cli",
                    description=description,
                    source_path=str(source_path.relative_to(source_path.parents[2])),
                    registry="builtin",
                    visibility_hints=["fast-path"],
                )
            )
    return commands


def _parse_commander_commands(
    text: str,
    source_path: Path,
    initial_paths: dict[str, str],
) -> list[RegistryCommand]:
    variable_paths = dict(initial_paths)
    commands: list[RegistryCommand] = []
    for match in COMMAND_CALL_RE.finditer(text):
        parent = match.group("parent")
        signature = match.group("signature")
        parent_path = variable_paths.get(parent, "")
        segment = signature.strip().split()[0]
        full_path = " ".join(part for part in (parent_path, segment) if part).strip()
        if not full_path:
            continue
        assigned_var = _find_assigned_variable(text, match.start())
        window = _command_chain_window(text, match.end())
        description = _extract_chain_description(window)
        aliases = [f"claude {' '.join(part for part in (parent_path, alias) if part)}" for alias in re.findall(r"\.alias\('([^']+)'\)", window)]
        visibility_hints: list[str] = []
        lookaround = text[max(0, match.start() - 40) : match.end() + 120]
        if "hidden: true" in lookaround or ".hideHelp(" in window:
            visibility_hints.append("hidden")
        if ".action(" not in window:
            visibility_hints.append("container")
        internal = "[ANT-ONLY]" in description
        commands.append(
            RegistryCommand(
                canonical=f"claude {full_path}".strip(),
                surface="cli",
                description=description,
                aliases=aliases,
                source_path=str(source_path),
                registry="builtin",
                visibility_hints=visibility_hints,
                internal=internal,
            )
        )
        if assigned_var:
            variable_paths[assigned_var] = full_path
    return commands


def _find_assigned_variable(text: str, index: int) -> str | None:
    prefix = text[max(0, index - 60) : index]
    match = re.search(r"const\s+(\w+)\s*=\s*$", prefix)
    return match.group(1) if match else None


def _command_chain_window(text: str, start: int, max_width: int = 2000) -> str:
    snippet = text[start : start + max_width]
    end_markers = [
        snippet.find(".action("),
        snippet.find(";\n"),
        snippet.find("\n  const "),
        snippet.find("\n  program.command("),
        snippet.find("\n  if ("),
        snippet.find("\n  //"),
    ]
    valid = [marker for marker in end_markers if marker > 0]
    if valid:
        snippet = snippet[: min(valid)]
    return snippet


def _extract_chain_description(text: str) -> str:
    match = re.search(r"\.description\((?P<body>.*?)\)", text, re.S)
    if not match:
        return ""
    strings = _extract_strings(match.group("body"))
    return _collapse(" ".join(strings[:8]))


def parse_mapping_rows(mapping_path: Path) -> list[MappingRow]:
    rows: list[MappingRow] = []
    text = mapping_path.read_text(encoding="utf-8")
    surface = "unknown"
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("## Slash Commands"):
            surface = "slash"
            continue
        if line.startswith("## CLI Subcommands"):
            surface = "cli"
            continue
        if not line.startswith("|") or line.startswith("| ---"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 7 or cells[0] in {"Claude Command", "Claude CLI Subcommand"}:
            continue
        codes = re.findall(r"`([^`]+)`", cells[0])
        if not codes:
            continue
        normalized_codes = [_normalize_code(code) for code in codes]
        rows.append(
            MappingRow(
                canonical=normalized_codes[0],
                codes=normalized_codes,
                intent=cells[1],
                status=cells[2],
                boundary=cells[5],
                reason=cells[6],
                surface=surface,
            )
        )
    return rows


def parse_alias_reference(alias_path: Path) -> dict[str, object]:
    text = alias_path.read_text(encoding="utf-8")
    slash_aliases: dict[str, set[str]] = {}
    cli_aliases: dict[str, set[str]] = {}
    current_surface = ""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("## Common Slash Command Aliases"):
            current_surface = "slash"
            continue
        if line.startswith("## Common CLI Aliases"):
            current_surface = "cli"
            continue
        if not line.startswith("|") or line.startswith("| ---"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 3 or cells[0] in {"Canonical Command", "Canonical CLI Form"}:
            continue
        canonical_codes = re.findall(r"`([^`]+)`", cells[0])
        alias_codes = re.findall(r"`([^`]+)`", cells[1])
        if not canonical_codes:
            continue
        target = slash_aliases if current_surface == "slash" else cli_aliases
        target.setdefault(_normalize_code(canonical_codes[0]), set()).update(
            _normalize_code(code) for code in alias_codes
        )
    return {
        "slash_aliases": {key: sorted(value) for key, value in slash_aliases.items()},
        "cli_aliases": {key: sorted(value) for key, value in cli_aliases.items()},
        "raw_text": text,
    }


def likely_overstrong_direct(mapping_row: MappingRow, upstream: RegistryCommand) -> bool:
    if mapping_row.status != "direct":
        return False
    haystack = " ".join(
        [
            upstream.description.lower(),
            " ".join(upstream.visibility_hints).lower(),
            " ".join(upstream.availability).lower(),
        ]
    )
    return any(term in haystack for term in DIRECT_RISK_TERMS)


def _normalize_code(code: str) -> str:
    if not code.startswith("claude "):
        return code.strip()
    parts = []
    for token in code.split():
        if token.startswith("<") or token.startswith("["):
            break
        parts.append(token)
    return " ".join(parts)


def _iter_import_statements(text: str) -> list[str]:
    statements: list[str] = []
    buffer: list[str] = []
    collecting = False
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.lstrip()
        if not collecting and not stripped.startswith("import "):
            continue
        if not collecting:
            buffer = [line.strip()]
            collecting = True
            if " from " in line:
                statement = " ".join(buffer)
                if " from './commands/" in statement:
                    statements.append(statement)
                buffer = []
                collecting = False
            continue
        if stripped.startswith("import "):
            statement = " ".join(buffer)
            if " from './commands/" in statement:
                statements.append(statement)
            buffer = [line.strip()]
            collecting = True
            if " from " in line:
                statement = " ".join(buffer)
                if " from './commands/" in statement:
                    statements.append(statement)
                buffer = []
                collecting = False
            continue
        buffer.append(line.strip())
        if " from " in line:
            statement = " ".join(buffer)
            if " from './commands/" in statement:
                statements.append(statement)
            buffer = []
            collecting = False
    return statements


def _iter_const_statements(text: str) -> list[str]:
    pattern = re.compile(
        r"(^\s*const\s+\w+\s*=.*?)(?=^\s*const\s+\w+\s*=|^\s*import\s+|^\s*export\s+|\Z)",
        re.S | re.M,
    )
    return [" ".join(match.group(1).splitlines()) for match in pattern.finditer(text)]


def format_report(findings: dict[str, list[str]]) -> str:
    lines: list[str] = []
    total = sum(len(items) for items in findings.values())
    lines.append(f"Findings: {total}")
    for section, items in findings.items():
        if not items:
            continue
        lines.append("")
        lines.append(section)
        for item in items:
            lines.append(f"- {item}")
    if total == 0:
        lines.append("")
        lines.append("No findings.")
    return "\n".join(lines)


def dump_json(data: object, path: Path | None = None) -> str:
    rendered = json.dumps(data, indent=2, ensure_ascii=True)
    if path is not None:
        path.write_text(rendered + "\n", encoding="utf-8")
    return rendered
