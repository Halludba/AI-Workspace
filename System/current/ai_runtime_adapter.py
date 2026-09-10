#!/usr/bin/env python3
"""Host-neutral loader for the Recursive AI Behavior Runtime.

This does not call an AI provider. It validates the portable config and emits a
compact instruction packet that can be supplied to a reasoning-capable host.
Capabilities are provided explicitly so modules cannot pretend the host has tools
it does not actually possess.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / 'ai_runtime_config.json'
SCHEMA = ROOT / 'ai_runtime_schema.json'
STATE = ROOT / 'ai_runtime_state.json'


def load():
    cfg = json.loads(CONFIG.read_text(encoding='utf-8'))
    schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
    jsonschema.validate(cfg, schema)
    state = json.loads(STATE.read_text(encoding='utf-8'))
    jsonschema.validate(state.get('profile_audit_session'), cfg['profile_performance_audit_policy']['session_state_schema'])
    return cfg, state


def resolve_profile_id(cfg, profile_id):
    if not profile_id:
        return profile_id
    aliases=cfg.get('profiles',{}).get('aliases',{})
    return aliases.get(profile_id,aliases.get(str(profile_id).lower(),profile_id))


def _feature_set(task_features=None):
    return {str(x).strip().lower() for x in (task_features or []) if str(x).strip()}


def resolve_prompt_lane(cfg, profile, task_features=None):
    if not profile.get('profile_parameters', {}).get('progressive_activation'):
        return None
    features = _feature_set(task_features)
    if features & {'deep', 'high_assurance', 'security', 'security_sensitive', 'conflict', 'high_consequence'}:
        return 'DEEP'
    if features & {'standard', 'research', 'deep_research', 'enhance', 'ambiguous', 'large_context'}:
        return 'STANDARD'
    return profile.get('profile_parameters', {}).get('default_execution_lane', cfg.get('prompt_execution_policy', {}).get('default_lane', 'FAST'))


def _selected_modules(profile, task_features=None):
    enabled = set(profile.get('enabled_modules', []))
    progressive = profile.get('progressive_activation')
    if not progressive:
        return enabled
    selected = set(progressive.get('always_hot_modules', []))
    features = _feature_set(task_features)
    if features & {'workspace', 'workspace_context', 'project_context', 'persist'}:
        selected.add('core.persistent_workspace_continuity')
    if features & {'decision_record', 'audit_trail', 'material_decision'}:
        selected.add('core.auditable_decision_records')
    return selected & enabled


def compatible_modules(cfg, capabilities, profile_id=None, task_features=None):
    caps = set(capabilities)
    active, degraded = [], []
    profile_id = resolve_profile_id(cfg, profile_id or cfg.get('profiles', {}).get('current_profile'))
    definitions = cfg.get('profiles', {}).get('definitions', {})
    if profile_id not in definitions:
        raise KeyError(f'Unknown profile: {profile_id}')
    profile = definitions[profile_id]
    selected = _selected_modules(profile, task_features)
    for m in cfg['modules']:
        if not m['enabled'] or m['id'] not in selected:
            continue
        missing = sorted(set(m.get('required_capabilities', [])) - caps)
        (degraded if missing else active).append((m, missing))
    return active, degraded


def instruction_packet(cfg, state, capabilities, profile_override=None, task_features=None):
    selected_profile = resolve_profile_id(cfg, profile_override or state.get('current_profile') or cfg.get('profiles', {}).get('current_profile'))
    definitions = cfg.get('profiles', {}).get('definitions', {})
    if selected_profile not in definitions:
        raise KeyError(f'Unknown profile: {selected_profile}')
    profile = definitions[selected_profile]
    active, degraded = compatible_modules(cfg, capabilities, selected_profile, task_features)
    execution_lane = resolve_prompt_lane(cfg, profile, task_features)
    lane_spec = cfg.get('prompt_execution_policy', {}).get('lanes', {}).get(execution_lane, {}) if execution_lane else {}
    effective_depth = lane_spec.get('decision_depth', profile.get('decision_depth', state.get('current_decision_depth', cfg.get('decision_policy', {}).get('current_depth'))))
    effective_interaction = profile.get('interaction_mode', state.get('current_interaction_mode', cfg.get('interaction_policy', {}).get('current_mode')))
    effective_optimization = lane_spec.get('optimization_profile', profile.get('optimization_profile', state.get('current_optimization_profile', cfg.get('optimization_policy', {}).get('current_profile'))))
    lines = [
        f"RUNTIME: {cfg['runtime_name']} {cfg['runtime_version']}",
        "AUTHORITY: " + " > ".join(cfg['authority_order']),
        f"STATE: phase={state.get('phase')} predictive_budget_remaining={state.get('predictive_budget_remaining')}",
        f"PROFILE: {selected_profile}",
        f"PROFILE PURPOSE: {profile.get('purpose','')}",
        f"DECISION DEPTH: {effective_depth}",
        f"INTERACTION MODE: {effective_interaction}",
        f"OPTIMIZATION PROFILE: {effective_optimization}",
    ]
    if execution_lane:
        lines += [f"PROMPT EXECUTION LANE: {execution_lane}"]
        progressive = profile.get('progressive_activation', {})
        lazy = progressive.get('lazy_modules', [])
        if lazy:
            lines += ["LAZY MODULES: " + ", ".join(lazy)]
    if profile.get('profile_parameters'):
        lines += ["PROFILE PARAMETERS: " + json.dumps(profile['profile_parameters'], ensure_ascii=False)]
    workflow_policy_name = profile.get('workflow_policy')
    if workflow_policy_name and isinstance(cfg.get(workflow_policy_name), dict):
        lines += ["", f"WORKFLOW POLICY: {workflow_policy_name}", json.dumps(cfg[workflow_policy_name], indent=2, ensure_ascii=False)]
        reference_policy_name = cfg[workflow_policy_name].get('theme_reference_policy')
        if reference_policy_name and isinstance(cfg.get(reference_policy_name), dict):
            lines += ["", f"REFERENCE POLICY: {reference_policy_name}", json.dumps(cfg[reference_policy_name], indent=2, ensure_ascii=False)]
    lines += ["", "ACTIVE MODULES:"]
    for m, _ in active:
        lines += [f"- {m['id']} [{m['type']}]: {m['purpose']}"]
        lines += [f"  trigger: {m['trigger']}", f"  scope: {m['scope']}"]
        for behavior in m['behavior']:
            lines.append(f"  * {behavior}")
    if degraded:
        lines += ["", "DEGRADED/UNAVAILABLE MODULES:"]
        for m, missing in degraded:
            lines.append(f"- {m['id']}: missing capabilities: {', '.join(missing)}")
    active_ids = {m['id'] for m, _ in active}
    prompt_progressive = bool(profile.get('profile_parameters', {}).get('progressive_activation'))
    if prompt_progressive:
        # Aggressive policy lazy-loading is intentionally confined to prompt profiles.
        policy_names = []
        policy_by_module = (
            ('core.persistent_workspace_continuity', 'workspace_policy'),
            ('core.auditable_decision_records', 'decision_record_policy'),
            ('extension.prompt_specification_architect', 'prompt_execution_policy'),
            ('extension.prompt_specification_architect', 'agent_development_policy'),
        )
        for module_id, policy_name in policy_by_module:
            if module_id in active_ids and policy_name not in policy_names and policy_name != workflow_policy_name:
                policy_names.append(policy_name)
    else:
        # Preserve established packet contracts for every non-prompt profile.
        policy_names = list(('workspace_policy','pdf_styler_policy','planning_policy','execution_capacity_policy','secondary_review_policy','decision_record_policy','release_impact_policy','periodic_quality_audit_policy','agent_development_policy'))
        if workflow_policy_name in policy_names:
            policy_names.remove(workflow_policy_name)
    for policy_name in policy_names:
        if isinstance(cfg.get(policy_name), dict):
            lines += ["", policy_name.upper() + ':', json.dumps(cfg[policy_name], indent=2, ensure_ascii=False)]
    load_plan = (not prompt_progressive) or 'extension.strategic_plan_orchestrator' in active_ids or 'project_plan' in _feature_set(task_features)
    if load_plan:
        plan_path = ROOT / cfg.get('planning_policy', {}).get('plan_path', 'project_plan.json')
        if plan_path.exists():
            try:
                lines += ["", "PROJECT PLAN SNAPSHOT:", json.dumps(json.loads(plan_path.read_text(encoding='utf-8')), indent=2, ensure_ascii=False)]
            except Exception:
                lines += ["", "PROJECT PLAN SNAPSHOT: unavailable/invalid; do not fabricate it."]
    lines += [
        "",
        "PRE-EXECUTION RULE:",
        "Predict and test reasonably foreseeable failures before execution. Apply only local, bounded, reversible fixes that preserve user intent; otherwise disclose/hand off rather than guess.",
        "",
        "AUTONOMY RULE:",
        "Required execution may recurse until verified closure. Optional predictive execution is limited to one materially useful action per new user directive, then handoff.",
        "",
        "PROFILE RULE:",
        "Decision depth controls breadth of checks/candidates, interaction mode controls handoff/explanation behavior, and optimization profiles tune effort only; none override higher-authority constraints.",
        "",
        "DETERMINISM BOUNDARY:",
        cfg['host_contract'].get('behavioral_determinism_boundary', ''),
        "",
        "CAPABILITY RULE:",
        cfg['host_contract']['capability_degradation_policy'],
    ]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--capability', action='append', default=['reasoning'], help='Host capability; repeatable')
    ap.add_argument('--output', default=str(ROOT / 'AI_Runtime_Instructions.txt'))
    ap.add_argument('--profile', choices=sorted(set(load()[0].get('profiles',{}).get('definitions',{})) | set(load()[0].get('profiles',{}).get('aliases',{}))), help='Generate an instruction packet for a named workflow profile or alias without mutating global runtime state')
    ap.add_argument('--feature', action='append', default=[], help='Task feature used for progressive activation/lane escalation; repeatable')
    args = ap.parse_args()
    cfg, state = load()
    packet = instruction_packet(cfg, state, args.capability, args.profile, args.feature)
    Path(args.output).write_text(packet, encoding='utf-8')
    print(args.output)

if __name__ == '__main__':
    main()
