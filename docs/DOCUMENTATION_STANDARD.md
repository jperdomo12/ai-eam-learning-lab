# 📚 Estándar de Documentación
## AI-EAM Learning Lab

> **Principio rector:** documentar para aprender, recordar y reutilizar; no para burocratizar.

| Campo | Valor |
|---|---|
| **Ruta** | `docs/DOCUMENTATION_STANDARD.md` |
| **Versión** | 0.4 |
| **Estado** | Activo de laboratorio |
| **Fecha** | 10/09/2026 |
| **Ámbito** | Toda la documentación del Learning Lab |

## 🕘 Historial

| Versión | Fecha | Cambio |
|---|---:|---|
| 0.4 | 10/09/2026 | Se adopta formalmente el modelo de **documentación viva**: los materiales históricos o importados son fuentes de referencia; la documentación vigente debe ser reconstruida, verificada y mantenida dentro del Learning Lab. |
| 0.3 | 10/09/2026 | Se adopta `main` como rama de trabajo por defecto para cambios habituales del Learning Lab. |
| 0.2 | 10/09/2026 | Se incorpora un bloque `Historial` obligatorio y ligero en cada documento. |
| 0.1 | 10/09/2026 | Primera versión del estándar. |

---

## 🎯 1. Propósito

Este estándar define cómo mantener `ai-eam-learning-lab` como una **memoria técnica viva, autosuficiente y reutilizable**.

El objetivo no es archivar documentos antiguos ni depender de chats previos. El objetivo es que, dentro de semanas o meses, el repositorio permita responder por sí mismo:

- qué queríamos aprender;
- qué hicimos realmente;
- cómo lo instalamos y configuramos;
- qué pruebas ejecutamos;
- qué funcionó y qué no;
- qué evidencias sustentan cada afirmación;
- qué aprendimos;
- qué relación tiene con EAM / IBM Maximo;
- qué queda pendiente.

---

## 🟢 2. Documentación viva: regla principal

La documentación oficial del Learning Lab es la documentación **creada y mantenida dentro de este repositorio bajo el enfoque actual**.

Los materiales anteriores —bitácoras, chats, Gemini, Claude, documentos locales, repositorios temporales, capturas, configuraciones, ZIPs, notas o PoCs— son **fuentes de entrada y evidencia**, no documentación vigente por sí mismos.

El flujo correcto es:

```text
FUENTES / EVIDENCIA
(docs antiguos, código, configs, capturas, chats, ZIPs...)
            ↓
      revisar / contrastar
            ↓
   resolver inconsistencias
            ↓
DOCUMENTACIÓN VIVA DEL LAB
            ↓
 mantener actualizada en GitHub
```

### Consecuencia práctica

Un documento antiguo puede ser útil para reconstruir qué ocurrió, pero **no se copia ni se adopta automáticamente**. El Learning Lab debe producir su propia explicación consolidada, clara y actualizada.

### Fuente de verdad del Learning Lab

Para lo estudiado y experimentado en este repositorio, prevalece:

1. evidencia primaria conservada o auditada;
2. documentación viva vigente del Learning Lab;
3. material histórico o narrativo de referencia.

Si dos fuentes históricas discrepan, la documentación viva debe registrar la discrepancia y resolverla cuando exista evidencia suficiente.

---

## ⚡ 3. Filosofía de trabajo

### 3.1 Aprender haciendo
Siempre que sea razonable, un concepto debe terminar en una prueba, ejemplo, ejercicio o experimento reproducible.

### 3.2 Claridad antes que formalismo
No se añade ceremonia que no aporte valor. La documentación puede ser ligera, pero nunca debe ser ambigua sobre lo que se hizo.

### 3.3 Escribir para el “yo de dentro de seis meses”
Una buena nota debe poder entenderse sin reconstruir un chat anterior.

### 3.4 `main` por defecto
El Learning Lab trabaja directamente sobre `main` cuando el cambio sea seguro, claro y reversible. Branches y PR se utilizan solo cuando aportan valor real.

---

## 🧭 4. Niveles de evidencia

Usar estas etiquetas cuando ayuden a evitar confusión:

- 📘 **ENTENDIDO** — concepto estudiado y explicado.
- 🧪 **PROBADO** — ejecutado realmente en el laboratorio.
- ✅ **VERIFICADO** — comprobado mediante evidencia primaria suficiente.
- 📎 **REFERENCIA** — material previo utilizado como fuente de reconstrucción.
- 💡 **INFERIDO** — conclusión razonable todavía no demostrada.
- 🟨 **CANDIDATO AI-EAM-MAXIMO** — aprendizaje potencialmente reutilizable en el producto.
- 🟩 **INCORPORADO AI-EAM-MAXIMO** — aprobado e incorporado en el repositorio de producto.

