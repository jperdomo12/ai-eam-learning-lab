# RAG — Conceptos esenciales

> **Subtítulo:** Fundamentos y conceptos intermedios que conviene dominar.
>
> **Tipo:** Nota de estudio del AI-EAM Learning Lab  
> **Estado:** 📘 ENTENDIDO — documento vivo de apoyo al aprendizaje  
> **Fecha:** 2026-09-13

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-13 | Se reorganiza la nota dentro de `rag/docs/study/` para separar claramente el material pedagógico de la documentación canónica del laboratorio. |
| 2026-09-13 | Creación inicial. Se consolidan los conceptos básicos de RAG y los conceptos intermedios necesarios para comprender el pipeline completo sin entrar todavía en implementaciones avanzadas. |

---

## 1. Qué es RAG

**RAG (Retrieval-Augmented Generation)** es un patrón que combina:

```text
RETRIEVAL
recuperar conocimiento relevante

        +

GENERATION
generar una respuesta usando ese conocimiento
```

Modelo mental:

```text
DOCUMENTOS
   ↓
preparar / dividir / indexar
   ↓
PREGUNTA
   ↓
recuperar fragmentos relevantes
   ↓
pregunta + contexto recuperado
   ↓
LLM
   ↓
RESPUESTA FUNDAMENTADA
```

La idea principal es:

> **El LLM no necesita memorizar todos los documentos; necesita recibir la evidencia correcta cuando responde.**

---

## 2. Qué problema resuelve

Un LLM puede conocer información general, pero no debe asumirse que conoce de forma fiable:

- el manual exacto de un equipo;
- la última revisión de un procedimiento;
- documentación interna de una empresa;
- instrucciones privadas de mantenimiento;
- información que cambió después de su entrenamiento.

RAG permite mantener ese conocimiento **fuera del modelo** y recuperarlo cuando hace falta.

---

## 3. Pipeline básico de RAG

```text
FUENTE
  ↓
ADQUISICIÓN
  ↓
EXTRACCIÓN / NORMALIZACIÓN
  ↓
CHUNKING
  ↓
REPRESENTACIÓN / INDEXACIÓN
  ↓
RETRIEVAL
  ↓
CONTEXTO
  ↓
LLM
  ↓
RESPUESTA + EVIDENCIA
```

Cada bloque cumple una función distinta. Entenderlos por separado ayuda a diagnosticar por qué un RAG funciona bien o mal.

---

## 4. Conceptos básicos

### 4.1 Fuente documental

Lugar donde reside el conocimiento original.

Ejemplos:

```text
carpeta Windows/Linux
SharePoint
Documentum
object storage
web interna
IBM Maximo / documentos enlazados
```

La fuente no es el RAG; es el origen del conocimiento que el RAG utilizará.

### 4.2 Adquisición / acceso

Mecanismo utilizado para obtener el documento desde su fuente.

```text
filesystem  → lectura de archivos
API         → consulta a un servicio
conector    → acceso a un repositorio
URL         → descarga o lectura remota
Maximo      → metadata/doclinks + acceso al documento
```

La adquisición cambia según la fuente. El resto del pipeline debería intentar mantenerse reutilizable.

### 4.3 Extracción

Conversión del archivo a contenido que el sistema pueda procesar.

```text
PDF  → texto extraído
DOCX → texto + estructura
HTML → contenido útil
imagen escaneada → OCR
```

Encontrar un archivo no significa todavía haber extraído correctamente su contenido.

### 4.4 Normalización

Limpieza y preparación del contenido para que diferentes formatos terminen en una representación coherente.

Puede incluir:

- eliminar ruido;
- conservar títulos y secciones;
- normalizar espacios o caracteres;
- preservar metadata relevante;
- identificar documento, revisión y origen.

### 4.5 Chunk

Un **chunk** es una unidad de contenido recuperable.

```text
DOCUMENTO COMPLETO
      ↓
secciones / fragmentos
      ↓
CHUNKS
```

El objetivo es recuperar solo los fragmentos necesarios para una pregunta, no enviar siempre documentos completos al LLM.

