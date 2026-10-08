# Validación - Sistema Experto

## Casos de prueba propuestos

### Caso 1: Equipo no enciende, sin alimentación externa
Hechos: encendido=no, bateria=no, luces=no, ventilador=no
- Regla esperada: r01
- Diagnóstico: Fallo de alimentación o adaptador/board
- Acción: probar adaptador, sin batería (extraíble), derivar a técnico

### Caso 2: Enciende, ventilador gira, sin imagen
Hechos: encendido=si, ventilador=si, pantalla=no, post=no
- Reglas: r04, r12 (según batería) -> diagnóstico sin imagen
- Verificación: probar pantalla externa (diferencial panel vs placa)

### Caso 3: Pasa logo, no arranca SO
Hechos: encendido=si, pantalla=si, post=si, arranque_so=no, bsod=no
- Regla: r05
- Acciones: orden de arranque, disco detectado en BIOS, reparación arranque, SMART

### Caso 4: BSOD al arrancar
Hechos: encendido=si, arranque_so=si, bsod=si
- Regla: r06
- Acciones: código STOP, modo seguro, drivers, RAM/disco

### Caso 5: Sobrecalentamiento
Hechos: calienta=si, lento=no
- Regla: r07

### Caso 6: Ruidos disco
Hechos: ruidos=si, disco=si
- Regla: r08 (crítico) -> backup inmediato

### Caso 7: Lentitud
Hechos: lento=si, disco=no
- Regla: r09

### Caso 8: WiFi
Hechos: wifi=si -> r10

### Caso 9: Audio
Hechos: audio=si -> r11

## Validación con tests

Ejecutar:
```bash
python -m unittest tests/test_reglas.py -v
```

Resultados esperados:
- test_carga_kb OK
- test_inferir_sin_hechos OK (0 diagnósticos)
- test_regla_no_enciende_sin_alimentacion OK (r01)
- test_sin_imagen_tras_encender OK (r04/r12)
- test_wifi_problema OK (r10)
- test_siguiente_pregunta_existe OK

## Validación manual (flujo consola)

```bash
python main.py
```
- Responder coherente a casos de prueba.
- Probar comandos: ayuda, reiniciar, salir, respuestas inválidas.
- Verificar explicación detallada del razonamiento.
- Comprobar que `no_sabe` no dispara reglas con igualdad estricta.

## Criterios de validación

- [x] Estructura de archivos creada según nombres obvios.
- [x] KB contiene preguntas y reglas suficientes para troubleshooting básico.
- [x] Motor realiza inferencia hacia adelante y solicita hechos faltantes.
- [x] Interfaz 100% consola, clara y usable.
- [x] Explicación del razonamiento disponible.
- [x] Tests básicos pasan.
- [x] Documentación (reglas, bitácora, entrevista, validación) completa.