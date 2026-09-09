from __future__ import annotations
import hashlib, json, re, time
from pathlib import Path
import fitz
from .common import write_json


def pdf_structural_hash(path: Path) -> str:
    doc = fitz.open(path)
    pages = []
    for page in doc:
        norm = []
        for w in page.get_text('words'):
            x0,y0,x1,y1,text,*_ = w
            norm.append((round(x0,1),round(y0,1),round(x1,1),round(y1,1),text))
        pages.append(norm)
    return hashlib.sha256(json.dumps(pages,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()


def _page_structural_hash(page) -> str:
    words=[]
    for w in page.get_text('words'):
        x0,y0,x1,y1,text,*_=w
        words.append((round(x0,1),round(y0,1),round(x1,1),round(y1,1),text))
    return hashlib.sha256(json.dumps(words,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def text_of_pdf(path: Path) -> str:
    with fitz.open(path) as doc:
        return '\n'.join(p.get_text() for p in doc)


def render_and_preflight(root: Path) -> tuple[list[str], float]:
    t=time.time(); issues=[]
    cache_dir=root/'.runtime_cache'; cache_dir.mkdir(exist_ok=True)
    cache_path=cache_dir/'pdf_verify_cache.json'
    try: cache=json.loads(cache_path.read_text(encoding='utf-8'))
    except Exception: cache={}
    for rel,outdir in [('Formats.pdf','_pdf_system_verify_formats'),('PDF_Workflow.pdf','_pdf_system_verify_workflow')]:
        pdf=root/rel; rd=root/outdir; rd.mkdir(exist_ok=True)
        with fitz.open(pdf) as doc:
            hashes=[_page_structural_hash(p) for p in doc]
            prev=cache.get(rel,{}).get('page_hashes',[])
            changed={i for i,h in enumerate(hashes) if i>=len(prev) or prev[i]!=h}
            if len(prev)!=len(hashes): changed=set(range(len(hashes)))
            render=set(changed)
            for i in list(changed):
                if i>0: render.add(i-1)
                if i+1<len(hashes): render.add(i+1)
            for i,page in enumerate(doc):
                for x0,y0,x1,y1,word,*_ in page.get_text('words'):
                    if x0 < -0.5 or y0 < -0.5 or x1 > page.rect.width+0.5 or y1 > page.rect.height+0.5:
                        issues.append(f'{rel} page {i+1}: text outside page: {word}')
                if i in render:
                    page.get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(rd/f'page-{i+1:03}.png')
            cache[rel]={'page_hashes':hashes,'changed_pages':[i+1 for i in sorted(changed)],'rendered_pages':[i+1 for i in sorted(render)]}
        note='Changed pages: '+(', '.join(map(str,cache[rel]['changed_pages'])) if cache[rel]['changed_pages'] else 'none')
        note+='\nRendered pages: '+(', '.join(map(str,cache[rel]['rendered_pages'])) if cache[rel]['rendered_pages'] else 'none (unchanged)')
        (root/f'{Path(rel).stem}_preflight.txt').write_text(note+'\nText bounds checked on all pages. Visual inspection by reasoning host required only for changed/rendered pages.\n'+'\n'.join(issues),encoding='utf-8')
    write_json(cache_path,cache)
    return issues,time.time()-t


def clean_pdf_markdown(pdf: Path, title: str) -> str:
    raw=text_of_pdf(pdf).splitlines()
    out=[f'# {title}','','> AI-optimized derived text view. The source PDF remains authoritative for rule meaning and visual layout.','']
    header_re=re.compile(r'^(Formats\.pdf - Master PDF Generation Specification|PDF Workflow - Operational Execution Procedure)\s+\d+$')
    heading_re=re.compile(r'^(\d+(?:\.\d+)*(?:\.[ivx]+)?)\s+(.+)$',re.I)
    for line in raw:
        s=line.strip()
        if not s or header_re.match(s) or re.fullmatch(r'\d+',s): continue
        m=heading_re.match(s)
        if m:
            ident=m.group(1); depth=min(5,1+ident.count('.'))
            out += ['', '#'*depth+' '+s, '']
        else: out.append(s)
    return '\n'.join(out).strip()+'\n'
