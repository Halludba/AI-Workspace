from __future__ import annotations
import subprocess
from pathlib import Path

MINOR_PATCH='MINOR_PATCH'
MAJOR_PATCH='MAJOR_PATCH'

DERIVED_PREFIXES=(
    'System/current/_pdf_system_verify_',
    'System/current/_visual_check',
    'System/current/.runtime_cache/',
    'System/current/AI Handoff/',
)
DERIVED_FILES={
    'System/current/Formats.pdf','System/current/PDF_Workflow.pdf',
    'System/current/Formats_preflight.txt','System/current/PDF_Workflow_preflight.txt',
    'System/current/generated_rules.py','System/current/pdf_system_manifest.json',
    'System/current/context_index.json','System/current/dependency_graph.json',
    'System/current/active_context.json','System/current/regression_test_report.txt',
    'System/current/recursive_convergence_report.txt','System/current/AI_Runtime_Instructions.txt',
}
MAJOR_PATHS={
    'System/current/ai_runtime_schema.json','System/current/pdf_system_schema.json',
    'System/current/project_plan_schema.json','System/current/decision_record_schema.json',
    'System/current/pdf_engine/orchestrator.py','System/current/pdf_engine/convergence.py',
    'System/current/pdf_engine/state.py','System/current/pdf_engine/release_impact.py',
}
MAJOR_DIFF_TOKENS=(
    'authority_order','core.recursive_mutation_lifecycle','release_impact_policy',
    'workspace_policy','planning_policy','execution_capacity_policy',
    'module_types','behavioral_determinism_boundary',
)

def _git(repo: Path,*args: str) -> str:
    p=subprocess.run(['git',*args],cwd=str(repo),text=True,capture_output=True)
    return p.stdout if p.returncode==0 else ''

def working_tree_changes(repo: Path) -> list[str]:
    out=_git(repo,'status','--porcelain')
    paths=[]
    for line in out.splitlines():
        if not line.strip(): continue
        path=line[3:].strip()
        if ' -> ' in path: path=path.split(' -> ',1)[1]
        paths.append(path.replace('\\','/'))
    return sorted(dict.fromkeys(paths))

def canonical_changes(paths: list[str]) -> list[str]:
    result=[]
    for path in paths:
        if path in DERIVED_FILES or any(path.startswith(p) for p in DERIVED_PREFIXES):
            continue
        if path.endswith('.pyc') or '/__pycache__/' in path: continue
        if path.startswith('System/current/_v') and path.endswith('.py'): continue
        if path.startswith('System/current/_part') and path.endswith('.py'): continue
        result.append(path)
    return result
def classify_change(repo: Path, paths: list[str] | None=None, *,
                    explicit_breaking: bool=False,
                    authority_change: bool=False,
                    state_migration: bool=False,
                    core_lifecycle_change: bool=False) -> dict:
    paths=canonical_changes(paths if paths is not None else working_tree_changes(repo))
    reasons=[]
    if explicit_breaking: reasons.append('explicit_breaking_change')
    if authority_change: reasons.append('authority_or_safety_boundary_change')
    if state_migration: reasons.append('incompatible_state_or_schema_migration')
    if core_lifecycle_change: reasons.append('core_lifecycle_change')
    major_paths=[p for p in paths if p in MAJOR_PATHS]
    if major_paths: reasons.append('major_path:'+','.join(major_paths))
    diff=_git(repo,'diff','--',*paths) if paths else ''
    changed_text='\n'.join(line[1:] for line in diff.splitlines() if (line.startswith('+') or line.startswith('-')) and not line.startswith('+++') and not line.startswith('---'))
    hits=[token for token in MAJOR_DIFF_TOKENS if token in changed_text]
    if hits: reasons.append('major_semantic_tokens:'+','.join(hits))
    impact=MAJOR_PATCH if reasons else MINOR_PATCH
    return {'impact':impact,'reasons':reasons or ['bounded_backward_compatible_change'],
            'canonical_changed_paths':paths}

def closure_plan(assessment: dict) -> dict:
    paths=assessment.get('canonical_changed_paths',[])
    impact=assessment['impact']
    if impact==MINOR_PATCH:
        return {'impact':impact,'full_convergence':False,'scoped_iteration_tests':True,
                'full_regression_before_commit':True,'refresh_global_indexes':False,
                'regenerate_all_derived':False,'portable_export':False,
                'manifest_refresh':False,'pdf_verification':'ONLY_IF_PDF_INPUT_CHANGED',
                'persistence':'ONE_ONEDRIVE_SYNCED_WORKTREE_PLUS_ONE_GIT_COMMIT_PUSH',
                'changed_paths':paths}
    return {'impact':impact,'full_convergence':True,'scoped_iteration_tests':True,
            'full_regression_before_commit':True,'refresh_global_indexes':True,
            'regenerate_all_affected_derived':True,'portable_export':False,
            'manifest_refresh':True,'pdf_verification':'AFFECTED_PDFS_AND_CHANGED_PAGES',
            'persistence':'ONE_ONEDRIVE_SYNCED_WORKTREE_PLUS_ONE_GIT_COMMIT_PUSH',
            'changed_paths':paths}
