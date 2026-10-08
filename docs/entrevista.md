# Entrevista - Adquisición de Conocimiento (Sistema Experto)

## Objetivo
Recopilar conocimiento para construir base de conocimiento para sistema experto de soporte técnico (troubleshooting y reparación básica de laptops/computadores).

## Preguntas planteadas (modelo de entrevista)

### 1. Alcance y dominio
- ¿Qué tipo de problemas debe cubrir el sistema (hardware, software, ambos)?
- ¿Qué nivel de reparación? (diagnóstico básico, usuario final, técnico nivel 1)?
- ¿Qué excluir (placas BGA complejas, soldaduras, datos críticos, etc.)?

### 2. Proceso de diagnóstico
- ¿Cuál es el flujo típico para un equipo que "no enciende"?
- ¿Qué preguntas diagnósticas consideras imprescindibles?
- ¿Cómo distinguir entre fallo de adaptador, batería, DC-in o placa base?
- ¿Cuándo usar prueba con pantalla externa?
- ¿Qué indica la presencia/ausencia de LEDs y ventilador?

### 3. Casos comunes
- No enciende / no arranca
- Sin imagen (black screen)
- Se queda en BIOS/logo
- Pantallas azules (BSOD)
- Sobrecalentamiento
- Ruidos (HDD vs ventilador)
- Lentitud del sistema
- Problemas WiFi/audio

### 4. Pasos de resolución
- ¿Qué acciones de primer nivel (verificables por usuario) recomiendas por caso?
- ¿Cuándo derivar a técnico (umbral de derivación)?
- Precauciones de seguridad (electricidad, hardware estático, datos)?

### 5. Incertidumbre
- ¿Cómo tratar respuestas "no sé" o información incompleta?
- ¿Usar grados de certeza/confianza por regla?

### 6. Representación del conocimiento
- ¿Prefieres reglas IF-THEN con prioridad? ¿O árbol de decisión?
- ¿Qué variables/atributos mínimos identificar por síntoma?

### Respuestas (síntesis para implementación)
- Enfoque: diagnóstico + pasos de resolución básicos para usuario final (nivel 1).
- Variables clave: encendido, alimentación (batería/adaptador/carga), indicadores (LEDs), ventilador, imagen (pantalla/POST), arranque SO, errores (BSOD), calentamiento, ruidos, disco, conectividad/audio, rendimiento.
- Estrategia diferencial: pantalla externa para distinguir panel vs placa; hard reset; probar adaptador/corriente; SMART/ruidos disco prioritarios (backup).
- Tratamiento incertidumbre: incluir "no_sabe", condiciones estrictas (no iguala) para evitar falsos positivos; confianza por regla.
- Reglas con prioridad para casos críticos (alimentación, disco mecánico).

Esta entrevista sirvió de base para definir preguntas y reglas en `conocimiento/reglas.json`.
