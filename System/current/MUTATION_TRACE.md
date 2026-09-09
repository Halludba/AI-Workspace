# Mutation Trace

**System version:** 0.23.0
**Directive:** Run Part 5: operationalize periodic agent quality audits.
**Target improvement:** Add a bounded on-demand system health audit that keeps reasoning integrity, artifact/code consistency and profile performance separate, reuses existing specialist auditors and preserves main-host authority.

## Candidate decisions
- **MERGE - Existing reasoning_auditor + profile_performance_auditor:** Reuse specialist semantic audit responsibilities instead of creating a redundant mega-auditor profile.
- **NEW - quality_audit.py deterministic evidence/consistency layer:** Artifact/code/link/hash consistency requires deterministic local checks not covered by the existing semantic auditors.
- **NEW - quality_audit_report_schema.json aggregate advisory report contract:** A system audit needs one evidence-linked container while preserving three independent dimensions.
- **DEFER - Automatic audit cadence:** Only three material decision records and no completed profile-session audit evidence exist; a schedule would be invented rather than evidence-based.

## Accepted changes
- On-demand periodic_quality_audit_policy
- quality_audit.py evidence packet and deterministic consistency checks
- quality_audit_report_schema.json
- workspace_ctl.py quality-audit command
- Three-dimension reasoning/artifact/profile separation
- Manual cadence until evidence supports change
- Formats 1.1k.xiv and Workflow 2.7.15
- First live Part 5 audit report

## Rejected / merged / no-op
- No system_quality_auditor mega profile
- No automatic audit schedule
- No aggregate correctness score
- No private chain-of-thought capture
- No automatic integration of audit proposals

## Convergence result
- Passes: 2
- Stable: True
