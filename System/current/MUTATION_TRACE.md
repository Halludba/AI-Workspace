# Mutation Trace

**System version:** 0.24.0
**Directive:** Optimize prompt generation for materially lower latency by cutting nonessential work while preserving core prompt quality.
**Target improvement:** Add a progressive prompt fast path that starts with minimal context/one candidate and lazily activates workspace, audit, research, enhancement and deep reasoning only when justified.

## Candidate decisions
- **NEW - prompt_execution_policy progressive activation:** Existing lazy loading stops at topic scope; prompt packets need a second module/policy activation layer.
- **REWRITE - custom_prompt default execution breadth:** Ordinary CREATE work does not justify deep/5-candidate reasoning; default FAST uses direct/speed with one candidate and escalation gates.
- **REWRITE - ai_runtime_adapter packet serialization:** Unconditional global policies and the full project plan dominated prompt packet context despite being unrelated to ordinary prompt creation.
- **MERGE - workspace continuity and decision-record features:** Retain both capabilities but make them lazy rather than deleting governance features globally.
- **KEEP - extension.prompt_specification_architect semantic contract and safety/capability boundaries:** These rules carry prompt quality; speed should come from less surrounding work, not weaker semantic requirements.
- **FIX - unknown profile resolution:** The touched adapter path could otherwise fail open to broad module activation; fail closed instead.
- **DEFER - 2-3x wall-clock speed claim:** Packet/context reduction can be measured immediately, but model wall-clock speed must be observed before asserting it.

## Accepted changes
- Prompt FAST/STANDARD/DEEP execution lanes with explicit escalation signals
- Custom Prompt defaults to FAST / direct / speed / one-candidate prompt-only output
- Prompt Enhancer defaults to STANDARD rather than DEEP
- Always-hot four-module prompt core with lazy workspace continuity and decision records
- Selective adapter policy serialization and project-plan omission unless actually required
- Repeatable adapter --feature flags for progressive activation/escalation
- Fail-closed unknown profile handling
- Prompt packet size regression ceiling and activation/escalation tests
- Material v0.24 prompt fast-path decision record with measured packet-size evidence and explicit wall-clock unknown

## Rejected / merged / no-op
- No removal of the shared semantic prompt architect
- No weakening of safety, privacy, capability or hard-constraint invariants
- No unconditional research/ENHANCE/security rule expansion
- No unsupported wall-clock speedup claim

## Convergence result
- Passes: 2
- Stable: True
