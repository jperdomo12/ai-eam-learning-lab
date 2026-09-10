# 🔌 MCP + IBM Maximo — Documentación viva del laboratorio

> 🎯 **Propósito:** ser la fuente viva y canónica del Learning Lab para todo lo aprendido, construido, configurado y comprobado sobre MCP aplicado al contexto EAM / IBM Maximo.
>
> 📍 **Estado:** ✅ CERRADO para el alcance actual de aprendizaje MCP.
> 🗓️ **Actualizado:** 2026-09-10

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-10 | Creación de la documentación viva canónica utilizando el corpus histórico completo: trabajo previo en Gemini/Claude, HandOffs, bitácoras, guías, ZIP original del laboratorio, código `maximo_mcp.py`, configuración real de Claude Desktop y revisión realizada en ChatGPT. |

---

# 1. Alcance de esta documentación

Este documento **no comienza en ChatGPT ni describe solo lo realizado desde el traslado del proyecto**.

La historia completa del laboratorio comienza con el trabajo previo realizado con **Gemini / Claude Desktop / VS Code + Cline** y continúa con su recuperación, auditoría, consolidación y documentación dentro de `ai-eam-learning-lab`.

Por tanto, la documentación viva se construye a partir de **todo el conocimiento y evidencia disponibles**, incluyendo:

- documentos y HandOffs generados durante el trabajo previo con Gemini;
- bitácoras y guías históricas del laboratorio;
- notas locales de las sesiones realizadas;
- ZIP `MCP-Claude.zip` con artefactos originales;
- código histórico `maximo_mcp.py`;
- versiones anteriores del script conservadas en el ZIP;
- archivo real `claude_desktop_config.json` aportado posteriormente;
- evidencia obtenida durante la revisión en ChatGPT;
- correcciones conceptuales y técnicas introducidas al consolidar el material;
- decisiones y aclaraciones posteriores del usuario.

El objetivo es que **el repositorio contenga la versión consolidada y actualizada de TODO el trabajo MCP realizado**, independientemente de qué herramienta o chat produjo originalmente cada parte.

---

# 2. Modelo de fuentes y verdad

Los documentos de Gemini, Claude y otros materiales previos son **fuentes de referencia e insumos para reconstrucción**. No se consideran automáticamente documentación vigente.

La relación correcta es:

```text
TRABAJO PREVIO
Gemini / Claude / Cline / archivos locales / bitácoras
                    ↓
             FUENTES + EVIDENCIA
                    ↓
         revisar / contrastar / corregir
                    ↓
      DOCUMENTACIÓN VIVA DEL LEARNING LAB
                    ↓
      verdad consolidada del aprendizaje MCP
```

Cuando existen discrepancias:

1. prevalece la evidencia primaria verificable;
2. después, la documentación viva consolidada;
3. finalmente, las narrativas históricas como contexto.

Las contradicciones no se ocultan: se documentan y, cuando existe evidencia suficiente, se resuelven.

---

# 3. Objetivo original del laboratorio

El laboratorio nació para explorar si una aplicación de IA podía interactuar con IBM Maximo mediante lenguaje natural utilizando MCP.

La pregunta principal fue:

> **¿Puede una aplicación de IA recibir una petición en lenguaje natural, descubrir una capacidad externa y ejecutar una operación EAM / IBM Maximo a través de MCP?**

El objetivo no era construir todavía una integración productiva, sino aprender el mecanismo haciendo una PoC real.

Modelo mental:

```text
Usuario
   ↓ lenguaje natural
Aplicación de IA / MCP Host
   ↓
MCP Client
   ↓ protocolo MCP
MCP Server
   ↓ Tool
Lógica Python
   ↓
Datos simulados
   o
OSLC / REST previsto → IBM Maximo
```

---

# 4. Evolución completa del laboratorio

## 4.1 Exploración inicial con Gemini / Google Cloud

La primera aproximación se estudió alrededor de Gemini y servicios Google Cloud / Vertex AI.

Para una PoC inicial, esta vía introducía demasiada infraestructura antes de validar el concepto: servicios cloud, endpoints, certificados, conectividad y configuración adicional.

