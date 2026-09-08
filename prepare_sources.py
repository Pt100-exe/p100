import json, pathlib, re, hashlib, shutil, datetime
root=pathlib.Path(__file__).resolve().parents[1]
pkg=root/'P100_TRANSFER'
pages=[json.loads(p.read_text(encoding='utf-8')) for p in sorted((root/'tmp/recovered').glob('page_*.json'))]
out=pkg/'00_ORIGINALES'/'conversacion_recuperada'
out.mkdir(parents=True,exist_ok=True)
for p in sorted((root/'tmp/recovered').glob('page_*.json')): shutil.copy2(p,out/p.name)
turns=sorted([t for p in pages for t in p['turns']],key=lambda t:(t.get('startedAt') or 0,t['id']))
rows=[]; transcript=['# Conversación histórica recuperada','\nFuente: Desarrollo de sistema cuantitativo, conversación 6a9df532-f49c-83e8-b7c7-f4431ecd3238.','\nEsta transcripción conserva el texto devuelto por la herramienta de lectura en orden cronológico. Los marcadores de citas y archivos pertenecen al chat original. No acreditan que los archivos citados estén incluidos. Una respuesta llega truncada a 20 000 caracteres; se señala explícitamente. Las herramientas internas y sus ejecuciones no están disponibles en esta exportación. No es una exportación total de la cuenta ni de las ramas invisibles.']
code=[]; tables=[]; opaque=[]
for n,t in enumerate(turns,1):
    tid=f'T{n:02}'
    stamp=datetime.datetime.fromtimestamp(t['startedAt'],datetime.timezone.utc).isoformat() if t.get('startedAt') else 'sin fecha'
    transcript += [f'\n# {tid} Turno histórico',f'\nID: {t["id"]} | Inicio UTC: {stamp}']
    for j,item in enumerate(t.get('items',[]),1):
        text=item.get('text')
        if text is None: text='\n'.join(c.get('text',json.dumps(c,ensure_ascii=False)) for c in item.get('content',[]))
        role='Patrick' if item['type']=='userMessage' else 'Asistente histórico'
        mid=f'{tid}M{j}'
        truncated=item['type']=='agentMessage' and len(text.encode('utf-16-le'))//2>=20000
        rows.append(dict(ref=mid,turn_id=t['id'],message_id=item.get('id'),role=role,chars=len(text),potentially_truncated=truncated,started_at_utc=stamp))
        transcript += [f'\n## {mid} {role}',f'\nID de mensaje: {item.get("id", "sin ID")}\n',text]
        if truncated: transcript += ['\n[NOTA DE RECUPERACIÓN: el contenido termina aquí por el límite de 20 000 caracteres. No se conoce el texto restante.]']
        for k,m in enumerate(re.finditer(r'```([^\n]*)\n(.*?)```',text,re.S),1):
            code.append(dict(ref=f'{mid}C{k}',source=mid,message_id=item.get('id'),language=m.group(1),content=m.group(2)))
        for k,m in enumerate(re.finditer(r'(?m)^\|.*(?:\n\|.*)+',text),1): tables.append(dict(ref=f'{mid}TAB{k}',source=mid,markdown=m.group(0)))
        for k in re.findall(r':chatgpt-content-reference\{index="(\d+)"\}',text): opaque.append(dict(source=mid,message_id=item.get('id'),index=int(k),status='REFERENCIA_OPACA_NO_RECUPERADA'))
    if not any(x['type']=='agentMessage' for x in t.get('items',[])): transcript += ['\n[NOTA DE RECUPERACIÓN: este turno no contiene respuesta de asistente en los datos devueltos. Se preserva, sin completarlo.]']
(out/'TRANSCRIPCION_LITERAL.md').write_text('\n'.join(transcript),encoding='utf-8')
(out/'INDICE_MENSAJES.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
ev=pkg/'02_EVIDENCIA'
for name,data in [('FRAGMENTOS_CODIGO_HISTORICO.json',code),('TABLAS_HISTORICAS.json',tables),('REFERENCIAS_ARCHIVOS_OPACAS.json',opaque)]: (ev/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
summary=dict(turns=len(turns),messages=len(rows),truncated=sum(x['potentially_truncated'] for x in rows),characters=sum(x['chars'] for x in rows),code_blocks=len(code),tables=len(tables),opaque_references=len(opaque),oldest=rows[0]['started_at_utc'],newest=rows[-1]['started_at_utc'])
(ev/'COBERTURA.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False));print(json.dumps(rows,ensure_ascii=False,indent=2))
