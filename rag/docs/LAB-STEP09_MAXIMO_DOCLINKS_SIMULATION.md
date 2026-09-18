# 🧪 Paso 09 — Simulación Maximo: ASSET + DOCLINKS + DOCINFO

> 🎯 **Objetivo:** comprobar de forma visible cómo un contexto EAM mínimo puede resolver qué documentos están asociados a un activo antes de entregar esos documentos al pipeline RAG.
>
> 📍 **Estado:** ✅ **VERIFICADO — resolución documental Maximo simulada validada localmente**
>
> 🗓️ **Actualizado:** 2026-09-15

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-18 | Auditoría final: se añade Resumen de contenido y se actualiza el antiguo “siguiente paso” como continuidad histórica ya completada en el Paso 10. |
| 2026-09-15 | ✅ Ejecución local verificada: `PT-201 / PLANTA1` resuelve `ASSETUID=1001`, `ASSETID=2001`, dos `DOCLINKS`, dos `DOCINFO` y ambos archivos asociados existen. |
| 2026-09-15 | Se explicita la coexistencia de `ASSETUID` y `ASSETID`; el LAB conserva ambos y usa `ASSETUID` como baseline site-specific para resolver `DOCLINKS.OWNERID`. |
| 2026-09-15 | Se crea el Paso 09 con datos Maximo simulados y un script de resolución `ASSET → DOCLINKS → DOCINFO → archivo`. |

---

## 🧭 Resumen de contenido

| Punto | Contenido |
|---|---|
| **1. Objetivo** | Comprender cómo Maximo asocia un activo con sus documentos antes de introducir RAG. |
| **2. Datos simulados** | Define ASSET, DOCLINKS y DOCINFO usados en la prueba. |
| **3. Script** | Identifica el programa que resuelve la cadena documental simulada. |
| **4. Prueba principal** | Verifica PT-201/PLANTA1 → ASSET → DOCLINKS → DOCINFO → archivos. |
| **5. Simplificaciones** | Enumera aspectos reales de Maximo deliberadamente fuera del mock. |
| **6. Cierre** | Confirma que Doclinks limita qué documentación corresponde al contexto EAM. |
| **7. Continuidad posterior** | Registra que el paso RAG previsto se ejecutó posteriormente en el Paso 10. |

---

## 1. Qué queremos aprender

Hasta el Paso 08, RAG conocía una carpeta de documentos y realizaba retrieval sobre ella.

Ahora añadimos una capa EAM previa:

```text
Usuario / contexto EAM
        ↓
ASSETNUM + SITEID
        ↓
ASSET simulado
        ↓
identificador interno usado por Doclinks
        ↓
DOCLINKS
        ↓
DOCINFO
        ↓
archivo asociado
        ↓
RAG   ← siguiente paso
```

La idea clave es:

> **Maximo determina qué documentación corresponde al activo; RAG buscará después el conocimiento dentro de esa documentación.**

Para `ASSET`, Maximo maneja tanto `ASSETUID` como `ASSETID`. En este LAB utilizamos deliberadamente `ASSETUID` como baseline site-specific, sin presentarlo como una regla universal.

---

## 2. Datos simulados

Se utilizan tres archivos deliberadamente simples:

```text
rag/data/maximo_mock/
├── assets.json
├── doclinks.json
└── docinfo.json
```

### ASSET

Activo inicial:

```text
assetuid    = 1001
assetid     = 2001
assetnum    = PT-201
siteid      = PLANTA1
description = Transmisor de presión PT-201
```

Interpretación:

```text
ASSETNUM
→ identificador funcional visible

ASSETUID
→ identificador interno usado por nuestra baseline site-specific

ASSETID
→ identificador real de Maximo que también puede participar en Doclinks
  cuando aplica comportamiento/configuración system-level
```

### DOCLINKS

El activo tiene dos vínculos documentales:

```text
DOCLINKSID 5001 → DOCINFOID 9001
DOCLINKSID 5002 → DOCINFOID 9002
```

con:

```text
OWNERTABLE = ASSET
OWNERID    = 1001
```

En esta prueba:

```text
DOCLINKS.OWNERID = ASSET.ASSETUID
```