### 4.6 Chunking

Estrategia usada para dividir el documento.

Puede basarse en:

```text
encabezados
párrafos
cantidad de caracteres
cantidad de tokens
estructura semántica
combinaciones de las anteriores
```

No existe un tamaño universalmente correcto. Chunks demasiado pequeños pueden perder contexto; demasiado grandes pueden introducir ruido.

### 4.7 Metadata

Información que acompaña al chunk y permite identificarlo o filtrarlo.

Ejemplo EAM:

```text
document_name
section
revision
assetnum
siteid
document_type
source_system
url / path
```

La metadata no sustituye al contenido, pero puede ser decisiva para recuperar la evidencia correcta.

---

## 5. Retrieval: encontrar los chunks correctos

**Retrieval** es el proceso de seleccionar los fragmentos más relevantes para una consulta.

```text
PREGUNTA
   ↓
comparar contra los chunks
   ↓
ordenar por relevancia
   ↓
seleccionar los mejores
```

### 5.1 Retrieval léxico

Busca principalmente coincidencias de palabras o términos.

```text
"calibración PT-201"
        ↕
"procedimiento de calibración PT-201"
```

Ventaja: simple y observable.

Limitación: puede fallar cuando la pregunta y el documento expresan la misma idea con palabras diferentes.

### 5.2 Retrieval semántico

Busca similitud de significado mediante **embeddings**.

```text
"ajustar el transmisor"
        ≈
"calibrar el instrumento"
```

Las palabras pueden ser diferentes y aun así resultar semánticamente próximas.

### 5.3 Retrieval híbrido

Combina búsqueda léxica y semántica.

```text
lexical
   +
semantic
   ↓
hybrid retrieval
```

Es un concepto intermedio importante porque en sistemas reales una combinación puede funcionar mejor que depender exclusivamente de una estrategia.

---

## 6. Embeddings

Un **embedding** es una representación numérica de un texto.

Conceptualmente:

```text
"procedimiento para calibrar PT-201"
        ↓
modelo de embeddings
        ↓
[0.21, -0.54, 0.76, ...]
```

La pregunta se representa de la misma forma:

```text
"¿cómo ajusto el transmisor?"
        ↓
embedding
        ↓
[0.19, -0.51, 0.79, ...]
```

Después se calcula qué vectores están más próximos.

La idea para recordar:

> **Los embeddings permiten comparar significado matemáticamente.**

---

## 7. Índice y vector store

Cuando existen muchos chunks necesitamos una estructura que permita buscarlos eficientemente.

En un RAG semántico suele almacenarse algo parecido a:

```text
CHUNK
+ EMBEDDING
+ METADATA
```

Un **vector store** está especializado en guardar y buscar representaciones vectoriales.

Importante:

> **Vector store no es sinónimo de RAG.**

RAG puede utilizar otras técnicas de búsqueda y no siempre necesita una base vectorial dedicada.

---

## 8. Top-k

`top-k` indica cuántos resultados de retrieval se seleccionan.

```text
top-k = 3
```

significa:

```text
recuperar los 3 chunks mejor posicionados
```

Un `k` demasiado pequeño puede dejar fuera evidencia necesaria; uno demasiado grande puede añadir ruido y consumir contexto innecesariamente.

---

## 9. Reranking

Concepto intermedio útil.

Después del retrieval inicial puede aplicarse un segundo mecanismo que reordene los candidatos con más precisión.

```text
pregunta
   ↓
retrieval inicial
   ↓
10 candidatos
   ↓
reranker
   ↓
3 mejores
```

No es obligatorio para un RAG básico, pero puede mejorar la calidad cuando el corpus crece o las consultas son complejas.

---

## 10. Contexto

Los chunks recuperados se convierten en **contexto** para el LLM.

```text
PREGUNTA
+
CHUNKS RECUPERADOS
        ↓
PROMPT / CONTEXTO
        ↓
LLM
```

El LLM genera utilizando tanto la pregunta como la evidencia suministrada.

Si el retrieval entrega contexto incorrecto, el LLM puede producir una respuesta incorrecta aunque el modelo sea muy capaz.

