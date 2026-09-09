# Recursive AI Config System - Changelog

## 0.21.0
- Added optional `deep_research_agent_architect` profile/module/policy as an evidence precursor for new Custom GPT/system-prompt design.
- Enforced `TARGET_AGENT_CONTRACT` vs `RESEARCH_AGENDA` separation so research questions/hypotheses cannot silently become agent requirements.
- Added explicit source-quality, prompt-injection/trust and capability-uncertainty boundaries; the profile never manufactures Deep Research/web/browser/tool capabilities.
- Research is bypassed when stable supplied context already determines the specification; current/specialized/disputed evidence or explicit research-first requests activate it.
- Deep Research output remains noncanonical evidence and is routed through Prompt Enhancer -> Reasoning Auditor -> MAIN_HOST_GATE before deployment.
- Added Formats 1.1k.xiii, Workflow 2.7.14 and regression coverage; 53/53 deterministic tests passed before artifact closure.

## 0.20.0
- Activated privacy-safe, append-only per-profile decision-rationale records after successful bounded Reasoning Auditor validation.
- Added `core.auditable_decision_records`, `decision_record_policy`, `decision_record_schema.json`, `decision_record.py`, and regression coverage.
- Records contain only externalizable objective/constraints/claims/evidence/assumptions/alternatives/decision/unknowns/verification plus stable links; private chain-of-thought and hidden scratchpads are explicitly prohibited.
- Reasoning Auditor may consume records as evidence/data but remains advisory; it cannot auto-edit records, audited outputs or system state.
- Repaired stale `ai_runtime_state.plan_context` so Part 2 is correctly recorded as completed and Part 3 as the active continuation.

## 0.19.0
- Added one shared `extension.prompt_specification_architect` core with separate `prompt_creator` (CREATE) and `prompt_enhancer` (ENHANCE) profiles instead of duplicating overlapping prompt logic.
- Added advisory `reasoning_auditor` / `extension.epistemic_reasoning_audit` for evidence, inference, constraint provenance, metric drift, recursive degradation, alternatives and rationale-to-output consistency.
- Reasoning Auditor never requests/private-chain-of-thought and never auto-fixes or auto-integrates; same-model self-audit is explicitly non-independent.
- Added `agent_development_policy`: create/enhance -> visible rationale when available -> reasoning audit -> main-host gate -> deploy -> observe -> profile-performance audit -> governed improvement.
- Activated `project_plan.json` with the user's staged roadmap; persistent decision-rationale records are deferred until Reasoning Auditor is validated on real recursive prompt work.
- Added Google Drive Agent Prompts reference storage; detected that the uploaded `CUSTOMPROMPT_PROMPTENHANCER.txt` content is actually a longer Prompt Creator variant, so it was not treated as an independent Prompt Enhancer authority.

## 0.18.0
- Added latency-optimized execution routing: DIRECT / SCOPED / GLOBAL before workspace access.
- Added generated minimal context, context index and dependency graph plus `workspace_ctl.py` for compact workspace retrieval and scoped verification.
- Reordered closure to converge semantic state before heavy artifacts; generators are content-addressed and unchanged PDF pages are not re-rendered.
- Added scoped iterative tests with one complete regression before closure, batched-I/O/direct-edit policy, compact execution output and local phase timing/cache-hit instrumentation.
- Token minimization is explicitly not an objective; correctness, safety, approval boundaries and final verification remain unchanged.
- Measured warm-cache closure after implementation: ~2.81-2.84 s internal runtime, with both authoritative PDF generators served from cache and incremental verification completing in ~0.15 s.

## 0.17.0
- Added general-purpose `extension.pdf_styler` so arbitrary PDF generation can resolve and apply reusable named style presets.
- Added `pdf_style_schema.json`, `pdf_styles/style.pdf.formats.json`, and executable `pdf_styler.py` validation/ReportLab adapter + specimen renderer.
- Refactored `style.formats_pdf` into the first named preset binding rather than a special-case styling mechanism.
- PDF style resolution now respects explicit user choice, document/project binding, specialized approved generators, then the configured default.
- Content semantics/readability/layout integrity outrank decorative style fidelity; unavailable fonts/assets require fidelity disclosure rather than fake exactness.
- Added regression coverage and visual specimen verification for the PDF Styler extension.

