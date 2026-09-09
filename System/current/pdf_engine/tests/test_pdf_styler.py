from __future__ import annotations
import json, tempfile, unittest
from pathlib import Path
import jsonschema
import pymupdf

ROOT=Path(__file__).resolve().parents[2]

class PDFStylerTests(unittest.TestCase):
    def test_formats_preset_validates(self):
        style=json.loads((ROOT/"pdf_styles/style.pdf.formats.json").read_text(encoding="utf-8"))
        schema=json.loads((ROOT/"pdf_style_schema.json").read_text(encoding="utf-8"))
        jsonschema.validate(style,schema)
        self.assertEqual(style["id"],"style.pdf.formats")
        self.assertTrue(style["adaptation"]["semantic_content_may_not_be_rewritten_for_style_fit"])

    def test_pdf_styler_policy_and_profile_activation(self):
        cfg=json.loads((ROOT/"ai_runtime_config.json").read_text(encoding="utf-8"))
        policy=cfg["pdf_styler_policy"]
        self.assertEqual(policy["default_style_id"],"style.pdf.formats")
        self.assertIn("semantic correctness",policy["content_priority"][0])
        for name in ["general_balanced","fast_direct","high_assurance","creative_exploration","theme_designer"]:
            self.assertIn("extension.pdf_styler",cfg["profiles"]["definitions"][name]["enabled_modules"])

    def test_resolver_and_fidelity_audit(self):
        import pdf_styler
        style=pdf_styler.resolve_style()
        self.assertEqual(style["id"],"style.pdf.formats")
        audit=pdf_styler.fidelity_audit(style)
        self.assertEqual(audit["status"],"EXACT")
        self.assertEqual(audit["missing_fonts"],[])

    def test_specimen_render_smoke(self):
        import pdf_styler
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/"specimen.pdf"
            pdf_styler.render_specimen(out,pdf_styler.resolve_style())
            self.assertTrue(out.is_file())
            self.assertGreater(out.stat().st_size,1000)
            doc=pymupdf.open(out)
            try:
                self.assertEqual(len(doc),1)
                self.assertIn("PDF Styler Specimen",doc[0].get_text())
            finally:
                doc.close()

if __name__=="__main__": unittest.main()

class PDFStylerPortabilityTests(unittest.TestCase):
    def test_handoff_contains_style_registry_and_styler_source(self):
        from pdf_engine.artifacts import create_ai_handoff
        from pdf_engine.state import resolve_root
        root,state,_=resolve_root(ROOT/"pdf_system_config.json")
        paths=create_ai_handoff(root,state)
        unified=json.loads(next(p for p in paths if p.name=="02_UNIFIED_SYSTEM_STATE.json").read_text(encoding="utf-8"))
        self.assertIn("pdf_style_schema",unified)
        self.assertIn("style.pdf.formats",unified["pdf_styles"])
        capsule=next(p for p in paths if p.name=="05_EXECUTION_ENGINE_AND_LOGIC.py").read_text(encoding="utf-8")
        self.assertIn("pdf_styler.py",capsule)

    def test_adapter_serializes_pdf_styler_policy(self):
        import ai_runtime_adapter
        cfg,state=ai_runtime_adapter.load()
        packet=ai_runtime_adapter.instruction_packet(cfg,state,["reasoning"])
        self.assertIn("PDF_STYLER_POLICY",packet)
        self.assertIn("style.pdf.formats",packet)
