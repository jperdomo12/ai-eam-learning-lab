# ⚡ MCP LAB — Fast Reading

> 🎯 **Objetivo:** recuperar en pocos minutos qué se aprendió, qué se probó y cómo quedó configurado el laboratorio MCP.
>
> 📍 **Estado:** ✅ **MCP LAB CERRADO / CONGELADO** para el alcance actual.
>
> 🗓️ **Actualizado:** 2026-09-12
>
> 📘 **Documento completo:** [`MCP_LAB_DOCUMENTATION.md`](MCP_LAB_DOCUMENTATION.md)

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-12 | Se aclara que la instalación mínima para reproducir **todo** el LAB incluye Claude Desktop y después Cline; se documenta además que Cline puede ejecutarse en varias superficies, pero en este laboratorio se utilizó específicamente como extensión de VS Code porque VS Code ya era el IDE principal y permitía concentrar código, terminal, diff, MCP y pruebas en un mismo entorno. |
| 2026-09-12 | Se reorganiza la lectura para reflejar la secuencia real **Claude Desktop → VS Code + Cline**, se incorpora la configuración resumida de Claude Desktop y se explican explícitamente la razón del cambio y las ventajas prácticas de Cline. |
| 2026-09-12 | Se añade Historial, se aclara Filesystem MCP/sandbox, se incorpora el prompt exacto de la prueba combinada final en Cline y se explica brevemente `verify=False`. |
| 2026-09-12 | Cierre/congelación del MCP LAB tras la revalidación final en VS Code + Cline. |
| 2026-09-10 | Creación del resumen de recuperación rápida del laboratorio MCP. |

## 1. En una frase

Se validó una PoC local donde aplicaciones de IA —primero **Claude Desktop** y después **VS Code + Cline**— utilizaron MCP Servers especializados para ejecutar capacidades EAM simuladas y trabajar con archivos locales.

**No se conectó IBM Maximo real.**

---

## 2. Arquitectura mental

```text
Usuario
  ↓ lenguaje natural
Host / entorno de IA
  ├─ Claude Desktop
  └─ VS Code + Cline
          ↓
       MCP Client
          ↓ stdio
   ┌──────┼───────────┐
   ↓      ↓           ↓
 Maximo  Filesystem  GitHub histórico
  MCP      MCP         MCP
```

El servidor Maximo propio está en:

```text
mcp/src/maximo_mcp.py
```

y permanece en:

```python
MODO_SIMULACION = True
```

---

## 3. Productos principales

| Producto | Papel |
|---|---|
| **VS Code** | IDE utilizado en el LAB |
| **Cline** | agente de desarrollo; en este LAB se utilizó como extensión de VS Code |
| **Claude Desktop** | primer Host usado en la PoC |
| **Python + FastMCP** | servidor Maximo MCP |
| **Node.js / npx** | ejecución de Filesystem MCP y del GitHub MCP histórico |
| **DeepSeek V4 Flash** | modelo seleccionado en la revalidación final de Cline; aparecía como `Free` en ese momento |
| **Filesystem MCP** | lectura/escritura en carpetas explícitamente autorizadas |

Cline **no es el modelo**. Cline usa un modelo seleccionado por el usuario.

Cline tampoco está conceptualmente limitado a VS Code: actualmente dispone de otras superficies/editores, además de CLI/SDK. **Nuestro laboratorio, sin embargo, se realizó con VS Code + Cline.**

---

## 4. Instalación mínima para reproducir TODO el aprendizaje

Si se quiere reproducir la secuencia completa del LAB —incluyendo la primera etapa con Claude Desktop y la posterior evolución a Cline— el orden mental es:

