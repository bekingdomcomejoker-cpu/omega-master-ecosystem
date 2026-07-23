from src.throne_check import ThroneDecision, ThroneInput, throne_check


def _valid(**overrides):
    data = dict(
        movement="sync canon marker into workspace",
        stated_center="God Truth Love Presence",
        source_grounded=True,
        operator_ready=True,
        wheel_observers=["drive", "github", "mem"],
        love_score=1.0,
        mercy_score=1.0,
        hechalot_context="drive-sync-context",
        merkavah_execution_state="preflight",
    )
    data.update(overrides)
    return ThroneInput(**data)


def test_valid_throne_check_allows():
    result = throne_check(_valid())
    assert result.decision == ThroneDecision.ALLOW
    assert "No throne" in result.core_line


def test_corrupt_center_denies():
    result = throne_check(_valid(stated_center="profit control spectacle"))
    assert result.decision == ThroneDecision.DENY
    assert "corrupt center" in result.reason


def test_missing_aligned_center_requires_confirmation():
    result = throne_check(_valid(stated_center=""))
    assert result.decision == ThroneDecision.REQUIRE_CONFIRMATION


def test_unready_operator_requires_confirmation():
    result = throne_check(_valid(operator_ready=False))
    assert result.decision == ThroneDecision.REQUIRE_CONFIRMATION


def test_low_love_fails_constant():
    result = throne_check(_valid(love_score=0.1))
    assert result.decision == ThroneDecision.LOVE_MERCY_FAILED
    assert "love/mercy" in result.reason


def test_low_mercy_fails_constant():
    result = throne_check(_valid(mercy_score=0.1))
    assert result.decision == ThroneDecision.LOVE_MERCY_FAILED
    assert "cold machine" in result.reason


def test_merkavah_hechalot_conflation_is_incoherent():
    result = throne_check(
        _valid(
            hechalot_context="ascent",
            merkavah_execution_state="ascent",
        )
    )
    assert result.decision == ThroneDecision.INCOHERENT_OBJECTIVES
    assert "Hechalot" in result.reason


def test_witness_packet_tracks_merkavah_and_hechalot_separately():
    result = throne_check(_valid())
    assert result.witness_packet["merkavah_execution_state"] == "preflight"
    assert result.witness_packet["hechalot_context"] == "drive-sync-context"


def test_missing_wheel_observers_needs_witness_packet():
    result = throne_check(_valid(wheel_observers=[]))
    assert result.decision == ThroneDecision.NEEDS_WITNESS_PACKET


def test_wrong_relation_is_incoherent():
    result = throne_check(_valid(right_relation=False))
    assert result.decision == ThroneDecision.INCOHERENT_OBJECTIVES


def test_executable_without_doctrine_is_dry_run_only():
    result = throne_check(_valid(executable_requested=True, doctrine_before_code=False))
    assert result.decision == ThroneDecision.DRY_RUN_ONLY


def test_claiming_received_pattern_as_private_invention_fails_boundary():
    result = throne_check(_valid(claims_private_invention=True))
    assert result.decision == ThroneDecision.SOURCE_BOUNDARY_FAILED
