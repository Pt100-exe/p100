from pathlib import Path
import json,hashlib,csv,zipfile,datetime,subprocess,sys,re
ROOT=Path(__file__).resolve().parents[1];PKG=ROOT/'P100_TRANSFER'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
assert sha(PKG/'00_ORIGINALES/PDFM1000v2.pdf')=='1ac4796614ba80f122a456531bad08cbc99b94b5354ca9d144d1cc2b2587c9db'
assert sha(PKG/'00_ORIGINALES/PDFM1000.pdf')=='9b1b96a98260b127e8cc024db88b0949bd157921c1e35d0110017b9fa840333f'
literal=(PKG/'00_ORIGINALES/conversacion_recuperada/TRANSCRIPCION_LITERAL.md').read_text(encoding='utf-8')
editable=(PKG/'04_DOCUMENTO/P100_Documento_integral.md').read_text(encoding='utf-8')
messages=0
for file in sorted((PKG/'00_ORIGINALES/conversacion_recuperada').glob('page_*.json')):
    for turn in json.loads(file.read_text(encoding='utf-8'))['turns']:
        for item in turn['items']:
            text=item.get('text')
            if text is None:text='\n'.join(c.get('text',json.dumps(c,ensure_ascii=False)) for c in item.get('content',[]))
            assert text in literal,item['id']
            assert text in editable,item['id']
            messages+=1
assert messages==27
for file in (PKG/'05_CODIGO/v06_foundations').rglob('*.py'):
    assert file.read_text(encoding='utf-8') in editable,file
for file in PKG.rglob('*.json'):json.loads(file.read_text(encoding='utf-8'))
experiments=json.loads((PKG/'02_EVIDENCIA/EXPERIMENTOS_HISTORICOS.json').read_text(encoding='utf-8'))
assert len(experiments['records'])==20
assert sum(experiments['records'][3]['results']['categories'].values())==5878
qa=json.loads((ROOT/'tmp/pdf_build/qa_automatic.json').read_text(encoding='utf-8'))
assert not qa['geometry_issues'];assert qa['pages']==186
code=PKG/'05_CODIGO/v06_foundations'
ver=subprocess.run([sys.executable,'-B','-m','p100_foundations','verify'],cwd=code,capture_output=True,text=True)
assert ver.returncode==0,ver.stdout+ver.stderr
closures={'MANIFEST_SHA256.json','PACKAGE_CHECK.json'}
inventory_path=PKG/'INVENTARIO_ARCHIVOS.csv'
paths=sorted({p.relative_to(PKG).as_posix() for p in PKG.rglob('*') if p.is_file()}|closures|{'INVENTARIO_ARCHIVOS.csv'})
assert not any('__pycache__' in p for p in paths)
def category(rel):
    if rel.startswith('00_ORIGINALES/'):return 'FUENTE_RECUPERADA_O_SOLICITUD_ACTUAL'
    if rel.startswith('05_CODIGO/'):return 'IMPLEMENTACION_NUEVA_Y_PRUEBAS_ACTUALES'
    if rel.startswith('06_VERIFICACION/'):return 'VERIFICACION_ACTUAL'
    if rel.startswith('02_EVIDENCIA/'):return 'AUDITORIA_O_DATOS_TRANSCRITOS'
    return 'DOCUMENTACION_DE_TRANSFERENCIA'
with inventory_path.open('w',encoding='utf-8-sig',newline='') as handle:
    writer=csv.writer(handle);writer.writerow(['ruta_relativa','categoria','estado'])
    writer.writerows((p,category(p),'PRESENTE') for p in paths)
records=[]
for file in sorted(p for p in PKG.rglob('*') if p.is_file() and p.relative_to(PKG).as_posix() not in closures):
    records.append({'path':file.relative_to(PKG).as_posix(),'bytes':file.stat().st_size,'sha256':sha(file)})
manifest={'schema':'P100-transfer-1','created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'historical_recovery_status':'INCOMPLETE_HISTORICAL_RECOVERY','excluded_self_dependent_files':sorted(closures),'files':records}
(PKG/'MANIFEST_SHA256.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
run=subprocess.run([sys.executable,'-B',str(PKG/'06_VERIFICACION/verify_package.py')],capture_output=True,text=True,encoding='utf-8')
assert run.returncode==0,run.stdout+run.stderr
check={'manifest_verification':json.loads(run.stdout),'source_message_preservation':{'messages_checked':messages,'literal_and_editable':'PASS'},'new_python_source_in_editable':'PASS','historical_experiment_groups':20,'reported_battery_arithmetic':5878,'new_component_freeze':json.loads(ver.stdout),'pdf_qa':qa,'historical_backtests_reproduced':False,'remaining_gaps':['Original prototype ZIPs, market CSV and raw results/config/tests/logs','Remainder of message 69184771-b0a3-4e0e-aeef-ee06818cb816','Opaque historical artifact references']}
(PKG/'PACKAGE_CHECK.json').write_text(json.dumps(check,ensure_ascii=False,indent=2),encoding='utf-8')
archive=ROOT/'P100_Transferencia_Codex_2026-09-07.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=7) as bundle:
    for file in sorted(p for p in PKG.rglob('*') if p.is_file()):bundle.write(file,'P100_TRANSFER/'+file.relative_to(PKG).as_posix())
with zipfile.ZipFile(archive) as bundle:
    assert bundle.testzip() is None
    assert len(bundle.namelist())==len(paths)
    for name in bundle.namelist():
        file=ROOT/name
        assert hashlib.sha256(bundle.read(name)).hexdigest()==sha(file),name
digest=sha(archive)
(ROOT/(archive.name+'.sha256')).write_text(digest+'  '+archive.name+'\n',encoding='utf-8')
result={'archive':str(archive),'archive_bytes':archive.stat().st_size,'archive_sha256':digest,'files_in_archive':len(paths),'manifest_files_checked':len(records),'document_pages':186,'source_messages':27,'new_tests_passed':38,'historical_recovery':'INCOMPLETE_EXPLICIT_GAPS','zip_crc_and_content_hashes':'PASS'}
(ROOT/'tmp/final_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
