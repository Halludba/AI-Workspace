import json, unittest
from pathlib import Path
from ai_runtime_adapter import instruction_packet

ROOT = Path(__file__).resolve().parents[2]

class AgentEcosystemTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cfg = json.loads((ROOT/'ai_runtime_config.json').read_text(encoding='utf-8'))
        cls.state = json.loads((ROOT/'ai_runtime_state.json').read_text(encoding='utf-8'))

    def test_custom_prompt_and_enhancer_share_one_core(self):
        profiles = self.cfg['profiles']['definitions']
        creator = profiles['custom_prompt']
        enhancer = profiles['prompt_enhancer']
        module = 'extension.prompt_specification_architect'
        self.assertIn(module, creator['enabled_modules'])
        self.assertIn(module, enhancer['enabled_modules'])
        self.assertEqual(creator['profile_parameters']['prompt_mode'], 'CREATE')
        self.assertEqual(creator['profile_parameters']['prompt_scope'], 'ANY_PROMPT')
        self.assertEqual(enhancer['profile_parameters']['prompt_mode'], 'ENHANCE')
        self.assertEqual(sum(m['id']==module for m in self.cfg['modules']), 1)

    def test_prompt_creator_is_alias_not_duplicate_profile(self):
        profiles=self.cfg['profiles']
        self.assertNotIn('prompt_creator',profiles['definitions'])
        self.assertEqual(profiles['aliases']['prompt_creator'],'custom_prompt')
        packet=instruction_packet(self.cfg,self.state,['reasoning'],'prompt_creator')
        self.assertIn('PROFILE: custom_prompt',packet)
    def test_custom_prompt_handles_research_without_enabling_capabilities(self):
        profiles=self.cfg['profiles']['definitions']
        self.assertNotIn('deep_research_agent_architect',profiles)
        self.assertFalse(any(m['id']=='extension.deep_research_agent_architect' for m in self.cfg['modules']))
        module=next(m for m in self.cfg['modules'] if m['id']=='extension.prompt_specification_architect')
        text=' '.join(module['behavior'])+' '+module['output_policy']
        self.assertIn('research or Deep Research prompts',text)
        self.assertIn('never enables Deep Research',text)
        self.assertIn('plugins/capabilities',text)

    def test_capability_activation_is_user_host_controlled(self):
        p=self.cfg['agent_development_policy']
        self.assertEqual(p['pipeline'][0],'CREATE_OR_ENHANCE')
        self.assertNotIn('RESEARCH_PRECURSOR_WHEN_NEEDED',p['pipeline'])
        self.assertIn('plugins/tools/capabilities',p['capability_activation_boundary'])
        self.assertNotIn('deep_research_agent_architect_policy',self.cfg)

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
        self.assertIn('CREATE_OR_ENHANCE', p['pipeline'])
        self.assertIn('REASONING_AUDIT', p['pipeline'])
        self.assertIn('PROFILE_PERFORMANCE_AUDIT', p['pipeline'])
        self.assertEqual(p['decision_record_status'], 'ACTIVE_AFTER_VALIDATION')
        self.assertIn('not hidden chain-of-thought', p['decision_record_rule'])

    def test_adapter_exposes_custom_prompt_mode_and_policy(self):
        packet = instruction_packet(self.cfg, self.state, ['reasoning'], 'custom_prompt')
        self.assertIn('PROFILE PARAMETERS:', packet)
        self.assertIn('"prompt_mode": "CREATE"', packet)
        self.assertIn('"prompt_scope": "ANY_PROMPT"', packet)
        self.assertIn('AGENT_DEVELOPMENT_POLICY:', packet)
        audit_packet = instruction_packet(self.cfg, self.state, ['reasoning'], 'reasoning_auditor')
        self.assertIn('extension.epistemic_reasoning_audit', audit_packet)

    def test_project_plan_part4_reflects_profile_capability_correction(self):
        plan = json.loads((ROOT/'project_plan.json').read_text(encoding='utf-8'))
        self.assertEqual(plan['last_completed_part_id'], 'deep-research-agent-architect')
        self.assertEqual(plan['next_recommended_part_id'], 'periodic-agent-quality-loop')
        by_id = {p['id']: p for p in plan['parts']}
        part4=by_id['deep-research-agent-architect']
        self.assertEqual(part4['status'],'COMPLETED')
        self.assertIn('Custom Prompt',part4['objective'])
        self.assertIn('separately user-enabled capabilities',part4['objective'])

if __name__ == '__main__':
    unittest.main()
