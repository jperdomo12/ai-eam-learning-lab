# 🧪 Paso 12 — Tools/MCP + datos EAM + RAG

> 🎯 **Objetivo:** comprobar cómo cambia la solución cuando las capacidades que antes estaban cableadas en un único script pasan a exponerse como **Tools MCP** invocables por un Host/LLM.
>
> 📍 **Estado:** ✅ **VERIFICADO — Tool transaccional, Tool RAG y composición de ambas desde Cline**
>
> 🗓️ **Actualizado:** 2026-09-17

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-17 | ✅ Se verifica la composición final: Cline selecciona e invoca por sí mismo las dos Tools de `eam-rag-lab` para una sola pregunta integrada y combina hechos `[MAXIMO]` con evidencia documental `[FUENTE n]`. Paso 12 cerrado. |
| 2026-09-17 | ✅ Se verifica `buscar_documentacion_activo` tras cambiar la carga de MiniLM a `local_files_only=True`; la Tool recupera 4 fuentes relevantes desde 2 documentos asociados por Doclinks. |
| 2026-09-17 | Se verifica `consultar_ots_abiertas_activo` desde Cline. `buscar_documentacion_activo` agotó timeouts de 60 s y 180 s con carga lazy normal. Diagnóstico local: MiniLM tarda ~46,7 s con resolución normal y ~20,8 s usando `local_files_only=True`. Se descartó seguir aumentando timeouts. |
| 2026-09-16 | Se prepara el Paso 12 con un MCP Server independiente dentro de `rag/`, dos Tools (`consultar_ots_abiertas_activo` y `buscar_documentacion_activo`) y una configuración Cline de ejemplo. |

---

## 1. Qué cambia respecto al Paso 11

El Paso 11 utilizó una orquestación fija en Python:

```text
script
→ consulta WORKORDER
→ resuelve DOCLINKS / DOCINFO
→ ejecuta RAG
→ llama a Llama 3
→ produce respuesta
```

En el Paso 12 las capacidades pasan a exponerse como Tools:

```text
Cline / LLM
     ↓
MCP Client
     ↓
MCP Server: eam-rag-lab
     ├── consultar_ots_abiertas_activo(...)
     └── buscar_documentacion_activo(...)
```

La diferencia verificada es:

```text
PASO 11
script decide previamente todo el flujo

PASO 12
Tools exponen capacidades
Host/LLM decide cuáles necesita e invoca
```

Todavía no se introduce un agente autónomo ni acciones de escritura sobre Maximo.

---

## 2. Decisión de diseño

El MCP Lab histórico bajo `mcp/` permanece **cerrado / congelado**.

Este experimento vive en:

```text
rag/src/step12_eam_rag_mcp_server.py
```

porque forma parte de la evolución del bloque `EAM + RAG` y no modifica el servidor histórico `mcp/src/maximo_mcp.py`.

```text
mcp/
→ evidencia y aprendizaje MCP ya cerrado

rag/
→ evolución actual donde RAG se combina con contexto EAM y se expone como Tool
```

---

## 3. Tool 1 — datos transaccionales

```text
consultar_ots_abiertas_activo(assetnum, siteid)
```

Responsabilidad:

```text
ASSETNUM + SITEID
→ WORKORDER simulado
→ filtro estructurado exacto
→ OTs abiertas
→ [MAXIMO]
```

No utiliza embeddings ni RAG.

Para la baseline del LAB, los estados considerados abiertos son:

```text
WAPPR
APPR
INPRG
WMATL
```

### Validación

✅ Verificada desde Cline usando exclusivamente `eam-rag-lab`.

Resultado:

```text
OTs totales del activo/sitio: 3
OTs abiertas: 2
OT-PT201-01 | APPR  | PM | prioridad 2
OT-PT201-02 | INPRG | CM | prioridad 1
```

El Host LLM añadió interpretaciones de códigos y prioridad en su redacción. Esto refuerza la separación:

```text
Tool → aporta datos
Host LLM → interpreta / explica
```

---

## 4. Tool 2 — conocimiento documental

```text
buscar_documentacion_activo(assetnum, siteid, pregunta)
```

Responsabilidad:

```text
ASSET
→ DOCLINKS
→ DOCINFO
→ documentos asociados
→ chunks de contenido
→ embeddings MiniLM
→ retrieval semántico
→ Top-k
→ texto original + procedencia
```

La Tool devuelve evidencia documental como:

```text
[FUENTE 1]
Documento: ...
Sección: ...
Contenido: ...
```

> **La Tool RAG no llama a otro LLM para redactar la respuesta final.**

El Host/LLM recibe la evidencia recuperada y realiza la síntesis final:

```text
RAG Tool
→ recupera evidencia

Host LLM
→ interpreta / combina / responde
```

### Incidencia técnica y solución

Las primeras llamadas desde Cline agotaron:

```text
60 s
180 s
```

El modelo se probó directamente con el mismo intérprete Python del servidor:

```text
carga normal                  → ~46,7 s
local_files_only=True         → ~20,8 s
```

La precarga del modelo antes de `mcp.run()` se descartó porque retrasaba el arranque del servidor y podía impedir que Cline registrara las Tools a tiempo.

Baseline técnica final:

```text
servidor MCP inicia inmediatamente
→ publica 2 Tools
→ primera llamada RAG carga MiniLM de forma lazy
→ carga exclusivamente desde caché local (`local_files_only=True`)
→ siguientes llamadas reutilizan la misma instancia en memoria
```