### Decisión

Simplificar el laboratorio y pasar a un modelo local.

## 4.2 Claude Desktop + MCP local

Claude Desktop se utilizó como aplicación de IA para ejecutar un servidor MCP local escrito en Python.

Arquitectura:

```text
Claude Desktop
      ↓ MCP / stdio
Python + FastMCP
      ↓
maximo_mcp.py
```

Esta etapa permitió demostrar el mecanismo fundamental: Claude podía descubrir e invocar una Tool expuesta por el servidor MCP local.

## 4.3 Evolución a VS Code + Cline

Posteriormente el centro de trabajo se trasladó a VS Code + Cline para reducir el ciclo manual de edición/prueba.

Flujo:

```text
pedir cambio
   ↓
IA analiza / modifica código
   ↓
usuario revisa
   ↓
se refresca / reinicia MCP
   ↓
se prueba
```

## 4.4 Entorno multi-MCP

El laboratorio evolucionó hacia tres servidores configurados simultáneamente:

```text
VS Code + Cline / Claude Desktop
   ├─ Maximo MCP
   ├─ Filesystem MCP
   └─ GitHub MCP
```

A esta combinación se la llamó informalmente **“Tridente MCP”**. El término pertenece al laboratorio y no al estándar MCP.

---

# 5. Cronología consolidada

Las fuentes históricas contienen una discrepancia de fechas que se conserva explícitamente.

| Fecha / periodo | Hito |
|---|---|
| Exploración inicial | Estudio Gemini / Google Cloud y decisión de simplificar hacia MCP local. |
| 20-04-2025 o 20-04-2026 según la fuente | Primera etapa Claude Desktop + MCP local, lógica dual y primeras Tools. |
| 21-04-2026 según notas locales | Configuración de Cline y réplica de servidores MCP en VS Code. |
| 09-09-2026 según bitácora v2.0 | Expansión documentada de 4 a 14 Tools y entorno multi-MCP. |
| 10-09-2026 | Traslado y consolidación en `ai-eam-learning-lab`. |

No se fuerza una fecha única cuando las fuentes no permiten resolverla con suficiente evidencia.

---

# 6. Entorno utilizado

| Componente | Uso histórico |
|---|---|
| Windows | Sistema operativo local |
| Visual Studio Code | IDE |
| Extensión Python | Soporte de desarrollo |
| Python | Runtime del servidor MCP |
| Claude Desktop | Primer MCP Host práctico utilizado |
| Cline | Entorno posterior dentro de VS Code |
| MCP Python SDK / FastMCP | Implementación del servidor MCP |
| `requests` | Llamadas HTTP previstas a Maximo |
| `urllib3` | Gestión de warnings SSL en la PoC |
| Node.js / `npx` | Ejecución de servidores MCP adicionales |
| Filesystem MCP | Acceso controlado a archivos locales |
| GitHub MCP | Investigación y acceso a repositorios |
| IBM Maximo | Sistema objetivo; conexión viva no validada |

Sobre Python, las fuentes no son totalmente homogéneas: algunas hablan de `3.10+` y otras registran `3.14`. La documentación viva conserva esa discrepancia sin convertirla en requisito del laboratorio.

---

# 7. Instalación y preparación

La secuencia reconstruida fue:

```text
1. Instalar VS Code
2. Instalar soporte Python
3. Instalar Python
4. Corregir PATH de Windows cuando Python/PIP no eran reconocidos
5. Instalar dependencias Python
6. Instalar Claude Desktop
7. Crear/configurar maximo_mcp.py
8. Configurar claude_desktop_config.json
9. Probar el servidor MCP
10. Incorporar Node.js/npx
11. Instalar Cline
12. Configurar servidores MCP en Cline
```

Dependencias documentadas:

```bash
pip install mcp requests urllib3
```

El código recuperado utiliza:

```python
from mcp.server.fastmcp import FastMCP
```

### Incidencia: PATH

Windows no reconocía inicialmente `python` o `pip` desde terminal.

