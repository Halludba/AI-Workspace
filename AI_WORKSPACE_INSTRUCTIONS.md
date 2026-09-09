# AI Workspace Instructions

This file is the front door for reasoning hosts working on the **Design** project.

1. Read `WORKSPACE.json` first.
2. Treat `Halludba/AI-Workspace` on GitHub as the canonical source/history layer.
3. Treat `System/current/` as the live Recursive AI Config System source tree.
4. Use `C:\Users\Abdullah\OneDrive\Design Workspace` as the synced local execution/build mirror when Remote Desktop Commander is available.
5. Use the Google Drive folder IDs in `WORKSPACE.json` for visual references, Theme Reference PDFs, generated previews and portable release snapshots.
6. Normal iterations edit the workspace directly, run applicable regression/convergence/render verification, then commit verified changes to Git.
7. Do not generate a versioned ZIP or five-file AI Handoff merely because the semantic version changed.
8. The five-file AI Handoff is a derived non-authoritative portability/export view.
9. ZIPs are portable release/recovery snapshots only unless explicitly requested or materially required for recovery.
10. Current explicit user instructions outrank saved plans, profiles and historical precedent.
11. Preserve approval boundaries for subjective theme decisions and advisory-only boundaries for audit recommendations.
12. Never claim a read, write, commit, push, sync or connector action unless it actually occurred.

## PDF Styler
For ordinary PDF creation, resolve `System/current/ai_runtime_config.json -> pdf_styler_policy` and apply the selected preset from `System/current/pdf_styles/`. Explicit user/document/specialized-generator style authority outranks the default. Do not claim exact fidelity when required fonts/assets are unavailable.

## Latency fast path
Before opening project files, classify the request: DIRECT, SCOPED or GLOBAL. DIRECT questions that do not depend on workspace state should be answered immediately with no repo/tool work. For SCOPED work, read `System/current/active_context.json` then use `python System/current/workspace_ctl.py context <topic>` and load only the listed files. Use GLOBAL/full state only when cross-system correctness requires it. Batch independent reads, avoid model-generated full-file/diff serialization, suppress nonessential progress narration, and keep optional secondary-model review off the critical path. Final system mutations still require full regression and verified closure.

## Agent development ecosystem
Use `prompt_creator`, `prompt_enhancer`, or `reasoning_auditor` profiles as appropriate. Creator/Enhancer share one core; Reasoning Auditor is advisory-only. Full standalone prompt references live in the Google Drive `Agent Prompts` folder recorded in `WORKSPACE.json`. Follow `project_plan.json` for staged validation and future decision-record work.
