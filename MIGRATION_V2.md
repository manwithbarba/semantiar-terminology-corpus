# Migración de consumidores a v2

Esta versión cambia el contenido de los archivos principales: `terminology_mapping.jsonl` y `terminology_occurrences.jsonl` contienen exclusivamente decisiones humanas. Para recuperar el universo anterior, unir la partición humana con `faiss_candidates.jsonl` o `faiss_candidate_occurrences.jsonl`, respectivamente. No mezclar candidatos con referencias de evaluación.

Los 1.560 registros originales se preservan, con sus valores, repeticiones y atributos. Se agregan campos obligatorios de validación, uso, auditoría y categorías normalizadas. El esquema v1 no valida filas v2: actualizar al SCHEMA_MAPPING.json de esta versión. Los IDs de entrada mantienen la fórmula anterior; el nuevo occurrenceId solo identifica una fila exportada y no una aparición documental verificable.

Para generación de candidatos, excluir `mappingUsage: review_only`. Para decisiones humanas, mantener atributos y distinguir procedencia de validación independiente. La vista lexical_inventory.jsonl contiene caracterización sin SCTID; no es un conjunto adicional de ocurrencias.

La documentación de origen permanece en el historial Git. No se añaden notas ni contexto textual. No se fabrican filas excluidas, auditorías, métricas de acuerdo ni particiones de prueba.
