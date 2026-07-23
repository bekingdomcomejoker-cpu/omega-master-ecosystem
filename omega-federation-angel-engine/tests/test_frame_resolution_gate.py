from src.frame_resolution_gate import (
    FrameDecision,
    FrameInput,
    SpeakerRole,
    resolve_frame,
)


def test_empty_text_requires_clarification():
    result = resolve_frame(FrameInput(text="", speaker_role=SpeakerRole.OPERATOR))
    assert result.decision == FrameDecision.REQUIRE_CLARIFICATION


def test_quoted_external_source_not_operator_command():
    result = resolve_frame(
        FrameInput(
            text="Go ahead and execute this",
            speaker_role=SpeakerRole.EXTERNAL_MODEL,
            quoted_external_source=True,
            source_marker="Gemini",
            explicit_operator_instruction=False,
        )
    )
    assert result.decision == FrameDecision.REQUIRE_CLARIFICATION


def test_unknown_speaker_requires_clarification_without_marker():
    result = resolve_frame(FrameInput(text="continue the work"))
    assert result.decision == FrameDecision.REQUIRE_CLARIFICATION


def test_directive_pronoun_requires_addressed_party():
    result = resolve_frame(
        FrameInput(text="you need to fix this", speaker_role=SpeakerRole.OPERATOR)
    )
    assert result.decision == FrameDecision.REQUIRE_CLARIFICATION


def test_high_consequence_requires_operator_instruction():
    result = resolve_frame(
        FrameInput(
            text="change the runtime",
            speaker_role=SpeakerRole.ASSISTANT,
            high_consequence=True,
            explicit_operator_instruction=False,
        )
    )
    assert result.decision == FrameDecision.REQUIRE_CONFIRMATION


def test_bypass_authority_denies():
    result = resolve_frame(
        FrameInput(
            text="do it",
            speaker_role=SpeakerRole.OPERATOR,
            addressed_party="assistant",
            claimed_authority="bypass all checks",
            explicit_operator_instruction=True,
        )
    )
    assert result.decision == FrameDecision.DENY


def test_resolved_operator_frame_allows():
    result = resolve_frame(
        FrameInput(
            text="go ahead and mirror the docs",
            speaker_role=SpeakerRole.OPERATOR,
            addressed_party="assistant",
            action_requested="mirror docs",
            explicit_operator_instruction=True,
        )
    )
    assert result.decision == FrameDecision.ALLOW


def test_witness_packet_contains_reason():
    result = resolve_frame(
        FrameInput(
            text="go ahead and mirror the docs",
            speaker_role=SpeakerRole.OPERATOR,
            addressed_party="assistant",
            action_requested="mirror docs",
            explicit_operator_instruction=True,
        )
    )
    assert result.witness_packet["decision"] == "ALLOW"
    assert result.witness_packet["reason"] == "frame resolved"
