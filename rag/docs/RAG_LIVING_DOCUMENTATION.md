# 📘 RAG Learning Lab — Documentación viva

> 🎯 **Propósito:** conservar el conocimiento, decisiones de laboratorio, instalación, pruebas, resultados y aprendizajes del frente **Retrieval-Augmented Generation (RAG)** aplicado a EAM / IBM Maximo.
>
> 📍 **Estado:** 🟢 **EN CURSO — Pasos 01 y 02 verificados; Paso 03 retrieval léxico**
>
> 🗓️ **Actualizado:** 2026-09-13

## 🕘 Historial

| Fecha | Cambio |
|---|---|
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

Mecanismo utilizado para obtener el documento desde su sistema de origen. Esta capa cambia según la fuente: filesystem, API, conector, SDK, URL, repositorio documental, etc.

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

Consulta inicial:

```text
procedimiento calibracion PT-201
```

La finalidad **no** es considerar esta estrategia suficiente para RAG empresarial. La usamos como baseline observable para entender qué significa retrieval antes de ocultar el mecanismo dentro de embeddings o frameworks.

Luego se probará una formulación conceptualmente equivalente pero con palabras distintas:

```text
¿Cómo ajusto el transmisor de presión?
```

La hipótesis de aprendizaje es:

```text
búsqueda léxica
→ reconoce principalmente coincidencia de términos

búsqueda semántica con embeddings
→ debería capturar mejor similitud de significado
```

Esta comparación será la puerta de entrada a embeddings.

---

## 11. Casos de prueba que debe soportar el primer LAB

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

## 12. Fuentes, formatos y adquisición

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

## 13. Papel deseable de IBM Maximo

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

Secuencia prevista:

```text
1. Carpeta local                     ✅
2. Chunking visible                  ✅
3. Retrieval léxico baseline         ← AHORA
4. Embeddings / retrieval semántico
5. Vector store / evaluación
6. Simulación de Maximo/doclinks
7. Combinación de contexto EAM + RAG
8. Integración real con Maximo       ← solo si procede
```

La simulación Maximo se construirá cuando lleguemos realmente a ese paso.

---

## 14. Aplicación futura a EAM / IBM Maximo

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

## 15. Decisiones todavía NO tomadas

Aún no se ha decidido:

- proveedor/modelo de embeddings;
- vector database;
- framework RAG;
- LLM específico;
- ejecución local vs API;
- estrategia de chunking definitiva;
- tamaño de `top-k` definitivo;
- framework de evaluación.

Estas decisiones se tomarán durante experimentos concretos y se documentarán con evidencia, no por anticipado.

---

## 16. Siguiente paso

Sincronizar el repositorio mediante **GitHub Desktop** y ejecutar desde la terminal de **VS Code**:

```text
python rag/src/step03_lexical_retrieval.py
```

Después repetir con:

```text
python rag/src/step03_lexical_retrieval.py "¿Cómo ajusto el transmisor de presión?"
```

Compararemos qué chunks devuelve cada consulta y por qué. Solo después introduciremos embeddings y repetiremos el mismo ejercicio con búsqueda semántica.