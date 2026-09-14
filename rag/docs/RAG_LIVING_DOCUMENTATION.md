# 📘 RAG Learning Lab — Documentación viva

> 🎯 **Propósito:** conservar el conocimiento, decisiones de laboratorio, instalación, pruebas, resultados y aprendizajes del frente **Retrieval-Augmented Generation (RAG)** aplicado a EAM / IBM Maximo.
>
> 📍 **Estado:** 🟢 **EN CURSO — Pasos 01–07B verificados; Paso 08 migrado a generación local con Ollama**
>
> 🗓️ **Actualizado:** 2026-09-14

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-14 | 🧪 Se intenta ejecutar el **Paso 08** mediante OpenAI Responses API. La integración alcanza correctamente al proveedor, pero la generación termina con `429 / credit_balance_exhausted`: continuar exige saldo API adicional e independiente de ChatGPT Plus. El usuario decide explícitamente **no realizar pagos adicionales** para terminar el LAB. Se conserva el intento como evidencia y se cambia únicamente el backend generativo a **Ollama + `gemma3:4b` local**, manteniendo índice, retrieval, `Top-k=4`, contexto y prompt. La implementación activa de `step08_generate_grounded_answer.py` pasa a generación local y `rag/requirements.txt` vuelve a contener solo dependencias necesarias para el pipeline local. |
| 2026-09-14 | 🔐 Durante la preparación de la ruta API se expuso accidentalmente una clave en el chat; se revocó y se creó una nueva. No se versionó ninguna clave en GitHub. Como la ruta API queda abandonada para este LAB, la credencial remanente debe eliminarse también del entorno local y revocarse si ya no se usará. |
| 2026-09-13 | ✅ Se completa la baseline de **evaluación del retrieval (Pasos 07A–07B)** con casos A–D. La sensibilidad a `Top-k` muestra cobertura completa desde `k=2` para A, `k=3` para B y `k=4` para C; D sigue sin respuesta documental aunque se amplíe hasta `k=5`. Se adopta **`k=4` solo como baseline temporal de la próxima evaluación de generación**, por ser el menor valor probado que cubre la evidencia esperada de A–C. También se confirma que evaluar únicamente por heading exacto es insuficiente: la cobertura debe considerar grupos de evidencia equivalentes. |
| 2026-09-13 | ✅ Se verifica el **Paso 06**: el índice persistido recupera el `Top-3`, el sistema vuelve desde los vectores al **texto original** de cada chunk, conserva documento/sección/chunk como procedencia y construye un **prompt fundamentado** con instrucciones explícitas de no inventar, declarar evidencia insuficiente y citar `[FUENTE n]`. Se confirma físicamente que los embeddings sirven para localizar evidencia, mientras que el LLM recibiría **pregunta + instrucciones + texto recuperado**, no los vectores. Se abre la etapa de **generación fundamentada**. |
| 2026-09-13 | ✅ Se verifica el **Paso 05** completo. La fase de indexación persiste 11 embeddings de 384 dimensiones en `embeddings.npy` junto con `metadata.json` y `manifest.json`; la fase de consulta posterior carga esos vectores y reproduce exactamente el mismo `Top-3` del Paso 04b generando únicamente el embedding de la pregunta. Se confirma experimentalmente la separación entre **INDEXACIÓN** y **CONSULTA**. Se abre el **Paso 06** para hacer visible la construcción del contexto y del prompt fundamentado antes de llamar a un LLM. |
| 2026-09-13 | ✅ Se verifica el **Paso 04 / 04b**: embeddings locales de 384 dimensiones, similitud semántica y `Top-k` funcionan. Las pruebas muestran que similitud temática no equivale necesariamente a capacidad de responder y que estructura/identificación pueden competir con contenido operativo. Al excluir solo estructura/metadata, el `Top-3` queda formado por seguridad antes de calibrar, seguridad previa y procedimiento de calibración. Se abre el **Paso 05** para persistir vectores + metadata localmente y separar claramente indexación de consulta, todavía sin vector database. |
| 2026-09-13 | ✅ Se verifica el **Paso 03**: el retrieval léxico funciona por coincidencia de términos, pero una formulación equivalente puede dejar fuera del `Top-k` el chunk realmente útil. |
| 2026-09-13 | ✅ Se verifica en el portátil el **Paso 02**: lectura y chunking visible. El manual `PT-201` se divide en 9 chunks usando encabezados Markdown. Se abre el **Paso 03** con retrieval léxico mínimo para observar primero búsqueda por palabras y sus limitaciones antes de introducir embeddings. |
| 2026-09-12 | Se separan los documentos fuente en `rag/data/source_documents/` para no mezclarlos con `docs/` ni `src/`. Se formaliza el principio de que **la adquisición cambia según la fuente**, mientras que extracción, normalización, chunking, indexación y retrieval deben permanecer desacoplados y reutilizables. |
| 2026-09-12 | Se corrige la secuencia práctica: las primeras pruebas RAG usarán una **carpeta local del portátil** como fuente. IBM Maximo queda como deseable posterior, primero simulado y eventualmente real. Se elimina la simulación Maximo creada prematuramente y se reutilizan únicamente los documentos sintéticos locales. |
| 2026-09-12 | Creación inicial del documento vivo del RAG Learning Lab. Se define el problema, el modelo mental, la pregunta guía y el plan incremental de aprendizaje. |