Se corrigieron Variables de Entorno / PATH hasta lograr una validación como:

```bash
python --version
```

---

# 8. Servidor `maximo_mcp.py`

El ZIP histórico contiene el servidor utilizado en el laboratorio.

Elementos confirmados directamente:

```python
import requests
import urllib3
from mcp.server.fastmcp import FastMCP

MODO_SIMULACION = True
MAXIMO_URL = "https://TU_SERVIDOR/maximo"
API_KEY = "TU_API_KEY_AQUÍ"

mcp = FastMCP("Maximo Enterprise")
```

Las capacidades se exponían mediante:

```python
@mcp.tool()
```

El archivo contiene:

- mocks de OTs, inventario, activos, workflow y Object Structures;
- lógica de transición de estados;
- rama preparada para OSLC/REST;
- Working Set temporal en memoria;
- 14 Tools MCP.

---

# 9. Modo simulación y modo real

## 9.1 Simulación

```python
MODO_SIMULACION = True
```

Fue el modo realmente utilizado para las pruebas.

Permitió probar:

- consultas de OTs;
- inventario;
- activos;
- cambios de estado simulados;
- creación simulada de OTs;
- workflow simulado;
- Working Set;
- selección e invocación de Tools desde lenguaje natural.

## 9.2 Rama real prevista

```python
MODO_SIMULACION = False
```

El código contiene lógica para llamar a Maximo mediante HTTP/OSLC, pero esa rama **no fue validada contra un IBM Maximo vivo**.

También aparecen `verify=False` y supresión de warnings SSL, decisiones de laboratorio que no deben trasladarse a producción.

---

# 10. Configuración real de Claude Desktop

El usuario aportó una copia real de `claude_desktop_config.json` obtenida desde:

```text
Claude Desktop
→ Configuración
→ Desarrollador
→ Editar configuración
```

La ruta local correspondía a una instalación Windows Store bajo:

```text
%LOCALAPPDATA%\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\
```

La configuración real confirma tres servidores MCP:

```json
{
  "mcpServers": {
    "maximo": {
      "command": "C:/RUTA/PYTHON/python.exe",
      "args": ["-u", "C:/RUTA/MCP-Claude/maximo_mcp.py"]
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:/RUTA/MCP-Claude",
        "C:/RUTA/Downloads"
      ]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "<SECRET>"
      }
    }
  }
}
```

Esto confirma directamente:

- uso de una ruta concreta a `python.exe`;
- parámetro `-u`;
- dos directorios autorizados para Filesystem MCP;
- GitHub MCP ejecutado con `npx`;
- autenticación mediante variable de entorno.

El repositorio conserva solo una versión sanitizada del archivo.

---

# 11. Cómo se obtenía la configuración de Claude

La forma práctica utilizada fue:

```text
Claude Desktop
→ Configuración
→ Desarrollador
→ Editar configuración
```

Esto permitía localizar el archivo efectivo utilizado por la instalación de Claude Desktop, evitando editar por error otra ruta de configuración.

---

# 12. Primera prueba de extremo a extremo

La Tool inicial fue:

```text
verificar_conexion
```

Secuencia:

```text
Usuario
  ↓
Claude Desktop
  ↓ descubre Tool
MCP Client
  ↓
MCP Server Python
  ↓
verificar_conexion()
  ↓
respuesta
  ↓
Claude Desktop
```

✅ **PROBADO:** Claude Desktop ejecutó una Tool del servidor MCP local.

Este fue el hito central de la PoC.

---

# 13. Pruebas funcionales realizadas

Las notas locales del ZIP registran, en modo simulación:

- consultas de varias OTs;
- consulta del artículo `SKF-6204` en almacén `CENTRAL`;
- cambio simulado de una OT de `INPRG` a `WMATL` con memo;
- cambio simulado de una OT de `APPR` a `INPRG` con memo;
- uso de Filesystem MCP para listar archivos;
- uso de Filesystem MCP para escribir un archivo.

Las fuentes dejan explícito que las operaciones relacionadas con Maximo se realizaron con:

