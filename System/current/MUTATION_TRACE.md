# Mutation Trace

**System version:** 0.17.0
**Directive:** Create the general-purpose PDF Styler extension originally intended: arbitrary PDFs should resolve and follow reusable style presets rather than only the self-revising PDFs having styling rules.
**Target improvement:** Add extension.pdf_styler, a reusable style preset schema/registry, style.pdf.formats as the first preset, executable ReportLab adapter/validator, and verification integration.

## Candidate decisions
- **NEW - general reusable PDF Styler extension:** Existing style.formats_pdf is coupled to the recursive pair and does not provide a general style-resolution/application contract.
- **REWRITE/MERGE - reuse Formats visual system as first named preset:** Preserves existing work while separating style tokens from recursive-system semantics.
- **REJECT - hardcode one style into every PDF generator:** Would block explicit style choice and specialized approved generators; preset resolution is more reusable.

## Accepted changes
- Add extension.pdf_styler and pdf_styler_policy.
- Add pdf_style_schema.json and pdf_styles/style.pdf.formats.json.
- Add executable pdf_styler.py loader/validator/ReportLab adapter and specimen renderer.
- Enable PDF Styler in normal generation profiles while preserving specialized-generator overrides.
- Add regression and PDF visual verification coverage.

## Rejected / merged / no-op
- No requirement that every PDF look like Formats.pdf; it is the default named preset, not an immutable universal aesthetic.
- No silent subjective style invention when a material style choice remains unresolved.

## Convergence result
- Passes: 2
- Stable: True
