# Mutation Trace

**System version:** 0.22.0
**Directive:** Make Custom Prompt the reusable selectable prompt profile, keep Deep Research/plugins separate, and classify completed changes so minor patches avoid broad persistence/regeneration.
**Target improvement:** Correct profile/capability abstraction and add executable impact-aware release closure that minimizes unnecessary directory/artifact work without weakening verification.

## Candidate decisions
- **REWRITE - Part 4 profile architecture:** Deep Research is a capability choice, not a workflow profile; the user selects Custom Prompt to construct the prompt.
- **MERGE - Research prompt architecture:** Fold useful research-question/evidence/output/stopping guidance into extension.prompt_specification_architect instead of maintaining a separate Deep Research agent.
- **NEW - release impact classifier:** A deterministic closure-cost decision is needed after completed parts/mutations to prevent unnecessary broad regeneration.
- **MERGE - Windows + OneDrive persistence:** The local project path is already inside OneDrive, so these are one working tree plus passive sync rather than separate manual persistence targets.

## Accepted changes
- custom_prompt canonical CREATE profile with prompt_creator compatibility alias
- research/Deep Research prompt construction merged into shared prompt specification core
- explicit profile-versus-capability activation boundary
- release_impact_policy and executable classifier/closure plan
- minor-patch minimal derived regeneration with major-patch escalation
- single OneDrive-backed Windows working tree plus one Git commit/push persistence model
- Formats 1.1k.xiii rewrite, Formats 1.1n.vi, Workflow 2.7.14 rewrite and Workflow 2.13.5

## Rejected / merged / no-op
- Removed deep_research_agent_architect profile/module/policy
- Removed automatic RESEARCH_PRECURSOR_WHEN_NEEDED pipeline stage
- No automatic Deep Research/web/plugin activation
- No separate manual Windows and OneDrive write/confirmation passes
- No routine portable ZIP or AI Handoff generation

## Convergence result
- Passes: 2
- Stable: True
