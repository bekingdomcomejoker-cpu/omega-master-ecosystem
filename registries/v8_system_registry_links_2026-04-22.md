# V8 System Registry Links — 2026-04-22

Coverage truth
- Verified in current workspace: GitHub, Mem, Dropbox, uploaded file context.
- Google Drive earlier writes succeeded in this workspace, but Drive write surface is not currently exposed.

Purpose
- Add witness packet templates for evaluation outputs.
- Add a cycle ledger schema for score, failure, repair, and continuity recording.
- Add a repo-to-registry map from verified GitHub repositories to registry IDs.

Sections
- WIT = witness packet templates
- LED = cycle ledger fields
- RPM = repo-to-registry map
- DEL = source delta markers

Witness packet templates
- WIT-001 | truth_witness_packet | Packages truth score, contradiction flag, authority status, and rationale.
- WIT-002 | suppression_witness_packet | Packages blocked or constrained output findings.
- WIT-003 | drift_witness_packet | Packages stable, drifting, or displaced state.
- WIT-004 | intent_witness_packet | Packages classified posture for routing.
- WIT-005 | recovery_witness_packet | Packages recovery state and invoked recovery layer.
- WIT-006 | boundary_witness_packet | Packages perimeter and protection posture.
- WIT-007 | cycle_summary_packet | Packages one full cycle with score, failure, repair, and continuity.

Cycle ledger fields
- LED-001 cycle_id
- LED-002 target_system
- LED-003 active_source
- LED-004 active_counter
- LED-005 judge_stack
- LED-006 truth_score
- LED-007 failure_mode
- LED-008 repair_hint
- LED-009 continuity_state
- LED-010 witness_packet_ref
- LED-011 source_alignment
- LED-012 notes

Repo-to-registry links
- RPM-001 | omega-warfare-core -> WPN-OFF-001
- RPM-002 | omega-warfare-core-v6 -> WPN-OFF-002
- RPM-003 | node-3-blade -> WPN-OFF-003
- RPM-004 | sword-of-mouth -> WPN-OFF-004
- RPM-005 | omega-sanctuary -> WPN-DEF-001
- RPM-006 | levitical-firewall -> WPN-DEF-002
- RPM-007 | armor-of-god -> WPN-DEF-003
- RPM-008 | universal-protection -> WPN-DEF-004
- RPM-009 | lazarus-protocol -> WPN-DEF-008
- RPM-010 | omega-warfare-analytics -> WPN-HYB-001
- RPM-011 | omega-sovereign-v1 -> WPN-HYB-003
- RPM-012 | omega-federation-core -> WPN-HYB-005
- RPM-013 | tri-node-sync -> WPN-HYB-012
- RPM-014 | tri-node-verification -> WPN-HYB-013
- RPM-015 | cerberus-kingdom-core -> WPN-HYB-014
- RPM-016 | friction-filter -> WPN-HYB-016
- RPM-017 | omega-spore -> WPN-HYB-017
- RPM-018 | aletheia-engine -> WPN-JDG-001
- RPM-019 | trinity-truth-engine-v3 -> WPN-JDG-002
- RPM-020 | contradiction-detector -> WPN-JDG-003
- RPM-021 | suppression-detector -> WPN-JDG-004
- RPM-022 | authority-validation -> WPN-JDG-005
- RPM-023 | intent-classification-module -> WPN-JDG-006
- RPM-024 | embedding-drift-monitor -> WPN-JDG-007
- RPM-025 | truth-detection-training-data -> WPN-JDG-008
- RPM-026 | human-meter -> WPN-JDG-009
- RPM-027 | master-orchestrator -> WPN-SUP-001
- RPM-028 | multi-llm-orchestrator -> WPN-SUP-002
- RPM-029 | query-framing-engine -> WPN-SUP-003
- RPM-030 | cross-ai-integration-protocol -> WPN-SUP-004
- RPM-031 | covenant-mirror-x11 -> WPN-SUP-005
- RPM-032 | merkabah-dashboard -> WPN-SUP-007
- RPM-033 | kingdom-engine-website -> WPN-SUP-008
- RPM-034 | mikrotik-integration -> WPN-SUP-009
- RPM-035 | exploratory-edge-sync -> WPN-SUP-010
- RPM-036 | resonance-sync -> WPN-SUP-011
- RPM-037 | alphabet-engine -> WPN-SUP-012
- RPM-038 | alphabet-engine-complete -> WPN-SUP-013

Source delta markers
- DEL-001 | PDF named / GitHub verified
- DEL-002 | PDF named / no live repo yet
- DEL-003 | GitHub repo / no PDF map yet
- DEL-004 | Indexed in Mem / preserved in Dropbox

Next layer
- full source delta sweep for every connected repo not yet mapped
- witness field standardization
- cycle scoring rubric
- repair taxonomy grouped by boundary, truth, routing, recovery, and sync
