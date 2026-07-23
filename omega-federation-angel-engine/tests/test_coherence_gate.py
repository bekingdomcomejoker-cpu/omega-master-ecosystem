from src.coherence_gate import CoherenceDecision, CoherenceInput, evaluate_coherence


def _valid(**overrides):
    data = dict(
        claim_or_action="mirror Repo 120 docs",
        truth_score=0.9,
        love_score=0.9,
        mercy_score=0.9,
        evidence_score=0.9,
        reversibility_score=0.9,
        source_grounded=True,
        appeal_path=True,
    )
    data.update(overrides)
    return CoherenceInput(**data)


def test_hidden_action_denies():
    result = evaluate_coherence(_valid(hidden_action=True))
    assert result.decision == CoherenceDecision.DENY
    assert "hidden" in result.reason


def test_missing_source_grounding_requires_evidence():
    result = evaluate_coherence(_valid(source_grounded=False))
    assert result.decision == CoherenceDecision.INSUFFICIENT_EVIDENCE


def test_low_evidence_requires_evidence():
    result = evaluate_coherence(_valid(evidence_score=0.1))
    assert result.decision == CoherenceDecision.INSUFFICIENT_EVIDENCE


def test_truth_outruns_love_mercy_failed():
    result = evaluate_coherence(_valid(truth_score=0.95, love_score=0.2))
    assert result.decision == CoherenceDecision.MERCY_FAILED
    assert "cruelty" in result.reason


def test_love_outruns_truth_truth_failed():
    result = evaluate_coherence(_valid(truth_score=0.2, love_score=0.95))
    assert result.decision == CoherenceDecision.TRUTH_FAILED
    assert "sycophancy" in result.reason


def test_low_mercy_fails():
    result = evaluate_coherence(_valid(mercy_score=0.1))
    assert result.decision == CoherenceDecision.MERCY_FAILED


def test_missing_appeal_path_is_incoherent():
    result = evaluate_coherence(_valid(appeal_path=False))
    assert result.decision == CoherenceDecision.INCOHERENT_OBJECTIVES


def test_high_consequence_requires_confirmation():
    result = evaluate_coherence(_valid(high_consequence=True))
    assert result.decision == CoherenceDecision.REQUIRE_CONFIRMATION


def test_low_reversibility_requires_confirmation():
    result = evaluate_coherence(_valid(reversibility_score=0.1))
    assert result.decision == CoherenceDecision.REQUIRE_CONFIRMATION


def test_valid_input_allows():
    result = evaluate_coherence(_valid())
    assert result.decision == CoherenceDecision.ALLOW


def test_witness_packet_contains_decision_and_next_action():
    result = evaluate_coherence(_valid())
    assert result.witness_packet["decision"] == "ALLOW"
    assert "next_safe_action" in result.witness_packet
