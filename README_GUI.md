# FASE 1 — Interfaz Gráfica de Escritorio (GUI)

Sustitución de la consola (`Rich`) por una **ventana de escritorio** construida con
[CustomTkinter](https://customtkinter.tomschimansky.com/). El sistema experto **no se ha
reescrito**: la GUI consume el motor, la base de conocimiento y el explicador tal cual.

> **Actualización (bis de la fase 1)** — Se corrigió un bug crítico por el que **escribir
> texto y pulsar `Enter` (o *Enviar*) no hacía nada**, y se rediseñó la interfaz con un
> estilo moderno minimalista en **grises + verde** (tema claro). Ver
> [sección 6.1](#61-corrección-del-envío-de-texto-libre-bug-de-ctkentry) y
> [sección 6.2](#62-nueva-paleta-grises--verde).

---

## 1. Requisitos e instalación

| Requisito | Versión | Notas |
|---|---|---|
| Python | >= 3.9 (probado en 3.12) | |
| CustomTkinter | >= 5.2 | Única dependencia nueva de esta fase |

```bash
pip install customtkinter
```

> `main.py` **intenta instalar CustomTkinter automáticamente** si no lo encuentra (`pip install customtkinter`).
> Si la instalación automática falla, se muestra un cuadro de diálogo de error indicando el
> comando exacto a ejecutar. Para desactivar el autoinstalador:
> `set SE_GUIA_SIN_AUTOINSTALAR=1` (Windows) / `export SE_GUIA_SIN_AUTOINSTALAR=1` (Linux/macOS).

CustomTkinter arrastra `tkinter` y `darkdetect` como dependencias (ya incluidas en Python).

---

## 2. Ejecución

```bash
cd "D:\Mis Documentos\UMA\Ciclo 10\Inteligencia Artificial\Sistema Experto"
python main.py
```

Se abre la ventana **"Asistente de Soporte Técnico"** con dos pantallas:

1. **Pantalla de inicio**: título, subtítulo y 5 tarjetas grandes de diagnóstico (botón
   verde + descripción), en tema claro grises/verde.
2. **Pantalla de chat**: cabecera blanca con *Reiniciar*, burbujas (asistente gris a la
   izquierda, usuario verde a la derecha), respuestas rápidas, resumen de datos confirmados,
   campo de texto (Enter para enviar) y botón *Enviar*.

---

## 3. Flujo de usuario

```text
python main.py
   └─> Pantalla INICIO
        ├─ [No enciende]   ─┐
        ├─ [Pantalla negra]  │
        ├─ [Va lento]        ├─> Pantalla CHAT: saludo + primera pregunta del grafo
        ├─ [WiFi]            │      └─> boton de respuesta rapida (Si / No / No estoy seguro)
        └─ [Otro]          ─┘          o campo de texto (preguntas abiertas)
                                            └─> el motor avanza por el grafo
                                                 └─> DIAGNOSTICO + pasos + "Ver razonamiento"
```

Ejemplo real (botón *No enciende*):

> **Asistente:** Vaya, lo siento. Vamos a ver qué pasa. ¿Ves alguna luz encendida en la torre o el cargador?
> `[Sí] [No] [No estoy seguro]`

Los botones de respuesta rápida dependen de la pregunta que devuelve el grafo:

| Pregunta | Opciones ofrecidas |
|---|---|
| Preguntas `si` / `no` / `no_sabe` | `Sí` · `No` · `No estoy seguro` |
| `es_laptop` | `Sí, es un portátil` · `No, es un PC de escritorio` · `No estoy seguro` |
| `es_hdd_o_ssd` | `Es un SSD` · `Es un HDD` · `No estoy seguro` |
| `tipo_ruido` | `Clics` · `Zumbido` · `Chirrido` · `No estoy seguro` |
| `codigo_error`, `error_conexion` | campo de texto libre |

Siempre se puede **escribir** la respuesta aunque haya botones (el texto libre se analiza
con los patrones de `reglas.json`).

---

## 4. Archivos de esta fase

| Archivo | Estado | Descripción |
|---|---|---|
| `gui.py` | **NUEVO** | Clase `ChatApp(ctk.CTk)`: pantalla de inicio + chat con burbujas, respuestas rápidas, resumen de datos y tarjeta de diagnóstico. |
| `main.py` | **MODIFICADO** | Ya no importa `interfaz.py`. Comprueba/instala dependencias, carga el motor y abre la ventana. |
| `motor.py` | **MODIFICADO (mínimo)** | Solo se *añade* API para la GUI. La lógica del grafo y `reglas.json` no se tocan. |
| `conocimiento/reglas.json` | Intacto | Base de conocimiento (grafo). |
| `explicacion.py` | Intacto | Se usa para el botón *Ver razonamiento*. |
| `interfaz.py` | Intacto (fuera de juego) | Interfaz de consola; queda como referencia/documentación. |

### 4.1 Qué se añadió a `motor.py` (sin tocar la lógica del grafo)

| Método nuevo | Para qué lo usa la GUI |
|---|---|
| `responder_pregunta(pregunta_id, respuesta, modo="cerrado"\|"libre")` | Registra la respuesta del usuario. `modo="cerrado"` → valor de dominio (`si`/`no`/`no_sabe`/`ssd`...). `modo="libre"` → texto del usuario: se guarda el hecho **y** se analiza con los patrones. |
| `obtener_estado_resumen()` | Snapshot del estado (etapa, hechos, sospechas, hipótesis, preguntas hechas) para la barra de "Datos confirmados". |
| `registrar_texto_libre(texto)` | Analiza texto libre con los patrones **sin** sobrescribir la descripción inicial de la sesión. |
| `siguiente_accion()` → rama `preguntar_minima` | Cambio de comportamiento: ahora devuelve **una** mínima por vez y la marca como hecha (antes se repetía la misma pregunta en bucle infinito). Si se agotan las 4, devuelve `{"tipo": "sin_informacion"}`. |

El resto del motor (`_actualizar_sospechas`, `siguiente_accion`, `_texto_pregunta`, …) es
**idéntico** a la versión anterior.

---

## 5. Arquitectura resultante

```text
Usuario (ventana)
      ↓
GUI (gui.py - CustomTkinter)   ── after() / callbacks de Tk (nunca bloquea la interfaz)
      ↓
Motor (motor.py - grafo + máquina de estados)
      ↕
Base de conocimiento (conocimiento/reglas.json)
      ↓
Explicador (explicacion.py)  →  botón "Ver razonamiento"
```

La GUI **no decide nada**: pide la siguiente acción a `motor.siguiente_accion()` y la
presenta. Las respuestas se devuelven con `motor.responder_pregunta(...)`.

---

## 6. Detalles de implementación relevantes

- **No se congela la ventana**: la llamada al motor se hace dentro de `self.after(...)`,
  de modo que el bucle de eventos de Tk sigue vivo (indicador "Escribiendo..." entre
  mensaje y mensaje).
- **Burbujas**: `CTkScrollableFrame` + `CTkLabel`; asistente alineado a la izquierda
  (columna 0 con peso 1) y usuario a la derecha (columna 1). El ancho de línea se
  recalcula en `<Configure>`.
- **Scroll automático** al final del chat tras cada mensaje.
- **Reiniciar** (cabecera o tarjeta de diagnóstico) limpia el motor (`motor.limpiar()`),
  vacía el chat y vuelve a la pantalla de inicio.
- **Atajos**: `Enter` envía el mensaje escrito (tanto en el campo como con el foco en otro
  widget de la ventana).
- **Errores claros**: si falta `conocimiento/reglas.json` o CustomTkinter, se muestra un
  `MessageBox` con el detalle y el proceso termina con código de error.

---

## 6.1 Corrección del envío de texto libre (bug de CTkEntry)

**Síntoma**: se escribía el texto y ni `Enter` ni el botón *Enviar* hacían nada.

**Causa raíz** (CustomTkinter 5.2.2): el *placeholder* de `CTkEntry` **se inserta dentro**
del `Entry` interno y, mientras está activo (`_placeholder_text_active`), `CTkEntry.get()`
devuelve `""` aunque haya texto escrito. Además, la GUI reconfiguraba el placeholder en
caliente (`configure(placeholder_text=...)`) **después** de `focus_set()`: como el widget ya
tenía el foco, no llegaba ningún `<FocusIn>` que lo desactivara, el placeholder se
reinsertaba y el `get()` seguía devolviendo cadena vacía → `_on_enviar()` retornaba antes de
enviar.

```text
antes:  estado tras abrir el chat -> {'placeholder_activo': True,
                                     'contenido_entry': 'O escribe tu respuesta aquí...',
                                     'get()': ''}
        tras teclear             -> 'O escribe tu respuesta aquí...es un portatil'
                                     get() == ''   ->  no se enviaba nada
```

**Solución**: el campo de entrada pasa a ser un **`CTkTextbox`**, que no tiene *placeholder*
y cuyo `get("1.0", "end-1c")` devuelve siempre el texto real:

| Antes (`CTkEntry`) | Ahora (`CTkTextbox`) |
|---|---|
| `configure(placeholder_text=...)` en cada pregunta | Sin placeholder: la pista se muestra en una etiqueta aparte (`label_pista`) |
| `get()` → `""` mientras el placeholder está activo | `get("1.0", "end-1c")` → texto real siempre |
| `delete(0, "end")` | `delete("1.0", "end")` |
| `state="disabled"` para bloquear | Nunca se deshabilita; `_asegurar_entrada_activa()` lo garantiza |

Además:

- `Enter` → `_on_enter()` → devuelve `"break"` (no inserta salto de línea) y llama a
  `_on_enviar()`.
- `Enter` también funciona **con el foco fuera del campo**: la ventana (`self`) tiene
  `<Return>` y `<KP_Enter>` registrados.
- El botón *Enviar* usa exactamente el mismo camino (`_on_enviar`), sin duplicados.
- Si el texto está vacío no se envía nada ni se cambia el foco de un botón pulsado.

---

## 6.2 Nueva paleta (grises + verde)

| Constante | Valor | Uso |
|---|---|---|
| `COLOR_FONDO` | `#F5F5F5` | Fondo de la aplicación |
| `COLOR_SUPERFICIE` | `#FFFFFF` | Tarjetas, cabecera y campo de entrada |
| `COLOR_BURBUJA_ASISTENTE` | `#E0E0E0` | Burbujas del asistente |
| `COLOR_BURBUJA_USUARIO` | `#4CAF50` | Burbujas del usuario |
| `COLOR_TEXTO_ASISTENTE` | `#212121` | Texto del asistente |
| `COLOR_TEXTO_USUARIO` | `#FFFFFF` | Texto del usuario |
| `COLOR_BOTON` | `#4CAF50` | Botón principal (Enviar, categorías, reiniciar diagnóstico) |
| `COLOR_BOTON_HOVER` | `#45A049` | *Hover* del botón principal |
| `COLOR_TEXTO_SUAVE` | `#70757F` | Subtítulos, metadatos y razonamiento |
| `COLOR_BORDE` / `COLOR_BORDE_FUERTE` | `#E3E5E8` / `#D5D8DD` | Bordes y separadores |
| `COLOR_OPCION` / `COLOR_OPCION_HOVER` | `#FFFFFF` / `#E9EBEE` | Respuestas rápidas |
| `COLOR_OK` | `#2E7D32` | Título de la tarjeta de diagnóstico |

Tema claro (`ctk.set_appearance_mode("light")`). Detalles de estilo: tarjeta de diagnóstico
blanca con borde y título verde, respuestas rápidas en blanco con borde redondeado de 18 px,
el borde del campo de entrada se pone **verde al ganar el foco**, separador de 1 px bajo la
cabecera y contenedor de altura fija (46 px) para que el campo y el botón *Enviar* queden
alineados.

---

## 7. Problema conocido (preexistente, no de esta fase)

`tests/test_reglas.py` sigue importando `MotorReglas`, una clase que **no existe** en la
versión actual de `motor.py` (ya estaba roto antes de esta fase):

```bash
python -m unittest discover -s tests
# ImportError: cannot import name 'MotorReglas' from 'motor'
```

No se ha tocado en esta fase porque exige reescribir el motor, que es justo lo que la
fase 1 prohíbe. Pendiente para una fase posterior: adaptar los tests a `MotorConversacional`
(`establecer_descripcion` / `responder_pregunta` / `siguiente_accion` / `obtener_estado_resumen`).

---

## 8. Verificación realizada

- Las **5 categorías** llegan hasta el diagnóstico final (`siguiente_accion()` → `diagnostico`).
- Flujo de *No enciende* verificado mensaje a mensaje, con los botones `Sí` / `No` /
  `No estoy seguro`.
- Preguntas abiertas respondidas por texto libre: el texto se guarda como hecho y se
  extraen síntomas (`pantalla azul` → hipótesis `H_BSOD`).
- Categoría *Otro*: descripción libre → hipótesis detectada por patrones.
- Diagnosis: título, explicación, pasos numerados, botón *Ver razonamiento* y
  *Reiniciar diagnóstico*.
- `python main.py` opens the window with the correct title.

### 8.1 Verificación del bis (fix de envío + rediseño)

- **Teclado real** (`event_generate` carácter a carácter + `<KeyPress>` Return): el texto
  llega al motor, aparece la burbuja del usuario, el campo se limpia y **no se duplica** el
  envío.
- **Ratón real** (`<Button-1>` sobre el canvas del botón): *Enviar* envía exactamente una vez.
- `Enter` **con el foco fuera del campo** → envía (binding de la ventana).
- Envío en blanco → no ocurre nada y el foco no se roba de un botón.
- El campo sigue siendo escribible después de varios envíos.
- Layout comprobado por geometría: cabecera 62 px + separador de 1 px, campo de texto y
  botón *Enviar* con la misma altura (46 px) y alineados, burbujas dentro de la ventana.
- Colores comprobados contra la paleta de la [sección 6.2](#62-nueva-paleta-grises--verde).
- Las 5 categorías siguen llegando al diagnóstico final.
