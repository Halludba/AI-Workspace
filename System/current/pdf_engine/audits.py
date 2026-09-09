from __future__ import annotations
from pathlib import Path
import jsonschema
from .common import load_json, safe_artifact_path
from .pdf_ops import text_of_pdf


def operational_risk_audit(root: Path, state: dict) -> list[str]:
    issues=[]
    if state.get('round_trip',{}).get('engine_self_modification') is not False:
        issues.append('BLOCK: stable engine self-modification must remain disabled')
    maxp=state.get('convergence',{}).get('max_passes',0)
    if not isinstance(maxp,int) or not (1<=maxp<=24): issues.append('BLOCK: convergence max_passes must be 1..24')
    rel=state.get('release',{})
    if rel.get('bundle_filename') != rel.get('bundle_filename_pattern','').format(version=rel.get('version','')):
        issues.append('BLOCK: release bundle filename does not match versioned filename pattern')
    if rel.get('ai_handoff_file_count') != 5: issues.append('BLOCK: AI handoff file count must equal 5')
    if rel.get('delivery_mode')=='persistent_workspace' and rel.get('bundle_required'):
        issues.append('BLOCK: persistent workspace delivery cannot require a routine bundle')
    for a in state.get('artifacts',[]):
        try: safe_artifact_path(root,a['path'])
        except Exception as e: issues.append(str(e))
        if a.get('generator'):
            gp=safe_artifact_path(root,a['generator'])
            if gp.suffix!='.py': issues.append(f'BLOCK: generator is not Python: {a["generator"]}')
    mod=state.get('modularity',{})
    if mod.get('enabled'):
        for relp in mod.get('engine_modules',[]):
            if not safe_artifact_path(root,relp).exists(): issues.append(f'BLOCK: missing modular engine source: {relp}')
        cli=root/'pdf_system_engine.py'
        if cli.exists() and len(cli.read_text(encoding='utf-8').splitlines())>80:
            issues.append('WARN: pdf_system_engine.py is no longer a thin CLI; modularity boundary may have regressed')
    testing=state.get('testing',{})
    if testing.get('enabled'):
        for relp in testing.get('test_files',[]):
            if not safe_artifact_path(root,relp).exists(): issues.append(f'BLOCK: missing regression test source: {relp}')
    plan=root/'project_plan.json'; plan_schema=root/'project_plan_schema.json'
    if plan.exists() or plan_schema.exists():
        if not plan.exists() or not plan_schema.exists(): issues.append('BLOCK: project plan/schema must materialize together')
        else:
            try: jsonschema.validate(load_json(plan),load_json(plan_schema))
            except Exception as e: issues.append(f'BLOCK: invalid strategic project plan: {e}')
    return issues


def structural_audit(root: Path, state: dict, require_materialized: bool=False, check_pdfs: bool=True) -> list[str]:
    issues=[]
    if require_materialized:
        for a in state['artifacts']:
            if a['classification']=='REQUIRED' and not safe_artifact_path(root,a['path']).exists():
                issues.append(f'missing REQUIRED artifact: {a["path"]}')
    if not check_pdfs:
        return issues
    f=root/'Formats.pdf'; w=root/'PDF_Workflow.pdf'
    if f.exists():
        txt=text_of_pdf(f)
        tokens=['1.1k.viii Profile Performance Audit & Advisory Improvement','1.1k.ix Audit Evidence, Efficiency & Governance','1.1a.iii Mutation Provenance & Causal Trace','1.1k.iv Selective Modularity & Mutation Blast-Radius Control','1.1k.v Theme-Authoring Workflow Profile & Approval-Gated Compilation','1.1k.x Reusable PDF Styler Extension & Preset Resolution','1.1k.xi Prompt-Agent Development & Epistemic Reasoning Audit','1.1k.xii Auditable Decision-Rationale Records & Evidence Linkage','1.1k.xiii Custom Prompt Profile & Capability Separation','1.1k.xiv Periodic Agent Quality Audit & Three-Dimension Separation','1.1n.iv Strategic Plan, Capacity-Aware Segmentation & Checkpoint Continuity','1.1n.v Latency-Aware Execution Routing & Incremental Verification','1.1n.vi Release Impact Classification & Minimal Persistence','1.1o.iv Persistent Workspace Source-of-Truth & Export Demotion','1.1q Build, Render & Verify']
        for token in tokens:
            if token not in txt: issues.append(f'Formats missing required rule: {token}')
    if w.exists():
        txt=text_of_pdf(w)
        tokens=['2.7.9 Audit a Completed Profile Session','2.7.10 Diagnose Friction & Hand Off Proposals','2.7.11 Apply Reusable PDF Styler','2.7.12 Develop, Audit & Govern Prompt Agents','2.7.13 Record Material Agent Decisions','2.7.14 Use Custom Prompt Without Activating Capabilities','2.7.15 Run Periodic Agent Quality Audit','2.6.2 Run Regression & Mutation Simulation Preflight','2.6.3 Route Latency-Critical Execution','2.12.4 Maintain Strategic Plan, Segment & Checkpoint','2.13.4 Commit Persistent Workspace & Synchronize Stores','2.13.5 Classify Release Impact & Persist Minimally','2.15 Build, Render & Verify']
        for token in tokens:
            if token not in txt: issues.append(f'Workflow missing required stage: {token}')
    return issues
