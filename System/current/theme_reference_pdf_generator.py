#!/usr/bin/env python3
"""Generate a self-demonstrating Theme Reference PDF from a compiled theme module.

The PDF is a visual reference artifact. The theme module remains the machine-readable
source for exact tokens. Unsupported/interactivity-only properties are represented as
specifications rather than silently discarded.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, Flowable,
)

HEX_RE = re.compile(r"^#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})$")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def find_theme(runtime: dict, theme_id: str) -> dict:
    for m in runtime.get("modules", []):
        if m.get("id") == theme_id and m.get("type") == "theme":
            return m
    raise SystemExit(f"Theme module not found: {theme_id}")


def slug_of(theme: dict) -> str:
    tid = str(theme.get("id", "theme.untitled"))
    s = tid.split("theme.", 1)[-1]
    s = re.sub(r"[^a-zA-Z0-9._-]+", "-", s).strip("-.") or "untitled"
    return s


def color_of(value: Any, fallback=colors.HexColor("#111111")):
    if isinstance(value, str) and HEX_RE.match(value.strip()):
        return colors.HexColor(value.strip())
    return fallback


def flatten(obj: Any, prefix=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else str(k)
            yield from flatten(v, key)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from flatten(v, f"{prefix}[{i}]")
    else:
        yield prefix, obj


def deep_get(d: dict, *keys, default=None):
    cur: Any = d
    for key in keys:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def first_hex(mapping: Any, preferred=()):
    if isinstance(mapping, dict):
        for k in preferred:
            v = mapping.get(k)
            if isinstance(v, str) and HEX_RE.match(v): return v
        for _, v in flatten(mapping):
            if isinstance(v, str) and HEX_RE.match(v): return v
    return None


def register_font_assets(theme: dict, root: Path):
    """Return mapping from declared family labels to ReportLab font names + warnings."""
    warnings = []
    font_map = {}
    typography = theme.get("parameters", {}).get("typography", {})
    for path_key, value in flatten(typography):
        if not isinstance(value, str):
            continue
        low = path_key.lower()
        if low.endswith(("font_file", "font_path", ".file", ".path")) and value.lower().endswith((".ttf", ".otf")):
            p = Path(value)
            if not p.is_absolute(): p = root / p
            if p.exists():
                name = "ThemeFont_" + re.sub(r"[^A-Za-z0-9]+", "_", path_key)
                try:
                    pdfmetrics.registerFont(TTFont(name, str(p)))
                    font_map[path_key.rsplit(".",1)[0]] = name
                except Exception as e:
                    warnings.append(f"Font asset could not be embedded: {value} ({e})")
            else:
                warnings.append(f"Declared font asset is missing: {value}")
    families = [(k,v) for k,v in flatten(typography) if isinstance(v,str) and (k.lower().endswith("family") or k.lower().endswith("font_family"))]
    if families and not font_map:
        warnings.append("Declared font families have no embeddable font_file/font_path asset; specimens use a fallback font while preserving the declared family names as tokens.")
    return font_map, warnings


class Swatch(Flowable):
    def __init__(self, hex_value: str, label: str, width=165*mm, height=15*mm):
        super().__init__(); self.hex=hex_value; self.label=label; self.width=width; self.height=height
    def wrap(self, aw, ah): return min(self.width, aw), self.height
    def draw(self):
        w=self._availWidth if hasattr(self,'_availWidth') else self.width
        c=color_of(self.hex)
        self.canv.setFillColor(c); self.canv.roundRect(0,0,min(self.width,w),self.height,3*mm,fill=1,stroke=0)
        # choose black/white text from luminance
        r,g,b=c.red,c.green,c.blue; lum=.2126*r+.7152*g+.0722*b
        self.canv.setFillColor(colors.black if lum>.58 else colors.white)
        self.canv.setFont("Helvetica-Bold",9)
        self.canv.drawString(5*mm,5.3*mm,self.label[:60])
        self.canv.setFont("Helvetica",8)
        self.canv.drawRightString(min(self.width,w)-5*mm,5.3*mm,self.hex.upper())


class ComponentDemo(Flowable):
    def __init__(self, palette: dict, geometry: dict, width=165*mm, height=52*mm):
        super().__init__(); self.p=palette; self.g=geometry; self.width=width; self.height=height
    def wrap(self,aw,ah): return min(self.width,aw),self.height
    def draw(self):
        bg=color_of(first_hex(self.p,("background","canvas","base")) or "#F3F3F3")
        surf=color_of(first_hex(self.p,("surface","panel","card")) or "#FFFFFF")
        text=color_of(first_hex(self.p,("text","foreground","text_primary")) or "#111111")
        accent=color_of(first_hex(self.p,("accent","primary","highlight")) or "#5B5BD6")
        muted=color_of(first_hex(self.p,("muted","secondary","border")) or "#A0A0A0")
        radius=3*mm
        for _,v in flatten(self.g):
            if isinstance(v,(int,float)) and 0 <= v <= 30:
                radius=min(float(v)*0.35*mm, 6*mm); break
        self.canv.setFillColor(bg); self.canv.roundRect(0,0,self.width,self.height,radius,fill=1,stroke=0)
        self.canv.setFillColor(surf); self.canv.roundRect(6*mm,7*mm,95*mm,38*mm,radius,fill=1,stroke=0)
        self.canv.setFillColor(text); self.canv.setFont("Helvetica-Bold",10); self.canv.drawString(11*mm,36*mm,"Component specimen")
        self.canv.setFont("Helvetica",8); self.canv.setFillColor(muted); self.canv.drawString(11*mm,29*mm,"Surface, border, geometry and hierarchy")
        self.canv.setFillColor(accent); self.canv.roundRect(11*mm,14*mm,31*mm,9*mm,radius,fill=1,stroke=0)
        self.canv.setFillColor(colors.white); self.canv.setFont("Helvetica-Bold",7.5); self.canv.drawCentredString(26.5*mm,17.2*mm,"PRIMARY")
        self.canv.setStrokeColor(muted); self.canv.roundRect(47*mm,14*mm,33*mm,9*mm,radius,fill=0,stroke=1)
        self.canv.setFillColor(text); self.canv.drawCentredString(63.5*mm,17.2*mm,"SECONDARY")
        self.canv.setFillColor(accent); self.canv.circle(127*mm,27*mm,13*mm,fill=1,stroke=0)
        self.canv.setFillColor(surf); self.canv.circle(127*mm,27*mm,8*mm,fill=1,stroke=0)


def build_reference(theme: dict, output: Path, root: Path) -> dict:
    params = theme.get("parameters", {}) if isinstance(theme.get("parameters"), dict) else {}
    palette = params.get("palette", {}) if isinstance(params.get("palette"), dict) else {}
    geometry = params.get("geometry", {}) if isinstance(params.get("geometry"), dict) else {}
    typography = params.get("typography", {}) if isinstance(params.get("typography"), dict) else {}
    slug=slug_of(theme); title=theme.get("name") or slug.replace("_"," ").replace("-"," ").title()
    font_map, warnings = register_font_assets(theme, root)
    # Static PDF cannot execute these; describe them.
    if params.get("motion") not in (None,{},[],"inherit"):
        warnings.append("Motion/interaction tokens are documented as specifications; a PDF cannot execute them.")
    bg_hex = first_hex(palette,("background","canvas","base")) or "#F6F6F6"
    text_hex = first_hex(palette,("text_primary","text","foreground")) or "#141414"
    accent_hex = first_hex(palette,("accent","primary","highlight")) or "#5A5AD6"
    surface_hex = first_hex(palette,("surface","panel","card")) or "#FFFFFF"
    doc = SimpleDocTemplate(str(output), pagesize=A4, leftMargin=20*mm,rightMargin=20*mm,topMargin=18*mm,bottomMargin=18*mm, title=f"Theme Reference - {title}")
    styles={
      'title': ParagraphStyle('title',fontName='Helvetica-Bold',fontSize=28,leading=31,textColor=color_of(text_hex),spaceAfter=10),
      'h1': ParagraphStyle('h1',fontName='Helvetica-Bold',fontSize=17,leading=21,textColor=color_of(text_hex),spaceBefore=8,spaceAfter=7),
      'h2': ParagraphStyle('h2',fontName='Helvetica-Bold',fontSize=11,leading=14,textColor=color_of(accent_hex),spaceBefore=5,spaceAfter=4),
      'body': ParagraphStyle('body',fontName='Helvetica',fontSize=9.3,leading=13,textColor=color_of(text_hex),spaceAfter=5),
      'small': ParagraphStyle('small',fontName='Helvetica',fontSize=7.6,leading=10,textColor=colors.HexColor('#666666'),spaceAfter=3),
      'mono': ParagraphStyle('mono',fontName='Courier',fontSize=6.8,leading=9,textColor=color_of(text_hex),spaceAfter=2),
    }
    story=[]
    story += [Spacer(1,18*mm), Paragraph("THEME REFERENCE", styles['small']), Paragraph(title,styles['title']), Paragraph(f"<b>Module:</b> {theme.get('id','theme.untitled')}",styles['body'])]
    fidelity = "STATIC VISUAL EXACT" if not warnings else "STATIC VISUAL PARTIAL"
    story += [Paragraph(f"<b>Fidelity status:</b> {fidelity}",styles['body'])]
    if theme.get("purpose"): story += [Paragraph(theme['purpose'],styles['body'])]
    story += [Spacer(1,6*mm), ComponentDemo(palette,geometry), Spacer(1,8*mm)]
    if warnings:
        story += [Paragraph("Fidelity notes",styles['h2'])]
        for w in warnings: story += [Paragraph("- "+w,styles['small'])]
    story += [PageBreak(),Paragraph("Palette",styles['h1'])]
    swatches=[]
    for k,v in flatten(palette):
        if isinstance(v,str) and HEX_RE.match(v): swatches.append((k,v))
    if swatches:
        for k,v in swatches: story += [Swatch(v,k),Spacer(1,3*mm)]
    else: story += [Paragraph("No explicit hex color tokens were compiled; colors inherit or remain unspecified.",styles['body'])]

    story += [PageBreak(),Paragraph("Typography",styles['h1'])]
    if typography:
        declared_family=None
        for k,v in flatten(typography):
            if isinstance(v,str) and (k.lower().endswith("family") or k.lower().endswith("font_family")):
                declared_family=v; break
        story += [Paragraph(f"Declared family: <b>{declared_family or 'inherit / unspecified'}</b>",styles['body'])]
        # Use first embedded font if available, else fallback.
        specimen_font = next(iter(font_map.values()), 'Helvetica')
        specimen = ParagraphStyle('specimen',fontName=specimen_font,fontSize=20,leading=25,textColor=color_of(text_hex),spaceAfter=8)
        story += [Paragraph("Aa Bb Cc 0123 - The quick brown fox", specimen)]
        for k,v in flatten(typography): story += [Paragraph(f"<b>{k}</b>: {v}",styles['small'])]
    else: story += [Paragraph("Typography inherits from the parent/default theme.",styles['body'])]

    story += [PageBreak(),Paragraph("Spacing, geometry & surfaces",styles['h1'])]
    for group_name in ("spacing","geometry","surfaces"):
        group=params.get(group_name)
        story += [Paragraph(group_name.title(),styles['h2'])]
        if group in (None,{},[],"inherit"): story += [Paragraph("inherit / unspecified",styles['small'])]
        else:
            for k,v in flatten(group): story += [Paragraph(f"<b>{k}</b>: {v}",styles['small'])]
    story += [Spacer(1,5*mm),ComponentDemo(palette,geometry)]

    extras=[g for g in ("components","iconography","imagery","motion") if params.get(g) not in (None,{},[],"inherit")]
    if extras:
        story += [PageBreak(),Paragraph("Optional design systems",styles['h1'])]
        for group_name in extras:
            story += [Paragraph(group_name.title(),styles['h2'])]
            for k,v in flatten(params[group_name]): story += [Paragraph(f"<b>{k}</b>: {v}",styles['small'])]

    story += [PageBreak(),Paragraph("Inheritance, exclusions & complete token appendix",styles['h1'])]
    for field in ("scope","inheritance","exclusions"):
        v=theme.get(field)
        if v is not None: story += [Paragraph(f"<b>{field.title()}:</b> {v}",styles['body'])]
    token_json=json.dumps(params,indent=2,ensure_ascii=False)
    for line in token_json.splitlines():
        esc=line.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
        story += [Paragraph(esc.replace(' ','&nbsp;'),styles['mono'])]

    def on_page(canvas, doc_):
        canvas.saveState(); canvas.setFillColor(color_of(bg_hex)); canvas.rect(0,0,A4[0],A4[1],fill=1,stroke=0)
        canvas.setFillColor(color_of(accent_hex)); canvas.rect(0,A4[1]-3*mm,A4[0],3*mm,fill=1,stroke=0)
        canvas.setFillColor(color_of(text_hex)); canvas.setFont('Helvetica',7); canvas.drawRightString(A4[0]-12*mm,8*mm,f"{title}  /  {doc_.page}")
        canvas.restoreState()
    output.parent.mkdir(parents=True,exist_ok=True)
    doc.build(story,onFirstPage=on_page,onLaterPages=on_page)
    return {'output':str(output),'theme_id':theme.get('id'),'fidelity':fidelity,'warnings':warnings,'pages_hint':'dynamic'}


def main():
    ap=argparse.ArgumentParser()
    src=ap.add_mutually_exclusive_group(required=True)
    src.add_argument('--theme-json',help='Standalone compiled theme module JSON')
    src.add_argument('--runtime',help='Runtime config containing the theme module')
    ap.add_argument('--theme-id',help='Required with --runtime, e.g. theme.retro_industrial')
    ap.add_argument('--output',help='Output PDF path; defaults to Themes/<slug>/Theme_Reference_<slug>.pdf')
    ap.add_argument('--module-snapshot',help='Optional paired theme-module JSON path; defaults beside the PDF as theme.<slug>.json')
    ap.add_argument('--report-json',help='Optional fidelity report path')
    args=ap.parse_args()
    root=Path.cwd()
    if args.theme_json:
        theme=load_json(Path(args.theme_json))
    else:
        if not args.theme_id: ap.error('--theme-id is required with --runtime')
        theme=find_theme(load_json(Path(args.runtime)),args.theme_id)
    slug=slug_of(theme)
    out=Path(args.output) if args.output else root/'Themes'/slug/f'Theme_Reference_{slug}.pdf'
    result=build_reference(theme,out,root)
    snapshot = Path(args.module_snapshot) if args.module_snapshot else out.parent / f"theme.{slug}.json"
    snapshot.parent.mkdir(parents=True, exist_ok=True)
    snapshot.write_text(json.dumps(theme, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    result["module_snapshot"] = str(snapshot)
    if args.report_json: Path(args.report_json).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
