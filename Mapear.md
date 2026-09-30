# Mapear — SemantIAr

## Recurso léxico-terminológico clínico del español rioplatense

Esta es una página de entrada al recurso público derivado de anotaciones clínicas. Publica formas, expansiones y vínculos conceptuales, sin notas clínicas. Ver [README.md](README.md) para alcance y reproducción.

- `terminology_mapping.jsonl` y `terminology_occurrences.jsonl`: decisiones humanas de origen.
- `faiss_candidates.jsonl` y `faiss_candidate_occurrences.jsonl`: propuestas automáticas separadas, pendientes de validación ontológica.
- `lexical_inventory.jsonl`: caracterización léxica, con correcciones aceptadas por el responsable.
- `REVIEW_DECISIONS.json`: 21 decisiones de revisión aceptadas, con candidatos originales preservados para trazabilidad.
- `QUALITY_REPORT.json`: estadísticas descriptivas; no métricas de concordancia ni precisión clínica.
- `SCHEMA_MAPPING.json`, constructor, validador y manifiesto: contrato e integridad técnica.

Las frecuencias cuentan registros derivados de anotación, no pacientes ni notas únicas. Los occurrenceId identifican filas públicas, sin vínculo documental; conservar duplicados. Concepto y atributos se interpretan conjuntamente. Acuerdo y adjudicación son procedencia; no equivalen a auditoría independiente. Las propuestas review_only no se utilizan para generación automática.

Autor: Julián Sánchez Viamonte, Facultad de Ciencias Médicas, UNLP; integrantes en INTEGRANTES_PROYECTO.md. Datos propios CC BY-SA 4.0 sujetos a NOTICE-SNOMED.md. Citar mediante CITATION.cff. Detalles de migración, revisión y tareas pendientes en MIGRATION_V2.md, AUDITORIA_Y_CAMBIOS.md y EVALUACION_Y_CONCORDANCIA.md.
