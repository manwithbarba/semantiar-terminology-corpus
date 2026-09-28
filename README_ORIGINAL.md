# Proyecto SemantIAr — Repositorio Terminológico Clínico de notas clínicas des identificadas en Español Rioplatense

 
Versión de salida: `semantiar-terminology-mapping.v1`  
Fecha: `2026-09-28`  
Investigador responsable: **Julián Sánchez Viamonte**  
Filiación: **Facultad de Ciencias Médicas, Universidad Nacional de La Plata (UNLP)**  
Licencia: **Creative Commons Atribución- 4.0 Internacional (CC BY-SA 4.0)**  

---

## 1. Contexto de investigación y justificación científica

El procesamiento del lenguaje natural (PLN) aplicado al ámbito biomédico en el español rioplatense enfrenta desafíos singulares derivados de las prácticas de registro hospitalario: alta frecuencia de abreviaturas locales no estandarizadas, elisiones léxicas, formas telegráficas y dialectos clínicos propios de la región.

En el marco del **Proyecto de Tesis Doctoral SemantIAr** (*Codificación de Texto Clínico a SNOMED CT con Índice de Incertidumbre Semántica en Español Rioplatense*), desarrollado en la **Facultad de Ciencias Médicas de la Universidad Nacional de La Plata (UNLP)**, este repositorio pone a disposición de la comunidad científica un inventario curado de términos clínicos, variantes superficiales y abreviaturas rioplatenses mapeadas a la ontología internacional **SNOMED CT (Edición Nacional Argentina)** en una versión congelada a mayo 2026.

---

## 2. Procedimiento metodológico

### 2.1 Fuente del corpus
Los datos fueron extraídos a partir de **notas clínicas des identificadas obtenidas de la Historia de Salud Integrada (HSI)** de la Provincia de Buenos Aires, comprendiendo episodios ambulatorios y de internación general en múltiples especialidades médicas. La muestra se seleccionó por densidad semántica (básico- avanzado y experto, ver protocolo de muestreo) y se estratificó por modalidad (ambulatorio, internación) así  como efector sanitario. Se buscó optimizar recuperación sin desbalance muestral.

### 2.2 Protocolo de anotación en doble ciego
Profesionales de la salud capacitados (anotadores) realizaron la tarea de identificación de entidades y asignación de códigos ontológicos mediante una plataforma web de anotación clínica con contratos formales de validación. La tarea se organizó en dos capas independientes:
- **Capa clínica:** Identificación de spans de texto que representan tres jerarquías en la ontología de SNOMED: hallazgos clínicos, procedimientos y fármacos, asociándolos a su respectivo identificador de concepto SNOMED CT (`sctid`), término preferido y categoría semántica.
- **Capa léxica:** Delimitación y caracterización contextual de formas breves, siglas, abreviaturas y términos sintácticos rioplatenses, registrando su forma superficial, tipo de forma, función discursiva y sentido contextual clínico (`senseId`).

Los anotadores trabajaron de manera independiente, se constituyeron 14 parejas de anotadores, con 7 muestras en total (una muestra por pareja de anotador) de 5 notas clínicas de nivel básico.

### 2.3 Evaluación de concordancia interanotador
Se compararon de forma reproducible las parejas de anotadores que completaron los mismos conjuntos de casos clínicos. Aquellas menciones donde ambos anotadores coincidieron con exactitud en los límites del span textual y en la codificación ontológica asignada constituyen el subconjunto de consenso directo (**Capa Gold**).

### 2.4 Protocolo de adjudicación arbitral
Ante discrepancias interanotador (desalineación de fronteras de span, divergencias semánticas o niveles disímiles de granularidad ontológica), las filas fueron procesadas mediante un procedimiento de arbitraje clínico ciego. El investigador principal resolvió cada discrepancia aplicando las directrices del manual metodológico del proyecto, registrando la decisión fundamentada (**Capa Silver**).

### 2.5 Normalización léxica asistida mediante FAISS (SapBERT)
A diferencia de la capa clínica, las formas léxicas (abreviaturas, siglas y formas breves rioplatenses) fueron vinculadas a conceptos SNOMED CT mediante inferencia semántica asistida.

Para ello se empleó el servicio de recuperación vectorial del proyecto doctoral (`SapBERT-UMLS-2020AB-all-lang-from-XLMR` sobre el índice denso `snomed_index.faiss` de 555.438 conceptos SNOMED), utilizando como texto de consulta el sentido clínico resuelto en la adjudicación (`senseId`), o la superficie cuando el sentido no estaba definido:

