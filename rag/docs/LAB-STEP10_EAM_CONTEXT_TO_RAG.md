# 🧪 Paso 10 — Contexto EAM → Doclinks → RAG → LLM

> 🎯 **Objetivo:** integrar por primera vez el contexto EAM simulado con el RAG ya validado, de modo que Maximo determine qué documentos son aplicables y RAG recupere conocimiento únicamente dentro de esos documentos.
>
> 📍 **Estado:** 🧪 **PREPARADO — pendiente de ejecución local y validación pedagógica**
>
> 🗓️ **Actualizado:** 2026-09-16

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-16 | Creación inicial del Paso 10, conectando la resolución `ASSET → DOCLINKS → DOCINFO` del Paso 09 con retrieval semántico y generación local. |

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

## 5. Ejecución

Desde la raíz del repositorio:

```bash
python rag/src/step10_eam_context_to_rag.py
```

También puede indicarse explícitamente el activo y site:

```bash
python rag/src/step10_eam_context_to_rag.py PT-201 PLANTA1
```

Y opcionalmente otra pregunta:

```bash
python rag/src/step10_eam_context_to_rag.py PT-201 PLANTA1 --query "¿Qué debo revisar antes de calibrar este activo?"
```

---

## 6. Qué debe observarse

La salida está dividida conceptualmente en cuatro partes:

```text
1. documentos resueltos por Maximo mock
2. alcance RAG determinado por el contexto EAM
3. retrieval semántico dentro de ese alcance
4. generación fundamentada
```

La prueba será satisfactoria si se observa que:

```text
PT-201 / PLANTA1
→ resuelve sus documentos por Doclinks
→ solo esos documentos producen chunks candidatos
→ MiniLM recupera los chunks relevantes
→ Llama 3 responde usando el texto recuperado
```

---

## 7. Qué NO estamos diciendo todavía

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

## 8. Criterio de cierre

El Paso 10 quedará ✅ **VERIFICADO** cuando una ejecución local confirme el flujo completo:

```text
contexto EAM
→ Doclinks
→ documentos asociados
→ retrieval limitado a esos documentos
→ contexto fundamentado
→ LLM
→ respuesta coherente y respaldada
```

---

## 9. Siguiente paso previsto

Una vez verificada esta integración, el siguiente bloque natural será incorporar además datos estructurados/transaccionales simulados de Maximo, por ejemplo OTs abiertas del activo:

```text
Maximo / MCP
→ datos operativos

RAG
→ conocimiento documental

LLM
→ combina ambos
```

Ejemplo objetivo futuro:

```text
“La bomba B-201 presenta alta temperatura.
¿Tiene OTs abiertas y qué indica su manual?”
```
