# Mutation Trace

**System version:** 0.21.0
**Directive:** Continue Part 4 and build the Deep Research / Agent Prompt Architect.
**Target improvement:** Add an optional evidence-research precursor that cleanly separates target-agent requirements from research questions, preserves capability uncertainty, and routes research-generated prompts through existing enhancement/audit/governance gates.

## Candidate decisions
- **NEW - extension.deep_research_agent_architect + profile/policy:** Research-brief architecture is distinct from final prompt specification and was not represented by the existing Prompt Creator/Enhancer.
- **MERGE - Downstream prompt creation/enhancement/audit logic:** Reuse Prompt Enhancer, Reasoning Auditor and main-host deployment gate rather than duplicating their semantics inside the research architect.
- **REWRITE - Agent-development pipeline entry:** Add RESEARCH_PRECURSOR_WHEN_NEEDED as an optional branch before CREATE_OR_ENHANCE while retaining the existing pipeline.
- **NO_OP - Deep Research execution capability:** The profile creates a research brief but does not manufacture web/Deep Research/browser capability; execution remains host-dependent.
- **NEW - Research bypass rule:** Prevent unnecessary research latency/ceremony when stable supplied context already determines the agent specification.

## Accepted changes
- Deep Research / Agent Prompt Architect profile and extension
- Deep Research architect workflow policy
- TARGET_AGENT_CONTRACT vs RESEARCH_AGENDA separation
- Capability-unknown and source-evidence boundaries
- Research-to-Prompt-Enhancer-to-Reasoning-Auditor-to-main-host route
- Latency context topic and regression coverage
- Formats 1.1k.xiii and Workflow 2.7.14

## Rejected / merged / no-op
- No duplicate Prompt Creator/Enhancer implementation
- No automatic research for simple/stable prompt tasks
- No invented Deep Research/web/browser/tool capabilities
- No research-result deployment authority

## Convergence result
- Passes: 2
- Stable: True
