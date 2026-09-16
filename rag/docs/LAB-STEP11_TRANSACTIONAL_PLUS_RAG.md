# 🧪 Paso 11 — Datos transaccionales + RAG documental

> 🎯 **Objetivo:** combinar, para un mismo contexto EAM, datos estructurados/transaccionales simulados de Maximo con conocimiento documental recuperado mediante RAG.
>
> 📍 **Estado:** ✅ **VERIFICADO — datos transaccionales + RAG documental integrados**
>
> 🗓️ **Actualizado:** 2026-09-16

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-16 | ✅ Verificación local del Paso 11: `WORKORDER` identifica 2 OTs abiertas de 3; Doclinks limita el universo documental; RAG recupera evidencia relevante y Llama 3 combina ambos tipos de evidencia en una respuesta integrada. Se observa que el modelo no respetó literalmente el formato de cita `[MAXIMO]`/`[FUENTE n]`, limitación menor ya conocida que no abre una nueva fase de tuning. |
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

Pregunta guía:

```text
¿Tiene el PT-201 alguna OT abierta y qué indica su documentación
que debo revisar antes de intervenirlo?
```

---

## 2. Reutilización del MCP Lab sin acoplar ambos laboratorios

El MCP Lab ya había utilizado campos típicos de órdenes de trabajo Maximo:

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

Los datos viven separadamente en:

```text
rag/data/maximo_mock/workorders.json
```

---

## 3. WORKORDER simulado

Para `PT-201 / PLANTA1` existen tres órdenes:

```text
OT-PT201-01 | APPR  | prioridad 2 | PM | abierta en la baseline
OT-PT201-02 | INPRG | prioridad 1 | CM | abierta en la baseline
OT-PT201-03 | COMP  | prioridad 3 | PM | excluida como completada
```

Campos utilizados:

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

Para esta prueba se consideran abiertos:

```text
WAPPR
APPR
INPRG
WMATL
```

Esta lista es una baseline pedagógica; en Maximo real pueden existir sinónimos/configuraciones propias del dominio de estados.

---

## 4. Dos rutas distintas para una sola pregunta

### Ruta A — datos transaccionales

```text
ASSETNUM + SITEID
→ filtrar WORKORDER
→ filtrar STATUS
→ obtener OTs abiertas
```

No hay embeddings ni RAG en esta ruta. Es consulta estructurada exacta sobre datos operativos simulados.

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

```text
¿Tiene el PT-201 alguna OT abierta?
→ datos transaccionales

¿Qué indica su documentación que debo revisar antes de intervenirlo?
→ conocimiento documental
```

La descomposición está **codificada explícitamente**, no decidida autónomamente por un agente.

Consulta documental usada para retrieval:

```text
¿Qué debo revisar antes de intervenir o calibrar el PT-201?
```

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

## 7. Resultado verificado

La ejecución local confirmó:

```text
PT-201 / PLANTA1
→ 3 OTs del activo/sitio
→ 2 OTs abiertas
→ 1 OT COMP excluida

OT-PT201-01 → APPR  → abierta
OT-PT201-02 → INPRG → abierta
OT-PT201-03 → COMP  → excluida
```

La ruta documental confirmó:

```text
2 documentos asociados por Doclinks
11 chunks de contenido candidatos
Top-k = 4
```

Los cuatro chunks recuperados fueron relevantes para la pregunta:

```text
1. Manual PT-201 — Inspección previa
2. Manual PT-201 — Seguridad previa
3. Manual PT-201 — Procedimiento de calibración
4. Procedimiento de seguridad — Antes de calibrar un transmisor de presión
```

La respuesta del LLM integró correctamente:

```text
[datos operativos]
→ existen 2 OTs abiertas
→ OT-PT201-01
→ OT-PT201-02

[conocimiento documental]
→ permiso de trabajo
→ aislamiento del instrumento
→ eliminación de presión residual
→ condición segura
→ EPP
→ revisión de conectores/tubing
→ ausencia de fugas
→ identificación PT-201
→ rango 0–10 bar
```

### Limitación observada

El modelo respetó el origen de la información, pero no siguió literalmente la convención de citas solicitada:

```text
esperado → [MAXIMO], [FUENTE 1], [FUENTE 2]
observado → "Según los datos transaccionales MAXIMO", "(FUENTE 1)", "(FUENTE 2)"
```

No afecta al objetivo pedagógico del Paso 11 y no justifica reabrir tuning de prompts.

El warning de Hugging Face por requests no autenticados tampoco afectó la prueba: MiniLM cargó y el retrieval se ejecutó correctamente.

---

## 8. Aprendizaje consolidado

La práctica verifica de forma visible la regla mental:

```text
DATOS ESTRUCTURADOS / TRANSACCIONALES
→ consulta estructurada / API / MCP

DOCUMENTOS / CONOCIMIENTO
→ RAG

LLM
→ combina ambos cuando hace falta
```

Y además:

```text
WORKORDER
→ aporta estado operativo

DOCLINKS
→ determina qué documentos aplican

RAG
→ recupera conocimiento dentro de esos documentos

LLM
→ integra ambas clases de evidencia
```

---

## 9. Qué NO valida este Paso 11

Todavía no se utiliza:

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

La orquestación permanece codificada de forma explícita para que sea visible y explicable.

---

## 10. Siguiente paso previsto

Con la separación ya verificada, el siguiente salto de aprendizaje es pasar de:

```text
orquestación fija en código
```

a estudiar cómo expresar esas capacidades como **Tools / MCP**, manteniendo todavía controlada la orquestación y dejando los agentes para una etapa posterior.
