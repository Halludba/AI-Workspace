from __future__ import annotations
import json, sys, time
from pathlib import Path
import jsonschema
from .common import write_json
from .state import resolve_root, export_generated_python, import_generated_python, primary_state
from .audits import operational_risk_audit, structural_audit
from .pdf_ops import render_and_preflight
from .artifacts import create_report, create_ai_handoff, finalize_runtime_state, update_trace_after_run, create_manifest, create_bundle
from .convergence import ConvergenceTracker
from .testing import run_regression_suite
from .latency import semantic_primary_state, run_generators_incremental, record_latency, refresh_context_files
from .release_impact import classify_change, closure_plan, MINOR_PATCH, MAJOR_PATCH


def _runtime(root: Path):
    cfg=json.loads((root/'ai_runtime_config.json').read_text(encoding='utf-8'))
    state=json.loads((root/'ai_runtime_state.json').read_text(encoding='utf-8'))
    return cfg,state


def _selected_impact(root: Path, rt_state: dict) -> tuple[dict,dict]:
    saved=rt_state.get('release_impact') or {}
    if saved.get('status')=='CLASSIFIED' and saved.get('directive_id')==rt_state.get('directive_id'):
        assessment=saved.get('assessment') or {}
        if assessment.get('impact') in (MINOR_PATCH,MAJOR_PATCH):
            return assessment,closure_plan(assessment)
    assessment=classify_change(root.parent.parent)
    return assessment,closure_plan(assessment)
def _changed(assessment: dict, rel: str) -> bool:
    target='System/current/'+rel.replace('\\','/')
    return target in set(assessment.get('canonical_changed_paths',[]))


def sync(config_path: Path, import_python_first: bool=False) -> int:
    total_start=time.time(); metrics={}
    root,state,schema=resolve_root(config_path)
    rt_cfg,rt_state=_runtime(root)
    assessment,plan=_selected_impact(root,rt_state)
    metrics['release_impact']=assessment['impact']
    metrics['impact_reasons']=assessment.get('reasons',[])
    risk=operational_risk_audit(root,state)
    if risk:
        print('\n'.join(risk),file=sys.stderr); return 2
    generated_state_needed=(assessment['impact']==MAJOR_PATCH or _changed(assessment,'pdf_system_config.json'))
    if import_python_first:
        state=import_generated_python(root); jsonschema.validate(state,schema); write_json(config_path,state)
        generated_state_needed=True
    if generated_state_needed:
        export_generated_python(root,state)
    refresh_context_files(root,state,rt_cfg,rt_state)

    t=time.time(); passes=[]; stable=False
    tracker=ConvergenceTracker(state['convergence'].get('detect_cycles',True))
    for n in range(1,state['convergence']['max_passes']+1):
        if generated_state_needed:
            export_generated_python(root,state)
        issues=structural_audit(root,state,False,check_pdfs=False)
        obs=tracker.observe(semantic_primary_state(root,state),issues)
        passes.append({'pass':n,'changed':obs['changed'],'issues':list(obs['issues'])})
        if obs['cycle']: break
        if obs['stable']: stable=True; break
    metrics['semantic_convergence_seconds']=round(time.time()-t,4)
    if not stable:
        create_report(root,state,passes,['semantic convergence did not reach stable fixed point'],metrics['semantic_convergence_seconds'],0)
        return 3

    t=time.time(); build=run_generators_incremental(root,state)
    metrics['generation_seconds']=round(time.time()-t,4)
    metrics['generated']=build['ran']; metrics['generator_cache_hits']=build['skipped']
    test_cfg=state.get('testing',{})
    if test_cfg.get('enabled',False) and test_cfg.get('preflight_required',False):
        t=time.time(); ok,output=run_regression_suite(root,test_cfg.get('report','regression_test_report.txt'))
        metrics['regression_seconds']=round(time.time()-t,4)
        if not ok:
            print(output,file=sys.stderr); record_latency(root,metrics); return 6

    final=structural_audit(root,state,False,check_pdfs=True)
    pdf_inputs_changed=bool(build['ran']) or any(_changed(assessment,x) for x in ('build_formats_pdf_v18.py','create_pdf_workflow_v13.py','Formats.pdf','PDF_Workflow.pdf'))
    if assessment['impact']==MAJOR_PATCH or pdf_inputs_changed:
        verify,verify_seconds=render_and_preflight(root); final+=verify
    else:
        verify_seconds=0.0
    metrics['verification_seconds']=round(verify_seconds,4)
    if final:
        create_report(root,state,passes,final,metrics['semantic_convergence_seconds'],verify_seconds)
        record_latency(root,metrics); return 4
    create_report(root,state,passes,[],metrics['semantic_convergence_seconds'],verify_seconds)
    finalize_runtime_state(root,state)
    update_trace_after_run(root,state,passes,[])
    rt_cfg,rt_state=_runtime(root)
    rt_state['release_impact']={
        'status':'CLOSED','directive_id':rt_state.get('directive_id'),
        'assessment':assessment,'closure_plan':plan
    }
    write_json(root/'ai_runtime_state.json',rt_state)
    refresh_context_files(root,state,rt_cfg,rt_state)
    delivery=state.get('release',{}).get('delivery_mode','portable_bundle')
    if delivery=='persistent_workspace':
        if assessment['impact']==MAJOR_PATCH:
            create_manifest(root,state,len(passes))
        closure=structural_audit(root,state,True,check_pdfs=True)
        metrics['total_seconds']=round(time.time()-total_start,4)
        metrics['closure']='PASS' if not closure else 'FAIL'
        record_latency(root,metrics)
        if closure:
            print('\n'.join(closure),file=sys.stderr); return 5
        print(f"PASS: release impact={assessment['impact']}")
        print(f'PASS: stable semantic fixed point in {len(passes)} passes')
        print(f"PASS: incremental build generated={len(build['ran'])} cache_hits={len(build['skipped'])}")
        if assessment['impact']==MINOR_PATCH:
            print('PASS: minimal persistent closure; unaffected derived artifacts/manifest not regenerated')
        else:
            print('PASS: major persistent workspace closure; portable exports deferred')
        return 0
    create_ai_handoff(root,state); create_manifest(root,state,len(passes)); bundle=create_bundle(root,state)
    closure=structural_audit(root,state,True,check_pdfs=True)
    metrics['total_seconds']=round(time.time()-total_start,4); metrics['closure']='PASS' if not closure else 'FAIL'; record_latency(root,metrics)
    if closure:
        print('\n'.join(closure),file=sys.stderr); return 5
    print(f"PASS: release impact={assessment['impact']}")
    print(f'PASS: stable semantic fixed point in {len(passes)} passes')
    print('PASS: AI handoff exactly five files')
    print(f'PASS: versioned categorized bundle={bundle.name}')
    return 0


def export_portable(config_path: Path) -> int:
    root,state,_=resolve_root(config_path)
    issues=operational_risk_audit(root,state)+structural_audit(root,state,True,check_pdfs=True)
    if issues:
        print('\n'.join(issues),file=sys.stderr); return 5
    create_ai_handoff(root,state); create_manifest(root,state,0); bundle=create_bundle(root,state)
    print('PASS: portable AI handoff exactly five files')
    print(f'PASS: versioned categorized bundle={bundle.name}')
    return 0


def status(config_path: Path) -> int:
    root,state,_=resolve_root(config_path)
    issues=operational_risk_audit(root,state)+structural_audit(root,state,True,check_pdfs=True)
    print(json.dumps({'release':state.get('release',{}).get('version'),'issues':issues,'primary_state':primary_state(root,state)},indent=2))
    return 1 if issues else 0
