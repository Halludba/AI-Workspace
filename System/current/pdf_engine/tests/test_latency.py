from __future__ import annotations
import json, tempfile, unittest
from pathlib import Path
from reportlab.pdfgen.canvas import Canvas
from pdf_engine.latency import semantic_primary_state, run_generators_incremental, refresh_context_files, compact_topic_context
from pdf_engine.pdf_ops import render_and_preflight
from pdf_engine.state import resolve_root

ROOT=Path(__file__).resolve().parents[2]
CONFIG=ROOT/'pdf_system_config.json'

class LatencyPolicyTests(unittest.TestCase):
    def test_latency_policy_contract(self):
        cfg=json.loads((ROOT/'ai_runtime_config.json').read_text(encoding='utf-8'))
        p=cfg['latency_policy']
        self.assertEqual(p['route_classes'],['DIRECT','SCOPED','GLOBAL'])
        self.assertTrue(p['semantic_before_artifacts'])
        self.assertTrue(p['incremental_generation'])
        self.assertTrue(p['incremental_pdf_rendering'])
        self.assertTrue(p['full_regression_before_closure'])
        self.assertFalse(p['secondary_model_critical_path'])
        for profile in cfg['profiles']['definitions'].values():
            self.assertIn('core.latency_optimized_execution',profile['enabled_modules'])
    def test_context_index_refresh_and_lookup(self):
        root,state,_=resolve_root(CONFIG)
        cfg=json.loads((ROOT/'ai_runtime_config.json').read_text(encoding='utf-8'))
        rt=json.loads((ROOT/'ai_runtime_state.json').read_text(encoding='utf-8'))
        refresh_context_files(root,state,cfg,rt)
        ctx=compact_topic_context(root,'pdf_styler')
        self.assertEqual(ctx['active_context']['system_version'],'0.18.0')
        self.assertIn('pdf_styler.py',ctx['scope']['files'])
        self.assertTrue((ROOT/'dependency_graph.json').is_file())

    def test_semantic_state_excludes_generated_pdfs(self):
        _,state,_=resolve_root(CONFIG)
        sem=semantic_primary_state(ROOT,state)
        self.assertNotIn('Formats.pdf',sem)
        self.assertNotIn('PDF_Workflow.pdf',sem)
        self.assertIn('ai_runtime_config.json',sem)

    def test_incremental_generator_cache(self):
        with tempfile.TemporaryDirectory() as td:
            r=Path(td); (r/'gen.py').write_text("from pathlib import Path\nPath('out.txt').write_text('x')\n",encoding='utf-8')
            state={'artifacts':[{'path':'out.txt','classification':'REQUIRED','generator':'gen.py'}]}
            first=run_generators_incremental(r,state); second=run_generators_incremental(r,state)
            self.assertEqual(first['ran'],['out.txt'])
            self.assertEqual(second['skipped'],['out.txt'])
    def test_pdf_render_cache_skips_unchanged_pages(self):
        with tempfile.TemporaryDirectory() as td:
            r=Path(td)
            for name in ('Formats.pdf','PDF_Workflow.pdf'):
                c=Canvas(str(r/name)); c.drawString(72,720,'stable page'); c.save()
            issues,_=render_and_preflight(r); self.assertEqual(issues,[])
            issues,_=render_and_preflight(r); self.assertEqual(issues,[])
            self.assertIn('Changed pages: none',(r/'Formats_preflight.txt').read_text(encoding='utf-8'))
            self.assertIn('none (unchanged)',(r/'PDF_Workflow_preflight.txt').read_text(encoding='utf-8'))

if __name__=='__main__': unittest.main()
