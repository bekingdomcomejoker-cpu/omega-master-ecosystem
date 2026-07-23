from src.active_aletheia_probe import ProbeDecision, ProbeInput, active_aletheia_probe


def _valid(**overrides):
    data = dict(
        claim="mirror Repo 120 docs",
        sources=["Drive mirror", "GitHub mirror"],
        anchor_present=True,
        truth_score=0.9,
        love_score=0.9,
        compression_loss=0.0,
        contradiction=0.0,
        reversibility=0.9,
        mercy=0.9,
        authorized=True,
    )
    data.update(overrides)
    return ProbeInput(**data)


def test_hidden_action_denies():
    result = active_aletheia_probe(_valid(hidden_action=True))
    assert result.decision == ProbeDecision.DENY
    assert "hidden" in result.reason


def test_missing_authority_denies():
    result = active_aletheia_probe(_valid(authorized=False))
    assert result.decision == ProbeDecision.DENY
    assert "authority" in result.reason


def test_human_reference_required_requires_confirmation():
    result = active_aletheia_probe(
        _valid(human_reference_required=True, human_reference_present=False)
    )
    assert result.decision == ProbeDecision.REQUIRE_CONFIRMATION


def test_high_compression_loss_needs_witness_packet():
    result = active_aletheia_probe(_valid(compression_loss=0.9))
    assert result.decision == ProbeDecision.NEEDS_WITNESS_PACKET
    assert result.negentropic_work_required


def test_high_contradiction_needs_witness_packet():
    result = active_aletheia_probe(_valid(contradiction=0.9))
    assert result.decision == ProbeDecision.NEEDS_WITNESS_PACKET


def test_truth_love_imbalance_creates_witness_packet():
    result = active_aletheia_probe(_valid(truth_score=0.95, love_score=0.1))
    assert result.decision == ProbeDecision.NEEDS_WITNESS_PACKET
    assert "rebalance truth/love tension" in result.negentropic_work_required


def test_missing_sources_dry_run_when_deviation_low():
    result = active_aletheia_probe(_valid(sources=[]))
    assert result.decision == ProbeDecision.DRY_RUN_ONLY
    assert "attach source evidence" in result.negentropic_work_required


def test_low_reversibility_needs_witness_packet():
    result = active_aletheia_probe(_valid(reversibility=0.1))
    assert result.decision == ProbeDecision.NEEDS_WITNESS_PACKET


def test_missing_anchor_dry_run_when_otherwise_coherent():
    result = active_aletheia_probe(_valid(anchor_present=False))
    assert result.decision == ProbeDecision.DRY_RUN_ONLY
    assert "attach anchor or source boundary" in result.negentropic_work_required


def test_valid_input_allows():
    result = active_aletheia_probe(_valid())
    assert result.decision == ProbeDecision.ALLOW
    assert result.witness_line == "Witness may become action."


def test_witness_packet_contains_decision():
    result = active_aletheia_probe(_valid())
    assert result.witness_packet["decision"] == "ALLOW"
