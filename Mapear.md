# Mapear

## SemantIAr: mapeo terminológico rioplatense a SNOMED CT

**Mapear** es la página de entrada del corpus público de SemantIAr. El release reúne formas clínicas y formas breves del español rioplatense vinculadas con SNOMED CT, con estados explícitos para decisiones humanas, adjudicación clínica y candidatos léxicos pendientes de validación.

## Qué contiene

- `terminology_mapping.jsonl`: mapeos terminológicos publicables.
- `terminology_occurrences.jsonl`: ocurrencias desidentificadas.
- `SCHEMA_MAPPING.json`: contratos de datos para los JSONL.
- `DATASET_CARD.md`: composición, usos previstos y límites.
- `METODOLOGIA_Y_PROCEDIMIENTO.md`: procedimiento de construcción y revisión.
- `CITATION.cff`: referencia bibliográfica y autoría.
- `RELEASE_MANIFEST.json`: inventario y hashes SHA-256 del release.

## Uso responsable

Los candidatos `faiss_candidate` y `faiss_candidate_below_threshold` son provisionales y requieren validación humana antes de promoverse a gold. Las ocurrencias no tienen un identificador público único; los duplicados exactos deben conservarse salvo que el consumidor documente otra política.

El paquete no incluye texto clínico libre, identificadores de caso ni material interno de revisión. Los consumidores deben verificar las condiciones de licencia de SNOMED CT aplicables en su territorio.

## Autoría y licencia

Autor principal: **Julián Sánchez Viamonte**, Facultad de Ciencias Médicas, Universidad Nacional de La Plata. El proyecto y sus integrantes se describen en [`INTEGRANTES_PROYECTO.md`](INTEGRANTES_PROYECTO.md).

Los datos de este release se distribuyen bajo **CC BY-SA 4.0**, con las salvedades indicadas en `LICENSE-DATA.txt` y `NOTICE-SNOMED.md`.

Para citar el conjunto, utilizar `CITATION.cff`.
