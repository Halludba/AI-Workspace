from __future__ import annotations
import json, tempfile, unittest
from pathlib import Path
from pdf_engine.release_impact import classify_change, closure_plan, canonical_changes, MINOR_PATCH, MAJOR_PATCH

ROOT=Path(__file__).resolve().parents[2]

class ReleaseImpactTests(unittest.TestCase):
    def test_bounded_change_is_minor_patch(self):
        with tempfile.TemporaryDirectory() as td:
            result=classify_change(Path(td),['System/current/README_FIRST.txt'])
        self.assertEqual(result['impact'],MINOR_PATCH)
        plan=closure_plan(result)
        self.assertFalse(plan['regenerate_all_derived'])
        self.assertFalse(plan['manifest_refresh'])
        self.assertTrue(plan['full_regression_before_commit'])

    def test_schema_or_core_lifecycle_change_is_major(self):
        with tempfile.TemporaryDirectory() as td:
            result=classify_change(Path(td),['System/current/ai_runtime_schema.json'])
        self.assertEqual(result['impact'],MAJOR_PATCH)
        self.assertTrue(closure_plan(result)['full_convergence'])

    def test_explicit_major_signal_escalates(self):
        with tempfile.TemporaryDirectory() as td:
            result=classify_change(Path(td),['System/current/README_FIRST.txt'],core_lifecycle_change=True)
        self.assertEqual(result['impact'],MAJOR_PATCH)
    def test_derived_paths_do_not_inflate_classifier(self):
        paths=canonical_changes([
            'System/current/Formats.pdf',
            'System/current/_visual_check_v999/page.png',
            'System/current/README_FIRST.txt'
        ])
        self.assertEqual(paths,['System/current/README_FIRST.txt'])

    def test_runtime_policy_matches_single_worktree_model(self):
        cfg=json.loads((ROOT/'ai_runtime_config.json').read_text(encoding='utf-8'))
        p=cfg['release_impact_policy']
        self.assertEqual(p['classes'],['MINOR_PATCH','MAJOR_PATCH'])
        self.assertIn('OneDrive-synced execution mirror',p['workspace_persistence'])
        self.assertIn('Git commit/push',p['workspace_persistence'])
        self.assertIn('skip routine ZIP/AI handoff/manifest/global context/PDF regeneration when unaffected',p['minor_closure'])

if __name__=='__main__': unittest.main()