```text
1. Instalar VS Code.
2. Instalar la extensión Python de Microsoft.
3. Instalar Python y verificar PATH.
4. pip install mcp requests urllib3
5. Instalar Node.js para disponer de node/npm/npx.
6. Instalar Claude Desktop.
7. Configurar y probar primero los MCP Servers en Claude Desktop.
8. Instalar Cline como extensión de VS Code.
9. Iniciar sesión en Cline si lo solicita.
10. Seleccionar un modelo vigente en Cline.
11. Configurar en Cline los MCP Servers que se quieran utilizar.
```

Comprobaciones útiles:

```bash
python --version
pip --version
node --version
npm --version
npx --version
```

> Si solo se quisiera reproducir la etapa final de VS Code + Cline, Claude Desktop no sería técnicamente obligatorio. Para **reproducir nuestro laboratorio completo**, sí forma parte del recorrido.

---

## 5. Claude Desktop — configuración y primera etapa

**Claude Desktop fue el primer Host MCP real del laboratorio.** Con él comprobamos que una aplicación de IA podía descubrir e invocar nuestro servidor Maximo local, usar Filesystem MCP y combinar servidores en una misma tarea.

Ruta efectiva utilizada en la instalación Windows Store del LAB:

```text
C:\Users\jpperdomo\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json
```

Acceso usado:

```text
Claude Desktop
→ Settings / Configuración
→ Developer / Desarrollador
→ Edit Configuration / Editar configuración
```

Patrón de configuración observado:

```json
"maximo": {
  "command": "C:/.../python.exe",
  "args": ["-u", "C:/.../maximo_mcp.py"]
}
```

En el mismo `mcpServers` se configuraron históricamente:

```text
maximo      → Python + maximo_mcp.py
filesystem  → npx + carpetas autorizadas
github      → npx + PAT histórico
```

Ejemplo sanitizado:

```text
mcp/config/claude_desktop_config.example.json
```

Para recoger determinados cambios era frecuente tener que:

```text
modificar configuración/código
→ Quit Claude completamente desde bandeja
→ abrir Claude otra vez
→ verificar MCP Server en Developer
→ volver a probar
```

Claude Desktop **funcionó correctamente** para aprender y usar MCP. El cambio posterior a Cline no se hizo porque Claude no sirviera, sino para reducir la fricción del ciclo de desarrollo.

---

## 6. Por qué pasamos de Claude Desktop a VS Code + Cline

El laboratorio evolucionó a **VS Code + Cline** porque estábamos modificando y probando `maximo_mcp.py` continuamente.

Con Claude Desktop el ciclo podía ser:

```text
editar fuera de Claude
→ guardar
→ cerrar completamente Claude
→ abrir
→ verificar servidor
→ probar
```

Con VS Code + Cline pudimos concentrar el trabajo en un único entorno:

```text
pedir/realizar cambio
→ editar código en VS Code
→ revisar diff
→ aprobar
→ Restart Server
→ probar
```

### ¿Por qué VS Code específicamente?

No hicimos una evaluación formal comparando todos los posibles front ends de Cline. **VS Code ya era el IDE principal del laboratorio** para trabajar con Python y `maximo_mcp.py`; por tanto, instalar Cline allí era la evolución con menor fricción y preservaba el entorno que ya estábamos usando.

Además, en nuestro trabajo práctico VS Code + Cline nos dio exactamente lo que necesitábamos:

- código y proyecto abiertos en el mismo IDE;
- extensión Python;
- terminal integrada;
- edición directa de archivos;
- revisión de cambios mediante diff;
- acceso a la configuración MCP;
- visibilidad de Tools / Resources / Prompts;
- reinicio individual de MCP Servers;
- prueba inmediata después de cada cambio.

Por eso la decisión real fue más bien:

```text
VS Code ya era nuestro IDE
        +
Cline aportaba el agente dentro de ese IDE
        ↓
menor fricción para editar → refrescar → probar
```

### Ventajas prácticas comprobadas de VS Code + Cline