```python
MODO_SIMULACION = True
```

Por tanto, cuando una nota histórica habla de “conexión exitosa con el servidor de Maximo”, debe interpretarse como **servidor MCP local orientado a Maximo**, no como conexión a IBM Maximo real.

---

# 14. Evolución de 4 a 14 Tools

La documentación histórica registra una evolución de un conjunto reducido de Tools hasta un catálogo de 14.

Parte de la ampliación se produjo después de utilizar GitHub MCP para investigar otras implementaciones y comparar capacidades.

Una consulta histórica aproximada fue:

```text
Busca en GitHub otros servidores MCP de Maximo para ver si alguien ha programado funciones que nosotros no tenemos
```

Esto permitió identificar ideas reutilizables y ampliar el script local.

---

# 15. Catálogo final de 14 Tools verificado

El código recuperado en `MCP-Claude.zip` confirma exactamente estas Tools:

| # | Tool | Propósito |
|---:|---|---|
| 1 | `consultar_ot` | Consultar una Orden de Trabajo |
| 2 | `consultar_inventario` | Consultar inventario |
| 3 | `listar_transiciones_ot` | Mostrar transiciones permitidas |
| 4 | `cambiar_estado_ot` | Cambiar estado de una OT |
| 5 | `query_maximo` | Consulta genérica sobre Object Structures |
| 6 | `consultar_activo` | Consultar un activo |
| 7 | `listar_object_structures` | Listar Object Structures |
| 8 | `crear_ot` | Crear una OT |
| 9 | `ws_editar_ot` | Preparar cambios en Working Set |
| 10 | `ws_confirmar_cambios` | Confirmar cambios |
| 11 | `ws_cancelar_cambios` | Cancelar cambios |
| 12 | `obtener_workflow_assignments` | Consultar asignaciones de workflow |
| 13 | `enviar_workflow_response` | Responder workflow |
| 14 | `verificar_conexion` | Verificar servidor/capacidades |

✅ **VERIFICADO EN CÓDIGO:** existen 14 funciones decoradas con `@mcp.tool()`.

---

# 16. Working Set y Human-in-the-Loop

El script incluyó un patrón experimental de confirmación:

```text
ws_editar_ot
   ↓
preview / Working Set
   ↓
confirmar o cancelar
```

El Working Set era memoria temporal dentro del proceso Python, no una funcionalidad nativa de IBM Maximo.

El aprendizaje importante fue:

```text
proponer → revisar → confirmar
```

Este patrón es especialmente relevante para futuras acciones EAM con impacto real.

---

# 17. Cline y el entorno multi-MCP

El laboratorio evolucionó a VS Code + Cline para disminuir fricción operativa.

Se configuraron:

- Maximo MCP;
- Filesystem MCP;
- GitHub MCP.

La documentación histórica describe la configuración de Cline en `cline_mcp_settings.json` y un ciclo de trabajo más corto que con Claude Desktop.

Ese archivo real de Cline no ha sido aportado directamente todavía, por lo que permanece clasificado como **REFERENCIA HISTÓRICA**, no como evidencia primaria recuperada.

---

# 18. Problemas y soluciones

## Python/PIP no reconocidos

**Problema:** PATH de Windows.

**Solución:** corrección de Variables de Entorno.

## Archivo de configuración Claude equivocado

**Problema:** edición inicial de una ubicación que no correspondía a la instalación efectiva.

**Solución:** usar `Configuración → Desarrollador → Editar configuración`.

## No disponer de Maximo real

**Problema:** imposibilidad de probar la integración objetivo.

**Solución:** `MODO_SIMULACION` + mocks.

## Ciclo lento en Claude Desktop

**Problema:** necesidad de reiniciar completamente para recargar cambios.

**Evolución:** uso posterior de VS Code + Cline.

---

# 19. Qué quedó probado

## 🧪 PROBADO

- servidor MCP local en Python/FastMCP;
- Tool ejecutada desde Claude Desktop;
- consultas EAM simuladas;
- cambios de estado simulados;
- Filesystem MCP para listar/escribir archivos;
- evolución a entorno multi-MCP;
- trabajo posterior con Cline.