---

## 1. Problema que queremos resolver

Un LLM puede responder usando conocimiento aprendido durante su entrenamiento y el contexto que recibe en la conversación, pero no debe asumirse que conoce de forma fiable:

- el manual concreto de un equipo;
- la última versión de un procedimiento;
- instrucciones internas de mantenimiento;
- límites, tolerancias o advertencias específicas de un fabricante;
- documentación privada o no incluida en su entrenamiento.

Para este laboratorio queremos responder preguntas como:

```text
¿Cómo calibro este equipo según su manual?
```

La respuesta correcta debe depender del contenido recuperado desde el documento, no de memoria genérica del modelo.

---

## 2. Qué es RAG

**Retrieval-Augmented Generation** combina dos pasos:

```text
RETRIEVAL
buscar y recuperar conocimiento relevante

        +

GENERATION
usar ese conocimiento como contexto para que el LLM responda
```

Modelo mental:

```text
Documentos
   ↓
preparar / dividir
   ↓
indexar para búsqueda
   ↓
Pregunta del usuario
   ↓
recuperar fragmentos relevantes
   ↓
Pregunta + contexto recuperado
   ↓
LLM
   ↓
Respuesta fundamentada
```

La idea esencial es:

> **el modelo no necesita “memorizar” el manual; necesita recibir en el momento adecuado los fragmentos relevantes del manual.**

---

## 3. Qué NO es RAG

RAG no significa:

- entrenar de nuevo el LLM;
- fine-tuning del modelo;
- cargar un PDF completo en cada prompt necesariamente;
- garantizar por sí solo ausencia de alucinaciones;
- sustituir la necesidad de evaluar la calidad de los documentos;
- convertir automáticamente al sistema en un agente.

RAG es principalmente un patrón de **recuperación + contexto + generación**.

---

## 4. Por qué un LLM solo no basta para este caso

Supongamos que preguntamos:

```text
¿Cuál es el procedimiento exacto de calibración del activo PT-201?
```

Sin el manual correcto, el LLM podría:

- dar una respuesta genérica;
- mezclar conocimiento de equipos distintos;
- inventar valores o pasos plausibles;
- no conocer una revisión reciente del procedimiento.

Con RAG buscamos este flujo:

```text
Pregunta
   ↓
recuperar sección correcta del manual
   ↓
entregar esa evidencia al LLM
   ↓
responder usando solo la evidencia disponible
   ↓
mostrar fuente / sección utilizada
```

---

## 5. Componentes que estudiaremos

### 5.1 Documento fuente

Manual, procedimiento, instructivo, boletín técnico u otra fuente de conocimiento.

