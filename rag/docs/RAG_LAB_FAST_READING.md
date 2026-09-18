# ⚡ RAG LAB — Fast Reading

> 🎯 **Objetivo:** recuperar en pocos minutos qué se aprendió, qué se probó y cómo quedó cerrado el bloque RAG + EAM + MCP.
>
> 📍 **Estado:** ✅ **RAG BÁSICO CERRADO** · ✅ **APLICACIÓN EAM VERIFICADA HASTA PASO 12**
>
> 🗓️ **Actualizado:** 2026-09-18
>
> 📘 **Documento canónico:** [`RAG_LIVING_DOCUMENTATION.md`](RAG_LIVING_DOCUMENTATION.md)

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-18 | Se añaden aclaraciones conceptuales sobre vector search, RAG como capability, MCP y múltiples fuentes documentales; se alinea el estado con la transferencia ya cerrada hacia AI-EAM-MAXIMO. |
| 2026-09-18 | Se actualiza el Fast Reading hasta Paso 12 y se alinea con la regla de continuidad sin depender de chats antiguos. |
| 2026-09-14 | Se incorpora la distinción práctica entre RAG documental y acceso a datos estructurados/transaccionales mediante SQL, API o MCP. |
| 2026-09-14 | Creación del resumen de recuperación rápida al cierre de los Pasos 01–08 del RAG Learning Lab. |

---

## 1. En una frase

Se verificó, de forma progresiva y práctica, que:

```text
Maximo / EAM
→ aporta contexto y datos operativos

RAG
→ recupera conocimiento documental

MCP
→ expone capacidades como Tools

LLM / Host
→ selecciona, interpreta y combina la evidencia
```

---

## 2. Mapa completo de Pasos 01–12

```text
01  descubrir documentos                              ✅
02  leer y hacer chunking visible                     ✅
03  retrieval léxico                                  ✅
04  retrieval semántico                               ✅
04b excluir estructura/metadata                       ✅
05  persistir y consultar índice vectorial            ✅
06  construir contexto fundamentado                   ✅
07  evaluar retrieval y sensibilidad Top-k            ✅
08  generar, evaluar, abstenerse y controlar prompt   ✅
09  Maximo simulado + Doclinks                        ✅
10  contexto EAM → Doclinks → RAG → LLM               ✅
11  datos transaccionales + RAG                       ✅
12  Tools/MCP + EAM + RAG                             ✅
```

No hay un Paso 13 aprobado automáticamente.

---

## 3. Arquitectura mental RAG

```text
DOCUMENTOS
   ↓
chunking
   ↓
embeddings / índice
   ↓
pregunta
   ↓
retrieval
   ↓
Top-k
   ↓
TEXTO ORIGINAL + PROCEDENCIA
   ↓
LLM
   ↓
respuesta
```

Idea clave:

> **Los embeddings ayudan a localizar evidencia; el LLM recibe el texto original recuperado.**

RAG no reentrena al LLM.

---

## 4. Qué aprendimos del retrieval

```text
similarity alta ≠ confianza
similarity alta ≠ evidencia suficiente
Top-k encontrado ≠ respuesta encontrada
```

Y:

```text
BUEN LLM + BUEN DOCUMENTO + MAL RETRIEVAL
=
MALA RESPUESTA RAG
```

El Caso D preguntó deliberadamente por un dato inexistente —el par de apriete de bornes del PT-201— y la respuesta correcta fue abstenerse.

---

## 5. Retrieval correcto tampoco garantiza buena generación

En el Paso 08 se observó:

```text
retrieval completo
+ contexto suficiente
≠
respuesta necesariamente completa
```

Con el mismo retrieval y LLM, un prompt orientado a revisar todas las partes de la pregunta mejoró la cobertura.

El control 08C fijó:

```text
temperature = 0
seed = 42
```

para comparar prompts de forma reproducible.

No se decidió seguir optimizando prompts/modelos porque ya se había alcanzado el objetivo de aprendizaje.

---

## 6. Datos estructurados ≠ RAG documental

Regla práctica consolidada:

```text
DATOS ESTRUCTURADOS / TRANSACCIONALES
→ SQL / API / MCP

DOCUMENTOS / CONOCIMIENTO
→ RAG

LLM / Host
→ combina ambos cuando hace falta
```

Ejemplo:

```text
¿Cuántas OTs abiertas tiene el activo?
→ Maximo / API / MCP

¿Qué indica su manual?
→ RAG
```

Una base de datos puede participar en RAG si almacena/busca embeddings, pero consultar una base de datos no convierte automáticamente la consulta en RAG.

Aclaración útil:

```text
tabla estructurada
├─ campos normales → SQL / filtros
└─ campo vector    → búsqueda semántica/vectorial
```

La tabla sigue siendo estructurada; la búsqueda sobre el vector es semántica.

---

## 7. Maximo + Doclinks — Paso 09

Se simuló:

```text
ASSET
→ DOCLINKS
→ DOCINFO
→ archivo asociado
```

Baseline:

```text
PT-201 / PLANTA1
ASSETUID = 1001
ASSETID  = 2001
2 documentos asociados
```

En el LAB:

```text
DOCLINKS.OWNERID → ASSET.ASSETUID
```

como variante site-specific deliberada.

**No es una regla universal de Maximo.** `ASSETID` también puede intervenir según comportamiento/configuración.

Aprendizaje:

> **Doclinks resuelve qué documentación aplica; RAG busca después dentro de esa documentación.**

---

## 8. Contexto EAM → RAG — Paso 10

