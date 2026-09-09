from __future__ import annotations
import hashlib, json, re, shutil, subprocess, sys, time
from pathlib import Path
import fitz


def pdf_structural_hash(path: Path) -> str:
    doc = fitz.open(path)
    pages = []
    for page in doc:
        norm = []
        for w in page.get_text('words'):
            x0, y0, x1, y1, text, *_ = w
            norm.append((round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1), text))
        pages.append(norm)
    return hashlib.sha256(json.dumps(pages, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


def text_of_pdf(path: Path) -> str:
    with fitz.open(path) as doc:
        return '\n'.join(p.get_text() for p in doc)


def render_and_preflight(root: Path) -> tuple[list[str], float]:
    t = time.time(); issues = []
    for rel, outdir in [('Formats.pdf', '_pdf_system_verify_formats'), ('PDF_Workflow.pdf', '_pdf_system_verify_workflow')]:
        pdf = root / rel; rd = root / outdir
        rd.mkdir(exist_ok=True)
        with fitz.open(pdf) as doc:
            for i,page in enumerate(doc):
                page.get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(rd / f'page-{i+1:03}.png')
                for x0,y0,x1,y1,word,*_ in page.get_text('words'):
                    if x0 < -0.5 or y0 < -0.5 or x1 > page.rect.width+0.5 or y1 > page.rect.height+0.5:
                        issues.append(f'{rel} page {i+1}: text outside page: {word}')
        (root / f'{Path(rel).stem}_preflight.txt').write_text('All pages rendered. Text bounds checked. Visual inspection by reasoning host required.\n'+'\n'.join(issues),encoding='utf-8')
    return issues, time.time() - t


def clean_pdf_markdown(pdf: Path, title: str) -> str:
    raw = text_of_pdf(pdf).splitlines()
    out = [f'# {title}', '', '> AI-optimized derived text view. The source PDF remains authoritative for rule meaning and visual layout.', '']
    header_re = re.compile(r'^(Formats\.pdf - Master PDF Generation Specification|PDF Workflow - Operational Execution Procedure)\s+\d+$')
    heading_re = re.compile(r'^(\d+(?:\.\d+)*(?:\.[ivx]+)?)\s+(.+)$', re.I)
    for line in raw:
        s = line.strip()
        if not s or header_re.match(s) or re.fullmatch(r'\d+', s): continue
        m = heading_re.match(s)
        if m:
            ident = m.group(1); depth = min(5, 1 + ident.count('.'))
            out += ['', '#' * depth + ' ' + s, '']
        else:
            out.append(s)
    return '\n'.join(out).strip() + '\n'
