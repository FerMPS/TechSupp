# motor.py
# Motor conversacional para sistema experto de soporte técnico

import json
import os
from typing import Dict, List, Any


class MotorConversacional:
    """
    Motor conversacional: recibe descripción en lenguaje natural,
    extrae síntomas, genera hipótesis, hace preguntas mínimas
    y propone diagnóstico con pasos de resolución.

    La GUI (gui.py) consume este motor mediante:
        - establecer_descripcion(texto)
        - responder_pregunta(pregunta_id, respuesta, modo)
        - siguiente_accion()
        - obtener_estado_resumen()
    """

    def __init__(self, ruta_kb: str = "conocimiento/reglas.json"):
        self.ruta_kb = ruta_kb
        self.kb: Dict[str, Any] = {}
        self.estado: Dict[str, Any] = {
            "descripcion": "",
            "notas": [],
            "hechos": {},  # clave -> valor (si/no/no_sabe)
            "sospechas": [],
            "hipotesis_activa": None,
            "preguntas_hechas": [],
            "etapa": "inicio",  # inicio | recopilando | diagnosticado
        }
        self.cargar()

    def cargar(self) -> None:
        if not os.path.exists(self.ruta_kb):
            raise FileNotFoundError(f"No existe {self.ruta_kb}")
        with open(self.ruta_kb, "r", encoding="utf-8") as f:
            self.kb = json.load(f)

    def limpiar(self) -> None:
        self.estado = {
            "descripcion": "",
            "notas": [],
            "hechos": {},
            "sospechas": [],
            "hipotesis_activa": None,
            "preguntas_hechas": [],
            "etapa": "inicio",
        }

    # ------------------------------------------------------------------
    # API de compatibilidad con la interfaz gráfica
    # ------------------------------------------------------------------

    def obtener_estado_resumen(self) -> Dict[str, Any]:
        """Devuelve una copia compacta del estado actual (para la GUI)."""
        return {
            "descripcion": self.estado.get("descripcion", ""),
            "notas": list(self.estado.get("notas", [])),
            "hechos": dict(self.estado.get("hechos", {})),
            "sospechas": list(self.estado.get("sospechas", [])),
            "hipotesis_activa": self.estado.get("hipotesis_activa"),
            "preguntas_hechas": list(self.estado.get("preguntas_hechas", [])),
            "etapa": self.estado.get("etapa", "inicio"),
        }

    def responder_pregunta(
        self,
        pregunta_id: str,
        respuesta: str,
        modo: str = "cerrado",
    ) -> Dict[str, Any]:
        """
        Registra la respuesta del usuario a una pregunta del grafo.

        modo="cerrado": la respuesta es un valor de dominio (si / no / no_sabe /
                        ssd / hdd / clics...). Se guarda como hecho.
        modo="libre":   la respuesta es texto del usuario. Se guarda como hecho
                        y además se analiza con los patrones de la base de
                        conocimiento para extraer síntomas adicionales.
        """
        texto = (respuesta or "").strip()
        if not texto:
            return self.obtener_estado_resumen()

        v = self._normalizar(texto)

        if v in ("si", "s", "yes", "y"):
            self.establecer_hecho(pregunta_id, "si")
        elif v in ("no", "n"):
            self.establecer_hecho(pregunta_id, "no")
        elif v in ("no_sabe", "ns", "nose", "no se", "no estoy seguro", "desconozco"):
            self.establecer_hecho(pregunta_id, "no_sabe")
        elif modo == "libre":
            self.establecer_hecho(pregunta_id, texto)
            self.registrar_texto_libre(texto)
        else:
            self.establecer_hecho(pregunta_id, texto)

        # Regla de dominio: si no es portátil, es PC de escritorio.
        if pregunta_id == "es_laptop":
            if self.estado["hechos"].get("es_laptop") == "no":
                self.establecer_hecho("es_pc", "si")
            elif self.estado["hechos"].get("es_laptop") == "si":
                self.estado["hechos"].pop("es_pc", None)

        return self.obtener_estado_resumen()

    def registrar_texto_libre(self, texto: str) -> None:
        """
        Analiza texto libre del usuario con los patrones de la base de
        conocimiento SIN sobrescribir la descripción inicial de la sesión.
        """
        if not texto:
            return
        self.estado.setdefault("notas", []).append(texto)
        self._extraer_de_texto(texto)

    # ------------------------------------------------------------------
    # Lógica de grafo (no modificar: aquí manda reglas.json)
    # ------------------------------------------------------------------

    def _normalizar(self, t: str) -> str:
        if not t:
            return ""
        t = t.lower().strip()
        reemplazos = {
            "á": "a",
            "é": "e",
            "í": "i",
            "ó": "o",
            "ú": "u",
            "ü": "u",
            "ñ": "n",
            "¿": "",
            "?": "",
            "¡": "",
            "!": "",
            ",": " ",
            ".": " ",
            ";": " ",
        }
        for k, v in reemplazos.items():
            t = t.replace(k, v)
        t = " ".join(t.split())
        return t

    def establecer_descripcion(self, texto: str) -> None:
        self.estado["descripcion"] = texto or ""
        self._extraer_de_texto(texto or "")

    def establecer_hecho(self, clave: str, valor: str) -> None:
        v = self._normalizar(valor)
        if v in ("si", "s", "sí", "y", "yes"):
            v_norm = "si"
        elif v in ("no", "n"):
            v_norm = "no"
        elif v in ("no_sabe", "ns", "nose", "no se", "desconozco"):
            v_norm = "no_sabe"
        else:
            v_norm = v
        self.estado["hechos"][clave] = v_norm
        self._actualizar_sospechas()

    def _extraer_de_texto(self, texto: str) -> None:
        if not texto:
            return
        t = self._normalizar(texto)
        pats = self.kb.get("patrones", {}) or {}
        hechos = self.estado["hechos"]

        if any(p in t for p in pats.get("tipo_laptop", [])):
            hechos["es_laptop"] = "si"
        if any(p in t for p in pats.get("tipo_pc", [])):
            hechos["es_pc"] = "si"

        no_enciende_match = any(p in t for p in pats.get("no_enciende", []))
        enciende_match = any(p in t for p in pats.get("enciende", []))
        if no_enciende_match:
            hechos["enciende"] = "no"
        elif enciende_match:
            hechos["enciende"] = "si"

        if any(p in t for p in pats.get("sin_luces", [])):
            hechos["encienden_leds"] = "no"
        if any(p in t for p in pats.get("sin_ventilador", [])):
            hechos["gira_ventilador"] = "no"

        queda_logo_match = any(p in t for p in pats.get("queda_logo", []))
        sin_imagen_match = any(p in t for p in pats.get("sin_imagen", []))
        if queda_logo_match:
            hechos["se_ve_logo_bios"] = "si"
            hechos["tiene_imagen"] = "si"
        if sin_imagen_match:
            hechos["tiene_imagen"] = "no"

        if any(p in t for p in pats.get("bsod", [])):
            hechos["aparece_bsod"] = "si"
            hechos["llega_a_so"] = "parcial"

        if any(p in t for p in pats.get("calienta", [])):
            hechos["calienta"] = "si"
        if any(p in t for p in pats.get("ruidos", [])):
            hechos["hay_ruidos"] = "si"
        if any(p in t for p in pats.get("disco", [])):
            hechos["sospecha_disco"] = "si"
        if any(p in t for p in pats.get("lento", [])):
            hechos["lento"] = "si"
        if any(p in t for p in pats.get("wifi", [])):
            hechos["problema_wifi"] = "si"
        if any(p in t for p in pats.get("audio", [])):
            hechos["problema_audio"] = "si"
        if any(p in t for p in pats.get("carga", [])):
            hechos["carga_bateria"] = "no"
        if any(p in t for p in pats.get("conectado", [])):
            hechos["conectado_a_corriente"] = "si"

        self._actualizar_sospechas()

    def _actualizar_sospechas(self) -> None:
        h = self.estado["hechos"]
        sospechas: List[str] = []

        if h.get("aparece_bsod") == "si":
            sospechas.append("H_BSOD")
        if h.get("enciende") == "no":
            sospechas.append("H_NO_ENCIENDE")
        if h.get("hay_ruidos") == "si" and h.get("sospecha_disco") == "si":
            sospechas.append("H_RUIDO_DISCO")
        if h.get("tiene_imagen") == "no" and h.get("enciende") != "no":
            sospechas.append("H_SIN_IMAGEN")
        if h.get("se_ve_logo_bios") == "si" and h.get("llega_a_so") not in ("si",):
            sospechas.append("H_ARRANQUE_SO")
        if h.get("carga_bateria") == "no" and h.get("es_laptop") == "si":
            sospechas.append("H_NO_CARGA")
        if h.get("calienta") == "si":
            sospechas.append("H_CALIENTA")
        if h.get("lento") == "si":
            sospechas.append("H_LENTO")
        if h.get("problema_wifi") == "si":
            sospechas.append("H_WIFI")
        if h.get("problema_audio") == "si":
            sospechas.append("H_AUDIO")

        hip_list = self.kb.get("hipotesis", []) or []
        prio_map = {x["id"]: x.get("prioridad", 0) for x in hip_list}
        unicos: List[str] = []
        vistos = set()
        for s in sospechas:
            if s not in vistos:
                unicos.append(s)
                vistos.add(s)
        unicos.sort(key=lambda k: prio_map.get(k, 0), reverse=True)
        self.estado["sospechas"] = unicos
        if self.estado["sospechas"] and not self.estado.get("hipotesis_activa"):
            self.estado["hipotesis_activa"] = self.estado["sospechas"][0]

    def siguiente_accion(self) -> Dict[str, Any]:
        if self.estado.get("etapa") == "inicio":
            self.estado["etapa"] = "recopilando"
            if self.estado.get("sospechas"):
                if not self.estado.get("hipotesis_activa"):
                    self.estado["hipotesis_activa"] = self.estado["sospechas"][0]
                hip = self.estado["hipotesis_activa"]
                plan_res = self.kb.get("plan_resolucion", {}) or {}
                plan = plan_res.get(hip, {}) if hip else {}
                if plan:
                    for pid in plan.get("preguntar", []):
                        if pid in self.estado.get("preguntas_hechas", []):
                            continue
                        if pid in self.estado.get("hechos", {}):
                            continue
                        self.estado.setdefault("preguntas_hechas", []).append(pid)
                        return {
                            "tipo": "preguntar",
                            "hipotesis": hip,
                            "plan": plan,
                            "pregunta_id": pid,
                            "texto": self._texto_pregunta(pid),
                        }
                    self.estado["etapa"] = "diagnosticado"
                    return {"tipo": "diagnostico", "hipotesis": hip, "plan": plan}
            return {
                "tipo": "pedir_descripcion",
                "texto": "Describe el problema con tus palabras: ¿Qué ocurre exactamente? ¿Cuándo empezó? ¿Qué síntomas notas?",
            }

        if not self.estado.get("hipotesis_activa") and self.estado.get("sospechas"):
            self.estado["hipotesis_activa"] = self.estado["sospechas"][0]

        hip = self.estado.get("hipotesis_activa")
        plan_res = self.kb.get("plan_resolucion", {}) or {}
        plan = plan_res.get(hip, {}) if hip else {}

        if not hip or not plan:
            preguntas_min = [
                {
                    "id": "es_laptop",
                    "texto": "¿Es un portátil (laptop) o un PC de escritorio? (laptop/pc/no_sabe)",
                },
                {
                    "id": "enciende",
                    "texto": "¿Enciende el equipo al pulsar el botón? (si/no/no_sabe)",
                },
                {
                    "id": "tiene_imagen",
                    "texto": "¿Se ve imagen en pantalla? (si/no/no_sabe)",
                },
                {
                    "id": "llega_a_so",
                    "texto": "¿Consigue llegar al escritorio/sistema operativo? (si/no/no_sabe)",
                },
            ]
            # Cada mínima se pregunta una sola vez y en orden: así la GUI
            # (o la consola) puede avanzar en vez de repetir la misma.
            for p in preguntas_min:
                if p["id"] in self.estado.get("hechos", {}):
                    continue
                if p["id"] in self.estado.get("preguntas_hechas", []):
                    continue
                self.estado.setdefault("preguntas_hechas", []).append(p["id"])
                return {
                    "tipo": "preguntar_minima",
                    "preguntas": [p],
                    "pregunta_id": p["id"],
                    "texto": p["texto"],
                }
            return {
                "tipo": "sin_informacion",
                "texto": (
                    "Con los datos que tengo todavía no puedo afinar el diagnóstico. "
                    "Cuéntame algo más (por ejemplo: ¿se queda en el logo? ¿pantalla azul? "
                    "¿hace ruidos el disco? ¿se calienta?) o empieza de nuevo."
                ),
            }

        for pid in plan.get("preguntar", []):
            if pid in self.estado.get("preguntas_hechas", []):
                continue
            if pid in self.estado.get("hechos", {}):
                continue
            self.estado.setdefault("preguntas_hechas", []).append(pid)
            return {
                "tipo": "preguntar",
                "hipotesis": hip,
                "plan": plan,
                "pregunta_id": pid,
                "texto": self._texto_pregunta(pid),
            }

        self.estado["etapa"] = "diagnosticado"
        return {
            "tipo": "diagnostico",
            "hipotesis": hip,
            "plan": plan,
        }

    def _texto_pregunta(self, pid: str) -> str:
        mapa = {
            "es_laptop": "¿Es portátil (laptop) o PC de escritorio? (laptop/pc/no_sabe)",
            "conectado_a_corriente": "¿Está conectado a corriente/adaptador en este momento? (si/no/no_sabe)",
            "encienden_leds": "¿Se encienden algún LED (alimentación) al intentar encenderlo? (si/no/no_sabe)",
            "gira_ventilador": "¿Gira el ventilador cuando intentas encenderlo? (si/no/no_sabe)",
            "enciende": "¿Enciende el equipo al pulsar el botón? (si/no/no_sabe)",
            "se_ve_logo_bios": "¿Llegas a ver el logo del fabricante/BIOS aunque sea un instante? (si/no/no_sabe)",
            "probo_pantalla_externa": "¿Has probado ya con pantalla externa (HDMI/VGA)? (si/no/no_sabe)",
            "llega_a_so": "¿Consigue llegar al escritorio del sistema operativo? (si/no/no_sabe)",
            "aparece_bsod": "¿Aparece alguna pantalla azul (BSOD)? (si/no/no_sabe)",
            "codigo_error": "¿Qué código/error muestra la pantalla azul, si lo recuerdas?",
            "detecta_disco_bios": "¿Aparece el disco duro/SSD detectado en BIOS? (si/no/no_sabe)",
            "intento_reparacion_arranque": "¿Has intentado reparación de arranque (recuperación/USB)? (si/no/no_sabe)",
            "enciende_led_carga": "¿Se ilumina el LED de carga al conectar el adaptador? (si/no/no_sabe)",
            "bateria_extraible": "¿La batería es extraíble? (si/no/no_sabe)",
            "se_apaga_solo": "¿Se apaga solo tras calentarse un rato? (si/no/no_sabe)",
            "ruido_ventilador": "¿Hace mucho ruido el ventilador? (si/no/no_sabe)",
            "bloquea_respira": "¿Lo usas sobre una superficie que pueda bloquear los respiraderos? (si/no/no_sabe)",
            "tipo_ruido": "¿Qué tipo de ruido es: clics, zumbido o chirrido? (descríbelo o no_sabe)",
            "hay_datos_importantes": "¿Hay datos importantes sin copia de seguridad? (si/no/no_sabe)",
            "arranca_so": "¿Sigue arrancando el sistema operativo normalmente? (si/no/no_sabe)",
            "es_hdd_o_ssd": "¿Sabes si el disco es HDD o SSD? (hdd/ssd/no_sabe)",
            "muchos_programas_inicio": "¿Notas que tarda mucho desde que enciende hasta el escritorio? (si/no/no_sabe)",
            "disco_lleno": "¿Tienes poco espacio libre en disco? (si/no/no_sabe)",
            "funciona_otro_dispositivo": "¿Funciona WiFi con otro dispositivo en la misma red? (si/no/no_sabe)",
            "detecta_redes": "¿Detecta redes WiFi aunque no consiga conectarse? (si/no/no_sabe)",
            "error_conexion": "¿Qué mensaje de error aparece al intentar conectarse?",
            "sale_por_auriculares": "¿Suena por auriculares pero NO por altavoces (o al revés)? (si/no/no_sabe)",
            "silenciado": "¿Has comprobado que no esté silenciado? (si/no/no_sabe)",
            "detecta_dispositivo": "¿Aparece el altavoz en Dispositivos de sonido? (si/no/no_sabe)",
        }
        return mapa.get(pid, f"Cuéntame un poco más sobre: {pid}")
