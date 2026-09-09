# Mutation Trace

**System version:** 0.15.0
**Directive:** User asked the main system to access the completed auditor result from another Design-project chat and continue.
**Target improvement:** Integrate evidence-supported Theme Designer improvements: resolve target surface before surface-dependent design and reduce unnecessary serialized approvals with optional reversible batching.

## Candidate decisions
- **REWRITE - P1 - target-surface gate and invariant/surface-dependent split:** Evidence-backed F6 failure affects sequencing inside the existing Theme Designer policy; strengthen existing target-surface behavior rather than add another module.
- **MERGE - P2 - opt-in adaptive batching after repeated approvals:** Evidence-backed F8 friction belongs inside existing iteration/interaction cadence. Add a bounded opt-in batching policy with granular fallback; do not create a separate agent.
- **MERGE/NO-OP - P3 - draft/noncanonical reference behavior:** Existing draft-state and Theme Reference authority boundaries already cover most of this. Add only an explicit clarification to prevent draft references from becoming canonical.
- **REJECT - automatic auditor-driven profile mutation:** The auditor is advisory by design; this main-host directive authorizes governance review/integration, not automatic self-acceptance of future audits.

## Accepted changes
- Theme Designer now gates surface-dependent design on resolved target_surface while permitting explicitly INVARIANT theme identity work to continue.
- Theme decisions are explicitly classified as INVARIANT or SURFACE_DEPENDENT for sequencing and later cross-surface reuse.
- Theme Studio may offer, but never silently enable, an opt-in batch of 2-3 adjacent low-conflict layers after two consecutive unqualified approvals.
- Any correction/rejection/ambiguity or user request returns batching to granular mode; final theme compilation still requires explicit approval.
- Draft references/mockups are explicitly noncanonical until approval/verification; compiled theme module and verified Theme Reference remain authoritative.
- Added regression coverage for unresolved-surface gating and opt-in reversible batching.

## Rejected / merged / no-op
- No new core governance function or separate batching agent was added.
- No numerical speedup claim is made because the audit did not measure controlled before/after timing.
- No broad Theme Designer rewrite was justified by the audit.
- No automatic future audit integration was enabled.

## Convergence result
- Passes: 2
- Stable: True
