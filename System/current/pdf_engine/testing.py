from __future__ import annotations
import subprocess, sys
from pathlib import Path

def run_regression_suite(root: Path, report_name: str = "regression_test_report.txt") -> tuple[bool, str]:
    cmd=[sys.executable,"-m","unittest","discover","-s","pdf_engine/tests","-p","test_*.py","-v"]
    p=subprocess.run(cmd,cwd=str(root),text=True,capture_output=True)
    output=(p.stdout or "")+(p.stderr or "")
    report=root/report_name
    report.write_text("REGRESSION / MUTATION SIMULATION PREFLIGHT\n\n"+output,encoding="utf-8")
    return p.returncode==0, output
