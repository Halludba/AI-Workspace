"""Reconstruct categorized release into a new working folder; never overwrite."""
import argparse,json,shutil
from pathlib import Path

def main():
    ap=argparse.ArgumentParser();ap.add_argument('destination');a=ap.parse_args()
    bundle=Path(__file__).resolve().parent.parent
    cfg=json.loads((bundle/'03 PDF System/State/pdf_system_config.json').read_text(encoding='utf-8'))
    dest=Path(a.destination).resolve()
    if dest.exists(): raise SystemExit('Choose a new destination; existing folders are preserved.')
    entries=[]
    for item in cfg['artifacts']:
        src=(bundle/item.get('bundle_folder','')/Path(item['path']).name).resolve()
        out=(dest/item['path']).resolve()
        if not src.is_relative_to(bundle) or not out.is_relative_to(dest):raise SystemExit('Unsafe manifest path')
        if src.is_file():entries.append((src,out))
        elif item['classification']=='REQUIRED':raise SystemExit('Missing required artifact: '+str(src))
    dest.mkdir(parents=True)
    for src,out in entries:
        out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,out)
    print('Materialized:',dest)
    print('Run python pdf_system_engine.py from that folder after installing requirements.txt.')
if __name__=='__main__':main()
