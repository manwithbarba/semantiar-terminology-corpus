# Metodología y procedimiento de SemantIAr

## 1. Propósito y unidad de publicación

La entrega representa formas clínicas, abreviaturas, siglas y formas breves del español rioplatense vinculadas a conceptos de SNOMED CT. La unidad pública es una combinación terminológica mapeable y, de forma separada, una ocurrencia sin identificadores operativos. No se publican notas clínicas completas, IDs de caso ni códigos de anotador.

## 2. Procedencia y doble ciego

Las fuentes son notas clínicas desidentificadas de la Historia de Salud Integrada. Profesionales de la salud trabajaron de manera independiente. La capa clínica identifica menciones y asigna categoría, SCTID, término y contexto; la capa léxica caracteriza formas breves según su forma, sentido, función, ubicación y pistas.

## 3. Flujo de anotación

1. **Lectura de la nota:** se revisa la nota completa y se registra, cuando corresponde, la especialidad sospechada como pista contextual.
2. **Marcación exhaustiva:** se recorren todas las menciones, se ajustan límites, se incorporan omisiones y se conservan spans superpuestos de forma independiente.
3. **Decisión secuencial:** cada aparición se clasifica como información clínica, forma breve contextual, ambas capas o anulación explícita. La decisión clínica y la léxica pueden coexistir en una misma aparición.

## 4. Adjudicación

Los desacuerdos de límites, presencia, granularidad, concepto o significado local se resuelven mediante adjudicación clínica. La salida distingue los acuerdos humanos (`human_agreement`) de las resoluciones adjudicadas (`human_adjudicated`). Las filas sin superficie o sin mapeo completo no se incorporan al mapeo público; sus conteos quedan documentados en `EXCLUSIONS.json`.

## 5. Normalización léxica asistida

Las formas breves se consultaron contra un índice FAISS con SapBERT. El sentido contextual (`senseId`) se usa como consulta cuando existe; en su defecto se usa la superficie. Los resultados se publican como `faiss_candidate` o `faiss_candidate_below_threshold`, con `inferenceScore` e `inferenceMethod`. Son candidatos provisionales y requieren validación humana.

## 6. Transformación para publicación

El constructor elimina `sourcePair` y cualquier identificador operativo, exige `surface`, `sctid`, `term` y `category`, recalcula `termId` después de todos los enriquecimientos, conserva los atributos contextuales y genera el manifiesto con hashes. La carpeta `review/` permanece fuera del payload público.

## 7. Reproducibilidad

Desde la raíz de la entrega: `python build_public_mapping_release.py`. La salida esperada es `release/`. La validación comprueba JSON Schema, identidad de `termId`, conteos de ocurrencias, hashes del manifiesto y coincidencia exacta con `PUBLIC_RELEASE_ALLOWLIST.txt`.

## 8. Interpretación y límites

Este recurso es un mapeo terminológico de investigación para lookup, normalización y generación de candidatos. No es una distribución completa de SNOMED CT ni una autorización para uso clínico directo. Los consumidores deben verificar las licencias de SNOMED CT y mantener separadas las decisiones humanas de los candidatos automáticos.
