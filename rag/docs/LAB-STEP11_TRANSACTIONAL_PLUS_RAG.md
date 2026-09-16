# 🧪 Paso 11 — Datos transaccionales + RAG documental

> 🎯 **Objetivo:** combinar, para un mismo contexto EAM, datos estructurados/transaccionales simulados de Maximo con conocimiento documental recuperado mediante RAG.
>
> 📍 **Estado:** 🧪 **PREPARADO — pendiente de ejecución local y validación pedagógica**
>
> 🗓️ **Actualizado:** 2026-09-16

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-16 | Creación inicial del Paso 11: se añade `WORKORDER` simulado para `PT-201`, consulta estructurada de OTs abiertas, Doclinks + RAG documental y combinación final mediante Llama 3 local. |

---

## 1. Qué queremos aprender

Los Pasos 09 y 10 demostraron:

```text
contexto EAM
→ ASSET
→ DOCLINKS / DOCINFO
→ documentos asociados
→ RAG
→ LLM
```

El Paso 11 incorpora por primera vez una segunda clase de información:

```text
DATOS ESTRUCTURADOS / TRANSACCIONALES
→ WORKORDER
→ consulta exacta
             \
              → LLM → respuesta integrada
             /
DOCUMENTOS / CONOCIMIENTO
→ DOCLINKS
→ RAG
```

La pregunta guía es:

```text
¿Tiene el PT-201 alguna OT abierta y qué indica su documentación
que debo revisar antes de intervenirlo?
```

---

## 2. Reutilización del MCP Lab sin acoplar ambos laboratorios

El MCP Lab ya había utilizado campos típicos de órdenes de trabajo Maximo como:

```text
WONUM
DESCRIPTION
STATUS
ASSETNUM
SITEID
WORKTYPE
WOPRIORITY
```

El Paso 11 conserva esa convención y añade `WORKORDERID`, pero **no modifica ni reabre el MCP Lab**, que permanece cerrado/congelado.

Los nuevos datos viven separadamente en:

```text
rag/data/maximo_mock/workorders.json
```

Esto permite reutilizar el aprendizaje sin crear dependencia entre los dos experimentos.

---

## 3. WORKORDER simulado

Para `PT-201 / PLANTA1` se crean tres órdenes:

```text
OT-PT201-01 | APPR  | prioridad 2 | PM | abierta en la baseline
OT-PT201-02 | INPRG | prioridad 1 | CM | abierta en la baseline
OT-PT201-03 | COMP  | prioridad 3 | PM | excluida como completada
```

Campos usados:

```text
workorderid
wonum
description
status
assetnum
siteid
worktype
wopriority
```

Los nombres representan atributos reales/típicos del objeto `WORKORDER`; los JSON usan minúsculas por conveniencia del LAB.

### Qué significa "abierta" aquí

Para esta prueba se define explícitamente:

```text
WAPPR
APPR
INPRG
WMATL
```

como conjunto de estados abiertos de la baseline pedagógica.

Esto **no pretende modelar universalmente la semántica de estados de cualquier instalación Maximo**. En sistemas reales pueden existir sinónimos y configuraciones propias del dominio de estados.

---

## 4. Dos rutas diferentes para responder una sola pregunta

### Ruta A — datos transaccionales

```text
ASSETNUM + SITEID
→ filtrar WORKORDER
→ filtrar estado
→ obtener OTs abiertas
```

No hay embeddings ni RAG en esta ruta.

Es una consulta estructurada exacta sobre datos operativos simulados.

### Ruta B — conocimiento documental

```text
ASSET
→ DOCLINKS
→ DOCINFO
→ documentos asociados
→ chunking
→ embeddings
→ retrieval semántico
→ Top-k
→ texto original
```

Esta ruta sí es RAG documental.

---

## 5. Descomposición controlada de la pregunta

La pregunta completa contiene dos necesidades distintas:

```text
¿Tiene el PT-201 alguna OT abierta?
→ datos transaccionales

¿Qué indica su documentación que debo revisar antes de intervenirlo?
→ conocimiento documental
```

En este Paso 11 la descomposición está **codificada explícitamente**, no decidida autónomamente por un agente.

La consulta documental usada para retrieval es:

```text
¿Qué debo revisar antes de intervenir o calibrar el PT-201?
```

Después, ambas clases de evidencia se entregan al LLM.

---

## 6. Script

```text
rag/src/step11_transactional_plus_rag.py
```

Flujo:

```text
PT-201 / PLANTA1
        ↓
        ├── WORKORDER mock
        │      ↓
        │   OTs abiertas
        │      ↓
        │   [MAXIMO]
        │
        └── DOCLINKS / DOCINFO
               ↓
            documentos
               ↓
              RAG
               ↓
        [FUENTE 1..N]

[MAXIMO] + [FUENTE 1..N]
        ↓
     Llama 3
        ↓
respuesta integrada
```

---

## 7. Ejecución

Desde la raíz del repositorio:

```bash
python rag/src/step11_transactional_plus_rag.py
```

La salida debe mostrar cuatro bloques:

```text
1. RUTA TRANSACCIONAL — WORKORDER
2. RUTA DOCUMENTAL — DOCLINKS + RAG
3. RETRIEVAL DOCUMENTAL
4. INTEGRACIÓN EN EL LLM
```

---

## 8. Qué esperamos comprobar

La prueba será satisfactoria si observamos que:

```text
PT-201 / PLANTA1
→ encuentra 3 OTs del activo
→ identifica 2 como abiertas en la baseline
→ excluye la OT en COMP

PT-201 / PLANTA1
→ resuelve 2 documentos por Doclinks
→ RAG recupera evidencia relevante

LLM
→ informa las OTs usando [MAXIMO]
→ responde la parte documental usando [FUENTE n]
```

La calidad exacta de redacción del LLM se observará, pero no se abrirá una nueva fase de tuning salvo que aparezca una necesidad pedagógica material.

---

## 9. Qué NO estamos haciendo todavía

Este Paso 11 no usa:

```text
Maximo real
API REST real
MCP activo
Maximo MCP Server oficial
agente autónomo
SQL generado por LLM
acciones sobre órdenes de trabajo
seguridad real
```

La orquestación está codificada de forma explícita para que siga siendo visible y explicable.

---

## 10. Aprendizaje objetivo

La regla mental que queremos comprobar en ejecución es:

```text
DATOS ESTRUCTURADOS / TRANSACCIONALES
→ consulta estructurada / API / MCP

DOCUMENTOS / CONOCIMIENTO
→ RAG

LLM
→ combina ambos cuando hace falta
```

Este Paso 11 es la primera demostración práctica conjunta de esa separación dentro del Learning Lab.

---

## 11. Siguiente paso previsto

Si el Paso 11 queda verificado, evaluaremos el siguiente salto con foco de aprendizaje:

```text
orquestación fija actual
→ decidir cuándo y cómo introducir Tools/MCP en la combinación
→ más adelante, agentes
```

No se introducirán agentes todavía hasta que la separación entre datos operativos, conocimiento documental y LLM quede suficientemente clara.