Se verificó:

```text
PT-201 / PLANTA1
→ ASSET
→ DOCLINKS / DOCINFO
→ 2 documentos asociados
→ RAG solo sobre esos documentos
→ Llama 3
→ respuesta
```

Regla:

```text
MAXIMO / EAM
→ determina QUÉ documentos aplican

RAG
→ determina QUÉ evidencia es relevante

LLM
→ interpreta y redacta
```

Se observó además una omisión puntual del LLM pese a que la evidencia sí estaba recuperada. Se documentó y no se abrió más tuning.

---

## 9. Datos transaccionales + RAG — Paso 11

Se añadió `WORKORDER` simulado:

```text
OT-PT201-01 | APPR  | PM | prioridad 2 | abierta
OT-PT201-02 | INPRG | CM | prioridad 1 | abierta
OT-PT201-03 | COMP  | PM | prioridad 3 | excluida
```

Una sola pregunta utilizó dos rutas:

```text
WORKORDER
→ consulta estructurada exacta
              \
               → LLM
              /
DOCLINKS / DOCINFO
→ RAG documental
```

La orquestación todavía estaba escrita explícitamente en Python.

---

## 10. Tools/MCP — Paso 12

Se creó:

```text
rag/src/step12_eam_rag_mcp_server.py
```

con dos Tools:

```text
consultar_ots_abiertas_activo(...)
→ datos WORKORDER
→ [MAXIMO]

buscar_documentacion_activo(...)
→ Doclinks + RAG
→ [FUENTE 1..N]
```

La Tool RAG **no llama a otro LLM**. Devuelve evidencia; Cline/Host LLM sintetiza.

Validación final:

```text
Cline
→ reconoció 2 Tools
→ verificó ambas individualmente
→ ante una pregunta integrada seleccionó ambas
→ combinó [MAXIMO] + [DOCUMENTACIÓN]
```

Diferencia clave:

```text
Paso 11 → script decide el flujo
Paso 12 → Host/LLM decide qué Tools necesita
```

Eso es **tool calling y composición dinámica**, no autonomía completa de un agente.

---

## 11. Incidencia técnica útil del Paso 12

La primera Tool RAG agotó timeouts.

Diagnóstico:

```text
carga normal MiniLM       ~46,7 s
local_files_only=True     ~20,8 s
```

Solución final:

```text
servidor publica Tools inmediatamente
→ primera llamada RAG carga MiniLM lazy desde caché local
→ siguientes llamadas reutilizan la instancia
```

La configuración sanitizada está en:

```text
rag/config/cline_step12_mcp_settings.example.json
```

---

## 12. Baseline pedagógica usada

```text
Embeddings → MiniLM multilingual
Índice     → NumPy + JSON
Top-k      → 4 como baseline pedagógica
Runtime    → Ollama en Pasos 08–11
LLM        → Llama 3 local en Pasos 08–11
MCP        → FastMCP en Paso 12
Host       → Cline en Paso 12
```

Nada de esto queda automáticamente aprobado para AI-EAM-MAXIMO.

---

## 13. Qué NO transferir como decisión de producto

No convertir automáticamente en arquitectura:

```text
MiniLM
384 dimensiones
NumPy + JSON
Top-k = 4
Ollama
Llama 3
FastMCP
local_files_only=True
timeout = 180
prompts exactos
```

Siguen abiertos para el producto:

```text
embedding model
vector DB
LLM provider
agent framework
chunking definitivo
Top-k / thresholds
runtime local vs cloud
```

---

## 14. Qué NO profundizar ahora

No continuar por defecto con:

```text
reranking
retrieval híbrido
threshold tuning
RAGAS
LLM-as-judge
auto-evaluadores avanzados
comparación de modelos
prompt tuning adicional
```

Solo hacerlo si una necesidad EAM concreta lo exige.

---

## 15. Aclaraciones conceptuales posteriores

```text
MCP
→ una forma estándar de exponer capacidades/Tools al LLM

RAG
→ una capacidad de recuperación de conocimiento; no es MCP

RAG vía MCP
→ posible: se expone RAG como una Tool, como hicimos en el Paso 12
```

El LLM usa una capacidad porque el sistema se la presenta con nombre, descripción y parámetros. MCP es una forma de hacerlo; también existen tool/function calling interno, orquestadores o workflows.

Una misma capacidad RAG puede consultar varias fuentes autorizadas:

```text
Maximo Doclinks
Documentum / otro repositorio documental
→ documentos aplicables
→ RAG
→ evidencia
```

Conviene mantener separadas internamente las capacidades EAM y Knowledge/RAG, aunque ambas puedan exponerse desde un mismo servidor MCP.

---

## 16. Relación con AI-EAM-MAXIMO

Después de cerrar Paso 12 se revisaron los aprendizajes transferibles al producto.

El assessment fue aprobado e integrado en `jperdomo12/ai-driven-eam-copilot` mediante PR #7. El LAB queda cerrado para este bloque y solo debe reabrirse ante una necesidad EAM concreta con valor educativo/práctico.

---

## 17. Qué leer para retomar

Mantenerlo simple:

```text
1. RAG_LAB_FAST_READING.md
   → recordar el tema

2. RAG_LIVING_DOCUMENTATION.md
   → estado consolidado

3. RAG_LAB_HANDOFF.md
   → continuidad operativa

4. LAB-STEP*.md / código
   → solo si necesitas detalle
```

Con esos documentos y el código de GitHub no debe ser necesario reconstruir chats antiguos.
