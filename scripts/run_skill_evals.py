from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from command_registry_lib import parse_alias_reference


STATUSES = {"direct", "approximate", "unavailable"}


@dataclass
class Fixture:
    id: str
    prompt: str
    expected_status: str
    expected_mapping_contains: list[str]
    notes: str


@dataclass
class EvalTarget:
    kind: str
    canonical: str
    phrases: list[str]
    status: str
    mechanism: str
    how_to_operate: str
    boundary: str
    reason: str

    @property
    def mapping_text(self) -> str:
        return " | ".join(
            part
            for part in (
                self.canonical,
                self.status,
                self.mechanism,
                self.how_to_operate,
                self.boundary,
                self.reason,
            )
            if part
        )


@dataclass
class EvalResult:
    fixture: Fixture
    actual: EvalTarget | None
    passed: bool
    failure_reasons: list[str]


def _normalize_text(text: str) -> str:
    return " ".join(text.lower().split())


def _parse_command_targets(skill_root: Path) -> list[EvalTarget]:
    mapping_path = skill_root / "references" / "command-mapping.md"
    alias_info = parse_alias_reference(skill_root / "references" / "aliases-and-visibility.md")
    canonical_commands: set[str] = set()
    raw_rows: list[tuple[str, list[str], str, str, str, str, str, str]] = []
    rows: list[EvalTarget] = []
    current_surface = ""
    for raw_line in mapping_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("## Slash Commands"):
            current_surface = "slash"
            continue
        if line.startswith("## CLI Subcommands"):
            current_surface = "cli"
            continue
        if not line.startswith("|") or line.startswith("| ---"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 7 or cells[0] in {"Claude Command", "Claude CLI Subcommand"}:
            continue
        codes = re.findall(r"`([^`]+)`", cells[0])
        if not codes:
            continue
        canonical = _normalize_code(codes[0])
        canonical_commands.add(canonical)
        raw_rows.append((current_surface, canonical, codes, cells[2], cells[3], cells[4], cells[5], cells[6]))

    for current_surface, canonical, codes, status, mechanism, how_to_operate, boundary, reason in raw_rows:
        phrases = set()
        for code in codes:
            normalized = _normalize_command_phrase(code, current_surface)
            if normalized:
                phrases.add(_normalize_text(normalized))
        alias_map = alias_info["slash_aliases"] if current_surface == "slash" else alias_info["cli_aliases"]
        for alias in alias_map.get(canonical, []):
            if alias in canonical_commands:
                continue
            phrases.add(_normalize_text(alias))
        if not phrases:
            continue
        rows.append(
            EvalTarget(
                kind="command",
                canonical=canonical,
                phrases=sorted(phrases, key=len, reverse=True),
                status=status,
                mechanism=mechanism,
                how_to_operate=how_to_operate,
                boundary=boundary,
                reason=reason,
            )
        )
    return rows


def _parse_workflow_targets(skill_root: Path) -> list[EvalTarget]:
    workflow_path = skill_root / "references" / "workflow-mapping.md"
    rows: list[EvalTarget] = []
    for raw_line in workflow_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or line.startswith("| ---"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 5 or cells[0] == "Claude Code Workflow":
            continue
        canonical = cells[0]
        phrases = {_normalize_text(canonical)}
        rows.append(
            EvalTarget(
                kind="workflow",
                canonical=canonical,
                phrases=sorted(phrases, key=len, reverse=True),
                status=cells[1],
                mechanism=cells[2],
                how_to_operate=cells[3],
                boundary=cells[4],
                reason="",
            )
        )
    return rows


def _normalize_code(code: str) -> str:
    code = code.strip()
    if not code.startswith("claude "):
        return code
    parts: list[str] = []
    for token in code.split():
        if token.startswith("<") or token.startswith("["):
            break
        parts.append(token)
    return " ".join(parts)


def _normalize_command_phrase(code: str, surface: str) -> str:
    code = code.strip()
    if surface == "slash":
        return code if code.startswith("/") else ""
    if code.startswith("claude "):
        return _normalize_code(code)
    return ""


def _load_fixtures(path: Path) -> list[Fixture]:
    data = json.loads(path.read_text(encoding="utf-8"))
    raw_fixtures: list[dict[str, Any]]
    if isinstance(data, list):
        raw_fixtures = data
    elif isinstance(data, dict) and isinstance(data.get("fixtures"), list):
        raw_fixtures = data["fixtures"]
    else:
        raise ValueError("Fixture file must be a JSON list or an object with a 'fixtures' list.")

    fixtures: list[Fixture] = []
    for item in raw_fixtures:
        status = item["expected_status"]
        if status not in STATUSES:
            raise ValueError(f"Invalid expected_status for fixture {item.get('id')}: {status}")
        contains = item.get("expected_mapping_contains", [])
        if isinstance(contains, str):
            contains = [contains]
        fixtures.append(
            Fixture(
                id=item["id"],
                prompt=item["prompt"],
                expected_status=status,
                expected_mapping_contains=contains,
                notes=item.get("notes", ""),
            )
        )
    return fixtures


def _match_target(prompt: str, targets: list[EvalTarget]) -> EvalTarget | None:
    normalized_prompt = _normalize_text(prompt)
    for target in sorted(targets, key=lambda item: max(len(phrase) for phrase in item.phrases), reverse=True):
        for phrase in target.phrases:
            if phrase and _phrase_match(normalized_prompt, phrase):
                return target
    return None


def _phrase_match(prompt: str, phrase: str) -> bool:
    pattern = re.compile(
        rf"(?<![a-z0-9_-]){re.escape(phrase)}(?![a-z0-9_-])",
        re.IGNORECASE,
    )
    return bool(pattern.search(prompt))


def _classify_prompt(prompt: str, command_targets: list[EvalTarget], workflow_targets: list[EvalTarget]) -> EvalTarget | None:
    command_match = _match_target(prompt, command_targets)
    if command_match is not None:
        return command_match
    return _match_target(prompt, workflow_targets)


def _evaluate_fixture(
    fixture: Fixture,
    command_targets: list[EvalTarget],
    workflow_targets: list[EvalTarget],
) -> EvalResult:
    actual = _classify_prompt(fixture.prompt, command_targets, workflow_targets)
    failure_reasons: list[str] = []
    if actual is None:
        failure_reasons.append("no_match")
        return EvalResult(fixture=fixture, actual=None, passed=False, failure_reasons=failure_reasons)

    if actual.status != fixture.expected_status:
        failure_reasons.append("status_mismatch")

    haystack = _normalize_text(actual.mapping_text)
    missing_phrases = [phrase for phrase in fixture.expected_mapping_contains if _normalize_text(phrase) not in haystack]
    if missing_phrases:
        failure_reasons.append(f"missing_mapping_text: {', '.join(missing_phrases)}")

    return EvalResult(
        fixture=fixture,
        actual=actual,
        passed=not failure_reasons,
        failure_reasons=failure_reasons,
    )


def _print_report(results: list[EvalResult]) -> None:
    total = len(results)
    passed = sum(1 for result in results if result.passed)
    failed = total - passed
    failed_ids = [result.fixture.id for result in results if not result.passed]

    print(f"Total samples: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Failed IDs: {', '.join(failed_ids) if failed_ids else '(none)'}")

    if not failed_ids:
        return

    print("")
    print("Failure details:")
    for result in results:
        if result.passed:
            continue
        actual_status = result.actual.status if result.actual else "(no match)"
        actual_mapping = result.actual.mapping_text if result.actual else "(no mapping text)"
        print(f"- {result.fixture.id}")
        print(f"  expected_status: {result.fixture.expected_status}")
        print(f"  actual_status: {actual_status}")
        if result.fixture.expected_mapping_contains:
            print(f"  expected_mapping_contains: {result.fixture.expected_mapping_contains}")
        print(f"  actual_mapping: {actual_mapping}")
        print(f"  reasons: {result.failure_reasons}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run minimal regression evals for the Claude Code for Codex skill.")
    parser.add_argument(
        "--skill-root",
        default=".",
        help="Path to the skill root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--fixtures",
        default="evals/fixtures/basic-regression.json",
        help="Path to the fixture JSON file.",
    )
    args = parser.parse_args()

    skill_root = Path(args.skill_root).resolve()
    fixtures_path = Path(args.fixtures)
    if not fixtures_path.is_absolute():
        fixtures_path = (skill_root / fixtures_path).resolve()

    command_targets = _parse_command_targets(skill_root)
    workflow_targets = _parse_workflow_targets(skill_root)
    fixtures = _load_fixtures(fixtures_path)

    results = [_evaluate_fixture(fixture, command_targets, workflow_targets) for fixture in fixtures]
    _print_report(results)
    return 1 if any(not result.passed for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
