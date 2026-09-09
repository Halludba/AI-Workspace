"""Validate observable audit reports. Semantic judgments remain with the host.
No integration or config mutation API is provided.
"""
import argparse, json
from pathlib import Path
import jsonschema
ROOT=Path(__file__).resolve().parent

def validate_report(report, schema=None):
    schema=schema or json.loads((ROOT/'profile_audit_report_schema.json').read_text(encoding='utf-8'))
    jsonschema.validate(report,schema)
    for key in ('evidence','findings','proposals'):
        ids=[x['id'] for x in report[key]]
        if len(ids)!=len(set(ids)): raise ValueError('Duplicate '+key+' id')
    ev={e['id']:e for e in report['evidence']}
    findings={f['id']:f for f in report['findings']}
    def check_refs(refs, available=False):
        if any(x not in ev for x in refs): raise ValueError('Unknown evidence reference')
        if available and not any(ev[x]['availability']=='AVAILABLE' for x in refs):
            raise ValueError('Supported claim requires available evidence')
    check_refs(report['target']['completion_evidence_refs'],report['status']=='COMPLETE')
    for f in report['findings']:
        check_refs(f['evidence_refs'],f['verdict']!='UNKNOWN')
        if f['verdict']=='UNKNOWN' and f['confidence']!='LOW': raise ValueError('Unknown verdict cannot be confident')
    for m in report['metrics']:
        check_refs(m['evidence_refs'],m['value'] is not None)
    for p in report['proposals']:
        if not p['finding_refs'] or any(x not in findings for x in p['finding_refs']): raise ValueError('Proposal needs known findings')
        if all(findings[x]['verdict']=='UNKNOWN' for x in p['finding_refs']): raise ValueError('Unsupported proposal')
    if report['status']=='INSUFFICIENT_EVIDENCE' and report['proposals']: raise ValueError('Insufficient evidence cannot support proposals')
    if report['status']=='COMPLETE':
        if any(e['availability']!='AVAILABLE' for e in report['evidence']) or any(f['verdict']=='UNKNOWN' for f in report['findings']):
            raise ValueError('Incomplete evidence must remain PARTIAL')
    return report

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('report');args=ap.parse_args()
    validate_report(json.loads(Path(args.report).read_text(encoding='utf-8')))
    print('VALID: structural evidence and advisory invariants; not proof of semantic correctness.')
if __name__=='__main__': main()
