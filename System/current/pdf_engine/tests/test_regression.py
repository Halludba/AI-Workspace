from __future__ import annotations
import json, subprocess, sys, unittest
from pathlib import Path
import jsonschema
from pdf_engine.common import safe_artifact_path
from pdf_engine.state import resolve_root
from pdf_engine.audits import operational_risk_audit
from pdf_engine.convergence import ConvergenceTracker

ROOT=Path(__file__).resolve().parents[2]
CONFIG=ROOT/"pdf_system_config.json"

class RegressionTests(unittest.TestCase):
    def test_current_config_validates(self):
        root,state,schema=resolve_root(CONFIG)
        jsonschema.validate(state,schema)
        self.assertEqual(root,ROOT)

    def test_runtime_state_version_matches_runtime_config(self):
        cfg=json.loads((ROOT/"ai_runtime_config.json").read_text(encoding="utf-8"))
        state=json.loads((ROOT/"ai_runtime_state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["runtime_version"],cfg["runtime_version"])

    def test_operational_risk_preflight_is_clean(self):
        root,state,_=resolve_root(CONFIG)
        self.assertEqual(operational_risk_audit(root,state),[])

    def test_release_filename_is_versioned(self):
        _,state,_=resolve_root(CONFIG)
        rel=state["release"]
        self.assertEqual(rel["bundle_filename"], rel["bundle_filename_pattern"].format(version=rel["version"]))

    def test_persistent_workspace_is_default_delivery(self):
        _,state,_=resolve_root(CONFIG)
        cfg=json.loads((ROOT/"ai_runtime_config.json").read_text(encoding="utf-8"))
        self.assertEqual(state["release"]["delivery_mode"],"persistent_workspace")
        self.assertFalse(state["release"]["bundle_required"])
        self.assertEqual(cfg["workspace_policy"]["mode"],"PERSISTENT_PRIMARY")
        self.assertFalse(cfg["handoff_policy"]["versioned_zip_required"])
        self.assertEqual(cfg["handoff_policy"]["default_delivery"],"workspace_commit")
        module=next(m for m in cfg["modules"] if m["id"]=="core.persistent_workspace_continuity")
        self.assertIn("portable",module["output_policy"].lower())
        for profile in cfg["profiles"]["definitions"].values():
            self.assertIn("core.persistent_workspace_continuity",profile["enabled_modules"])

    def test_ai_handoff_regeneration_is_in_place_and_cache_free(self):
        from pdf_engine.artifacts import create_ai_handoff
        root,state,_=resolve_root(CONFIG)
        d=root/"AI Handoff"; d.mkdir(exist_ok=True)
        marker=d/"01_AI_BRIEFING_AND_HISTORY.md"; marker.write_text("STALE",encoding="utf-8")
        paths=create_ai_handoff(root,state)
        self.assertEqual(len(paths),5)
        self.assertNotEqual(marker.read_text(encoding="utf-8"),"STALE")
        self.assertFalse((d/"__pycache__").exists())

    def test_status_cli_never_crashes(self):
        p=subprocess.run([sys.executable,"pdf_system_engine.py","--status"],cwd=str(ROOT),text=True,capture_output=True)
        self.assertIn(p.returncode,(0,1),msg=p.stderr)
        self.assertNotIn("Traceback",p.stderr)

    def test_immediate_previous_bundle_matches_release_pointer(self):
        root,state,_=resolve_root(CONFIG)
        rel=state["release"]
        if rel.get("delivery_mode")=="persistent_workspace":
            self.assertFalse(rel["bundle_required"])
            self.assertNotIn("previous_bundle_path",rel)
            self.assertEqual([a for a in state["artifacts"] if a.get("role")=="immediate_previous_release"],[])
            return
        expected=rel.get("previous_bundle_path")
        matches=[a for a in state["artifacts"] if a.get("role")=="immediate_previous_release"]
        self.assertEqual(len(matches),1)
        self.assertEqual(matches[0]["path"],expected)
        self.assertTrue((root/expected).is_file())

    def test_ai_handoff_contract_is_exactly_five(self):
        _,state,_=resolve_root(CONFIG)
        self.assertEqual(state["release"]["ai_handoff_file_count"],5)

    def test_artifact_paths_are_workspace_confined(self):
        root,state,_=resolve_root(CONFIG)
        for artifact in state["artifacts"]:
            safe_artifact_path(root,artifact["path"])

    def test_theme_designer_profile_contract(self):
        cfg=json.loads((ROOT/"ai_runtime_config.json").read_text(encoding="utf-8"))
        profile=cfg["profiles"]["definitions"]["theme_designer"]
        self.assertEqual(profile["interaction_mode"],"theme_studio")
        self.assertEqual(profile["optimization_profile"],"creative_exploration")
        self.assertIn("extension.theme_design_collaborator",profile["enabled_modules"])
        self.assertNotIn("extension.predictive_next_step",profile["enabled_modules"])
        policy=cfg["theme_authoring_policy"]
        self.assertTrue(policy["commit_requires_explicit_user_approval"])
        self.assertLessEqual(policy["max_parallel_directions"],3)

    def test_theme_designer_adapter_override(self):
        p=subprocess.run([sys.executable,"ai_runtime_adapter.py","--profile","theme_designer","--output",str(ROOT/"_theme_profile_test.txt")],cwd=str(ROOT),text=True,capture_output=True)
        try:
            self.assertEqual(p.returncode,0,msg=p.stderr)
            text=(ROOT/"_theme_profile_test.txt").read_text(encoding="utf-8")
            self.assertIn("PROFILE: theme_designer",text)
            self.assertIn("extension.theme_design_collaborator",text)
            self.assertIn("REFERENCE_EXPORT",text)
            self.assertIn("theme_reference_pdf_generator.py",text)
        finally:
            (ROOT/"_theme_profile_test.txt").unlink(missing_ok=True)


    def test_theme_designer_surface_gate_and_invariant_split(self):
        cfg=json.loads((ROOT/"ai_runtime_config.json").read_text(encoding="utf-8"))
        policy=cfg["theme_authoring_policy"]["target_surface_policy"]
        self.assertTrue(policy["resolve_before_surface_dependent_design"])
        self.assertIn("INVARIANT",policy["decision_classes"])
        self.assertIn("SURFACE_DEPENDENT",policy["decision_classes"])
        self.assertIn("only INVARIANT",policy["unresolved_rule"])
        module=next(m for m in cfg["modules"] if m["id"]=="extension.theme_design_collaborator")
        self.assertTrue(any("target_surface" in b and "SURFACE_DEPENDENT" in b for b in module["behavior"]))
        state=json.loads((ROOT/"ai_runtime_state.json").read_text(encoding="utf-8"))
        if state["theme_session"].get("target_surface") is None:
            self.assertEqual(state["theme_session"]["target_surface_status"],"UNRESOLVED")

    def test_theme_designer_batching_is_opt_in_and_reversible(self):
        cfg=json.loads((ROOT/"ai_runtime_config.json").read_text(encoding="utf-8"))
        batch=cfg["theme_authoring_policy"]["batching_policy"]
        self.assertEqual(batch["default_mode"],"GRANULAR")
        self.assertEqual(batch["offer_after_consecutive_unqualified_approvals"],2)
        self.assertTrue(batch["enable_requires_explicit_user_opt_in"])
        self.assertLessEqual(batch["max_adjacent_items"],3)
        self.assertIn("return to granular",batch["fallback"].lower())
        self.assertIn("explicit final approval",batch["final_commit_boundary"].lower())
        state=json.loads((ROOT/"ai_runtime_state.json").read_text(encoding="utf-8"))
        self.assertEqual(state["theme_session"]["batching"]["mode"],"GRANULAR")
        self.assertFalse(state["theme_session"]["batching"]["offered"])

    def test_theme_reference_policy_contract(self):
        cfg=json.loads((ROOT/"ai_runtime_config.json").read_text(encoding="utf-8"))
        p=cfg["theme_reference_policy"]
        self.assertTrue(p["required_after_theme_compile"])
        self.assertTrue(p["self_demonstrating"])
        self.assertEqual(p["generator"],"theme_reference_pdf_generator.py")
        self.assertIn("REFERENCE_EXPORT",cfg["theme_authoring_policy"]["session_phases"])
        profile=cfg["profiles"]["definitions"]["theme_designer"]
        self.assertIn("extension.theme_reference_cross_surface",profile["enabled_modules"])

    def test_theme_reference_generator_smoke(self):
        import tempfile
        fixture={
          "id":"theme.regression_fixture","type":"theme","enabled":True,
          "parameters":{
            "palette":{"background":"#101114","surface":"#191B20","text_primary":"#F1F3F5","accent":"#8D7CFF"},
            "typography":{},"spacing":{"base":6},"geometry":{"radius":8},"surfaces":{"panel":"#191B20"}
          }
        }
        with tempfile.TemporaryDirectory() as td:
            td=Path(td); src=td/"theme.json"; out=td/"reference.pdf"
            src.write_text(json.dumps(fixture),encoding="utf-8")
            p=subprocess.run([sys.executable,"theme_reference_pdf_generator.py","--theme-json",str(src),"--output",str(out)],cwd=str(ROOT),text=True,capture_output=True)
            self.assertEqual(p.returncode,0,msg=p.stderr)
            self.assertTrue(out.is_file()); self.assertGreater(out.stat().st_size,1000)
            self.assertTrue((td/"theme.regression_fixture.json").is_file())

    def test_ai_handoff_code_capsule_includes_theme_reference_generator(self):
        from pdf_engine.artifacts import create_ai_handoff
        root,state,_=resolve_root(CONFIG)
        paths=create_ai_handoff(root,state)
        code=[p for p in paths if p.name=="05_EXECUTION_ENGINE_AND_LOGIC.py"][0].read_text(encoding="utf-8")
        self.assertIn("theme_reference_pdf_generator.py",code)

    def test_project_plan_validates_and_state_is_coherent(self):
        cfg=json.loads((ROOT/"ai_runtime_config.json").read_text(encoding="utf-8"))
        plan=json.loads((ROOT/cfg["planning_policy"]["plan_path"]).read_text(encoding="utf-8"))
        schema=json.loads((ROOT/cfg["planning_policy"]["schema_path"]).read_text(encoding="utf-8"))
        jsonschema.validate(plan,schema)
        if plan["status"]=="AWAITING_DIRECTION":
            self.assertIsNone(plan["master_objective"]); self.assertEqual(plan["parts"],[])
        else:
            self.assertIn(plan["status"],["ACTIVE","COMPLETED"]); self.assertTrue(plan["master_objective"]); self.assertTrue(plan["parts"])
            ids={p["id"] for p in plan["parts"]}
            if plan["current_part_id"] is not None: self.assertIn(plan["current_part_id"],ids)
            if plan["last_completed_part_id"] is not None: self.assertIn(plan["last_completed_part_id"],ids)
            if plan["next_recommended_part_id"] is not None: self.assertIn(plan["next_recommended_part_id"],ids)
            if plan["status"]=="COMPLETED":
                self.assertIsNone(plan["current_part_id"]); self.assertIsNone(plan["next_recommended_part_id"])

    def test_checkpoint_capacity_policy_contract(self):
        cfg=json.loads((ROOT/"ai_runtime_config.json").read_text(encoding="utf-8"))
        state=json.loads((ROOT/"ai_runtime_state.json").read_text(encoding="utf-8"))
        p=cfg["execution_capacity_policy"]
        self.assertTrue(p["estimate_before_heavy_execution"])
        self.assertIn("probabilistic",p["estimation_boundary"].lower())
        self.assertEqual(p["checkpoint_location"],"ai_runtime_state.json.execution_checkpoint")
        self.assertIn("current explicit user instruction",p["resume_resolution_order"][0])
        self.assertIn("execution_checkpoint",state)

    def test_strategic_reviewer_profile_and_adapter(self):
        cfg=json.loads((ROOT/"ai_runtime_config.json").read_text(encoding="utf-8"))
        profile=cfg["profiles"]["definitions"]["strategic_reviewer"]
        self.assertEqual(profile["interaction_mode"],"strategic_advisory")
        self.assertIn("extension.strategic_second_mind",profile["enabled_modules"])
        self.assertNotIn("extension.predictive_next_step",profile["enabled_modules"])
        p=subprocess.run([sys.executable,"ai_runtime_adapter.py","--profile","strategic_reviewer","--output",str(ROOT/"_strategic_reviewer_test.txt")],cwd=str(ROOT),text=True,capture_output=True)
        try:
            self.assertEqual(p.returncode,0,msg=p.stderr)
            text=(ROOT/"_strategic_reviewer_test.txt").read_text(encoding="utf-8")
            self.assertIn("PROFILE: strategic_reviewer",text)
            self.assertIn("PROJECT PLAN SNAPSHOT",text)
            self.assertIn("SECONDARY_REVIEW_POLICY",text)
        finally:
            (ROOT/"_strategic_reviewer_test.txt").unlink(missing_ok=True)

    def test_ai_handoff_unified_state_contains_project_plan(self):
        from pdf_engine.artifacts import create_ai_handoff
        root,state,_=resolve_root(CONFIG)
        paths=create_ai_handoff(root,state)
        unified=json.loads([p for p in paths if p.name=="02_UNIFIED_SYSTEM_STATE.json"][0].read_text(encoding="utf-8"))
        self.assertIn("project_plan",unified)
        self.assertIn("project_plan_schema",unified)
        self.assertEqual(unified["project_plan"]["plan_version"],"1.0")

    def test_fixed_point_detection(self):
        t=ConvergenceTracker()
        self.assertFalse(t.observe({"x":1})["stable"])
        r=t.observe({"x":1})
        self.assertTrue(r["stable"]); self.assertFalse(r["cycle"])

    def test_cycle_detection(self):
        t=ConvergenceTracker()
        t.observe({"x":1}); t.observe({"x":2}); r=t.observe({"x":1})
        self.assertTrue(r["cycle"]); self.assertIn("BLOCK: convergence cycle detected",r["issues"])

if __name__=="__main__": unittest.main()
