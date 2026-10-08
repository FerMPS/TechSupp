# Bitácora de IA

## Fecha
2025-10-07

## Proceso de desarrollo

1. **Análisis de estructura**
   - Revisada estructura de carpetas: conocimiento/, docs/, tests/, archivos Python vacíos.
   - Nombres obvios identificados: motor.py, interfaz.py, main.py, explicacion.py, conocimiento/reglas.json, tests/test_reglas.py.

2. **Diseño del sistema experto**
   - Tipo: basado en reglas (IF-THEN), inferencia hacia adelante.
   - Dominio: soporte técnico, troubleshooting y reparación básica de laptops/computadores (consola).
   - Características: hacer preguntas diagnósticas, responder/diagnosticar según hechos, generar diagnóstico y pasos de resolución, explicar razonamiento.

3. **Implementación**

   - **conocimiento/reglas.json**: creado con metadata, preguntas diagnósticas (encendido, luces, ventilador, batería/carga, pantalla/POST/SO/BSOD, calentamiento, ruidos/disco, wifi/audio, lentitud) y 12 reglas con prioridad, condiciones, diagnóstico, confianza, pasos y explicación. Valores permitidos si/no/no_sabe.
   - **motor.py**: `MotorReglas` con carga KB, gestión de hechos, detección de hechos faltantes, siguiente pregunta, inferencia (orden por prioridad), obtención de diagnóstico principal/alternativos. Lógica: condición cumple solo si todos los hechos conocidos coinciden exactamente (no_sabe no iguala si/no -> no dispara).
   - **interfaz.py**: CLI con bienvenida, ayuda, lectura de respuestas (normaliza si/no/no_sabe/salir/reiniciar/ayuda), muestra diagnóstico (principal+alternativos), hechos recopilados, prompts de continuación.
   - **explicacion.py**: `Explicador` para generar explicación de razonamiento (regla, condiciones cumplidas, conclusión, justificación) y explicación completa del proceso.
   - **main.py**: Flujo principal: bucle diagnóstico -> preguntas hasta completar -> inferencia -> mostrar resultados -> opcional explicación detallada -> nuevo caso/reiniciar/salir.
   - **tests/test_reglas.py**: Pruebas unitarias (carga KB, sin hechos no infiere, r01 caso sin alimentación, casos con/sin imagen, wifi, siguiente_pregunta).

4. **Documentación**
   - `docs/reglas.md`: descripción, estructura, variables, tabla de reglas, funcionamiento, ejecución y pruebas.
   - `docs/bitacora_ia.md`: esta bitácora.

## Decisiones técnicas

- Motor simple y claro (reglas explícitas en JSON) para cumplir objetivos académicos.
- Inferencia hacia adelante con prioridad para priorizar diagnóstico más específico/grave.
- Tratamiento de `no_sabe`: no satisface igualdad estricta (evita falsos positivos).
- Diferenciación r04/r12 para reforzar diagnóstico diferencial (panel vs placa) vía salida externa.
- Interfaz estrictamente por consola, sin GUI.

## Validación

Pruebas básicas incluidas en `tests/test_reglas.py`. Funcionamiento esperado:
- Caso sin alimentación -> r01
- Sin imagen con ventilador girando -> r04/r12
- WiFi -> r10
- BSOD -> r06

## Resultados

Todos los archivos del proyecto (Python, JSON, MD, tests) han sido escritos con contenido completo y coherente con la estructura propuesta.
