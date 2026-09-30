#!/usr/bin/env python3
"""Validate the public lexical-terminology release using the Python standard library."""
import hashlib
import json
import re
import sys
from pathlib import Path
from build_public_mapping_release import aggregate, canonical, compute_report, read_rows

ROOT=Path(__file__).resolve().parent
DENIED={'clinicaltext','textoclinico','caseid','blindrecordid','annotatorid','sourcepair',
 'patientid','dni','email','phone','adjudicationrationale','start','end','documentid'}

def require(condition,message):
    if not condition: raise ValueError(message)

def check_schema(value,schema,path='$'):
    """Validate the explicit subset used by SCHEMA_MAPPING.json; fail on unsupported keywords."""
    supported={'$schema','$id','title','description','type','required','properties','additionalProperties',
      'enum','const','pattern','minLength','minimum','maximum','items','uniqueItems','allOf','if','then','not','anyOf'}
    require(not set(schema)-supported, f'Unsupported schema keywords at {path}: {set(schema)-supported}')
    types={'object':lambda v:isinstance(v,dict),'array':lambda v:isinstance(v,list),
      'string':lambda v:isinstance(v,str),'number':lambda v:isinstance(v,(float,int)) and not isinstance(v,bool),
      'integer':lambda v:isinstance(v,int) and not isinstance(v,bool),'null':lambda v:v is None,
      'boolean':lambda v:isinstance(v,bool)}
    if 'type' in schema:
        allowed=schema['type'] if isinstance(schema['type'],list) else [schema['type']]
        require(any(types[t](value) for t in allowed),f'Type mismatch at {path}')
    if 'enum' in schema: require(value in schema['enum'],f'Invalid enum at {path}')
    if 'const' in schema: require(value==schema['const'],f'Invalid constant at {path}')
    if isinstance(value,dict):
        require(set(schema.get('required',[]))<=set(value),f'Missing required fields at {path}')
        if schema.get('additionalProperties') is False:
            require(set(value)<=set(schema.get('properties',{})),f'Extra properties at {path}')
        for key,sub in schema.get('properties',{}).items():
            if key in value: check_schema(value[key],sub,path+'.'+key)
    if isinstance(value,list) and 'items' in schema:
        for i,item in enumerate(value): check_schema(item,schema['items'],f'{path}[{i}]')
    if isinstance(value,list) and schema.get('uniqueItems'):
        require(len({canonical(item) for item in value})==len(value),f'Duplicate array items at {path}')
    if isinstance(value,str):
        require(len(value)>=schema.get('minLength',0),f'Empty string at {path}')
        if 'pattern' in schema: require(re.search(schema['pattern'],value) is not None,f'Pattern at {path}')
    if isinstance(value,(int,float)) and not isinstance(value,bool):
        require(value>=schema.get('minimum',float('-inf')) and value<=schema.get('maximum',float('inf')),f'Range at {path}')
    def matches(sub):
        try: check_schema(value,sub,path);return True
        except ValueError:return False
    for sub in schema.get('allOf',[]): check_schema(value,sub,path)
    if 'anyOf' in schema: require(any(matches(s) for s in schema['anyOf']),f'anyOf at {path}')
    if 'not' in schema: require(not matches(schema['not']),f'not at {path}')
    if 'if' in schema and matches(schema['if']) and 'then' in schema:check_schema(value,schema['then'],path)

def walk(value):
    if isinstance(value,dict):
        for key,child in value.items():
            require(re.sub('[^a-z0-9]','',key.casefold()) not in DENIED,f'Forbidden source field: {key}')
            walk(child)
    elif isinstance(value,list):
        for child in value:walk(child)

def validate():
    manifest=json.loads((ROOT/'RELEASE_MANIFEST.json').read_text())
    files=manifest['files']
    require(files==(ROOT/'PUBLIC_RELEASE_ALLOWLIST.txt').read_text().splitlines(),'Allowlist differs')
    actual=sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
      and not any(part.startswith('.') or part=='__pycache__' for part in p.relative_to(ROOT).parts) and p.suffix!='.pyc')
    require(files==actual,'File inventory differs')
    require(set(manifest['sha256'])==set(files)-{'RELEASE_MANIFEST.json'},'Hash inventory differs')
    for name,h in manifest['sha256'].items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,f'Hash mismatch: {name}')
    schema=json.loads((ROOT/'SCHEMA_MAPPING.json').read_text())
    human=read_rows('terminology_occurrences.jsonl');candidates=read_rows('faiss_candidate_occurrences.jsonl')
    allrows=human+candidates
    require(len({r['occurrenceId'] for r in allrows})==len(allrows),'Occurrence IDs are not unique')
    for rows,allowed in ((human,{'human_agreement','human_adjudicated'}),(candidates,{'faiss_candidate','faiss_candidate_below_threshold'})):
        for r in rows:
            check_schema(r,schema['occurrences']);walk(r)
            require(r['mappingStatus'] in allowed,'Partition contamination')
            require(r['mappingValidationStatus']==('human_source_decision' if r['mappingStatus'].startswith('human_') else 'pending_human_validation'),'Validation status mismatch')
            require(r['independentAuditStatus']=='not_audited','No independent audit has been performed in this release')
            if r['mappingStatus'].startswith('faiss_'):
                require((r['inferenceScore']>=.70)==(r['mappingStatus']=='faiss_candidate'),'Threshold label mismatch')
                if r['auditFlags']:require(r['mappingUsage']=='review_only','Flagged candidate is usable')
    for source,name in ((human,'terminology_mapping.jsonl'),(candidates,'faiss_candidates.jsonl')):
        actualrows=read_rows(name)
        require(actualrows==aggregate(source),f'Aggregation differs: {name}')
        for r in actualrows:check_schema(r,schema['terms']);walk(r)
    lexical=read_rows('lexical_inventory.jsonl')
    expected=[{k:r.get(k) for k in ('occurrenceId','surface','surfaceNormalized','normalizedKey','formType','senseId',
      'expansion','correctedForm','function','section','noteType','specialty','evidence','lexicalValidationStatus','independentAuditStatus')}
      for r in candidates+[r for r in human if r['layer']=='lexical']]
    review=json.loads((ROOT/'REVIEW_DECISIONS.json').read_text())
    decisions={r['occurrenceId']:r for r in review['decisions']}
    require(len(decisions)==21,'Expected 21 accepted review records')
    require(set(decisions)=={r['occurrenceId'] for r in candidates if r['mappingUsage']=='review_only'},'Reviewed records differ')
    for item in expected:
        if item['occurrenceId'] in decisions:
            decision=decisions[item['occurrenceId']]
            item.update(decision['lexicalChanges'])
            item['reviewStatus']='proposal_accepted_by_project_responsible'
            item['mappingAction']=decision['mappingAction']
            item['reviewNote']=decision['note']
    require(lexical==expected,'Lexical inventory differs')
    for r in lexical:walk(r)
    report=compute_report(human,candidates)
    require(report==manifest['counts']==json.loads((ROOT/'QUALITY_REPORT.json').read_text()),'Report differs')
    exclusions=json.loads((ROOT/'EXCLUSIONS.json').read_text())
    require(exclusions['inputOccurrences']==len(allrows)+exclusions['excludedOccurrences'],'Source counts differ')
    print('VALID RELEASE: source-free payload, schemas, partitions, aggregation, report and exact-byte hashes')
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=='__main__':
    try:validate()
    except (ValueError,KeyError,OSError) as exc:
        print('INVALID RELEASE: '+str(exc),file=sys.stderr);sys.exit(1)