---

## 11. Grounding y citas

**Grounding** significa que la respuesta está apoyada por evidencia disponible.

En un RAG bien diseñado queremos poder mostrar:

```text
respuesta
  ↓
qué chunk la sustenta
  ↓
qué documento
  ↓
qué sección / revisión / fuente
```

Esto es especialmente importante en EAM, mantenimiento, seguridad y decisiones técnicas.

---

## 12. Alucinación

RAG puede reducir respuestas inventadas, pero **no elimina automáticamente las alucinaciones**.

Puede fallar si:

- se recupera el chunk equivocado;
- el documento contiene información incorrecta;
- falta evidencia;
- el contexto es ambiguo;
- el LLM ignora o interpreta mal la evidencia.

Por eso un comportamiento correcto también puede ser:

```text
No existe evidencia suficiente en la documentación disponible.
```

---

## 13. Evaluación

No basta con que una respuesta "suene bien".

Conviene evaluar al menos:

```text
¿recuperamos el chunk correcto?
¿la respuesta está respaldada por la fuente?
¿citamos la evidencia correcta?
¿detectamos cuando no hay información suficiente?
```

Para nuestro LAB usamos cuatro casos básicos:

```text
A. respuesta presente
B. misma idea expresada con otras palabras
C. información repartida en varios chunks/documentos
D. respuesta inexistente
```

---

## 14. Actualización del conocimiento

Una ventaja importante de RAG es que normalmente no exige reentrenar el LLM cuando cambia la documentación.

Ejemplo:

```text
Manual revisión 4
        ↓
se sustituye por revisión 5
        ↓
reprocesar / reindexar
        ↓
las nuevas consultas recuperan revisión 5
```

La gestión de versiones, vigencia y eliminación de contenido obsoleto es por tanto parte importante de un RAG empresarial.

---

## 15. Seguridad y permisos

Concepto intermedio especialmente importante en entornos empresariales.

Un RAG no debería recuperar documentos que el usuario no está autorizado a consultar.

```text
usuario
  ↓
permisos
  ↓
fuentes / metadata permitidas
  ↓
retrieval
```

La seguridad debe considerarse desde la adquisición y el retrieval, no únicamente al mostrar la respuesta final.

---

## 16. Ejemplo EAM / IBM Maximo

Pregunta futura:

```text
La bomba P-102 presenta alta temperatura.
¿Qué trabajo está abierto y qué indica el manual que debo revisar?
```

Responsabilidades:

```text
MCP / Maximo
→ activo, OTs, historial, mediciones

RAG
→ manuales, procedimientos, troubleshooting

LLM
→ integra hechos + conocimiento documental
→ genera una respuesta fundamentada
```

RAG aporta principalmente **conocimiento documental recuperable**; MCP aporta **acceso a datos, sistemas y acciones**.

---

## 17. Mapa rápido para recordar

```text
FUENTE
  ↓
ADQUISICIÓN
  ↓
EXTRACCIÓN
  ↓
CHUNKS + METADATA
  ↓
EMBEDDINGS / ÍNDICE
  ↓
RETRIEVAL
  ↓
TOP-K / RERANKING
  ↓
CONTEXTO
  ↓
LLM
  ↓
RESPUESTA + EVIDENCIA
  ↓
EVALUACIÓN
```

Conceptos básicos que conviene dominar primero:

```text
fuente
chunk
chunking
metadata
embedding
retrieval
vector store / índice
top-k
contexto
grounding
```

Conceptos intermedios importantes:

```text
retrieval híbrido
reranking
actualización / reindexación
control de acceso
evaluación
```

---

## 18. Qué no debe confundirse

- **RAG no es un LLM.**
- **Chunking no es retrieval.**
- **Embedding no es el texto original.**
- **Vector store no es el LLM.**
- **Retrieval no genera la respuesta; selecciona evidencia.**
- **El LLM no debería sustituir evidencia ausente con una invención.**
- **Más chunks recuperados no significa necesariamente mejor respuesta.**
- **RAG no elimina la necesidad de evaluar calidad, seguridad y vigencia documental.**
