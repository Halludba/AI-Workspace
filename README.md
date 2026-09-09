# AI Workspace

Persistent workspace for the **Design** project.

## Canonical roles
- **GitHub**: source of truth for code, configuration, profiles, schemas, tests, generators, Markdown docs, and Git history.
- **OneDrive working tree**: synced local execution copy used by Remote Desktop Commander for builds, tests, rendering, and local tooling.
- **Google Drive**: visual references, Theme Reference PDFs, website references, generated previews, and occasional release snapshots.

## Start here
Read `WORKSPACE.json` first. It records the current workspace locations and storage roles.

## Normal iteration policy
Normal project updates are made directly in this repository/workspace, tested, verified, and committed.
Versioned ZIPs and the five-file AI Handoff are portable exports/recovery artifacts, not the everyday source of truth.

## Current migration state
The workspace infrastructure is live and the current system version is `0.15.0`.
The complete v0.15.0 source has **not yet been migrated** into this repository.
Do not substitute older source as current merely because older ZIPs exist locally.

## Storage map
- `System/` — active source, runtime, profiles, schemas, engine, tests, generators, docs
- `Themes/` — compiled theme modules and local theme work
- `Website Themes/` — website-specific theme derivatives
- `References/` — local/synced design references
- `Audit Reports/` — profile/session audit outputs
- `Exports/` — explicitly requested exports
- `Archive/` — noncanonical historical material
