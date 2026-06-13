"""Fail-closed inventory auditor for the Glass-Chess canary.

Phase 1 of the Perception Integrity Layer.

Doctrine:
- Enumerate first.
- Search second.
- Compare both directions.
- Preserve UNKNOWN.
- Never certify completeness from relevance-ranked retrieval.

The module is standard-library only and accepts newline, numbered Markdown,
GitHub URLs, or JSON emitted by ``gh repo list --json ...``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence


NAME_KEYS = (
    "nameWithOwner",
    "name_with_owner",
    "full_name",
    "repository_full_name",
    "name",
)
CONTAINER_KEYS = ("repositories", "repos", "items", "results", "data")
LINE_PREFIX = re.compile(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)")
GITHUB_PREFIX = re.compile(
    r"^(?:https?://github\.com/|git@github\.com:)", re.IGNORECASE
)
GIT_SUFFIX = re.compile(r"\.git$", re.IGNORECASE)
NON_ALNUM = re.compile(r"[^a-z0-9]+")


class InventoryParseError(ValueError):
    """Raised when an inventory cannot be parsed."""


@dataclass(frozen=True)
class InventoryRecord:
    display_name: str
    key: str


@dataclass(frozen=True)
class DuplicateRecord:
    key: str
    occurrences: tuple[str, ...]


@dataclass(frozen=True)
class CanaryResult:
    canary: str
    present: bool
    matched_name: str | None


@dataclass(frozen=True)
class OutlierRecord:
    name: str
    score: float


@dataclass(frozen=True)
class UnknownEntry:
    unknown_id: str
    expected_object: str
    reason_expected: str
    missing_from: str
    resolution_requirement: str
    status: str = "UNKNOWN"


@dataclass(frozen=True)
class AuditReport:
    status: str
    canon_eligible: bool
    expected_source: str
    actual_source: str
    expected_raw_count: int
    expected_unique_count: int
    actual_raw_count: int
    actual_unique_count: int
    declared_expected_count: int
    returned_count_matches_declared: bool
    pagination_complete: str
    scope_declared: bool
    missing: tuple[str, ...]
    unexpected: tuple[str, ...]
    duplicates: tuple[DuplicateRecord, ...]
    canaries: tuple[CanaryResult, ...]
    lexical_outliers: tuple[OutlierRecord, ...]
    expected_sha256: str
    actual_sha256: str
    unknown_ledger: tuple[UnknownEntry, ...]
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalize_name(value: str) -> InventoryRecord:
    """Normalize a repository identifier while preserving display spelling."""
    display = value.strip().strip("`'\"")
    display = LINE_PREFIX.sub("", display).strip()
    display = GITHUB_PREFIX.sub("", display)
    display = display.split("?", 1)[0].split("#", 1)[0].strip("/")
    display = GIT_SUFFIX.sub("", display)
    if not display:
        raise InventoryParseError("Encountered a blank repository name.")
    return InventoryRecord(display_name=display, key=display.casefold())


def _extract_json_names(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        result: list[str] = []
        for item in value:
            result.extend(_extract_json_names(item))
        return result
    if not isinstance(value, dict):
        return []

    for key in NAME_KEYS:
        candidate = value.get(key)
        if isinstance(candidate, str) and candidate.strip():
            return [candidate]

    result: list[str] = []
    used_container = False
    for key in CONTAINER_KEYS:
        if key in value:
            used_container = True
            result.extend(_extract_json_names(value[key]))
    if not used_container:
        for candidate in value.values():
            if isinstance(candidate, (dict, list)):
                result.extend(_extract_json_names(candidate))
    return result


def parse_inventory_text(text: str, source: str = "<memory>") -> list[InventoryRecord]:
    """Parse newline, numbered Markdown, JSON, or gh-cli inventory text."""
    stripped = text.lstrip()
    if not stripped:
        raise InventoryParseError(f"{source}: inventory is empty.")

    if stripped[0] in "[{":
        try:
            raw_names = _extract_json_names(json.loads(text))
        except json.JSONDecodeError as exc:
            raise InventoryParseError(f"{source}: invalid JSON: {exc}") from exc
    else:
        raw_names = []
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            line = LINE_PREFIX.sub("", line).strip()
            if line and not line.endswith(":"):
                raw_names.append(line)

    records = [normalize_name(name) for name in raw_names]
    if not records:
        raise InventoryParseError(f"{source}: no repository names found.")
    return records


def load_inventory(path: Path) -> list[InventoryRecord]:
    try:
        return parse_inventory_text(path.read_text(encoding="utf-8"), str(path))
    except OSError as exc:
        raise InventoryParseError(f"{path}: cannot read inventory: {exc}") from exc


def _unique_map(records: Sequence[InventoryRecord]) -> dict[str, str]:
    result: dict[str, str] = {}
    for record in records:
        result.setdefault(record.key, record.display_name)
    return result


def find_duplicates(records: Sequence[InventoryRecord]) -> tuple[DuplicateRecord, ...]:
    occurrences: dict[str, list[str]] = {}
    for record in records:
        occurrences.setdefault(record.key, []).append(record.display_name)
    return tuple(
        sorted(
            (
                DuplicateRecord(key=key, occurrences=tuple(values))
                for key, values in occurrences.items()
                if len(values) > 1
            ),
            key=lambda item: item.key,
        )
    )


def _trigrams(value: str) -> set[str]:
    compact = NON_ALNUM.sub("", value.casefold())
    if len(compact) < 3:
        return {compact} if compact else set()
    return {compact[index : index + 3] for index in range(len(compact) - 2)}


def _jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 1.0


def lexical_outliers(
    records: Sequence[InventoryRecord], limit: int = 5
) -> tuple[OutlierRecord, ...]:
    """Return low-similarity names as a lightweight Phase-1 heuristic."""
    unique = list(_unique_map(records).items())
    if len(unique) <= 1 or limit <= 0:
        return ()

    grams = {key: _trigrams(key.rsplit("/", 1)[-1]) for key, _ in unique}
    scored: list[OutlierRecord] = []
    for key, display in unique:
        similarities = sorted(
            (
                _jaccard(grams[key], grams[other])
                for other, _ in unique
                if other != key
            ),
            reverse=True,
        )
        nearest = similarities[: min(3, len(similarities))]
        mean_nearest = sum(nearest) / len(nearest) if nearest else 0.0
        scored.append(
            OutlierRecord(name=display, score=round(1.0 - mean_nearest, 6))
        )
    return tuple(
        sorted(scored, key=lambda item: (-item.score, item.name.casefold()))[:limit]
    )


def stable_hash(names: Iterable[str]) -> str:
    normalized = "\n".join(sorted(name.casefold() for name in names)) + "\n"
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def audit_inventory(
    expected: Sequence[InventoryRecord],
    actual: Sequence[InventoryRecord],
    *,
    expected_source: str,
    actual_source: str,
    declared_expected_count: int | None = None,
    pagination_complete: str = "unknown",
    scope_declared: bool = False,
    canaries: Sequence[str] = ("glass-chess",),
    outlier_limit: int = 5,
) -> AuditReport:
    """Run the two-way, fail-closed inventory audit."""
    if pagination_complete not in {"true", "false", "unknown"}:
        raise ValueError("pagination_complete must be true, false, or unknown")

    expected_map = _unique_map(expected)
    actual_map = _unique_map(actual)
    expected_keys = set(expected_map)
    actual_keys = set(actual_map)

    missing = tuple(expected_map[key] for key in sorted(expected_keys - actual_keys))
    unexpected = tuple(actual_map[key] for key in sorted(actual_keys - expected_keys))
    duplicates = find_duplicates(actual)
    declared = (
        declared_expected_count
        if declared_expected_count is not None
        else len(expected_map)
    )
    count_matches = len(actual_map) == declared

    canary_results: list[CanaryResult] = []
    for canary in canaries:
        normalized = normalize_name(canary)
        match = actual_map.get(normalized.key)
        if match is None and "/" not in normalized.key:
            suffix = f"/{normalized.key}"
            matches = [
                display for key, display in actual_map.items() if key.endswith(suffix)
            ]
            match = matches[0] if len(matches) == 1 else None
        canary_results.append(
            CanaryResult(canary=canary, present=match is not None, matched_name=match)
        )

    absent_canaries = [item.canary for item in canary_results if not item.present]
    reasons: list[str] = []
    if missing:
        reasons.append(f"{len(missing)} expected member(s) are missing.")
    if unexpected:
        reasons.append(f"{len(unexpected)} unexpected member(s) are present.")
    if duplicates:
        reasons.append(f"{len(duplicates)} duplicate key(s) were detected.")
    if not count_matches:
        reasons.append(
            f"Returned unique count {len(actual_map)} does not match "
            f"declared expected count {declared}."
        )
    if pagination_complete != "true":
        reasons.append(f"Pagination completeness is {pagination_complete}.")
    if not scope_declared:
        reasons.append("Inventory scope was not explicitly declared.")
    if absent_canaries:
        reasons.append("Missing canary/canaries: " + ", ".join(absent_canaries) + ".")

    hard_failure = bool(
        missing or unexpected or duplicates or not count_matches or absent_canaries
    )
    partial_view = pagination_complete != "true" or not scope_declared
    status = "FAIL_CLOSED" if hard_failure else (
        "PARTIAL_VIEW" if partial_view else "PASS"
    )

    unknown_entries = [
        UnknownEntry(
            unknown_id=f"UNKNOWN_EXPECTED_MEMBER_{index:03d}",
            expected_object=name,
            reason_expected=(
                "Present in canonical inventory but absent from actual inventory."
            ),
            missing_from=actual_source,
            resolution_requirement=(
                "Obtain an authoritative full enumeration and verify owner/name."
            ),
        )
        for index, name in enumerate(missing, start=1)
    ]

    residual = max(0, declared - len(actual_map) - len(missing))
    unknown_entries.extend(
        UnknownEntry(
            unknown_id=f"UNRESOLVED_INVENTORY_DELTA_{index:03d}",
            expected_object="<unresolved>",
            reason_expected=(
                "Declared expected count exceeds returned unique count, but the "
                "canonical set does not identify the missing object."
            ),
            missing_from=actual_source,
            resolution_requirement=(
                "Enumerate the authoritative source; do not repair with semantic search."
            ),
        )
        for index in range(1, residual + 1)
    )

    return AuditReport(
        status=status,
        canon_eligible=status == "PASS",
        expected_source=expected_source,
        actual_source=actual_source,
        expected_raw_count=len(expected),
        expected_unique_count=len(expected_map),
        actual_raw_count=len(actual),
        actual_unique_count=len(actual_map),
        declared_expected_count=declared,
        returned_count_matches_declared=count_matches,
        pagination_complete=pagination_complete,
        scope_declared=scope_declared,
        missing=missing,
        unexpected=unexpected,
        duplicates=duplicates,
        canaries=tuple(canary_results),
        lexical_outliers=lexical_outliers(actual, outlier_limit),
        expected_sha256=stable_hash(expected_map.values()),
        actual_sha256=stable_hash(actual_map.values()),
        unknown_ledger=tuple(unknown_entries),
        reasons=tuple(reasons),
    )


def format_human(report: AuditReport) -> str:
    """Render a concise human-readable witness report."""
    lines = [
        "Glass-Chess Canary Inventory Audit",
        "===================================",
        f"Status: {report.status}",
        f"Canon eligible: {'YES' if report.canon_eligible else 'NO'}",
        f"Expected source: {report.expected_source}",
        f"Actual source: {report.actual_source}",
        (
            "Counts: "
            f"expected unique={report.expected_unique_count}, "
            f"declared expected={report.declared_expected_count}, "
            f"actual raw={report.actual_raw_count}, "
            f"actual unique={report.actual_unique_count}"
        ),
        f"Pagination complete: {report.pagination_complete}",
        f"Scope declared: {'yes' if report.scope_declared else 'no'}",
        f"Expected SHA-256: {report.expected_sha256}",
        f"Actual SHA-256:   {report.actual_sha256}",
    ]

    def section(title: str, values: Sequence[str]) -> None:
        lines.extend(["", title])
        if values:
            lines.extend(f"- {value}" for value in values)
        else:
            lines.append("- none")

    section("Missing", report.missing)
    section("Unexpected", report.unexpected)
    section(
        "Duplicates",
        tuple(
            f"{item.key}: {', '.join(item.occurrences)}" for item in report.duplicates
        ),
    )
    section(
        "Canaries",
        tuple(
            f"{item.canary}: PASS ({item.matched_name})"
            if item.present
            else f"{item.canary}: FAIL"
            for item in report.canaries
        ),
    )
    section(
        "Lexical outliers",
        tuple(f"{item.name}: {item.score:.6f}" for item in report.lexical_outliers),
    )
    section("Reasons", report.reasons)
    section(
        "UNKNOWN ledger",
        tuple(
            f"{item.unknown_id}: {item.expected_object} — {item.reason_expected}"
            for item in report.unknown_ledger
        ),
    )
    return "\n".join(lines)


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="glass-chess-canary",
        description=(
            "Fail-closed inventory auditor: enumerate first, compare both "
            "directions, preserve UNKNOWN."
        ),
    )
    commands = parser.add_subparsers(dest="command", required=True)
    inventory = commands.add_parser("inventory", help="Audit expected vs actual inventory.")
    inventory.add_argument("--expected", required=True, type=Path)
    inventory.add_argument("--actual", required=True, type=Path)
    inventory.add_argument("--expected-count", type=int)
    inventory.add_argument(
        "--pagination-complete",
        choices=("true", "false", "unknown"),
        default="unknown",
    )
    inventory.add_argument(
        "--scope",
        help=(
            "Declared scope, e.g. owner=bekingdomcomejoker-cpu; visibility=all; "
            "archived=included; forks=included"
        ),
    )
    inventory.add_argument(
        "--canary",
        action="append",
        dest="canaries",
        help="Expected canary; repeat for multiple. Defaults to glass-chess.",
    )
    inventory.add_argument("--outlier-limit", type=int, default=5)
    inventory.add_argument("--format", choices=("human", "json"), default="human")
    inventory.add_argument("--write-report", type=Path)
    inventory.add_argument("--write-unknown-ledger", type=Path)
    return parser


def run_inventory(args: argparse.Namespace) -> int:
    expected = load_inventory(args.expected)
    actual = load_inventory(args.actual)
    report = audit_inventory(
        expected,
        actual,
        expected_source=str(args.expected),
        actual_source=str(args.actual),
        declared_expected_count=args.expected_count,
        pagination_complete=args.pagination_complete,
        scope_declared=bool(args.scope and args.scope.strip()),
        canaries=tuple(args.canaries or ("glass-chess",)),
        outlier_limit=max(0, args.outlier_limit),
    )
    payload = report.to_dict()
    print(
        json.dumps(payload, indent=2, ensure_ascii=False)
        if args.format == "json"
        else format_human(report)
    )
    if args.write_report:
        _write_json(args.write_report, payload)
    if args.write_unknown_ledger:
        _write_json(
            args.write_unknown_ledger,
            [asdict(item) for item in report.unknown_ledger],
        )
    return 0 if report.canon_eligible else 2


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "inventory":
            return run_inventory(args)
        parser.error(f"Unsupported command: {args.command}")
    except InventoryParseError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 3
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