Nada pasa del Learning Lab al producto automáticamente.

---

## 🗂️ 5. Tipos de documentos

| Tipo | Uso |
|---|---|
| `README.md` | Entrada del tema y mapa de navegación. |
| `*_LIVING_DOCUMENTATION.md` | Documento vivo canónico de un tema cuando se necesita una memoria completa y evolutiva. |
| `STUDY-*.md` | Nota conceptual específica. |
| `LAB-*.md` | Experimento o PoC reproducible. |
| `GUIDE-*.md` | Procedimiento reutilizable. |
| `*_HANDOFF.md` | Estado y continuidad entre etapas/chats. |
| `history/` | Material histórico de referencia; nunca fuente vigente por sí solo. |

> **Regla:** actualizar antes que crear. Evitar duplicar la misma verdad en varios documentos.

---

## 🧪 6. Qué debe registrar una prueba práctica

Cuando se realice una instalación, configuración o prueba, registrar según aplique:

```text
Objetivo
↓
Precondiciones / entorno
↓
Instalaciones
↓
Configuración
↓
Pasos ejecutados
↓
Prueba
↓
Resultado observado
↓
Problema / solución
↓
Evidencia
↓
Aprendizaje
↓
Estado final / siguiente paso
```

No esperar al final de varios meses para reconstruirlo todo retrospectivamente.

---

## 🕘 7. Historial mínimo, siempre

Todo documento Markdown mantenido por el laboratorio debe incluir:

```markdown
## 🕘 Historial

| Fecha | Cambio |
|---|---|
| AAAA-MM-DD | Creación inicial. |
| AAAA-MM-DD | Cambio relevante posterior. |
```

Registrar solo creación y cambios con valor real para comprender la evolución.

---

## 🧭 8. README de cada tema

Cada tema activo debe tener un `README.md` corto que permita conocer:

- objetivo;
- estado;
- documento vivo principal;
- pruebas realizadas;
- referencias históricas disponibles;
- siguiente paso.

El README orienta; no debe competir con el documento vivo principal.

---

## 🔄 9. HandOff ligero

El HandOff sirve para continuidad, no para duplicar toda la documentación.

Debe apuntar al documento vivo correspondiente y resumir:

- dónde estamos;
- qué está cerrado;
- qué está pendiente;
- qué archivos leer primero;
- cuál es el siguiente paso.

---

## 📎 10. Material histórico y fuentes de referencia

Todo material importado de estudios o experimentos anteriores debe tratarse como **referencia**.

Cuando se conserve bajo `history/`, debe indicarse claramente:

> ⚠️ **REFERENCIA HISTÓRICA — no constituye documentación técnica vigente. La verdad consolidada debe consultarse en el documento vivo del tema.**

Puede conservar discrepancias, errores o formulaciones antiguas porque su objetivo es preservar contexto histórico, no sustituir la documentación vigente.

---

## 🔐 11. Seguridad en un repositorio público

Nunca almacenar:

- contraseñas;
- API keys;
- PATs/tokens;
- credenciales Maximo;
- endpoints privados sensibles;
- datos reales de clientes;
- información personal/confidencial innecesaria.

Las configuraciones deben publicarse sanitizadas mediante placeholders, variables de entorno o archivos `*.example.*`.

---

## 🔗 12. Relación con AI-EAM-MAXIMO

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

El repositorio `jperdomo12/ai-driven-eam-copilot` continúa siendo la fuente de verdad del producto AI-EAM-MAXIMO.

---

## ✅ 13. Quality Check

Antes de cerrar una etapa comprobar:

- ¿la documentación viva explica qué se hizo sin depender del chat?;
- ¿incluye instalaciones, configuración, pruebas y resultados cuando aplican?;
- ¿se distingue evidencia primaria de referencia histórica?;
- ¿las contradicciones conocidas están resueltas o explícitamente marcadas?;
- ¿los ejemplos sensibles están sanitizados?;
- ¿el README apunta a la documentación viva correcta?;
- ¿el HandOff refleja el estado real?;

---

## 🌱 14. Regla final

> **Las fuentes históricas ayudan a recordar. La documentación viva del Learning Lab explica la verdad consolidada de lo que aprendimos, hicimos y comprobamos.**
