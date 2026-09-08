from pathlib import Path
import json
root=Path(__file__).resolve().parents[1];pkg=root/'P100_TRANSFER'
for folder in ['01_CONTEXTO','02_EVIDENCIA']:
    for path in (pkg/folder).glob('*'):
        if path.suffix not in ('.md','.json'):continue
        text=path.read_text(encoding='utf-8')
        text=text.replace('tmp/experiment_records.json','02_EVIDENCIA/EXPERIMENTOS_HISTORICOS.json').replace('tmp/artifact_mentions.json','02_EVIDENCIA/MENCIONES_ARCHIVOS.json').replace('tmp/pdf_pages.json','06_VERIFICACION/pdf_checks/PDFM1000v2_pages.json')
        text=text.replace('El mensaje fuente inicial fue truncado a 20.000 caracteres; revisar recuperación ampliada.','El mensaje llega recortado a 20 000 unidades UTF-16; el resto requiere una exportación del original.')
        path.write_text(text,encoding='utf-8')
path=pkg/'02_EVIDENCIA/MENCIONES_ARCHIVOS.json';obj=json.loads(path.read_text(encoding='utf-8'))
obj['attachments'][0]['status']='PRESENTE_VERIFICADO_EN_00_ORIGINALES'
obj['attachments'][0]['package_path']='00_ORIGINALES/PDFM1000v2.pdf'
obj['attachments'][0]['source']='attachments de page_001.json; archivo expuesto por herramienta de lectura'
obj['additional_recovered_originals']=[{'name':'PDFM1000.pdf','package_path':'00_ORIGINALES/PDFM1000.pdf','source':'Downloads; comparación con el anexo v2 documentada en AUDITORIA_PDF.md','status':'PRESENTE_VERIFICADO'}]
path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
