from pathlib import Path
import json,re
from pypdf import PdfReader
import pdfplumber
ROOT=Path(__file__).resolve().parents[1];PKG=ROOT/'P100_TRANSFER';TMP=ROOT/'tmp/pdf_build'
pdf=PKG/'04_DOCUMENTO/P100_Documento_integral.pdf'
r=PdfReader(pdf);layout=json.loads((TMP/'layout_index.json').read_text(encoding='utf-8'))
texts=[p.extract_text() or '' for p in r.pages]
issues=[]
with pdfplumber.open(pdf) as document:
    for i,page in enumerate(document.pages[:layout['body_pages']]):
        chars=[c for c in page.chars if c.get('text','').strip()]
        outside=[c for c in chars if c['x0']<42 or c['x1']>page.width-42 or c['top']<15 or c['bottom']>page.height-15]
        if outside:issues.append({'page':i+1,'outside_count':len(outside),'sample':''.join(c['text'] for c in outside)[:300]})
        if not chars:issues.append({'page':i+1,'empty':True})
annex_checks=[]
for annex in layout['annexes']:
    original=PdfReader(PKG/'00_ORIGINALES'/annex['title'])
    for i,p in enumerate(original.pages):
        assert (p.extract_text() or '')==texts[annex['page']-1+i],(annex['title'],i)
    annex_checks.append({'source':annex['title'],'pages':len(original.pages),'text_identical':True})
full='\n'.join(texts[:layout['body_pages']])
for needle in ['T01M1','T06M2','T14M2','Ran 38 tests','12.838862164299517','2024-11-09','DESARROLLO_NOPE']:
    if needle=='DESARROLLO_NOPE':continue
    assert needle in full,needle
assert '' not in full
for chapter in layout['chapters']:
    assert chapter['title'] in texts[chapter['page']-1],chapter
links=[]
for p in r.pages[1:3]:
    for an in p.get('/Annots',[]):
        a=an.get_object()
        if a.get('/Subtype')=='/Link':
            dest=a.get('/Dest') or a.get('/A',{}).get('/D')
            links.append(str(dest)[:180])
report={'pages':len(r.pages),'body_pages':layout['body_pages'],'geometry_issues':issues,'annex_checks':annex_checks,'toc_link_annotations':len(links),'source_markers_normalized':True,'chapter_page_checks':'PASS'}
(TMP/'qa_automatic.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
