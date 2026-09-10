# 📚 Estándar de Documentación
## AI-EAM Learning Lab

> **Principio rector:** documentar para aprender, recordar y reutilizar; no para burocratizar.

| Campo | Valor |
|---|---|
| **Ruta** | `docs/DOCUMENTATION_STANDARD.md` |
| **Versión** | 0.3 |
| **Estado** | Activo de laboratorio |
| **Fecha** | 10/09/2026 |
| **Ámbito** | Notas de estudio, experimentos, guías prácticas, handoffs e histórico del Learning Lab |

## 🕘 Historial

| Versión | Fecha | Cambio |
|---|---:|---|
| 0.3 | 10/09/2026 | Se adopta `main` como rama de trabajo por defecto para cambios habituales del Learning Lab; branches y PR quedan reservados para cambios donde aporten valor real. |
| 0.2 | 10/09/2026 | Se incorpora un bloque `Historial` obligatorio y ligero en cada documento del Learning Lab. |
| 0.1 | 10/09/2026 | Primera versión del estándar, adaptada a un repositorio ágil de estudio y experimentación. |

---

## 🎯 1. Propósito

Este estándar define una forma **ligera, visual y orientada al estudio** de documentar el repositorio `ai-eam-learning-lab`.

El objetivo no es reproducir el nivel formal de documentación de un producto. El objetivo es que, después de semanas o meses, sea posible volver a un tema y responder rápidamente:

- ¿qué quería aprender?;
- ¿qué entendí?;
- ¿qué probé realmente?;
- ¿qué funcionó y qué no?;
- ¿qué evidencia tengo?;
- ¿qué relación tiene con EAM / IBM Maximo?;
- ¿qué debería estudiar o probar después?

---

## ⚡ 2. Filosofía del Learning Lab

### 2.1 Aprender haciendo
Siempre que sea razonable, un concepto debe terminar en una prueba, ejemplo, ejercicio o experimento reproducible.

### 2.2 Claridad antes que formalismo
No se añade una sección porque una plantilla diga que debe existir. Si no aporta valor al aprendizaje, se omite.

### 2.3 Historial mínimo, siempre
Todo documento Markdown mantenido por el laboratorio debe incluir un bloque breve `## 🕘 Historial`.

La intención no es duplicar Git ni mantener control de versiones pesado. El bloque sirve para que, al abrir un documento, se entienda inmediatamente **cuándo nació y qué cambios relevantes tuvo**.

Formato recomendado:

```markdown
## 🕘 Historial

| Fecha | Cambio |
|---|---|
| AAAA-MM-DD | Creación inicial. |
| AAAA-MM-DD | Cambio relevante posterior. |
```

Si el documento usa versión explícita, puede añadirse la columna `Versión`.

No registrar correcciones ortográficas, ajustes cosméticos o cambios sin valor para el aprendizaje.

### 2.4 Escribir para el “yo de dentro de seis meses”
Una buena nota debe poder entenderse sin reconstruir el chat original.

### 2.5 Separar conocimiento de evidencia
No confundir:

- 📘 **ENTENDIDO** — concepto estudiado y explicado;
- 🧪 **PROBADO** — ejecutado realmente en el laboratorio;
- ✅ **VERIFICADO** — resultado comprobado con evidencia suficiente;
- 💡 **INFERIDO** — conclusión razonable todavía no demostrada;
- 🟨 **CANDIDATO AI-EAM-MAXIMO** — aprendizaje potencialmente reutilizable en el producto;
- 🟩 **INCORPORADO AI-EAM-MAXIMO** — solo cuando haya sido aprobado e incorporado allí.

Nada pasa del Learning Lab al producto automáticamente.

### 2.6 `main` por defecto: agilidad antes que ceremonia

El Learning Lab trabaja **directamente sobre `main` como regla general**.

Esto aplica especialmente a:

- notas de estudio;
- README y handoffs;
- material histórico;
- documentación y ajustes de estructura pequeños;
- pequeños scripts de laboratorio;
- experimentos acotados y fácilmente reversibles.

Crear una branch es **opcional** y se utiliza cuando el cambio tiene suficiente entidad como para que aislarlo aporte valor: refactorizaciones relevantes, automatizaciones, CI/CD, cambios estructurales amplios, código que pueda afectar varios experimentos o pruebas que convenga mantener separadas temporalmente.

Los Pull Requests tampoco son obligatorios en el laboratorio. Se usan cuando ayudan a revisar, comparar o cerrar un cambio importante; no como trámite.

> **Regla práctica:** si trabajar directamente en `main` es seguro, claro y reversible, trabajar en `main`.

Esta regla es propia del Learning Lab y **no modifica** el flujo formal del repositorio de producto `ai-driven-eam-copilot`.

---

## 🗂️ 3. Tipos de documentos

El laboratorio utiliza pocos tipos documentales y solo se crean cuando son necesarios.

| Tipo | Uso |
|---|---|
| `README.md` | Punto de entrada de un tema y mapa de navegación. |
| `STUDY-*.md` | Nota de estudio conceptual cuando el contenido merece una fuente propia. |
| `LAB-*.md` | Experimento, prueba práctica o PoC reproducible. |
| `GUIDE-*.md` | Procedimiento práctico que merece reutilizarse. |
| `*_HANDOFF.md` | Estado actual y próximo paso cuando se necesita continuidad entre chats o etapas. |
| `history/` | Material histórico conservado como referencia, no como verdad técnica vigente. |

