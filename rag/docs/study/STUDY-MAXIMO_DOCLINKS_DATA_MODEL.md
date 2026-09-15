# 📘 IBM Maximo Doclinks — modelo de datos para el Learning Lab

> **Tipo:** STUDY  
> **Estado:** 📘 ENTENDIDO — base conceptual para el bloque Maximo simulado + Doclinks + RAG  
> **Actualizado:** 2026-09-15  
>
> **Propósito:** entender cómo IBM Maximo Manage representa los documentos adjuntos y sus vínculos con objetos de negocio para construir una simulación fiel, pero simple, antes de conectarla con el RAG ya validado.

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-15 | Se corrige y amplía la explicación de `DOCLINKS.OWNERID` para `ASSET`: se documentan `ASSETUID` y `ASSETID` y se fija `ASSETUID` como baseline site-specific del LAB, sin asumir que sea la única variante válida en Maximo. |
| 2026-09-14 | Creación inicial a partir de documentación oficial IBM sobre attachments/doclinks, API REST y almacenamiento de documentos. |

---

## 1. Idea principal

En Maximo, un documento adjunto se entiende mejor como dos cosas relacionadas:

```text
DOCINFO
→ información del documento / referencia al archivo o URL

DOCLINKS
→ vínculo entre ese documento y un registro de negocio Maximo
```

Modelo mental:

```text
ASSET / WORKORDER / PM / SR / ...
            ↓
         DOCLINKS
            ↓
          DOCINFO
            ↓
archivo físico / object storage / URL
```

IBM documenta que, al trabajar con attachments, se crean objetos `DOCINFO` y `DOCLINK`; además, un mismo documento puede ser referenciado más de una vez manteniendo un único `DOCINFO` y varios vínculos.

---

## 2. DOCLINKS — el vínculo con el objeto de negocio

`DOCLINKS` identifica qué registro de Maximo es propietario o está asociado al documento.

Los campos conceptualmente más importantes para nuestro laboratorio son:

```text
DOCLINKSID
→ identificador del vínculo

OWNERTABLE
→ objeto Maximo propietario
→ ejemplos: ASSET, WORKORDER, PM, SR

OWNERID
→ identificador interno utilizado para relacionar el documento con el registro propietario

DOCINFOID
→ referencia al documento descrito por DOCINFO

DOCTYPE
→ categoría/tipo documental, por ejemplo Attachments
```

La documentación REST vigente de Maximo Manage expone metadata de attachments que incluye, entre otros, `ownerid`, `ownertable`, `docinfoid`, `docType` y `urlType`.

### Importante: OWNERID no es el número funcional visible

`OWNERID` no debe confundirse con identificadores funcionales como `ASSETNUM` o `WONUM`.

Para `WORKORDER`, por ejemplo, el vínculo puede utilizar el identificador interno `WORKORDERID`.

Para `ASSET` existe un matiz importante: Maximo maneja tanto `ASSETUID` como `ASSETID`, y el comportamiento de Attached Documents puede hacer que `DOCLINKS.OWNERID` se relacione con uno u otro según el contexto/configuración.

Modelo conceptual simplificado:

```text
ASSETNUM
→ identificador funcional visible

ASSETUID
→ identificador único utilizado en relaciones site-specific

ASSETID
→ identificador de activo utilizado en comportamiento system-level
```

Por tanto, no debemos enseñar esta regla como universal:

```text
DOCLINKS.OWNERID = ASSETUID siempre   ❌
```

La regla correcta para nuestro nivel de aprendizaje es:

```text
DOCLINKS.OWNERID
→ identificador interno esperado por la relación de Doclinks del objeto

Para ASSET puede implicar:
→ ASSETUID en relaciones site-specific
→ ASSETID en comportamiento/configuración system-level
```

IBM documenta comportamiento específico de Asset Doclinks asociado a la configuración `SYSTEMLEVASSETDOCS`, por lo que ambas variantes deben conocerse aunque el LAB utilice solo una como baseline.

### Baseline elegida para este LAB

Para mantener una primera práctica simple y reproducible utilizaremos:

```text
ASSETUID = 1001
ASSETID  = 2001

DOCLINKS.OWNERTABLE = ASSET
DOCLINKS.OWNERID    = 1001

Baseline:
OWNERID ↔ ASSETUID
```

Esto representa deliberadamente una resolución **site-specific**. `ASSETID` también se conserva en el mock para que el modelo de datos no oculte la otra posibilidad real.

---

## 3. DOCINFO — información del documento

`DOCINFO` conserva la información que describe y localiza el documento.

Para nuestro objetivo son especialmente útiles estos conceptos/campos:

```text
DOCINFOID
→ identificador interno del documento

DOCUMENT
→ nombre/identificador documental

DESCRIPTION
→ descripción

DOCTYPE
→ tipo/categoría documental

URLTYPE
→ tipo de referencia, normalmente FILE o URL

URLNAME
→ ruta, nombre o referencia utilizada para localizar el documento
```

La documentación IBM también utiliza `DOCUMENTDATA` cuando el contenido del archivo viaja codificado, por ejemplo mediante API/importación.

---

## 4. FILE no significa necesariamente filesystem local

El modelo lógico del documento está separado de su almacenamiento físico.

Un attachment puede terminar almacenado, según arquitectura/configuración, en:

```text
Persistent Volume / filesystem
S3 / Cloud Object Storage
URL externa
```

En Maximo Application Suite, IBM documenta tanto almacenamiento persistente como almacenamiento S3 para attached documents.

