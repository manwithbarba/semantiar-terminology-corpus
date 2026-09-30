# SemantIAr — Recurso léxico-terminológico clínico del español rioplatense

Versión: `semantiar-lexical-terminology.v2` · 29/09/2026  
Responsable: **Julián Sánchez Viamonte**, Facultad de Ciencias Médicas, UNLP.  
Datos propios: **CC BY-SA 4.0**, sujeto a [NOTICE-SNOMED.md](NOTICE-SNOMED.md).

## Qué es

Corpus Publico de expresiones clínicas y formas breves registradas durante la anotación de notas desidentificadas de la Historia de Salud Integrada de la Provincia de Buenos Aires. Conserva formas, expansiones, decisiones humanas, atributos de significado y propuestas de conceptos SNOMED CT. Su unidad es un registro léxico-terminológico derivado de anotación.

## Para qué sirve

Sirve para lookup, diccionarios, estudio de variantes, expansión léxica y generación de candidatos. La semántica está representada por conceptos y atributos con estados de validación explícitos. La entrega no incluye notas clínicas; no permite evaluar NER, límites de spans, omisiones ni interpretación contextual desde la nota.

## Archivos publicados

| Archivo | Contenido | Cantidad |
|---|---|---:|
| [terminology_mapping.jsonl](terminology_mapping.jsonl) | Entradas agregadas de decisiones humanas | 953 |
| [terminology_occurrences.jsonl](terminology_occurrences.jsonl) | Registros humanos: 210 acuerdos y 878 adjudicaciones | 1.088 |
| [faiss_candidates.jsonl](faiss_candidates.jsonl) | Entradas agregadas de candidatos pendientes | 412 |
| [faiss_candidate_occurrences.jsonl](faiss_candidate_occurrences.jsonl) | Registros FAISS; 6 bajo umbral | 472 |
| [lexical_inventory.jsonl](lexical_inventory.jsonl) | Caracterización léxica sin candidato ontológico | 472 |
| [QUALITY_REPORT.json](QUALITY_REPORT.json) | Estadísticas descriptivas recalculables | — |

Las particiones humanas y automáticas conservan los 1.560 registros previos. El inventario léxico es una vista: **no se suma** como registros adicionales. Hay 904 formas normalizadas y 899 SCTID distintos incluyendo candidatos. Las 1.365 entradas combinadas no son términos únicos: la identidad agrega forma, concepto, atributos y score cuando corresponde.

## Calidad y uso

`human_agreement` y `human_adjudicated` describen procedencia, Todos los registros siguen `not_audited` en la dimensión de auditoría independiente.

La expansión léxica y su mapeo ontológico tienen estados separados. FAISS propone candidatos pendientes; el umbral 0,70 es similitud, no probabilidad de acierto. Cobertura de asignación no es exactitud.

1. Para decisiones humanas, comenzar por `terminology_mapping.jsonl`.
2. Conservar **concepto y atributos**: `afebril → fiebre` con `polarity: Negado` cambia de significado si se elimina la negación.
3. Para formas y expansiones, usar `lexical_inventory.jsonl`.
4. Si se usan candidatos, filtrar `mappingUsage == "candidate_generation_only"`; las filas `review_only` requieren revisión previa.
5. No elegir automáticamente el sentido más frecuente de expresiones con varios conceptos.

Las frecuencias cuentan registros derivados de anotación, no pacientes, notas únicas, prevalencia ni necesariamente apariciones independientes. Se preservan repeticiones. `occurrenceId` identifica el registro exportado; no enlaza una nota ni paciente.

## Procedencia y límites

 15 parejas, 15 lotes y 5 notas básicas por lote. Notas únicas, premarcación, muestreo efectivo y detalle por pareja no se verifican con estos archivos. La edición declarada es Argentina 20260520.

Documentación: [ficha](DATASET_CARD.md), [metodología](METODOLOGIA_Y_PROCEDIMIENTO.md), [campos](ETIQUETAS_Y_CAMPOS.md), [evaluación y concordancia](EVALUACION_Y_CONCORDANCIA.md), [auditoría y pendientes](AUDITORIA_Y_CAMBIOS.md).




## Revisión aceptada por el responsable

Julián Sánchez Viamonte (investigador principal)
