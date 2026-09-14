# 📘 Fundamentos de IA e historia mínima para AI-Driven EAM

> **Tipo:** STUDY  
> **Estado:** 📘 ENTENDIDO — nota transversal del Learning Lab  
> **Actualizado:** 2026-09-14
>
> **Propósito:** consolidar en una sola nota los conceptos básicos de IA que sirven de base para entender LLM, RAG, MCP y agentes, conectándolos con EAM / IBM Maximo sin convertir esta nota en un tratado académico.

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-14 | Creación inicial a partir de notas personales de estudio revisadas y del aprendizaje práctico realizado en los LAB de MCP y RAG. Se actualiza específicamente la situación de IBM Maximo 9.2 respecto a MCP, OSLC y capacidades RAG/DocSearch documentadas por IBM. |

---

## 1. Mapa mental general

La forma más útil de ordenar los conceptos es:

```text
INTELIGENCIA ARTIFICIAL
    ↓
Machine Learning
    ↓
Deep Learning
    ↓
Modelos generativos
    ↓
LLM / modelos multimodales
    ↓
+ Prompting
+ RAG
+ Tools / MCP
+ Agentes
```

No son capas completamente excluyentes, pero esta jerarquía ayuda a entender cómo se relacionan.

---

## 2. Historia mínima que conviene recordar

### 1950 — Alan Turing

Turing propone una forma práctica de discutir si una máquina puede mostrar comportamiento inteligente mediante una conversación indistinguible de la de una persona.

### 1956 — Dartmouth

John McCarthy y otros investigadores consolidan el término **Artificial Intelligence** como nombre de un nuevo campo de investigación.

### IA simbólica y sistemas expertos

Durante décadas predominó una visión basada en:

```text
hechos
+
reglas explícitas
+
inferencia lógica
```

Lenguajes como Prolog representan bien esta filosofía.

Importante: la IA simbólica no "desapareció". Sigue siendo útil donde se necesitan reglas explícitas, lógica, restricciones o conocimiento estructurado.

### 1997 — IBM Deep Blue

Deep Blue derrota al campeón mundial de ajedrez Garry Kasparov. Es un hito de sistemas especializados y cálculo intensivo, no un antecedente directo de los LLM modernos.

### 2012 — auge moderno del Deep Learning

El éxito de redes neuronales profundas entrenadas con grandes cantidades de datos y GPUs acelera fuertemente la investigación práctica en visión, lenguaje y otras áreas.

### 2017 — *Attention Is All You Need*

Investigadores de Google publican el paper que introduce la arquitectura **Transformer**. Es uno de los hitos decisivos que hacen posible la evolución posterior de los grandes modelos de lenguaje.

No es correcto afirmar que toda la IA moderna "nace únicamente" de ese paper, pero sí que Transformer cambió profundamente el procesamiento de secuencias y se convirtió en la base de gran parte de la IA generativa actual.

### 2022 — popularización masiva de GenAI

ChatGPT lleva los LLM al uso cotidiano de millones de personas. A partir de aquí se acelera la adopción empresarial de asistentes, copilots y generación multimodal.

### 2024 — MCP

Anthropic introduce **Model Context Protocol (MCP)** como estándar abierto para conectar aplicaciones y agentes de IA con herramientas, datos y sistemas externos mediante una interfaz común.

### 2025–2026 — de asistente a agente

La evolución práctica pasa de:

```text
preguntar → responder
```

a:

```text
entender objetivo
→ consultar sistemas
→ usar herramientas
→ combinar información
→ ejecutar acciones controladas
```

Para EAM, esto abre escenarios como consultar Maximo, recuperar documentación técnica, generar análisis y eventualmente ejecutar acciones con gobierno y permisos adecuados.

---

## 3. Qué es un LLM

Un **Large Language Model** es un modelo neuronal entrenado sobre grandes cantidades de texto para aprender patrones estadísticos del lenguaje.

Simplificando:

```text
texto
→ tokenización
→ representación numérica
→ Transformer
→ predicción del siguiente token
→ repetición
→ respuesta
```

Un LLM no funciona como una base de datos exacta de frases ni como un disco duro que recupera registros literales.

Su conocimiento queda distribuido en millones o miles de millones de **pesos** aprendidos durante el entrenamiento.

---

## 4. Tokenización

Los LLM no procesan directamente palabras completas como lo hacemos las personas.