Se mantiene `stdout` reservado al protocolo MCP `stdio`.

### Validación

✅ Verificada desde Cline.

Para la pregunta:

```text
¿Qué debo revisar antes de intervenir o calibrar el PT-201?
```

la Tool resolvió 2 documentos asociados por Doclinks y recuperó Top-k=4:

```text
FUENTE 1 → manual_transmisor_PT201.md / 3. Inspección previa
FUENTE 2 → manual_transmisor_PT201.md / 2. Seguridad previa
FUENTE 3 → manual_transmisor_PT201.md / 4. Procedimiento de calibración
FUENTE 4 → procedimiento_seguridad_instrumentacion.md / 3. Antes de calibrar un transmisor de presión
```

El Host LLM organizó luego esa evidencia en una respuesta final sin necesitar un segundo LLM dentro de la Tool.

---

## 5. Arquitectura verificada

```text
Usuario
  ↓
Cline + modelo seleccionado
  ↓
MCP Client
  ↓
eam-rag-lab MCP Server
  │
  ├─ Tool A: consultar_ots_abiertas_activo
  │           ↓
  │        WORKORDER mock
  │           ↓
  │        [MAXIMO]
  │
  └─ Tool B: buscar_documentacion_activo
              ↓
          ASSET / DOCLINKS / DOCINFO
              ↓
             RAG
              ↓
          [FUENTE 1..N]

[MAXIMO] + [FUENTE 1..N]
          ↓
       Host LLM
          ↓
       respuesta integrada
```

En esta etapa:

```text
MCP → protocolo para exponer/invocar capacidades
Tool A → datos operativos estructurados
Tool B → retrieval documental RAG
LLM del Host → decide qué Tools necesita y sintetiza
```

---

## 6. Implementación

Servidor:

```text
rag/src/step12_eam_rag_mcp_server.py
```

Configuración Cline de ejemplo:

```text
rag/config/cline_step12_mcp_settings.example.json
```

Dependencias:

```text
sentence-transformers
mcp
```

El servidor utiliza `FastMCP`, igual que el aprendizaje previo del MCP Lab, pero no reutiliza ni modifica el servidor histórico.

---

## 7. Configuración local validada

Ruta actual de configuración de Cline:

```text
C:\Users\jpperdomo\.cline\data\settings\cline_mcp_settings.json
```

El servidor `eam-rag-lab` quedó activo con:

```text
2 Tools
```

y timeout configurado en 180 s. El timeout ampliado se conserva como margen, aunque la solución real al problema de latencia fue usar la caché local del modelo.

No se requieren API keys ni secretos para este servidor.

---

## 8. Verificación final de composición

Pregunta usada:

```text
Para el activo PT-201 en el sitio PLANTA1 responde:

¿Tiene alguna orden de trabajo abierta y qué indica su documentación
que debo revisar antes de intervenirlo?

Decide qué Tools del servidor eam-rag-lab necesitas utilizar.
```

No se indicó al modelo qué Tool debía llamar ni en qué orden.

Resultado observado:

```text
Cline / Host LLM
→ seleccionó consultar_ots_abiertas_activo
→ seleccionó buscar_documentacion_activo
→ ejecutó ambas correctamente
→ distinguió [MAXIMO] de [DOCUMENTACIÓN]
→ produjo una respuesta integrada
```

Hechos operativos recuperados:

```text
OT-PT201-01 | APPR  | PM | prioridad 2
OT-PT201-02 | INPRG | CM | prioridad 1
```

Evidencia documental recuperada:

```text
inspección previa
seguridad previa
procedimiento de calibración
seguridad específica antes de calibrar
```

✅ **Criterio de cierre satisfecho.**

---

## 9. Aprendizaje principal

La práctica demuestra una evolución clara:

```text
PASO 11
orquestación fija en Python
→ el programador decide el flujo

PASO 12
capacidades expuestas como Tools MCP
→ el Host/LLM interpreta la pregunta
→ selecciona las Tools necesarias
→ recibe resultados estructurados/documentales
→ integra la respuesta
```

Esto no convierte automáticamente al sistema en un agente autónomo. Demuestra **tool calling y composición dinámica de capacidades mediante MCP**.

También se confirma:

> **Servidor MCP activo no implica selección perfecta de Tools en todos los casos.**

Nombre, descripción y esquema de parámetros siguen siendo parte importante del diseño de una Tool.

---

## 10. Qué NO se validó

```text
Maximo real
IBM Maximo MCP Server oficial
acciones de escritura
workflow real
seguridad productiva
autorización documental real
agente autónomo
planificación multistep compleja
```

Tampoco se incorpora nada automáticamente al producto AI-EAM-MAXIMO.

---

## 11. Estado final

```text
consultar_ots_abiertas_activo  ✅ verificada
buscar_documentacion_activo    ✅ verificada
composición de ambas Tools      ✅ verificada
```

**Paso 12: ✅ VERIFICADO / CERRADO para el alcance pedagógico previsto.**

El siguiente salto debe decidirse por valor de aprendizaje, evitando añadir complejidad solo por continuar la secuencia. Los candidatos naturales son:

```text
A. composición MCP más realista / contraste con IBM Maximo MCP oficial
B. introducir conceptos mínimos de agente sobre capacidades ya comprendidas
C. cerrar este bloque y transferir aprendizajes candidatos a AI-EAM-MAXIMO
```
