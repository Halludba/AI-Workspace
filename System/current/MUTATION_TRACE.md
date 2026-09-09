# Mutation Trace

**System version:** 0.18.0
**Directive:** Implement the planned settings to significantly reduce prompt/output production time; token usage is not an issue.
**Target improvement:** Minimize wall-clock latency while preserving correctness and final verification quality.

## Candidate decisions
- **MERGE - latency router + lazy context:** Reduces unnecessary context/tool work without weakening authority or final verification.
- **REWRITE - regression sequencing:** Use scoped tests during iteration and one full suite before closure instead of repeatedly running all tests.
- **NEW - content-addressed build/render cache:** Skip only work whose inputs or rendered page hashes are unchanged.

## Accepted changes
- DIRECT/SCOPED/GLOBAL pre-workspace routing
- Tiered lazy context with active_context/context_index/dependency_graph
- workspace_ctl compact control interface
- semantic convergence before heavy artifact generation
- content-addressed generator cache
- incremental PDF page render cache
- scoped iterative test support plus full final regression
- batch independent I/O policy
- local deterministic edit/diff mechanics
- compact execution responses and suppressed nonessential progress narration
- secondary AI excluded from latency-critical path
- local phase timing/cache-hit instrumentation

## Rejected / merged / no-op
- No token-minimization objective
- No reduction of final correctness/safety/approval checks
- No mandatory secondary-model call
- No claim of guaranteed host prompt-cache speedup

## Convergence result
- Passes: 2
- Stable: True
