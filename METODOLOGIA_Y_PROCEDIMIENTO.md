# Metodología del recurso léxico-terminológico

## Procedencia

Expresiones y formas breves derivadas de anotaciones HSI desidentificadas. El origen declara decisiones independientes y adjudicación por el investigador responsable. Su última descripción informa 15 parejas/15 lotes de 5 notas básicas. Notas únicas y premarcación no son verificables en el payload público. Corpus fuente y recurso derivado son unidades diferentes.

## Transformación v2

Se preservan las superficies, SCTID, términos, atributos y evidencias de 1.560 registros. Se separan 1.088 decisiones humanas y 472 candidatos. No se corrigen códigos por conjetura ni se atribuye validación clínica nueva. Se agregan estados de expansión, mapeo y auditoría, IDs de registros públicos y una categoría de etiqueta normalizada sin certificar jerarquía SNOMED.

La identidad agregada figura en `IDENTITY_FIELDS` del constructor; incluye contexto y score, no representa término único. Las propuestas con umbral bajo, sentido no documentado o discordancia focal detectada quedan en `review_only`. El resto sigue pendiente; no se certifica su corrección. La vista léxica conserva formas y sentidos separadamente del mapeo automático.

## Evidencia, reproducción y pendientes

Acuerdo y adjudicación son procedencia. No se publican nuevas métricas de concordancia: faltan textos, pares, límites y denominadores. SCTID y atributos pueden ser conjuntamente necesarios. Sección y especialidad no sustituyen contexto textual.

`python build_public_mapping_release.py` regenera derivados y manifiesto en la raíz desde las particiones públicas; no accede a notas ni restaura adjudicación privada. `python validate_public_release.py` comprueba coherencia técnica. El schema admite futuras decisiones humanas léxicas, sin que se creen aquí. El constructor no ejecuta inferencia ni adjudicación.

Pendientes: auditoría independiente de expansiones y SCTID, actividad/jerarquía/edición, protocolo de ciego y premarcación, concordancia, casos no mapeables y benchmark independiente. Procedimientos en EVALUACION_Y_CONCORDANCIA.md; no se presentan como evidencia realizada.
