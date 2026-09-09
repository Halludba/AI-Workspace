import json, tempfile, unittest
from pathlib import Path
import decision_record as dr

ROOT = Path(__file__).resolve().parents[2]

def sample():
    return {
      'record_version':'1.0','record_id':'part3-test-record','recorded_utc':'2026-09-09T07:30:00Z',
      'directive_id':'test-directive','profile_id':'general_balanced','supersedes_record_id':None,
      'objective':'Verify the decision-record contract.','constraints':[],'claims':[],'evidence':[],
      'assumptions':[],'alternatives':[{'id':'a1','option':'retain','disposition':'NO_CHANGE','reason':'control'}],
      'decision':'Use the schema-valid record.','unknowns':[],
      'verification':[{'check':'schema','status':'PASS','evidence_ref':None}],
      'links':[],'privacy_attestation':'NO_PRIVATE_CHAIN_OF_THOUGHT_OR_HIDDEN_SCRATCHPAD_STORED'
    }

class DecisionRecordTests(unittest.TestCase):
    def test_schema_and_privacy_contract(self):
        self.assertEqual(dr.validate_record(sample())['record_id'],'part3-test-record')
        bad=sample(); bad['chain_of_thought']='forbidden'
        with self.assertRaises(Exception): dr.validate_record(bad)

    def test_append_only_writer(self):
        old=dr.ROOT
        with tempfile.TemporaryDirectory() as td:
            dr.ROOT=Path(td); (dr.ROOT/'decision_record_schema.json').write_text((ROOT/'decision_record_schema.json').read_text(encoding='utf-8'),encoding='utf-8')
            out=dr.write_record(sample()); self.assertTrue(out.exists())
            with self.assertRaises(FileExistsError): dr.write_record(sample())
        dr.ROOT=old

    def test_runtime_policy_is_active_and_auditable(self):
        cfg=json.loads((ROOT/'ai_runtime_config.json').read_text(encoding='utf-8'))
        p=cfg['decision_record_policy']
        self.assertTrue(p['enabled']); self.assertTrue(p['append_only'])
        self.assertIn('private chain-of-thought', p['privacy_boundary'])
        self.assertEqual(cfg['agent_development_policy']['decision_record_status'],'ACTIVE_AFTER_VALIDATION')
        self.assertIn('core.auditable_decision_records', cfg['profiles']['definitions']['reasoning_auditor']['enabled_modules'])

if __name__=='__main__': unittest.main()