## ✅ VERIFICADO MEDIANTE EVIDENCIA PRIMARIA

- contenido del `maximo_mcp.py` recuperado;
- 14 Tools;
- modo simulación;
- mocks EAM;
- Working Set;
- lógica OSLC/REST prevista;
- configuración real de Claude Desktop con Maximo + Filesystem + GitHub MCP.

## 📎 REFERENCIA HISTÓRICA

- narrativas de Gemini;
- bitácoras antiguas;
- HandOffs previos;
- configuración de Cline no recuperada directamente.

## ❌ NO VALIDADO

- conexión viva con IBM Maximo;
- lectura real contra Maximo;
- escritura real contra Maximo;
- workflow real;
- seguridad productiva;
- beneficio cuantificado del 30 %;
- RAG.

---

# 20. Conceptos MCP consolidados

## Host

Aplicación/entorno de IA que coordina conexiones MCP. No es el PC físico.

## Client

Componente que mantiene la conexión/protocolo con un MCP Server.

## Server

Proceso que expone capacidades MCP.

## Tool

Capacidad invocable.

## MCP no es solo Tools

También contempla Resources y Prompts.

## MCP no crea autonomía por sí mismo

MCP estandariza acceso a capacidades; la lógica del Host/agente decide cuándo y cómo utilizarlas.

---

# 21. Aprendizajes para EAM / IBM Maximo

📘 **Simular primero funciona.** Permite aprender el patrón de integración sin depender de infraestructura real.

📘 **Las Tools pueden expresar semántica EAM.** Consultar OT, inventario, activos o workflow es más útil que exponer únicamente HTTP genérico.

📘 **MCP y OSLC/REST son complementarios.** MCP puede ser la frontera de consumo de la IA mientras OSLC/REST ejecuta la integración subyacente.

📘 **Las acciones requieren control humano.** El Working Set anticipó un patrón útil de preview + confirmación.

📘 **Varios servidores especializados pueden convivir.** Maximo, filesystem y GitHub demostraron dominios de capacidad distintos bajo el mismo entorno.

---

# 22. Aspectos que no deben copiarse directamente a producción

La PoC contiene simplificaciones propias de laboratorio:

- `verify=False`;
- warnings SSL deshabilitados;
- credencial modelada de forma simple;
- Working Set solo en memoria;
- reglas de transición codificadas localmente;
- respuestas mayoritariamente como strings;
- Tool genérica `query_maximo` demasiado amplia para un entorno productivo;
- falta de autorización robusta;
- falta de observabilidad/auditoría productiva.

---

# 23. Relación con AI-EAM-MAXIMO

```text
AI-EAM Learning Lab
       ↓
aprender / experimentar
       ↓
🟨 CANDIDATO A INCORPORAR
       ↓ decisión explícita
AI-EAM-MAXIMO
```

Nada de este laboratorio se convierte automáticamente en arquitectura o implementación del producto.

---

# 24. Qué se conserva de las fuentes históricas

Las fuentes previas siguen siendo importantes para trazabilidad y contexto, pero el lector futuro no debe necesitar reconstruirlas manualmente.

Su función es:

- justificar cómo se llegó a determinadas conclusiones;
- preservar detalles históricos;
- permitir volver a la evidencia cuando aparezca una duda;
- detectar contradicciones o cambios de criterio.

La **explicación vigente y consolidada** es este documento.

---

# 25. Resultado final

El laboratorio MCP queda cerrado para su alcance actual porque se alcanzó:

```text
ENTENDER MCP
+
CONSTRUIR UN MCP SERVER
+
EJECUTAR TOOLS DESDE IA
+
SIMULAR CAPACIDADES EAM / MAXIMO
+
EXPLORAR MULTI-MCP
+
RECUPERAR EVIDENCIA PRIMARIA
+
DOCUMENTAR TODO EL CICLO DE FORMA VIVA
```

➡️ El siguiente laboratorio independiente será **RAG (Retrieval-Augmented Generation)**.
