# Sistema Experto - Agente Diagnóstico Conversacional

## Índice

- [Descripción General](#descripción-general)
- [Filosofía del Proyecto](#filosofía-del-proyecto)
- [Arquitectura](#arquitectura)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Descripción de Componentes](#descripción-de-componentes)
- [Base de Conocimiento (Grafo de Decisión)](#base-de-conocimiento-grafo-de-decisión)
- [Flujo de Conversación](#flujo-de-conversación)
- [Características Clave](#características-clave)
- [Tecnologías y Dependencias](#tecnologías-y-dependencias)
- [Instalación y Uso](#instalación-y-uso)
- [Testing](#testing)
- [Extensibilidad](#extensibilidad)
- [Licencia y Alcance](#licencia-y-alcance)

## Descripción General

El **Sistema Experto para Soporte Técnico Básico** es un agente de diagnóstico conversacional diseñado para guiar a usuarios no técnicos en la resolución de problemas comunes de PCs y portátiles (laptops). 

A diferencia de un sistema basado en cadenas de `if-elif` anidadas, este proyecto ha sido refactorizado para funcionar como un **asistente conversacional humano**: hace preguntas de sondeo lógicas, recuerda el contexto de la conversación, gestiona la incertidumbre cuando el usuario no conoce términos técnicos, y proporciona explicaciones en lenguaje natural junto a un diagnóstico orientativo paso a paso.

**Problemas que puede diagnosticar (actualmente):**

- PC/portátil no enciende (sin signos de vida, con signos parciales)
- Enciende pero pantalla negra (sin imagen, pasa/no pasa POST, logo BIOS)
- BSOD (Pantallas Azules) al arrancar o usar el sistema
- Se queda en logo/fabricante y no carga el Sistema Operativo
- Equipos lentos (lentitud general)
- Problemas de alimentación, RAM, disco, GPU o bootloader

## Filosofía del Proyecto

El diseño se basa en los siguientes principios fundamentales:

### 1. Explicabilidad (Explainable AI)
- **Razonamiento transparente**: Cada diagnóstico va acompañado de una explicación del razonamiento que detalla el camino de sondeo seguido, hechos recopilados y nivel de certeza.
- **Justificación natural**: El módulo `explicacion.py` traduce el estado interno del motor a lenguaje comprensible para un usuario no técnico.
- **Sin caja negra**: Todas las reglas de decisión son explícitas, visibles y auditables en `reglas.json`.

### 2. Determinismo y Fiabilidad
- **Basado en reglas, no estocástico**: Prioriza lógica determinista (grafos + hechos) frente a generación libre de LLM para garantizar resultados consistentes y testeables.
- **100% local**: No depende de APIs externas de pago, servicios en la nube o modelos remotos. Funciona completamente offline.
- **Diagnóstico orientativo**: Promueve la seguridad con advertencias para derivar a técnico ante casos de hardware crítico.

### 3. Conversación Natural (Human-like)
- **Apertura → Cierre**: Comienza con una pregunta abierta ("Cuéntame qué pasa...") para no abrumar al usuario, y va cerrando el sondeo a opciones específicas ("¿Se ve imagen en pantalla?").
- **Gestión de incertidumbre**: Si el usuario responde `no_sabe`, el sistema explica brevemente el término técnico, ofrece alternativas de diagnóstico y continúa sin romper el flujo conversacional.
- **Contexto persistente**: Recuerda todos los hechos confirmados, nodos visitados, preguntas realizadas e incertidumbres a lo largo de toda la conversación.

### 4. Modularidad y Mantenibilidad
- **Separación de responsabilidades**: Motor (lógica), Interfaz (UX), Explicación (razonamiento) y Conocimiento (reglas) están completamente desacoplados.
- **Sin ifs anidados**: La lógica de transición es declarativa (grafo de nodos) en lugar de imperativa, lo que facilita su lectura, extensión y validación.
- **Fácil de testear**: Estructura diseñada para permitir tests unitarios del motor, validación del grafo y pruebas de flujos conversacionales.

### 5. Experiencia de Usuario (UX) en Consola
- **Estilo ChatGPT/terminal moderna**: Interfaz con `Rich` que simula un chat real con colores diferenciados por rol (Asistente/Tú).
- **Efecto "escribiendo..."**: Delays de escritura configurables para dar naturalidad al diálogo sin ralentizar innecesariamente.
- **Feedback claro**: Muestra resumen de hechos acumulados, nivel de certeza, puntos con incertidumbre y camino de razonamiento.

## Arquitectura

El sistema sigue una arquitectura en capas con flujo unidireccional:

```
Usuario (Consola)
  ↓
Interfaz (interfaz.py - Rich)
  ↓
Main (main.py - Orquestador)
  ↓
Motor Conversacional (motor.py - Grafo + Máquina de Estados)
  ↕
Base de Conocimiento (conocimiento/reglas.json - Grafo de Nodos)
  ↓
Explicador (explicacion.py - Lenguaje Natural)
  ↑
Interfaz (Visualización al usuario)
```

### Componentes arquitectónicos

| Capa | Responsabilidad | Tecnología |
|---|---|---|
| **Presentación** | Chat conversacional, colores, delays, entrada/salida | `Rich` |
| **Orquestación** | Control de flujo, manejo de comandos (`salir/reiniciar/ayuda`), bucle conversacional | Python puro |
| **Lógica/Dominio** | Máquina de estados, navegación por grafo, inferencia de hechos, gestión de incertidumbre, cálculo de certeza | Python puro (+ `NetworkX` opcional) |
| **Conocimiento** | Modelo declarativo del árbol de decisión (nodos, transiciones si/no/no_sabe, diagnósticos finales) | JSON |
| **Explicación** | Generación de razonamiento en lenguaje natural | Python puro |

## Estructura del Proyecto

```text
Sistema Experto/
│
├── README.md                    # Documentación comprensiva del proyecto (este archivo)
│
├── main.py                      # Punto de entrada. Orquesta flujo conversacional y comandos
├── motor.py                     # Motor conversacional basado en grafo + máquina de estados
├── interfaz.py                  # Interfaz tipo chat con Rich (UI consola)
├── explicacion.py               # Generador de explicaciones en lenguaje natural
│
├── conocimiento/
│   └── reglas.json             # Base de conocimiento en formato grafo de nodos (KB)
│
├── tests/
│   ├── __pycache__/            # Cache de Python
│   └── test_reglas.py           # Tests unitarios del motor (compatibles con API clásica)
│
├── docs/
│   ├── arbol_decision.png      # Diagrama visual del árbol de decisión
│   ├── bitacora_ia.md           # Bitácora del desarrollo con IA
│   ├── entrevista.md           # Documentación de entrevista/requirements
│   ├── reglas.md               # Documentación de reglas (formato anterior)
│   └── validacion.md           # Documentación de validación
│
└── __pycache__/                 # Cache de bytecode Python
```

## Descripción de Componentes

### 1. `motor.py` - Motor Conversacional (Grafo + Estados)

Clase principal: `MotorConversacionalGrafo`

**Propósito**: Núcleo del sistema. Ejecuta el razonamiento diagnóstico sin cadenas if-elif anidadas, gestionando el estado de la conversación y navegando dinámicamente por el grafo de conocimiento.

**Atributos clave del estado (`self.estado`):**

| Campo | Tipo | Descripción |
|---|---|---|
| `descripcion` | `str` | Descripción inicial del problema (lenguaje natural) |
| `hechos` | `Dict[str, str]` | Hechos inferidos/confirmados (`si`/`no`/`no_sabe`) |
| `nodo_actual` | `str` | ID del nodo actual en el grafo |
| `nodo_anterior` | `str` | Nodo previo (para trazabilidad) |
| `nodos_visitados` | `List[str]` | Camino completo de sondeo seguido |
| `preguntas_hechas` | `List[str]` | IDs de nodos/preguntas ya realizadas |
| `etapa` | `str` | Etapa: `inicio` \| `sondeando` \| `diagnosticado` |
| `diagnostico_final` | `str \| None` | Diagnóstico cuando llega a nodo final |
| `pasos_solucion` | `List[str]` | Lista ordenada de pasos a seguir |
| `certeza` | `float` | Nivel de certeza (0.0 - 1.0) basado en hechos ciertos |
| `incertidumbre` | `List[str]` | Puntos donde usuario respondió `no_sabe` |
| `alternativas_sugeridas` | `List[str]` | Comprobaciones alternativas ante incertidumbre |

**Métodos principales:**

- `cargar()` / `_cargar_grafo()`: Carga KB desde JSON. Soporta `NetworkX.DiGraph` (recomendado) con fallback a dict puro.
- `limpiar()`: Reinicia estado para nueva conversación.
- `_normalizar()` / `_normalizar_respuesta()`: Normaliza texto y mapea sinónimos (`sí/s/y/yes` → `si`, `no sé/ns` → `no_sabe`).
- `establecer_descripcion(texto)`: Procesa descripción abierta e infiere hechos mediante patrones + reglas de inferencia.
- `establecer_hecho(clave, valor)`: Registra hecho confirmado, actualiza incertidumbre y certeza.
- `_extraer_hechos_desde_texto(texto)`: Extracción no determinista pero controlada (patrones + tabla de inferencias). Evita ifs anidados mediante lista de reglas.
- `_siguiente_por_grafo(respuesta)`: Determina siguiente nodo según transición `si/no/no_sabe` (o `default`). Lógica basada en grafo, no condicionales anidados.
- `siguiente_accion()`: Máquina de estados. Retorna acción a ejecutar: `pedir_descripcion`, `preguntar` o `diagnostico`.
- `responder_pregunta(respuesta)`: Procesa respuesta, registra hecho, avanza grafo, retorna siguiente acción.
- `obtener_estado_resumen()`: Devuelve snapshot del estado para trazabilidad/explicación.

**Diseño clave**: Transiciones declarativas. El motor consulta el grafo (edges con acción `si/no/no_sabe`) en lugar de evaluar árboles de `if`. Esto cumple el requisito "Motor Conversacional (No Ifs anidados)".

### 2. `interfaz.py` - Interfaz Chat con Rich

Clase principal: `InterfazConsolaChat`

**Propósito**: Proporciona una experiencia conversacional natural en consola, simulando un chat tipo ChatGPT con feedback visual claro.

**Características:**

| Característica | Implementación |
|---|---|
| **Colores por rol** | Asistente (cyan/borde cyan), Usuario (verde/borde verde), Errores (rojo) |
| **Efecto "escribiendo..."** | `_escribir_con_delay()` con `Live()` de Rich + delay por carácter + delay mínimo por mensaje |
| **Paneles diferenciados** | Usa `Panel` + `Markdown` para mensajes formateados (listas, negritas, citas) |
| **Resumen de contexto** | `mostrar_resumen_hechos()` con iconos (✅/❌/❓) por hecho |
| **Gestión incertidumbre** | `preguntar_con_explicacion()` muestra explicación breve + sugerencia de `no_sabe` |
| **UX pulida** | `mostrar_pensando()` (spinner), `console.clear()` en bienvenida, espaciados para legibilidad |

**Métodos públicos:**

- `mostrar_bienvenida()`, `mostrar_ayuda()`, `mostrar_adios()`
- `pedir_descripcion()` → descripción abierta inicial
- `preguntar(texto, opciones)` → pregunta cerrada con sugerencias
- `preguntar_con_explicacion(texto, explicacion_breve, opciones)` → pregunta con ayuda ante término técnico
- `mostrar_resumen_hechos(hechos)`, `mostrar_diagnostico(...)`, `mostrar_info_incertidumbre(...)`
- `preguntar_continuar()`, `mostrar_mensaje()`, `mostrar_error()`

### 3. `explicacion.py` - Explicador en Lenguaje Natural

Clase principal: `ExplicadorNatural`

**Propósito**: Genera explicaciones conversacionales del razonamiento del motor (no imprime texto plano). Hace el diagnóstico interpretable y transparente.

**Método `explicar(estado: Dict, accion: Dict = None) -> str`** genera un informe estructurado con:

1. **Descripción inicial** - Lo que el usuario planteó
2. **Etapa y nodo actual** - Estado del grafo (`etapa`, `nodo_actual`)
3. **Hechos inferidos/confirmados** - Listado clave→valor con trazabilidad
4. **Camino de sondeo** - Secuencia de nodos visitados (`nodos_visitados`) mostrando el razonamiento paso a paso
5. **Confianza e incertidumbre** - `% certeza` + lista de puntos con `no_sabe` (explicando cómo afectaron)
6. **Conclusión** - Justificación natural del diagnóstico orientativo (o por qué sigue sondeando)

Este módulo cumple el requisito **Manejo de Incertidumbre y Explicación (4)**: transforma estado interno a lenguaje natural comprensible.

### 4. `main.py` - Orquestador

**Propósito**: Punto de entrada y coordinador del flujo. Conecta interfaz ↔ motor ↔ explicador, gestionando el bucle conversacional y comandos globales.

**Lógica principal:**

```text
1. Inicializar InterfazConsolaChat, MotorConversacionalGrafo, ExplicadorNatural
2. Mostrar bienvenida
3. Bucle principal (sesión):
   - Limpiar motor
   - Pedir descripción abierta (inicio)
   - Procesar comandos (salir/reiniciar/ayuda)
   - Extraer hechos → mostrar resumen
   - Bucle interno (sondeo diagnóstico):
     - Obtener siguiente_accion() (máquina de estados)
     - Según tipo: pedir_descripcion | preguntar | diagnostico
       - preguntar: puede usar explicación breve si requiere_exp
       - diagnostico: mostrar diagnóstico + explicación razonamiento + preguntar continuar
     - Procesar respuesta/comando
   - Si reiniciar → vuelve a (3), si salir → termina
```

**Manejo de comandos**: Normaliza (`salir/q/exit/fin`, `reiniciar/r/reset`, `ayuda/h/help`). Los comandos son globales y pueden invocarse en cualquier momento.

### 5. `conocimiento/reglas.json` - Base de Conocimiento (Grafo)

Ver sección [Base de Conocimiento](#base-de-conocimiento-grafo-de-decisión) detallada más abajo.

### 6. `tests/test_reglas.py` - Tests

Tests unitarios básicos para el motor. El fichero testea API histórica (`MotorReglas`) con métodos: `base_conocimiento`, `limpiar_hechos()`, `establecer_hecho()`, `inferir()`, `hay_preguntas_faltantes()`, `siguiente_pregunta()`.

> **Nota de compatibilidad**: Con el refactor a `MotorConversacionalGrafo` (API por grafo/estados), los tests existentes son para el motor clásico. Se recomienda mantener compatibilidad hacia atrás con un adaptador wrapper o actualizar tests a la nueva arquitectura. Ambos enfoques son válidos; el nuevo diseño prioriza testabilidad del grafo y flujos conversacionales.

## Base de Conocimiento (Grafo de Decisión)

El sistema utiliza un **grafo dirigido de nodos** (`nodos`) en lugar de una lista plana de reglas. Esto permite modelar el diagnóstico como un árbol/flujo conversacional con ramas dinámicas.

### Estructura de `reglas.json`

```json
{
  "metadata": { ... },
  "patrones": {
    "extraccion": { "<hecho>": ["patrón1", "patrón2", ...] }
  },
  "nodos": {
    "<nodo_id>": { ... propiedades del nodo ... }
  }
}
```

### Propiedades por nodo

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `id` | `string` | Sí | Identificador único del nodo |
| `tipo` | `string` | Opcional | Clasificación: `sondeo_abierto`, `clasificacion`, `sondeo`, `final` |
| `es_final` | `boolean` | Recomendado (finales) | `true` si es nodo diagnóstico final |
| `pregunta_sugerida` | `string` | Sí (no finales) | Pregunta a realizar al usuario (natural, conversacional) |
| `opciones_respuesta` | `string[]` | Opcional | Sugerencias: `["si","no","no_sabe"]` o `["describir"]` |
| `clave_hecho` | `string` | Opcional | Clave de hecho a registrar al responder (`enciende`, `tiene_imagen`, ...) |
| `siguiente_nodo_si_si` | `string` | Opcional | Nodo destino si respuesta = `si` |
| `siguiente_nodo_si_no` | `string` | Opcional | Nodo destino si respuesta = `no` |
| `siguiente_nodo_si_no_sabe` | `string` | Opcional | Nodo destino si respuesta = `no_sabe` (gestión incertidumbre) |
| `siguiente_nodo` | `string` | Opcional | Transición por defecto (fallback) |
| `diagnostico_final` | `string` | Sí (finales) | Título/etiqueta del diagnóstico orientativo |
| `pasos_solucion` | `string[]` | Sí (finales) | Pasos prácticos ordenados a seguir |
| `alternativas_sugeridas` | `string[]` | Opcional | Comprobaciones extra o alternativas ante incertidumbre |
| `explicacion_natural` | `string` | Opcional | Explicación conversacional del diagnóstico (lenguaje natural) |
| `explicacion_breve` | `string` | Opcional | Explicación breve para usuario que responde `no_sabe` |
| `requiere_explicacion` | `boolean` | Opcional | Si `true`, muestra `explicacion_breve` al preguntar |
| `peso` | `number` (0-1) | Opcional | Peso/confianza del nodo/rama (usado para razonamiento) |

### Rutas de Diagnóstico (≥3 implementadas)

El grafo actual cubre **3 rutas principales + adicionales**:

| Ruta | Nodos clave | Diagnóstico final |
|---|---|---|
| **1. PC no enciende** | `clasificar_problema` (no) → `no_enciende_base` → `no_enciende_sin_signos`/`con_signos` | `dx_no_enciende_sin_vida`, `dx_no_enciende_parcial_vida`, `dx_alimentacion_inestable` |
| **2. Enciende pero pantalla negra** | `clasificar_problema` (si) → `enciende_parcial` (no imagen) → `sin_imagen_rama` (logo sí/no) | `dx_sin_imagen_con_vida`, `dx_sin_imagen_pasa_post`, `dx_sin_imagen_no_pasa_post` |
| **3. PC va lenta** | `clasificar_problema` (si) → `tiene_imagen` (si) → `tiene_imagen_rama` (llega SO sí) → `llega_so_rama` (lento sí) | `dx_lento` |
| **4. BSOD** | Llega a SO no + aparece BSOD sí | `dx_bsod` |
| **5. No carga SO (queda logo)** | Llega a SO no + BSOD no | `dx_queda_logo_sin_cargar_so` |
| **6. Estable con síntomas confusos** | Llega SO sí + no lento → rama otros síntomas | `dx_general_estable` |

### Extracción de Hechos (Patrones)

El campo `patrones.extraccion` permite inferencia inicial desde descripción abierta. Además, `motor.py` aplica tabla de inferencias (sin ifs anidados) con reglas como:

- `no_enciende`/`no prende`/`no arranca` → `enciende = "no"`
- `enciende` (positivo) → `enciende = "si"`
- `pantalla negra`/`sin imagen` → `tiene_imagen = "no"`
- `se queda en logo`/`queda en bios` → `se_ve_logo_bios = "si"`
- `pantalla azul`/`bsod` → `aparece_bsod = "si"`
- `va lento` → `lento = "si"`, etc.

## Flujo de Conversación

```text
Usuario abre app
  ↓
[Bienvenida] Interfaz muestra info + comandos
  ↓
Motor: etapa=INICIO → acción pedir_descripcion
  ↓
Usuario: describe problema (ABIERTO)
  ↓
Motor: establecer_descripcion() 
  → extrae hechos (patrones + inferencias)
  → actualiza certeza
  → etapa=SONDEANDO, nodo_actual=clasificar_problema (o inicio)
  ↓
Interfaz: muestra resumen_hechos()
  ↓
Bucle SONDEANDO:
  - Motor.siguiente_accion(): busca nodo con pregunta_sugerida no hecha
    - Si nodo es FINAL → acción DIAGNOSTICO
    - Si tiene clave_hecho con valor conocido → avanza por grafo (deducción)
    - Else → acción PREGUNTAR (nodo)
  - Si PREGUNTAR:
      → Interfaz.preguntar() (o con explicación breve si requiere_exp)
      → Usuario responde: si/no/no_sabe/describir/comando
      → Comandos: salir/reiniciar/ayuda (gestionados)
      → Motor.responder_pregunta(r): establece hecho, actualiza incertidumbre, avanza grafo (_siguiente_por_grafo)
      → Interfaz.mostrar_resumen_hechos()
      → Vuelve a bucle
  - Si DIAGNOSTICO (nodo es_final):
      → Interfaz.mostrar_diagnostico() (diagnóstico + pasos + alternativas + certeza + incertidumbre + explicación natural)
      → ExplicadorNatural.explicar() → Interfaz.mostrar_mensaje() (razonamiento completo)
      → Interfaz.preguntar_continuar()
      → Usuario: seguir/describir/reiniciar/salir
        - describir → mot.establecer_descripcion(op) (retroalimentación, continúa sondeo)
        - seguir → sugiere pasos, pide feedback ("probé paso X...")
        - reiniciar → rompe bucle interno → nueva sesión
        - salir → termina
```

## Características Clave

| Característica | Descripción | Ubicación |
|---|---|---|
| **Máquina de Estados** | Etapas `inicio/sondeando/diagnosticado`. Transiciones controladas, sin estados implícitos. | `motor.py::siguiente_accion()` |
| **Grafo Dinámico** | Navegación por aristas `si/no/no_sabe` (NetworkX o fallback dict). Transiciones declarativas. | `motor.py::_cargar_grafo()`, `_siguiente_por_grafo()` |
| **Sin Ifs Anidados** | El razonamiento usa grafo + tabla de inferencias (lista de lambdas/reglas) en lugar de `if/elif` encadenados. | `motor.py` (diseño central) |
| **Contexto Persistente** | Acumula hechos, nodos visitados, incertidumbres, preguntas hechas durante toda la conversación. | `estado` dict |
| **Abierto → Cerrado** | Inicio conversacional abierto (`pedir_descripcion`) → sondeo progresivo con preguntas cerradas por nodo. | Flujo `main.py` + nodos KB |
| **Gestión de Incertidumbre** | Respuesta `no_sabe`: registra incertidumbre, muestra `explicacion_breve`, sugiere alternativas, continúa flujo (no bloquea). | `motor.py`, `interfaz.py`, KB nodos |
| **Certeza Probabilística** | Calcula `certeza = ciertos/(total_hechos)` donde ciertos = `si/no` (vs `no_sabe`). Visible en diagnóstico y explicación. | `motor.py::_actualizar_certeza()` |
| **Explicación Natural** | Genera razonamiento conversacional (camino, hechos, certeza, incertidumbre, justificación). No texto plano. | `explicacion.py::ExplicadorNatural.explicar()` |
| **Retroalimentación** | Usuario puede describir lo probado tras diagnóstico → motor re-procesa descripción y continúa/ajusta sondeo. | `main.py` (rama `diagnostico` → `describir`) |
| **Determinista** | Misma secuencia de hechos → mismas transiciones (grafo explícito). Ideal para testeo. | Diseño global |
| **Modular** | 4 capas desacopladas (UI/Motor/Explicación/KB). Fácil mantenimiento/extensión. | Estructura proyecto |

## Tecnologías y Dependencias

### Dependencias de producción

| Librería | Versión mínima | Uso | Obligatoria |
|---|---|---|---|
| [`rich`](https://github.com/Textualize/rich) | `>=13.0.0` | UI consola: paneles, Markdown, Live (typing), spinner, colores | **Sí** |
| [`networkx`](https://networkx.org/) | `>=3.0` | Modelado explícito de grafo dirigido (DiGraph), navegación por aristas, trazabilidad. | **Opcional** (tiene fallback a dict puro) |

> **Nota**: Sin `networkx`, el sistema funciona igualmente (usa lógica dict en `_siguiente_por_grafo()`). `networkx` facilita visualizar, extender y validar el grafo, pero no es imprescindible.

### Entorno

- **Python**: `>=3.10` (recomendado 3.11+)
- **Plataforma**: Multiplataforma (Windows/Linux/macOS). Probado en entorno `win32`.
- **Dependencias externas**: Ninguna (100% local, sin APIs).

### Instalación dependencias

```bash
pip install rich networkx
```

O solo Rich:

```bash
pip install rich
```

## Instalación y Uso

### 1. Clonar/ubicarse en el directorio

```bash
cd "D:\Mis Documentos\UMA\Ciclo 10\Inteligencia Artificial\Sistema Experto"
```

### 2. Instalar dependencias (recomendado)

```bash
pip install rich networkx
```

### 3. Ejecutar el sistema

```bash
python main.py
```

### 4. Comandos disponibles durante la conversación

| Comando | Alternativas | Acción |
|---|---|---|
| `salir` | `q`, `exit`, `fin` | Finaliza la conversación con despedida |
| `reiniciar` | `r`, `reset` | Reinicia diagnóstico desde cero (nueva sesión) |
| `ayuda` | `h`, `help` | Muestra ayuda con respuestas válidas y consejos |

### 5. Formatos de respuesta aceptados

**Preguntas cerradas (si/no/no_sabe):**

- Afirmativo: `si`, `sí`, `s`, `y`, `yes`, `true`, `1`
- Negativo: `no`, `n`, `false`, `0`
- Incertidumbre: `no_sabe`, `ns`, `nose`, `no se`, `no sé`, `desconozco`

**Preguntas abiertas**: Lenguaje natural libre ("El equipo hace un clic y no enciende...", "Empezó después de una actualización...").

### Ejemplo de flujo (resumido)

```text
[Asistente] Cuéntame qué pasa con tu PC o portátil...
[Tú] Mi PC no enciende, no hay luces
[Asistente] ¿Se encienden algún LED (alimentación) al intentar encenderlo?
[Tú] no
[Asistente] ¿Gira el ventilador al intentar encenderlo?
[Tú] no
[Asistente] DIAGNÓSTICO ORIENTATIVO: PC NO ENCIENDE - Sin signos de vida...
  → Pasos, alternativas, certeza, explicación razonamiento
[Asistente] ¿Quieres seguir guiándote o contarme qué has probado?
```

## Testing

### Estructura de tests

```text
tests/
└── test_reglas.py  # Tests unitarios (API MotorReglas clásico)
```

### Ejecutar tests

Con `unittest`:

```bash
python -m unittest tests.test_reglas -v
```

Con `pytest`:

```bash
python -m pytest tests/ -v
```

### Cobertura de tests (actual)

Los tests existentes validan:

- Carga de base de conocimiento (`test_carga_kb`)
- Inferencia sin hechos (`test_inferir_sin_hechos`)
- Regla R01: no enciende sin alimentación (`test_regla_no_enciende_sin_alimentacion`)
- Sin imagen tras encender (R04/R12) (`test_sin_imagen_tras_encender`)
- Problema WiFi (R10) (`test_wifi_problema`)
- Siguiente pregunta existe (`test_siguiente_pregunta_existe`)

### Recomendación para tests del nuevo motor

Para cubrir la nueva arquitectura (grafo+estados), se recomienda añadir tests específicos:

```python
# Sugerido: tests/test_motor_grafo.py
- test_transicion_si_no_no_sabe()
- test_contexto_persistente_hechos()
- test_gestion_incertidumbre_no_sabe()
- test_nodos_visitados_camino()
- test_diagnostico_nodo_final()
- test_extraccion_descripcion_abierta()
- test_certeza_calculo()
- test_retroalimentacion_descripcion_despues_diagnostico()
```

## Extensibilidad

El diseño declarativo facilita añadir nuevos casos sin modificar lógica Python.

### Añadir nuevo síntoma/ruta

1. **Añadir patrones** (opcional, para inferencia desde descripción abierta): `patrones.extraccion.<nuevo_hecho>` con lista de términos.
2. **Crear nodos** en `conocimiento/reglas.json`:
   - Nodo sondeo: con `pregunta_sugerida`, `clave_hecho`, transiciones `siguiente_nodo_si_si/no/no_sabe`
   - Nodo final: con `es_final: true`, `diagnostico_final`, `pasos_solucion`, `alternativas_sugeridas`, `explicacion_natural`
3. **Conectar al grafo**: enlazar desde nodo existente (p.ej. `otros_problemas_rama` o crear rama nueva).
4. **Validar**: ejecutar `python main.py` y probar flujo. No requiere tocar `motor.py`, `interfaz.py` ni `explicacion.py`.

### Buenas prácticas al extender

- Usar IDs descriptivos (`dx_<causa>`, `rama_<categoria>`)
- Siempre proporcionar `siguiente_nodo_si_no_sabe` para gestionar incertidumbre
- Incluir `explicacion_breve` + `requiere_explicacion` si el término puede ser desconocido
- Nodo final debe tener `pasos_solucion` ordenados, concisos y seguros
- Añadir `alternativas_sugeridas` ante posibles incertidumbres
- Mantener `peso` coherente para trazabilidad

## Licencia y Alcance

**Alcance**: Sistema de diagnóstico orientativo para **troubleshooting básico** de hardware/software (PCs/portátiles). No sustituye a diagnóstico profesional.

**Limitaciones conocidas**:

- Enfoque determinista basado en reglas (no cubre todos los casos posibles)
- Requiere que el usuario pueda describir síntomas o responder preguntas (o usar `no_sabe`)
- Diagnóstico **orientativo**, no concluyente. Siempre incluye recomendación de derivar a técnico ante casos críticos (ruidos mecánicos, hardware, etc.)

**Principios de seguridad**: Código local, sin logging de secretos, sin llamadas externas, modular y explicable.

---

**Versión del proyecto**: 3.0.0 (Grafo de Conocimiento Conversacional)  
**Arquitectura**: Máquina de Estados + Grafo Dirigido + Interfaz Chat Rich  
**Filosofía**: Explicable • Determinista • Local • Conversacional • Modular • Centrado en Usuario