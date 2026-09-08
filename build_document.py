from pathlib import Path
import re,html,json,math,textwrap,unicodedata
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,PageBreak,Table,TableStyle,XPreformatted,KeepTogether
from reportlab.platypus.tableofcontents import TableOfContents
from pypdf import PdfReader,PdfWriter

ROOT=Path(__file__).resolve().parents[1];PKG=ROOT/'P100_TRANSFER';OUT=PKG/'04_DOCUMENTO';OUT.mkdir(exist_ok=True)
TMP=ROOT/'tmp/pdf_build';TMP.mkdir(exist_ok=True)
FONTS=Path('C:/Windows/Fonts')
for name,file in [('Body','arial.ttf'),('BodyBold','arialbd.ttf'),('BodyItalic','ariali.ttf'),('Mono','consola.ttf'),('Symbols','seguisym.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONTS/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='BodyItalic',boldItalic='BodyBold')
W,H=A4; M=49; WIDTH=W-2*M
styles={
    'body':ParagraphStyle('body',fontName='Body',fontSize=10.1,leading=14.1,spaceAfter=7,textColor=colors.black,splitLongWords=True),
    'h1':ParagraphStyle('h1',fontName='BodyBold',fontSize=19,leading=24,spaceBefore=15,spaceAfter=13,keepWithNext=True),
    'h2':ParagraphStyle('h2',fontName='BodyBold',fontSize=13,leading=17,spaceBefore=14,spaceAfter=8,keepWithNext=True),
    'h3':ParagraphStyle('h3',fontName='BodyBold',fontSize=10.6,leading=14,spaceBefore=10,spaceAfter=6,keepWithNext=True),
    'small':ParagraphStyle('small',fontName='Body',fontSize=8.2,leading=11,spaceAfter=6,splitLongWords=True),
    'cell':ParagraphStyle('cell',fontName='Body',fontSize=8.1,leading=10.5,spaceAfter=0,splitLongWords=True),
    'code':ParagraphStyle('code',fontName='Mono',fontSize=8,leading=10.2,spaceAfter=0,leftIndent=8,rightIndent=8),
    'quote':ParagraphStyle('quote',fontName='BodyItalic',fontSize=10,leading=14,leftIndent=13,spaceAfter=7),
}

unrendered=set()
def normalized(s):
    return s.replace('\u2011','-').replace('\u2013','-').replace('\u2014','-').replace('\u2212','-').replace('\xa0',' ')
def safe(s,base='Body'):
    out=[];primary=pdfmetrics.getFont(base).face.charWidths;secondary=pdfmetrics.getFont('Symbols').face.charWidths
    for ch in normalized(s):
        cp=ord(ch)
        if cp>0xFFFF:
            unrendered.add(f'U+{cp:04X}');out.append(f'[U+{cp:04X}]')
        elif ch in '\r\n\t' or cp in primary:out.append(html.escape(ch))
        elif cp in secondary:out.append('<font name="Symbols">'+html.escape(ch)+'</font>')
        elif cp in (0xfe0f,0xfe0e,0x200d):continue
        else:
            unrendered.add(f'U+{cp:04X}');out.append(f'[U+{cp:04X}]')
    return ''.join(out)

def reading_text(s):
    s=re.sub(r'filecite(.*?)',lambda m:'[referencia de archivo original '+m.group(1).replace('',' ')+', no resuelta]',s)
    s=re.sub(r'cite(.*?)',lambda m:'[referencia web original '+m.group(1).replace('',' ')+', no resuelta]',s)
    s=re.sub(r':chatgpt-content-reference\{index="(\d+)"\}',r'[archivo histórico referenciado con índice \1, no recuperado]',s)
    return s
def inline(s):
    s=reading_text(s)
    chunks=re.split(r'(`[^`]+`|\*\*[^*]+\*\*)',s)
    out=[]
    for c in chunks:
        if c.startswith('`') and c.endswith('`'):out.append('<font name="Mono" size="9">'+safe(c[1:-1],'Mono')+'</font>')
        elif c.startswith('**') and c.endswith('**'):out.append('<b>'+safe(c[2:-2])+'</b>')
        else:
            c=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',lambda m:m.group(1)+' ('+m.group(2)+')',c)
            out.append(safe(c))
    return ''.join(out)

def para(s,style='body'):return Paragraph(inline(s),styles[style])

def code_block(source):
    lines=[]
    for line in source.expandtabs(4).splitlines():
        if not line:lines.append(' ');continue
        # Visual line wrap only; original source file retains exact bytes.
        width=91
        while len(line)>width:
            lines.append(line[:width]);line='    '+line[width:]
        lines.append(line)
    return [Spacer(1,5),XPreformatted('\n'.join(safe(x,'Mono') for x in lines),styles['code']),Spacer(1,9)]

def table(rows):
    if not rows:return []
    n=max(map(len,rows));rows=[r+['']*(n-len(r)) for r in rows]
    if n>7:
        return code_block('\n'.join(' | '.join(r) for r in rows))
    weights=[]
    for c in range(n):
        typical=sum(min(len(r[c]),65) for r in rows)/len(rows)
        weights.append(max(9,min(35,typical)))
    if n==2:weights=[max(15,min(24,weights[0])),45]
    widths=[WIDTH*w/sum(weights) for w in weights]
    data=[[Paragraph(inline(v),styles['cell']) for v in row] for row in rows]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#D9D9D9')),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#DCE6F0')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F7F8FA')])]))
    return [t,Spacer(1,9)]

def parse(md,heading_shift=0):
    lines=md.splitlines();out=[];i=0
    while i<len(lines):
        line=lines[i].rstrip()
        if not line.strip():i+=1;continue
        if line.startswith('```'):
            block=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):block.append(lines[i]);i+=1
            out+=code_block('\n'.join(block));i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                row=lines[i].strip().strip('|').split('|')
                if not all(re.fullmatch(r'\s*:?-+:?\s*',v) for v in row):rows.append([v.strip() for v in row])
                i+=1
            out+=table(rows);continue
        m=re.match(r'^(#{1,6})\s+(.+)',line)
        if m:
            level=min(3,len(m.group(1))+heading_shift)
            out.append(para(m.group(2),f'h{level}'));i+=1;continue
        if re.fullmatch(r'\s*[-_*]{3,}\s*',line):out.append(Spacer(1,7));i+=1;continue
        if line.strip() in ('\\[','$$'):
            end='\\]' if line.strip()=='\\[' else '$$';b=[];i+=1
            while i<len(lines) and lines[i].strip()!=end:b.append(lines[i]);i+=1
            out.append(para('Expresión matemática conservada en la notación del mensaje original','small'));out+=code_block('\n'.join(b));i+=1;continue
        m=re.match(r'^\s*(?:[-*]|\d+[.)])\s+(.+)',line)
        if m:
            out.append(para('• '+m.group(1)));i+=1;continue
        if line.startswith('>'):
            out.append(para(line.lstrip('> '),'quote'));i+=1;continue
        block=[line];i+=1
        while i<len(lines) and lines[i].strip() and not re.match(r'^(#|```|\||>|[-*] |\d+[.)] |\\\[)',lines[i]):
            block.append(lines[i]);i+=1
        out.append(para(' '.join(block)))
    return out

class Dossier(BaseDocTemplate):
    def __init__(self,path,**kw):
        super().__init__(path,pagesize=A4,leftMargin=M,rightMargin=M,topMargin=48,bottomMargin=47,**kw)
        frame=Frame(M,47,WIDTH,H-95,id='body',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
        self.addPageTemplates(PageTemplate(id='main',frames=frame,onPage=self.page))
        self.entries=[]
    def beforeDocument(self):self.entries=[]
    def page(self,canvas,doc):
        canvas.saveState();canvas.setFont('Body',8);canvas.setFillColor(colors.HexColor('#505B67'))
        canvas.drawString(M,H-29,'P100   /   Transferencia del proyecto   /   Patrick y Atlas')
        canvas.drawString(M,27,'Expediente de investigación | Fuentes y estados de evidencia explícitos')
        canvas.drawRightString(W-M,27,str(doc.page));canvas.restoreState()
    def afterFlowable(self,flow):
        if isinstance(flow,Paragraph) and flow.style.name=='h1':
            txt=flow.getPlainText();key='chapter_'+str(len(self.entries))
            self.canv.bookmarkPage(key);self.canv.addOutlineEntry(txt,key,0,False)
            self.notify('TOCEntry',(0,txt,self.pageNumber if hasattr(self,'pageNumber') else self.canv.getPageNumber(),key))
            self.entries.append({'title':txt,'page':self.canv.getPageNumber()})

def chapter(title,md):
    return [PageBreak(),para(title,'h1')]+parse(re.sub(r'^# .*\n','',md,count=1),heading_shift=1)

files=[
('Alcance y cobertura','02_EVIDENCIA/COBERTURA_Y_FALTANTES.md'),
('Contexto maestro de P100','01_CONTEXTO/PROJECT_CONTEXT.md'),
('Patrick y Atlas','01_CONTEXTO/EQUIPO_Y_ATLAS.md'),
('La guía original y su auditoría','02_EVIDENCIA/AUDITORIA_PDF.md'),
('Decisiones y evolución técnica','01_CONTEXTO/DECISIONS.md'),
('Registro de experimentos históricos','01_CONTEXTO/EXPERIMENT_LOG.md'),
('Problemas conocidos','01_CONTEXTO/KNOWN_ISSUES.md'),
('Roadmap de v0 6','01_CONTEXTO/ROADMAP.md'),
('Cambios y pruebas de esta transferencia','01_CONTEXTO/CAMBIOS_ACTUALES.md'),
('Arranque para continuar en Codex','03_ARRANQUE/START_HERE.md'),
('Solicitudes de Patrick en esta tarea','00_ORIGINALES/SOLICITUDES_DE_ESTA_TAREA.md'),
]
story=[Spacer(1,45),Paragraph('P100',ParagraphStyle('cover',fontName='BodyBold',fontSize=36,leading=42,spaceAfter=16)),Paragraph('Documento integral del proyecto cuantitativo',ParagraphStyle('title',fontName='BodyBold',fontSize=23,leading=29,spaceAfter=23)),para('Transferencia para Codex y lectura del equipo'),para('Preparado para Patrick | Atlas, asistente de inteligencia artificial de OpenAI'),para('7 de septiembre de 2026 | Costa Rica'),Spacer(1,25),para('Este documento reúne el contexto del proyecto, las decisiones y resultados declarados desde v0.1 hasta v0.5, el roadmap de v0.6, la conversación recuperada, el código nuevo y sus pruebas. Los dos PDF originales se conservan íntegros como anexos.'),para('La base nueva pasó 38 pruebas. Los backtests históricos no se han reproducido: faltan sus ZIP y CSV, y una respuesta del chat llega recortada. Cada sección distingue fuentes, resultados declarados, verificaciones actuales y propuestas.'),Spacer(1,14),para('Lectura recomendada: empezar por alcance y cobertura; después contexto y experimentos. Usar el índice y los marcadores del PDF para acudir a las fuentes y al código.','small'),PageBreak(),Paragraph('Índice de lectura',styles['h2'])]
toc=TableOfContents();toc.levelStyles=[ParagraphStyle('toc',fontName='Body',fontSize=10,leading=14,spaceBefore=5,leftIndent=0,firstLineIndent=0)];story+=[toc]
combined=['# P100 Documento integral del proyecto cuantitativo','\nVersión editable. Los binarios de ambos PDF se conservan en 00_ORIGINALES. En esta edición textual sus extracciones se incorporan al final; el PDF de lectura anexa los originales con diseño íntegro.\n']
for title,path in files:
    md=(PKG/path).read_text(encoding='utf-8');story+=chapter(title,md);combined+=['\n# '+title,md]

trans=(PKG/'00_ORIGINALES/conversacion_recuperada/TRANSCRIPCION_LITERAL.md').read_text(encoding='utf-8')
story += [PageBreak(),para('Conversación histórica recuperada','h1'),para('Se conserva todo el texto obtenido. Las citas internas inaccesibles se representan con etiquetas explicativas. El archivo literal y los JSON preservan los marcadores exactos. Las expresiones matemáticas en notación del chat se muestran como texto de archivo. Las afirmaciones «ejecuté» o «funciona» pertenecen al asistente histórico y no implican una reejecución en esta transferencia.')]
parts=re.split(r'(?m)^# (T\d+ Turno histórico)\n',trans)
story+=parse(parts[0],heading_shift=1)
for i in range(1,len(parts),2):story += [PageBreak(),para(parts[i],'h1')]+parse(parts[i+1],heading_shift=1)
combined+=['\n# Conversación histórica recuperada',trans]

codebase=PKG/'05_CODIGO/v06_foundations'
story+=[PageBreak(),para('Código nuevo de la base v0 6','h1')]
for file in ['README.md','CHANGELOG.md','TEST_REPORT.md']:
    md=(codebase/file).read_text(encoding='utf-8');story+=parse(md,heading_shift=1);combined+=['\n# Base nueva '+file,md]
source_files=sorted(p for p in codebase.rglob('*') if p.suffix=='.py')+[codebase/'config/example.json',codebase/'FREEZE_MANIFEST.json',codebase/'test_run.log',codebase/'freeze_verify.log']
for path in source_files:
    rel=path.relative_to(codebase).as_posix();content=path.read_text(encoding='utf-8')
    story += [para(rel,'h2')]+code_block(content);combined+=['\n## '+rel,'```text\n'+content+'\n```']

story+=[PageBreak(),para('Verificaciones de las fuentes PDF','h1')]
for filename in ['verify_pdf_sources.py','verification.log']:
    content=(PKG/'06_VERIFICACION/pdf_checks'/filename).read_text(encoding='utf-8');story+=[para(filename,'h2')]+code_block(content);combined+=['\n## '+filename,'```text\n'+content+'\n```']
story+=[PageBreak(),para('Anexos originales','h1'),para('Las páginas que siguen reproducen los binarios originales, en este orden: PDFM1000v2.pdf, 35 páginas; PDFM1000.pdf, 14 páginas. Cada original conserva su numeración y diseño. Los marcadores del documento permiten abrir cada anexo. Las páginas originales contienen errores y afirmaciones históricas que se analizan en la auditoría; su preservación no equivale a confirmarlas.'),para('Para datos numéricos estructurados, diferencias de extracción completas e inventario, consultar los JSON y CSV incluidos en el paquete. Ningún archivo de mercado ha sido sustituido por datos generados.'),para('Los scripts que construyen la presentación del documento no forman parte del motor cuantitativo. Los scripts de investigación y verificación sí están incluidos con sus resultados.')]

doc=Dossier(str(TMP/'body.pdf'),title='P100 Documento integral del proyecto cuantitativo',author='Atlas para Patrick')
doc.multiBuild(story)
reader=PdfReader(TMP/'body.pdf');writer=PdfWriter();writer.append(reader)
offset=len(reader.pages);annex=[]
for name in ['PDFM1000v2.pdf','PDFM1000.pdf']:
    source=PdfReader(PKG/'00_ORIGINALES'/name);annex.append({'title':name,'page':offset+1,'pages':len(source.pages)})
    writer.append(source,outline_item=name);offset+=len(source.pages)
writer.add_metadata({'/Title':'P100 Documento integral del proyecto cuantitativo','/Author':'Atlas para Patrick','/Subject':'Transferencia de contexto con evidencia y código nuevo separado'})
with (OUT/'P100_Documento_integral.pdf').open('wb') as handle:writer.write(handle)
for name in ['PDFM1000v2','PDFM1000']:
    combined+=['\n# Extracción por páginas del original '+name]
    for page in json.loads((PKG/'06_VERIFICACION/pdf_checks'/f'{name}_pages.json').read_text(encoding='utf-8')):combined+=['\n## Página original '+str(page['page']),page['text']]
(OUT/'P100_Documento_integral.md').write_text('\n'.join(combined),encoding='utf-8')
report={'body_pages':len(reader.pages),'total_pages':offset,'chapters':doc.entries,'annexes':annex,'unicode_fallbacks':sorted(unrendered)}
(TMP/'layout_index.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
