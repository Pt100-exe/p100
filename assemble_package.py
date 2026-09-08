import pathlib,json,re,shutil,sys,subprocess,datetime,platform
root=pathlib.Path(__file__).resolve().parents[1]; pkg=root/'P100_TRANSFER'; ev=pkg/'02_EVIDENCIA'; ctx=pkg/'01_CONTEXTO'
shutil.copy2(root/'tmp/historical_audit.md',ev/'AUDITORIA_HISTORICA.md')
shutil.copy2(root/'tmp/pdf_audit.md',ev/'AUDITORIA_PDF.md')
shutil.copy2(root/'tmp/experiment_records.json',ev/'EXPERIMENTOS_HISTORICOS.json')
shutil.copy2(root/'tmp/artifact_mentions.json',ev/'MENCIONES_ARCHIVOS.json')
audit=(ev/'AUDITORIA_HISTORICA.md').read_text(encoding='utf-8').replace('20.000 caracteres','20.000 unidades UTF-16')
audit=audit.replace('`tmp/recovered/page_001.json` y `page_002.json`','`00_ORIGINALES/conversacion_recuperada/page_001.json` y `page_002.json`')
(ev/'AUDITORIA_HISTORICA.md').write_text(audit,encoding='utf-8')
decisions='# Registro de decisiones y evolución técnica\n\nEste registro conserva el contexto completo de las decisiones históricas y sus revisiones. Los arreglos declarados no han sido reproducidos contra el código ausente. V01/P03/etc. se resuelven en el mapa de procedencia de AUDITORIA_HISTORICA.md. Las decisiones nuevas aparecen en CAMBIOS_ACTUALES.md.\n\n'+audit.split('## Cronología y decisiones',1)[1]
(ctx/'DECISIONS.md').write_text(decisions,encoding='utf-8')
records=json.loads((ev/'EXPERIMENTOS_HISTORICOS.json').read_text(encoding='utf-8'))['records']
indices=json.loads((pkg/'00_ORIGINALES/conversacion_recuperada/INDICE_MENSAJES.json').read_text(encoding='utf-8'))
refs={r['message_id']:r['ref'] for r in indices}
def scalar(v):
    if v is None:return 'No reportado'
    if isinstance(v,bool):return 'Sí' if v else 'No'
    return str(v)
def describe(v,prefix=''):
    lines=[]
    if isinstance(v,dict):
        if 'columns' in v and 'rows' in v:
            cols=v['columns']; rows=v['rows']
            # Transponer tablas muy anchas para legibilidad sin perder métricas.
            if len(cols)>6:
                lines+=['| Métrica | '+' | '.join(str(r[0]) for r in rows)+' |','|---|'+'---|'*len(rows)]
                for k,c in enumerate(cols[1:],1):lines+=['| '+c+' | '+' | '.join(scalar(r[k]) for r in rows)+' |']
            else:
                lines+=['| '+' | '.join(cols)+' |','|'+'---|'*len(cols)]
                lines+=['| '+' | '.join(scalar(x) for x in r)+' |' for r in rows]
        for k,x in v.items():
            if k in ('columns','rows'):continue
            lines+=describe(x,(prefix+'.' if prefix else '')+k)
    elif isinstance(v,list):
        if all(not isinstance(x,(dict,list)) for x in v):lines+=['- '+prefix+': '+', '.join(scalar(x) for x in v)]
        else:
            for n,x in enumerate(v):lines+=describe(x,f'{prefix}[{n}]')
    else:lines+=['- '+prefix+': '+scalar(v)]
    return lines
parts=['# Registro de experimentos históricos','\n20 grupos de resultados declarados, sin nueva reproducción de los backtests. Porcentajes expresados en puntos porcentuales; un campo percent=5.01 significa 5.01%. null se muestra como No reportado. Los nombres de métricas conservan sus unidades y la marca approx cuando existe. Los drawdowns se conservan con el signo de su fuente; no homogeneizar máximos negativos y magnitudes positivas sin explicarlo.','\nLos grupos reúnen tablas y pruebas comunicadas, no necesariamente ejecuciones independientes. Todos tienen currently_reproduced=false. La fuente primaria es la transcripción literal; los JSON estructurados facilitan consulta y no reemplazan archivos de mercado o resultados que faltan.']
for rec in records:
    parts += ['\n## '+rec['id']+' '+rec['experiment'], '\nFuente '+refs.get(rec['source']['message_id'],'')+' | Mensaje '+rec['source']['message_id']+'\n','### Protocolo\n']+describe(rec.get('protocol',{}))+['\n### Resultados\n']+describe(rec.get('results',{}))+['\n### Límites\n']+['- '+x for x in rec.get('limitations',[])]
(ctx/'EXPERIMENT_LOG.md').write_text('\n'.join(parts),encoding='utf-8')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
code=pkg/'05_CODIGO/v06_foundations'
run=subprocess.run([sys.executable,'-B','-m','unittest','discover','-s','tests','-v'],cwd=code,capture_output=True,text=True,encoding='utf-8',env={**__import__('os').environ,'PYTHONUTF8':'1'})
log=f'UTC: {now}\nPython: {sys.version}\nPlatform: {platform.platform()}\nCommand: python -B -m unittest discover -s tests -v\nExit: {run.returncode}\n'+run.stdout+run.stderr
(code/'test_run.log').write_text(log,encoding='utf-8')
print(log)
if run.returncode:raise SystemExit(run.returncode)
if not (code/'FREEZE_MANIFEST.json').exists():
    fr=subprocess.run([sys.executable,'-B','-m','p100_foundations','freeze'],cwd=code,capture_output=True,text=True,encoding='utf-8',env={**__import__('os').environ,'PYTHONUTF8':'1'})
    (code/'freeze_run.log').write_text(fr.stdout+fr.stderr,encoding='utf-8');print(fr.stdout);assert fr.returncode==0
vr=subprocess.run([sys.executable,'-B','-m','p100_foundations','verify'],cwd=code,capture_output=True,text=True,encoding='utf-8',env={**__import__('os').environ,'PYTHONUTF8':'1'})
(code/'freeze_verify.log').write_text(vr.stdout+vr.stderr,encoding='utf-8');print(vr.stdout);assert vr.returncode==0