> **Regla:** actualizar antes que crear. Si el conocimiento cabe naturalmente en un README o documento existente, no crear otro archivo.

---

## 🧠 4. Formato fresco para una nota de estudio

```markdown
# 🧠 Tema

> 🎯 **Quiero entender:** ...
> 📍 **Estado:** estudiando / entendido / pendiente de práctica
> 🗓️ **Actualizado:** AAAA-MM-DD

## 🕘 Historial
| Fecha | Cambio |
|---|---|
| AAAA-MM-DD | Creación inicial. |

## 💡 En mis palabras
Explicación breve del concepto como lo entiendo ahora.

## 🗺️ Modelo mental
Diagrama, analogía o estructura que ayude a recordarlo.

## 🔑 Ideas que quiero recordar
- ...

## 🧪 Lo llevamos a la práctica
Qué ejercicio o experimento hicimos y dónde está.

## 👀 Qué observé
Resultados reales, sorpresas, errores o diferencias con lo esperado.

## 🔧 Relación con EAM / IBM Maximo
Por qué podría importar en mi contexto profesional.

## ❓ Dudas abiertas
Lo que todavía no comprendo o quiero investigar.

## 🚀 Siguiente paso
Una acción concreta para continuar.

## 🔗 Referencias
Fuentes realmente utilizadas.
```

No es obligatorio usar todas las secciones, salvo el bloque `Historial`.

---

## 🧪 5. Formato para experimentos

```markdown
# 🧪 LAB — Nombre del experimento

> 🎯 **Objetivo:** ...
> 📍 **Resultado:** pendiente / funciona / funciona parcialmente / no funciona
> 🗓️ **Fecha:** AAAA-MM-DD

## 🕘 Historial
| Fecha | Cambio |
|---|---|
| AAAA-MM-DD | Creación inicial. |

## Hipótesis
¿Qué esperamos que ocurra?

## Setup
Entorno, herramientas y dependencias relevantes.

## Pasos
Solo los necesarios para reproducir la prueba.

## Resultado observado
Qué ocurrió realmente.

## Evidencia
Logs, capturas, salida, archivos o comportamiento verificable.

## Qué aprendí
Conclusiones útiles, incluyendo errores y falsas suposiciones.

## Relación con EAM / Maximo
Aplicabilidad potencial, si existe.

## Siguiente experimento
Una continuación concreta.
```

Un experimento fallido sigue siendo un resultado válido si deja aprendizaje útil.

---

## 🧭 6. README de cada tema

Cada área activa —por ejemplo `mcp/`— debe tener un `README.md` corto que funcione como **panel de estudio**.

Debe permitir ver rápidamente qué estamos estudiando, qué nivel hemos alcanzado, qué probamos, qué está pendiente y cuál es el siguiente paso.

El README no debe convertirse en un tratado. Su función principal es orientar.

---

## 🔄 7. HandOff ligero

Un HandOff se crea o actualiza cuando sea útil cambiar de chat, cerrar una etapa o dejar una pausa prolongada.

Estructura mínima:

```markdown
# 🧭 <TEMA>_HANDOFF

## 🕘 Historial
...

## Dónde estamos
...

## Qué ya entendimos
...

## Qué ya probamos
...

## Qué NO está demostrado todavía
...

## Archivos clave
...

## Próximo paso
...
```

No debe reconstruir toda la conversación.

---

## 🕰️ 8. Material histórico

El material importado de estudios, chats, Gemini, Claude, PoCs anteriores u otros proyectos puede conservarse bajo `history/`.

Debe quedar claramente marcado:

> ⚠️ **HISTÓRICO — material de referencia. No constituye documentación técnica vigente del Learning Lab ni del producto AI-EAM-MAXIMO.**

El histórico se conserva para aprender de lo realizado, no para asumir que sigue siendo técnicamente correcto.

---

## 🔐 9. Seguridad en un repositorio público

Este repositorio es público. Nunca almacenar contraseñas, API keys, tokens o PATs, secretos MCP, credenciales Maximo, URLs internas sensibles, datos reales de clientes o información personal/confidencial.

Las configuraciones reutilizables deben usar ejemplos seguros, variables de entorno o archivos `*.example.*`.

---

## 🔗 10. Relación con AI-EAM-MAXIMO

```text
AI-EAM Learning Lab
   aprender / experimentar
          ↓
   aprendizaje útil
          ↓
🟨 CANDIDATO A INCORPORAR
          ↓ revisión y decisión
AI-EAM-MAXIMO
          ↓
🟩 documentación + implementación oficial
```

El repositorio oficial `ai-driven-eam-copilot` sigue siendo la fuente de verdad del producto AI-EAM-MAXIMO.

---

## ✅ 11. Quality Check de 30 segundos

Antes de dar por útil una nota o experimento, comprobar:

- ¿entiendo qué aprendimos?;
- ¿queda claro qué fue probado y qué es explicación o inferencia?;
- ¿podría retomarlo dentro de seis meses?;
- ¿el bloque `Historial` refleja los cambios relevantes?;
- ¿hay información sensible?;
- ¿existe un siguiente paso si el tema continúa?

---

## 🌱 12. Regla final

> **La documentación del Learning Lab debe ser tan pequeña como sea posible y tan completa como sea necesario para seguir aprendiendo sin perder conocimiento.**
