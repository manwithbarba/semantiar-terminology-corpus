# SemantIAr — Recurso léxico-terminológico clínico del español rioplatense

Versión: `semantiar-lexical-terminology.v2` · 29/09/2026  
Responsable: **Julián Sánchez Viamonte**, Facultad de Ciencias Médicas, UNLP.  
Datos propios: **CC BY-SA 4.0**, sujeto a [NOTICE-SNOMED.md](NOTICE-SNOMED.md).

## Qué es

Publica expresiones clínicas y formas breves registradas durante la anotación de notas desidentificadas de la Historia de Salud Integrada de la Provincia de Buenos Aires. Conserva formas, expansiones, decisiones humanas, atributos de significado y propuestas de conceptos SNOMED CT. Su unidad es un registro léxico-terminológico derivado de anotación.

Sirve para lookup, diccionarios, estudio de variantes, expansión léxica y generación de candidatos. La semántica está representada por conceptos y atributos con estados de validación explícitos. La entrega pública no incluye notas clínicas; no permite evaluar NER, límites de spans, omisiones ni interpretación contextual desde la nota. No constituye un gold standard auditado ni valida IIS/IIC.

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

`human_agreement` y `human_adjudicated` describen procedencia, no una garantía ni una escala universal gold/silver. Una adjudicación puede superar en calidad un acuerdo inicial. Todos los registros siguen `not_audited` en la dimensión de auditoría independiente.

La expansión léxica y su mapeo ontológico tienen estados separados. FAISS propone candidatos pendientes; el umbral 0,70 es similitud, no probabilidad de acierto. Cobertura de asignación no es exactitud.

1. Para decisiones humanas, comenzar por `terminology_mapping.jsonl`.
2. Conservar **concepto y atributos**: `afebril → fiebre` con `polarity: Negado` cambia de significado si se elimina la negación.
3. Para formas y expansiones, usar `lexical_inventory.jsonl`.
4. Si se usan candidatos, filtrar `mappingUsage == "candidate_generation_only"`; las filas `review_only` requieren revisión previa.
5. No elegir automáticamente el sentido más frecuente de expresiones con varios conceptos.

Las frecuencias cuentan registros derivados de anotación, no pacientes, notas únicas, prevalencia ni necesariamente apariciones independientes. Se preservan repeticiones. `occurrenceId` identifica el registro exportado; no enlaza una nota ni paciente.

## Procedencia y límites

La documentación más reciente de origen informa 15 parejas, 15 lotes y 5 notas básicas por lote. Notas únicas, premarcación, muestreo efectivo y detalle por pareja no se verifican con estos archivos. La edición declarada es Argentina 20260520; no se revalidó íntegramente actividad, jerarquía o equivalencia SCTID. Los expedientes éticos e institucionales declarados en la documentación de origen no se incluyen ni se verificaron en esta actualización técnica.

Documentación: [ficha](DATASET_CARD.md), [metodología](METODOLOGIA_Y_PROCEDIMIENTO.md), [campos](ETIQUETAS_Y_CAMPOS.md), [evaluación y concordancia](EVALUACION_Y_CONCORDANCIA.md), [auditoría y pendientes](AUDITORIA_Y_CAMBIOS.md).

## Reproducibilidad

Python 3.10 o posterior; biblioteca estándar, sin dependencias externas:

```bash
python validate_public_release.py
python build_public_mapping_release.py
python validate_public_release.py
```

El constructor regenera agregados, vista léxica, reporte y manifiesto desde las **ocurrencias públicas**. No reconstruye el proceso privado de anotación. El validador comprueba contrato, particiones, campos prohibidos, IDs, agregación, inventario y hashes de bytes exactos. No certifica calidad clínica ni anonimización absoluta de los valores textuales. Configuración Git/CI fuera del inventario de archivos de datos. Finales de línea LF.

Pendientes: auditoría humana independiente, validación ontológica, informe de concordancia con denominadores, aclaración de muestreo/premarcación y casos sin mapeo. Las particiones de benchmark requieren referencia auditada y controles de repetición. No se incorporan notas clínicas. Se conserva el nombre histórico del repositorio para mantener enlaces; README_ORIGINAL.md remite al historial anterior.


## Revisión aceptada por el responsable

El 29/09/2026 Julián Sánchez Viamonte aceptó las propuestas para los 21 registros señalados. REVIEW_DECISIONS.json conserva las decisiones y su alcance; lexical_inventory.jsonl incorpora los ajustes léxicos. Los candidatos originales permanecen para trazabilidad, en review_only, y no se asignan nuevos SCTID sin validación ontológica. Los sentidos expresamente desconocidos o condicionales siguen pendientes. Esta aceptación no equivale a auditoría independiente del recurso.
