# Mutation Trace

**System version:** 0.16.0
**Directive:** User requested a shared persistent workspace all Design chats can use, with GitHub/PC/cloud editing instead of rebuilding a ZIP for every version.
**Target improvement:** Promote persistent workspace state and Git history to the normal continuity/delivery model; retain ZIP/AI Handoff only for explicit portability/recovery; repair OneDrive-safe handoff regeneration.

## Candidate decisions
- **NEW - Persistent workspace continuity:** The prior system had portable handoff continuity but no canonical cross-chat repository/execution/asset workspace contract.
- **REWRITE - Mandatory ZIP and categorized bundle on every mutation:** Git history and persistent connectors now provide the normal continuity layer; routine ZIP generation adds churn without improving correctness.
- **REWRITE - Delete-and-recreate AI Handoff directory:** Observed OneDrive/Remote Desktop ACL denies directory deletion; in-place deterministic overwrite preserves the five-file contract without destructive regeneration.
- **REJECT - Assume connected tools are always reachable:** Connector/device availability is runtime state and must be verified before claiming access or synchronization.

## Accepted changes
- Added persistent workspace policy and core workspace-continuity module across profiles.
- Routine system closure now targets verified workspace state; ZIP and five-file AI Handoff are explicit portability/recovery exports.
- Added optional portable-export CLI path while preserving versioned categorized ZIP rules when export is requested.
- Changed AI Handoff regeneration to deterministic in-place overwrite with syntax validation that does not create __pycache__.
- Added regression coverage for persistent delivery and OneDrive-safe handoff generation.
- Git tags/commits preserve exact v0.15.0 lineage; previous ZIP embedding is no longer required in persistent mode.

## Rejected / merged / no-op
- No unrelated Theme Designer, auditor or strategic-review behavior was changed.
- No claim is made that workspace connectors bypass context, permission, safety or availability limits.
- Portable ZIP/export capability is retained rather than deleted.

## Convergence result
- Passes: 2
- Stable: True