- editar `maximo_mcp.py` directamente en el IDE;
- revisar cambios mediante diff antes de aceptarlos;
- disponer de terminal integrada cuando correspondía;
- visualizar MCP Servers y, para Maximo, **Tools (14), Resources (0), Prompts (0)**;
- reiniciar individualmente un servidor mediante **Restart Server**;
- editar la configuración MCP y probar sin reiniciar todo VS Code;
- seleccionar/cambiar el modelo de IA utilizado por Cline;
- combinar MCP con capacidades propias del agente/IDE.

**Idea clave:** Cline añadió capacidades agénticas y redujo la fricción de iteración; MCP siguió siendo el protocolo que exponía nuestras capacidades externas.

---

## 7. VS Code + Cline — configuración actual verificada

Ruta efectiva recuperada directamente:

```text
C:\Users\jpperdomo\.cline\data\settings\cline_mcp_settings.json
```

UI actual:

```text
VS Code
→ Cline
→ Customize
→ MCP
→ Installed
→ Edit Configuration
```

La configuración actual usa una sección `transport`:

```json
"maximo": {
  "transport": {
    "type": "stdio",
    "command": "C:/.../python.exe",
    "args": ["-u", "C:/.../maximo_mcp.py"]
  }
}
```

Ejemplo sanitizado:

```text
mcp/config/cline_mcp_settings.example.json
```

Ese ejemplo conserva `maximo`, `filesystem` y el `github` histórico recuperado. La sección GitHub es **evidencia de configuración**, no recomendación de instalación nueva: `@modelcontextprotocol/server-github` está deprecated y no fue revalidado funcionalmente en el cierre.

La ruta histórica `%APPDATA%\Code\User\globalStorage\...` pertenece a una configuración/versión anterior de Cline y ya no es la ruta efectiva actual.

Durante la revalidación final fue necesario iniciar sesión de nuevo en Cline y sustituir el modelo histórico que devolvía 404 por **DeepSeek V4 Flash**, mostrado entonces como `Free`.

---

## 8. Maximo MCP

Cline mostró:

```text
Tools (14)
Resources (0)
Prompts (0)
```

Las 14 Tools cubren:

- OTs;
- inventario;
- activos;
- transiciones y cambio de estado;
- consulta genérica `query_maximo`;
- creación de OT;
- Working Set;
- workflow;
- diagnóstico.

Prueba individual final:

```text
¿Cuántos SKF-6204 tenemos en el almacén CENTRAL?
```

Resultado mock:

```text
15 unidades
PASILLO-B2-ESTANTE4
```

---

## 9. Selección de Tools

El modelo utiliza señales como:

```text
nombre Tool
+ descripción/docstring
+ esquema de parámetros
+ intención/contexto
```

Una petición normal puede funcionar sin decir “usa MCP”.

Pero no es determinista: en una tarea el modelo intentó llamar una Tool inexistente y produjo:

```text
AI_NoSuchToolError
```

El servidor seguía activo. Una tarea nueva usando `consultar_inventario` real volvió a funcionar.

**Lección:** servidor activo ≠ tool calling siempre correcto.

---

## 10. Filesystem MCP y sandbox

**Qué es:** un MCP Server especializado en leer/escribir archivos y carpetas locales.

**Dónde se limita:** en la configuración del Host, dentro de los `args` de `@modelcontextprotocol/server-filesystem`, se indican las carpetas raíz permitidas.

**Cómo funciona:** Filesystem MCP solo puede operar dentro de esas raíces y sus subcarpetas; una ruta fuera de ellas queda bloqueada. Ese límite actúa como **sandbox**.

Prueba controlada:

```text
MCP-Claude  ✅ permitido
Downloads   ❌ inicialmente rechazado
```

Después se añadió `Downloads` en `args` y se ejecutó `Restart Server` solo sobre `filesystem`:

```text
MCP-Claude  ✅
Downloads   ✅
```

Esto confirmó que las raíces configuradas delimitan el acceso del servidor.

Además se observó que una petición no controlada puede hacer que **Cline use terminal o herramientas nativas** en lugar de Filesystem MCP. Para una prueba MCP específica conviene restringir explícitamente el mecanismo.