Esto es una **elección explícita del LAB**, no la afirmación de que Maximo utilice siempre `ASSETUID` para Asset Doclinks.

### DOCINFO

Los dos documentos apuntan a archivos que ya existían en el RAG LAB:

```text
MANUAL-PT201
→ rag/data/source_documents/manual_transmisor_PT201.md

PROC-SEG-INSTR
→ rag/data/source_documents/procedimiento_seguridad_instrumentacion.md
```

No se duplican documentos; la simulación solo añade metadata EAM que permite encontrarlos.

---

## 3. Script

```text
rag/src/step09_resolve_maximo_doclinks.py
```

El script define de forma visible:

```text
ASSET_DOCLINK_OWNER_KEY = "assetuid"
```

Y realiza exclusivamente esta resolución:

```text
assetnum + siteid
→ localizar ASSET
→ leer ASSETUID y ASSETID
→ usar ASSETUID como OWNER KEY de la baseline
→ buscar DOCLINKS con OWNERTABLE=ASSET y OWNERID=ASSETUID
→ resolver DOCINFOID
→ obtener URLTYPE / URLNAME
→ comprobar que el archivo existe
```

Todavía **no ejecuta embeddings, retrieval ni LLM**. La separación es intencional para ver con claridad la función de la capa Maximo.

---

## 4. Prueba principal

Desde la raíz del repositorio:

```bash
python rag/src/step09_resolve_maximo_doclinks.py
```

Los valores por defecto son:

```text
ASSETNUM = PT-201
SITEID   = PLANTA1
```

También puede ejecutarse explícitamente:

```bash
python rag/src/step09_resolve_maximo_doclinks.py PT-201 PLANTA1
```

### Resultado verificado

La ejecución local del 2026-09-15 confirmó:

```text
ASSETNUM : PT-201
SITEID   : PLANTA1
ASSETUID : 1001
ASSETID  : 2001
OWNER KEY: ASSETUID (baseline site-specific)
OWNERID  : 1001

Documentos asociados: 2

DOCLINKSID 5001 → DOCINFOID 9001 → MANUAL-PT201    → EXISTE: sí
DOCLINKSID 5002 → DOCINFOID 9002 → PROC-SEG-INSTR → EXISTE: sí
```

El objetivo no es memorizar el output, sino observar el JOIN conceptual elegido para esta baseline:

```text
ASSET.assetuid
        ↓
DOCLINKS.ownerid
DOCLINKS.docinfoid
        ↓
DOCINFO.docinfoid
        ↓
DOCINFO.urlname
```

Y recordar que, en Maximo real, la relación de Asset Doclinks puede involucrar `ASSETID` según el comportamiento/configuración aplicable.

---

## 5. Qué estamos simplificando

Esta prueba no pretende reproducir toda la implementación real de Maximo.

No incluye todavía:

```text
cambio dinámico ASSETUID ↔ ASSETID
API REST real
MCP real
S3 / object storage
seguridad y permisos
propagación/herencia de doclinks
otros objetos propietarios
URLs externas
versionado documental
```

La estructura se mantiene mínima para comprender la relación antes de añadir otra capa.

---

## 6. Criterio de cierre del Paso 09

✅ **Cumplido.** La ejecución local confirmó que:

```text
PT-201 / PLANTA1
→ se resuelve al ASSET simulado
→ se muestran ASSETUID 1001 y ASSETID 2001
→ la baseline usa ASSETUID 1001 como OWNERID
→ se encuentran sus DOCLINKS
→ se resuelven sus DOCINFO
→ se localizan los dos archivos existentes
```

Aprendizaje consolidado:

> **Doclinks actúa como la capa de asociación EAM que limita qué documentación corresponde al contexto del activo; RAG todavía no ha intervenido.**

---

## 7. Continuidad posterior

El flujo que figuraba como siguiente paso:

```text
ASSET + DOCLINKS + DOCINFO
→ documentos permitidos por contexto EAM
→ RAG
→ LLM
```

**ya fue ejecutado y verificado posteriormente en el Paso 10**.

Por tanto, no existe un pendiente asociado a este documento. El Paso 09 permanece cerrado como evidencia de la resolución documental previa al RAG.
