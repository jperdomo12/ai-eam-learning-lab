# Manual técnico simulado — Transmisor de presión PT-201

> ⚠️ **DOCUMENTO SINTÉTICO DE LABORATORIO.** No corresponde a un fabricante ni debe utilizarse para mantenimiento real.

## Identificación

- Activo: `PT-201`
- Sitio: `PLANTA1`
- Tipo: transmisor de presión
- Rango simulado: `0–10 bar`
- Revisión documental: `4`

## 1. Propósito

Este documento contiene información simulada para aprender y evaluar un pipeline RAG aplicado a mantenimiento industrial.

## 2. Seguridad previa

Antes de intervenir el transmisor:

1. confirmar el permiso de trabajo aplicable;
2. aislar el instrumento del proceso;
3. eliminar presión residual;
4. verificar condición segura antes de conectar el calibrador;
5. utilizar el equipo de protección definido por el procedimiento local.

## 3. Inspección previa

Antes de calibrar:

- revisar conectores y tubing;
- comprobar ausencia de fugas;
- verificar que la placa del instrumento corresponde a `PT-201`;
- confirmar que el rango configurado es `0–10 bar`.

## 4. Procedimiento de calibración

Para calibrar `PT-201`:

1. conectar un calibrador de presión de referencia al transmisor aislado;
2. aplicar `0,0 bar` y comprobar el cero;
3. si el error absoluto supera `0,02 bar`, ajustar **ZERO**;
4. aplicar `10,0 bar` y comprobar el fondo de escala;
5. si es necesario, ajustar **SPAN**;
6. aplicar `5,0 bar` como punto intermedio de verificación;
7. repetir la secuencia `0 → 5 → 10 bar`;
8. aceptar la calibración únicamente si el error en cada punto es menor o igual a `±0,05 bar`;
9. registrar los valores finales **as-left** en el registro de mantenimiento.

## 5. Criterio de aceptación

La calibración se considera aceptable cuando:

- error a `0 bar` ≤ `±0,05 bar`;
- error a `5 bar` ≤ `±0,05 bar`;
- error a `10 bar` ≤ `±0,05 bar`.

Si cualquier punto supera la tolerancia después del ajuste, el instrumento debe marcarse para evaluación adicional.

## 6. Troubleshooting

### Lectura inestable

Revisar:

- conexiones flojas;
- aire atrapado en la línea;
- vibración excesiva;
- fuente de alimentación;
- estado del calibrador de referencia.

### Desviación recurrente

Si el instrumento vuelve a quedar fuera de tolerancia poco después de calibrarlo, evaluar deriva del sensor y considerar sustitución o diagnóstico especializado.