### 5.2 Adquisición / acceso

Mecanismo utilizado para obtener el documento desde su fuente. Esta capa cambia según el origen: filesystem, API, conector, SDK, URL, repositorio documental, etc.

### 5.3 Extracción

Conversión del documento a contenido utilizable por el sistema.

### 5.4 Chunking

División del documento en fragmentos manejables llamados **chunks**.

### 5.5 Embeddings

Representaciones numéricas que permiten comparar similitud semántica entre textos.

### 5.6 Índice / vector store

Estructura donde se almacenan representaciones y metadatos para recuperar información.

### 5.7 Retriever

Componente que recibe una consulta y devuelve los fragmentos considerados más relevantes.

### 5.8 Contexto

Fragmentos recuperados que se incorporan a la petición enviada al LLM.

### 5.9 Generación

El LLM utiliza pregunta + contexto para producir la respuesta.

### 5.10 Grounding / citas

Capacidad de vincular la respuesta con la evidencia utilizada.

### 5.11 Evaluación

Comprobación de que:

- se recuperó el fragmento correcto;
- la respuesta está respaldada por la fuente;
- el sistema reconoce cuándo no tiene evidencia suficiente.

---

## 6. Pipeline inicial de referencia

```text
FUENTE
  ↓ acceso específico
DOCUMENTO + METADATOS
  ↓
extraer / normalizar
  ↓
crear chunks
  ↓
generar embeddings
  ↓
guardar/indexar
  ↓

PREGUNTA
  ↓
generar representación de consulta
  ↓
buscar chunks similares
  ↓
seleccionar top-k
  ↓
construir contexto
  ↓
LLM
  ↓
RESPUESTA + EVIDENCIA
```

Este es el pipeline típico que iremos desmontando y probando pieza por pieza.

**Principio de diseño:** la capa de acceso a la fuente puede cambiar; las etapas posteriores deberían depender de una representación común de documento + metadatos, no del sistema de origen.

---

## 7. Enfoque metodológico del laboratorio

No empezaremos con frameworks complejos ni con “Agentic RAG”.

Secuencia acordada:

```text
entender
→ observar manualmente
→ construir mínimo
→ probar
→ medir
→ cambiar una variable
→ volver a probar
→ documentar
```

La prioridad es saber **qué está ocurriendo y por qué**, no conseguir rápidamente una demo sofisticada difícil de explicar.

---

## 8. Paso 01 — Fuente local y descubrimiento de documentos

Las primeras prácticas usan una **carpeta local del portátil** como fuente de documentos.

Razón:

- elimina inicialmente conectores y autenticación;
- hace visible cada paso del pipeline;
- permite depurar fácilmente;
- nos deja concentrarnos en RAG, no en integración de sistemas.

Carpeta reproducible:

```text
rag/data/source_documents/
```

Separación:

```text
rag/docs/                  → documentación SOBRE el laboratorio
rag/src/                   → código fuente del laboratorio
rag/data/source_documents/ → documentos QUE CONSUME el RAG
```

Documentos sintéticos iniciales:

```text
manual_transmisor_PT201.md
procedimiento_seguridad_instrumentacion.md
```

Script:

```text
rag/src/step01_discover_documents.py
```

### Resultado

✅ **VERIFICADO en el portátil** el 2026-09-12.

El script encontró correctamente los dos documentos desde `rag/data/source_documents/` y mostró sus rutas y formatos.

Este paso todavía no realiza retrieval; valida la adquisición local más simple.

---

## 9. Paso 02 — Lectura y chunking visible

Script:

```text
rag/src/step02_read_and_chunk.py
```

Baseline deliberadamente simple:

```text
Markdown (.md) → un chunk por sección/encabezado
Texto (.txt)    → un chunk por bloque separado por línea en blanco
```

Todavía no intervienen embeddings ni búsqueda semántica.

### Resultado observado

✅ **VERIFICADO en el portátil** el 2026-09-12.

El manual:

```text
manual_transmisor_PT201.md
```

produjo:

```text
9 chunks
```

