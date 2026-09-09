#!/usr/bin/env python3
"""Thin CLI for the modular Recursive AI Config / Formats PDF engine."""
from __future__ import annotations
import argparse
from pathlib import Path
from pdf_engine.common import DEFAULT_ROOT, CONFIG_NAME
from pdf_engine.state import resolve_root, export_generated_python
from pdf_engine.orchestrator import sync, status, export_portable
from pdf_engine.testing import run_regression_suite


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--config',default=str(DEFAULT_ROOT/CONFIG_NAME))
    ap.add_argument('--from-python',action='store_true')
    ap.add_argument('--to-python',action='store_true')
    ap.add_argument('--status',action='store_true')
    ap.add_argument('--test',action='store_true')
    ap.add_argument('--export-portable',action='store_true')
    args=ap.parse_args(); cfg=Path(args.config).resolve()
    if args.status: return status(cfg)
    if args.export_portable: return export_portable(cfg)
    root,state,_=resolve_root(cfg)
    if args.test:
        ok,out=run_regression_suite(root,state.get('testing',{}).get('report','regression_test_report.txt'))
        print(out,end=''); return 0 if ok else 6
    if args.to_python:
        print(export_generated_python(root,state)); return 0
    return sync(cfg,args.from_python)


if __name__=='__main__':
    raise SystemExit(main())
