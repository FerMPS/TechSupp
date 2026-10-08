# Base de Conocimiento - Sistema Experto (Soporte Técnico)

## Descripción

Sistema experto por consola para diagnóstico y resolución básica de problemas de laptops y computadores. Utiliza inferencia hacia adelante basada en reglas IF-THEN.

## Estructura

- `motor.py`: Motor de inferencia, gestión de hechos y evaluación de reglas.
- `interfaz.py`: Interfaz de usuario por consola (preguntas, diagnósticos, pasos).
- `main.py`: Punto de entrada y flujo de ejecución.
- `explicacion.py`: Explicación del razonamiento (reglas disparadas, condiciones, justificación).
- `conocimiento/reglas.json`: Base de conocimiento (preguntas, reglas, metadata).
- `tests/test_reglas.py`: Pruebas unitarias básicas.

## Variables/Hechos

Los hechos son respuestas a preguntas diagnósticas: `si`, `no`, `no_sabe`.

Preguntas definidas (IDs): `encendido`, `luces`, `ventilador`, `bateria`, `carga`, `pantalla`, `post`, `arranque_so`, `bsod`, `calienta`, `ruidos`, `wifi`, `audio`, `lento`, `disco`.

## Reglas (resumen)

| ID | Prioridad | Condición resumida | Diagnóstico |
|---|-----------|-------------------|-------------|
| r01 | 100 | encendido=no, bateria=no, luces=no, ventilador=no | Fallo de alimentación/adaptador/placa |
| r02 | 95  | encendido=no, bateria=si, carga=no, luces=no | Sin indicación de carga (adaptador/circuito) |
| r03 | 90  | encendido=no, luces=si, ventilador=no, pantalla=no | Alimentación parcial, ventilador bloqueado/fallo |
| r04 | 90  | encendido=si, ventilador=si, pantalla=no, post=no | Sin imagen (panel/backlight/RAM/GPU/BIOS) |
| r05 | 88  | encendido=si, pantalla=si, post=si, arranque_so=no, bsod=no | Se queda en logo, no arranca SO |
| r06 | 87  | encendido=si, arranque_so=si, bsod=si | BSOD (drivers/RAM/disco) |
| r07 | 80  | calienta=si, lento=no | Sobrecalentamiento (polvo/pasta térmica/flujo aire) |
| r08 | 78  | ruidos=si, disco=si | Ruidos HDD (fallo mecánico) - backup prioritario |
| r09 | 75  | lento=si, disco=no | Lentitud software (inicio/memoria/SSD vs HDD) |
| r10 | 70  | wifi=si | Problemas WiFi (drivers/router/señal) |
| r11 | 68  | audio=si | Problemas audio (salida/drivers/hardware) |
| r12 | 85  | encendido=si, ventilador=si, pantalla=no, post=no, bateria=si | Sin imagen (diferencial panel/placa) |

## Funcionamiento

1. Motor carga KB desde `conocimiento/reglas.json`.
2. Mientras existan hechos faltantes necesarios para reglas: solicita siguiente pregunta (ordenada por relevancia).
3. Usuario responde `si/no/no_sabe`.
4. Al tener hechos suficientes: inferencia hacia adelante -> dispara reglas cuyas condiciones se cumplen (prioridad desc).
5. Se muestra diagnóstico principal + pasos de resolución + alternativas.
6. Opcional: explicación detallada del razonamiento.

## Notas

- No requiere entorno gráfico (solo consola).
- Reglas diseñadas para troubleshooting y reparación básica (diagnóstico + pasos accionables).
- Usa valores `no_sabe` cuando hay incertidumbre (no satisface condición estricta).

## Ejecución

```bash
python main.py
```

## Pruebas

```bash
python -m unittest tests/test_reglas.py
```