Esto permitió observar físicamente la transición:

```text
DOCUMENTO COMPLETO
      ↓
SECCIONES CON SIGNIFICADO
      ↓
CHUNKS INDEPENDIENTES
```

La lección importante es que el retriever futuro no buscará necesariamente sobre “el PDF entero”, sino sobre unidades de contenido recuperables. La forma de dividirlas influirá directamente en la calidad posterior.

---

## 10. Paso 03 — Retrieval léxico mínimo

Antes de embeddings introducimos una baseline extremadamente simple de recuperación por palabras.

Script:

```text
rag/src/step03_lexical_retrieval.py
```

Funcionamiento:

```text
pregunta
  ↓
normalizar / tokenizar palabras
  ↓
comparar con palabras de cada chunk
  ↓
score = cantidad de términos coincidentes
  ↓
ordenar
  ↓
Top-k chunks
```

### Resultado observado

✅ **VERIFICADO**.

La consulta:

```text
procedimiento calibracion PT-201
```

funciona razonablemente porque existen coincidencias literales.

Al usar:

```text
¿Cómo ajusto el transmisor de presión?
```

se observa que el algoritmo reconoce `transmisor` y `presión`, pero no entiende equivalencias como:

```text
ajusto ≈ ajustar
ajustar ≈ calibrar
```

El chunk de calibración puede quedar fuera del `Top-3` aunque contenga la respuesta.

**Lección:** que la información exista en los documentos no significa que el LLM vaya a recibirla; el retrieval debe encontrar primero la evidencia correcta.

---

## 11. Paso 04 — Embeddings y retrieval semántico

Scripts:

```text
rag/src/step04_semantic_retrieval.py
rag/src/step04b_semantic_retrieval_content_filter.py
```

Modelo de laboratorio:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

Características observadas:

```text
14 chunks evaluados inicialmente
384 dimensiones por embedding
cosine similarity mediante vectores normalizados
Top-k = 3
embeddings calculados todavía en RAM
```

### 11.1 Primera consulta

```text
¿Cómo ajusto el transmisor de presión?
```

El chunk **4. Procedimiento de calibración** quedó en:

```text
#06 | similarity=0.3804
```

mientras chunks de título, identificación y seguridad quedaron por encima.

### 11.2 Consulta con intención procedural explícita

```text
¿Qué pasos debo seguir para ajustar correctamente el transmisor de presión PT-201?
```

El chunk de calibración subió a:

```text
#04 | similarity=0.5694
```

Esto demuestra que la formulación de la consulta afecta el ranking.

### 11.3 Consulta sin identificador del activo

```text
¿Qué pasos debo seguir para ajustar correctamente un transmisor de presión?
```

El chunk de calibración quedó en:

```text
#05 | similarity=0.4643
```

La hipótesis de que quitar `PT-201` mejoraría automáticamente el ranking **no se confirmó**. En cambio, quedaron arriba contenidos de seguridad relacionados con la intervención/calibración.

### 11.4 Lección sobre similarity

Un valor como:

```text
similarity = 0.6545
```

**no significa 65,45 % de probabilidad de ser la respuesta correcta**. Es una medida de proximidad relativa en el espacio vectorial del modelo.

También se confirma:

```text
similitud semántica
≠
capacidad garantizada de responder
```

El embedding puede identificar muy bien el **tema** sin priorizar exactamente el fragmento que un humano considera más útil para responder.

---

## 12. Paso 04b — Separar estructura/metadata de contenido recuperable

Se mantiene deliberadamente:

```text
mismo modelo
mismos documentos
mismo chunking
misma consulta
mismo Top-k
```

Solo cambia el conjunto elegible para retrieval.

En este experimento se excluyen:

```text
chunk 1 de cada documento → estructura/título/aviso
sección Identificación    → metadata
```

No se eliminan del documento. Simplemente no compiten en el ranking semántico de contenido operativo.

Resultado observado:

```text
#01 | 0.6545 | Antes de calibrar un transmisor de presión
#02 | 0.5852 | Seguridad previa
#03 | 0.4643 | Procedimiento de calibración
```