## 0.16.0
- Promoted persistent GitHub/OneDrive/Google Drive workspace continuity to the normal project delivery model.
- Routine mutations now close through verified workspace state and Git history; versioned ZIP and five-file AI Handoff generation are on-demand portability/recovery exports.
- Added `core.persistent_workspace_continuity` and workspace policy serialization for reasoning hosts.
- Repaired derived AI Handoff generation for OneDrive/Remote Desktop ACLs by overwriting the five known files in place and validating code without creating/deleting `__pycache__`.
- Preserved exact v0.15.0 as a Git tag before this mutation.
- Added persistent-delivery and OneDrive-safe regeneration regression coverage.

## 0.15.0
- Integrated completed Theme Designer performance-audit findings under main-host governance.
- REWRITE: target surface must resolve before surface-dependent theme decisions; invariant theme identity work may continue while unresolved.
- MERGE: after two consecutive unqualified approvals, Theme Studio may offer an explicit opt-in batch of 2-3 adjacent low-conflict layers; batching is never automatic and is reversible to granular mode.
- MERGE/NO-OP: clarified that exploratory references/mockups/draft artifacts are noncanonical until approval/verification.
- Preserved auditor advisory boundary; no automatic audit-driven mutation and no unsupported speedup claim.
- Added regression tests for unresolved-surface gating and opt-in/reversible batching.
- Lineage note: the embedded v0.14.0 predecessor was reconstructed from its five-file AI Handoff; it carries a RECOVERY_NOTICE and is not claimed byte-identical to the original cross-chat archive.

## 0.14.0
- Added advisory `profile_performance_auditor` for evidence-based retrospective review of completed workflow-profile sessions.
- Added report schema/validator and regression tests; proposals remain PENDING_MAIN_HOST and cannot auto-integrate.
- Added Formats rules 1.1k.viii-ix and Workflow stages 2.7.9-2.7.10.
- Reused existing history/governance mechanisms; `strategic_reviewer` remains the broader direction reviewer.
- Recovered release portability by using workspace-relative artifact roots and a release materializer.
- Convergence: 2 passes; stable fixed point.

## 0.13.0
- Timestamp (UTC): 2026-09-08T19:10:02.210823+00:00
- Convergence passes: 2
- Phase timings: convergence_seconds=9.297s, verification_seconds=17.622s
- Prompt cause: Qwen/DeepSeek review conversations proposed a centralized long-range plan, part-based resumption, capacity-aware checkpointing and a complementary secondary-AI advisory role.
- Added `project_plan.json` + schema as persistent macro-direction state; the plan starts empty until the user supplies the real objective/goals.
- Added dependency-aware part decomposition/priority/resume policy; commands such as `part 2`, `next part` or `continue` can resume an unambiguous saved part as a fresh directive.
- Added probabilistic execution-overrun estimation and `ai_runtime_state.execution_checkpoint`; no exact token/time guarantees and no background execution claims.
- Added optional `strategic_reviewer` profile for a second AI that interprets, pressure-tests and suggests while the main execution host retains integration/execution responsibility.
- Added plan/checkpoint/reviewer policy serialization to host packets and the five-file handoff unified state.
- A real outer timeout occurred during the full run; finalization resumed from the completed semantic fixed point instead of rebuilding from zero.
- Regression suite: 19 tests passed. Formats.pdf: 20 pages; PDF_Workflow.pdf: 12 pages; both rendered/preflighted cleanly.

## 0.12.0
- Timestamp (UTC): 2026-09-08T18:47:55.722279+00:00
- Convergence passes: 2
- Phase timings: convergence_seconds=9.620s, verification_seconds=17.137s
- Prompt cause: Requested Theme Designer to automatically create an exact-theme PDF after approval and make that PDF reusable as a reference for later website-theme creation.
- Added required post-approval `REFERENCE_EXPORT`: compile theme module -> generate Theme Reference PDF -> fidelity/preflight verification -> handoff.
- Added `theme_reference_pdf_generator.py`, a self-demonstrating reference artifact generator with visual specimens and a complete token appendix.
- Added fidelity boundary: missing fonts/assets or non-static properties may not be silently substituted while claiming exact fidelity.
- Added `extension.theme_reference_cross_surface` for future website-theme derivation from Theme Reference visual evidence plus exact module tokens.
- Updated Theme Designer adapter packets to include the workflow/reference policies and updated the five-file AI source capsule to include the Theme Reference generator.
- Added runtime-version consistency and Theme Reference regression coverage; final suite passed 15 tests.
- Formats.pdf: 19 pages; PDF_Workflow.pdf: 12 pages; both rendered and preflighted cleanly.