---

## 11. Prueba combinada final en Cline

Prompt utilizado en la prueba controlada final:

> Usa la Tool `query_maximo` del servidor MCP `maximo` para consultar `MXWO` y obtener las órdenes de trabajo disponibles, incluyendo `wonum`, `description`, `status` y `assetnum`. Considera abiertas las que no estén en estado `COMP`, `CLOSE` o `CAN`. Después usa exclusivamente una Tool del servidor MCP `filesystem` para crear `C:\Users\jpperdomo\Downloads\ots_abiertas_cline_mcp.csv` con las columnas `numero_ot`, `descripcion`, `estado` y `activo`. No uses terminal, comandos del sistema, herramientas nativas de archivos ni leas ningún CSV existente.

Se obligó así a utilizar:

```text
Maximo MCP
  └─ query_maximo(MXWO)

Filesystem MCP
  └─ write_file
```

sin terminal ni CSV previo.

Resultado:

```text
C:\Users\jpperdomo\Downloads\ots_abiertas_cline_mcp.csv
```

con cuatro OTs abiertas simuladas:

```text
OT-1001
OT-1002
OT-1003
OT-1004
```

`OT-1005` quedó fuera por estado `COMP` = **Completada**.

✅ Se validó composición de dos MCP Servers en Cline.

Claude Desktop ya había superado una prueba equivalente creando `ots_abiertas.csv` mediante Maximo MCP + Filesystem MCP.

---

## 12. Claude Desktop vs VS Code + Cline

| Tema | Claude Desktop | VS Code + Cline |
|---|---|---|
| Papel en el LAB | primer Host MCP | entorno posterior de desarrollo/prueba |
| Modelo | Claude integrado | modelo seleccionable |
| Config | `claude_desktop_config.json` | `cline_mcp_settings.json` |
| JSON observado | `command/args/env` | `transport.type/command/args/env` |
| Recarga | podía requerir Quit/reabrir | `Restart Server` individual |
| Edición de código | fuera del flujo principal de chat | integrada en el IDE + diff/approve |
| Terminal | no fue el foco del Host | integrada en el entorno Cline/VS Code |
| Visibilidad MCP | servidor/conectores según UI | servidores + Tools/Resources/Prompts visibles |
| Prueba Maximo + Filesystem | ✅ | ✅ |

---

## 13. GitHub MCP

Históricamente se usó:

```text
@modelcontextprotocol/server-github
```

Ese paquete quedó deprecated. El issue #1 del Learning Lab documenta el incidente y la decisión de **no reinstalarlo ahora**.

La configuración Cline sanitizada conserva esa sección histórica porque formó parte del entorno recuperado, pero **no se considera revalidada ni recomendada para nuevas instalaciones**.

Si alguna vez se recupera, se usará la implementación oficial vigente `github/github-mcp-server` y autenticación de mínimo privilegio.

---

## 14. Lo que NO debe confundirse con producción

La PoC incluye simplificaciones deliberadas:

- `MODO_SIMULACION = True`;
- sin Maximo real;
- `verify=False` en la rama HTTP histórica: Python `requests` acepta la conexión HTTPS **sin verificar el certificado TLS/SSL del servidor**. Fue útil en una PoC con certificados internos, pero reduce seguridad y **no debe trasladarse a producción**;
- credenciales modeladas de forma simple;
- Working Set en memoria;
- reglas de estado locales;
- sin autorización empresarial;
- sin auditoría/observabilidad robusta.

Conclusión correcta:

> **PoC MCP orientada a Maximo validada en simulación; integración viva con IBM Maximo no validada.**

---

## 15. Próximo paso

➡️ **RAG Learning Lab** bajo `rag/`.

Pregunta guía:

```text
¿Cómo calibro este equipo según su manual?
```

MCP → acceso a sistemas/capacidades.

RAG → recuperación de conocimiento desde documentos.