✅ **VERIFICADO**.

La respuesta potencial ya recibe un conjunto mucho más útil de candidatos:

```text
seguridad
+
seguridad específica previa
+
procedimiento operativo
```

### Aprendizaje de diseño

El experimento muestra la utilidad de distinguir:

```text
ESTRUCTURA / METADATA
→ título
→ activo
→ sitio
→ revisión
→ tipo

CONTENIDO RECUPERABLE
→ seguridad
→ inspección
→ calibración
→ criterio de aceptación
→ troubleshooting
```

En EAM, datos como:

```text
assetnum = PT-201
siteid   = PLANTA1
revision = 4
```

pueden servir como contexto o filtros, mientras el retrieval semántico se concentra en conocimiento operativo.

**Importante:** la regla actual `chunk 1` / `Identificación` es una heurística pedagógica del LAB, no una decisión de arquitectura productiva.

---

## 13. Paso 05 — Índice vectorial persistente mínimo

Hasta el Paso 04 los embeddings de los documentos se calculaban en cada ejecución y desaparecían al terminar el proceso.

El Paso 05 separa dos momentos:

```text
INDEXACIÓN
Documentos
   ↓
chunks recuperables
   ↓
embeddings
   ↓
guardar vectores + metadata

CONSULTA
Pregunta
   ↓
embedding de la pregunta
   ↓
comparar contra vectores ya guardados
   ↓
Top-k
```

Scripts:

```text
rag/src/step05_build_vector_index.py
rag/src/step05_query_vector_index.py
```

Artefactos generados localmente:

```text
rag/data/vector_index/embeddings.npy
rag/data/vector_index/metadata.json
rag/data/vector_index/manifest.json
```

La carpeta está ignorada por Git porque contiene **artefactos derivados/regenerables**, no documentación fuente ni código.

Este paso utiliza archivos NumPy + JSON como índice pedagógico mínimo. **No es todavía una vector database**. La finalidad es entender persistencia e indexación antes de introducir un producto especializado.

### 13.1 Resultado de indexación

✅ **VERIFICADO**.

```text
chunks indexados: 11
dimensiones: 384
```

Los embeddings quedan persistidos en `embeddings.npy`; `metadata.json` mantiene la correspondencia entre cada fila vectorial y el texto/documento/sección originales; `manifest.json` registra el modelo y propiedades básicas del índice.

### 13.2 Resultado de consulta

✅ **VERIFICADO**.

La consulta:

```text
¿Qué pasos debo seguir para ajustar correctamente un transmisor de presión?
```

produce desde el índice persistido exactamente:

```text
#01 | 0.6545 | Antes de calibrar un transmisor de presión
#02 | 0.5852 | Seguridad previa
#03 | 0.4643 | Procedimiento de calibración
```

Es el mismo ranking del Paso 04b.

La diferencia no está en el significado ni en el ranking, sino en **cuándo se realiza el trabajo**:

```text
Paso 04b
→ embeddings de documentos + embedding de pregunta se calculan en la ejecución

Paso 05B
→ embeddings de documentos ya existen en disco
→ solo se calcula el embedding de la pregunta
```

### Aprendizaje de diseño

> **Persistir el índice no cambia qué significa el contenido; separa y reutiliza el trabajo de indexación para las consultas posteriores.**

---

## 14. Paso 06 — Construcción de contexto fundamentado

Hasta el Paso 05 el retrieval termina en una lista de chunks relevantes. El Paso 06 hace explícito cómo esos chunks vuelven a convertirse en **texto de contexto** antes de la generación.

Script:

```text
rag/src/step06_build_grounded_context.py
```

Flujo:

```text
PREGUNTA
   ↓
embedding de consulta
   ↓
índice persistido
   ↓
Top-k
   ↓
metadata / texto original
   ↓
CONTEXTO RECUPERADO
   ↓
PROMPT FUNDAMENTADO
   ↓
LLM   ← todavía no se llama en este paso
```

