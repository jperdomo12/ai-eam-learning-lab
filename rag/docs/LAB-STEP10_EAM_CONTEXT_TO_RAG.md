# 🧪 Paso 10 — Contexto EAM → Doclinks → RAG → LLM

> 🎯 **Objetivo:** integrar por primera vez el contexto EAM simulado con el RAG ya validado, de modo que Maximo determine qué documentos son aplicables y RAG recupere conocimiento únicamente dentro de esos documentos.
>
> 📍 **Estado:** ✅ **VERIFICADO — integración EAM → Doclinks → RAG → LLM comprobada localmente; se documenta una limitación puntual de generación**
>
> 🗓️ **Actualizado:** 2026-09-16

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-18 | Auditoría final: se añade Resumen de contenido y el antiguo siguiente paso se marca como continuidad histórica ya completada en el Paso 11. |
| 2026-09-16 | ✅ Ejecución local verificada del flujo completo `PT-201 / PLANTA1 → ASSET → DOCLINKS → DOCINFO → documentos asociados → retrieval semántico → Llama 3`. Se documenta una inconsistencia puntual de la respuesta generada: el LLM afirmó que no había evidencia sobre `as-found` y observaciones aunque la FUENTE 2 sí las contiene. |
| 2026-09-16 | Creación inicial del Paso 10, conectando la resolución `ASSET → DOCLINKS → DOCINFO` del Paso 09 con retrieval semántico y generación local. |

---

## 🧭 Resumen de contenido

| Punto | Contenido |
|---|---|
| **1. Cambio respecto al Paso 09** | Introduce RAG después de resolver qué documentos corresponden al activo. |
| **2. Script** | Identifica la implementación utilizada para el flujo EAM → documentos → RAG → LLM. |
| **3. Reutilización** | Muestra qué componentes RAG previos se reutilizan sin rehacer el laboratorio. |
| **4. Simplificación** | Explica las decisiones pedagógicas que mantienen visible el mecanismo. |
| **5. Ejecución** | Registra la prueba local completa con PT-201 y su documentación asociada. |
| **6. Generación** | Documenta la respuesta y una limitación puntual observada en el LLM. |
| **7. Verificado** | Consolida la separación Maximo/EAM → documentos, RAG → evidencia, LLM → redacción. |
| **8. Límites** | Enumera lo que todavía no valida el experimento. |
| **9. Cierre** | Confirma el flujo completo para el objetivo del Paso 10. |
| **10. Continuidad posterior** | Registra que la incorporación de datos transaccionales se completó en el Paso 11. |

---

## 1. Qué cambia respecto al Paso 09

El Paso 09 verificó únicamente:

```text
PT-201 / PLANTA1
→ ASSET
→ DOCLINKS
→ DOCINFO
→ archivos asociados
```

El Paso 10 añade las capas RAG y LLM:

```text
PT-201 / PLANTA1
        ↓
Maximo mock
        ↓
ASSET → DOCLINKS → DOCINFO
        ↓
documentos asociados
        ↓
chunking + embeddings
        ↓
retrieval semántico
        ↓
Top-k
        ↓
texto original recuperado
        ↓
Llama 3 vía Ollama
        ↓
respuesta fundamentada
```

Idea central:

> **Maximo determina QUÉ documentación aplica al contexto EAM; RAG determina QUÉ evidencia dentro de esa documentación responde la pregunta.**

---

## 2. Script

```text
rag/src/step10_eam_context_to_rag.py
```

Por defecto trabaja con:

```text
ASSETNUM = PT-201
SITEID   = PLANTA1
```

y con la pregunta:

```text
Estoy trabajando sobre el activo PT-201 en PLANTA1.
¿Cómo debo calibrarlo según la documentación asociada al activo?
```

---

## 3. Reutilización de lo ya aprendido

El Paso 10 no crea un RAG nuevo. Reutiliza componentes ya verificados:

```text
Paso 02 → chunking
Paso 04 → embeddings + similitud semántica
Paso 04b → excluir estructura/metadata del ranking
Paso 06 → contexto fundamentado
Paso 08B → prompt orientado a completeness
Paso 08 → generación local con Ollama + Llama 3
Paso 09 → resolución Maximo ASSET + DOCLINKS + DOCINFO
```

---

## 4. Simplificación pedagógica importante

En los Pasos 05–08 se utilizó un índice vectorial persistente.

En el Paso 10 hacemos algo deliberadamente más simple para observar la integración EAM:

```text
Maximo mock
→ selecciona documentos
→ se generan embeddings en memoria solo para esos documentos
→ retrieval
```

No se modifica ni se reconstruye el índice persistente existente.

Esto **no es una decisión de arquitectura productiva**. En una solución real sería habitual mantener un índice persistente más amplio y aplicar filtros de metadata/documento/seguridad antes o durante el retrieval.

