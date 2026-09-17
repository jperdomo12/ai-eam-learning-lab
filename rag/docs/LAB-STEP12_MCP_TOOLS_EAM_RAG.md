# 🧪 Paso 12 — Tools/MCP + datos EAM + RAG

> 🎯 **Objetivo:** comprobar cómo cambia la solución cuando las capacidades que antes estaban cableadas en un único script pasan a exponerse como **Tools MCP** invocables por un Host/LLM.
>
> 📍 **Estado:** 🧪 **EN VALIDACIÓN — Tool transaccional verificada; Tool RAG en ajuste técnico de carga local de embeddings**
>
> 🗓️ **Actualizado:** 2026-09-17

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-17 | Se verifica `consultar_ots_abiertas_activo` desde Cline. `buscar_documentacion_activo` agota timeouts de 60 s y 180 s con carga lazy normal. Diagnóstico local: MiniLM tarda ~46,7 s con resolución normal y ~20,8 s usando `local_files_only=True`. Se descarta seguir aumentando timeouts; el servidor vuelve a publicar Tools inmediatamente y la primera llamada RAG cargará MiniLM solo desde caché local. |
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

En el Paso 12 se separan esas capacidades como Tools:

```text
Cline / LLM
     ↓
MCP Client
     ↓
MCP Server: eam-rag-lab
     ├── consultar_ots_abiertas_activo(...)
     └── buscar_documentacion_activo(...)
```

La idea pedagógica es observar que el Host/LLM puede decidir invocar capacidades diferentes según la necesidad de la pregunta.

Todavía no se introduce un agente autónomo ni acciones de escritura sobre Maximo.

---

## 2. Decisión de diseño

El MCP Lab histórico bajo `mcp/` permanece **cerrado / congelado**.

Este nuevo experimento vive en:

```text
rag/src/step12_eam_rag_mcp_server.py
```

porque forma parte de la evolución del bloque actual `EAM + RAG` y no modifica el servidor histórico `mcp/src/maximo_mcp.py`.

Así mantenemos:

```text
mcp/
→ evidencia y aprendizaje MCP ya cerrado

rag/
→ evolución actual donde RAG se combina con contexto EAM y ahora se expone como Tool
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

No utiliza:

```text
embeddings
RAG
LLM interno
```

Para la baseline del LAB, los estados considerados abiertos siguen siendo:

```text
WAPPR
APPR
INPRG
WMATL
```

### Validación local

✅ Verificada desde Cline usando exclusivamente `eam-rag-lab`.

Resultado:

```text
OTs totales del activo/sitio: 3
OTs abiertas: 2
OT-PT201-01 | APPR  | PM | prioridad 2
OT-PT201-02 | INPRG | CM | prioridad 1
```

Se observó además que el LLM del Host añadió interpretación semántica sobre códigos y prioridad. Esto refuerza la separación:

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

Importante:

> **La Tool RAG no llama a otro LLM para redactar la respuesta final.**

El Host/LLM recibe la evidencia recuperada y realiza la síntesis final. Esto evita ocultar un segundo LLM dentro de la Tool y mantiene visible la separación:

```text
RAG Tool
→ recupera evidencia

Host LLM
→ interpreta / combina / responde
```

### Incidencia de carga observada

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

Baseline técnica vigente:

```text
servidor MCP inicia inmediatamente
→ publica Tools
→ primera llamada RAG carga MiniLM de forma lazy
→ carga exclusivamente desde caché local
→ siguientes llamadas reutilizan la misma instancia en memoria
```

Esto evita consultas innecesarias al Hugging Face Hub y mantiene `stdout` reservado al protocolo MCP `stdio`.

---

## 5. Arquitectura del experimento

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
       respuesta
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

Dependencias declaradas:

```text
sentence-transformers
mcp
```

El servidor utiliza `FastMCP`, igual que el aprendizaje previo del MCP Lab, pero no reutiliza ni modifica el servidor histórico.

---

## 7. Configuración local en Cline

Ruta documentada actualmente para la configuración de Cline:

```text
C:\Users\jpperdomo\.cline\data\settings\cline_mcp_settings.json
```

Desde la UI:

```text
VS Code
→ Cline
→ Customize
→ MCP
→ Installed
→ Edit Configuration
```

Debe existir un servidor adicional, por ejemplo:

```json
"eam-rag-lab": {
  "transport": {
    "type": "stdio",
    "command": "python",
    "args": [
      "-u",
      "C:/Users/jpperdomo/JP/Profesional/IA/Proyecto_AI-EAM-LEARNING-LAB/ai-eam-learning-lab/rag/src/step12_eam_rag_mcp_server.py"
    ]
  },
  "timeout": 180
}
```

Si la configuración `maximo` existente usa una ruta absoluta a otro intérprete Python, conviene reutilizar ese patrón o utilizar el intérprete donde estén disponibles `mcp` y `sentence-transformers`.

No se requieren API keys ni secretos para este servidor.

---

## 8. Verificación previa del entorno

Desde el terminal del repositorio se verificó:

```bash
python -c "import mcp, sentence_transformers; print('Dependencias OK')"
```

Resultado:

```text
Dependencias OK
```

La caché local del modelo también quedó verificada con `local_files_only=True`.

---

## 9. Prueba controlada en Cline

Una vez activo `eam-rag-lab`, Cline debe mostrar:

```text
2 Tools
```

Prueba final prevista:

```text
Usa exclusivamente el servidor MCP eam-rag-lab para responder esta pregunta.
Para PT-201 en PLANTA1, consulta tanto los datos de órdenes de trabajo
como la documentación asociada y responde:

¿Tiene alguna OT abierta y qué indica su documentación que debo revisar
antes de intervenirlo?

Distingue claramente los hechos operativos [MAXIMO] de la evidencia
documental [FUENTE n].
```

Resultado esperado:

```text
Tool transaccional
→ 2 OTs abiertas
→ OT-PT201-01 APPR
→ OT-PT201-02 INPRG

Tool documental
→ evidencia de inspección previa
→ seguridad previa
→ preparación antes de calibrar

Host LLM
→ combina ambas salidas
```

---

## 10. Qué queremos observar

La validación no consiste solo en obtener una respuesta correcta.

Queremos observar el cambio de responsabilidad:

```text
Paso 11
script decide el flujo

Paso 12
Tools exponen capacidades
Host/LLM selecciona e invoca capacidades
```

También queremos comprobar el aprendizaje ya visto en el MCP Lab:

> **Servidor MCP activo no garantiza que el modelo seleccione siempre correctamente las Tools.**

Por eso nombre, descripción y esquema de parámetros de cada Tool se han diseñado de forma explícita.

---

## 11. Qué NO estamos haciendo todavía

No se valida aún:

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

## 12. Criterio de cierre

El Paso 12 quedará ✅ **VERIFICADO** cuando Cline confirme que:

```text
eam-rag-lab está activo
→ expone 2 Tools
→ consultar_ots_abiertas_activo aporta datos [MAXIMO]
→ buscar_documentacion_activo aporta evidencia RAG [FUENTE n]
→ el Host/LLM utiliza ambas capacidades
→ produce una respuesta integrada
```

Estado actual:

```text
consultar_ots_abiertas_activo  ✅ verificada
buscar_documentacion_activo    🧪 pendiente de revalidación tras carga local-only
composición de ambas Tools      ⏳ pendiente
```

Una vez verificado, podremos comparar claramente:

```text
orquestación fija
vs.
Tool calling mediante MCP
```

antes de decidir si el siguiente salto debe ser hacia una composición MCP más realista o hacia conceptos de agentes.
