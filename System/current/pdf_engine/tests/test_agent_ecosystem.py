import json, unittest
from pathlib import Path
from ai_runtime_adapter import instruction_packet

ROOT = Path(__file__).resolve().parents[2]

class AgentEcosystemTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = json.loads((ROOT/'ai_runtime_config.json').read_text(encoding='utf-8'))
        cls.state = json.loads((ROOT/'ai_runtime_state.json').read_text(encoding='utf-8'))

    def test_prompt_profiles_share_one_specification_core(self):
        profiles = self.cfg['profiles']['definitions']
        creator = profiles['prompt_creator']
        enhancer = profiles['prompt_enhancer']
        module = 'extension.prompt_specification_architect'
        self.assertIn(module, creator['enabled_modules'])
        self.assertIn(module, enhancer['enabled_modules'])
        self.assertEqual(creator['profile_parameters']['prompt_mode'], 'CREATE')
        self.assertEqual(enhancer['profile_parameters']['prompt_mode'], 'ENHANCE')
        self.assertEqual(sum(m['id']==module for m in self.cfg['modules']), 1)
    def test_reasoning_auditor_is_advisory_and_private_reasoning_safe(self):
        profiles = self.cfg['profiles']['definitions']
        auditor = profiles['reasoning_auditor']
        self.assertEqual(auditor['profile_type'], 'advisory_review_agent')
        self.assertIn('extension.epistemic_reasoning_audit', auditor['enabled_modules'])
        module = next(m for m in self.cfg['modules'] if m['id']=='extension.epistemic_reasoning_audit')
        text = ' '.join(module['behavior']) + ' ' + module['output_policy']
        self.assertIn('private chain-of-thought', text)
        self.assertIn('PENDING_MAIN_HOST', text)
        self.assertIn('never auto-correct', text.lower())

    def test_agent_development_pipeline_and_decision_record_boundary(self):
        p = self.cfg['agent_development_policy']
        self.assertEqual(p['pipeline'][0], 'CREATE_OR_ENHANCE')
        self.assertIn('REASONING_AUDIT', p['pipeline'])
        self.assertIn('PROFILE_PERFORMANCE_AUDIT', p['pipeline'])
        self.assertEqual(p['decision_record_status'], 'ACTIVE_AFTER_VALIDATION')
        self.assertIn('not hidden chain-of-thought', p['decision_record_rule'])
    def test_adapter_exposes_profile_mode_and_policy(self):
        packet = instruction_packet(self.cfg, self.state, ['reasoning'], 'prompt_creator')
        self.assertIn('PROFILE PARAMETERS:', packet)
        self.assertIn('"prompt_mode": "CREATE"', packet)
        self.assertIn('AGENT_DEVELOPMENT_POLICY:', packet)
        audit_packet = instruction_packet(self.cfg, self.state, ['reasoning'], 'reasoning_auditor')
        self.assertIn('extension.epistemic_reasoning_audit', audit_packet)

    def test_project_plan_contains_ordered_agent_roadmap(self):
        plan = json.loads((ROOT/'project_plan.json').read_text(encoding='utf-8'))
        self.assertEqual(plan['status'], 'ACTIVE')
        self.assertGreaterEqual(len(plan['parts']), 5)
        self.assertIsNone(plan['current_part_id'])
        self.assertEqual(plan['last_completed_part_id'], 'decision-rationale-records')
        self.assertEqual(plan['next_recommended_part_id'], 'deep-research-agent-architect')
        by_id = {p['id']: p for p in plan['parts']}
        self.assertEqual(by_id['agent-foundation']['status'], 'COMPLETED')
        self.assertEqual(by_id['reasoning-auditor-validation']['status'], 'COMPLETED')
        self.assertEqual(by_id['decision-rationale-records']['status'], 'COMPLETED')
        self.assertIn('agent-foundation', by_id['reasoning-auditor-validation']['dependencies'])

if __name__ == '__main__':
    unittest.main()
