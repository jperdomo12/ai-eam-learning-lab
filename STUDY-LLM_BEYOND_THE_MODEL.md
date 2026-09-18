# 🧠 LLM más allá del modelo
## Cómo accede a datos, herramientas y conocimiento externo

> **Tipo:** STUDY  
> **Estado:** 📘 ENTENDIDO — nota transversal del Learning Lab  
> **Actualizado:** 2026-09-18  
>
> **Propósito:** explicar, con nivel técnico suficiente pero sin detalle innecesario, cómo un LLM amplía sus capacidades mediante Connectors/Apps, Tool Calling, MCP, RAG y acceso a sistemas empresariales como IBM Maximo.

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-18 | Se añade un **Resumen de contenido** inmediatamente después del Historial para facilitar la recuperación rápida de los 14 bloques del estudio. |
| 2026-09-18 | Creación inicial a partir de las aclaraciones posteriores a los Labs MCP y RAG. |

---


## 🧭 Resumen de contenido

| Punto | Contenido |
|---|---|
| **1. Idea principal** | Explica por qué un LLM necesita que el Host le presente capacidades externas para acceder a sistemas y datos. |
| **2. Formas de ampliar un LLM** | Resume Connectors/Apps, Tool Calling y MCP como mecanismos de acceso a capacidades externas. |
| **3. Cómo elige una capacidad** | Muestra cómo nombre, descripción y parámetros ayudan al LLM a seleccionar una o varias Tools. |
| **4. MCP, RAG y OSLC** | Aclara que son conceptos distintos y que RAG u OSLC pueden utilizarse detrás de Tools MCP. |
| **5. RAG como capacidad** | Explica cómo RAG puede exponerse como Tool y cómo se validó este patrón en el Paso 12. |
| **6. Fuentes del RAG** | Describe cómo Maximo Doclinks, Documentum u otros repositorios pueden alimentar una capacidad de conocimiento. |
| **7. Datos estructurados y vectores** | Distingue consulta estructurada, búsqueda vectorial y participación de una base de datos en un flujo RAG. |
| **8. MCP local y remoto** | Resume la diferencia entre Hosts locales/desktop/CLI y aplicaciones web para conectarse a servidores MCP. |
| **9. Connector vs. MCP** | Separa la experiencia de integración visible del protocolo que puede existir por debajo. |
| **10. Aplicación a IBM Maximo** | Presenta una arquitectura conceptual que combina capacidades EAM, Maximo, RAG y MCP. |
| **11. Qué demostraron los Labs** | Resume los aprendizajes prácticos de MCP, RAG, Maximo simulado y composición de Tools. |
| **12. Regla para AI-EAM-MAXIMO** | Fija el criterio de separar capacidades y decidir mecanismos de integración just-in-time. |
| **13. Chuleta para recordar** | Condensa los conceptos principales en definiciones de una línea. |
| **14. Relación con otros documentos** | Indica dónde profundizar en fundamentos, MCP, RAG y continuidad del Lab. |

---

## 1. Idea principal

Un LLM por sí solo no consulta automáticamente Maximo, Google Drive, Documentum ni una base de datos.

Para hacerlo, la aplicación o **Host** debe ofrecerle capacidades externas.

```text
LLM
│
├─ conocimiento aprendido + contexto actual
│
└─ capacidades externas
   ├─ Connectors / Apps
   ├─ Tools / Function Calling
   └─ MCP
        ↓
   sistemas, APIs, RAG, datos y acciones
```

> **El LLM no “sabe” mágicamente qué sistemas existen; el Host le presenta las capacidades disponibles y el modelo puede decidir cuándo utilizarlas.**

---

## 2. Formas comunes de ampliar un LLM

### Connectors / Apps

Integraciones preparadas entre una plataforma de IA y un servicio externo.

Ejemplo conceptual:

```text
ChatGPT
→ Google Drive
```

Normalmente el usuario conecta y autoriza el servicio.

### Tool / Function Calling

La aplicación presenta al modelo funciones concretas:

```text
get_open_work(...)
retrieve_knowledge(...)
create_work_order(...)
```

Cada Tool dispone de un nombre, descripción, parámetros y resultado.

### MCP

**Model Context Protocol** estandariza la forma en que aplicaciones de IA pueden descubrir y utilizar capacidades publicadas por servidores MCP.

