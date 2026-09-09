"""Validate and append privacy-safe decision-rationale records.

This stores externalizable decision summaries, never private chain-of-thought.
Records are append-only; corrections create a superseding record.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parent
SCHEMA = ROOT / 'decision_record_schema.json'
FORBIDDEN_KEYS = {'chain_of_thought','private_reasoning','hidden_reasoning','scratchpad','cot'}

def load_schema():
    return json.loads(SCHEMA.read_text(encoding='utf-8'))

def _walk_keys(value):
    if isinstance(value, dict):
        for k,v in value.items():
            yield str(k).lower()
            yield from _walk_keys(v)
    elif isinstance(value, list):
        for v in value: yield from _walk_keys(v)

def validate_record(record, schema=None):
    jsonschema.validate(record, schema or load_schema(), format_checker=jsonschema.FormatChecker())
    bad = FORBIDDEN_KEYS.intersection(_walk_keys(record))
    if bad: raise ValueError('Forbidden private-reasoning field(s): '+', '.join(sorted(bad)))
    return record

def record_path(record):
    profile = re.sub(r'[^A-Za-z0-9._-]+','_', record['profile_id']).strip('._') or 'unknown'
    date = record['recorded_utc'][:10]
    rid = record['record_id']
    base = (ROOT / 'decision_records').resolve()
    out = (base / profile / date / f'{rid}.json').resolve()
    out.relative_to(base)
    return out

def write_record(record):
    validate_record(record)
    out = record_path(record)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists():
        raise FileExistsError('Append-only decision record already exists: '+str(out))
    out.write_text(json.dumps(record, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    return out

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    mode=ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--validate', metavar='JSON')
    mode.add_argument('--write', metavar='JSON')
    args=ap.parse_args()
    path=Path(args.validate or args.write)
    record=json.loads(path.read_text(encoding='utf-8'))
    if args.validate:
        validate_record(record); print('VALID')
    else:
        print(write_record(record))

if __name__=='__main__': main()
