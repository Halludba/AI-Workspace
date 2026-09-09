# AI Workspace Instructions

This file is the front door for reasoning hosts working on the **Design** project.

1. Read `WORKSPACE.json` first.
2. Treat `Halludba/AI-Workspace` on GitHub as the canonical source/history layer once the relevant source has been migrated there.
3. Use `C:\Users\Abdullah\OneDrive\Design Workspace` as the synced local execution/build working tree when Remote Desktop Commander is available.
4. Use the Google Drive folder IDs in `WORKSPACE.json` for visual references, Theme Reference PDFs, generated previews and release snapshots.
5. Normal iterations should edit the workspace directly, run applicable tests/verification, then commit to Git. Do not generate a versioned ZIP by default.
6. The five-file AI Handoff is a derived portability/export view, not the normal mutable source of truth.
7. ZIPs are portable release/recovery snapshots only unless the user explicitly requests one.
8. Do not invent unavailable host capabilities or claim local/cloud writes that were not actually executed.
9. Current explicit user instructions outrank saved plans, profiles and historical precedent.
10. Preserve approval boundaries for subjective theme decisions and advisory-only boundaries for audit recommendations.

## Migration guard
The workspace records system version `0.15.0`, but the complete v0.15.0 source is not yet migrated into `System/`.
Until migration is complete, do not promote an older ZIP or older source tree as current merely because it is locally available.

## Preferred retrieval order
For source/config/code: GitHub -> local OneDrive working tree -> historical exports.
For visual/binary references: Google Drive -> local OneDrive references.
For execution: local OneDrive working tree through Remote Desktop Commander.