```text
Host / aplicación IA
        ↓
    MCP Client
        ↓
    MCP Server
        ↓
 Tools / Resources / sistemas
```

MCP ayuda a reducir integraciones ad-hoc entre aplicaciones de IA y herramientas externas.

---

## 3. Cómo sabe el LLM qué capacidad utilizar

El Host presenta las Tools disponibles:

```text
nombre
+ descripción
+ parámetros
```

El LLM interpreta la pregunta y puede seleccionar una o varias.

Ejemplo:

```text
¿Tiene P-102 órdenes abiertas?
→ capacidad EAM

¿Qué recomienda su manual?
→ capacidad Knowledge / RAG

¿Tiene órdenes abiertas y qué recomienda el manual?
→ ambas capacidades
```

El nombre y la descripción de una Tool son importantes porque ayudan al modelo a elegir correctamente.

---

## 4. MCP no es RAG y MCP no es OSLC

Conviene recordar:

```text
RAG  ≠ MCP
OSLC ≠ MCP
```

- **RAG** → recupera conocimiento relevante, normalmente documental.
- **OSLC / API** → mecanismos para acceder a información y operaciones de sistemas como IBM Maximo.
- **MCP** → protocolo/interfaz para exponer capacidades al Host/LLM.

Por tanto:

```text
Tool MCP: consultar_ots_abiertas
→ puede usar Maximo / OSLC / API por debajo

Tool MCP: buscar_documentacion
→ puede usar RAG por debajo
```

> **MCP no sustituye a RAG ni a OSLC; puede exponer capacidades que utilizan RAG, OSLC, APIs u otros mecanismos internamente.**

---

## 5. RAG también puede exponerse como una capacidad

RAG no tiene que estar “dentro” del LLM.

Puede presentarse como:

```text
retrieve_knowledge(context, query)
→ evidencia documental
```

En el Paso 12 del RAG Lab hicimos:

```text
Tool A
consultar_ots_abiertas_activo(...)
→ datos EAM

Tool B
buscar_documentacion_activo(...)
→ Doclinks + RAG
→ evidencia documental
```

El Host/LLM seleccionó una, otra o ambas según la pregunta.

La Tool RAG recuperaba evidencia; **no utilizaba un segundo LLM para redactar**. La síntesis final correspondía al LLM principal.

---

## 6. Fuentes del RAG

Las fuentes se definen en la capa de conocimiento, no dentro del LLM.

Ejemplo:

```text
Knowledge / RAG
├─ Maximo Doclinks
├─ Documentum
├─ SharePoint / otro repositorio
└─ otras fuentes autorizadas
        ↓
 documentos aplicables
        ↓
 retrieval
        ↓
 evidencia
```

Para Maximo:

```text
Activo P-102
→ Maximo determina documentos asociados
→ RAG busca solo dentro de esos documentos
```

Separación importante:

```text
DISCOVERY / SCOPE
→ qué documentos aplican

RAG
→ qué contenido dentro de ellos responde
```

---

## 7. Datos estructurados y búsqueda vectorial

Una tabla puede seguir siendo estructurada aunque tenga una columna vectorial.

```text
tabla
├─ campos normales → filtros / SQL
└─ campo VECTOR    → búsqueda semántica/vectorial
```

Si esos vectores representan chunks documentales y los resultados se entregan al LLM como contexto, esa búsqueda puede formar parte de un flujo RAG.

> **Base de datos ≠ RAG automáticamente. El uso que se hace de sus datos determina si participa o no en RAG.**

---

## 8. MCP local y remoto

Un Host MCP necesita saber cómo localizar y conectarse al servidor MCP.

### Herramientas locales / desktop / CLI

Pueden, según el producto, ejecutar o conectarse a servidores MCP locales.

Ejemplos:

```text
Claude Desktop
Cline
Gemini CLI
```

### Herramientas web

Normalmente necesitan un servidor MCP accesible por red o mediante un mecanismo seguro de conexión.

Modelo mental:

```text
Host local
→ puede acceder al entorno local

Host web
→ normalmente necesita endpoint remoto / acceso por red
```

La implementación concreta depende de cada producto y puede evolucionar.

---

## 9. Connector y MCP no son lo mismo

