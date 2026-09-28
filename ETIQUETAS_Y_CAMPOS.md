# Diccionario de etiquetas y campos

## Correspondencia entre la anotación y la publicación

| Campo de anotación | Campo público |
|---|---|
| `textoLiteral` / `surface` | `surface` |
| `cat` / `clinicalCategory` | `category` |
| `sctid` / `clinicalSctid` | `sctid` |
| `term` / `clinicalTerm` | `term` |
| `pol` / `clinicalPolarity` | `polarity` |
| `cert` / `clinicalCertainty` | `certainty` |
| `temp` / `clinicalTemporality` | `temporality` |
| `suj` / `clinicalSubject` | `subject` |
| `annotation.normalizedKey` | `normalizedKey` |
| `annotation.formType` | `formType` |
| `annotation.senseId` | `senseId` |
| `annotation.proposedExpansion` | `expansion` |
| `annotation.correctedForm` | `correctedForm` |
| `annotation.function` | `function` |
| `annotation.section` | `section` |

`mappingStatus` es una etiqueta de publicación añadida por este release: no reemplaza el `decisionStatus` original, sino que separa evidencia humana de candidatos FAISS. Los identificadores operativos, `sourcePair`, offsets, texto clínico y comentarios de adjudicación se excluyen del payload público.

## Capas de anotación

| Capa | Significado público | Campos principales |
|---|---|---|
| `clinical` | Mención con información clínica y concepto SNOMED CT | `surface`, `category`, `sctid`, `term`, `polarity`, `certainty`, `temporality`, `subject` |
| `lexical` | Abreviatura, sigla, forma breve o variante contextual | `surface`, `normalizedKey`, `formType`, `senseId`, `expansion`, `function`, `section` |

## Clasificación visible de una aparición

- **Solo información clínica:** se conserva la capa clínica.
- **Solo abreviatura contextual:** se conserva la capa léxica.
- **Información clínica + abreviatura contextual:** se conservan ambas capas sobre la misma aparición.
- **Sin valor clínico ni abreviatura (Anular):** se rechaza explícitamente la marca.

## Evidencia y estado de mapeo

| Campo | Valores | Interpretación |
|---|---|---|
| `evidence` | `agreement`, `adjudicated_disagreement`, `mixed` | Procedencia de la evidencia humana agregada |
| `mappingStatus` | `human_agreement` | Acuerdo exacto entre anotadores |
| `mappingStatus` | `human_adjudicated` | Resolución clínica adjudicada |
| `mappingStatus` | `faiss_candidate` | Candidato FAISS con score >= 0,70; pendiente de validación |
| `mappingStatus` | `faiss_candidate_below_threshold` | Candidato conservado para transparencia, no recomendado para uso automático |

## Tipo de forma (`formType`)

| Código | Etiqueta visible |
|---|---|
| `abbreviation` | Abreviatura |
| `acronym` | Acrónimo pronunciable |
| `initialism` | Sigla / inicialismo |
| `alphanumeric` | Forma alfanumérica |
| `symbolic_abbreviation` | Abreviatura simbólica |
| `other` | Otra forma léxica |

## Estado léxico de origen (`decisionStatus`)

| Código | Etiqueta |
|---|---|
| `pending` | Pendiente |
| `resolved` | Sentido resuelto |
| `ambiguous` | Ambigua aun con contexto |
| `unknown` | No puedo determinarla |
| `new_sense_proposed` | Proponer sentido nuevo |
| `form_error` | Forma errónea o corrupta |
| `nonclinical` | Uso no clínico/estructural |
| `rejected` | No es abreviatura ni acrónimo (Anulada) |

## Función (`function`)

| Código | Etiqueta |
|---|---|
| `header` | Encabezado |
| `entity` | Entidad clínica |
| `value` | Valor |
| `result` | Resultado |
| `modifier` | Modificador |
| `structural` | Marca estructural |
| `other` | Otra función |
| `null` | Sin clasificar |

## Categorías clínicas y jerarquías SNOMED

| Categoría | ECL raíz |
|---|---|
| `Hallazgo clínico` | `<<404684003` |
| `Procedimiento` | `<<71388002` |
| `Fármaco` | `<<373873005` |

## Atributos contextuales

- `polarity`: `Activo` / `Negado`.
- `certainty`: `Confirmado` / `Sospecha` / `Diferencial`.
- `temporality`: `Actual` / `Histórico`.
- `subject`: `Paciente` / `Familiar`.

Los códigos de esta tabla describen el contrato de anotación. El mapeo público agrega además `mappingStatus` para impedir que una inferencia automática se interprete como validación clínica.