## 0.11.0
- Timestamp (UTC): 2026-09-08T18:21:36.740496+00:00
- Convergence passes: 2
- Phase timings: convergence_seconds=8.839s, verification_seconds=17.658s
- Prompt cause: Requested a workflow profile/agent with its own rules governing how it collaborates with the user specifically to create new themes.
- Target improvement: Add a portable approval-gated Theme Designer workflow profile rather than another core governance layer.
- Added `theme_designer` profile using deep decision breadth, `theme_studio` interaction mode and `creative_exploration` optimization.
- Added `extension.theme_design_collaborator` with reference-first analysis, bounded concept exploration, approved/rejected/locked/open decision tracking and explicit approval before theme commit.
- Added `theme_authoring_policy` phases: DISCOVER -> SYNTHESIZE -> EXPLORE -> REFINE -> VALIDATE -> APPROVE -> COMPILE -> HANDOFF.
- Extended portable module schema with optional structured `parameters` so approved `theme.<slug>` modules can carry machine-readable design tokens.
- Added `ai_runtime_adapter.py --profile theme_designer` so the agent can be loaded without changing the global default profile.
- Added Formats rule 1.1k.v, Workflow stage 2.7.6 and two regression tests for the Theme Designer profile/adapter contract.
- Theme exploration remains reversible draft state; no concrete aesthetic was invented and general predictive-next-step is intentionally excluded from the Theme Designer profile.
- Release-closure inspection caught and repaired a stale immediate-previous-bundle pointer; v0.11.0 now embeds v0.10.0 and the invariant has permanent regression coverage.

## 0.10.0
- Timestamp (UTC): 2026-09-08T18:04:59.984727+00:00
- Convergence passes: 2
- Phase timings: convergence_seconds=9.354s, verification_seconds=15.769s
- Prompt cause: Shared two Qwen roadmap responses plus DeepSeek recommendations about direction, missing mechanisms, customization and extensions.
- Target improvement: Add the highest-value non-subjective resilience mechanism while ranking the rest without feature creep.
- Added deterministic Regression & Mutation Simulation Preflight before expensive generation/rendering.
- Extracted fixed-point/cycle tracking into a directly testable convergence component.
- Added a standard-library unittest suite plus `python pdf_system_engine.py --test`.
- Initial suite passed 7 tests in ~0.14s; an observed `--status` import regression was then converted into an eighth permanent regression test, and final quick preflight passed all 8 tests.
- Full semantic state converged in 2 passes with zero structural issues; both PDFs passed render/preflight.
- Hardened the physical AI Handoff folder so transient Python bytecode is removed and exactly five files remain.
- Deferred templates/data ingestion, semantic-version policy, diff/rollback, checkpoint/resume, MCP, SAT/Z3, RAG and multi-format expansion as separately ranked future candidates.

## 0.9.0
- Timestamp (UTC): 2026-09-08T17:47:26.117495+00:00
- Convergence passes: 2
- Observed run duration: 25.262 s
- Phase timings: convergence_seconds=8.834s, verification_seconds=16.428s
- Prompt cause: Shared Qwen modularization discussion plus DeepSeek handoff/efficiency review.
- Target improvement: Reduce implementation mutation blast radius and attention dilution without fragmenting cohesive code or changing the five-file AI handoff.
- Added selective modularity/blast-radius governance; line count is a soft signal rather than a split trigger.
- Refactored `pdf_system_engine.py` to a 26-line CLI backed by focused `pdf_engine/` modules.
- Deferred PDF-generator splitting because current generators remain cohesive despite being longer.
- Kept cross-model review optional and preserved exactly five AI-handoff files; File 5 now encapsulates the modular sources.
- Deferred incremental dependency-aware build caching as a separate future candidate rather than feature-creeping this release.

