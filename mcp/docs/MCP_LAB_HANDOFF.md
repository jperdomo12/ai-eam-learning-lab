# 🧭 MCP_LAB_HANDOFF

> 📍 **Estado:** ✅ **MCP LAB CERRADO / CONGELADO**
>
> 🗓️ **Actualizado:** 2026-09-12
>
> ➡️ **Próximo frente:** RAG Learning Lab bajo `rag/`.

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-12 | Se incorpora el Historial exigido por el estándar documental y se mantiene el estado final del MCP LAB tras la revisión documental. |
| 2026-09-12 | Cierre/congelación del laboratorio tras completar la revalidación final en VS Code + Cline. |
| 2026-09-10 | Creación del HandOff para continuidad del laboratorio MCP. |

## 1. Estado final

El laboratorio MCP queda cerrado para el alcance actual de aprendizaje.

Se completó la revalidación pendiente en **VS Code + Cline** y ya no existe ningún pendiente MCP necesario antes de pasar a RAG.

### Validado

- ✅ Maximo MCP operativo en Cline.
- ✅ Cline muestra **14 Tools, 0 Resources, 0 Prompts** para `maximo`.
- ✅ consulta de inventario `SKF-6204 / CENTRAL` → **15 unidades** en modo simulación.
- ✅ Filesystem MCP operativo.
- ✅ sandbox de Filesystem probado negativamente: `Downloads` fue rechazado cuando no estaba autorizado.
- ✅ `Downloads` añadido a la configuración Cline y habilitado mediante `Restart Server`.
- ✅ acceso posterior a `Downloads` mediante Filesystem MCP.
- ✅ composición controlada **Maximo MCP + Filesystem MCP** en Cline.
- ✅ `query_maximo` recuperó OTs simuladas y `write_file` creó `ots_abiertas_cline_mcp.csv`.
- ✅ prueba equivalente Maximo + Filesystem ya estaba validada también en Claude Desktop.
- ✅ configuración efectiva de Cline recuperada directamente.
- ✅ comparación práctica Claude Desktop vs Cline documentada.

### No validado

- ❌ IBM Maximo real.
- ❌ lectura/escritura real contra Maximo.
- ❌ workflow real.
- ❌ seguridad productiva.
- ❌ GitHub MCP oficial actual instalado/validado en esta máquina.
- ❌ RAG.

---

## 2. Configuración Cline efectiva recuperada

Ruta actual:

```text
C:\Users\jpperdomo\.cline\data\settings\cline_mcp_settings.json
```

Acceso desde UI:

```text
VS Code
→ Cline
→ Customize
→ MCP
→ Installed
→ Edit Configuration
```

El JSON actual utiliza el patrón:

```json
"maximo": {
  "transport": {
    "type": "stdio",
    "command": "...python.exe",
    "args": ["-u", "...maximo_mcp.py"]
  }
}
```

La ruta histórica documentada en abril de 2026:

```text
%APPDATA%\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json
```

queda como evidencia de una versión/configuración anterior y **no debe usarse como ruta actual por defecto**.

Ejemplo sanitizado vigente:

```text
mcp/config/cline_mcp_settings.example.json
```

El ejemplo conserva también la sección `github` histórica recuperada. Esa sección representa evidencia de configuración; el paquete `@modelcontextprotocol/server-github` está deprecated y no fue revalidado funcionalmente en el cierre.

---

## 3. Productos / entorno que debe recordarse

```text
VS Code             → IDE
Cline               → extensión/agente en VS Code
Modelo IA           → seleccionado por Cline; no es Cline
Python + FastMCP    → Maximo MCP histórico
Node.js / npx       → Filesystem MCP y GitHub MCP histórico
Filesystem MCP      → archivos dentro de raíces autorizadas
Claude Desktop      → primer Host MCP del laboratorio
```

Durante la revalidación:

- fue necesario volver a iniciar sesión en Cline;
- el modelo histórico `kwaipilot/kat-coder-pro` devolvió 404;
- se seleccionó **DeepSeek V4 Flash**, mostrado como `Free` en ese momento;
- las pruebas MCP volvieron a funcionar.

Esto demuestra que autenticación/modelo del Host y estado del MCP Server son capas diferentes.

