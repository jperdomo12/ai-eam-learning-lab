# 🔌 MCP — Model Context Protocol

> 🎯 **Objetivo:** aprender MCP de forma práctica con foco EAM / IBM Maximo y conservar una memoria técnica completa, actualizada y reutilizable.
>
> 📍 **Estado:** ✅ **CERRADO / CONGELADO** para el alcance actual de aprendizaje.
>
> 🗓️ **Actualizado:** 2026-09-12

## 🕘 Historial

| Fecha | Cambio |
|---|---|
| 2026-09-18 | Cierre documental final: se registra que el RAG Lab posterior llegó hasta Paso 12, combinó Tools MCP + EAM + RAG y transfirió aprendizajes al producto; este MCP Lab permanece congelado y se reabre solo bajo demanda de AI-EAM-MAXIMO. |
| 2026-09-12 | Se incorpora el Historial exigido por el estándar documental y se aclara que la configuración Cline sanitizada conserva también el GitHub MCP histórico como evidencia, aunque no fue revalidado funcionalmente. |
| 2026-09-12 | Cierre/congelación del MCP LAB v1.2 tras la revalidación final de VS Code + Cline. |
| 2026-09-10 | Creación y consolidación inicial del área MCP en el Learning Lab. |

## 📚 Por dónde empezar

Para recuperar MCP rápidamente, leer en este orden:

1. [`docs/MCP_LAB_FAST_READING.md`](docs/MCP_LAB_FAST_READING.md) — resumen final de lectura rápida.
2. [`docs/MCP_LAB_DOCUMENTATION.md`](docs/MCP_LAB_DOCUMENTATION.md) — documentación canónica y detallada.
3. [`docs/MCP_LAB_HANDOFF.md`](docs/MCP_LAB_HANDOFF.md) — estado final y continuidad hacia RAG.
4. [`src/maximo_mcp.py`](src/maximo_mcp.py) — código de la PoC Maximo MCP preservado.
5. [`config/claude_desktop_config.example.json`](config/claude_desktop_config.example.json) — configuración Claude Desktop sanitizada.
6. [`config/cline_mcp_settings.example.json`](config/cline_mcp_settings.example.json) — configuración VS Code + Cline sanitizada; conserva `maximo`, `filesystem` y el `github` histórico recuperado.

`src/history/` conserva código temprano únicamente para reconstrucción histórica.

> **Importante:** la sección `github` del ejemplo Cline representa la configuración histórica recuperada. El paquete `@modelcontextprotocol/server-github` está deprecated y **no fue revalidado funcionalmente** en el cierre 2026-09-12; no debe usarse como receta para una instalación nueva.

---

## ✅ Qué quedó demostrado

- servidor MCP local Python/FastMCP;
- `stdio` como transporte local;
- Maximo MCP con **14 Tools**;
- datos EAM simulados;
- Claude Desktop como primer Host;
- VS Code + Cline como entorno posterior;
- selección autónoma y controlada de Tools;
- Filesystem MCP con sandbox de directorios;
- cambio de configuración + `Restart Server` en Cline;
- composición **Maximo MCP + Filesystem MCP** en Claude Desktop y Cline;
- Working Set experimental / Human-in-the-Loop;
- uso histórico de GitHub MCP.

## ❌ Qué no quedó validado

- conexión con una instancia viva de IBM Maximo;
- lectura/escritura real contra Maximo;
- workflow real;
- seguridad productiva;
- GitHub MCP oficial actual instalado en esta máquina;
- RAG **dentro de este MCP Lab**; RAG se estudió y verificó posteriormente bajo `rag/`, incluyendo composición MCP + RAG en el Paso 12.

---

## 🧩 Productos principales

```text
VS Code             → IDE
Cline               → extensión/agente en VS Code
Claude Desktop      → Host MCP inicial
Python + FastMCP    → servidor Maximo MCP histórico
Node.js / npx       → Filesystem MCP y GitHub MCP histórico
Filesystem MCP      → acceso delimitado a carpetas locales
Modelo IA en Cline  → seleccionable; no es Cline
```

La revalidación final de Cline utilizó **DeepSeek V4 Flash**, mostrado entonces como `Free`.

---

## ⚙️ Rutas de configuración verificadas

### Claude Desktop — instalación usada en el LAB

```text
C:\Users\jpperdomo\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json
```

### Cline — configuración actual recuperada

```text
C:\Users\jpperdomo\.cline\data\settings\cline_mcp_settings.json
```

La ruta histórica de Cline bajo `%APPDATA%\Code\User\globalStorage\...` se conserva solo como referencia de una versión/configuración anterior.

---

## 🔗 Relación con AI-EAM-MAXIMO

```text
Learning Lab MCP
      ↓
aprendizaje / evidencia
      ↓
🟨 CANDIDATO A INCORPORAR
      ↓ revisión explícita
AI-EAM-MAXIMO
```

Nada del laboratorio se convierte automáticamente en decisión o implementación del producto.

---

## 🧊 Estado posterior / reapertura

El frente RAG que figuraba originalmente como siguiente paso **ya fue completado** posteriormente bajo `rag/` hasta el Paso 12, incluyendo la composición de una Tool transaccional y una Tool RAG mediante MCP.

Los aprendizajes transferibles fueron evaluados e integrados de forma controlada en `jperdomo12/ai-driven-eam-copilot`.

Este MCP Lab queda **cerrado / congelado**. Solo se reabre si AI-EAM-MAXIMO presenta una necesidad concreta que requiera nueva experimentación MCP.
