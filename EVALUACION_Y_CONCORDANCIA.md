# Evaluación del recurso léxico-terminológico

## Resultados disponibles y límites

QUALITY_REPORT.json contiene estadísticas descriptivas recalculadas sobre los archivos públicos. No presenta precisión semántica, concordancia interanotador, prevalencia clínica ni validación de incertidumbre. No hay insumos públicos suficientes para calcular esas medidas. Las frecuencias cuentan registros derivados de anotación; no prueban número de pacientes, notas únicas ni apariciones clínicas independientes.

`human_agreement` describe la procedencia de una decisión. No equivale a un gold standard auditado. Una adjudicación fundamentada puede superar en calidad un acuerdo inicial. La calidad independiente se registra por separado en `independentAuditStatus`.

## Informe de concordancia pendiente sobre insumos restringidos

Para cada pareja y lote deben documentarse: notas únicas, unidades anotadas por cada persona, premarcación o marcación libre, reglas de alineación y denominadores. Publicar los resultados previos a adjudicación, separando:

1. Límites exactos: precisión, exhaustividad y F1 con dirección de comparación explícita, o una definición simétrica documentada.
2. Solapamiento parcial, si se utiliza: regla de emparejamiento uno a uno y umbral.
3. Coincidencia SCTID condicionada a fragmentos alineados; reportar también evaluación conjunta de límite y concepto.
4. Coincidencia por atributo: negación, certeza, temporalidad y sujeto; distribución de clases y faltantes.
5. Desacuerdos por omisión, límites, concepto, granularidad y contexto; resultados por pareja y globales.

No dividir acuerdos publicados por registros adjudicados para estimar concordancia. La transformación y las exclusiones alteran las unidades y denominadores. Si se compartieron fragmentos premarcados, el resultado no debe presentarse como evaluación de detección libre.

## Evaluación de normalización aislada

Puede construirse un benchmark con fragmentos ya seleccionados y referencias humanas auditadas. Antes de ello deben revisarse las expresiones que requieren contexto, las equivalencias aceptables y la granularidad esperada. La salida correcta incluye concepto y atributos cuando corresponda. Ejemplo: `afebril` asociado a `fiebre` con negación no autoriza a eliminar el atributo.

No se crean particiones de entrenamiento/prueba en esta entrega: faltan vínculos entre notas y una auditoría independiente. Para futuras particiones léxicas, agrupar variantes por familia, informar conceptos y formas vistos/no vistos y controlar duplicados. Para corpus contextual privado, dividir por documento y controlar textos repetidos. No usar propuestas del mismo SapBERT como referencia independiente para evaluarlo.

## Incertidumbre y abstención

La similitud vectorial no es probabilidad calibrada ni exactitud. El IIS requiere predicciones independientes, referencia humana, distribución de candidatos y análisis del error frente a incertidumbre, cobertura y abstención. La entrega actual aporta vocabulario y candidatos, no valida el IIS ni el IIC.

Conservar en futuras entregas léxicas separadas los casos sin SCTID, ambiguos, desconocidos, estructurales y sin equivalencia adecuada. No reconstruir las 86 exclusiones a partir de conteos: las filas originales no están disponibles aquí.

## Auditoría humana pendiente

Revisar expansión y vínculo ontológico por separado; registrar edición SNOMED, actividad del concepto, jerarquía, especificidad, atributos, equivalencias aceptadas, decisión y fecha. Los identificadores de revisión pueden ser públicos y desvinculados de pacientes. Ninguna auditoría clínica independiente se ha realizado como parte de esta reorganización técnica.
