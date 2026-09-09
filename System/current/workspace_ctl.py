#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
from pdf_engine.state import resolve_root
from pdf_engine.latency import compact_topic_context, recent_latency, refresh_context_files
from pdf_engine.testing import run_regression_suite

ROOT=Path(__file__).resolve().parent
CONFIG=ROOT/'pdf_system_config.json'


def load_runtime():
    return (json.loads((ROOT/'ai_runtime_config.json').read_text(encoding='utf-8')),
            json.loads((ROOT/'ai_runtime_state.json').read_text(encoding='utf-8')))


def cmd_refresh(quiet: bool=False):
    root,state,_=resolve_root(CONFIG); cfg,rt=load_runtime()
    refresh_context_files(root,state,cfg,rt)
    if not quiet: print('PASS: context index refreshed')


def cmd_context(topic: str):
    cmd_refresh(True)
    print(json.dumps(compact_topic_context(ROOT,topic),indent=2,ensure_ascii=False))

def cmd_status():
    cfg,rt=load_runtime()
    p=subprocess.run(['git','status','--short','--branch'],cwd=str(ROOT.parent.parent),text=True,capture_output=True)
    print(json.dumps({'release':cfg.get('release_version'),'profile':rt.get('current_profile'),'phase':rt.get('phase'),'git':(p.stdout or '').strip().splitlines()[:8]},indent=2))


def cmd_verify(scope: str | None):
    cfg,_=load_runtime()
    if scope:
        spec=cfg.get('latency_policy',{}).get('context_topics',{}).get(scope)
        if not spec: raise SystemExit(f'Unknown scope: {scope}')
        ok,out=run_regression_suite(ROOT,'regression_test_report.txt',test_files=spec.get('tests',[]))
    else:
        ok,out=run_regression_suite(ROOT,'regression_test_report.txt')
    print(out,end='')
    raise SystemExit(0 if ok else 6)


def cmd_metrics(limit: int):
    print(json.dumps({'runs':recent_latency(ROOT,limit)},indent=2))

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True)
    sub.add_parser('refresh')
    p=sub.add_parser('context'); p.add_argument('topic')
    sub.add_parser('status')
    p=sub.add_parser('verify'); p.add_argument('--scope')
    p=sub.add_parser('metrics'); p.add_argument('--limit',type=int,default=10)
    a=ap.parse_args()
    if a.cmd=='refresh': cmd_refresh()
    elif a.cmd=='context': cmd_context(a.topic)
    elif a.cmd=='status': cmd_status()
    elif a.cmd=='verify': cmd_verify(a.scope)
    elif a.cmd=='metrics': cmd_metrics(a.limit)

if __name__=='__main__': main()
