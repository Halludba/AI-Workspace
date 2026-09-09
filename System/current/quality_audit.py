"""Prepare and validate periodic system/profile quality audits.

The deterministic layer collects evidence and checks artifact/link consistency.
Semantic reasoning integrity and profile-performance judgments remain with the
existing reasoning_auditor and profile_performance_auditor profiles.
"""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
import jsonschema
from decision_record import validate_record

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
DECISION_DIR = ROOT / 'decision_records'
REPORT_SCHEMA = ROOT / 'quality_audit_report_schema.json'
AUDIT_ROOT = REPO / 'Audit Reports'


def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

def _local_candidates(target: str) -> list[Path]:
    base=target.split('#',1)[0].strip()
    if not base or re.match(r'^[a-z]+://',base,re.I): return []
    clean=base.replace('\\','/').lstrip('./')
    candidates=[(ROOT/base).resolve(), (REPO/clean).resolve()]
    seen=[]
    for p in candidates:
        if p not in seen: seen.append(p)
    return seen


def _git_commit_exists(commit: str) -> bool:
    if not commit: return False
    p=subprocess.run(['git','cat-file','-e',f'{commit}^{{commit}}'],cwd=str(REPO),capture_output=True)
    return p.returncode==0


def _inspect_target(kind: str, target: str, expected_sha: str|None) -> dict:
    if kind=='commit':
        exists=_git_commit_exists(target)
        return {'kind':kind,'target':target,'status':'PRESENT' if exists else 'MISSING','expected_sha256':expected_sha,'current_sha256':None}
    candidates=_local_candidates(target)
    path=next((p for p in candidates if p.exists() and p.is_file()),None)
    if path is None:
        return {'kind':kind,'target':target,'status':'UNRESOLVED_OR_MISSING','expected_sha256':expected_sha,'current_sha256':None}
    current=sha256_file(path)
    status='PRESENT_NO_RECORDED_HASH' if not expected_sha else ('HASH_MATCH' if current==expected_sha else 'CURRENT_BYTES_DRIFTED')
    return {'kind':kind,'target':target,'resolved_path':str(path.relative_to(REPO)) if path.is_relative_to(REPO) else str(path),'status':status,'expected_sha256':expected_sha,'current_sha256':current}

def select_decision_records(profile: str|None=None, limit_per_profile: int=5) -> list[tuple[Path,dict]]:
    groups=defaultdict(list)
    if not DECISION_DIR.exists(): return []
    for path in DECISION_DIR.rglob('*.json'):
        try:
            rec=json.loads(path.read_text(encoding='utf-8')); validate_record(rec)
        except Exception:
            continue
        if profile and rec.get('profile_id')!=profile: continue
        groups[rec.get('profile_id','unknown')].append((path,rec))
    selected=[]
    for items in groups.values():
        items.sort(key=lambda x:x[1].get('recorded_utc',''),reverse=True)
        selected.extend(items[:limit_per_profile])
    selected.sort(key=lambda x:x[1].get('recorded_utc',''),reverse=True)
    return selected


def inspect_decision_record(path: Path, record: dict) -> dict:
    links=[_inspect_target(x['kind'],x['target'],x.get('sha256')) for x in record.get('links',[])]
    local_evidence=[]
    for e in record.get('evidence',[]):
        candidates=_local_candidates(e.get('source',''))
        if candidates and any(p.exists() and p.is_file() for p in candidates):
            local_evidence.append(_inspect_target('source',e['source'],e.get('sha256')))
    drift=any(x['status']=='CURRENT_BYTES_DRIFTED' for x in links+local_evidence)
    has_commit=any(x.get('kind')=='commit' and x.get('status')=='PRESENT' for x in links)
    missing=any(x['status']=='MISSING' for x in links)
    unresolved=sum(x['status']=='UNRESOLVED_OR_MISSING' for x in links)
    return {
        'record_id':record['record_id'],'profile_id':record['profile_id'],'recorded_utc':record['recorded_utc'],
        'path':str(path.relative_to(REPO)),'record_sha256':sha256_file(path),'schema_valid':True,
        'has_verified_commit_link':has_commit,'historical_byte_drift_without_commit':bool(drift and not has_commit),
        'missing_commit_links':int(missing),'unresolved_local_links':unresolved,
        'link_checks':links,'local_evidence_checks':local_evidence,
    }