Primero convierten el texto en **tokens**, que pueden ser:

- palabras;
- partes de palabras;
- signos;
- números;
- combinaciones frecuentes de caracteres.

Por ejemplo, una frase técnica como:

```text
Ajustar ZERO si el error supera 0,02 bar
```

se convierte internamente en una secuencia de tokens que el modelo procesa matemáticamente.

Consecuencia práctica:

```text
context window
→ se mide en tokens
→ no en páginas ni en palabras exactas
```

Más documentos o más chunks en un prompt implican más tokens consumidos.

---

## 5. Transformer y Attention

### Transformer

La arquitectura Transformer sustituyó gran parte del procesamiento secuencial tradicional por mecanismos de atención que permiten modelar relaciones entre elementos de una secuencia de forma mucho más eficiente.

### Attention

**Attention** permite que el modelo determine qué partes del contexto son relevantes entre sí.

Ejemplo simplificado:

```text
"si el error supera 0,02 bar, ajustar ZERO"
```

el modelo puede relacionar:

```text
error ↔ 0,02 bar
ajustar ↔ ZERO
```

En una pregunta RAG puede relacionar también:

```text
Pregunta: ¿Cómo calibro el PT-201?
                ↕
Contexto: ZERO / SPAN / 0-5-10 bar / tolerancia
```

### Attention no es Retrieval

Esta distinción es crítica:

```text
RAG retrieval
→ decide qué información EXTERNA entra en el contexto

Attention
→ relaciona los tokens que YA están dentro del contexto del modelo
```

Por tanto:

```text
retrieval ≠ attention
```

---

## 6. Entrenamiento, inferencia y memoria

### Entrenamiento

Durante el entrenamiento el modelo ajusta sus pesos para reducir el error de predicción.

Conceptualmente:

```text
datos de entrenamiento
→ predicción
→ error
→ backpropagation
→ ajuste de pesos
→ repetir a gran escala
```

### Inferencia

La **inferencia** ocurre cuando usamos el modelo ya entrenado para responder una consulta.

```text
prompt
→ modelo ya entrenado
→ generación
```

### Pesos no son memoria exacta

Los pesos representan patrones aprendidos, no una colección de documentos recuperables de forma exacta.

Por eso un LLM puede:

- generalizar;
- inferir;
- combinar patrones;
- cometer errores;
- producir una respuesta plausible pero falsa.

---

## 7. Modelos, runtimes y productos

Es importante no confundir estas tres capas.

### Modelo

Ejemplos:

```text
GPT
Gemini
Claude
Llama
Mistral
Qwen
DeepSeek
Gemma
```

### Runtime / plataforma que ejecuta un modelo

Ejemplo del Learning Lab:

```text
Llama 3
→ modelo

Ollama
→ runtime local que ejecuta el modelo
```

### Producto

Ejemplos:

```text
ChatGPT
Gemini
Claude Desktop
Cline
```

Un producto puede usar uno o varios modelos y añadir memoria, búsqueda, herramientas, interfaces, seguridad, orquestación y otros servicios.

### Modelos pequeños y grandes

Existen modelos suficientemente pequeños y cuantizados para ejecutarse en:

```text
portátil
edge
algunos smartphones
```

mientras modelos de mayor capacidad suelen ejecutarse en infraestructura cloud con GPUs especializadas.

---

## 8. Cuantización

La **cuantización** reduce la precisión numérica usada para representar los pesos del modelo.

Ejemplo conceptual:

```text
más precisión
→ más memoria y cómputo

menos precisión controlada
→ menos memoria
→ más velocidad
→ posible pequeña pérdida de calidad
```

Esto ayuda a ejecutar modelos relativamente grandes en hardware personal.

En el RAG LAB usamos `llama3:latest` con cuantización `Q4_0` mediante Ollama.

---

## 9. Qué es IA Generativa

La IA generativa crea contenido nuevo a partir de patrones aprendidos.

Puede generar:

```text
texto
código
imagen
audio
video
```

En lenguaje, un LLM genera una respuesta token a token condicionada por:

```text
entrenamiento
+
prompt actual
+
contexto disponible
```

---

## 10. Cómo ampliamos las capacidades de un LLM

### Prompting

Le damos instrucciones y contexto dentro de la propia petición.

### RAG

Recuperamos conocimiento externo relevante y lo incorporamos al prompt antes de generar la respuesta.