## 0.8.0
- Timestamp (UTC): 2026-09-08T17:26:26.349384+00:00
- Convergence passes: 2
- Observed run duration: 26.675 s
- Phase timings: convergence_seconds=9.763s, verification_seconds=16.912s
- Prompt cause: Requested a unique versioned ZIP filename for every iteration and role-based folders inside the ZIP; shared Qwen proposal for a five-file AI-optimized handoff view.
- Target improvement: Make releases collision-proof and easier to navigate while reducing AI upload/context friction without creating a competing source of truth.
- Added semantic-versioned ZIP naming: `Recursive_AI_Config_System_v<version>.zip`.
- Added role-based ZIP folders: Start Here, AI Runtime, PDF System, History & Audit, AI Handoff, Previous Versions.
- Added exactly five derived AI-handoff files to reduce upload/context friction.
- Avoided a manifest self-reference loop by using a direct artifact snapshot in the unified AI state view.
- Expanded the artifact registry to match the actual shipped system.
- Cross-model review remains optional; the runtime stays host-agnostic.

## 0.7.0
- Timestamp (UTC): 2026-09-08T17:12:16.633458+00:00
- Convergence passes: 2
- Observed run duration: 23.808 s
- Phase timings: convergence_seconds=18.015s, verification_seconds=0.0s, materialization_seconds=0.0s
- Prompt cause: Shared Qwen discussion showing that rapid recursive revisions are becoming hard to understand and proposing a direct mapping from prompts to actual system changes.
- Target improvement: Make every system mutation explainable as a causal chain from user intent through candidate admission/audits to accepted changes, affected files and convergence outcome.
- Candidate decisions: NEW:Mutation Provenance & Causal Trace; NO-OP:Portable workflow/profile composition; NO-OP:Reasoning depth; NO-OP:Interaction modes; NO-OP:Optimization profiles; NO-OP/MERGE:Tone.pdf as separate source of truth
- Added end-to-end mutation provenance so each release records the causal path from user directive to inferred target, candidate audit decisions, accepted/rejected changes, affected artifacts and convergence result.
- Added synchronized machine-readable mutation_trace.json and human-readable MUTATION_TRACE.md artifacts.
- Integrated mutation provenance into CHANGELOG.md, version_history.json and recursive convergence reporting.
- Redundancy audit classified Qwen suggestions already implemented in v0.6.0 as NO-OP/MERGE instead of duplicating them.
- Added a privacy boundary: provenance records concise task-relevant summaries/decisions, not private chain-of-thought or unnecessary sensitive conversation content.

## 0.6.0
- Timestamp (UTC): 2026-09-08T16:56:50.519835+00:00
- Convergence passes: 2
- Observed run duration: 29.31 s
- Phase timings: convergence_seconds=16.253s, verification_seconds=12.731s, materialization_seconds=0.117s
- Added host-agnostic decision-depth/check-breadth policy without claiming control of private hidden reasoning.
- Added bounded interaction modes: bounded-autonomous, collaborative and educational-summary.
- Added optimization profiles for speed, balanced, high-assurance and creative-exploration while preserving lexicographic hard constraints.
- Added reusable runtime profile/workflow composition so users can swap module sets and policies without retraining the host model.
- Classified Qwen suggestions against existing rules: personality-as-code was already covered; Tone.pdf merged into existing theme/style module architecture rather than creating a redundant source of truth.
- Recorded the determinism boundary: portable governance improves consistency/auditability but cannot make an LLM host mathematically deterministic.

## 0.5.0
- Timestamp (UTC): 2026-09-08T16:40:26.545342+00:00
- Convergence passes: 2
- Observed run duration: 29.57 s
- Phase timings: convergence_seconds=16.912s, verification_seconds=12.428s, materialization_seconds=0.12s
- Added internal question/checklist optimization.
- Added adaptive convergence effort/value budgeting with base cap 12 and bounded extension.
- Added synchronized version snapshots, changelog and previous-bundle history.
- Added historical change feedback as optimization evidence.
- Primary ZIP now embeds the immediately previous complete ZIP under Previous Versions/.
- Separated convergence-cost history from render/verification cost so adaptive pass budgeting learns from the correct bottleneck.

## 0.4.0
- Convergence passes: 2
- Portable AI runtime, predictive preflight, bounded optional autonomy and bundled handoff were active.
