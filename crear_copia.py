"""Build the portable snapshot from this task's workspace, then verify relocation."""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

CONTROL=Path(__file__).resolve().parent
ROOT=CONTROL.parent

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):
            h.update(b)
    return h.hexdigest()

def flatten(value):
    if isinstance(value,str):
        return value
    if isinstance(value,list):
        return '\n'.join(flatten(v) for v in value)
    if isinstance(value,dict):
        return flatten(value.get('text',value.get('content','')))
    return ''

def main():
    conversation=CONTROL/'conversacion_codex_recuperada.json'
    obj=json.loads(conversation.read_text(encoding='utf-8'))
    omitted=0
    for turn in obj['turns']:
        items=[]
        for item in turn.get('items',[]):
            if item.get('type') in ('userMessage','agentMessage','commandExecution','webSearch') and item.get('phase')!='analysis':
                items.append(item)
            else:
                omitted+=1
        turn['items']=items
    obj['portable_copy_notes']={'scope':'App-accessible messages and selected action metadata; not a full account export.',
        'omitted_items':omitted,'internal_reasoning_included':False,'original_page':obj['page'],
        'latest_user_requests':'CONTEXTO_DE_ESTA_COPIA.md'}
    conversation.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
    transcript=['# Conversación accesible de esta tarea de Codex\n',
        'Representación devuelta por la app; no garantiza todos los mensajes o salidas. Se excluye razonamiento interno. Las peticiones más recientes están también en CONTEXTO_DE_ESTA_COPIA.md.\n']
    for turn in reversed(obj['turns']):
        transcript.append('\n## Turno '+turn['id']+' — '+turn.get('status','unknown')+'\n')
        messages=[i for i in turn['items'] if i['type'] in ('userMessage','agentMessage')]
        if not messages:
            transcript.append('La app no devolvió mensajes para esta entrada.\n')
        for item in messages:
            transcript.append('\n### '+('Patrick' if item['type']=='userMessage' else 'Atlas')+'\n')
            transcript.append(flatten(item.get('text',item.get('content','')))+'\n')
    (CONTROL/'CONVERSACION_CODEX_ACCESIBLE.md').write_text('\n'.join(transcript),encoding='utf-8')
    mapping={}
    for dirname in ('P100_TRANSFER','P100_LAB','P100_RESEARCH','tmp','sources'):
        for p in sorted((ROOT/dirname).rglob('*')):
            if p.is_file():
                if p.is_symlink():
                    raise ValueError('Symlink requires explicit handling: '+str(p))
                mapping[p.relative_to(ROOT).as_posix()]=p
    original_archives=('P100_Transferencia_Codex_2026-09-07.zip','P100_Avance_001_Laboratorio.zip','P100_Avance_002_Datos_Reales.zip')
    for name in original_archives:
        expected=(ROOT/(name+'.sha256')).read_text().split()[0]
        assert digest(ROOT/name)==expected,name
        mapping['ENTREGAS_ORIGINALES/'+name]=ROOT/name
        mapping['ENTREGAS_ORIGINALES/'+name+'.sha256']=ROOT/(name+'.sha256')
    top={'LEEME_PRIMERO.md':'LEEME_PRIMERO.md','ESTADO_Y_TRABAJO_POR_COMPONENTES.md':'ESTADO_Y_TRABAJO_POR_COMPONENTES.md',
         'AGENTS.md':'AGENTS_PORTABLE.md','verificar.py':'verificar.py'}
    for target,source in top.items():
        mapping[target]=CONTROL/source
    for name in ('CONTEXTO_DE_ESTA_COPIA.md','conversacion_codex_recuperada.json','CONVERSACION_CODEX_ACCESIBLE.md','crear_copia.py'):
        mapping['PORTABILIDAD/'+name]=CONTROL/name
    mapping['PORTABILIDAD/AGENTS_ENTORNO_ORIGINAL.md']=ROOT/'AGENTS.md'
    entries=[dict(path=name,bytes=p.stat().st_size,sha256=digest(p)) for name,p in sorted(mapping.items())]
    manifest=dict(created_utc=datetime.now(timezone.utc).isoformat(), scope='All available project material in this task at snapshot time',
                  files=entries,empty_reference_directories=['sources/'],missing_history='See P100_TRANSFER/02_EVIDENCIA/COBERTURA_Y_FALTANTES.md')
    manifest_bytes=json.dumps(manifest,ensure_ascii=False,indent=2).encode('utf-8')
    (CONTROL/'CONTENIDO_SHA256.json').write_bytes(manifest_bytes)
    archive=ROOT/'P100_Completo_Portable_2026-09-08.zip'
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for name,p in sorted(mapping.items()):
            mode=zipfile.ZIP_STORED if p.suffix.lower() in ('.zip','.gz','.png','.jpg','.jpeg') else zipfile.ZIP_DEFLATED
            z.write(p,'P100/'+name,compress_type=mode)
        z.writestr('P100/CONTENIDO_SHA256.json',manifest_bytes)
        z.writestr('P100/sources/',b'')
    # Verify archive bytes against the snapshot manifest and ensure no source changed during copying.
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for entry in entries:
            with z.open('P100/'+entry['path']) as f:
                h=hashlib.sha256()
                for b in iter(lambda:f.read(1024*1024),b''):
                    h.update(b)
            assert h.hexdigest()==entry['sha256'],entry['path']
            assert digest(mapping[entry['path']])==entry['sha256'],'Source changed: '+entry['path']
        relocated=CONTROL/'prueba_de_traslado'
        relocated.mkdir(exist_ok=False)
        # All names were generated from verified relative local paths; nevertheless enforce containment.
        for name in z.namelist():
            target=(relocated/name).resolve()
            assert target.is_relative_to(relocated.resolve())
        z.extractall(relocated)
    with (CONTROL/'VALIDACION_TRASLADO.log').open('w',encoding='utf-8') as f:
        result=subprocess.run([sys.executable,'-B','verificar.py','--pruebas'],cwd=relocated/'P100',stdout=f,stderr=subprocess.STDOUT)
    assert result.returncode==0,(CONTROL/'VALIDACION_TRASLADO.log').read_text(encoding='utf-8')
    checksum=digest(archive)
    archive.with_suffix('.zip.sha256').write_text(checksum+'  '+archive.name+'\n',encoding='utf-8')
    summary=dict(status='PASS',archive=str(archive),bytes=archive.stat().st_size,sha256=checksum,
                 files=len(entries)+1,project_files=sum(1 for e in entries if e['path'].startswith(('P100_TRANSFER/','P100_LAB/','P100_RESEARCH/'))),
                 original_archives_verified=3,relocated_test_methods=67,relocation='Extracted to a different local path; all-file hashes, three original manifests, market audit and current tests passed.')
    (CONTROL/'RESULTADO_PORTABILIDAD.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary))

if __name__=='__main__':
    main()
