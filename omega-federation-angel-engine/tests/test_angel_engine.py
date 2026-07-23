from src.angel_engine import AngelEngine, Decision, Reason, Signal


def _engine(dry_run=True):
    engine = AngelEngine(dry_run=dry_run)
    engine.register_action("backup_files", lambda: None)
    return engine


def _valid_signal(**overrides):
    data = dict(
        intent="backup owned files",
        source="dominique",
        target="omega-federation",
        is_owned=True,
        is_reversible=True,
        evidence=["repo path verified"],
    )
    data.update(overrides)
    return Signal(**data)


def test_unknown_action_denies():
    result = _engine().select(_valid_signal(), "unknown")
    assert result.decision == Decision.DENY
    assert result.reason == Reason.UNKNOWN_ACTION


def test_missing_intent_denies():
    result = _engine().select(_valid_signal(intent=""), "backup_files")
    assert result.decision == Decision.DENY
    assert result.reason == Reason.MISSING_INTENT


def test_missing_authority_denies():
    result = _engine().select(_valid_signal(authority=False), "backup_files")
    assert result.decision == Decision.DENY
    assert result.reason == Reason.MISSING_AUTHORITY


def test_missing_evidence_denies():
    result = _engine().select(_valid_signal(evidence=[]), "backup_files")
    assert result.decision == Decision.DENY
    assert result.reason == Reason.MISSING_EVIDENCE


def test_not_owned_without_authorization_denies():
    result = _engine().select(_valid_signal(is_owned=False), "backup_files")
    assert result.decision == Decision.DENY
    assert result.reason == Reason.NOT_OWNED


def test_not_owned_with_authorization_can_dry_run():
    result = _engine().select(
        _valid_signal(is_owned=False, explicit_authorization=True),
        "backup_files",
    )
    assert result.decision == Decision.DRY_RUN_ONLY
    assert result.reason == Reason.DRY_RUN


def test_non_reversible_requires_confirmation():
    result = _engine().select(_valid_signal(is_reversible=False), "backup_files")
    assert result.decision == Decision.REQUIRE_CONFIRMATION
    assert result.reason == Reason.NOT_REVERSIBLE


def test_non_reversible_with_confirmation_can_dry_run():
    result = _engine().select(
        _valid_signal(is_reversible=False, explicit_confirmation=True),
        "backup_files",
    )
    assert result.decision == Decision.DRY_RUN_ONLY
    assert result.reason == Reason.DRY_RUN


def test_mercy_failed_denies():
    result = _engine().select(_valid_signal(mercy=False), "backup_files")
    assert result.decision == Decision.DENY
    assert result.reason == Reason.MERCY_FAILED


def test_valid_signal_in_dry_run_returns_dry_run_only():
    result = _engine(dry_run=True).select(_valid_signal(), "backup_files")
    assert result.decision == Decision.DRY_RUN_ONLY
    assert result.reason == Reason.DRY_RUN


def test_valid_signal_with_dry_run_false_allows():
    result = _engine(dry_run=False).select(_valid_signal(), "backup_files")
    assert result.decision == Decision.ALLOW
    assert result.reason == Reason.ALLOWED


def test_result_serializes_to_json():
    result = _engine().select(_valid_signal(), "backup_files")
    payload = result.to_json()
    assert '"decision": "DRY_RUN_ONLY"' in payload
    assert '"reason": "DRY_RUN"' in payload