```text
documentos
→ chunks
→ embeddings
→ índice
→ retrieval
→ contexto
→ LLM
```

RAG no reentrena el modelo.

### Fine-tuning

Modifica el comportamiento del modelo mediante entrenamiento adicional con ejemplos especializados.

Puede ser útil para adaptar comportamiento, formato o tareas concretas, pero no sustituye automáticamente a RAG para información documental que cambia con frecuencia.

### Tools

El modelo puede invocar funciones externas para consultar o ejecutar acciones.

### MCP

MCP estandariza la forma en que aplicaciones/agentes de IA descubren y utilizan herramientas, datos y capacidades ofrecidas por servidores MCP.

### Agentes

Un agente combina normalmente:

```text
LLM
+
instrucciones
+
herramientas
+
estado/contexto
+
bucle de ejecución
```

para avanzar hacia un objetivo sin que el usuario tenga que indicar cada paso intermedio.

---

## 11. RAG y MCP: no resuelven el mismo problema

Modelo mental para AI-Driven EAM:

```text
LLM
→ razonamiento y generación

RAG
→ conocimiento documental

MCP
→ acceso a sistemas, datos y acciones

Maximo
→ contexto EAM transaccional y operacional
```

Ejemplo:

```text
"La bomba B-201 presenta alta temperatura.
¿Tiene OTs abiertas y qué indica el manual?"

MCP / Maximo
→ OTs y estado actual

RAG
→ manual / procedimiento

LLM
→ integra ambas evidencias
```

---

## 12. IBM Maximo: OSLC, MCP y IA en 2026

### 12.1 OSLC sigue siendo relevante

La llegada de MCP **no elimina ni sustituye OSLC**.

IBM Maximo continúa utilizando APIs y estructuras de objetos para acceso a datos. La documentación actual del Maximo Assistant describe, por ejemplo, un flujo `nl2oslc` donde el modelo genera la información necesaria para construir una solicitud a la API OSLC y recuperar datos de Maximo.

Por tanto, la relación correcta es más parecida a:

```text
Agente / LLM
      ↓
MCP o capacidades del Assistant
      ↓
Tools
      ↓
Maximo Manage
      ↓
OSLC / Object Structures / Automation Scripts / Workflows
```

MCP añade una **capa estandarizada orientada a agentes y tools**; no invalida los mecanismos de integración de Maximo existentes.

### 12.2 Servidor MCP oficial de Maximo

La documentación vigente de **Maximo Application Suite 9.2** incluye un **Maximo MCP server** oficial.

Características documentadas por IBM:

- se ejecuta como pod en Red Hat OpenShift;
- permite a agentes de IA acceder a datos y funcionalidades de Maximo Manage mediante tool calls estandarizadas;
- sincroniza la lista de tools con Maximo Manage;
- admite tools personalizadas construidas con Automation Scripts, Object Structures o Workflows;
- permite conectar agentes externos al servidor MCP;
- soporta autenticación para esas conexiones externas;
- el Maximo Assistant agentic utiliza ese servidor MCP para encadenar múltiples tools.

Nota temporal: IBM publicó el Feature Channel de abril de 2026 el **30/04/2026**. La documentación actual de MAS 9.2 ya describe formalmente el servidor Maximo MCP. Esta nota no intenta fijar aquí el primer build exacto en el que apareció la capacidad.

### 12.3 ¿Tiene Maximo RAG?

La respuesta necesita matiz.

IBM sí documenta capacidades relacionadas con RAG dentro de Maximo Assistant:

- el parámetro `use_domain_rule_filter` puede ejecutar una **hybrid RAG search** sobre prompts/reglas de dominio para seleccionar solo las más relevantes;
- el Maximo Assistant agentic dispone de una tool `docsearch` que busca sobre una copia estática de la documentación oficial de IBM.

Por tanto, no sería correcto afirmar que **Maximo no utiliza RAG en absoluto**.

Sin embargo, en la documentación IBM revisada hasta 2026-09-14 **no se ha identificado una capacidad general de RAG orientada a indexar documentación técnica propia del cliente —por ejemplo manuales, procedimientos o archivos vinculados mediante Doclinks— y responder sobre ella como hicimos en nuestro RAG Learning Lab**.

La distinción es:

