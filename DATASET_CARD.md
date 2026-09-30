# Ficha del recurso léxico-terminológico SemantIAr

Versión `semantiar-lexical-terminology.v2`, 29/09/2026. Español clínico rioplatense, derivado de anotaciones HSI, Provincia de Buenos Aires. Responsable: Julián Sánchez Viamonte, FCM UNLP. Edición SNOMED declarada: Argentina 20260520, no revalidada íntegramente en esta actualización.

## Composición y unidad

1.088 registros humanos (210 acuerdos, 878 adjudicados), agregados en 953 entradas; 472 registros FAISS (466 sobre umbral, 6 bajo umbral), agregados en 412 entradas. `lexical_inventory.jsonl` es una vista derivada sin candidatos SNOMED. Conteos en QUALITY_REPORT.json. Unidad: registro derivado de anotación, no documento clínico ni paciente.

Se conservan 1.560 registros publicables de 1.646 originales declarados. 86 exclusiones: 7 sin superficie y 79 sin mapeo completo; estas últimas incluyen 75 acuerdos clínicos y 4 registros léxicos. No se recuperan ni reconstruyen exclusiones. Estos conteos no permiten estimar concordancia.

## Representatividad y calidad

El README más reciente de origen declara 15 parejas/15 lotes de 5 notas básicas. No se verifican notas únicas, independencia de apariciones, premarcación, estratificación efectiva ni selección por efector. La calibración básica no representa automáticamente toda la HSI ni el español rioplatense. Las frecuencias no son prevalencia.

La capa clínica usa tres categorías; las propuestas léxicas abarcan etiquetas heterogéneas. `categoryCanonical` normaliza escritura sin validar pertenencia ontológica; `category` conserva el original. Faltantes de atributos no son clases negativas. Concepto y atributos deben interpretarse conjuntamente.

`mappingValidationStatus`, `lexicalValidationStatus` e `independentAuditStatus` separan vínculo ontológico, expansión y auditoría. Ninguna fila se promueve a auditada aquí. Acuerdo/adjudicación son procedencia, no escala gold/silver. Candidatos separados, sin usarlos como referencia clínica.

## Usos, privacidad y reproducción

Lookup, diccionarios, variantes, expansión y generación de candidatos. Normalización aislada: requiere referencia auditada y particiones independientes. No permite evaluar NER, spans, omisiones, interpretación contextual, IIS/IIC o seguridad clínica, ni autoriza decisiones clínicas directas.

No se agregan notas, IDs documentales fuente, offsets ni anotadores. `occurrenceId` identifica un registro público por contenido y repetición, sin vínculo documental. Controlar claves prohibidas no prueba anonimización absoluta de superficies. Las autorizaciones institucionales son declaradas por el origen y no reexaminadas aquí.

Datos propios CC BY-SA 4.0 sujetos a NOTICE-SNOMED.md. Constructor y validador usan biblioteca estándar. Ver README.md y EVALUACION_Y_CONCORDANCIA.md.


## Revisión aceptada por el responsable

El 29/09/2026 Julián Sánchez Viamonte aceptó las propuestas para los 21 registros señalados. REVIEW_DECISIONS.json conserva las decisiones y su alcance; lexical_inventory.jsonl incorpora los ajustes léxicos. Los candidatos originales permanecen para trazabilidad, en review_only, y no se asignan nuevos SCTID sin validación ontológica. Los sentidos expresamente desconocidos o condicionales siguen pendientes. Esta aceptación no equivale a auditoría independiente del recurso.