Por tanto, para RAG conviene separar:

```text
METADATA MAXIMO
→ qué documento corresponde al activo/OT

STORAGE / CONTENT ACCESS
→ dónde y cómo obtenemos el contenido real
```

---

## 5. La API REST confirma el modelo

IBM Maximo Manage permite acceder a attachments de un recurso mediante un subrecurso `doclinks`.

Ejemplo conceptual basado en la documentación IBM:

```text
GET /oslc/os/mxapiasset/{id}
      ↓
"doclinks": {
  "href": "/oslc/os/mxapiasset/{id}/doclinks"
}
```

Después:

```text
GET /oslc/os/mxapiasset/{id}/doclinks
```

retorna referencias y metadata del attachment, incluyendo valores como:

```text
ownerid
ownertable
docinfoid
docType
urlType
fileName
description
```

Y el contenido puede recuperarse mediante la URL del propio attachment.

Esto es especialmente relevante para una futura integración real porque evita depender de acceso directo a las tablas físicas.

---

## 6. Un documento puede estar vinculado más de una vez

La separación `DOCINFO` / `DOCLINKS` permite conceptualmente:

```text
                 DOCINFO #57
              manual_PT201.pdf
                 /       \
                /         \
       DOCLINKS #75      DOCLINKS #91
          ↓                  ↓
       ASSET PT-201       otra entidad
```

Es decir:

```text
1 documento
→ 1 DOCINFO
→ varios DOCLINKS posibles
```

Esto es importante para no duplicar innecesariamente contenido en nuestra futura simulación.

---

## 7. Modelo mínimo que utilizaremos en la simulación

Para el Learning Lab no necesitamos reproducir toda la complejidad de Maximo.

Baseline propuesta:

```text
ASSET_MOCK
- assetuid
- assetid
- assetnum
- siteid
- description

DOCINFO_MOCK
- docinfoid
- document
- description
- doctype
- urltype
- urlname

DOCLINKS_MOCK
- doclinksid
- ownertable
- ownerid
- docinfoid
- doctype
```

Ejemplo:

```text
ASSET
assetuid    = 1001
assetid     = 2001
assetnum    = PT-201
siteid      = PLANTA1

DOCLINKS
doclinksid  = 5001
ownertable  = ASSET
ownerid     = 1001      ← baseline del LAB: ASSETUID
docinfoid   = 9001

DOCINFO
docinfoid   = 9001
document    = MANUAL-PT201
description = Manual transmisor PT-201
doctype     = Attachments
urltype     = FILE
urlname     = rag/data/source_documents/manual_transmisor_PT201.md
```

Este modelo es una **simulación pedagógica**, no una copia completa del esquema de Maximo.

---

## 8. Cómo entra RAG

La conexión que queremos probar es:

```text
Usuario pregunta por PT-201
        ↓
contexto Maximo simulado
        ↓
ASSETNUM / SITEID
        ↓
ASSET
        ↓
identificador interno definido por la relación de Doclinks
        ↓
DOCLINKS
        ↓
DOCINFO
        ↓
URLNAME / referencia al contenido
        ↓
RAG
        ↓
chunks / embeddings / retrieval
        ↓
LLM
        ↓
respuesta fundamentada
```

Idea central:

> **Maximo identifica qué documento está asociado al contexto EAM; RAG recupera el conocimiento dentro de ese documento.**

---

## 9. Qué NO vamos a simular todavía

Para mantener el aprendizaje controlado, inicialmente no modelaremos:

```text
cambio dinámico entre ASSETUID y ASSETID
seguridad real de attachments
S3/COS real
PVC/OpenShift
versionado documental completo
permisos por usuario/grupo
relationships complejas heredadas
propagación de doclinks entre objetos relacionados
API real de Maximo
```

La distinción `ASSETUID` / `ASSETID` queda documentada, pero el Paso 09 usa una sola baseline: `ASSETUID`.

---

## 10. Fuentes IBM revisadas

Fuentes principales utilizadas para esta nota:

- IBM Maximo Manage REST API Guide — Handling attachments  
  https://www.ibm.com/docs/en/masv-and-l/maximo-manage/cd?topic=apis-handling-attachments

- IBM Maximo Manage — Attached document properties  
  https://www.ibm.com/docs/en/masv-and-l/maximo-manage/cd?topic=properties-attached-document

- IBM Maximo Manage — Configuring system properties for persistent storage  
  https://www.ibm.com/docs/en/masv-and-l/maximo-manage/cd?topic=storage-configuring-system-properties-persistent

- IBM Maximo Manage — S3 attachments  
  https://www.ibm.com/docs/en/masv-and-l/maximo-manage/cd?topic=properties-attachment-s3

- IBM Support — How to import attachments into Maximo using MIF  
  https://www.ibm.com/support/pages/how-import-attachments-maximo-using-mif

- IBM Support — consultas/relaciones de Doclinks para Asset usando `ASSETID` / `OWNERID`  
  https://www.ibm.com/support/pages/node/1112727

- IBM Support — comportamiento system-level de Asset attached documents (`SYSTEMLEVASSETDOCS`)  
  https://www.ibm.com/support/pages/node/4820487

---

## 11. Próximo paso

Ejecutar y verificar la simulación mínima de:

```text
ASSET
+
DOCLINKS
+
DOCINFO
```

con la baseline explícita:

```text
DOCLINKS.OWNERID ↔ ASSET.ASSETUID
```

y después conectar esa resolución documental con el pipeline RAG ya existente.