---

## 4. Hallazgo importante sobre selección de Tools

Una petición natural:

```text
¿Cuántos SKF-6204 tenemos en el almacén CENTRAL?
```

permitió a Cline seleccionar correctamente la capacidad de inventario.

En otra tarea/contexto, el modelo intentó invocar una Tool inexistente y apareció:

```text
AI_NoSuchToolError: Model tried to call unavailable tool
```

La UI seguía mostrando `maximo` activo con 14 Tools.

En una tarea nueva, indicando la Tool real `consultar_inventario`, la operación funcionó de nuevo.

Conclusión:

> **Servidor MCP activo no implica que el modelo vaya a acertar siempre en el tool calling.**

Nombre, docstring y esquema de parámetros ayudan a la selección, pero no la hacen determinista.

---

## 5. Filesystem MCP — prueba de permisos

Estado inicial Cline:

```text
C:\Users\jpperdomo\JP\Profesional\IA\MCP-Claude  ✅
C:\Users\jpperdomo\Downloads                       ❌
```

Se añadió `Downloads` a `args` en `cline_mcp_settings.json` y se reinició únicamente `filesystem`.

Estado posterior:

```text
MCP-Claude  ✅
Downloads   ✅
```

La prueba negativa/positiva confirmó que Filesystem MCP aplica un sandbox basado en las raíces configuradas.

También se observó que Cline puede resolver una consulta de archivos mediante terminal/herramientas propias si el prompt no exige Filesystem MCP. Para una validación controlada se debe especificar la ruta MCP que se desea probar.

---

## 6. Prueba combinada definitiva en Cline

Flujo validado:

```text
Cline + DeepSeek V4 Flash
        │
        ├─ Maximo MCP
        │    └─ query_maximo(MXWO)
        │
        └─ Filesystem MCP
             └─ write_file
                    ↓
C:\Users\jpperdomo\Downloads\ots_abiertas_cline_mcp.csv
```

Resultado: cuatro OTs abiertas simuladas:

```text
OT-1001
OT-1002
OT-1003
OT-1004
```

`OT-1005` quedó fuera por estado `COMP` = **Completada**.

La simulación de `query_maximo` no reproduce toda la expresividad OSLC; Cline terminó aplicando parte del criterio de filtrado.

---

## 7. GitHub MCP — decisión cerrada

El laboratorio histórico utilizó:

```text
@modelcontextprotocol/server-github
```

Ese paquete quedó deprecated/archivado.

El issue #1 del repositorio documenta el incidente y la decisión consciente de **no invertir más tiempo en reinstalarlo** durante este laboratorio.

Si se necesitara de nuevo:

```text
github/github-mcp-server
```

será la referencia a evaluar, con autenticación de mínimo privilegio.

No reabrir este punto salvo nueva necesidad real.

---

## 8. Documentos y artefactos vigentes

```text
DOCUMENTATION_STANDARD.md
mcp/docs/MCP_LAB_FAST_READING.md
mcp/docs/MCP_LAB_DOCUMENTATION.md
mcp/docs/MCP_LAB_HANDOFF.md
mcp/src/maximo_mcp.py
mcp/src/history/connection_test.py
mcp/src/history/maximo_mcp_gemini_v1.py
mcp/config/claude_desktop_config.example.json
mcp/config/cline_mcp_settings.example.json
```

La documentación histórica de Gemini / Claude / Cline queda como fuente de transición; no compite con estos documentos vigentes.

---

## 9. Relación con AI-EAM-MAXIMO

Nada del MCP LAB pasa automáticamente al producto `jperdomo12/ai-driven-eam-copilot`.

Cualquier aprendizaje reutilizable debe tratarse allí como:

```text
🟨 CANDIDATO A INCORPORAR
→ análisis
→ decisión explícita
→ implementación/documentación del producto si procede
```

---

## 10. Próximo paso

➡️ Iniciar **RAG Learning Lab**.

Pregunta guía inicial:

```text
¿Cómo calibro este equipo según su manual?
```

No es necesario reabrir MCP para empezar RAG. MCP queda disponible como conocimiento consolidado y podrá combinarse más adelante con RAG si un experimento futuro lo requiere.