El prompt pedagógico incluye reglas explícitas:

```text
- responder únicamente con base en el contexto recuperado;
- no inventar pasos, valores ni condiciones;
- declarar evidencia insuficiente cuando corresponda;
- citar [FUENTE 1], [FUENTE 2], etc.
```

### 14.1 Resultado observado

✅ **VERIFICADO**.

Para la consulta:

```text
¿Qué pasos debo seguir para ajustar correctamente un transmisor de presión?
```

se recuperó exactamente el mismo `Top-3` del Paso 05:

```text
#01 | 0.6545 | Antes de calibrar un transmisor de presión
#02 | 0.5852 | Seguridad previa
#03 | 0.4643 | Procedimiento de calibración
```

A continuación el sistema reconstruyó el contexto con el **texto original** de cada chunk y su procedencia:

```text
[FUENTE 1]
Documento + sección + chunk + contenido

[FUENTE 2]
Documento + sección + chunk + contenido

[FUENTE 3]
Documento + sección + chunk + contenido
```

Finalmente construyó el prompt:

```text
INSTRUCCIONES
+
PREGUNTA
+
CONTEXTO RECUPERADO
```

### Aprendizaje de diseño

> **El embedding no viaja al LLM como respuesta ni como contexto. Su función fue localizar la evidencia; el LLM recibe el texto original recuperado, acompañado de instrucciones y procedencia.**

Este paso completa físicamente el puente entre **retrieval** y **generation**.

---

## 15. Paso 07 — Baseline de evaluación del retrieval

Antes de conectar un LLM se creó una pequeña baseline reproducible con cuatro tipos de caso:

```text
A. respuesta presente
B. formulación distinta
C. información repartida
D. respuesta inexistente
```

Artefactos:

```text
rag/data/evaluation_cases.json
rag/src/step07_evaluate_retrieval_cases.py
rag/src/step07b_evaluate_topk_sensitivity.py
```

### 15.1 Paso 07A — casos A–D

Resultados iniciales con `Top-k = 3`:

```text
Caso A → evidencia esperada recuperada
Caso B → evidencia esperada recuperada
Caso C → recuperación parcial; seguridad previa fuera del Top-3
Caso D → existe Top-k aunque la respuesta no está documentada
```

El Caso D confirma:

```text
Top-k encontrado
≠
respuesta encontrada
```

Además, una similarity relativamente alta no demuestra suficiencia de evidencia: el Caso D obtuvo un primer candidato de `0.5414` sin contener el dato solicitado.

### 15.2 Diagnóstico del Caso C

Ranking relevante:

```text
#1 | 0.6864 | Inspección previa
#2 | 0.6438 | Procedimiento de calibración
#3 | 0.4909 | Criterio de aceptación
#4 | 0.4400 | Antes de calibrar un transmisor de presión
#5 | 0.4209 | Seguridad previa
```

Esto muestra que evaluar únicamente por un heading exacto puede ser demasiado rígido. Se introducen **grupos de evidencia**, donde distintas secciones pueden aportar evidencia equivalente para una necesidad concreta.

Para el Caso C se evalúan tres grupos:

```text
1. inspección previa
2. seguridad previa
3. procedimiento de calibración
```

### 15.3 Paso 07B — sensibilidad a Top-k

Se mantiene fijo:

```text
modelo
embeddings
corpus
consultas
```

y solo se varía:

```text
k = 1, 2, 3, 4, 5
```

Resultado:

```text
Caso A → cobertura completa desde k=2
Caso B → cobertura completa desde k=3
Caso C → cobertura completa desde k=4
Caso D → sigue sin respuesta documental; aumentar k no crea evidencia inexistente
```

Por tanto, para la próxima evaluación de generación se adopta temporalmente:

```text
Top-k = 4
```

porque es el menor valor probado que cubre toda la evidencia esperada de A–C en este corpus.

**Importante:** `k=4` es solo una baseline pedagógica del LAB. No existe un `Top-k` universalmente correcto; aumentar `k` puede mejorar recall/cobertura, pero también añade ruido, tokens y coste.

