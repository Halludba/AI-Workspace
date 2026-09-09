from __future__ import annotations
import pprint, shutil, subprocess, sys, zipfile
from pathlib import Path
from .common import MANIFEST_NAME, REPORT_NAME, SCHEMA_NAME, load_json, write_json, safe_artifact_path, sha256_file
from .pdf_ops import clean_pdf_markdown


def artifact_snapshot(root: Path, state: dict) -> list[dict]:
    rec = []
    for a in state['artifacts']:
        p = safe_artifact_path(root, a['path'])
        if p.exists() and p.is_file() and not a['path'].startswith('AI Handoff/') and Path(a['path']).name not in {MANIFEST_NAME, state['release']['bundle_filename']}:
            rec.append({'path': a['path'], 'role': a['role'], 'sha256': sha256_file(p), 'bytes': p.stat().st_size})
    return rec


def create_ai_handoff(root: Path, state: dict) -> list[Path]:
    d = root / 'AI Handoff'
    d.mkdir(parents=True, exist_ok=True)
    p1 = d / '01_AI_BRIEFING_AND_HISTORY.md'
    chunks = ['# AI Briefing and History', '', '> Derived handoff view. Authoritative sources remain the validated runtime/config files and PDFs.', '']
    runtime_cfg = load_json(root/'ai_runtime_config.json')
    review = runtime_cfg.get('secondary_review_policy', {})
    if review:
        chunks += ['## Optional Strategic Second-Mind Role', '',
                   'When this five-file handoff is given to a secondary AI for review, use the strategic_reviewer role/profile when appropriate. The reviewer complements rather than duplicates the main execution host: interpret state and outcomes, maintain the why, pressure-test direction, surface blind spots/trade-offs, and make suggestions. The user chooses direction; the main execution host decides how/if reviewer feedback integrates under the normal lifecycle. A second model is optional and provides supplemental perspective, not guaranteed independence or correctness.', '']
    chunks += ['## Profile Performance Auditor', '', runtime_cfg['profile_performance_audit_policy']['purpose'], 'Use profile_performance_auditor for a specific completed session; strategic_reviewer remains the broader direction reviewer. Proposals remain pending main-host governance.', '']
    for rel, label in [('README_FIRST.txt','Start Here'),('MUTATION_TRACE.md','Latest Mutation Trace'),('CHANGELOG.md','Changelog'),(REPORT_NAME,'Latest Convergence Report')]:
        p = root / rel
        if p.exists(): chunks += [f'## {label}', '', p.read_text(encoding='utf-8', errors='replace').strip(), '']
    p1.write_text('\n'.join(chunks).strip() + '\n', encoding='utf-8')
    p2 = d / '02_UNIFIED_SYSTEM_STATE.json'
    unified = {'view_type':'AI_OPTIMIZED_DERIVED_STATE','authoritative':False,'release_version':state['release']['version'],'pdf_system_config':state,'pdf_system_schema':load_json(root/SCHEMA_NAME),'ai_runtime_config':load_json(root/'ai_runtime_config.json'),'ai_runtime_schema':load_json(root/'ai_runtime_schema.json'),'ai_runtime_state':load_json(root/'ai_runtime_state.json'),'project_plan':load_json(root/'project_plan.json') if (root/'project_plan.json').exists() else None,'project_plan_schema':load_json(root/'project_plan_schema.json') if (root/'project_plan_schema.json').exists() else None,'mutation_trace':load_json(root/'mutation_trace.json'),'profile_audit_report_schema':load_json(root/'profile_audit_report_schema.json'),'version_history':load_json(root/'version_history.json'),'artifact_snapshot':artifact_snapshot(root,state),'manifest_note':'Direct artifact_snapshot is used here to avoid a circular dependency with the final manifest, which is generated after this derived view.'}
    write_json(p2, unified)
    p3 = d / '03_AUTHORITATIVE_RULES.md'; p3.write_text(clean_pdf_markdown(root/'Formats.pdf','Formats - Authoritative Rules'), encoding='utf-8')
    p4 = d / '04_OPERATIONAL_WORKFLOW.md'; p4.write_text(clean_pdf_markdown(root/'PDF_Workflow.pdf','PDF Workflow - Operational Procedure'), encoding='utf-8')
    p5 = d / '05_EXECUTION_ENGINE_AND_LOGIC.py'
    component_paths = ['pdf_system_engine.py','generated_rules.py','ai_runtime_adapter.py','profile_audit.py','materialize_release.py'] + list(state.get('modularity', {}).get('engine_modules', [])) + list(state.get('testing', {}).get('test_files', []))
    component_paths += [a['path'] for a in state.get('artifacts', []) if a.get('classification') == 'REQUIRED' and a.get('include_in_bundle', True) and str(a.get('path','')).endswith('.py') and 'generator' in str(a.get('role',''))]
    component_paths = list(dict.fromkeys(component_paths))
    components = {name: (root/name).read_text(encoding='utf-8') for name in component_paths}
    capsule = '''#!/usr/bin/env python3\n"""AI-optimized derived source capsule.\n\nThis file is not an authoritative mutable source. It contains exact snapshots of\nthe executable components and can reconstruct their relative paths for inspection/testing.\n"""\nfrom pathlib import Path\n\nCOMPONENTS = ''' + pprint.pformat(components, width=120, sort_dicts=False) + '''\n\ndef materialize(directory):\n    directory=Path(directory); directory.mkdir(parents=True,exist_ok=True)\n    for name,source in COMPONENTS.items():\n        target=directory/name; target.parent.mkdir(parents=True,exist_ok=True)\n        target.write_text(source,encoding="utf-8")\n    return list(COMPONENTS)\n\nif __name__ == "__main__":\n    print("Contained components:")\n    for name in COMPONENTS: print(" -",name)\n'''
    p5.write_text(capsule, encoding='utf-8')
    paths = [p1,p2,p3,p4,p5]
    if len(paths) != state['release']['ai_handoff_file_count']: raise RuntimeError('BLOCK: AI handoff does not contain exactly five files')
    for p in paths:
        if not p.exists() or p.stat().st_size == 0: raise RuntimeError(f'BLOCK: invalid AI handoff file {p.name}')
    compile(p5.read_text(encoding='utf-8'), str(p5), 'exec')
    actual_files=sorted(x.name for x in d.iterdir() if x.is_file())
    expected_files=sorted(x.name for x in paths)
    if actual_files != expected_files: raise RuntimeError(f'BLOCK: AI handoff folder contains unexpected files: {actual_files}')
    return paths


