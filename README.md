# SemantIAr — Recurso léxico-terminológico clínico del español rioplatense

Versión: `semantiar-lexical-terminology.v2` · datos del 29/09/2026  
Documentación revisada: 13/10/2026  
Responsable: **Julián Sánchez Viamonte**, Facultad de Ciencias Médicas, UNLP.  
Datos propios: **CC BY-SA 4.0**, sujeto a [NOTICE-SNOMED.md](NOTICE-SNOMED.md).

## Qué es

Corpus público de expresiones clínicas y formas breves registradas durante la anotación y recuperación de conceptos clínicos y formas léxicas de notas desidentificadas de la Historia de Salud Integrada de la Provincia de Buenos Aires. Conserva formas, expansiones, decisiones humanas, atributos de significado y propuestas de conceptos SNOMED CT. Su unidad es un registro léxico-terminológico derivado de anotación.

## Acceso, descarga y reutilización

El repositorio es público: el README y los archivos se pueden consultar y descargar gratuitamente, sin iniciar sesión en GitHub. Acceso comprobado el 13/10/2026.

- [Descargar el paquete de la rama main (ZIP)](https://github.com/manwithbarba/semantiar-terminology-corpus/archive/refs/heads/main.zip).
- Para descargar un archivo individual, abrirlo en la tabla siguiente y usar **Raw** o **Download raw file**.
- Los datos propios se distribuyen según [LICENSE-DATA.txt](LICENSE-DATA.txt), que declara **CC BY-SA 4.0**: atribución, enlace a la licencia e indicación de cambios; las adaptaciones deben compartirse bajo la misma licencia. Consultar también las condiciones adicionales allí declaradas.
- El acceso público no concede derechos sobre SNOMED CT. Sus SCTID, descripciones y derivados están sujetos a las condiciones indicadas en [NOTICE-SNOMED.md](NOTICE-SNOMED.md); cada consumidor debe verificar la autorización aplicable.

## Validación reproducible

Con Python 3, desde la carpeta descargada, ejecutar:

```console
python validate_public_release.py
```

No requiere paquetes adicionales. Un resultado válido comienza con `VALID RELEASE`. El validador comprueba inventario, hashes SHA-256, esquemas, particiones, agregación y conteos contra [RELEASE_MANIFEST.json](RELEASE_MANIFEST.json). Esta comprobación técnica no equivale a una auditoría clínica u ontológica independiente.

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

`human_agreement` y `human_adjudicated` describen procedencia. Todos los registros siguen `not_audited` en la dimensión de auditoría independiente.

La expansión léxica y su mapeo ontológico tienen estados separados. FAISS propone candidatos pendientes; el umbral 0,70 es similitud, no probabilidad de acierto. Cobertura de asignación no es exactitud.

1. Para decisiones humanas, comenzar por `terminology_mapping.jsonl`.
2. Conservar **concepto y atributos**: `afebril → fiebre` con `polarity: Negado` cambia de significado si se elimina la negación.
3. Para formas y expansiones, usar `lexical_inventory.jsonl`.
4. Si se usan candidatos, filtrar `mappingUsage == "candidate_generation_only"`; las filas `review_only` requieren revisión previa.
5. No elegir automáticamente el sentido más frecuente de expresiones con varios conceptos.

Las frecuencias cuentan registros derivados de anotación, no pacientes, notas únicas, prevalencia ni necesariamente apariciones independientes. Se preservan repeticiones. `occurrenceId` identifica el registro exportado; no enlaza una nota ni paciente.

## Procedencia y límites

Se reportan 15 parejas, 15 lotes y 5 notas básicas por lote (75 asignaciones de notas; no un total verificado de notas únicas). Notas únicas, premarcación, muestreo efectivo y detalle por pareja no se verifican con estos archivos. La edición declarada es Argentina 20260520.

Documentación: [ficha](DATASET_CARD.md), [metodología](METODOLOGIA_Y_PROCEDIMIENTO.md), [campos](ETIQUETAS_Y_CAMPOS.md), [evaluación y concordancia](EVALUACION_Y_CONCORDANCIA.md), [auditoría y pendientes](AUDITORIA_Y_CAMBIOS.md).

## Revisión aceptada por el responsable

Julián Sánchez Viamonte (investigador principal). La aceptación del 29/09/2026 corresponde a las 21 decisiones documentadas en [REVIEW_DECISIONS.json](REVIEW_DECISIONS.json); no implica auditoría independiente ni aprobación de revisiones documentales posteriores.