---

## 16. Paso 08 — Generación fundamentada

Objetivo: cerrar el circuito RAG añadiendo un LLM real **sin cambiar lo que ya fue verificado** en retrieval.

Contrato del paso:

```text
índice persistido
   ↓
retrieval semántico
   ↓
Top-k = 4
   ↓
texto original + procedencia
   ↓
prompt fundamentado
   ↓
LLM
   ↓
respuesta + citas / abstención
```

Script activo:

```text
rag/src/step08_generate_grounded_answer.py
```

### 16.1 Primer intento — API externa

Se preparó inicialmente OpenAI Responses API para aislar la generación sin añadir infraestructura local. La configuración llegó correctamente hasta la llamada al proveedor, pero la ejecución devolvió:

```text
429
credit_balance_exhausted
```

Aprendizajes:

```text
ChatGPT Plus
≠
saldo de OpenAI API
```

La API se factura por separado. Como el objetivo del LAB no justifica realizar pagos adicionales, se decide **no añadir crédito** y abandonar esta ruta como camino activo.

El intento sigue siendo útil porque demostró que:

```text
retrieval + contexto + prompt
```

estaban construidos correctamente antes de la llamada generativa; el fallo estaba exclusivamente en la capa de facturación/API.

### 16.2 Decisión — generación local

Se cambia una sola variable conceptual:

```text
ANTES
backend generativo = API externa

AHORA
backend generativo = LLM local mediante Ollama
```

Se mantienen:

```text
mismo índice
mismo embedding model
mismo retrieval
mismo Top-k = 4
mismo contexto
mismo prompt fundamentado
mismos casos A–D
```

Baseline local:

```text
runtime: Ollama
modelo:  gemma3:4b
```

`gemma3:4b` es una **baseline de laboratorio**, no una decisión de arquitectura de AI-EAM-MAXIMO. El modelo puede sustituirse mediante:

```text
OLLAMA_MODEL
```

sin cambiar el pipeline RAG.

La implementación usa el comando local `ollama run`, por lo que no requiere SDK generativo adicional, API key ni coste por consulta.

### 16.3 Qué evaluaremos

Primero se ejecutará el **Caso C**, porque exige combinar inspección, seguridad y procedimiento. Después se ejecutará el **Caso D**, donde el comportamiento correcto es abstenerse de inventar.

Criterios:

```text
groundedness         → ¿usa solo evidencia recuperada?
completeness         → ¿cubre la evidencia necesaria?
citation correctness → ¿cita [FUENTE n] coherentemente?
abstention           → ¿evita inventar cuando no existe respuesta?
```

Este paso demostrará además un principio importante:

> **El mecanismo RAG puede mantenerse estable mientras cambia el proveedor o runtime generativo.**

---

## 17. Casos de prueba que debe soportar el primer LAB

### Caso A — respuesta presente

La respuesta aparece explícitamente en el documento.

### Caso B — formulación distinta

La pregunta usa palabras diferentes a las del manual, para comprobar recuperación semántica.

### Caso C — información repartida

La respuesta requiere combinar más de un fragmento o más de un documento.

### Caso D — respuesta inexistente

La documentación disponible no contiene la respuesta.

Resultado esperado:

```text
No existe evidencia suficiente en la documentación disponible.
```

Este caso será especialmente importante para controlar alucinaciones.

---

## 18. Fuentes, formatos y adquisición

RAG no depende de un único formato ni de un único repositorio documental.

Fuentes posibles:

```text
Windows / Linux filesystem
Documentum
SharePoint
web interna
object storage
IBM Maximo / Maximo Manage
otros repositorios documentales
```

Formatos posibles, según el parser disponible:

```text
PDF
DOCX
TXT
Markdown
HTML
CSV
imágenes escaneadas + OCR
otros formatos convertibles a contenido utilizable
```

La **forma de adquirir** el documento sí depende del origen:

