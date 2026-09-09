import copy,json,unittest
from pathlib import Path
from profile_audit import validate_report
from ai_runtime_adapter import instruction_packet
ROOT=Path(__file__).resolve().parents[2]

def fixture():
 return dict(schema_version='1.0',advisory_only=True,target=dict(profile_id='theme_designer',session_id='synthetic-1',profile_version='0.13.0',contract_snapshot='User approved blue; reference PDF required after approval.',completion_evidence_refs=['e1']),status='COMPLETE',evidence=[dict(id='e1',source='synthetic fixture',locator='turns 1-4',summary='Blue approved; PDF delivered; same answered question asked twice.',availability='AVAILABLE',sha256=None)],findings=[dict(id='f1',dimension='unnecessary_friction',requirement='Reuse supplied answers',verdict='MISSED',claim_type='OBSERVATION',evidence_refs=['e1'],rationale='Second identical question had no changed constraint.',confidence='HIGH',attribution='HOST_EXECUTION')],proposals=[dict(id='p1',finding_refs=['f1'],target='theme question policy',before='Ask material questions',after='Check prior answers before asking',lifecycle_candidate='MERGE',expected_benefit='May avoid repeated turns; unmeasured',risk='Could miss changed preferences',feasibility='Reasoning host can consult trace',validation='Replay with unchanged and changed preferences',rollback='Retain original policy if changed preferences are missed',decision='PENDING_MAIN_HOST')],limitations=['Synthetic test, not a real performance assessment'],metrics=[])

class AuditTests(unittest.TestCase):
 def test_valid_report_does_not_mutate_inputs(self):
  r=fixture(); old=copy.deepcopy(r);validate_report(r);self.assertEqual(old,r)
 def test_dangling_evidence_rejected(self):
  r=fixture();r['findings'][0]['evidence_refs']=['missing']
  with self.assertRaises(ValueError):validate_report(r)
 def test_unavailable_evidence_not_failure(self):
  r=fixture();r.update(status='INSUFFICIENT_EVIDENCE',proposals=[]);r['evidence'][0]['availability']='UNAVAILABLE';r['findings'][0].update(verdict='UNKNOWN',confidence='LOW');validate_report(r)
 def test_partial_trace_cannot_claim_complete(self):
  r=fixture();r['evidence'][0]['availability']='TRUNCATED'
  with self.assertRaises(ValueError):validate_report(r)
 def test_integration_and_over_budget_rejected(self):
  import jsonschema
  for key,value in [('advisory_only',False),('proposals',fixture()['proposals']*4)]:
   r=fixture();r[key]=value
   with self.assertRaises(jsonschema.ValidationError):validate_report(r)
  r=fixture();r['proposals'][0]['decision']='ACCEPTED'
  with self.assertRaises(jsonschema.ValidationError):validate_report(r)
 def test_policy_serialized_and_no_execution_modules(self):
  c=json.loads((ROOT/'ai_runtime_config.json').read_text());s=json.loads((ROOT/'ai_runtime_state.json').read_text());old=copy.deepcopy(s)
  p=instruction_packet(c,s,['reasoning'],'profile_performance_auditor')
  self.assertIn('profile_performance_audit_policy',p);self.assertIn('private chain-of-thought',p);self.assertIn('Subjective'.lower(),p.lower());self.assertIn('PENDING',json.dumps(json.loads((ROOT/'profile_audit_report_schema.json').read_text())))
  self.assertEqual(s,old)
  selected=c['profiles']['definitions']['profile_performance_auditor']['enabled_modules']
  self.assertNotIn('extension.predictive_next_step',selected);self.assertNotIn('core.recursive_mutation_lifecycle',selected)
  self.assertNotEqual(selected,c['profiles']['definitions']['strategic_reviewer']['enabled_modules'])
 def test_unknown_metric_cannot_be_reported_as_measured(self):
  r=fixture();r['metrics']=[dict(name='duration',value=12,unit='s',scope_and_denominator='session',evidence_refs=[])]
  with self.assertRaises(ValueError):validate_report(r)
 def test_config_schema_enforces_advisory(self):
  import jsonschema
  c=json.loads((ROOT/'ai_runtime_config.json').read_text());schema=json.loads((ROOT/'ai_runtime_schema.json').read_text());c['profile_performance_audit_policy']['auto_integrate']=True
  with self.assertRaises(jsonschema.ValidationError):jsonschema.validate(c,schema)
