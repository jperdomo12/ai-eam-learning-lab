# 📚 Estándar de Documentación
## AI-EAM Learning Lab

> **Principio rector:** documentar para aprender, recordar y reutilizar; no para burocratizar.

| Campo | Valor |
|---|---|
| **Ruta** | `DOCUMENTATION_STANDARD.md` |
| **Versión** | 0.7 |
| **Estado** | Vigente — aplicable también cuando el Lab esté congelado |
| **Fecha** | 18/09/2026 |
| **Ámbito** | Toda la documentación del Learning Lab |

## 🕘 Historial

| Versión | Fecha | Cambio |
|---|---:|---|
| 0.7 | 18/09/2026 | Se formaliza la regla de **congelación / reapertura bajo demanda**, se aclara que los Markdown usados como datos fuente bajo `data/` no son documentación viva y se amplía el Quality Check para verificar el estado de cierre. |
| 0.6 | 18/09/2026 | Se incorpora el **Resumen de contenido** después del Historial para documentos medianos/largos o de consulta futura, con tabla breve de puntos y contenido; se añade la comprobación correspondiente al Quality Check. |
| 0.5 | 12/09/2026 | Se mueve el estándar a la raíz del repositorio para simplificar la estructura y se reafirma que **todo documento Markdown mantenido por el laboratorio debe incluir su Historial**. |
| 0.4 | 10/09/2026 | Se adopta formalmente el modelo de **documentación viva**: los materiales históricos o importados son fuentes de referencia; la documentación vigente debe ser reconstruida, verificada y mantenida dentro del Learning Lab. |
| 0.3 | 10/09/2026 | Se adopta `main` como rama de trabajo por defecto para cambios habituales del Learning Lab. |
| 0.2 | 10/09/2026 | Se incorpora un bloque `Historial` obligatorio y ligero en cada documento. |
| 0.1 | 10/09/2026 | Primera versión del estándar. |

---


## 🧭 Resumen de contenido

| Punto | Contenido |
|---|---|
| **1. Propósito** | Define para qué existe el estándar y qué debe poder recuperar el repositorio con el tiempo. |
| **2. Documentación viva** | Establece qué documentación es vigente y cómo tratar fuentes históricas o importadas. |
| **3. Filosofía de trabajo** | Fija principios de aprendizaje práctico, claridad, mantenibilidad, uso de `main` y congelación cuando el objetivo ya está cumplido. |
| **4. Niveles de evidencia** | Distingue entendido, probado, verificado, referencia, inferido y transferencia al producto. |
| **5. Tipos de documentos** | Define el uso de README, STUDY, LAB, GUIDE, HandOff y documentación viva. |
| **6. Pruebas prácticas** | Enumera qué debe registrarse cuando se realiza una instalación, configuración o experimento. |
| **7. Historial y resumen de contenido** | Define el Historial obligatorio y el Resumen de contenido para documentos medianos/largos. |
| **8. README de tema** | Define el README como entrada y mapa de navegación, no como duplicado de la documentación. |
| **9. HandOff** | Establece cómo mantener continuidad sin repetir toda la documentación. |
| **10. Material histórico** | Explica cómo conservar referencias antiguas sin confundirlas con la verdad vigente. |
| **11. Seguridad** | Evita publicar secretos, credenciales, endpoints privados o datos confidenciales. |
| **12. Relación con AI-EAM-MAXIMO** | Separa experimentación del Lab y decisiones oficiales del producto. |
| **13. Quality Check** | Resume las verificaciones antes de cerrar una etapa. |
| **14. Regla final** | Reafirma la documentación viva como memoria consolidada del aprendizaje. |

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

1. **evidencia primaria conservada o auditada**;
2. **documentación viva vigente** del Learning Lab;
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

### 3.5 Congelar cuando el objetivo está cumplido

Un LAB no debe continuar por inercia ni por numeración.

Cuando el objetivo pedagógico esté satisfecho:

```text
entender lo esencial
→ probar lo necesario
→ documentar lo justo
→ cerrar / congelar
→ volver al producto
```

Un LAB congelado se reabre únicamente si **AI-EAM-MAXIMO** plantea una necesidad concreta que requiera estudiar, validar o experimentar algo adicional. No se crean pasos, carpetas o documentos nuevos solo para mantener activa una secuencia.

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

**Todo documento Markdown mantenido por el laboratorio debe incluir su propio Historial.**

Formato mínimo:

```markdown
## 🕘 Historial

| Fecha | Cambio |
|---|---|
| AAAA-MM-DD | Creación inicial. |
| AAAA-MM-DD | Cambio relevante posterior. |
```

Registrar solo creación y cambios con valor real para comprender la evolución.

La regla aplica también a:

- README raíz;
- README de cada tema;
- documentación canónica;
- Fast Reading / resúmenes vigentes;
- HandOffs;
- guías y estudios mantenidos como documentación viva.

No aplica a archivos de código o configuración (`.py`, `.json`, etc.) ni obliga a modificar artefactos históricos preservados únicamente como evidencia.

### 7.1 Resumen de contenido para documentos medianos/largos

Los documentos diseñados para consulta futura deben permitir entender su estructura **sin tener que recorrerlos completos**.

Después del bloque `Historial`, incluir un:

```markdown
## 🧭 Resumen de contenido

| Punto | Contenido |
|---|---|
| **1. Nombre del punto** | Descripción muy breve de lo que contiene. |
| **2. Nombre del punto** | Descripción muy breve de lo que contiene. |
```

Reglas:

- debe aparecer **inmediatamente después del Historial**;
- debe resumir las secciones principales, no repetir el contenido;
- cada descripción debe ser breve y orientada a recuperación rápida;
- debe mantenerse actualizado si cambian secciones o numeración;
- es **obligatorio** en documentos medianos/largos o de consulta futura, especialmente `STUDY-*.md`, `*_LIVING_DOCUMENTATION.md` y guías extensas;
- es **opcional** en documentos cortos, Fast Reading, HandOffs o README cuando su propia estructura ya cumple claramente la función de navegación;
- los Markdown bajo `data/` utilizados deliberadamente como **datos de entrada, fixtures o documentos fuente de una prueba** no se consideran documentación viva y están exentos de `Historial` y `Resumen de contenido`.

> **Principio:** el Resumen de contenido debe ayudar a decidir en segundos dónde está la información buscada.

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
- ¿todo documento Markdown vigente incluye su `Historial`?;
- ¿los documentos medianos/largos incluyen un `Resumen de contenido` breve y actualizado después del Historial?;
- ¿incluye instalaciones, configuración, pruebas y resultados cuando aplican?;
- ¿se distingue evidencia primaria de referencia histórica?;
- ¿las contradicciones conocidas están resueltas o explícitamente marcadas?;
- ¿los ejemplos sensibles están sanitizados?;
- ¿el README apunta a la documentación viva correcta?;
- ¿el HandOff refleja el estado real?;
- ¿si el objetivo del LAB ya está cumplido, su documentación indica claramente que está cerrado/congelado y que solo se reabre bajo demanda?;

---

## 🌱 14. Regla final

> **Las fuentes históricas ayudan a recordar. La documentación viva del Learning Lab explica la verdad consolidada de lo que aprendimos, hicimos y comprobamos.**
