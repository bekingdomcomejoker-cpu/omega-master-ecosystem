"""Tests for the Phase 1 Glass-Chess Canary CLI."""

import json

from src.glass_chess_canary import (
    audit_inventory,
    lexical_outliers,
    normalize_name,
    parse_inventory_text,
)


def records(*names: str):
    return [normalize_name(name) for name in names]


def test_exact_match_passes() -> None:
    expected = records("owner/omega-core", "owner/glass-chess")
    actual = records("owner/glass-chess", "owner/omega-core")

    report = audit_inventory(
        expected,
        actual,
        expected_source="expected",
        actual_source="actual",
        declared_expected_count=2,
        pagination_complete="true",
        scope_declared=True,
    )

    assert report.status == "PASS"
    assert report.canon_eligible is True
    assert report.missing == ()
    assert report.unexpected == ()
    assert report.canaries[0].present is True
    assert report.expected_sha256 == report.actual_sha256


def test_missing_glass_chess_fails_closed_and_records_unknown() -> None:
    expected = records("owner/omega-core", "owner/glass-chess")
    actual = records("owner/omega-core")

    report = audit_inventory(
        expected,
        actual,
        expected_source="expected",
        actual_source="actual",
        declared_expected_count=2,
        pagination_complete="true",
        scope_declared=True,
    )

    assert report.status == "FAIL_CLOSED"
    assert report.canon_eligible is False
    assert report.missing == ("owner/glass-chess",)
    assert report.canaries[0].present is False
    assert report.unknown_ledger[0].expected_object == "owner/glass-chess"


def test_duplicates_fail_even_when_unique_set_matches() -> None:
    expected = records("owner/glass-chess")
    actual = records("owner/glass-chess", "OWNER/GLASS-CHESS")

    report = audit_inventory(
        expected,
        actual,
        expected_source="expected",
        actual_source="actual",
        declared_expected_count=1,
        pagination_complete="true",
        scope_declared=True,
    )

    assert report.status == "FAIL_CLOSED"
    assert len(report.duplicates) == 1
    assert report.duplicates[0].key == "owner/glass-chess"


def test_unknown_pagination_is_partial_view() -> None:
    expected = records("owner/glass-chess")
    actual = records("owner/glass-chess")

    report = audit_inventory(
        expected,
        actual,
        expected_source="expected",
        actual_source="actual",
        declared_expected_count=1,
        pagination_complete="unknown",
        scope_declared=True,
    )

    assert report.status == "PARTIAL_VIEW"
    assert report.canon_eligible is False


def test_missing_scope_is_partial_view() -> None:
    expected = records("owner/glass-chess")
    actual = records("owner/glass-chess")

    report = audit_inventory(
        expected,
        actual,
        expected_source="expected",
        actual_source="actual",
        declared_expected_count=1,
        pagination_complete="true",
        scope_declared=False,
    )

    assert report.status == "PARTIAL_VIEW"


def test_gh_json_and_numbered_text_parsing_match() -> None:
    json_text = json.dumps(
        [
            {"nameWithOwner": "owner/omega-core"},
            {"nameWithOwner": "owner/glass-chess"},
        ]
    )
    numbered_text = "1. owner/omega-core\n17. owner/glass-chess\n"

    parsed_json = parse_inventory_text(json_text)
    parsed_text = parse_inventory_text(numbered_text)

    assert [record.key for record in parsed_json] == [
        record.key for record in parsed_text
    ]


def test_github_url_normalization() -> None:
    record = normalize_name("https://github.com/Owner/Glass-Chess.git")

    assert record.display_name == "Owner/Glass-Chess"
    assert record.key == "owner/glass-chess"


def test_two_way_comparison_detects_unexpected_member() -> None:
    expected = records("owner/glass-chess")
    actual = records("owner/glass-chess", "owner/unexpected")

    report = audit_inventory(
        expected,
        actual,
        expected_source="expected",
        actual_source="actual",
        declared_expected_count=1,
        pagination_complete="true",
        scope_declared=True,
    )

    assert report.status == "FAIL_CLOSED"
    assert report.unexpected == ("owner/unexpected",)


def test_outlier_heuristic_returns_requested_limit() -> None:
    actual = records(
        "owner/omega-core",
        "owner/omega-router",
        "owner/omega-engine",
        "owner/glass-chess",
    )

    outliers = lexical_outliers(actual, limit=2)

    assert len(outliers) == 2
    assert all(0.0 <= item.score <= 1.0 for item in outliers)