```text
RAG documentado por IBM
→ reglas/prompts del Assistant
→ búsqueda en IBM Documentation

Necesidad AI-EAM que seguimos explorando
→ manuales y procedimientos propios
→ documentación asociada a activos
→ Doclinks / repositorios documentales
→ RAG técnico del cliente
```

Esto deja un espacio arquitectónico muy relevante para AI-EAM-MAXIMO:

```text
Maximo MCP
→ contexto y acciones transaccionales

RAG propio
→ conocimiento técnico documental del cliente

LLM / agente
→ combinación de ambos
```

---

## 13. Lo probado realmente en este Learning Lab

### MCP LAB — ✅ cerrado

Se verificó:

```text
Claude Desktop
→ Claude
→ Maximo MCP simulado + Filesystem MCP
```

y posteriormente:

```text
VS Code + Cline
→ DeepSeek V4 Flash
→ Maximo MCP simulado + Filesystem MCP
```

Cline fue el agente/entorno; DeepSeek fue el LLM seleccionado.

### RAG LAB básico — ✅ cerrado

Se verificó:

```text
documentos locales
→ chunking
→ embeddings MiniLM
→ índice persistente
→ retrieval semántico
→ Top-k
→ contexto recuperado
→ Llama 3 local mediante Ollama
→ respuesta fundamentada
```

También se verificó:

```text
retrieval correcto ≠ generación necesariamente completa
Top-k encontrado ≠ respuesta encontrada
similarity ≠ confianza
sin evidencia → el LLM debe abstenerse
```

---

## 14. Analogías útiles, con sus límites

### LLM = cerebro entrenado

Útil para recordar que contiene patrones, no registros exactos.

### RAG = bibliotecario

Busca la documentación apropiada antes de pedir al LLM que responda.

### MCP = USB / interfaz estándar

Ayuda a visualizar una interfaz común para conectar agentes con capacidades externas.

No significa que desaparezca el trabajo de integración: alguien debe implementar o configurar el servidor MCP y su conexión con Maximo, bases de datos, APIs u otros sistemas.

### Agente = profesional con cerebro + herramientas

El modelo razona y las herramientas le permiten observar o actuar sobre sistemas reales.

---

## 15. Qué conviene recordar para AI-Driven EAM

```text
LLM solo
→ conocimiento general + razonamiento

LLM + RAG
→ conocimiento documental específico y recuperado

LLM + MCP
→ acceso a datos y acciones de sistemas

LLM + RAG + MCP
→ conocimiento documental + contexto operacional + capacidad de actuar
```

Para EAM el valor no está en usar IA por sí misma, sino en conectar correctamente:

```text
activo
OTs
historial
condición
manuales
procedimientos
reglas de negocio
permisos
acciones
```

con un modelo capaz de interpretar la intención del usuario y producir una respuesta controlada y verificable.

---

## 16. Referencias principales

- Vaswani et al., **Attention Is All You Need** (2017): https://arxiv.org/abs/1706.03762
- IBM Docs — **Maximo MCP server overview**: https://www.ibm.com/docs/en/masv-and-l/cd?topic=developing-maximo-mcp-server-overview
- IBM Docs — **Connecting external AI agents to the Maximo MCP server**: https://www.ibm.com/docs/en/masv-and-l/cd?topic=developing-connecting-external-agents
- IBM Docs — **Enabling Maximo Assistant to retrieve data**: https://www.ibm.com/docs/en/masv-and-l/cd?topic=assistant-enabling-data-retrieval
- IBM Docs — **Enabling the agentic Maximo Assistant**: https://www.ibm.com/docs/en/masv-and-l/cd?topic=assistant-enabling-agentic
- IBM Docs — **Testing Maximo Assistant**: https://www.ibm.com/docs/en/masv-and-l/cd?topic=assistant-testing
- IBM Support — **Maximo Application Suite 9.2.x Feature Channel April Release**: https://www.ibm.com/support/pages/readme-file-maximo-application-suite-92x-feature-channel-april-release

---

## 17. Regla de uso de esta nota

Esta nota es una **síntesis conceptual transversal**.

Para detalles experimentales consultar:

```text
mcp/
→ evidencia y documentación del MCP LAB

rag/
→ evidencia y documentación del RAG LAB
```

Para decisiones de producto consultar siempre el repositorio oficial de AI-EAM-MAXIMO. Nada de esta nota se convierte automáticamente en una decisión de arquitectura productiva.