Para el objetivo actual basta con demostrar claramente:

```text
contexto EAM
→ reduce el universo documental
→ RAG trabaja dentro de ese universo
```

---

## 5. Ejecución verificada

Comando ejecutado desde la raíz del repositorio:

```bash
python rag/src/step10_eam_context_to_rag.py
```

Contexto resuelto:

```text
ASSETNUM : PT-201
SITEID   : PLANTA1
ASSETUID : 1001
ASSETID  : 2001
OWNER KEY: ASSETUID (baseline site-specific)
```

Documentos resueltos por Maximo mock:

```text
MANUAL-PT201    → manual_transmisor_PT201.md
PROC-SEG-INSTR  → procedimiento_seguridad_instrumentacion.md
```

Resultado del alcance RAG:

```text
Documentos habilitados por Doclinks : 2
Chunks totales                      : 14
Chunks de contenido candidatos      : 11
Chunks estructura/metadata excluidos: 3
```

Modelo de embeddings:

```text
sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
384 dimensiones
```

Top-k efectivo:

```text
#1  0.4526  manual_transmisor_PT201.md                  | 3. Inspección previa
#2  0.3537  procedimiento_seguridad_instrumentacion.md | 4. Registro
#3  0.3418  manual_transmisor_PT201.md                  | 4. Procedimiento de calibración
#4  0.3146  manual_transmisor_PT201.md                  | 1. Propósito
```

La carga del modelo mostró un warning de Hugging Face por uso no autenticado. No bloqueó la ejecución ni afecta la validación conceptual del experimento.

---

## 6. Resultado de generación

El LLM local (`llama3:latest` vía Ollama) utilizó correctamente evidencia recuperada para responder sobre:

```text
inspección previa
rango 0–10 bar
ZERO
SPAN
puntos 0 / 5 / 10 bar
criterio ±0,05 bar
registro as-left
```

La respuesta demuestra que el flujo completo llegó hasta generación y que el LLM recibió texto original de los chunks recuperados, no embeddings.

### Limitación observada

La última frase generada indicó que no había evidencia para registrar valores `as-found` y observaciones, aunque la propia `FUENTE 2` —sección **4. Registro** del procedimiento de seguridad— sí contiene explícitamente:

```text
activo
fecha
técnico
valores as-found
valores as-left
observaciones
```

Por tanto:

```text
retrieval correcto + evidencia presente
≠
interpretación/generación siempre correcta
```

La inconsistencia se registra como evidencia útil del comportamiento del LLM. **No se abre una nueva fase de tuning**, porque el objetivo del Paso 10 es validar la integración EAM + RAG y ese objetivo quedó demostrado.

---

## 7. Qué quedó verificado

```text
PT-201 / PLANTA1
→ Maximo mock localiza el ASSET
→ DOCLINKS / DOCINFO resuelven 2 documentos asociados
→ solo esos documentos forman el universo RAG del experimento
→ se crean chunks solo dentro de ese alcance
→ MiniLM realiza retrieval semántico
→ Top-k recupera evidencia pertinente
→ el texto original recuperado se envía al LLM
→ Llama 3 genera una respuesta fundamentada en gran medida
```

Conclusión conceptual:

```text
MAXIMO / EAM
→ determina QUÉ documentación corresponde al contexto

RAG
→ determina QUÉ evidencia dentro de esa documentación es relevante

LLM
→ interpreta y redacta la respuesta
```

---

## 8. Qué NO estamos diciendo todavía

Este Paso 10 no valida aún:

```text
Maximo real
API REST real
Maximo MCP Server real
seguridad de documentos
filtros de acceso por usuario
índice vectorial productivo con metadata EAM
actualización incremental de documentos
acciones automáticas sobre Maximo
agentes
```

Tampoco convierte el mock en arquitectura oficial de AI-EAM-MAXIMO.

---

## 9. Criterio de cierre

✅ **CUMPLIDO para el objetivo de integración del Paso 10.**

El flujo técnico completo fue observado localmente:

```text
contexto EAM
→ Doclinks
→ documentos asociados
→ retrieval limitado a esos documentos
→ contexto fundamentado
→ LLM
→ respuesta
```

La inconsistencia puntual de generación queda documentada, pero no invalida la verificación del flujo de integración.

---

## 10. Continuidad posterior

El siguiente bloque previsto —incorporar datos estructurados/transaccionales de Maximo junto con RAG— **ya fue ejecutado y verificado en el Paso 11**.

La evolución posterior fue:

```text
Paso 10 → contexto EAM + RAG
Paso 11 → WORKORDER estructurado + RAG documental
```

Por tanto, este documento no mantiene trabajo pendiente. El Paso 10 permanece cerrado.
