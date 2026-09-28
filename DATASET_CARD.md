# SemantIAr — Mapeo terminológico rioplatense

Versión candidata: `semantiar-terminology-mapping.v1`

Esta entrega publica un mapeo de formas clínicas y formas breves del español rioplatense hacia SNOMED CT Edición Nacional Argentina 20260520. No contiene textos clínicos libres, identificadores de caso ni identificadores de anotadores.

## Contenido

- `1365` entradas agregadas en `terminology_mapping.jsonl`.
- `1560` ocurrencias publicables en `terminology_occurrences.jsonl`.
- `86` ocurrencias excluidas sobre `1646` originales; el detalle agregado está en `EXCLUSIONS.json`.
- `1088` ocurrencias con decisión humana y `472` ocurrencias léxicas con candidato FAISS.
- `6` ocurrencias FAISS por debajo del umbral de 0,70.

## Estados de mapeo

- `human_agreement`: acuerdo exacto entre anotadores.
- `human_adjudicated`: resolución clínica adjudicada.
- `faiss_candidate`: candidato léxico inferido con similitud >= 0,70; requiere validación humana.
- `faiss_candidate_below_threshold`: candidato conservado para transparencia, no recomendado para uso automático.

La etiqueta `mappingStatus` es obligatoria y no debe interpretarse como una garantía clínica. Las filas FAISS incluyen `inferenceScore` e `inferenceMethod`.

## Identidad pública de las ocurrencias

`terminology_occurrences.jsonl` no publica un identificador único de caso, aparición ni anotador. Por privacidad, dos filas exactamente iguales pueden representar apariciones distintas. En esta versión hay `56` repeticiones exactas adicionales, distribuidas en `55` grupos que reúnen `111` filas. No deben deduplicarse salvo que el análisis lo requiera de forma explícita.

## Uso previsto

Diccionarios, lookup terminológico, generación de candidatos y estudios de variación léxica rioplatense. No es una autorización para decisiones clínicas directas ni una distribución completa de SNOMED CT. Cada consumidor debe verificar su licencia SNOMED CT aplicable.

## Exclusiones, privacidad e integridad

Las filas sin `surface`, `sctid`, `term` o `category` no se publican en el mapeo principal. La carpeta interna `review/` y los insumos de adjudicación permanecen fuera de la distribución pública. `SCHEMA_MAPPING.json` rechaza propiedades no declaradas y `validate_public_release.py` controla esquemas, campos sensibles, conteos, agregación, allowlist y hashes.
