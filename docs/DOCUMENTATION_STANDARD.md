# 📚 Estándar de Documentación
## AI-EAM Learning Lab

> **Principio rector:** documentar para aprender, recordar y reutilizar; no para burocratizar.

| Campo | Valor |
|---|---|
| **Ruta** | `docs/DOCUMENTATION_STANDARD.md` |
| **Versión** | 0.1 |
| **Estado** | Borrador activo de laboratorio |
| **Fecha** | 10/09/2026 |
| **Ámbito** | Notas de estudio, experimentos, guías prácticas, handoffs e histórico del Learning Lab |

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

### 2.3 Git conserva la historia

No es obligatorio mantener tablas extensas de versiones en cada nota de estudio. Git conserva la evolución del contenido.

Solo los documentos estructurales del propio laboratorio —como este estándar o un HandOff importante— necesitan versión explícita cuando aporte valor.

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

Una nota de estudio puede utilizar esta estructura como guía flexible:

```markdown
# 🧠 Tema

> 🎯 **Quiero entender:** ...
> 📍 **Estado:** estudiando / entendido / pendiente de práctica
> 🗓️ **Actualizado:** AAAA-MM-DD

## 💡 En mis palabras
Explicación breve del concepto como lo entiendo ahora.

## 🗺️ Modelo mental
Diagrama, analogía o estructura que ayude a recordarlo.

## 🔑 Ideas que quiero recordar
- ...
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

No es obligatorio usar todas las secciones.

---

## 🧪 5. Formato para experimentos

Un experimento debe privilegiar reproducibilidad y aprendizaje:

```markdown
# 🧪 LAB — Nombre del experimento

> 🎯 **Objetivo:** ...
> 📍 **Resultado:** pendiente / funciona / funciona parcialmente / no funciona
> 🗓️ **Fecha:** AAAA-MM-DD

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

Debe permitir ver rápidamente:

1. qué estamos estudiando;
2. qué nivel hemos alcanzado;
3. conceptos principales;
4. experimentos realizados;
5. qué está pendiente;
6. siguiente paso;
7. enlaces a los documentos relevantes.

El README no debe convertirse en un tratado. Su función principal es orientar.

---

## 🔄 7. HandOff ligero

Un HandOff se crea o actualiza cuando sea útil cambiar de chat, cerrar una etapa o dejar una pausa prolongada.

Debe contener solo:

```markdown
# 🧭 <TEMA>_HANDOFF

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

Este repositorio es público. Nunca almacenar:

- contraseñas;
- API keys;
- tokens o PATs;
- secretos MCP;
- credenciales Maximo;
- URLs internas sensibles;
- datos reales de clientes;
- información personal o confidencial.

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

Antes de dar por útil una nota o experimento, comprobar solamente:

- ¿entiendo qué aprendimos?;
- ¿queda claro qué fue probado y qué es solo explicación o inferencia?;
- ¿podría retomarlo dentro de seis meses?;
- ¿hay información sensible?;
- ¿existe un siguiente paso si el tema continúa?

Si las respuestas son satisfactorias, la documentación es suficiente.

---

## 🌱 12. Regla final

> **La documentación del Learning Lab debe ser tan pequeña como sea posible y tan completa como sea necesario para seguir aprendiendo sin perder conocimiento.**