def create_report(root: Path, state: dict, passes: list[dict], issues: list[str], convergence_seconds: float, verification_seconds: float) -> Path:
    trace = load_json(root/'mutation_trace.json') if (root/'mutation_trace.json').exists() else {}
    lines = ['RECURSIVE AI CONFIG SYSTEM - CONVERGENCE / CLOSURE REPORT','',f'Release: {state["release"]["version"]}',f'Directive: {trace.get("user_prompt_summary","n/a")}',f'Target: {trace.get("target_improvement","n/a")}',f'Convergence seconds: {convergence_seconds:.3f}',f'Verification seconds: {verification_seconds:.3f}','']
    for p in passes:
        lines.append(f"PASS {p['pass']}: changed_from_previous={p['changed']} issues={len(p['issues'])}")
        lines += [f'  - {x}' for x in p['issues']]
    lines += ['', 'FINAL STATUS: ' + ('STABLE FIXED POINT + EXECUTION CLOSURE' if not issues else 'NOT CLOSED')]
    if issues: lines += [f'- {x}' for x in issues]
    lines += ['', 'Boundary: semantic rule invention remains the responsibility of a reasoning host; local code synchronizes and verifies known structured artifacts.']
    out = root / REPORT_NAME; out.write_text('\n'.join(lines) + '\n', encoding='utf-8'); return out


def create_manifest(root: Path, state: dict, stable_passes: int) -> Path:
    records = []
    for a in state['artifacts']:
        p = safe_artifact_path(root, a['path']); rec = {'path':a['path'],'classification':a['classification'],'role':a['role'],'bundle_folder':a.get('bundle_folder'),'exists':p.exists()}
        if p.exists() and p.is_file() and p.name != MANIFEST_NAME: rec.update(sha256=sha256_file(p), bytes=p.stat().st_size)
        records.append(rec)
    manifest = {'system_name':state['system_name'],'subsystem_version':state['system_version'],'release_version':state['release']['version'],'bundle_filename':state['release']['bundle_filename'],'stable':True,'convergence_passes':stable_passes,'artifacts':records}
    out = root / MANIFEST_NAME; write_json(out, manifest); return out


def create_bundle(root: Path, state: dict) -> Path:
    out = root / state['release']['bundle_filename']
    if out.exists(): out.unlink()
    entries = []
    for a in state['artifacts']:
        if not a.get('include_in_bundle', True): continue
        p = safe_artifact_path(root, a['path'])
        if not p.exists() or not p.is_file(): continue
        folder = a.get('bundle_folder','').strip('/')
        arc = f'{folder}/{p.name}' if folder else p.name
        entries.append((p,arc))
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p,arc in sorted(entries,key=lambda x:x[1].lower()): z.write(p,arcname=arc)
    return out


def finalize_runtime_state(root: Path, state: dict) -> None:
    p = root / 'ai_runtime_state.json'
    if not p.exists(): return
    st = load_json(p); st['phase']='HANDOFF'; st['stable']=True; st['predictive_budget_remaining']=0
    st['last_transition_reason'] = f'Release {state["release"]["version"]} reached verified fixed point and categorized handoff closure.'
    write_json(p, st)


def update_trace_after_run(root: Path, state: dict, passes: list[dict], issues: list[str]) -> None:
    p = root/'mutation_trace.json'; tr = load_json(p); tr['system_version']=state['release']['version']; tr['convergence_result']={'passes':len(passes),'stable':not issues,'issues':issues}
    tr['affected_artifacts']=[a['path'] for a in state['artifacts'] if safe_artifact_path(root,a['path']).exists()]
    write_json(p,tr)
    history = load_json(root/'version_history.json')
    history['releases'][-1]['verification'] = tr['convergence_result']
    write_json(root/'version_history.json',history)
    md=['# Mutation Trace','',f'**System version:** {tr["system_version"]}',f'**Directive:** {tr["user_prompt_summary"]}',f'**Target improvement:** {tr["target_improvement"]}','','## Candidate decisions']
    for c in tr['candidate_decisions']: md.append(f'- **{c["decision"]} - {c["candidate"]}:** {c["reason"]}')
    md += ['','## Accepted changes'] + [f'- {x}' for x in tr['accepted_changes']] + ['','## Rejected / merged / no-op'] + [f'- {x}' for x in tr['rejected_or_noop']] + ['','## Convergence result',f'- Passes: {len(passes)}',f'- Stable: {not issues}']
    (root/'MUTATION_TRACE.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
