#!/usr/bin/env python3
"""Rebuild public derivatives from public occurrences; never accepts clinical notes."""
import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IDENTITY_FIELDS = ('layer','surfaceNormalized','category','sctid','term','polarity',
 'certainty','temporality','subject','normalizedKey','formType','senseId','expansion',
 'correctedForm','function','section','mappingStatus','inferenceScore')
HUMAN = {'human_agreement','human_adjudicated'}
CANDIDATE = {'faiss_candidate','faiss_candidate_below_threshold'}

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def read_rows(name):
    return [json.loads(line) for line in (ROOT/name).read_text(encoding='utf-8').splitlines() if line.strip()]

def write_json(name, value):
    (ROOT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

def write_rows(name, rows):
    (ROOT/name).write_text(''.join(canonical(row)+'\n' for row in rows),encoding='utf-8',newline='\n')

def aggregate(rows):
    groups = collections.defaultdict(list)
    for row in rows:
        groups[tuple(row.get(key) for key in IDENTITY_FIELDS)].append(row)
    result = []
    for identity, group in groups.items():
        row = {key:value for key,value in group[0].items() if key not in {'noteType','specialty','occurrenceId'}}
        raw=canonical(identity)
        row.update(termId=hashlib.sha256(raw.encode()).hexdigest()[:16],
          occurrenceCount=len(group), agreementOccurrences=sum(r['evidence']=='agreement' for r in group),
          adjudicatedOccurrences=sum(r['evidence']=='adjudicated_disagreement' for r in group),
          noteTypes=sorted({r['noteType'] for r in group if r.get('noteType')}),
          specialties=sorted({r['specialty'] for r in group if r.get('specialty')}))
        evidences={r['evidence'] for r in group}
        row['evidence']=next(iter(evidences)) if len(evidences)==1 else 'mixed'
        result.append(row)
    return result

def compute_report(human, candidates):
    rows=human+candidates
    review=json.loads((ROOT/'REVIEW_DECISIONS.json').read_text(encoding='utf-8'))['decisions']
    terms=aggregate(rows)
    surfaces=collections.defaultdict(set)
    for row in rows: surfaces[row['surfaceNormalized']].add(row['sctid'])
    duplicate=collections.Counter(canonical({k:v for k,v in r.items() if k!='occurrenceId'}) for r in rows)
    return {
      'scope':'Descriptive statistics of published annotation-derived records; not inter-annotator agreement or clinical prevalence.',
      'humanOccurrences':len(human),'candidateOccurrences':len(candidates),
      'publishedOccurrences':len(rows),'humanEntries':len(aggregate(human)),
      'candidateEntries':len(aggregate(candidates)),'totalEntries':len(terms),
      'uniqueNormalizedSurfaces':len(surfaces),'distinctSctidsIncludingCandidates':len({r['sctid'] for r in rows}),
      'singletonEntries':sum(r['occurrenceCount']==1 for r in terms),
      'surfacesWithMultipleSctids':sum(len(v)>1 for v in surfaces.values()),
      'mappingStatusCounts':dict(sorted(collections.Counter(r['mappingStatus'] for r in rows).items())),
      'exactDuplicateExcessIgnoringPublicOccurrenceId':sum(n-1 for n in duplicate.values()),
      'reviewOnlyCandidateOccurrences':sum(r['mappingUsage']=='review_only' for r in candidates),
      'independentlyAuditedOccurrences':sum(r['independentAuditStatus']=='audited' for r in rows),
      'acceptedReviewDecisions':len(review),
      'acceptedMappingActions':dict(sorted(collections.Counter(r['mappingAction'] for r in review).items())),
      'interAnnotatorAgreement':{'status':'not_recomputable_from_public_payload','reason':'No source texts, offsets, paired annotations or denominators are published.'},
      'sampling':{'reportedPairs':15,'reportedBatches':15,'reportedNotesPerBatch':5,
        'uniqueNotes':None,'premarkingStatus':'not_verified','source':'README.md at bb36b7f7ebabf10c3f2642ef9cf5040366241f70; numbers reported, not independently verified.'}}

def build():
    human=read_rows('terminology_occurrences.jsonl')
    candidates=read_rows('faiss_candidate_occurrences.jsonl')
    if any(r['mappingStatus'] not in HUMAN for r in human): raise ValueError('Human payload contains automatic candidates')
    if any(r['mappingStatus'] not in CANDIDATE for r in candidates): raise ValueError('Candidate payload contains human mappings')
    write_rows('terminology_mapping.jsonl',aggregate(human))
    write_rows('faiss_candidates.jsonl',aggregate(candidates))
    # Lexical senses are preserved separately from provisional ontology mappings.
    lexical=[]
    decisions={r['occurrenceId']:r for r in json.loads((ROOT/'REVIEW_DECISIONS.json').read_text(encoding='utf-8'))['decisions']}
    for r in candidates+[r for r in human if r['layer']=='lexical']:
        item={k:r.get(k) for k in ('occurrenceId','surface','surfaceNormalized','normalizedKey',
          'formType','senseId','expansion','correctedForm','function','section','noteType','specialty',
          'evidence','lexicalValidationStatus','independentAuditStatus')}
        if r['occurrenceId'] in decisions:
            decision=decisions[r['occurrenceId']]
            item.update(decision['lexicalChanges'])
            item['reviewStatus']='proposal_accepted_by_project_responsible'
            item['mappingAction']=decision['mappingAction']
            item['reviewNote']=decision['note']
        lexical.append(item)
    write_rows('lexical_inventory.jsonl',lexical)
    report=compute_report(human,candidates)
    write_json('QUALITY_REPORT.json',report)
    files=sorted(p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()
      and not any(part.startswith('.') or part=='__pycache__' for part in p.relative_to(ROOT).parts)
      and p.suffix!='.pyc')
    if 'RELEASE_MANIFEST.json' not in files: files.append('RELEASE_MANIFEST.json');files.sort()
    (ROOT/'PUBLIC_RELEASE_ALLOWLIST.txt').write_text(''.join(n+'\n' for n in files),encoding='utf-8',newline='\n')
    manifest={'schemaVersion':'semantiar-lexical-terminology.v2','release':'SEMANTIAR-LEXICO-TERMINOLOGICO-20260929',
      'locale':'es-AR','terminology':{'editionUri':'http://snomed.info/sct/11000221109/version/20260520',
        'editionValidationStatus':'source_declared_not_revalidated','licenseReviewRequired':True},
      'counts':report,'files':files,
      'integrityPolicy':{'algorithm':'SHA-256','manifestSelfHashExcluded':True,'lineEndings':'LF; hashes cover exact published bytes'},
      'qualityPolicy':{'human':'Human source decisions, not an independently audited gold standard.',
        'faiss':'Separate provisional candidates; review_only candidates excluded from generation by default.',
        'privacy':'No source notes, source document IDs, source offsets or annotator IDs are added.'},
      'sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in files if name!='RELEASE_MANIFEST.json'}}
    write_json('RELEASE_MANIFEST.json',manifest)
    return report

if __name__=='__main__': print(json.dumps(build(),ensure_ascii=False,indent=2))
