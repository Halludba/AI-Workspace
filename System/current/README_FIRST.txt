Recursive AI Config System v0.24.0

PURPOSE
Persistent self-revising AI behavior/configuration runtime with governed workflow profiles, PDF implementation, Theme Designer, Theme Reference export, strategic planning/checkpoints, and Profile Performance Auditor.

PERSISTENT WORKSPACE
Normal project continuity is the configured workspace: canonical Git repository/source history, synced local execution mirror, and configured visual/binary asset store. Read WORKSPACE.json when available.

PORTABLE EXPORTS
ZIP bundles and the exactly-five-file AI Handoff remain supported for portability/recovery, but are no longer generated for every routine mutation. Run: python pdf_system_engine.py --export-portable

LOCAL USE
Run tests: python pdf_system_engine.py --test
Run convergence: python pdf_system_engine.py --config pdf_system_config.json
Run status: python pdf_system_engine.py --status

THEME DESIGNER
Theme Designer retains target-surface gating, invariant/surface-dependent decisions, granular-by-default approvals, optional reversible batching, and explicit final approval before compilation.

PROFILE PERFORMANCE AUDITOR
The auditor remains advisory: evidence-linked recommendations return to main-host/user governance and never auto-integrate.

PDF STYLER
General PDF creation may use extension.pdf_styler. Default preset: style.pdf.formats. Explicit user/document/specialized-generator styles outrank the default.
Run: python pdf_styler.py --list
Run: python pdf_styler.py --style style.pdf.formats --validate

LATENCY-OPTIMIZED EXECUTION
Start from active_context.json/context_index.json. DIRECT questions avoid workspace work; scoped mutations use workspace_ctl.py and dependency-relevant context/tests; global changes use full closure. Semantic convergence precedes expensive generation, and unchanged builds/pages are cached. Custom Prompt adds a second progressive-activation layer: ordinary CREATE starts FAST with one candidate and only the always-hot prompt core, while workspace/audit/specialized/deeper reasoning wakes only when triggered.

AGENT DEVELOPMENT ECOSYSTEM
Prompt Creator and Prompt Enhancer share one specification-engineering core with CREATE/ENHANCE modes. Reasoning Auditor is advisory-only and audits visible evidence/rationale, not private chain-of-thought. Strategic sequencing lives in project_plan.json.

DECISION RECORDS
Material governed choices may emit append-only per-profile records under decision_records/. They store concise externalizable decision rationale and evidence links, never private chain-of-thought. Validate/write with decision_record.py.

CUSTOM PROMPT PROFILE
Use the selectable custom_prompt profile whenever an optimal prompt is needed. It can create research/Deep Research, coding, analysis, Custom GPT/system and other prompt types. prompt_creator is a compatibility alias only. Profiles define behavior; Deep Research/web/files/connectors and other plugins/tools remain separately enabled by the user/host.

RELEASE IMPACT / MINIMAL PERSISTENCE
After a completed system part or reusable mutation, classify operational blast radius as MINOR_PATCH or MAJOR_PATCH before release materialization. Minor patches update only changed canonical files plus required provenance/state, use scoped checks during iteration, run one full regression before commit, and regenerate derived artifacts only when dependencies changed. Major patches use full closure. The Windows working tree is already OneDrive-synced, so edit it once; OneDrive replicates passively and Git records canonical history with one commit/push.


SYSTEM QUALITY AUDIT
Run on demand: python workspace_ctl.py quality-audit
This prepares bounded evidence for three separate dimensions: reasoning integrity, artifact/code consistency, and profile performance. Reasoning Auditor and Profile Performance Auditor are reused; no redundant mega-auditor profile is created. Automatic cadence is disabled until real evidence justifies a separately governed schedule. All proposals remain PENDING_MAIN_HOST.
