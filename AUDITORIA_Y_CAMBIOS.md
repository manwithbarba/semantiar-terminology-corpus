# Reorganización técnica del 29/09/2026

Base: `bb36b7f7ebabf10c3f2642ef9cf5040366241f70`. Objetivo: recurso léxico-terminológico con evidencia separada, sin incorporar notas clínicas.

## Realizado

- Documentación centrada en unidad, usos y límites reales.
- Preservación de 1.560 registros: 1.088 humanos y 472 candidatos separados. Vista léxica sin inferencia ontológica.
- Estados de expansión, mapeo y auditoría independientes. Ninguna promoción a gold ni corrección clínica por inferencia.
- Atributos/categorías originales preservados; columna de etiquetas normalizadas sin jerarquía certificada.
- IDs públicos sin enlace documental, constructor, reporte, validación sin dependencias, LF y CI.
- Eliminación de rutas obsoletas y afirmaciones de calidad no demostradas; documentación anterior en historial Git.

## Revisión focal

Se conservan los candidatos originales y se marcan `expansion_candidate_semantic_mismatch` y `review_only`:

| Forma | Expansión | SCTID / término candidato | Score |
|---|---|---|---:|
| `3L` | tres litros | `258775009` / femtolitro | 0,7084 |
| `(O2 3 LT)` | Aporte de Oxigeno a 3 litros | `401955005` / tubo de oxígeno, 300 litros | 0,7001 |
| `a/a` | aire ambiente | `224786002` / medio ambiente al aire libre | 0,8751 |

Se observa discordancia entre expansión y descripción publicada. No se ejecuta validación completa contra servidor SNOMED ni auditoría clínica de todos los candidatos. Los restantes siguen pendientes; no se propone reemplazo automático.

## Pendientes

Notas únicas, parejas efectivas, premarcación, muestreo/ciego; resultados y denominadores de concordancia; auditoría humana independiente; edición/actividad/jerarquía/granularidad; exclusiones y abstenciones no disponibles; benchmark con referencia auditada y particiones independientes. Expedientes institucionales no examinados. La reorganización técnica no convierte estas tareas en validaciones realizadas.


## Revisión aceptada por el responsable

El 29/09/2026 Julián Sánchez Viamonte aceptó las propuestas para los 21 registros señalados. REVIEW_DECISIONS.json conserva las decisiones y su alcance; lexical_inventory.jsonl incorpora los ajustes léxicos. Los candidatos originales permanecen para trazabilidad, en review_only, y no se asignan nuevos SCTID sin validación ontológica. Los sentidos expresamente desconocidos o condicionales siguen pendientes. Esta aceptación no equivale a auditoría independiente del recurso.