```text
Windows / Linux → filesystem
Documentum      → API / conector
SharePoint      → API / conector
Object storage  → SDK / API
IBM Maximo      → metadata/doclinks + recuperación del archivo o URL
```

Después buscamos normalizar todas esas entradas hacia un contrato común:

```text
DOCUMENTO
+ contenido extraído
+ metadatos
+ identificación de fuente
```

A partir de ahí, el resto del pipeline puede ser compartido:

```text
normalización
→ chunking
→ embeddings
→ índice
→ retrieval
→ generación
```

Esto evita construir un RAG distinto para cada sistema fuente.

---

## 19. Papel deseable de IBM Maximo

IBM Maximo es el **ejemplo EAM deseable para una fase posterior**, no la fuente inicial del LAB.

Conceptualmente:

```text
Activo en Maximo
      ↓
documentos enlazados / metadata
      ↓
localizar documento físico o URL
      ↓
extraer contenido
      ↓
RAG
```

Maximo puede actuar como **catálogo/contexto EAM** del documento, aunque el archivo físico pueda residir en filesystem, object storage u otro repositorio.

Metadatos potencialmente útiles:

```text
assetnum
siteid
document_id
tipo_documento
revision
vigencia
ruta / URL
source_system
```

Secuencia vigente:

```text
1. Carpeta local                              ✅
2. Chunking visible                           ✅
3. Retrieval léxico baseline                  ✅
4. Embeddings / retrieval semántico           ✅
5. Índice vectorial persistente mínimo        ✅
6. Construcción de contexto fundamentado      ✅
7. Baseline de evaluación del retrieval       ✅
8. Generación fundamentada local              ← AHORA
9. Simulación de Maximo/doclinks
10. Combinación de contexto EAM + RAG
11. Integración real con Maximo                ← solo si procede
```

La simulación Maximo se construirá cuando lleguemos realmente a ese paso.

---

## 20. Aplicación futura a EAM / IBM Maximo

Fuentes candidatas de conocimiento:

- manuales de equipos;
- procedimientos de mantenimiento;
- instrucciones de calibración;
- troubleshooting;
- normas internas;
- boletines técnicos;
- documentación de seguridad;
- estándares de mantenimiento.

Ejemplo futuro combinado:

```text
“La bomba B-201 presenta alta temperatura.
¿Tiene OTs abiertas y qué indica su manual que debo revisar?”

MCP → activo / OTs / historial desde Maximo
RAG → manual / procedimiento
LLM → integra la evidencia
```

Esta combinación es futura; primero se validará RAG por separado.

---

## 21. Decisiones todavía NO tomadas

Para **este LAB** sí se ha decidido temporalmente:

```text
generación → local mediante Ollama
modelo baseline → gemma3:4b
Top-k de evaluación → 4
```

Aún no se ha decidido para una solución futura/productiva:

- proveedor/modelo de embeddings;
- vector database dedicada;
- framework RAG;
- LLM específico de producción;
- ejecución local vs API en producción;
- estrategia de chunking definitiva;
- tamaño de `top-k` definitivo;
- framework de evaluación definitivo.

El modelo `paraphrase-multilingual-MiniLM-L12-v2`, el índice NumPy/JSON, `Top-k = 4`, Ollama y `gemma3:4b` son **baselines de aprendizaje del LAB**, no decisiones de arquitectura de AI-EAM-MAXIMO.

---

## 22. Siguiente paso

Antes de instalar el runtime local conviene cerrar la ruta API que ya no se utilizará:

```text
1. revocar/eliminar la API key actual si no se usará
2. eliminar OPENAI_API_KEY del entorno de usuario de Windows
```

Después:

```text
3. instalar Ollama para Windows
4. verificar: ollama --version
5. descargar una sola vez: ollama pull gemma3:4b
6. ejecutar: python rag/src/step08_generate_grounded_answer.py
```

La consulta por defecto será el **Caso C**. Si la generación resulta correctamente fundamentada, se repetirá con:

```text
¿Cuál es el par de apriete de los bornes eléctricos del PT-201?
```

para verificar el **Caso D — abstención**.
