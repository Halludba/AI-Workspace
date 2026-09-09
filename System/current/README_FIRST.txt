Recursive AI Config System v0.18.0

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
Start from active_context.json/context_index.json. DIRECT questions avoid workspace work; scoped mutations use workspace_ctl.py and dependency-relevant context/tests; global changes use full closure. Semantic convergence precedes expensive generation, and unchanged builds/pages are cached.
