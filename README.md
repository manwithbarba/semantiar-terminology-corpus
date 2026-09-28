# SemantIAr — release público de mapeo terminológico

Este directorio es el paquete público autocontenido de `semantiar-terminology-mapping.v1`. Contiene `1365` términos agregados y `1560` ocurrencias publicables; no incluye notas clínicas, identificadores operativos ni material interno de revisión.

## Archivos principales

- `terminology_mapping.jsonl`: una fila por combinación terminológica publicable, con `termId` determinístico.
- `terminology_occurrences.jsonl`: ocurrencias desidentificadas sin identificador público único.
- `SCHEMA_MAPPING.json`: contratos JSON Schema estrictos para ambos JSONL.
- `EXCLUSIONS.json`: conteos agregados de las `86` filas no publicadas.
- `DATASET_CARD.md`: composición, usos previstos, límites y advertencias de privacidad.
- `README_ORIGINAL.md`: documentación metodológica validada. Describe además la estructura del repositorio de trabajo completo; las rutas `public/` y `review/` que allí se mencionan son trazabilidad del proceso y no forman parte de este payload.
- `METODOLOGIA_Y_PROCEDIMIENTO.md` y `ETIQUETAS_Y_CAMPOS.md`: procedimiento y diccionario de datos.
- `RELEASE_MANIFEST.json`: inventario, conteos y SHA-256 de todos los archivos salvo su propio hash, que se excluye para evitar autorreferencia.
- `validate_public_release.py`: verificación reproducible del paquete.

## Validación

Ejecutar `python validate_public_release.py`. Un resultado válido termina con `VALID RELEASE`.

## Advertencias

Los estados FAISS son candidatos pendientes de validación humana y no deben promoverse automáticamente a gold. Las ocurrencias no tienen ID público único: duplicados exactos pueden corresponder a apariciones distintas. Los consumidores deben verificar las condiciones de licencia de SNOMED CT aplicables en su territorio.