def discover_profile_audit_reports() -> list[str]:
    if not AUDIT_ROOT.exists(): return []
    out=[]
    for path in AUDIT_ROOT.rglob('*.json'):
        try:
            data=json.loads(path.read_text(encoding='utf-8'))
        except Exception:
            continue
        if isinstance(data,dict) and data.get('advisory_only') is True and 'target' in data and 'findings' in data and 'proposals' in data:
            out.append(str(path.relative_to(REPO)))
    return sorted(out)


def prepare_packet(profile: str|None=None, limit_per_profile: int=5, audit_id: str|None=None) -> dict:
    audit_id=audit_id or datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-system-quality-audit')
    selected=select_decision_records(profile,limit_per_profile)
    inspections=[inspect_decision_record(path,rec) for path,rec in selected]
    drift=sum(x['historical_byte_drift_without_commit'] for x in inspections)
    unresolved=sum(x['unresolved_local_links'] for x in inspections)
    missing_commits=sum(x['missing_commit_links'] for x in inspections)
    return {
        'packet_version':'1.0','audit_id':audit_id,'created_utc':datetime.now(timezone.utc).isoformat(),
        'sampling':{'profile_filter':profile,'decision_record_limit_per_profile':limit_per_profile,'selected_record_count':len(inspections)},
        'selected_records':inspections,
        'available_profile_audit_reports':discover_profile_audit_reports(),
        'deterministic_summary':{
            'schema_valid_records':len(inspections),
            'records_with_unversioned_historical_byte_drift':drift,
            'unresolved_local_links':unresolved,
            'missing_commit_links':missing_commits,
        },
        'host_review_required':[
            'reasoning_integrity: run reasoning_auditor over the sampled externalizable decision rationale and evidence',
            'profile_performance: run profile_performance_auditor only for completed sessions with real contract/trace/artifact evidence',
        ],
        'privacy_boundary':'Packet contains externalizable records and artifact metadata only; never private chain-of-thought or hidden scratchpads.',
    }


def write_packet(packet: dict, output: Path|None=None) -> Path:
    if output is None:
        date=packet['created_utc'][:10]
        output=AUDIT_ROOT/date/packet['audit_id']/'evidence_packet.json'
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(packet,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return output

def validate_report(report: dict, schema: dict|None=None) -> dict:
    schema=schema or json.loads(REPORT_SCHEMA.read_text(encoding='utf-8'))
    jsonschema.validate(report,schema,format_checker=jsonschema.FormatChecker())
    ev={e['id'] for e in report['evidence']}
    dim_ids=[d['id'] for d in report['dimensions']]
    required={'reasoning_integrity','artifact_code_consistency','profile_performance'}
    if set(dim_ids)!=required or len(dim_ids)!=3:
        raise ValueError('Audit must contain each quality dimension exactly once')
    findings={f['id'] for d in report['dimensions'] for f in d['findings']}
    for d in report['dimensions']:
        if any(x not in ev for x in d['evidence_refs']): raise ValueError('Unknown dimension evidence reference')
        for f in d['findings']:
            if any(x not in ev for x in f['evidence_refs']): raise ValueError('Unknown finding evidence reference')
    for p in report['proposals']:
        if any(x not in findings for x in p['finding_refs']): raise ValueError('Proposal references unknown finding')
    if report['status']=='INSUFFICIENT_EVIDENCE' and report['proposals']:
        raise ValueError('Insufficient evidence cannot support proposals')
    if report['status']=='COMPLETE' and any(d['status'] in {'UNKNOWN','PENDING_HOST_REVIEW'} for d in report['dimensions']):
        raise ValueError('Complete audit cannot contain unresolved dimensions')
    return report


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    mode=ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--prepare',action='store_true')
    mode.add_argument('--validate-report',metavar='JSON')
    ap.add_argument('--profile')
    ap.add_argument('--limit',type=int,default=5)
    ap.add_argument('--audit-id')
    ap.add_argument('--output')
    args=ap.parse_args()
    if args.validate_report:
        validate_report(json.loads(Path(args.validate_report).read_text(encoding='utf-8')))
        print('VALID: evidence-linked advisory system quality audit; no mutation authority.')
        return
    if args.limit < 1 or args.limit > 20: raise SystemExit('--limit must be 1..20')
    packet=prepare_packet(args.profile,args.limit,args.audit_id)
    out=write_packet(packet,Path(args.output) if args.output else None)
    print(out)
    print(json.dumps(packet['deterministic_summary'],indent=2))


if __name__=='__main__': main()
