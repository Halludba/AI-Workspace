import copy, json, tempfile, unittest
from pathlib import Path
import jsonschema
from quality_audit import prepare_packet, validate_report
from ai_runtime_adapter import instruction_packet

ROOT=Path(__file__).resolve().parents[2]


def report_fixture():
    return {
      'schema_version':'1.0','advisory_only':True,'audit_id':'qa-synthetic-0001','created_utc':'2026-09-09T10:00:00+00:00',
      'scope':{'profiles':['general_balanced'],'decision_record_ids':['r1'],'profile_session_ids':[],'sampling_rule':'latest bounded material records'},
      'status':'PARTIAL',
      'evidence':[{'id':'e1','kind':'decision_record','source':'synthetic','availability':'AVAILABLE','sha256':None}],
      'dimensions':[
        {'id':'reasoning_integrity','status':'PASS','evidence_refs':['e1'],'findings':[{'id':'f1','verdict':'SUPPORTED','summary':'Visible rationale is internally supported in fixture.','evidence_refs':['e1'],'confidence':'MEDIUM','owner':'REASONING_AUDITOR'}]},
        {'id':'artifact_code_consistency','status':'PASS','evidence_refs':['e1'],'findings':[]},
        {'id':'profile_performance','status':'UNKNOWN','evidence_refs':[],'findings':[{'id':'f2','verdict':'UNKNOWN','summary':'No completed profile-session trace supplied.','evidence_refs':[],'confidence':'LOW','owner':'PROFILE_PERFORMANCE_AUDITOR'}]},
      ],
      'proposals':[], 'limitations':['Synthetic fixture'],
      'self_audit_boundary':'AUDIT_CANNOT_AUTO_MUTATE_OR_APPROVE_ITSELF; ALL_PROPOSALS_REMAIN_PENDING_MAIN_HOST'
    }


class QualityAuditTests(unittest.TestCase):
    def test_prepare_packet_uses_real_decision_records_without_private_reasoning(self):
        p=prepare_packet(limit_per_profile=5,audit_id='qa-test-packet')
        self.assertGreaterEqual(p['sampling']['selected_record_count'],1)
        self.assertIn('reasoning_integrity',p['host_review_required'][0])
        self.assertNotIn('chain_of_thought',json.dumps(p).lower())
    def test_report_validator_preserves_three_dimensions_and_advisory_boundary(self):
        r=report_fixture(); old=copy.deepcopy(r); validate_report(r); self.assertEqual(r,old)
        bad=copy.deepcopy(r); bad['advisory_only']=False
        with self.assertRaises(jsonschema.ValidationError): validate_report(bad)
        bad=copy.deepcopy(r); bad['proposals']=[{'id':'p1','finding_refs':['f1'],'target':'x','summary':'y','lifecycle_candidate':'REWRITE','validation':'test','rollback':'revert','decision':'ACCEPTED'}]
        with self.assertRaises(jsonschema.ValidationError): validate_report(bad)

    def test_complete_cannot_hide_pending_dimensions(self):
        r=report_fixture(); r['status']='COMPLETE'
        with self.assertRaises(ValueError): validate_report(r)

    def test_runtime_policy_reuses_existing_auditors_not_mega_profile(self):
        cfg=json.loads((ROOT/'ai_runtime_config.json').read_text(encoding='utf-8'))
        p=cfg['periodic_quality_audit_policy']
        self.assertEqual(p['reasoning_owner'],'reasoning_auditor')
        self.assertEqual(p['profile_performance_owner'],'profile_performance_auditor')
        self.assertFalse(p['automatic_schedule_enabled'])
        self.assertEqual(p['default_cadence'],'MANUAL_ON_DEMAND')
        self.assertNotIn('system_quality_auditor',cfg['profiles']['definitions'])
        self.assertIn('quality_audit.py',p['deterministic_checker'])
        state=json.loads((ROOT/'ai_runtime_state.json').read_text(encoding='utf-8'))
        packet=instruction_packet(cfg,state,['reasoning'],'general_balanced')
        self.assertIn('PERIODIC_QUALITY_AUDIT_POLICY:',packet)

    def test_sampling_is_bounded_and_missing_session_evidence_stays_unknown(self):
        cfg=json.loads((ROOT/'ai_runtime_config.json').read_text(encoding='utf-8'))
        p=cfg['periodic_quality_audit_policy']
        self.assertLessEqual(p['sampling']['decision_records_per_profile'],10)
        self.assertIn('UNKNOWN',p['missing_evidence_rule'])
        self.assertIn('PENDING_MAIN_HOST',p['governance_rule'])


if __name__=='__main__': unittest.main()