- **Control de calidad:** Se aplicó un umbral de similitud semántica ($\ge 0.70$) que permitió mapear 392 de las 395 formas léxicas (99,2%), preservando sin asignación las 3 formas ambiguas para prevenir falsos positivos.
- **Aviso de inferencia realizada:** Cada registro léxico resultante lleva la marca explícita `decisionStatus: "faiss_inferred_pending_validation"`.
- **Aviso formal:** Este mapeo constituye una **inferencia algorítmica asistida realizada en fase preliminar, pendiente de validación clínica humana**.
- Para especificaciones técnicas adicionales de los parámetros del modelo, consúltese la sección correspondiente en [`public/DATASET_CARD.md`](public/DATASET_CARD.md) y el registro trazable de consultas en [`review/faiss_lexical_inference_audit.json`](review/faiss_lexical_inference_audit.json).

### 2.6 Estratificación de calidad (`silver-gold`) y conversión a Gold Standard
El repositorio se distribuye con la etiqueta de calidad **`silver-gold`**:
- **Gold:** Acuerdos exactos espontáneos entre profesionales de la salud independientes.
- **Silver:** Resoluciones de discrepancias validadas mediante arbitraje clínico documentado.

> **Transición a Gold Standard:** Este paquete representa la fase consolidada de calibración y evaluación. Se prevé que, tras una posterior ronda de auditoría humana independiente sobre el subconjunto adjudicado y las inferencias léxicas, el corpus consolidado sea promovido y publicado en una entrega posterior como **`Gold Standard`** definitivo para PLN clínico rioplatense.

---

## 3. Política de privacidad y desidentificación por diseño

Para salvaguardar el secreto profesional médico y la confidencialidad de los pacientes de acuerdo con las normativas vigentes:
- **No se distribuyen textos clínicos libres completos.**
- Se eliminaron todos los identificadores directos e indirectos: identificadores de paciente (`patientId`), números de documento (`dni`), identificadores de caso (`caseId`, `blindRecordId`), códigos de anotador y fundamentos narrativos de adjudicación.
- La distribución se limita estrictamente a las unidades léxico-terminológicas agregadas: forma superficial (`surface`), forma normalizada, atributos de contexto sintáctico/seccional, código SNOMED CT (`sctid`), término preferido, categoría semántica y frecuencias observadas.

---

## 4. Estructura del repositorio

- `public/terms_repository.jsonl`: inventario agregado y deduplicado de términos clínicos y abreviaturas con metadatos contextuales y ontológicos.
- `public/agreement_occurrences.jsonl`: ocurrencias individuales procedentes de acuerdos exactos entre anotadores independientes (*capa gold*).
- `public/adjudicated_occurrences.jsonl`: ocurrencias individuales procedentes de decisiones de adjudicación documentada (*capa silver*).
- `public/SCHEMA_TERMS.json`: contrato formal JSON Schema (Draft 2020-12) para el repositorio de términos.
- `public/SCHEMA_OCCURRENCES.json`: contrato formal JSON Schema para las ocurrencias individuales.
- `public/DATASET_CARD.md`: ficha técnica con especificaciones de composición, uso previsto, autorizaciones y limitaciones.
- `public/LICENSE-DATA.txt`: términos legales de la licencia Creative Commons Atribución-CompartirIgual 4.0 Internacional (CC BY-SA 4.0).
- `public/NOTICE-SNOMED.md`: especificaciones y alcance sobre propiedad intelectual de la terminología SNOMED CT.
- `public/CITATION.cff`: archivo de metadatos para citación bibliográfica formal (Citation File Format 1.2.0).
- `MANIFEST.json`: manifiesto con sumas de comprobación criptográficas SHA-256 y conteos oficiales de la entrega.
- `review/`: auditoría técnica interna, trazabilidad de procedencia (*lineage*), controles de integridad y log de inferencia FAISS (`faiss_lexical_inference_audit.json`).

---

## 5. Aspectos éticos e institucionales

El proyecto cuenta con el marco de gobernanza requerido para investigación biomédica:
- **Aprobación de dos comités de ética independientes** en investigación en salud.
- **Dictamen favorable del proyecto de investigación doctoral** (Proyecto 238, Facultad de Ciencias Médicas, Universidad Nacional de La Plata - UNLP).
- **Datos derivados de notas clínicas des identificadas** del sistema Historia de Salud Integrada (HSI).
- La documentación formal de respaldo obra en los expedientes institucionales del proyecto doctoral.
