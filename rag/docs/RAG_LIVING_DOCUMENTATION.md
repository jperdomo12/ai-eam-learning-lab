# 📘 RAG Learning Lab — Documentación viva

> 🎯 **Propósito:** conservar el conocimiento, decisiones de laboratorio, instalación, pruebas, resultados y aprendizajes del frente **Retrieval-Augmented Generation (RAG)** aplicado a EAM / IBM Maximo.
>
> 📍 **Estado:** 🟢 **EN CURSO — etapa conceptual inicial**
>
> 🗓️ **Actualizado:** 2026-09-12

## 🕘 Historial

| Fecha | Cambio |
|---|---|
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
¿Cuál es el procedimiento exacto de calibración de la bomba B-201?
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

> construir un RAG pequeño donde podamos ver claramente qué fragmentos se recuperan antes de que el LLM genere la respuesta.

Queremos poder observar algo como:

```text
Pregunta:
¿Cómo calibro el sensor de presión?

Chunks recuperados:
1. sección 4.2 — calibración
2. sección 4.3 — tolerancias
3. sección 2.1 — seguridad

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

La respuesta requiere combinar más de un fragmento.

### Caso D — respuesta inexistente

El documento no contiene la respuesta.

Resultado esperado:

```text
No existe evidencia suficiente en la documentación disponible.
```

Este caso será especialmente importante para controlar alucinaciones.

---

## 10. Aplicación futura a EAM / IBM Maximo

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

## 11. Decisiones todavía NO tomadas

Aún no se ha decidido:

- proveedor/modelo de embeddings;
- vector database;
- framework RAG;
- LLM específico;
- ejecución local vs API;
- estrategia de chunking;
- tamaño de `top-k`;
- formato de documentos definitivo;
- framework de evaluación.

Estas decisiones se tomarán durante experimentos concretos y se documentarán con evidencia, no por anticipado.

---

## 12. Siguiente paso

Primera etapa práctica:

1. seleccionar un documento pequeño y controlable;
2. definir preguntas con respuesta conocida;
3. construir el pipeline mínimo;
4. mostrar los chunks recuperados;
5. generar respuesta basada únicamente en ellos;
6. probar deliberadamente una pregunta sin respuesta.

El código y las carpetas técnicas se crearán en GitHub cuando este primer experimento defina qué artefactos necesita realmente.