Un **Connector/App** es una integración o experiencia preparada para acceder a un sistema.

**MCP** es un protocolo que puede utilizarse para implementar o exponer ese acceso.

Ejemplo:

```text
IBM Maximo Connector
→ integración visible

por debajo puede usar
→ MCP
→ API
→ OSLC
→ otros servicios
```

Un Connector puede ser específico de una plataforma, mientras un backend o servidor MCP bien diseñado puede ser reutilizable por diferentes Hosts compatibles.

---

## 10. Aplicación conceptual a IBM Maximo

Una vista simple:

```text
                 LLM / Host
                     │
            capacidades disponibles
             ┌───────┴────────┐
             ↓                ↓
        EAM / Maximo       Knowledge
             ↓                ↓
       MCP / OSLC / API      RAG
             ↓                ↓
          Maximo       Doclinks / Documentum
```

También podrían exponerse ambas familias desde un mismo servidor MCP:

```text
MCP Server AI-EAM / Maximo
├─ get_asset(...)
├─ get_open_work(...)
├─ get_failure_history(...)
├─ search_asset_documentation(...)
└─ search_corporate_documentation(...)
```

Pero internamente conviene conservar la separación:

```text
EAM
→ datos y acciones operacionales

Knowledge / RAG
→ conocimiento documental
```

Unificarlas bajo MCP no las convierte en la misma cosa.

---

## 11. Qué demostraron nuestros Labs

### MCP Lab

Un Host puede descubrir Tools publicadas por servidores MCP y decidir utilizarlas.

### RAG Lab

```text
documentos
→ retrieval
→ evidencia
→ LLM
```

Después se añadió contexto Maximo:

```text
Maximo simulado
→ determina documentos aplicables
→ RAG busca dentro de ellos
```

### Paso 12

Se combinaron ambos aprendizajes:

```text
Usuario
  ↓
Host / LLM
  ↓
MCP
├─ Tool EAM
└─ Tool RAG
  ↓
LLM combina evidencia
```

Esto demuestra **Tool Calling y composición dinámica de capacidades**.

No significa que toda solución definitiva deba implementar RAG mediante MCP.

---

## 12. Regla útil para AI-EAM-MAXIMO

El aprendizaje no es:

```text
RAG tiene que ser MCP
```

ni:

```text
Maximo debe consultarse siempre por OSLC
```

La regla útil es:

> **Diseñar capacidades de negocio y conocimiento claramente separadas, y elegir el mecanismo de integración adecuado cuando el caso real lo requiera.**

Modelo mental:

```text
Core / LLM
→ conoce capabilities

EAM capabilities
→ Simulation / Maximo

Knowledge capability
→ RAG

MCP
→ posible frontera estándar para exponer/invocar capabilities
```

La implementación definitiva se decide **just-in-time**, evitando acoplamiento prematuro.

---

## 13. Chuleta para recordar

```text
LLM
→ interpreta / razona / genera

Connector / App
→ integración preparada con un sistema

Tool Calling
→ el modelo puede invocar funciones ofrecidas por la aplicación

MCP
→ estándar para descubrir e invocar capacidades

OSLC / API
→ mecanismo para acceder a sistemas como Maximo

RAG
→ recupera conocimiento documental

Vector search
→ encuentra contenido semánticamente parecido

Maximo Doclinks
→ ayuda a saber qué documentos aplican

Documentum
→ puede ser otra fuente documental

Agente
→ usa modelo + contexto + Tools para avanzar hacia un objetivo
```

Si solo se recuerda una frase:

> **El LLM se vuelve útil en empresa cuando, además de razonar, puede obtener el contexto correcto y utilizar capacidades externas de forma controlada.**

---

## 14. Relación con los documentos del Lab

Para fundamentos generales e historia:

`STUDY-AI_FOUNDATIONS_AND_HISTORY.md`

Para experimentos:

```text
mcp/
rag/
```

Para el bloque RAG/EAM/MCP ya cerrado:

```text
rag/docs/RAG_LAB_FAST_READING.md
rag/docs/RAG_LIVING_DOCUMENTATION.md
rag/docs/RAG_LAB_HANDOFF.md
```

Este documento sirve como **puente conceptual transversal** entre esos Labs y el trabajo posterior en `jperdomo12/ai-driven-eam-copilot`.
