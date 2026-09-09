from __future__ import annotations
import json, subprocess, sys, time
from pathlib import Path
import jsonschema
from .common import safe_artifact_path, write_json
from .state import resolve_root, export_generated_python, import_generated_python, primary_state
from .audits import operational_risk_audit, structural_audit
from .pdf_ops import render_and_preflight
from .artifacts import create_report, create_ai_handoff, finalize_runtime_state, update_trace_after_run, create_manifest, create_bundle
from .convergence import ConvergenceTracker
from .testing import run_regression_suite


def run_known_generators(root: Path, state: dict) -> None:
    seen=[]
    for a in state['artifacts']:
        g=a.get('generator')
        if a['classification']=='REQUIRED' and g and g not in seen: seen.append(g)
    for rel in seen:
        script=safe_artifact_path(root,rel)
        if not script.exists(): raise RuntimeError(f'BLOCK: missing generator {rel}')
        subprocess.run([sys.executable,str(script)],check=True,cwd=str(root),stdout=subprocess.DEVNULL)


def sync(config_path: Path, import_python_first: bool=False) -> int:
    root,state,schema=resolve_root(config_path)
    risk=operational_risk_audit(root,state)
    if risk:
        print('\n'.join(risk),file=sys.stderr); return 2
    if import_python_first:
        state=import_generated_python(root); jsonschema.validate(state,schema); write_json(config_path,state)
    export_generated_python(root,state)
    test_cfg=state.get('testing',{})
    if test_cfg.get('enabled',False) and test_cfg.get('preflight_required',False):
        ok, output = run_regression_suite(root, test_cfg.get('report','regression_test_report.txt'))
        if not ok:
            print(output,file=sys.stderr); return 6
    t0=time.time(); passes=[]; stable=False; tracker=ConvergenceTracker(state['convergence'].get('detect_cycles',True))
    for n in range(1,state['convergence']['max_passes']+1):
        run_known_generators(root,state); export_generated_python(root,state)
        issues=structural_audit(root,state,False); current=primary_state(root,state)
        obs=tracker.observe(current,issues)
        passes.append({'pass':n,'changed':obs['changed'],'issues':list(obs['issues'])})
        if obs['cycle']: break
        if obs['stable']: stable=True; break
    conv=time.time()-t0
    if not stable:
        create_report(root,state,passes,['convergence did not reach stable fixed point'],conv,0); return 3
    final=structural_audit(root,state,False)
    verify,verify_seconds=render_and_preflight(root); final+=verify
    if final:
        create_report(root,state,passes,final,conv,verify_seconds); return 4
    create_report(root,state,passes,[],conv,verify_seconds)
    finalize_runtime_state(root,state)
    update_trace_after_run(root,state,passes,[])
    delivery=state.get('release',{}).get('delivery_mode','portable_bundle')
    if delivery == 'persistent_workspace':
        create_manifest(root,state,len(passes))
        closure=structural_audit(root,state,True)
        if closure:
            print('\n'.join(closure),file=sys.stderr); return 5
        print(f'PASS: stable fixed point in {len(passes)} passes')
        print('PASS: persistent workspace closure; portable exports deferred')
        return 0
    create_ai_handoff(root,state)
    create_manifest(root,state,len(passes))
    bundle=create_bundle(root,state)
    closure=structural_audit(root,state,True)
    if closure:
        print('\n'.join(closure),file=sys.stderr); return 5
    print(f'PASS: stable fixed point in {len(passes)} passes')
    print('PASS: AI handoff exactly five files')
    print(f'PASS: versioned categorized bundle={bundle.name}')
    return 0


def export_portable(config_path: Path) -> int:
    root,state,_=resolve_root(config_path)
    issues=operational_risk_audit(root,state)+structural_audit(root,state,True)
    if issues:
        print('\n'.join(issues),file=sys.stderr); return 5
    create_ai_handoff(root,state)
    create_manifest(root,state,0)
    bundle=create_bundle(root,state)
    print('PASS: portable AI handoff exactly five files')
    print(f'PASS: versioned categorized bundle={bundle.name}')
    return 0


def status(config_path: Path) -> int:
    root,state,_=resolve_root(config_path)
    issues=operational_risk_audit(root,state)+structural_audit(root,state,True)
    print(json.dumps({'release':state.get('release',{}).get('version'),'issues':issues,'primary_state':primary_state(root,state)},indent=2))
    return 1 if issues else 0
