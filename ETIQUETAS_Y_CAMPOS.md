# Campos del recurso léxico-terminológico v2

| Campo | Significado |
|---|---|
| `surface`, `surfaceNormalized` | Fragmento y normalización de origen |
| `sctid`, `term` | Concepto/descripción de origen, o propuesta si es FAISS |
| `category` | Etiqueta original conservada |
| `categoryCanonical` | Equivalencia textual normalizada, no jerarquía verificada |
| `categoryValidationStatus` | `source_label_normalized_not_ontology_verified` |
| `layer` | `clinical` o `lexical` |
| `evidence` | `agreement`, `adjudicated_disagreement`; agregados admiten `mixed` |
| `mappingStatus` | `human_agreement`, `human_adjudicated`, `faiss_candidate`, `faiss_candidate_below_threshold` |
| `mappingValidationStatus` | `human_source_decision` o `pending_human_validation` |
| `lexicalValidationStatus` | `not_applicable`, `source_resolved_not_independently_audited`, `not_documented` |
| `independentAuditStatus` | `not_audited` en esta entrega; schema contempla futura auditoría |
| `mappingUsage` | `human_reference_requires_audit`, `candidate_generation_only`, `review_only` |
| `auditFlags` | Umbral bajo, sentido no documentado, discordancia expansión-candidato |
| `occurrenceId` | ID reproducible del registro, sin enlace a nota/paciente |
| `termId` | Hash de la identidad agregada definida en el constructor |
| `inferenceScore`, `inferenceMethod` | Similitud y método, solo en propuestas automáticas |
| `occurrenceCount` | Registros por grupo, no pacientes/documentos |
| `agreementOccurrences`, `adjudicatedOccurrences` | Procedencia, no concordancia |
| `noteTypes`, `specialties` | Valores no nulos de registros agregados |

## Contexto y léxico

`polarity`: Activo/Negado; `certainty`: Confirmado/Sospecha/Diferencial; `temporality`: Actual/Histórico; `subject`: Paciente/Familiar. Son parte del significado, no deben descartarse. `null` indica falta de información.

`formType`: abbreviation, acronym, initialism, alphanumeric, symbolic_abbreviation, other. `function`: header, entity, value, result, modifier, structural, other o null. `section` es ubicación estructural declarada. `senseId` conserva etiqueta/expansión de origen: no se presume un ID estable de ontología de sentidos. `expansion` y `correctedForm` mantienen los valores originales.

La capa clínica usa hallazgo clínico, procedimiento y fármaco; las propuestas léxicas incluyen otras etiquetas. No usar categorías como certificación de jerarquía SNOMED. El contrato de la plataforma de anotación se describe en CONTRATO_CAPA_LEXICA_V2.md; no es el esquema del payload público.

## Correcciones aceptadas

REVIEW_DECISIONS.json registra cambios aceptados por el responsable, enlazados solo al occurrenceId público. lexical_inventory.jsonl incorpora estos ajustes y añade reviewStatus, mappingAction y reviewNote en las 21 filas revisadas; lexicalValidationStatus puede ser proposal_accepted_by_project_responsible para expansiones aceptadas. Se preservan las anotaciones originales en las particiones de ocurrencias. La aprobación de una propuesta no valida automáticamente un SCTID ni convierte la revisión del responsable en auditoría independiente.
