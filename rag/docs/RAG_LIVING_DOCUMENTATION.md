# 📘 RAG Learning Lab — Documentación viva

> 🎯 **Propósito:** conservar el conocimiento, decisiones de laboratorio, instalación, pruebas, resultados y aprendizajes del frente **Retrieval-Augmented Generation (RAG)** aplicado a EAM / IBM Maximo.
>
> 📍 **Estado:** 🟢 **EN CURSO — etapa conceptual + primer experimento**
>
> 🗓️ **Actualizado:** 2026-09-12

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-12 | Se adopta IBM Maximo como referencia EAM para el descubrimiento de documentos del primer experimento. Se documenta el modelo multi-fuente/multi-formato y se crean datos/documentos sintéticos para probar primero el descubrimiento antes del retrieval semántico. |
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

### 5.2 Extracción

Conversión del documento a contenido utilizable por el sistema.

### 5.3 Chunking

División del documento en fragmentos manejables llamados **chunks**.

### 5.4 Embeddings

Representaciones numéricas que permiten comparar similitud semántica entre textos.

### 5.5 Índice / vector store

Estructura donde se almacenan representaciones y metadatos para recuperar información.

### 5.6 Retriever

Componente que recibe una consulta y devuelve los fragmentos considerados más relevantes.

### 5.7 Contexto

Fragmentos recuperados que se incorporan a la petición enviada al LLM.

### 5.8 Generación

El LLM utiliza pregunta + contexto para producir la respuesta.

### 5.9 Grounding / citas

Capacidad de vincular la respuesta con la evidencia utilizada.

### 5.10 Evaluación

Comprobación de que:

- se recuperó el fragmento correcto;
- la respuesta está respaldada por la fuente;
- el sistema reconoce cuándo no tiene evidencia suficiente.

---

## 6. Pipeline inicial de referencia

```text
MANUAL
  ↓
extraer texto
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

## 8. Primer experimento previsto

Objetivo:

> construir un RAG pequeño donde podamos ver claramente qué documentos se descubren y qué fragmentos se recuperan antes de que el LLM genere la respuesta.

Queremos poder observar algo como:

```text
Activo en Maximo:
PT-201

Documentos enlazados:
1. Manual técnico
2. Procedimiento de seguridad

Pregunta:
¿Cómo calibro PT-201?

Chunks recuperados:
1. manual — procedimiento de calibración
2. manual — criterio de aceptación
3. procedimiento — seguridad previa

Respuesta:
...

Fuentes utilizadas:
...
```

No consideraremos exitoso el experimento solo porque la respuesta “suene bien”. Primero debe recuperarse evidencia apropiada.

---

## 9. Casos de prueba que debe soportar el primer LAB

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

## 10. Fuentes, formatos y papel de IBM Maximo

RAG no depende de un único formato ni de un único repositorio documental.

Una arquitectura empresarial puede recibir documentos desde:

```text
Windows / Linux filesystem
Documentum
SharePoint
web interna
object storage
IBM Maximo / Maximo Manage
otros repositorios documentales
```

Los formatos pueden incluir, según el parser disponible:

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

El patrón general es:

```text
FUENTE
  ↓
CONECTOR / ACCESO
  ↓
EXTRACCIÓN / PARSING
  ↓
NORMALIZACIÓN
  ↓
CHUNKS + METADATOS
  ↓
ÍNDICE / RETRIEVAL
```

### 10.1 Maximo como referencia del LAB

Para el aprendizaje EAM queremos utilizar **IBM Maximo como ejemplo de sistema que conoce qué documentos están asociados a un activo**.

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

Metadatos útiles para RAG:

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

Estos metadatos permiten restringir primero el universo documental y luego aplicar búsqueda semántica sobre contenido relevante.

### 10.2 Decisión para el primer experimento

No disponemos de una instancia Maximo viva para este LAB. Por eso se simula únicamente la capa de descubrimiento documental:

```text
asset_doclinks_mock.json
      ↓
PT-201 / PLANTA1
      ↓
manual + procedimiento enlazados
      ↓
archivos sintéticos del repositorio
```

Esto permite aprender el patrón correcto sin afirmar que exista integración real con Maximo.

Artefactos iniciales:

```text
rag/data/maximo/asset_doclinks_mock.json
rag/data/documents/manual_transmisor_PT201.md
rag/data/documents/procedimiento_seguridad_instrumentacion.md
rag/src/step01_discover_documents.py
```

Los documentos son **sintéticos de laboratorio** y no deben utilizarse para mantenimiento real.

---

## 11. Aplicación futura a EAM / IBM Maximo

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

## 12. Decisiones todavía NO tomadas

Aún no se ha decidido:

- proveedor/modelo de embeddings;
- vector database;
- framework RAG;
- LLM específico;
- ejecución local vs API;
- estrategia de chunking;
- tamaño de `top-k`;
- framework de evaluación.

Estas decisiones se tomarán durante experimentos concretos y se documentarán con evidencia, no por anticipado.

---

## 13. Siguiente paso

Ejecutar y observar el **Paso 01 — descubrimiento de documentos desde Maximo simulado**:

```text
PT-201 / PLANTA1
      ↓
consultar catálogo Maximo simulado
      ↓
obtener documentos vigentes enlazados
      ↓
verificar que los archivos existen
```

Después:

1. leer los documentos encontrados;
2. dividirlos en chunks observables;
3. construir el primer retrieval;
4. mostrar los chunks recuperados;
5. generar respuesta basada únicamente en ellos;
6. probar deliberadamente una pregunta sin respuesta.
