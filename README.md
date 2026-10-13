# SemantIAr — Recurso léxico-terminológico clínico del español rioplatense

[![Validate public terminology resource](https://github.com/manwithbarba/semantiar-terminology-corpus/actions/workflows/validate.yml/badge.svg)](https://github.com/manwithbarba/semantiar-terminology-corpus/actions/workflows/validate.yml)

Versión: `semantiar-lexical-terminology.v2` (`v2.0.0`) · datos del 29/09/2026
Documentación revisada: 13/10/2026
Responsable: **Julián Sánchez Viamonte**, Facultad de Ciencias Médicas, Universidad Nacional de La Plata (UNLP) · [Equipo de anotación e integrantes](INTEGRANTES_PROYECTO.md)
Datos propios: **CC BY-SA 4.0** ([LICENSE-DATA.txt](LICENSE-DATA.txt)), sujeto a [NOTICE-SNOMED.md](NOTICE-SNOMED.md).

<details>
<summary><strong>English Abstract (Click to expand)</strong></summary>

**SemantIAr (`semantiar-lexical-terminology.v2`)** is an open clinical lexical-terminological resource for Rioplatense Spanish (`es-AR`), derived from annotation of de-identified clinical notes from the *Historia de Salud Integrada* (Buenos Aires Province, Argentina). It publishes clinical surface forms, abbreviations, lexical expansions, contextual meaning attributes (`polarity`, `certainty`, `temporality`, `subject`), and SNOMED CT mappings without exposing free-text clinical notes or case identifiers. The resource strictly separates human source decisions (`terminology_mapping.jsonl`, `terminology_occurrences.jsonl`), provisional automatic FAISS candidates (`faiss_candidates.jsonl`, `faiss_candidate_occurrences.jsonl`), and ontology-independent lexical characterizations (`lexical_inventory.jsonl`).
</details>

## Qué es

Corpus público de expresiones clínicas y formas breves registradas durante la anotación y recuperación de conceptos clínicos y formas léxicas de notas desidentificadas de la Historia de Salud Integrada de la Provincia de Buenos Aires. Conserva formas, expansiones, decisiones humanas, atributos de significado y propuestas de conceptos SNOMED CT. Su unidad es un registro léxico-terminológico derivado de anotación.

## Acceso, descarga y reutilización

El repositorio es público: el README y los archivos se pueden consultar y descargar gratuitamente, sin iniciar sesión en GitHub. Acceso comprobado el 13/10/2026.

- [Descargar el paquete de la rama main (ZIP)](https://github.com/manwithbarba/semantiar-terminology-corpus/archive/refs/heads/main.zip).
- Para descargar un archivo individual, abrirlo en las tablas siguientes y usar **Raw** o **Download raw file**.
- Los datos propios se distribuyen según [LICENSE-DATA.txt](LICENSE-DATA.txt), que declara **CC BY-SA 4.0**: atribución y compartir igual.
- El acceso público no concede derechos sobre SNOMED CT. Sus SCTID, descripciones y derivados están sujetos a las restricciones descritas en [NOTICE-SNOMED.md](NOTICE-SNOMED.md).

## Validación reproducible y reconstrucción

Con Python 3 (solo biblioteca estándar, sin paquetes adicionales), desde la carpeta descargada, ejecutar:

```console
python validate_public_release.py
```

Un resultado válido comienza con `VALID RELEASE`. El validador comprueba inventario ([PUBLIC_RELEASE_ALLOWLIST.txt](PUBLIC_RELEASE_ALLOWLIST.txt)), integridad exacta en bytes mediante SHA-256 ([RELEASE_MANIFEST.json](RELEASE_MANIFEST.json)), ausencia de los nombres de campos sensibles prohibidos y balance de exclusiones ([EXCLUSIONS.json](EXCLUSIONS.json)), esquema de campos ([SCHEMA_MAPPING.json](SCHEMA_MAPPING.json)) y consistencia de la agregación del corpus. Esta comprobación técnica no constituye una auditoría clínica, ontológica ni una garantía exhaustiva de desidentificación.

Si se modifica un archivo incluido en el manifiesto (incluyendo documentación), se debe regenerar el manifiesto de hashes antes de hacer commit para que el validador y la integración continua pasen:

```console
python build_public_mapping_release.py
python validate_public_release.py
```

## Para qué sirve

Sirve para consulta terminológica, construcción de diccionarios, estudio de variantes regionales (`es-AR`), expansión léxica y generación de candidatos SNOMED CT. La entrega no incluye notas clínicas ni permite evaluar NER, límites de spans, omisiones o interpretación contextual desde la nota. Las decisiones humanas no constituyen una referencia gold auditada para evaluar exactitud.

## Archivos publicados

### 1. Datos léxico-terminológicos y vistas agregadas

| Archivo | Contenido | Cantidad |
|---|---|---:|
| [terminology_mapping.jsonl](terminology_mapping.jsonl) | Entradas agregadas de decisiones humanas (`human_agreement` y `human_adjudicated`) | 953 |
| [terminology_occurrences.jsonl](terminology_occurrences.jsonl) | Registros individuales humanos: 210 acuerdos y 878 adjudicaciones | 1088 |
| [faiss_candidates.jsonl](faiss_candidates.jsonl) | Entradas agregadas de candidatos automáticos pendientes | 412 |
| [faiss_candidate_occurrences.jsonl](faiss_candidate_occurrences.jsonl) | Registros individuales FAISS; 466 sobre umbral y 6 bajo umbral (`< 0.70`) | 472 |
| [lexical_inventory.jsonl](lexical_inventory.jsonl) | Caracterización léxica y expansiones sin candidato ontológico | 472 |

Las particiones humanas y automáticas conservan los 1.560 registros publicados (`1088 + 472`). El inventario léxico es una vista de **472** registros con caracterización léxica: **no se suma** como registros adicionales. Hay 904 formas normalizadas y 899 SCTID distintos incluyendo candidatos. Las 1.365 entradas combinadas no son términos únicos: su identidad combina forma, concepto, atributos y score cuando corresponde.

### 2. Metadatos de control, auditoría y contrato técnico

| Archivo | Propósito |
|---|---|
| [QUALITY_REPORT.json](QUALITY_REPORT.json) | Estadísticas descriptivas recalculables del corpus publicado |
| [REVIEW_DECISIONS.json](REVIEW_DECISIONS.json) | 21 decisiones de revisión aceptadas por el responsable con trazabilidad de cambios |
| [SCHEMA_MAPPING.json](SCHEMA_MAPPING.json) | Esquemas JSON formales para ocurrencias (`occurrences`) y entradas agregadas (`terms`) |
| [EXCLUSIONS.json](EXCLUSIONS.json) | Conteo de registros de entrada y exclusiones aplicadas antes de la publicación |
| [RELEASE_MANIFEST.json](RELEASE_MANIFEST.json) | Manifiesto de versión, edición SNOMED CT, políticas de integridad y hashes SHA-256 |
| [PUBLIC_RELEASE_ALLOWLIST.txt](PUBLIC_RELEASE_ALLOWLIST.txt) | Inventario de los 27 archivos del paquete público; el constructor lo regenera a partir de los archivos presentes |

## Estructura de los registros

Ejemplos completos tomados de los archivos publicados, formateados para lectura. En JSONL cada registro ocupa una sola línea. Se conservan los valores de origen, sin certificar el mapeo ontológico.

### Entrada terminológica humana (`terminology_mapping.jsonl`)

```json
{
  "adjudicatedOccurrences": 1,
  "agreementOccurrences": 0,
  "auditFlags": [],
  "category": "Procedimiento",
  "categoryCanonical": "Procedimiento",
  "categoryValidationStatus": "source_label_normalized_not_ontology_verified",
  "certainty": "Confirmado",
  "correctedForm": null,
  "evidence": "adjudicated_disagreement",
  "expansion": null,
  "formType": null,
  "function": null,
  "independentAuditStatus": "not_audited",
  "layer": "clinical",
  "lexicalValidationStatus": "not_applicable",
  "mappingStatus": "human_adjudicated",
  "mappingUsage": "human_reference_requires_audit",
  "mappingValidationStatus": "human_source_decision",
  "normalizedKey": null,
  "noteTypes": [
    "INTERNACION"
  ],
  "occurrenceCount": 1,
  "polarity": "Activo",
  "sctid": "57485005",
  "section": null,
  "senseId": null,
  "specialties": [
    "Medicina de emergencias"
  ],
  "subject": "Paciente",
  "surface": "(O2 3 LT)",
  "surfaceNormalized": "(o2 3 lt)",
  "temporality": "Actual",
  "term": "oxigenoterapia",
  "termId": "2e1202b7480fefc6"
}
```

### Entrada de inventario léxico (`lexical_inventory.jsonl`)

```json
{
  "correctedForm": null,
  "evidence": "adjudicated_disagreement",
  "expansion": "positivo",
  "formType": "symbolic_abbreviation",
  "function": "result",
  "independentAuditStatus": "not_audited",
  "lexicalValidationStatus": "source_resolved_not_independently_audited",
  "normalizedKey": "(+)",
  "noteType": "AMBULATORIO",
  "occurrenceId": "7c6db68a65467a80719d71ea",
  "section": "examen físico",
  "senseId": "positivo",
  "specialty": "Pediatría",
  "surface": "(+)",
  "surfaceNormalized": "(+)"
}
```

## Calidad, uso recomendado y carga rápida en Python

`human_agreement` y `human_adjudicated` describen procedencia de anotación. Todos los registros siguen con `independentAuditStatus: "not_audited"` en la dimensión de auditoría independiente.

La expansión léxica y su mapeo ontológico tienen estados separados. FAISS propone candidatos pendientes; el umbral publicado es `inferenceScore >= 0.70`. El score mide similitud, no probabilidad de acierto; cobertura de asignación no es exactitud.

1. Para decisiones humanas de origen, comenzar por [terminology_mapping.jsonl](terminology_mapping.jsonl).
2. Conservar **concepto y atributos conjuntamente**: un mapeo como `afebril -> fiebre` acompañado de polaridad negativa (`polarity`) cambia radicalmente de significado clínico si se ignora el modificador.
3. Para estudiar formas breves, abreviaturas y expansiones independientemente de SNOMED CT, usar [lexical_inventory.jsonl](lexical_inventory.jsonl).
4. Si se exploran ocurrencias de candidatos automáticos ([faiss_candidate_occurrences.jsonl](faiss_candidate_occurrences.jsonl)), excluir las filas marcadas con `mappingUsage == "review_only"` (que requieren validación experta).
5. No elegir automáticamente el sentido más frecuente de superficies polisémicas (existen **184** superficies normalizadas asociadas a múltiples SCTID).

Las frecuencias (`occurrenceCount`) cuentan registros derivados de anotación, no pacientes, notas únicas, prevalencia epidemiológica ni necesariamente usos del lenguaje general.

### Ejemplo de carga en Python

```python
import json
from pathlib import Path

def load_jsonl(filename):
    with Path(filename).open(encoding="utf-8") as source:
        return [json.loads(line) for line in source if line.strip()]

human_terms = load_jsonl("terminology_mapping.jsonl")
# Solo para generar candidatos; siguen pendientes de validación humana.
generation_candidates = [
    row for row in load_jsonl("faiss_candidate_occurrences.jsonl")
    if row.get("mappingUsage") == "candidate_generation_only"
]
print(f"Entradas humanas: {len(human_terms)} | Candidatos para generación: {len(generation_candidates)}")
```

## Procedencia y documentación complementaria

Se reportan 15 parejas de anotación, 15 lotes y 5 notas básicas por lote (75 asignaciones de notas; no un total verificado de notas clínicas únicas).

- **Ficha del recurso:** [DATASET_CARD.md](DATASET_CARD.md)
- **Metodología y procedimiento:** [METODOLOGIA_Y_PROCEDIMIENTO.md](METODOLOGIA_Y_PROCEDIMIENTO.md)
- **Diccionario de etiquetas y campos:** [ETIQUETAS_Y_CAMPOS.md](ETIQUETAS_Y_CAMPOS.md)
- **Evaluación y concordancia:** [EVALUACION_Y_CONCORDANCIA.md](EVALUACION_Y_CONCORDANCIA.md)
- **Contrato de la capa léxica v2:** [CONTRATO_CAPA_LEXICA_V2.md](CONTRATO_CAPA_LEXICA_V2.md)
- **Auditoría y registro de cambios:** [AUDITORIA_Y_CAMBIOS.md](AUDITORIA_Y_CAMBIOS.md)
- **Guía de migración a v2:** [MIGRATION_V2.md](MIGRATION_V2.md)
- **Resumen de entrada e historial documental:** [Mapear.md](Mapear.md) · [README_ORIGINAL.md](README_ORIGINAL.md)
- **Equipo del proyecto:** [INTEGRANTES_PROYECTO.md](INTEGRANTES_PROYECTO.md)

## Revisión aceptada por el responsable

**Julián Sánchez Viamonte** (investigador principal). La aceptación histórica no implica auditoría independiente ni aprobación de cambios documentales posteriores. La aceptación del 29/09/2026 corresponde a las 21 decisiones documentadas en [REVIEW_DECISIONS.json](REVIEW_DECISIONS.json) y [AUDITORIA_Y_CAMBIOS.md](AUDITORIA_Y_CAMBIOS.md).

## Cómo citar

Si utilizas este recurso en investigaciones o desarrollos de procesamiento del lenguaje natural clínico, por favor cítalo utilizando los metadatos de [CITATION.cff](https://github.com/manwithbarba/semantiar-terminology-corpus/blob/main/CITATION.cff):

```bibtex
@misc{sanchez_viamonte_2026_semantiar,
  author       = {Sánchez Viamonte, Julián and {Proyecto SemantIAr}},
  title        = {{SemantIAr: Recurso léxico-terminológico clínico del español rioplatense}},
  year         = {2026},
  month        = sep,
  version      = {2.0.0},
  institution  = {Facultad de Ciencias Médicas, Universidad Nacional de La Plata},
  url          = {https://github.com/manwithbarba/semantiar-terminology-corpus},
  note         = {Licencia CC BY-SA 4.0 (sujeto a NOTICE-SNOMED.md)}
}
```
